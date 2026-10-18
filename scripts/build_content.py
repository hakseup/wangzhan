"""Build the site's text-only question bank from the user's 117 attachments.

Source labels and hand checked corrections live in catalog.py / overrides.json.
No PDF is copied into the public directory. Original audio is copied without alteration.
"""
import collections,glob,hashlib,json,re,shutil,sys
from pathlib import Path
from catalog import labels,ORAL_ZH,ORAL_FIX,topic_for

ROOT=Path(__file__).resolve().parents[1]
PUBLIC=ROOT/'public'; PUBLIC.mkdir(exist_ok=True)
(PUBLIC/'audio').mkdir(exist_ok=True)
AUDIO_SOURCES={}
PAGES=collections.defaultdict(list)
for f in (ROOT/'data'/'extracted').glob('*.json'):
 p=json.loads(f.read_text());PAGES[p['file']].append(p)
for ps in PAGES.values():ps.sort(key=lambda p:p['page'])
ANSWER_PAGES={json.loads(p.read_text())['file']:json.loads(p.read_text())['text'] for p in (ROOT/'data'/'answers').glob('*.json')}
QUESTION_PAGES={(d['file'],d['page']):d['text'] for p in (ROOT/'data'/'questions').glob('*.json') for d in [json.loads(p.read_text())]}
def question_text(p):return QUESTION_PAGES.get((p['file'],p['page']),p['text'])
def material_text(p):
 path=ROOT/'data'/'materials'/(hashlib.sha1((p['file']+str(p['page']-1)).encode()).hexdigest()[:16]+'.json')
 if not path.exists():return p['text']
 other=json.loads(path.read_text())['text']
 # Prefer the complete original-image pass when thresholding hid body lines.
 old_words=len(re.findall(r'\b[a-zà-ÿ]{2,}\b',p['text'],re.I))
 new_words=len(re.findall(r'\b[a-zà-ÿ]{2,}\b',other,re.I))
 return other if new_words>old_words*1.2 else p['text']

def strip(s):
 s=re.sub(r'法\s*语\s*课\s*代\s*表|大\s*脸\s*法\s*语|[䀀-鿿]{4,}','',s)
 s=re.sub(r'(?im)^.*(?:www\.talentfr\.com|DELF\s*[-–#]?\s*DALF.{0,12}课|公众.{0,8}搜索).*$','',s)
 s=re.sub(r'(?im)^\s*(?:DOCUMENT RÉSERVÉ[^\n]*|DALF C1[^\n]*|听力\s*\d*|阅读\s*\d*|口语|Page \d+|\d{1,2})\s*$','',s)
 s=re.sub(r'(?m)^\s*[^\w\n]*\s*$','',s)
 return s.strip()

def paras(s):
 s=strip(s)
 keymark=re.search(r'答案\s*[:：]',s)
 if keymark and keymark.start()>600:s=s[:keymark.start()]
 else:s=re.sub(r'答案\s*[:：]\s*[ABC\s]{3,20}','',s)
 # Undo only layout line breaks, retain paragraphs and speaker changes.
 groups=re.split(r'\n\s*\n',s)
 out=[]
 for x in groups:
  x=re.sub(r'-\s*\n\s*(?=[a-zà-ÿ])','',x)
  x=re.sub(r'\s*\n\s*',' ',x).strip()
  if len(x)>12 and re.search(r'[A-Za-zÀ-ÿ]{3}',x):
   if len(x)>1300:
    chunk=''
    for sentence in re.split(r'(?<=[.!?])\s+',x):
     if len(chunk)+len(sentence)>950 and chunk:out.append({'fr':chunk.strip()});chunk=''
     chunk+=sentence+' '
    if chunk.strip():out.append({'fr':chunk.strip()})
   else:out.append({'fr':x})
 return out

def source_key(name):
 m=re.search(r'(\d{4})年(\d{1,2})月(中国|法国|非洲)',name)
 if m:return f'{m[1]}-{int(m[2])}-'+{'中国':'cn','法国':'fr','非洲':'af'}[m[3]]
 m=re.search(r'补充(\d+)',name)
 if m:return 'extra-'+m[1]
 m=re.search(r'第([一二三四五六])套模拟',name)
 if m:return 'mock-'+str('一二三四五六'.index(m[1])+1)
 return hashlib.sha1(name.encode()).hexdigest()[:10]

def provenance(name):
 m=re.search(r'(\d{4})年(\d{1,2})月(中国|法国|非洲)',name)
 return f'{m[1]} 年 {m[2]} 月 · {m[3]}场次' if m else ('阅读模拟材料' if '模拟' in name else '口语主题材料' if '口语' in name else '写作补充材料')

def audio_for(key,segment=None):
 for p in glob.glob('/workspace/attachments/*/*'):
  if Path(p).suffix.lower() not in ['.m4a','.mp3']:continue
  if source_key(Path(p).name)!=key:continue
  isshort='短听力' in p
  if segment and not isshort:continue
  if not segment and isshort:continue
  if segment and ('（一）' in p or '(一)' in p)!=(segment==1):continue
  target=f'{key}'+(f'-{segment}' if segment else '')+Path(p).suffix
  shutil.copy2(p,PUBLIC/'audio'/target)
  AUDIO_SOURCES['/audio/'+target]=Path(p).name
  return '/audio/'+target
 return None

def answers_from(s):
 out={}
 # Reference keys must have a visible numeric identifier. Never guess an unreadable key.
 s=re.sub(r'(?<=\d)\s*[．。]', '.',s)
 pat=r'(?m)^\s*(\d{1,2})\s*[.、:：)]?\s*([^\n]+(?:\n(?!\s*\d{1,2}\s*[.、:：)]?\s*[^\n])[^\n]+)*)'
 for m in re.finditer(pat,s):
  n=int(m[1]);body=m[2].strip()
  if not 1<=n<=25:continue
  if re.fullmatch(r'[ABCÀ€]\s*[.,。]?',body):out[n]={'value':{'À':'A','€':'C'}.get(body[0],body[0]),'reference':body[0]}
  elif re.match(r'^(?:Vrai|Faux|对|错|正确|错误)',body,re.I):
   value='Vrai' if re.match(r'^(?:Vrai|对|正确)',body,re.I) else 'Faux'
   out[n]={'value':value,'reference':strip(body)}
  elif len(body)>8 and ('\u4e00'<=body[0]<='\u9fff' or re.search(r'\b(?:parce|pour|car|les|le|la|il|elle|c’est|afin)\b',body,re.I)):
   if sum(c in body for c in 'HUAXRPEQK')>len(body)*.18:continue
   out[n]={'reference':strip(re.sub(r'(?<=[\u4e00-\u9fff])\s+(?=[\u4e00-\u9fff])','',body))}
 return out

OPTION=re.compile(r'^\s*[^A-Za-z0-9À-ÿ]{0,4}\s*([ABCÀ€8])(?:\s+|\s*[\[\]()0OD©]+\s*)(.*)$')
START=re.compile(r"^(?:Quels?\b|Quelles?\b|Qu[’']|Que\b|Pourquoi\b|Comment\b|En quoi\b|Dans\b|Selon\b|D[’']après\b|Pour\b|Sur quoi\b|Au sujet\b|À quel\b|A quel\b|Vrai ou faux|Cochez VRAI|Cochez Vrai)",re.I)
NUMBER=re.compile(r'^\s*(\d{1,2})\s*[.\-)]?\s+([A-Za-zÀ-ÿ«].*)$')
CIRCLE=re.compile(r'^\s*[^A-Za-zÀ-ÿ0-9\s]{1,3}\s*([A-Za-zÀ-ÿ«].*)$')

def parse_questions(raw):
 raw=re.sub(r'(?m)^(\s*\d{1,2}\s+)=',r'\1',raw)
 raw=re.sub(r'(?m)^\s*[oÔÉ]\s+(?=(?:Quel|Pourquoi|Comment|Pour |Selon|De quel))','@ ',raw)
 lines=raw.splitlines(); qs=[];current=None;last_blank=True
 def flush():
  nonlocal current
  if not current:return
  prompt=' '.join(current.pop('promptLines')).strip()
  prompt=re.sub(r'\b\d+(?:[,\.]\d+)?\s*points?\b','',prompt,flags=re.I)
  prompt=re.sub(r'\s+',' ',prompt).strip(' |:')
  if len(prompt)<7:current=None;return
  current['prompt']=prompt
  current['type']='choice' if len(current['options'])>=2 else 'tf' if re.search(r'vrai|faux',prompt,re.I) else 'text'
  if current['type']!='choice':current.pop('options')
  current['number']=len(qs)+1
  qs.append(current);current=None
 for rawline in lines:
  l=rawline.strip()
  if not l:last_blank=True;continue
  l=re.sub(r'^[^A-Za-z0-9À-ÿ©®@]+(?=[A-Za-zÀ-ÿ])','',l)
  l=re.sub(r'^[©®@]\s*[:;.]*\s*','@ ',l)
  alpha=[c for c in l if c.isalpha()]
  if len(alpha)>15 and sum(c.isupper() for c in alpha)/len(alpha)>.72:continue
  if re.search(r'[a-zA-Z]{35,}',l) and not re.search(r'\b(?:les|des|pour|que|dans|une|est)\b',l,re.I):continue
  l=re.sub(r'^(5elon|5elon)', 'Selon',l)
  if re.search(r'^听力|^\d?\s*Document\s*[12].*questions|^QUESTIONS|^Prise de notes|^PRISE DE NOTES|^Pour répondre aux questions|^Vous allez entendre|^La colonne|^pour prendre des|^lors de la correction|^Lisez maintenant',l,re.I):continue
  if re.match(r'^[. …•_—\-]{4,}',l) or re.search(r'^[A-Z]{16,}$',l):last_blank=True;continue
  if re.fullmatch(r'\d+(?:[,\.]\d+)?\s*points?',l,re.I):continue
  if re.search(r'points? si le|aucun point|si le choi|si le chou|Justification|JUSTPICAT|votre réponse\.|votre répanse\.|justifie votre réponse|^\s*[01,\.5 ]+points?',l,re.I):continue
  if re.match(r'^[0-9 ]{8,}',l):continue
  if re.search(r'Vrai ou faux|Cochez VRAI|Cochez Vrai|Cochez \(?Vrau',l,re.I):
   flush();current={'sourceNumber':None,'promptLines':['Vrai ou faux ?'],'options':[],'forcedTf':True,'hasStatement':False};last_blank=True;continue
  if current and current.get('forcedTf') and not current.get('hasStatement'):
   if re.search(r'phrase|partie de texte|votre ré|[0-9] point|coch|bonne réponse',l,re.I):continue
   current['promptLines'].append(l);current['hasStatement']=True;last_blank=False;continue
  m=OPTION.match(l)
  if m and current and len(m[2].strip())>2 and not re.match(r'^\d{1,2}\s+(?![\[\]O])',l) and not re.match(r'^[ÀA] quel',l,re.I):
   key={'À':'A','€':'C','8':'B'}.get(m[1],m[1])
   text=re.sub(r'^(?:\[[^\]]{0,3}\]|[O0CDIÏÙ][\]\)]|[\[©])\s*','',m[2]).strip()
   current['options'].append({'id':key,'text':text});last_blank=False;continue
  num=NUMBER.match(l)
  trailing=re.match(r'^(.{15,}?)(\d{1,2})$',l)
  if trailing and not l.startswith(('A ','B ','C ')):
   l=trailing[1];num=NUMBER.match(f'{trailing[2]} {l}')
  circ=CIRCLE.match(l)
  stripped=circ[1] if circ else l
  if re.match(r'^[6ÔOQ]\s+(?:Quel|Qu[’\']|En |Selon|Pourquoi|Comment)',l):stripped=l[2:]
  isstart=bool(num and 1<=int(num[1])<=25) or bool(circ and (START.match(stripped) or len(stripped)>20))
  if not isstart and START.match(stripped):
   isstart=current is None or len(current.get('options',[]))>=2 or ((last_blank or '?' in ' '.join(current['promptLines'])) and (any('?' in p for p in current['promptLines']) or len(' '.join(current['promptLines']))>100))
  # Unnumbered declarative questions in scanned short-listening sheets.
  if not isstart and last_blank and not current:
   isstart=bool(re.match(r'^(?:Le |La |Les |L[’\']|Aujourd|Lors |Ce |Cette |Cet |Un |De nombreux|L[’\']enfant)',stripped))
  if not isstart and current and (len(current['options'])>=2 or '?' in ' '.join(current['promptLines'])):
   isstart=bool(re.match(r'^(?:Le |La |Les |L[’\']|Aujourd|Lors |Ce |Cette |Cet |Un |De nombreux|L[’\']enfant|[A-ZÀ-Þ][a-zà-ÿ-]+ [A-ZÀ-Þ][a-zà-ÿ-]+)',stripped))
  if isstart:
   flush();current={'sourceNumber':int(num[1]) if num else None,'promptLines':[num[2] if num else stripped],'options':[]}
  elif current:
   if current['options'] and not last_blank:
    current['options'][-1]['text']+=' '+l
   elif not re.search(r'Justification|aucun point|point si le choix|recopiez la phrase',l,re.I) and not re.fullmatch(r'.{0,5}Vrai.{0,12}Faux.{0,5}',l,re.I):
    current['promptLines'].append(l)
  last_blank=False
 flush()
 for q in qs:
  q.pop('forcedTf',None);q.pop('hasStatement',None)
  q['id']='q'+str(q['number'])
  if q.get('options'):
   # Remove duplicate OCR option identifiers only, preserving all distinct answers.
   opts={o['id']:o for o in q['options']};q['options']=list(opts.values())
   if len(opts)<2:q['type']='text';q.pop('options')
 return qs

def short_sections(ps):
 sections={1:{'q':[],'t':[]},2:{'q':[],'t':[]}}
 for p in ps:
  t=p['text']
  # Source PDFs group question sheets separately from transcripts.
  is_q=len(re.findall(r'(?m)^\s*[ABCÀ8]\s*(?:\[|\s)',t))>=4
  parts=re.split(r'(?im)^\s*(?:听力\s*([23])|Document\s*([12])\s*[:.]?[^\n]*questions[^\n]*)\s*\n',t)
  if len(parts)>1:
   active=1
   if parts[0].strip():sections[1]['q' if is_q else 't'].append(parts[0])
   for i in range(1,len(parts),3):
    n=parts[i] or parts[i+1];active=int(n)-1 if parts[i] else int(n)
    active=max(1,min(2,active));sections[active]['q' if is_q else 't'].append(parts[i+2])
  else:
   sections[1]['q' if is_q else 't'].append(t)
 return sections

def make():
 bank=[];audit=[]
 overrides=json.loads((ROOT/'data'/'overrides.json').read_text()) if (ROOT/'data'/'overrides.json').exists() else {}
 for name,ps in sorted(PAGES.items()):
  if '口语' in name:
   idx=0 if '第一' in name else 1
   for n in range(len(ps)//2):
    pair=ps[n*2:n*2+2];first=strip(pair[0]['text'])
    title=re.split(r'DOCUMENT\s*1',first,flags=re.I)[0]
    title=re.sub(r'^.*?Thème de l[’\']exposé\s*:?','',title,flags=re.S|re.I)
    title=re.sub(r'\s+',' ',title).strip()
    title=ORAL_FIX.get((idx,n),title)
    bank.append({'id':f'speaking-{idx+1}-{n+1}','category':'speaking','title':title,'titleZh':ORAL_ZH[idx][n], 'topic':topic_for(title),'source':f'口语主题材料 {idx+1} · 第 {n+1} 题','paragraphs':paras('\n\n'.join(material_text(p) for p in pair)),'questions':[],'ocr':any(p['method']=='ocr' for p in pair),'sourceFiles':[name]})
   continue
  cat='long' if '长听力' in name else 'short' if '短听力' in name else 'reading' if '阅读' in name else 'writing'
  key=source_key(name);metadata=labels(cat)
  answer_text=ps[-1]['text']
  if len(re.findall(r'(?m)^\s*\d{1,2}\s*[.．、]',answer_text))<3:answer_text=ANSWER_PAGES.get(name,answer_text)
  answers=answers_from(answer_text)
  if cat=='short':
   sections=short_sections(ps)
   for n in [1,2]:
    labelkey=key+'-'+str(n);title,zh,topic=metadata[labelkey]
    s=sections[n];qs=parse_questions('\n\n'.join(s['q']))
    bank.append({'id':'short-'+labelkey,'category':cat,'title':title,'titleZh':zh,'topic':topic,'source':provenance(name),'paragraphs':paras('\n\n'.join(s['t'])),'questions':qs,'audio':audio_for(key,n),'ocr':any(p['method']=='ocr' for p in ps),'sourceFiles':[name]})
  else:
   title,zh,topic=metadata[key]
   if cat=='reading':
    if key in ['2024-12-fr','2024-6-fr']:material=ps;question_pages=[]
    elif key=='2024-5-fr':material=ps[:2];question_pages=ps[2:]
    elif key in ['mock-2','mock-4']:material=ps[:2];question_pages=ps[1:-1]
    else:material=ps[:2];question_pages=ps[2:-1]
   elif cat=='long':
    transcript_start=next((i for i,p in enumerate(ps[:-1]) if len(re.findall(r'(?:[A-ZÀ-Ý][A-Za-zÀ-ÿ’\-]+(?: [A-ZÀ-Ý]?[A-Za-zÀ-ÿ’\-]+){0,2}|[A-Z]{1,5})\s*:',p['text']))>=4 or re.search(r'^\s*TRANSCRIPTION',p['text'])),None)
    if transcript_start==0:material=ps[:2];question_pages=ps[2:-1]
    elif transcript_start is not None:question_pages=ps[:transcript_start];material=ps[transcript_start:-1]
    else:question_pages=ps[:2];material=ps[2:-1] if len(ps)>=5 else ps[2:3]
   else:material=ps;question_pages=[]
   qraw='\n\n'.join(question_text(p) for p in question_pages)
   if key in ['mock-2','mock-4']:
    parts=re.split(r'\bQUESTIONS\b',qraw,flags=re.I)
    if len(parts)>1:qraw=parts[-1]
   qs=parse_questions(qraw)
   for q in qs:
    sn=q['sourceNumber']
    a=answers.get(sn)
    if a and (q['type']=='text' or a.get('value') in [o['id'] for o in q.get('options',[])] or q['type']=='tf'):
     q['answer']=a
   mraw='\n\n'.join(material_text(p) for p in material)
   if key in ['mock-2','mock-4']:mraw=re.split(r'\bQUESTIONS\b',mraw,flags=re.I)[0]
   bank.append({'id':cat+'-'+key,'category':cat,'title':title,'titleZh':zh,'topic':topic,'source':provenance(name),'paragraphs':paras(mraw),'questions':qs,'audio':audio_for(key) if cat=='long' else None,'ocr':any(p['method']=='ocr' for p in ps),'sourceFiles':[name]})
 extra_path=ROOT/'data'/'audio-supplements.json'
 if extra_path.exists():
  for e in json.loads(extra_path.read_text()):
   e['audio']=audio_for(e.pop('audioKey'),e.pop('audioSegment'));bank.append(e)
 (ROOT/'data'/'raw-bank.json').write_text(json.dumps(bank,ensure_ascii=False))
 translations=json.loads((ROOT/'data'/'translations.json').read_text()) if (ROOT/'data'/'translations.json').exists() else {}
 writing_tasks=json.loads((ROOT/'data'/'writing-tasks.json').read_text()) if (ROOT/'data'/'writing-tasks.json').exists() else {}
 for e in bank:
  if e['id'] in overrides:
   patch=overrides[e['id']]
   for k,v in patch.items():
    if k=='answers':
     for q in e['questions']:
      if str(q['number']) in v:q['answer']=v[str(q['number'])]
    else:e[k]=v
  if e.get('audio') in AUDIO_SOURCES:e['sourceFiles']=list(dict.fromkeys(e['sourceFiles']+[AUDIO_SOURCES[e['audio']]]))
  for i,p in enumerate(e['paragraphs']):
   p['id']='p'+str(i)
   zh=translations.get(hashlib.sha256(p['fr'].encode()).hexdigest())
   if zh:p['zh']=zh
  if all(p.get('zh') for p in e['paragraphs']):e['translationKind']='machine-fr-en-zh'
  if e['category']=='writing':
   raw='\n\n'.join(material_text(p) for p in PAGES[e['sourceFiles'][0]])
   m=re.search(r'Essai\s+argument[ée]',raw,re.I)
   if m:
    task=re.split(r'(?:DOCUMENT\s*(?:n[°o]\s*)?1|Synthèse de documents|ÉPREUVE\s*N.{0,4}1)',raw[m.end():],flags=re.I)[0]
    task=re.sub(r'^\s*[\d\W]*(?:points?)?\s*','',task)
    task=strip(re.sub(r'\s+',' ',task))
    start=re.search(r'(?:Vous |Vôus |Pour que |Un ?magazine |Un journal |Le maire |Dans son magazine |« Quelle)',task)
    if start:task=task[start.start():]
    if 60<len(task)<2500:e['tasks']=[{'id':'essai','fr':task,'zh':'按上述原题规定的身份、对象与立场完成议论文；注意原题词数要求。'}]
   if e['id'] in writing_tasks:e['tasks']=[writing_tasks[e['id']]]
  for i,q in enumerate(e['questions']):q['id']='q'+str(i+1)
  audit.append({'id':e['id'],'title':e['title'],'paragraphs':len(e['paragraphs']),'questions':len(e['questions']),'answers':sum('answer'in q for q in e['questions']),'options':[len(q.get('options',[])) for q in e['questions']]})
 bank.sort(key=lambda e:({'long':0,'short':1,'reading':2,'writing':3,'speaking':4}[e['category']],e['id']))
 payload={'version':1,'name':'胡桃法语 · DALF C1','sourceFileCount':117,'pdfCount':len(PAGES),'pageCount':sum(map(len,PAGES.values())),'exercises':bank}
 (PUBLIC/'content.json').write_text(json.dumps(payload,ensure_ascii=False,separators=(',',':')))
 (ROOT/'data'/'import-audit.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2))
 print(json.dumps({'sets':len(bank),'questions':sum(len(e['questions']) for e in bank),'categories':dict(collections.Counter(e['category'] for e in bank)),'audioFiles':len(list((PUBLIC/'audio').glob('*')))},ensure_ascii=False))

if __name__=='__main__':make()
