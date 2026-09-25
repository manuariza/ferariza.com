"""Enrich missing press dates from public article metadata; no article text is copied."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import subprocess,json,re
from bs4 import BeautifulSoup
R=Path(__file__).resolve().parents[1]
d=json.loads((R/'data/inventory.json').read_text())
def enrich(a):
 if a['date'] and (a['publication']!='Zenda' or a.get('dateEvidence')):return a
 r=subprocess.run(['curl','-sSL','--fail','--max-time','20',a['url']],capture_output=True)
 if r.returncode:return a
 s=BeautifulSoup(r.stdout,'html.parser')
 date=s.select_one('meta[property="article:published_time"]')
 if a['publication']=='Zenda':
  visible=s.select_one('.blog-date')
  match=re.search(r'(\d+)\s+(\w+)\s+(\d{4})',visible.get_text(' ',strip=True)) if visible else None
  months={'ene':1,'feb':2,'mar':3,'abr':4,'may':5,'jun':6,'jul':7,'ago':8,'sep':9,'oct':10,'nov':11,'dic':12}
  if match:
   a['date']=f'{match[3]}-{months[match[2].lower()[:3]]:02}-{int(match[1]):02}'
   a['dateEvidence']=visible.get_text(' ',strip=True);a['dateSource']=a['url']
 elif date:a['date']=date.get('content','')[:10];a['dateSource']=a['url']
 desc=s.select_one('meta[property="og:description"]');image=s.select_one('meta[property="og:image"]')
 if desc:a['sourceDescription']=desc.get('content')
 if image:a['sourceImage']=image.get('content')
 return a
with ThreadPoolExecutor(max_workers=3) as pool:d['articles']=list(pool.map(enrich,d['articles']))
(R/'data/inventory.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
print('Dated records:',sum(bool(a['date']) for a in d['articles']),'of',len(d['articles']))
