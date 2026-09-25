"""Refresh public source snapshots and cover candidates. Uses system curl; no dependencies installed."""
import subprocess,json,re
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urljoin
ROOT=Path(__file__).resolve().parents[1]
sources={
'jekyll':'https://www.ceuediciones.es/catalogo/libros/critica-literaria/dualidad-y-sentido-etico-en-dr-jekyll-y-mr-hyde-guia-de-lectura/',
'pensamiento':'https://www.marcialpons.es/libros/el-pensamiento-narrativo/9788419661067/',
'puentes':'https://www.comares.com/libro/construyendo-puentes_150232/',
'debate':'https://www.eldebate.com/autor/fernando-ariza/',
'zenda':'https://www.zendalibros.com/author/fernandoariza/',
'becquer':'https://www.agapea.com/libros/Becquer-el-romantico-9788496751118-i.htm',
'valle':'https://www.agapea.com/libros/Valle-Inclan-el-bohemio-9788496751231-i.htm',
'camino':'https://www.agapea.com/libros/El-camino-Guia-de-Lectura-9788496634220-i.htm',
'delibes':'https://www.iberoamericana-vervuert.es/Libros/231977.pdf',
'zambrano':'https://www.comares.com/media/comares/files/toc-166568.pdf',
'baroja':'https://www.popularlibros.com/libro/pio-baroja-y-vicente-blasco-ibanez-_1697581',
}
manifest=[]
for key,url in sources.items():
 p=ROOT/'research'/(key+('.pdf' if '.pdf' in url else '.html'))
 r=subprocess.run(['curl','-sSL','--fail','--max-time','25',url,'-o',str(p)])
 if r.returncode: print(key,'failed');continue
 if p.suffix=='.pdf':continue
 s=BeautifulSoup(p.read_text(errors='replace'),'html.parser')
 og=s.select_one('meta[property="og:image"]');candidate=og.get('content') if og else None
 if key not in ['debate','zenda']:
  imgs=[(i.get('alt'),i.get('src')) for i in s.select('img') if any(w in (str(i.get('alt'))+' '+str(i.get('src'))).lower() for w in ['portada','978','979','jekyll','puentes'])]
  print(key, candidate,imgs[:5])
  manifest.append({'id':key,'source':url,'imageCandidate':candidate,'images':imgs[:5]})
(ROOT/'research'/'image-candidates.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
