"""Publish newly inventoried articles through Buffer; no third-party packages."""
import argparse
from datetime import date, datetime, timezone
import json
import os
from pathlib import Path
import subprocess
from urllib.request import Request, urlopen
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / 'data/twitter-ledger.json'
HOSTS = {'El Debate': 'www.eldebate.com', 'Zenda': 'www.zendalibros.com'}

def articles():
    return {a['url']: a for a in json.loads((ROOT / 'data/inventory.json').read_text())['articles']
            if a['publication'] in HOSTS and urlsplit(a['url']).hostname == HOSTS[a['publication']]}

def message(article):
    return f"Nuevo artículo en {article['publication']}:\n{article['url']}"

def save(state, persist=False):
    LEDGER.write_text(json.dumps(state, ensure_ascii=False, indent=2) + '\n')
    if persist:
        subprocess.run(['git', 'add', str(LEDGER)], check=True)
        if subprocess.run(['git', 'diff', '--cached', '--quiet']).returncode:
            subprocess.run(['git', 'commit', '-m', 'Record Buffer article publishing state'], check=True)
            subprocess.run(['git', 'push'], check=True)

def api(query):
    key = os.environ.get('BUFFER_API_KEY')
    if not key:
        raise RuntimeError('BUFFER_API_KEY secret is missing')
    request = Request('https://api.buffer.com', data=json.dumps({'query': query}).encode(),
                      headers={'Content-Type': 'application/json', 'Authorization': 'Bearer ' + key})
    # Never blindly retry a mutation: a timeout may follow a successful creation.
    with urlopen(request, timeout=45) as response:
        result = json.load(response)
    if result.get('errors'):
        raise RuntimeError('Buffer GraphQL request failed; inspect API permissions/schema')
    return result['data']

def check_connection(channel):
    expiry = os.environ.get('BUFFER_KEY_EXPIRES_AT')
    if expiry and (date.fromisoformat(expiry) - datetime.now(timezone.utc).date()).days <= 0:
        raise RuntimeError('Buffer key has expired. Renew the key and GitHub secret to keep X publishing active.')
    account = api('query {account {organizations {id}}}')
    matched = []
    for org in account['account']['organizations']:
        channels = api('query {channels(input: {organizationId: ' + json.dumps(org['id'])
                       + '}) {id name service isDisconnected isLocked isQueuePaused}}')['channels']
        matched.extend((org['id'], c) for c in channels if c['id'] == channel)
    if len(matched) != 1:
        raise RuntimeError('Configured Buffer channel was not uniquely found')
    org, c = matched[0]
    if c['service'] != 'twitter' or c['name'].lstrip('@') != 'ferariza_' or any(
            c[k] for k in ('isDisconnected', 'isLocked', 'isQueuePaused')):
        raise RuntimeError('ferariza_ X channel is unavailable for automatic publishing')
    return org


def existing_posts(org, channel):
    cursor = None
    posts = []
    while True:
        after = ', after: ' + json.dumps(cursor) if cursor else ''
        query = ('query { posts(first: 100' + after + ', input: {organizationId: ' + json.dumps(org)
                 + ', filter: {channelIds: [' + json.dumps(channel) + ']}}) '
                 '{edges {node {id text status}} pageInfo {hasNextPage endCursor}}}')
        page = api(query)['posts']
        posts.extend(edge['node'] for edge in page['edges'])
        if not page['pageInfo']['hasNextPage']:
            return posts
        next_cursor = page['pageInfo']['endCursor']
        if not next_cursor or next_cursor == cursor:
            raise RuntimeError('Invalid Buffer pagination')
        cursor = next_cursor

def publish(state, inventory, channel, persist=False):
    pending = [url for url in inventory if url not in state['articles'] or
               state['articles'][url]['status'] in ('attempting', 'retry')]
    if not pending:
        print('No new articles to publish; historical baseline excluded.')
        return
    org = check_connection(channel)
    posts = existing_posts(org, channel)
    for url in sorted(pending, key=lambda u: (inventory[u]['date'], u)):
        text = message(inventory[url])
        matches = [p for p in posts if p['text'] == text or url in (p['text'] or '')]
        if matches:
            p = matches[0]
            state['articles'][url] = {'status': 'submitted', 'bufferPostId': p['id']}
            save(state, persist)
            if p['status'] == 'error':
                raise RuntimeError('Existing Buffer post failed delivery; resolve it in Buffer without creating a duplicate')
            continue
        if state['articles'].get(url, {}).get('status') == 'attempting':
            raise RuntimeError('Uncertain previous Buffer response: no matching post found. Inspect Buffer before retrying to prevent duplicates')
        state['articles'][url] = {'status': 'attempting'}
        save(state, persist)  # Persist intent before the external side effect.
        query = ('mutation {createPost(input: {channelId: ' + json.dumps(channel)
                 + ', text: ' + json.dumps(text) + ', schedulingType: automatic, mode: shareNow, '
                 'assets: [], needsApproval: false, saveToDraft: false}) '
                 '{... on PostActionSuccess {post {id}} ... on MutationError {message}}}')
        result = api(query)['createPost']
        if not result.get('post', {}).get('id'):
            state['articles'][url] = {'status': 'retry'}
            save(state, persist)
            raise RuntimeError('Buffer rejected post; retry on next successful daily run')
        state['articles'][url] = {'status': 'submitted', 'bufferPostId': result['post']['id']}
        save(state, persist)
        print('Submitted new article to Buffer.')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--baseline', action='store_true')
    parser.add_argument('--publish', action='store_true')
    parser.add_argument('--persist', action='store_true')
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    if args.check:
        org = check_connection(os.environ['BUFFER_CHANNEL_ID'])
        posts = existing_posts(org, os.environ['BUFFER_CHANNEL_ID'])
        if any(p['status'] == 'error' for p in posts):
            raise RuntimeError('Buffer reports a failed X post. Inspect and retry it in Buffer.')
        print('Buffer credential, ferariza_ channel and post-reading checks passed.')
        return
    inventory = articles()
    if args.baseline:
        if LEDGER.exists():
            raise RuntimeError('Baseline already exists; refusing to erase publishing history')
        save({'version': 1, 'baselineAt': datetime.now(timezone.utc).isoformat(),
              'articles': {url: {'status': 'baseline'} for url in sorted(inventory)}})
        print(f'Excluded {len(inventory)} historical articles.')
        return
    state = json.loads(LEDGER.read_text())
    if args.publish:
        if os.environ.get('TWITTER_UPDATES_ENABLED') != 'true':
            print('X publishing disabled.')
            return
        publish(state, inventory, os.environ['BUFFER_CHANNEL_ID'], args.persist)
    else:
        print(f"New articles eligible for X: {sum(u not in state['articles'] for u in inventory)}")

if __name__ == '__main__':
    main()
