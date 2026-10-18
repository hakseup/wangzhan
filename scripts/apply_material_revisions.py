"""Publish checked PDF text/layout revisions; preserve originals and provenance."""
import collections,hashlib,json,re,sys,unicodedata
from pathlib import Path
sys.path.insert(0,'/workspace/tooling/python')
from wordfreq import zipf_frequency
ROOT=Path(__file__).resolve().parents[1]
def norm(s):return re.sub('[^a-z0-9]','',unicodedata.normalize('NFD',s.lower()).encode('ascii','ignore').decode())
ANCHORS={
'2021-10-fr':'Congé paternité','2021-3-cn':'Les animaux','2021-5-cn':'Internet permet','2022-11-cn':'évolution de la population','2022-3-cn':'Jeux vidéo','2022-6-cn':'Le bilinguisme','2023-10-fr':'Quelles réalités','2023-11-cn':"Les fautes d'orthographe",'2023-3-cn':'Nourrir la planète','2023-6-cn':'Quand les machines','2024-11-af':'Rendre les','2024-11-cn':'Publicité sur les','2024-3-fr':"essor de l'économie",'2024-5-fr':'Nous ne prendrons','2024-6-cn':'Éducation','2025-11-cn':'Éduquer','2025-3-cn':'Nutrition végane','2025-6-cn':"avenir de l'automobile",'2025-8-fr':'De nouvelles stratégies','2026-3-cn':'Et si on','2026-6-cn':'Manger sainement','extra-1':'Le mouvement','extra-2':'Les béquilles','extra-3':'Vegan','extra-4':'De plus en plus jeunes','extra-5':'Pourquoi les femmes','extra-6':'Aller au travail','extra-7':'préseniol'}
TITLE_FIX={
'2021-3-cn':'Les animaux et nous','2022-11-cn':"L’évolution de la population mondiale",'2022-3-cn':'Jeux vidéo : savoir revenir du virtuel au réel','2022-6-cn':'Le bilinguisme sculpte le cerveau','2023-11-cn':"Les fautes d’orthographe diminuent les chances d’être recruté",'2023-3-cn':"Nourrir la planète en 2050, un défi déjà d’actualité",'2023-6-cn':'Quand les machines remplaceront les hommes','2024-11-af':'Rendre les zoos plus éthiques, est-ce vraiment possible ?','2024-11-cn':'Publicité sur les trottoirs : une initiative discutée','2024-3-fr':"L’essor de l’économie collaborative : moins d’hyperconsommation, plus de partage",'2024-6-cn':'Éducation : et si les devoirs à la maison disparaissaient ?','2025-11-cn':'Éduquer ? Mission impossible !','2025-3-cn':'Nutrition végane et avantages','2025-6-cn':"L’avenir de l’automobile : triomphe ou déclin ?",'2026-3-cn':'Et si on lâchait la bride à nos enfants ?','extra-7':'Cours en présentiel ou à distance : une rentrée hybride'}
PAGES=collections.defaultdict(list)
for f in (ROOT/'data/revised-pages').glob('*.json'):
 d=json.loads(f.read_text());PAGES[d['file']].append(d)
for ps in PAGES.values():ps.sort(key=lambda d:d['page'])
bank=json.loads((ROOT/'public/content.json').read_text())['exercises']
manual=json.loads((ROOT/'data/material-corrections.json').read_text()) if (ROOT/'data/material-corrections.json').exists()else{}
existing_tasks=json.loads((ROOT/'data/writing-tasks.json').read_text())
report={'sourcePages':sum(map(len,PAGES.values())),'exercises':[],'removedScanArtifacts':0}

def clean(t,native=False):
 t=re.sub('[\u3400-\u9fff\ufffd\u2e80-\u2fff]','',t)
 t=t.replace('҉','fi').replace('|',' ').replace('_',' ').replace('\\',' ')
 t=re.sub(r'\s+',' ',t).strip()
 if re.search(r'(?:RÉSERVÉ AU|ÉPREUVES COLLECT|DELF\s*DALF|LETTRES ET SCIENCES|Règle de décompte|[\w-]+/public/fichiers|DOCUMENT.{0,45}(?:NEUVES|C4A|CAYWD|COLLECTIVE))',t,re.I):return ''
 if not re.search('[A-Za-zÀ-ÿœŒ]{2}',t):return ''
 t=re.sub(r'^[^A-Za-zÀ-ÿœŒ«“\[(*–—\-]+','',t)
 t=re.sub(r'(?<!\w)(?:[A-Z]{2,}\s+){3,}[A-Z]{2,}(?!\w)','',t)
 for a,b in {'zo0s':'zoos','z00s':'zoos','€n apparence':'en apparence','biologie°':'biologie','Fautil':'Faut-il','fean-Pierre':'Jean-Pierre','Bristish':'British'}.items():t=t.replace(a,b)
 t=re.sub(r'\s+([,.;:!?])',r'\1',t)
 t=re.sub(r'\s+',' ',t).strip()
 if len(t)<4:return ''
 if not native:
  words=re.findall('[A-Za-zÀ-ÿœŒ]{2,}',t)
  if len(words)>3 and sum(zipf_frequency(w.lower(),'fr')>=2 for w in words)/len(words)<.35:
   report['removedScanArtifacts']+=1;return ''
 return t

def reflow(paras):
 result=[]
 for p in paras:
  p=dict(p);p['fr']=clean(p['fr'],p['extractionMethod']=='native-repaired')
  if not p['fr']:continue
  if p['extractionMethod'].startswith('ocr') and p['role']=='heading' and not p.get('confirmedHeading'):p['role']='body'
  doc=re.match(r'^[>»\s]*(?:J?DOCUMENT)\s*[-:]?\s*(?:n[°o]?\s*)?([12])\b\s*[:.\-]?(.*)',p['fr'],re.I)
  if doc:
   result.append({**p,'fr':'DOCUMENT '+doc[1],'role':'document'})
   trailing=doc[2].strip()
   if len(trailing)>15 and re.search('[a-zà-ÿ]{3}',trailing):result.append({**p,'fr':trailing,'role':'heading'})
   continue
  if p['role']=='body' and result and result[-1]['role']=='body':
   prev=result[-1]['fr']
   if (not re.search(r'[.!?:;»”\]]$',prev)) or re.match('[a-zà-ÿœ]',p['fr']):
    result[-1]['fr']+=('' if prev.endswith('-')else ' ')+p['fr'];continue
  result.append(p)
 return result

revisions={}
for e in bank:
 if e['category']not in ['writing','speaking']:continue
 source=e['sourceFiles'][0];ps=PAGES[source]
 if e['category']=='speaking':
  _,series,index=e['id'].split('-');ps=ps[(int(index)-1)*2:int(index)*2]
 all_paras=[dict(p)for page in ps for p in page['paragraphs']]
 if e['category']=='writing':
  key=e['id'][8:];anchor=norm(ANCHORS[key]);start=next((i for i,p in enumerate(all_paras)if anchor in norm(p['fr'])),None)
  if start is None:raise ValueError('Missing source title anchor: '+e['id'])
  materials=[dict(p) for p in all_paras[start:]]
  materials[0]['confirmedHeading']=True
  if key in TITLE_FIX:materials[0]={**materials[0],'fr':TITLE_FIX[key],'role':'heading'}
  end=next((i for i,p in enumerate(materials)if re.search(r'(?:ÉPREUVE|EPREUVE|EXERCICE)\s*N?[°o]?\s*2|Essai\s*argument[ée]|^SYNTHÈSE\s*:',p['fr'],re.I)),None)
  if end is not None:materials=materials[:end]
  elif key in ['2021-10-fr','2021-3-cn','2022-3-cn','2022-6-cn','2025-8-fr']:
   pattern={'2021-10-fr':r'^Vous écrivez','2021-3-cn':r'^Une revue','2022-3-cn':r'^Tout en reconnaissant','2022-6-cn':r'^Vous avez lu','2025-8-fr':r'^Vous avez lu'}[key]
   end=next((i for i,p in enumerate(materials)if re.search(pattern,p['fr'],re.I)),None)
   if end is not None:materials=materials[:end]
  expected=manual.get(e['id'],{}).get('tasks',e.get('tasks',[]))
  prefixes=[norm(t['fr'])[:28]for t in expected if len(t['fr'])>60]
  tail=next((i for i,p in enumerate(materials)if i>2 and any(norm(clean(p['fr'])).startswith(prefix)for prefix in prefixes)),None)
  if tail is not None:materials=materials[:tail]
  if key in TITLE_FIX:
   materials=[p for i,p in enumerate(materials)if i==0 or not(len(norm(p['fr']))<40 and norm(p['fr'])in norm(TITLE_FIX[key]))]
  materials=reflow(materials)
  if materials:materials[0]['role']='heading' if len(materials[0]['fr'])<240 else 'body'
  for p in materials:
   if p['role']=='heading'and len(p['fr'])>300:p['role']='body'
  # Recover the original essay prompt separately from the source articles.
  tasks=[]
  task_at=next((i+1 for i,p in enumerate(all_paras)if re.search(r'Essai\s*argument[ée]',p['fr'],re.I)),None)
  if task_at is None:
   for i,p in enumerate(all_paras):
    if i>len(all_paras)*.65 and re.match(r'^(?:Vous (?:écrivez|avez lu)|Une revue|Tout en reconnaissant)',p['fr'],re.I):task_at=i;break
  if task_at is not None:
   task=[]
   for p in all_paras[task_at:]:
    if re.search(r'\d{3}\s*mots?\s*minimum|^DOCUMENT\s*[12]',p['fr'],re.I):break
    t=clean(p['fr'])
    if t:task.append(t)
   text=' '.join(task)
   if len(text)>80:tasks=[{'id':'essai','fr':text,'zh':'按法语原题指定的身份、对象和要求展开论证；词数以原题为准。','minWords':240 if '240 mots minimum'in' '.join(p['fr']for p in all_paras[task_at:task_at+5])else 250}]
  if e['id']in existing_tasks:tasks=[existing_tasks[e['id']]]
  patch={'paragraphs':materials,'materialRevision':'pdf-rechecked-2026-10-17','tasks':tasks}
 else:
  patch={'paragraphs':reflow(all_paras),'materialRevision':'pdf-rechecked-2026-10-17'}
 if e['id']in manual:patch.update(manual[e['id']])
 seen=collections.Counter()
 for p in patch['paragraphs']:
  digest=hashlib.sha256(p['fr'].encode()).hexdigest()[:14];seen[digest]+=1
  p['id']='r-'+digest+('-'+str(seen[digest])if seen[digest]>1 else '')
  p.setdefault('sourcePage',1)
  p.setdefault('extractionMethod','manually-checked-against-pdf')
 revisions[e['id']]=patch
 report['exercises'].append({'id':e['id'],'paragraphsBefore':len(e['paragraphs']),'paragraphsAfter':len(patch['paragraphs']),'charactersBefore':sum(len(p['fr'])for p in e['paragraphs']),'charactersAfter':sum(len(p['fr'])for p in patch['paragraphs'])})
(ROOT/'data/material-revisions.json').write_text(json.dumps(revisions,ensure_ascii=False,separators=(',',':')))
(ROOT/'data/material-revision-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print('Prepared',len(revisions),'exercise revisions from',report['sourcePages'],'pages.')
