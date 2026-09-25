"""Focused regression checks for unattended publication, no third-party packages."""
import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location('updater', Path(__file__).with_name('update-articles.py'))
u = importlib.util.module_from_spec(spec)
spec.loader.exec_module(u)

class ArticleRefreshTests(unittest.TestCase):
    def article(self, author='Fernando Ariza', canonical='https://www.zendalibros.com/example/'):
        return f'''<html><head><link rel="canonical" href="{canonical}"><meta name="author" content="{author}"><meta property="article:published_time" content="2024-08-29T23:44:00Z"></head><body><h1>Un título &amp; una lectura</h1><div class="blog-date"><a>30 Ago 2024</a></div><div class="blog-date">25 Sep 2026</div></body></html>'''
    def test_visible_date_overrides_utc_and_related_articles(self):
        a = u.parse_article(self.article(), 'https://www.zendalibros.com/example/', 'Zenda')
        self.assertEqual(a['date'], '2024-08-30')
        self.assertEqual(a['title'], 'Un título & una lectura')
        self.assertFalse(a['featured'])
    def test_wrong_author_rejected(self):
        with self.assertRaises(ValueError):
            u.parse_article(self.article(author='Another writer'), 'https://www.zendalibros.com/example/', 'Zenda')
    def test_wrong_canonical_host_rejected(self):
        with self.assertRaises(ValueError):
            u.parse_article(self.article(canonical='https://example.org/'), 'https://www.zendalibros.com/example/', 'Zenda')
    def test_local_debate_date(self):
        html = '<meta name="author" content="Fernando Ariza"><link rel="canonical" href="https://www.eldebate.com/example.html"><h1>Una lectura</h1><time datetime="2024-08-30T00:30:00+02:00">30 ago.</time>'
        self.assertEqual(u.parse_article(html, 'https://www.eldebate.com/example.html', 'El Debate')['date'], '2024-08-30')
    def test_empty_or_changed_archive_rejected(self):
        with self.assertRaises(ValueError): u.archive_links('<h1>Access denied</h1>', 'Zenda')
    def test_pagination_and_tracking_deduplication(self):
        html = '<h3 class="gdlr-blog-title"><a href="/example/?utm_source=x">Title</a></h3><a href="/author/fernandoariza/page/2/">2</a>'
        links, pages = u.archive_links(html, 'Zenda')
        self.assertEqual(list(links), ['https://www.zendalibros.com/example/'])
        self.assertIn('https://www.zendalibros.com/author/fernandoariza/page/2/', pages)
    def test_repeat_run_preserves_curated_record(self):
        archives = {}
        existing = []
        for pub, base in u.SOURCES.items():
            url = base.replace('/autor/fernando-ariza/', '/existing.html').replace('/author/fernandoariza/', '/existing/')
            cls = 'c-article__title' if pub == 'El Debate' else 'gdlr-blog-title'
            archives[base] = f'<h2 class="{cls}"><a href="{url}">Existing</a></h2>'
            existing.append({'url':url, 'publication':pub, 'featured':True, 'title':'Edited title'})
        additions, counts = u.collect(existing, archives.__getitem__)
        self.assertEqual(additions, [])
        self.assertTrue(existing[0]['featured'])
        self.assertEqual(existing[0]['title'], 'Edited title')
    def test_partial_archive_is_failure(self):
        existing = [{'url':f'https://www.eldebate.com/{i}.html','publication':'El Debate'} for i in range(10)]
        with self.assertRaises(ValueError):
            u.collect(existing, lambda _: '<h2 class="c-article__title"><a href="/0.html">One</a></h2>')

if __name__ == '__main__': unittest.main()
