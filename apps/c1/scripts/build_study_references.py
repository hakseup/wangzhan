"""Attach independently stored learning references without replacing source materials.
Source evidence is always taken from the current October-17 paragraph text.
"""
import json,re,html,difflib,unicodedata,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
bank=json.loads((ROOT/'public/content.json').read_text())
models=json.loads((ROOT/'data/study/models.json').read_text())
evidence=json.loads((ROOT/'data/study/evidence.json').read_text())
reasons=json.loads((ROOT/'data/study/explanation-reasons.json').read_text())
audit={'models':[],'explanations':0,'missingEvidence':[]}
for e in bank['exercises']:
 if e['id'] in models:
  e['studyModels']=models[e['id']]
  for m in e['studyModels']:audit['models'].append({'exercise':e['id'],'kind':m['id'],'words':len(' '.join(m['paragraphs']).split())})
 for i,q in enumerate(e['questions']):
  if e['category']not in ['long','short','reading']:continue
  reference=q.get('answer',{});value=reference.get('value');answer=reference.get('reference','')
  opt=next((o['text']for o in q.get('options',[])if o['id']==value),None)
  if opt:answer=value+' — '+opt
  elif value and value not in answer:answer=value+' — '+answer
  quotes=[]
  for match in evidence.get(e['id'],{}).get(q['id'],[]):
   pid=match['pid']
   p=next((p for p in e['paragraphs']if p['id']==pid),None)
   if p:quotes.append({'pid':pid,'quote':match['quote']if match['quote']in p['fr']else p['fr'],'zh':p.get('zh','')})
  reason=(reasons.get(e['id'],[])+['']*len(e['questions']))[i]
  q['explanation']={'answer':answer,'reason':reason,'evidence':quotes}
  if not quotes:
   q['explanation']['limitation']='当前原文摘录不足以核实具体答案句，请勿把推测当作原文证据。';audit['missingEvidence'].append({'exercise':e['id'],'question':q['id']})
  audit['explanations']+=1
(ROOT/'public/content.json').write_text(json.dumps(bank,ensure_ascii=False,separators=(',',':')))
(ROOT/'data/study/audit.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2))
print('Models',len(audit['models']),'explanations',audit['explanations'],'missing evidence',len(audit['missingEvidence']))
