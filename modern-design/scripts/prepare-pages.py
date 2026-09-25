"""Stage public website and discovery files; exclude research and private build data."""
from pathlib import Path
import json
import shutil
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT.parent / '_site'
if OUT.exists():
    shutil.rmtree(OUT)
OUT.mkdir()
html = (ROOT/'index.html').read_text().replace('noindex,follow', 'index,follow,max-image-preview:large')
(OUT/'index.html').write_text(html)
for name in ['style.css', 'app.js', 'favicon.ico']:
    shutil.copy2(ROOT/name, OUT/name)
shutil.copytree(ROOT/'images', OUT/'images')
(OUT/'.nojekyll').touch()
(OUT/'robots.txt').write_text('User-agent: *\nAllow: /\n\nSitemap: https://ferariza.com/sitemap.xml\n')
# Only the canonical page belongs in the sitemap. Hashes are sections, not separate pages.
# Omit lastmod rather than pretend every scheduled build is a content change.
(OUT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n  <url><loc>https://ferariza.com/</loc></url>\n</urlset>\n')
(OUT/'llms.txt').write_text('''# Fernando Ariza

> Official website of Fernando Ariza, writer, literary critic and professor.

## Public website
- [Home](https://ferariza.com/): novels, essays, editions, biography and contact.
- [Works](https://ferariza.com/#indice): bibliographic records and links to publication sources.
- [Literary criticism](https://ferariza.com/#lecturas): dated links to articles on their original publishers’ websites.
- [Biography](https://ferariza.com/#autor)
- [Contact](https://ferariza.com/#contacto)
- [X profile](https://x.com/ferariza_)

This is an experimental navigation aid, not an indexing or ranking mechanism. Refer to the visible website and linked sources for factual information.
''')
def redirect(path, target, preserve_hash=False):
    full = 'https://ferariza.com/' + target
    script = '<script>location.replace("/" + location.hash);</script>' if preserve_hash else ''
    page = f'<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><link rel="canonical" href="https://ferariza.com/"><meta http-equiv="refresh" content="0;url={full}"><title>Fernando Ariza</title>{script}</head><body><a href="{full}">Fernando Ariza</a></body></html>'
    dest = OUT/path
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(page)
# GitHub Pages cannot configure native per-path 301s; immediate refresh is Google's
# supported permanent redirect fallback. A future edge layer can upgrade these to 301s.
redirect('fernando.html', '#autor')
redirect('ciudad-dormida.html', '#libro-ciudad-dormida')
redirect('fuiste-el-rey.html', '#libro-fuiste-el-rey')
redirect('modern-design/index.html', '', preserve_hash=True)
(OUT/'404.html').write_text('<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>Página no encontrada — Fernando Ariza</title></head><body><h1>Página no encontrada</h1><p><a href="/">Volver a Fernando Ariza</a></p></body></html>')
print('Staged public files in', OUT)
