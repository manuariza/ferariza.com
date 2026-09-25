"""Daily, additive press refresh. Standard library + curl; default is a dry run."""
import argparse
import csv
from datetime import date, datetime, timezone
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import subprocess
import tempfile
import time
from urllib.parse import urljoin, urlsplit, urlunsplit

ROOT = Path(__file__).resolve().parents[1]
SOURCES = {
    'El Debate': 'https://www.eldebate.com/autor/fernando-ariza/',
    'Zenda': 'https://www.zendalibros.com/author/fernandoariza/',
}
MONTHS = dict(zip('ene feb mar abr may jun jul ago sep oct nov dic'.split(), range(1, 13)))

class Node:
    def __init__(self, tag='', attrs=(), parent=None):
        self.tag, self.attrs, self.parent, self.children = tag, dict(attrs), parent, []
    def text(self):
        return ' '.join(''.join(c if isinstance(c, str) else c.text() + ' ' for c in self.children).split())
    def all(self, tag=None):
        for c in self.children:
            if isinstance(c, Node):
                if tag is None or c.tag == tag:
                    yield c
                yield from c.all(tag)
    def has_class(self, name):
        return name in self.attrs.get('class', '').split()

class Document(HTMLParser):
    def __init__(self, html):
        super().__init__(convert_charrefs=True)
        self.root = self.current = Node()
        self.feed(html)
    def handle_starttag(self, tag, attrs):
        node = Node(tag, attrs, self.current)
        self.current.children.append(node)
        if tag not in {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}:
            self.current = node
    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        self.handle_endtag(tag)
    def handle_endtag(self, tag):
        node = self.current
        while node.parent:
            if node.tag == tag:
                self.current = node.parent
                return
            node = node.parent
    def handle_data(self, data):
        self.current.children.append(data)


def canonical_url(url):
    parts = urlsplit(url)
    if parts.scheme not in ('https', 'http') or parts.username or parts.password:
        raise ValueError('Invalid article URL')
    return urlunsplit(('https', parts.netloc.lower(), parts.path.rstrip('/') + ('/' if not parts.path.endswith('.html') else ''), '', ''))


def fetch(url):
    # Only configured public publisher hosts are requested. No browser session or credentials.
    if urlsplit(url).hostname not in {urlsplit(u).hostname for u in SOURCES.values()}:
        raise ValueError('Unexpected publisher host')
    result = subprocess.run(['curl', '--fail', '--silent', '--show-error', '--location',
                             '--proto', '=https', '--proto-redir', '=https', '--max-time', '30',
                             '--retry', '2', '--retry-delay', '2', '--max-filesize', '10000000',
                             '--user-agent', 'FernandoArizaSite/1.0 (+https://ferariza.com)', url],
                            capture_output=True, check=True)
    time.sleep(.3)
    return result.stdout.decode('utf-8', errors='replace')


def archive_links(html, publication):
    root = Document(html).root
    base = SOURCES[publication]
    cls = 'c-article__title' if publication == 'El Debate' else 'gdlr-blog-title'
    links = {}
    for heading in root.all():
        if heading.has_class(cls):
            for a in heading.all('a'):
                url = canonical_url(urljoin(base, a.attrs.get('href', '')))
                if urlsplit(url).hostname == urlsplit(base).hostname and a.text():
                    links[url] = a.text()
    if not links:
        raise ValueError(f'{publication}: no article headings found; refusing an empty scrape')
    pattern = re.escape(base) + (r'\d+/' if publication == 'El Debate' else r'page/\d+/')
    pages = {canonical_url(urljoin(base, a.attrs.get('href',''))) for a in root.all('a')
             if re.fullmatch(pattern, urljoin(base, a.attrs.get('href','')))}
    return links, pages


def parse_article(html, url, publication):
    root = Document(html).root
    meta = {n.attrs.get('name', n.attrs.get('property','')): n.attrs.get('content','') for n in root.all('meta')}
    if meta.get('author', '').strip().casefold() != 'fernando ariza':
        raise ValueError(f'Authorship not verified: {url}')
    canonical = next((n.attrs.get('href') for n in root.all('link') if n.attrs.get('rel') == 'canonical'), None)
    if not canonical:
        raise ValueError(f'Missing canonical URL: {url}')
    canonical = canonical_url(urljoin(url, canonical))
    if urlsplit(canonical).hostname != urlsplit(SOURCES[publication]).hostname:
        raise ValueError('Canonical points outside publisher')
    title = next((n.text() for n in root.all('h1') if n.text()), '')
    if not title or len(title) > 500:
        raise ValueError(f'Missing or invalid title: {url}')
    if publication == 'Zenda':
        label = next((n.text() for n in root.all() if n.has_class('blog-date')), '')
        match = re.search(r'(\d{1,2})\s+(\w+)\s+(\d{4})', label)
        if not match or match[2].lower()[:3] not in MONTHS:
            raise ValueError(f'Missing visible publication date: {url}')
        published = date(int(match[3]), MONTHS[match[2].lower()[:3]], int(match[1]))
    else:
        label = next((n.attrs.get('datetime','') for n in root.all('time') if n.attrs.get('datetime')), '')
        published = date.fromisoformat(label[:10])
    if published > datetime.now(timezone.utc).date() or published.year < 1995:
        raise ValueError(f'Invalid publication date: {url}')
    return {'id': urlsplit(canonical).path.rstrip('/').split('/')[-1].removesuffix('.html'),
            'title': title, 'publication': publication, 'date': published.isoformat(),
            'url': canonical, 'source': SOURCES[publication], 'dateSource': canonical,
            'dateEvidence': label, 'authorshipEvidence': 'Publisher author metadata: Fernando Ariza',
            'retrievedAt': datetime.now(timezone.utc).date().isoformat(), 'featured': False}


def collect(existing, get=fetch):
    known = {canonical_url(a['url']) for a in existing}
    additions, counts = [], {}
    for publication, base in SOURCES.items():
        pending, visited, discovered = [base], set(), {}
        while pending:
            url = pending.pop(0)
            if url in visited:
                continue
            if len(visited) >= 30:
                raise ValueError('Archive pagination exceeds limit; needs review')
            visited.add(url)
            links, pages = archive_links(get(url), publication)
            discovered.update(links)
            pending.extend(sorted(pages - visited))
        counts[publication] = {'pages': len(visited), 'articles': len(discovered)}
        # Detect broken pagination/partial responses before accepting a successful refresh.
        previous = {canonical_url(a['url']) for a in existing if a['publication'] == publication}
        if previous and len(previous.intersection(discovered)) < len(previous) * .8:
            raise ValueError(f'{publication}: archive coverage fell below 80%; needs review')
        for url in sorted(discovered):
            if url in known:
                continue
            article = parse_article(get(url), url, publication)
            if article['url'] not in known:
                additions.append(article)
                known.add(article['url'])
            known.add(url)
    return additions, counts


def atomic_write(path, text):
    with tempfile.NamedTemporaryFile('w', dir=path.parent, delete=False, encoding='utf-8') as f:
        f.write(text)
        temp = Path(f.name)
    temp.replace(path)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true', help='Persist validated additions; otherwise dry run')
    args = parser.parse_args()
    path = ROOT / 'data/inventory.json'
    data = json.loads(path.read_text())
    additions, coverage = collect(data['articles'])
    print(json.dumps({'newArticles': additions, 'coverage': coverage}, ensure_ascii=False, indent=2))
    if args.write and additions:
        data['articles'] = sorted(data['articles'] + additions, key=lambda a:(a['date'], a['title']), reverse=True)
        ids = [a['id'] for a in data['articles']]
        if len(ids) != len(set(ids)):
            raise ValueError('Article ID collision; needs review')
        atomic_write(path, json.dumps(data, ensure_ascii=False, indent=2) + '\n')
        rows = data['articles']
        with (ROOT/'data/articles.csv').open('w') as f:
            writer = csv.DictWriter(f, fieldnames=list(dict.fromkeys(k for a in rows for k in a)))
            writer.writeheader()
            writer.writerows(rows)

if __name__ == '__main__':
    main()
