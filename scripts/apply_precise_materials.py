"""Apply trace repairs; use two-pass consensus instead of replacing good scan text.
Changed paragraphs preserve source page; translations are reused only for exact
normalized text or minimal spelling/typography repairs, otherwise retranslated.
"""
import os,sys,json,re,glob,hashlib,unicodedata,collections,difflib
from pathlib import Path
sys.path.insert(0,'/workspace/work/python-refinements')
from wordfreq import zipf_frequency
from precise_materials import paragraphs,ordered,tidy
ROOT=Path(__file__).resolve().parents[1]
backup=Path('/workspace/work/pre-refinements-content.json')
if not backup.exists():backup.write_bytes((ROOT/'public/content.json').read_bytes())
bank=json.loads(backup.read_text());pages={}
for f in Path(os.environ.get('NOIX_PRECISE_PAGES','/workspace/work/precise-pages')).glob('*.json'):
 d=json.loads(f.read_text());pages[(d['file'],d['page'])]=d
norm=lambda s:re.sub(r'[^a-z0-9]','',unicodedata.normalize('NFD',s.lower()).encode('ascii','ignore').decode())
corrections=json.loads((ROOT/'data/translation-corrections.json').read_text());cache=json.loads((ROOT/'data/translations.json').read_text())
report={'sourcePages':len(pages),'changedParagraphs':0,'tracePages':0,'consensusPages':0,'translationReused':0,'newTranslations':0,'changes':[],'missingBoundaries':[],'unresolved':[]}
word_cache={}
def freq(w):
 if w not in word_cache:word_cache[w]=zipf_frequency(w,'fr')
 return word_cache[w]
def consensus(old,ocr):
 # Only replace invalid scan words when a second extraction supplies a close,
 # recognized spelling at the matching position. Preserve names and numbers.
 pat=r'[A-Za-zÀ-ÖØ-öø-ÿœŒ]+(?:[’\'-][A-Za-zÀ-ÖØ-öø-ÿœŒ]+)*';a=list(re.finditer(pat,old));b=list(re.finditer(pat,ocr));aa=[m.group().lower()for m in a];bb=[m.group().lower()for m in b];edits=[]
 for tag,i,j,k,l in difflib.SequenceMatcher(None,aa,bb,autojunk=False).get_opcodes():
  if tag!='replace' or j-i!=l-k or j-i>4:continue
  for x,y in zip(a[i:j],b[k:l]):
   before=x.group();after=y.group()
   if len(before)<4 or before[0].isupper() or after[0].isupper():continue
   ratio=difflib.SequenceMatcher(None,before.lower(),after.lower()).ratio()
   if ratio>=.65 and freq(before)<1.6 and freq(after)>3.2:edits.append((x.start(),x.end(),after))
 for start,end,text in reversed(edits):old=old[:start]+text+old[end:]
 return tidy(old)
def safe_text(ps):
 out=[]
 for p in ps:
  text=tidy(p['fr'])
  if not text or re.search(r'^(?:\d+\s+mots?\s*minimum|Règle de décompte|Exercice\s*2|ÉPREUVE\s*2)',text,re.I):continue
  if re.search(r'DELF.{0,5}DALF|FARE.*C1|www\..*/public/fichiers',text,re.I):continue
  doc=re.match(r'^[>»\s]*(?:DOCUMENT)\s*[-:]?\s*(?:n[°o]?\s*)?([12])\b\s*[:.\-]?(.*)',text,re.I)
  if doc:
   out.append({**p,'fr':'DOCUMENT '+doc[1],'role':'document'})
   if doc[2].strip():out.append({**p,'fr':doc[2].strip(),'role':'heading'})
  else:out.append({**p,'fr':text})
 return out
for e in bank['exercises']:
 if e['category']not in ['writing','speaking']:continue
 old=e['paragraphs'];new=[];seen=collections.Counter();by_page=collections.defaultdict(list)
 for p in old:by_page[p['sourcePage']].append(p)
 for n,previous in sorted(by_page.items()):
  d=pages[(e['sourceFiles'][0],n)]
  if not d['paragraphs']:
   report['unresolved'].append({'exercise':e['id'],'page':n,'reason':'OCR returned no text; retained source text'});new+=previous;continue
  if d['method']=='ocr-fra-best-300dpi':
   text=' '.join(p['fr']for p in d['paragraphs']);report['consensusPages']+=1
   for p in previous:
    fr=consensus(p['fr'],text);new.append({**p,'fr':fr,'extractionMethod':'ocr-consensus-rechecked'})
   continue
  report['tracePages']+=1
  # Regroup cached physical lines with the final column-aware algorithm.
  ls,_=ordered(d['lines'],595.3);ps=safe_text(paragraphs(ls,n,d['method']))
  if e['category']=='writing':
   # On the first material page exclude exam instructions above the source title.
   if n==min(by_page):
    target=norm(previous[0]['fr']);matches=[(difflib.SequenceMatcher(None,target[:75],norm(p['fr'])[:75]).ratio(),i)for i,p in enumerate(ps)]
    if matches and max(matches)[0]>.55:ps=ps[max(matches)[1]:]
    else:report['missingBoundaries'].append({'exercise':e['id'],'page':n,'boundary':'start'});ps=previous
   task_prefixes=[norm(t['fr'])[:35]for t in e.get('tasks',[])if len(t.get('fr',''))>60]
   end=next((i for i,p in enumerate(ps)if re.search(r'^(?:EXERCICE\s*2|ÉPREUVE\s*2|Essai\s*argumenté|SYNTHÈSE\s*:)',p['fr'],re.I)or any(norm(p['fr']).startswith(t)for t in task_prefixes)),None)
   if end is not None:ps=ps[:end]
   # Don't introduce unrelated text below the final source footnote.
   if n==max(by_page) and previous and ps:
    target=norm(previous[-1]['fr']);matches=[(difflib.SequenceMatcher(None,target[-90:],norm(p['fr'])[-90:]).ratio(),i)for i,p in enumerate(ps)]
    if matches and max(matches)[0]>.65:ps=ps[:max(matches)[1]+1]
  if not ps:report['unresolved'].append({'exercise':e['id'],'page':n,'reason':'No safe replacement; retained original'});ps=previous
  new+=ps
 for p in new:
  candidates=[o for o in old if o.get('sourcePage')==p.get('sourcePage')]
  exact=next((o for o in candidates if norm(o['fr'])==norm(p['fr'])),None)
  similar=exact
  if not similar and candidates:
   candidate=max(candidates,key=lambda o:difflib.SequenceMatcher(None,norm(o['fr']),norm(p['fr'])).ratio())
   ratio=difflib.SequenceMatcher(None,norm(candidate['fr']),norm(p['fr'])).ratio()
   if ratio>.94 and re.findall(r'\d+',candidate['fr'])==re.findall(r'\d+',p['fr']):similar=candidate
  if similar:
   p['id']=similar['id'];p['zh']=similar['zh'];p['translationReviewed']=similar.get('translationReviewed',False)
   cache[hashlib.sha256(p['fr'].encode()).hexdigest()]=p['zh'];report['translationReused']+=1
   if p['translationReviewed']:corrections[hashlib.sha256(p['fr'].encode()).hexdigest()]=p['zh']
  elif 'zh' in p and p.get('extractionMethod')=='ocr-consensus-rechecked':
   cache[hashlib.sha256(p['fr'].encode()).hexdigest()]=p['zh'];report['translationReused']+=1
   if p.get('translationReviewed'):corrections[hashlib.sha256(p['fr'].encode()).hexdigest()]=p['zh']
  else:
   p['id']='r3-'+hashlib.sha256(p['fr'].encode()).hexdigest()[:14];p.pop('zh',None);p['translationReviewed']=False;report['newTranslations']+=1
  seen[p['id']]+=1
  if seen[p['id']]>1:p['id']+='-'+str(seen[p['id']])
  if not exact or exact['fr']!=p['fr']:
   report['changedParagraphs']+=1;report['changes'].append({'exercise':e['id'],'page':p['sourcePage'],'id':p['id'],'old':similar['fr']if similar else None,'new':p['fr']})
 e['paragraphs']=new;e['materialRevision']='trace-columns-rechecked-v3'
(ROOT/'public/content.json').write_text(json.dumps(bank,ensure_ascii=False,separators=(',',':')))
(ROOT/'data/translations.json').write_text(json.dumps(cache,ensure_ascii=False,separators=(',',':')))
(ROOT/'data/translation-corrections.json').write_text(json.dumps(corrections,ensure_ascii=False,indent=2))
(ROOT/'data/precise-materials-audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print({k:v for k,v in report.items()if k not in ['changes','missingBoundaries','unresolved']});print('Boundaries needing check',report['missingBoundaries']);print('Unresolved',report['unresolved'])
