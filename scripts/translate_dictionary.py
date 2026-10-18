"""Supplement missing dictionary senses and cache exact corpus-sentence translations locally."""
import json,re,hashlib,sqlite3,time,html,sys
from pathlib import Path
import ctranslate2,sentencepiece as spm
ROOT=Path(__file__).resolve().parents[1];DATA=ROOT/'data/dictionary';MODELS=ROOT.parent/'tooling/models'
frsp=spm.SentencePieceProcessor(model_file=str(MODELS/'fr_en/sentencepiece.model'));zhsp=spm.SentencePieceProcessor(model_file=str(MODELS/'translate-en_zh-1_9/sentencepiece.model'))
fr=ctranslate2.Translator(str(MODELS/'fr_en/model'),compute_type='int8',intra_threads=4);zh=ctranslate2.Translator(str(MODELS/'translate-en_zh-1_9/model'),compute_type='int8',intra_threads=4)
db=sqlite3.connect(DATA/'lookup-translations.sqlite');db.execute('create table if not exists translations(kind text,source text,zh text,primary key(kind,source))')
pending=json.loads((DATA/'pending-meanings.json').read_text());sentences=json.loads((DATA/'sentences.json').read_text())
base=json.loads((DATA/'base.json').read_text())
old=sqlite3.connect(ROOT/'data/revised-translations-v3.sqlite')
for s in sentences:
 row=old.execute('select zh from translations where hash=?',(hashlib.sha256(s.encode()).hexdigest(),)).fetchone()
 if row:db.execute('insert or ignore into translations values (?,?,?)',('fr',s,row[0]))
db.commit()
def translate(items,kind):
 if kind=='fr':
  en=fr.translate_batch([frsp.encode(html.unescape(s),out_type=str) for s in items],beam_size=2,max_batch_size=64,max_decoding_length=450)
  items=[frsp.decode(x.hypotheses[0]) for x in en]
 out=zh.translate_batch([zhsp.encode(s,out_type=str) for s in items],beam_size=2,max_batch_size=64,max_decoding_length=500)
 return [zhsp.decode(x.hypotheses[0]).strip() for x in out]
started=time.time()
phases=[('en',list(dict.fromkeys(s for _,e in pending for s in e['senses'])))]
if '--sentences' in sys.argv:phases.append(('fr',sentences))
for kind,items in phases:
 items=[s for s in items if not db.execute('select 1 from translations where kind=? and source=?',(kind,s)).fetchone()]
 print(kind,'pending',len(items),flush=True)
 for i in range(0,len(items),48):
  batch=items[i:i+48]
  for s,t in zip(batch,translate(batch,kind)):db.execute('insert or replace into translations values (?,?,?)',(kind,s,t))
  db.commit()
  if i%480==0:print(kind,min(i+48,len(items)),'/',len(items),round(time.time()-started),'s',flush=True)
 # Save usable progress after each complete phase.
 cache={s:t for s,t in db.execute('select source,zh from translations where kind="en"')}
 for word,e in pending:
  senses=[cache[s] for s in e['senses'] if cache.get(s)]
  if senses and not any(x['pos']==e['pos'] for x in base['entries'].get(word,[])):base['entries'].setdefault(word,[]).append({**e,'senses':senses})
 base['translations']={re.sub(r'\s+',' ',s.replace('’',"'")).strip().lower():t for s,t in db.execute('select source,zh from translations where kind="fr"')}
 base['entries']={w:es for w,es in base['entries'].items() if es}
 (DATA/'translated.json').write_text(json.dumps(base,ensure_ascii=False,separators=(',',':')))
 print('Saved',kind,'phase',flush=True)
print('Complete',flush=True)
