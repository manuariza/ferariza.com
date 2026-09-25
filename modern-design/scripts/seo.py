"""Technical discovery metadata; no visible page content changes."""
import html
import json
from urllib.parse import urljoin

SITE = 'https://ferariza.com/'
DESCRIPTION = 'La obra de Fernando Ariza: novelas, biografías, ensayo, ediciones y crítica literaria.'

def metadata(data):
    person = {'@type':'Person','@id':SITE+'#person','name':'Fernando Ariza',
              'url':SITE+'#autor','image':SITE+'images/fernando.webp',
              'jobTitle':['Escritor','Profesor de Literatura','Crítico literario'],
              'worksFor':{'@type':'Organization','name':'Universidad CEU San Pablo'},
              'sameAs':['https://x.com/ferariza_']}
    graph = [person, {'@type':'WebSite','@id':SITE+'#website','url':SITE,'name':'Fernando Ariza',
                     'inLanguage':'es','publisher':{'@id':person['@id']}},
             {'@type':'WebPage','@id':SITE+'#webpage','url':SITE,
              'name':'Fernando Ariza — Literatura, ensayo y crítica','description':DESCRIPTION,
              'inLanguage':'es','isPartOf':{'@id':SITE+'#website'},'about':{'@id':person['@id']},
              'mainEntity':{'@id':SITE+'#bibliography'}}]
    items = []
    for i, w in enumerate(sorted(data['works'], key=lambda w:-w['year']), 1):
        work = {'@type':'CreativeWork' if w['category']=='Tesis' else 'Book',
                '@id':SITE+'#obra-'+w['id'],'url':SITE+'#obra-'+w['id'],
                'name':w['title'],'inLanguage':'es','description':w['description'],
                'image':urljoin(SITE,w['cover'])}
        # Never label an edition/coordinated volume as a solely authored book.
        if w['role']=='Autor' or w['role'].startswith('Coautor'):
            work['author'] = [{'@id':person['@id']}]
            if w['id']=='pensamiento': work['author'].append({'@type':'Person','name':'Miguel Herrero Herrero'})
        else:
            work['contributor'] = {'@id':person['@id']}
        if w['isbn'] and work['@type']=='Book':work['isbn']=w['isbn']
        if w['pages'] and work['@type']=='Book':work['numberOfPages']=w['pages']
        graph.append(work)
        items.append({'@type':'ListItem','position':i,'item':{'@id':work['@id']}})
    graph.append({'@type':'ItemList','@id':SITE+'#bibliography','name':'Obra de Fernando Ariza',
                  'numberOfItems':len(items),'itemListElement':items})
    encoded = json.dumps({'@context':'https://schema.org','@graph':graph},ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')
    values = {'og:type':'website','og:locale':'es_ES','og:site_name':'Fernando Ariza',
              'og:title':'Fernando Ariza — Literatura, ensayo y crítica','og:description':DESCRIPTION,
              'og:url':SITE,'og:image':SITE+'images/fernando.webp','og:image:alt':'Fernando Ariza',
              'og:image:width':'360','og:image:height':'440'}
    result = f'<link rel="canonical" href="{SITE}"><link rel="icon" href="favicon.ico">'
    result += ''.join(f'<meta property="{k}" content="{html.escape(v,quote=True)}">' for k,v in values.items())
    result += '<meta name="twitter:card" content="summary"><meta name="twitter:site" content="@ferariza_"><meta name="twitter:creator" content="@ferariza_">'
    result += f'<meta name="twitter:title" content="Fernando Ariza — Literatura, ensayo y crítica"><meta name="twitter:description" content="{DESCRIPTION}"><meta name="twitter:image" content="{SITE}images/fernando.webp"><meta name="twitter:image:alt" content="Fernando Ariza">'
    return result + f'<script type="application/ld+json">{encoded}</script>'
