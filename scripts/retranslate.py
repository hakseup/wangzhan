"""Rebuild all reference translations with Argos 1.9, sentence-aware batches and audit.
Models are local, and the text never leaves this execution environment.
Set NOIX_MODELS to a directory containing translate-fr_en-1_9 and translate-en_zh-1_9.
This script deliberately does not present machine output as human-verified translation.
"""
import os,sys,json,re,html,hashlib,time,sqlite3,unicodedata
from pathlib import Path
sys.path.insert(0,'/workspace/tooling/python')
import ctranslate2,sentencepiece as spm
ROOT=Path(__file__).resolve().parents[1]
MODELS=Path(os.environ.get('NOIX_MODELS','/workspace/work/translation-models/unpacked'))
a=spm.SentencePieceProcessor(model_file=str(MODELS/'translate-fr_en-1_9/sentencepiece.model'))
b=spm.SentencePieceProcessor(model_file=str(MODELS/'translate-en_zh-1_9/sentencepiece.model'))
f=ctranslate2.Translator(str(MODELS/'translate-fr_en-1_9/model'),compute_type='int8',intra_threads=4)
z=ctranslate2.Translator(str(MODELS/'translate-en_zh-1_9/model'),compute_type='int8',intra_threads=4)
DB=sqlite3.connect(ROOT/'data/translation-v2-cache.sqlite');DB.execute('CREATE TABLE IF NOT EXISTS entries (key TEXT PRIMARY KEY, fr TEXT, en TEXT, zh TEXT)')
def clean(s):
 s=html.unescape(unicodedata.normalize('NFKC',s)).replace('’',"'").replace('‘',"'").replace('œ','oe').replace('Œ','OE').replace('\u00ad','').replace('\u00a0',' ')
 return re.sub(r'\s+',' ',s).strip()
def key(s):return hashlib.sha256(s.encode()).hexdigest()
def decode(tokenizer,tokens):return tokenizer.decode(tokens).replace('▁',' ').replace('⁇','').strip()
def segments(text):
 # Preserve sentence boundaries and avoid cutting the tail of long source paragraphs.
 result=[]
 for sentence in re.split(r'(?<=[.!?…])\s+(?=[A-ZÀ-Ü«"0-9])|\n+',clean(text)):
  if not sentence:continue
  tokens=a.encode(sentence,out_type=str)
  if len(tokens)<=145:result.append(tokens);continue
  for part in re.split(r'(?<=[;:])\s+|(?<=,)\s+(?=mais|et|qui|dont|car|tandis)',sentence):
   tok=a.encode(part,out_type=str)
   for i in range(0,len(tok),145):result.append(tok[i:i+145])
 return result or [a.encode(clean(text),out_type=str)]
bank=json.loads((ROOT/'public/content.json').read_text())
texts=list(dict.fromkeys([p['fr'] for e in bank['exercises'] for p in e['paragraphs']]+[t['fr'] for e in bank['exercises'] for t in e.get('tasks',[]) if t.get('fr')]))
pending=[s for s in texts if DB.execute('SELECT 1 FROM entries WHERE key=?',(key(s),)).fetchone() is None]
start=time.time();print('Retranslating',len(pending),'unique source paragraphs/instructions',flush=True)
for i in range(0,len(pending),12):
 batch=pending[i:i+12];parts=[];owners=[]
 for j,s in enumerate(batch):
  segs=segments(s);parts+=segs;owners += [j]*len(segs)
 enresults=f.translate_batch(parts,beam_size=3,max_batch_size=32,max_decoding_length=220,repetition_penalty=1.05)
 ens=[decode(a,r.hypotheses[0]) for r in enresults]
 zhresults=z.translate_batch([b.encode(clean(s),out_type=str) for s in ens],beam_size=3,max_batch_size=32,max_decoding_length=250,repetition_penalty=1.05)
 zz=[decode(b,r.hypotheses[0]) for r in zhresults]
 for j,s in enumerate(batch):
  english=' '.join(x for x,o in zip(ens,owners) if o==j);chinese=''.join(x for x,o in zip(zz,owners) if o==j)
  chinese=re.sub(r'([\u4e00-\u9fff]),',r'\1，',chinese);chinese=re.sub(r'([\u4e00-\u9fff])\.',r'\1。',chinese);chinese=re.sub(r'([\u4e00-\u9fff]):',r'\1：',chinese)
  DB.execute('INSERT OR REPLACE INTO entries VALUES (?,?,?,?)',(key(s),s,english,chinese))
 DB.commit()
 if i%60==0:print(min(i+12,len(pending)),'/',len(pending),'elapsed',round(time.time()-start),'sec',flush=True)
# Human corrections live separately and always override machine output on repeat runs.
overrides=json.loads((ROOT/'data/translation-corrections.json').read_text()) if (ROOT/'data/translation-corrections.json').exists() else {}
review=[]
for e in bank['exercises']:
 e['translationKind']='argos-1.9-reference'
 for p in e['paragraphs']+e.get('tasks',[]):
  if not p.get('fr'):continue
  row=DB.execute('SELECT zh FROM entries WHERE key=?',(key(p['fr']),)).fetchone()
  if row:p['zh']=overrides.get(key(p['fr']),row[0])
  p['translationReviewed']=key(p['fr']) in overrides
  if p.get('role')=='heading' and p['fr'].strip()==e['title'].strip():p['zh']=e['titleZh']
  zh=p.get('zh','');fr=p['fr']
  english_words=re.findall(r'[A-Za-z]{3,}',zh)
  if not zh or '�' in zh or '⁇' in zh or (not p.get('translationReviewed') and (len(english_words)>12 or (len(fr)>180 and len(zh)<12))):review.append({'exercise':e['id'],'paragraph':p['id'],'fr':fr,'zh':zh})
(ROOT/'data/translations.json').write_text(json.dumps({row[0]:overrides.get(row[0],row[1]) for row in DB.execute('SELECT key,zh FROM entries')},ensure_ascii=False,separators=(',',':')))
(ROOT/'public/content.json').write_text(json.dumps(bank,ensure_ascii=False,separators=(',',':')))
report={'engine':'Argos Translate 1.9 FR→EN→ZH; beam 3; sentence-aware','uniqueSources':len(texts),'paragraphs':sum(len(e['paragraphs']) for e in bank['exercises']),'manualCorrections':len(overrides),'needsReview':review,'sourceLimitations':[{'exercise':e['id'],'paragraph':p['id']} for e in bank['exercises'] for p in e['paragraphs'] if '［' in p.get('zh','')],'humanVerified':False}
(ROOT/'data/translation-v2-audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print('All translations rebuilt. Flagged paragraphs:',len(review),flush=True)
