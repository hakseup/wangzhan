"""Build an offline French–Chinese lexicon from attributed Wiktionary exports.

Raw public exports stay outside the app; only text, POS, forms and derivations
are retained. No HTML from the exports is executed or displayed.
"""
import json,re,zipfile,collections,html
from pathlib import Path
import spacy
from opencc import OpenCC
from wordfreq import zipf_frequency

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'data/dictionary';OUT.mkdir(exist_ok=True)
cc=OpenCC('t2s');nlp=spacy.load('fr_core_news_sm',disable=['ner'])
def key(s):return re.sub(r'\s+',' ',s.replace('’',"'").replace('ʼ',"'")).strip().lower()
def flat(x):
 if isinstance(x,str):return x
 if isinstance(x,list):return ''.join(flat(i) for i in x)
 if isinstance(x,dict):
  if x.get('tag')=='details':return ''
  return flat(x.get('content',''))
 return ''
def nodes(x,label):
 if isinstance(x,list):
  for v in x:yield from nodes(v,label)
 elif isinstance(x,dict):
  if x.get('data',{}).get('content')==label:yield x
  yield from nodes(x.get('content',[]),label)
def glosses(row):
 return [re.sub(r'\s+',' ',flat(li)).strip() for block in nodes(row[5],'glosses') for li in block.get('content',[]) if isinstance(li,dict) and li.get('tag')=='li']
def rows(lang):
 with zipfile.ZipFile(ROOT.parent/f'tooling/fr-{lang}-wiktionary.zip') as z:
  for name in z.namelist():
   if name.startswith('term_bank_'):yield from json.loads(z.read(name))

entries=collections.defaultdict(list);forms=collections.defaultdict(list);english={};relations=collections.defaultdict(set)
def form(w,base):
 w,base=key(w),key(base)
 if w!=base and base not in forms[w] and len(forms[w])<12:forms[w].append(base)
def relate(w,base):
 w,base=key(w),key(base)
 if w!=base and len(base)>2:relations[w].add(base);relations[base].add(w)
for lang in ['zh','en']:
 for r in rows(lang):
  w=key(r[0]);pos=r[3] or ''
  if len(w)>100:continue
  if not pos:
   for v in r[5]:
    if isinstance(v,list) and len(v)==2 and isinstance(v[0],str):form(w,v[0])
   continue
  senses=glosses(r)
  if not senses:continue
  if lang=='zh':
   meanings=[]
   for sense in senses:
    sense=cc.convert(sense)
    m=re.match(r"^([A-Za-zÀ-ÿœŒ’'\- ]+?)\s*的(?:变位|第一|第二|第三|复数|单数|阴性|阳性|过去|现在|将来|简单|条件|命令|直陈|虚拟|变形)",sense)
    if m:form(w,m[1]);continue
    if sense and sense not in meanings:meanings.append(sense)
   if meanings:entries[w].append({'pos':pos,'senses':meanings[:10],'source':'wiktionary-zh'})
  else:
   english.setdefault(w,[]).append({'pos':pos,'senses':senses[:4],'source':'wiktionary-en-mt'})
   if pos=='name':
    name_entry={'pos':'name','senses':['专有名称，保留原文：'+r[0]],'source':'wiktionary'}
    if name_entry not in entries[w]:entries[w].append(name_entry)
  for label in ['details-entry-Morphemes','details-entry-Etymology']:
   for block in nodes(r[5],label):
    # Only explicit French suffix derivation, never arbitrary similar spellings.
    raw=' '.join(flat(v) for v in block.get('content',[]) if isinstance(v,dict) and v.get('tag')!='summary')
    m=re.search(r"(?:^|From\s+)([A-Za-zÀ-ÿœŒ’'-]+)(?:\s*\([^)]*\))?\s*\+\s*-[a-zé]+",raw)
    if m:relate(w,m[1])
print('Native entries',len(entries),'forms',len(forms),flush=True)

bank=json.loads((ROOT/'public/content.json').read_text());texts=[]
for e in bank['exercises']:
 texts.extend(p['fr'] for p in e['paragraphs'])
 texts.extend(q['prompt'] for q in e['questions'])
 texts.extend(o['text'] for q in e['questions'] for o in q.get('options',[]))
 texts.extend(html.unescape(re.sub('<[^>]+>',' ',m['html'])) for m in e.get('models',[]))
texts=list(dict.fromkeys(texts));corpus=set();sentences=set();coll=collections.defaultdict(collections.Counter)
for doc in nlp.pipe(texts,batch_size=32):
 for token in doc:
  if not token.is_alpha:continue
  lemma=key(token.lemma_);corpus.add(lemma);form(token.text,lemma)
  if token.pos_ in ['NOUN','VERB','ADJ'] and token.dep_ not in ['punct','det']:
   for child in token.children:
    if child.dep_ not in ['obj','amod','nmod','obl:arg']:continue
    if child.pos_ not in ['NOUN','ADJ','PROPN']:continue
    start,end=min(token.i,child.left_edge.i),max(token.i,child.right_edge.i)+1
    span=doc[start:end]
    if 2<=len(span)<=7 and not any(t.is_punct for t in span):coll[lemma][span.text]+=1
 for sent in doc.sents:
  text=sent.text.strip()
  if 12<=len(text)<=650 and len([t for t in sent if t.is_alpha])>=3:sentences.add(text)

pending=[]
for w,rr in english.items():
 if w not in corpus and zipf_frequency(w,'fr')<2.8:continue
 existing={x['pos'] for x in entries[w]}
 for entry in rr:
  if entry['pos'] in existing or entry['pos']=='name':continue
  pending.append([w,entry])

# Corpus collocations are actual text spans, not invented usage rules.
collocations={w:[t for t,n in counts.most_common(5)] for w,counts in coll.items() if w in entries or w in english}
related={w:sorted(b for b in bs if b in entries or b in english)[:12] for w,bs in relations.items()}
payload={'version':1,'entries':dict(entries),'forms':dict(forms),'related':related,'collocations':collocations,'translations':{},'credit':'Wiktionary / Kaikki / Wiktionary-to-Yomitan · 2025-04-08 · CC BY-SA 4.0 / GFDL；补充译文为本地机器翻译。'}
(OUT/'base.json').write_text(json.dumps(payload,ensure_ascii=False,separators=(',',':')))
(OUT/'pending-meanings.json').write_text(json.dumps(pending,ensure_ascii=False,separators=(',',':')))
(OUT/'sentences.json').write_text(json.dumps(sorted(sentences),ensure_ascii=False,separators=(',',':')))
print('Corpus lemmas',len(corpus),'pending senses',sum(len(r[1]['senses']) for r in pending),'sentences',len(sentences),flush=True)
