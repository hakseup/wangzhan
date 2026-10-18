"""Merge final reference translations and small reviewed edits into the distributable bank."""
from pathlib import Path
import json,hashlib,re,html
ROOT=Path(__file__).resolve().parents[1];p=ROOT/'public/content.json';bank=json.loads(p.read_text());translations=json.loads((ROOT/'data/revised-translations.json').read_text());manual=json.loads((ROOT/'data/translation-edits.json').read_text())
key=lambda s:hashlib.sha256(s.encode()).hexdigest()
question_edits={}
for line in (ROOT/'data/question-translations.tsv').read_text().splitlines():
 if line and not line.startswith('#'):
  exercise,*questions=line.split('|');question_edits[exercise]=questions
option_edits={};exercise=None
for line in (ROOT/'data/option-translations.tsv').read_text().splitlines():
 if not line or line.startswith('#'):continue
 if '|' not in line:exercise=line;continue
 qid,*options=line.split('|');option_edits[exercise+':'+qid]=options
paragraph_edits={}
for line in (ROOT/'data/paragraph-translations.tsv').read_text().splitlines():
 if line and not line.startswith('#'):
  exercise,pid,text=line.split('|',2);paragraph_edits[exercise+':'+pid]=text
glossary=json.loads((ROOT/'data/name-glossary.json').read_text())
variants={'Paris':['巴黎'],'France':['法国'],'Chine':['中国'],'Europe':['欧洲'],'États-Unis':['美国'],'Royaume-Uni':['英国'],'Canada':['加拿大'],'Québec':['魁北克'],'Japon':['日本'],'Allemagne':['德国'],'Espagne':['西班牙'],'Italie':['意大利'],'Afrique':['非洲'],'Inde':['印度'],'Australie':['澳大利亚'],'Brésil':['巴西'],'Belgique':['比利时'],'Suisse':['瑞士'],'Russie':['俄罗斯'],'La Réunion':['留尼汪'],'Petit Palais':['小皇宫','小宫'],'Facebook':['脸书','面书'],'Le Figaro':['费加罗报'],'Figaro':['费加罗报'],'Mark Zuckerberg':['马克·祖克尔贝格','马克·扎克伯格','马克·祖克伯格'],'Médiapart':['地中海省'],'France Inter':['法国国际广播电台'],'RFI':['法国国际广播电台'],'Internet':['因特网'],'Xavier de la Porte':['萨维尔·德拉波特'],'Maël Virat':['马埃尔·维拉特'],'Mélanie Marcel':['梅拉尼·马塞尔','Mélanie·Marcel(Melanie Marcel)'],'Gerbert Bakx':['格伯特·巴克克斯']}
for name,t in glossary.items():
 if t in ['世界','科学','自然','现在','工作','人类','文化','艺术','故事','名字']:continue
 variants.setdefault(name,[]).append(t)
 # Models sometimes add the original spelling in parentheses after a translated name.
 if '(' in t and ')' in t:variants[name].append(t.split('(')[0])
for line in (ROOT/'data/name-variants.tsv').read_text().splitlines():
 if line and not line.startswith('#'):
  name,*forms=line.split('|');variants.setdefault(name,[]).extend(forms)
scoped_variants=[(name,name.casefold(),re.compile(r'(?<!\w)'+re.escape(name)+r'(?!\w)',re.I),sorted(set(variants[name]),key=len,reverse=True)) for name in sorted(variants,key=len,reverse=True)]

def polish(t,source):
 t=html.unescape(t)
 source_folded=source.casefold()
 for name,folded,pattern,forms in scoped_variants:
  if folded not in source_folded or not pattern.search(source):continue
  for target in forms:
   if len(target)>1:
    t=re.sub(re.escape(target)+r'(?!人|语)',lambda _:name,t) if name in ['France','Chine','Europe','États-Unis','Royaume-Uni','Canada','Japon','Allemagne'] else t.replace(target,name)
  t=t.replace(name+'('+name+')',name).replace(name+'（'+name+'）',name)
 # These are ordinary terms, never person or place names.
 if re.search(r'\bmakers\b',source,re.I):
  for word in ['决策者','制造商','制造者']:t=t.replace(word,'创客')
 if 'déconnexion matérielle' in source:t=t.replace('材料断开','与设备断开连接').replace('物质脱节','与设备断开连接')
 t=t.replace('以获得慰藉、忘记现实','以获得慰藉、暂离现实')
 return t
missing=[]
for e in bank['exercises']:
 for pi,para in enumerate(e['paragraphs']):
  t=translations.get(key(para['fr']),para.get('zh',''))
  if not t:missing.append((e['id'],para['id']))
  para['zh']=polish(t,para['fr'])
 for q in e['questions']:
  q['zh']=polish(translations.get(key(q['prompt']),q.get('zh','')),q['prompt'])
  for o in q.get('options',[]):o['zh']=polish(translations.get(key(o['text']),o.get('zh','')),o['text'])
  q['answer']['reference']=polish(q['answer'].get('reference',''),q['prompt']+' '+q['answer'].get('reference',''))
  if q.get('explanation'):q['explanation']['reason']=polish(q['explanation']['reason'],' '.join(x['fr'] for x in e['paragraphs']))
 edits=manual.get(e['id'],{})
 for i,t in enumerate(edits.get('paragraphs',[])):e['paragraphs'][i]['zh']=t
 for para in e['paragraphs']:
  if para['id'] in edits.get('byParagraph',{}):para['zh']=edits['byParagraph'][para['id']]
  if e['id']+':'+para['id'] in paragraph_edits:para['zh']=paragraph_edits[e['id']+':'+para['id']]
 for i,t in enumerate(edits.get('questions',[])):e['questions'][i]['zh']=t
 for q in e['questions']:
  if q['id'] in edits.get('byQuestion',{}):q['zh']=edits['byQuestion'][q['id']]
 if e['questions']:
  reviewed=question_edits[e['id']]
  assert len(reviewed)==len(e['questions']),(e['id'],len(reviewed),len(e['questions']))
  for q,t in zip(e['questions'],reviewed):q['zh']=t
  for q in e['questions']:
   if not q.get('options'):continue
   reviewed_options=option_edits[e['id']+':'+q['id']]
   assert len(reviewed_options)==len(q['options']),(e['id'],q['id'])
   for o,t in zip(q['options'],reviewed_options):o['zh']=t
 if 'titleZh' in edits:e['titleZh']=edits['titleZh']
 e['titleZh']=polish(e['titleZh'],e['title'])
 e['translationKind']='revised-local-fr-en-zh'
# Clear, natural card titles keep proper places and website names.
for e in bank['exercises']:
 e['titleZh']={
 'short-2022-6-cn-2':'La Réunion的Cité des Arts',
 'short-2023-3-cn-2':'Paris的地方货币',
 'short-2024-3-cn-2':'Paris的参与式预算',
 'short-2024-3-fr-1':'让更多人走进Opéra-Comique',
 'reading-2022-6-cn':'Facebook与我们的焦虑',
 'reading-2023-3-cn':'无车Paris，究竟为谁而建？',
 'reading-mock-2':'COP21有什么作用？'
 }.get(e['id'],e['titleZh'])
assert not missing,missing
for e in bank['exercises']:
 for q in e['questions']:
  assert q['zh'],(e['id'],q['id'],'prompt translation missing')
  for o in q.get('options',[]):assert o['zh'],(e['id'],q['id'],o['id'],'option translation missing')
p.write_text(json.dumps(bank,ensure_ascii=False,separators=(',',':')))
print('Merged',len(bank['exercises']),'sets;',sum(len(e['paragraphs']) for e in bank['exercises']),'paragraphs; all prompts and options translated.')
