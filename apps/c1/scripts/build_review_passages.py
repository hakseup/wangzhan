"""Build exact, deduplicated answer-sentence pairs from reviewed local translations.
No translation API and no count-based French/Chinese sentence alignment.
"""
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
path=ROOT/'public/content.json';bank=json.loads(path.read_text());translations=json.loads((ROOT/'data/study/review-translations.json').read_text());count=0
for e in bank['exercises']:
 if e['category']not in ['long','short','reading']:continue
 bypid={p['id']:p for p in e['paragraphs']};pindex={p['id']:i for i,p in enumerate(e['paragraphs'])};found={}
 for q in e['questions']:
  for v in q['explanation']['evidence']:
   p=bypid[v['pid']];start=p['fr'].index(v['quote']);end=start+len(v['quote']);cursor=0;ids=[]
   sentences=[];boundary=0
   for m in re.finditer(r'[.!?…](?:\s*[»”\")])?\s+(?=[A-ZÀ-ÖØ-Þ«“])',p['fr']):
    sentences.append(p['fr'][boundary:m.end()].strip());boundary=m.end()
   if p['fr'][boundary:].strip():sentences.append(p['fr'][boundary:].strip())
   for sentence in sentences:
    pos=p['fr'].index(sentence,cursor);cursor=pos+len(sentence)
    if pos>=end or cursor<=start:continue
    pairid=f"{e['id']}:{p['id']}:{pos}"
    assert sentence in translations,(e['id'],sentence)
    if pairid not in found:found[pairid]={'id':pairid,'pid':p['id'],'start':pos,'fr':sentence,'zh':translations[sentence],'questionIds':[],'paragraphNumber':pindex[p['id']]+1}
    if q['id']not in found[pairid]['questionIds']:found[pairid]['questionIds'].append(q['id'])
    ids.append(pairid)
   v['pairIds']=ids
   v.pop('zh',None) # The old field held a whole-paragraph translation for a partial quote.
 e['reviewPassages']=sorted(found.values(),key=lambda x:(x['paragraphNumber'],x['start']));count+=len(found)
path.write_text(json.dumps(bank,ensure_ascii=False,separators=(',',':')));print('Built',count,'exact paired source passages.')
