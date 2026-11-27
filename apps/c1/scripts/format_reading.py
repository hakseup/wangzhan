"""Mark reading hierarchy without changing source text or annotation offsets."""
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parents[1]
p=ROOT/'public/content.json';b=json.loads(p.read_text())
headings={
 'reading-2021-10-fr':['p0','p4','p8','p11','p15','p18'],
 'reading-2025-3-cn':['p0','p5','p10'],
 'reading-2024-6-cn':['p0','p1','p5','p11'],
 'reading-2026-6-cn':['p2'],
 'reading-mock-1':['p2','p4','p8','p12','p15','p20'],
 'reading-mock-3':['p2','p5','p10','p13','p17'],
 'reading-mock-5':['p11','p13','p15','p17','p19','p21','p23'],
 'reading-mock-6':['p2','p21','p31','p32'],
}
report=[]
for e in b['exercises']:
 if e['category']!='reading':continue
 for i,p in enumerate(e['paragraphs']):
  fr=p['fr'].strip();role='body'
  if p['id'] in headings.get(e['id'],[]):role='heading'
  elif i==0 and not e['id'].startswith('reading-mock') and e['id']!='reading-2026-6-cn' and len(fr)<180:role='heading'
  elif re.match(r'^[*•“‘+]?\s*\w+\s*:',fr) and i>len(e['paragraphs'])-6 and len(fr)<220:role='note'
  elif re.search(r"D.apr[eè]s|www\.|https?://",fr) and len(fr)<190:role='source'
  elif 'PARTIE 2' in fr or 'COMPRÉHENSION DES' in fr or 'Lisez le texte' in fr:role='label'
  elif fr.endswith('?') and len(fr)<230:role='heading'
  p['role']=role
  # Continue visibly on a new line but without paragraph spacing when OCR split a sentence.
  p['continuation']= bool(role=='body' and i>0 and e['paragraphs'][i-1]['role']=='body' and not re.search(r'[.!?…»]$|[.!?…][”\"]$',e['paragraphs'][i-1]['fr'].strip()))
 report.append({'id':e['id'],'headings':sum(p['role']=='heading' for p in e['paragraphs']),'continuations':sum(p['continuation'] for p in e['paragraphs'])})
(ROOT/'public/content.json').write_text(json.dumps(b,ensure_ascii=False,separators=(',',':')))
(ROOT/'data/reading-layout-audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print('Formatted',len(report),'reading sets; source and paragraph IDs preserved.')
