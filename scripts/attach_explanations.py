"""Attach reviewed reasons and source-exact evidence from reviewed paragraph locations."""
import json,re,math,unicodedata,collections
from pathlib import Path
import spacy
ROOT=Path(__file__).resolve().parents[1]
bank=json.loads((ROOT/'public/content.json').read_text())
locations=json.loads((ROOT/'data/evidence-locations.json').read_text())
reasons=json.loads((ROOT/'data/explanation-reasons.json').read_text())
nlp=spacy.load('fr_core_news_sm',disable=['parser','ner'])
norm=lambda s:''.join(c for c in unicodedata.normalize('NFD',s.lower()) if not unicodedata.combining(c))
stop={norm(x) for x in nlp.Defaults.stop_words}|{'document','texte','auteur','journaliste','article','selon','expliquer','exemple','reponse','principal','donner','deux','raison','propos','question','interlocuteur','interviewe','intervenant'}
def tokens(s):return {norm(t.lemma_) for t in nlp(s) if (t.is_alpha or t.like_num) and norm(t.lemma_) not in stop and len(t.text)>2}
locations['long-2025-11-cn'][-1]='36'
locations['long-2021-5-cn'][4]='10'
locations['long-2021-5-cn'][5]='11+12'
# Exact starts for answers whose wording differs substantially from the source.
needles={
('short-2025-8-fr-1','q4','p3'):'La maîtrise des coûts',
('short-2024-6-cn-1','q3','p7'):'lorsqu’on double, le temps paraît rapide',
('long-2021-3-cn','q3','p2'):'Ceux qui connaissent',
('long-2021-3-cn','q6','p4'):'Parce que par exemple',
('long-2022-6-cn','q2','p2'):'À vos côtés',
('long-2023-10-fr','q1','p1'):'Et le problème',
('long-2023-10-fr','q3','p1'):'Ce qui est souvent mis en avant',
('long-2023-10-fr','q3','p2'):'Donc ça permet',
('long-2023-10-fr','q9','p6'):'Je ne sais pas',
('long-2023-10-fr','q9','p7'):'Encore une fois',
('reading-2021-10-fr','q2','p5'):'Plus fort encore',
('reading-2021-10-fr','q4','p6'):'Or il entre',
('reading-2021-10-fr','q7','p12'):'« Les élèves',
('reading-2024-11-cn','q10','p8'):'Si l’enjeu',
('reading-mock-3','q14','p19'):'Les bénéfices politiques',
('reading-mock-5','q2','p2'):'St un quart',
('reading-mock-5','q11','p18'):'Seuls',
}
audit=[]
for e in bank['exercises']:
 if not e['questions']:continue
 assert len(locations[e['id']])==len(e['questions'])
 for idx,q in enumerate(e['questions']):
  ref=q['answer'].get('reference','');answer=next((o['text'] for o in q.get('options',[]) if o['id']==q['answer'].get('value')),ref)
  query=tokens(re.split(r'[\u4e00-\u9fff]',answer)[0]);prompt=tokens(q['prompt']);evidence=[]
  for pid in locations[e['id']][idx].split('+'):
   p=next(p for p in e['paragraphs'] if p['id']=='p'+pid);text=p['fr']
   sentences=[s for s in re.split(r'(?<=[.!?])\s+(?=[A-ZÀ-Ü«])',text) if len(s)>20]
   if not sentences:sentences=[text]
   needle=needles.get((e['id'],q['id'],p['id']))
   if needle and needle in text:
    start=text.index(needle);end=re.search(r'[.!?](?:\s|$)',text[start:]);quote=text[start:start+end.end()].strip() if end else text[start:]
   else:
    ranked=[]
    for s in sentences:
     t=tokens(s);score=(len(t&query)*4+len(t&prompt)*.7)/(max(1,len(t))**.3)
     if s in ref:score+=8
     ranked.append((score,s))
    quote=max(ranked,key=lambda x:x[0])[1]
   # A long unpunctuated OCR line is retained verbatim, rather than rewritten as a fake quotation.
   evidence.append({'pid':p['id'],'quote':quote})
  q['explanation']={'reason':reasons[e['id']][idx],'evidence':evidence}
  for v in evidence:assert v['quote'] in next(p['fr'] for p in e['paragraphs'] if p['id']==v['pid'])
  audit.append({'exercise':e['id'],'question':q['id'],'paragraphs':[v['pid'] for v in evidence],'maxQuoteLength':max(len(v['quote']) for v in evidence)})
(ROOT/'public/content.json').write_text(json.dumps(bank,ensure_ascii=False,separators=(',',':')))
(ROOT/'data/evidence-audit.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2))
print('Source-verified explanations:',len(audit))
