"""Release checks for canonicalization, markup and public discovery files."""
from pathlib import Path
import json
import subprocess
import sys
import unittest
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from seo import metadata, SITE
ROOT = Path(__file__).resolve().parents[1]

class Head(HTMLParser):
    def __init__(self, text):
        super().__init__();self.tags=[];self.feed(text)
    def handle_starttag(self,tag,attrs):self.tags.append((tag,dict(attrs)))

class SearchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        subprocess.run([sys.executable,str(ROOT/'scripts/build.py')],check=True,capture_output=True)
        subprocess.run([sys.executable,str(ROOT/'scripts/prepare-pages.py')],check=True,capture_output=True)
        cls.out=ROOT.parent/'_site'
        cls.page=(cls.out/'index.html').read_text()
        cls.tags=Head(cls.page).tags
    def test_preview_and_production_index_controls(self):
        self.assertIn('noindex,follow',(ROOT/'index.html').read_text())
        self.assertNotIn('noindex',self.page)
        canon=[a['href'] for t,a in self.tags if t=='link' and a.get('rel')=='canonical']
        self.assertEqual(canon,[SITE])
    def test_sitemap_only_canonical_home(self):
        doc=ET.fromstring((self.out/'sitemap.xml').read_text())
        self.assertEqual([n.text for n in doc.findall('.//{*}loc')],[SITE])
        self.assertIn('Sitemap: '+SITE+'sitemap.xml',(self.out/'robots.txt').read_text())
    def test_structured_data_matches_inventory(self):
        data=json.loads((ROOT/'data/inventory.json').read_text())
        fragment=metadata(data).split('<script type="application/ld+json">')[1].split('</script>')[0]
        graph=json.loads(fragment)['@graph']
        items={n['@id']:n for n in graph}
        self.assertEqual(len(items),len(graph))
        for w in data['works']:
            entry=items[SITE+'#obra-'+w['id']]
            self.assertEqual(entry['name'],w['title'])
            self.assertIn('id="obra-'+w['id']+'"',self.page)
        self.assertNotIn('author',items[SITE+'#obra-delibes'])
        self.assertNotIn('author',items[SITE+'#obra-macrae'])
    def test_assets_exist_and_build_internals_not_published(self):
        for tag,attrs in self.tags:
            for key in ['src','href']:
                value=attrs.get(key,'')
                if value and not value.startswith(('https:','http:','mailto:','#')):
                    self.assertTrue((self.out/value).is_file(),value)
        self.assertFalse((self.out/'research').exists())
        self.assertFalse((self.out/'data').exists())
    def test_legacy_destinations_and_noindex_404(self):
        for file,fragment in [('fernando.html','#autor'),('ciudad-dormida.html','#libro-ciudad-dormida'),('fuiste-el-rey.html','#libro-fuiste-el-rey')]:
            content=(self.out/file).read_text()
            self.assertIn('content="0;url='+SITE+fragment,content)
        self.assertIn('location.hash',(self.out/'modern-design/index.html').read_text())
        self.assertIn('content="noindex"',(self.out/'404.html').read_text())

if __name__=='__main__': unittest.main()
