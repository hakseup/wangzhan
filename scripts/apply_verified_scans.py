"""Apply manually PDF-checked, watermarked oral source pages from the versioned audit."""
import json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
bank=json.loads((ROOT/'public/content.json').read_text())
patch=json.loads((ROOT/'data/source-corrections-v3.json').read_text())
for e in bank['exercises']:
 if e['id'] not in patch:continue
 old={p['fr']:p for p in e['paragraphs']};out=[]
 for p in patch[e['id']]:
  p={**p,'id':'v3-'+hashlib.sha256(p['fr'].encode()).hexdigest()[:14],'extractionMethod':'manually-checked-against-pdf-v3','translationReviewed':False}
  if p['fr'] in old:p.update({k:v for k,v in old[p['fr']].items()if k in ['zh','translationReviewed']})
  out.append(p)
 e['paragraphs']=out
(ROOT/'public/content.json').write_text(json.dumps(bank,ensure_ascii=False,separators=(',',':')))
print('Applied',sum(map(len,patch.values())),'manually checked source paragraphs')
