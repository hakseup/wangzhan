"""Keep static GitHub dictionary assets modest; offline packaging merges them again."""
import json
from pathlib import Path
from bank_assets import load_bank
ROOT=Path(__file__).resolve().parents[1];public=ROOT/'public';bank=load_bank(public)
encode=lambda x:json.dumps(x,ensure_ascii=False,separators=(',',':'))
parts=[]
for key in ['entries','formLemmas','translations','phrases']:
 value=bank['lexicon'].pop(key,{})
 if isinstance(value,list):
  parts.append({key:value});continue
 chunk={};size=0
 for word,entry in value.items():
  size+=len(encode({word:entry}).encode())
  if size>3000000 and chunk:parts.append({key:chunk});chunk={};size=len(encode({word:entry}).encode())
  chunk[word]=entry
 if chunk:parts.append({key:chunk})
for path in (public/'dictionary').glob('part-*.json'):path.unlink()
bank['lexiconFiles']=[]
for i,part in enumerate(parts):
 name=f'/dictionary/part-{i:03}.json';(public/name.lstrip('/')).write_text(encode(part));bank['lexiconFiles'].append(name)
(public/'content.json').write_text(encode(bank))
print('Split',len(parts),'dictionary assets; core',round((public/'content.json').stat().st_size/1024**2,1),'MiB; content identical after merge.')
