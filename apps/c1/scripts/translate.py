"""Optional, entirely local FR→EN→ZH reference translation using Argos models.

Models: official Argos package index revision 9504015, pinned package URLs.
Nothing is sent to an external translation service. Results are explicitly marked
as machine translations and are not used to determine correct exam answers.
"""
import hashlib,json,re,sqlite3,time
from pathlib import Path
import ctranslate2,sentencepiece as spm
ROOT=Path(__file__).resolve().parents[1]
MODELS=Path('/workspace/tooling/models')
db=sqlite3.connect(ROOT/'data'/'translation-cache.sqlite')
db.execute('CREATE TABLE IF NOT EXISTS translations (hash TEXT PRIMARY KEY, fr TEXT, zh TEXT)')
def key(s):return hashlib.sha256(s.encode()).hexdigest()
def split(text,sp):
 result=[]
 for sentence in re.split(r'(?<=[.!?…])\s+',text):
  tokens=sp.encode(sentence,out_type=str)
  for i in range(0,len(tokens),110):result.append(tokens[i:i+110])
 return result or [[]]
frsp=spm.SentencePieceProcessor(model_file=str(MODELS/'fr_en/sentencepiece.model'))
zhsp=spm.SentencePieceProcessor(model_file=str(MODELS/'en_zh/sentencepiece.model'))
fr=ctranslate2.Translator(str(MODELS/'fr_en/model'),device='cpu',compute_type='int8',intra_threads=4)
zh=ctranslate2.Translator(str(MODELS/'en_zh/model'),device='cpu',compute_type='int8',intra_threads=4)
bank=json.loads((ROOT/'public/content.json').read_text())
texts=list(dict.fromkeys(p['fr'] for e in bank['exercises'] for p in e['paragraphs']))
pending=[s for s in texts if not db.execute('SELECT 1 FROM translations WHERE hash=?',(key(s),)).fetchone()]
print(f'Translating {len(pending)} paragraphs locally',flush=True)
start=time.time()
for i in range(0,len(pending),16):
 batch=pending[i:i+16];segments=[];owners=[]
 for j,s in enumerate(batch):
  parts=split(s,frsp);segments.extend(parts);owners.extend([j]*len(parts))
 english=fr.translate_batch(segments,beam_size=1,max_batch_size=32,max_decoding_length=180)
 en=[frsp.decode(r.hypotheses[0]) for r in english]
 chinese=zh.translate_batch([zhsp.encode(s,out_type=str) for s in en],beam_size=1,max_batch_size=32,max_decoding_length=220)
 translated=['']*len(batch)
 for owner,result in zip(owners,chinese):translated[owner]+=zhsp.decode(result.hypotheses[0])
 for s,t in zip(batch,translated):db.execute('INSERT OR REPLACE INTO translations VALUES (?,?,?)',(key(s),s,t))
 db.commit()
 if i%128==0:print(f'{min(i+16,len(pending))}/{len(pending)}, {time.time()-start:.0f}s',flush=True)
result={r[0]:r[1] for r in db.execute('SELECT hash,zh FROM translations')}
(ROOT/'data'/'translations.json').write_text(json.dumps(result,ensure_ascii=False,separators=(',',':')))
print('Reference translations complete',flush=True)
