"""Re-extract writing/oral source pages with font-aware repair and higher quality OCR.
Only recovered PDF text is used; unreadable text is never replaced with invented prose.
"""
import concurrent.futures,collections,csv,glob,hashlib,io,json,os,re,statistics,subprocess,sys,tempfile
from pathlib import Path
import fitz,numpy as np
from PIL import Image,ImageFilter,ImageOps
sys.path.insert(0,'/workspace/tooling/python')
from wordfreq import zipf_frequency
from extract import repair_span
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'data/revised-pages';OUT.mkdir(parents=True,exist_ok=True)
os.environ['OMP_THREAD_LIMIT']='1'
SYMBOLS={0x35b:',',0x35c:';',0x35f:'…',0x360:'-',0x364:'!',0x36a:'‘',0x386:'/',0x398:'(',0x399:')',0x39c:'[',0x39d:']',0x448:'%',0x44a:'+',0x44f:'=',0x486:'ff',0x48a:'ffi',0x48f:'fl',0x490:'ffl',**{0x3dd+i:str(i) for i in range(10)}}
def decode(s,font=''):
 if '\x03' in s:s=repair_span(s)
 elif re.search('[ñõþÿýā-Č]',s) and 'Spectral' in font:
  s=''.join(chr(ord(c)-144)if 241<=ord(c)<=268 else c for c in s)
 else:s=repair_span(s)
 return ''.join(SYMBOLS.get(ord(c),c)for c in s).replace('ﬁ','fi').replace('ﬂ','fl').replace('\u00ad','')
def cleanup(s):
 s=re.sub('[\u3400-\u9fff\u2e80-\u2fff\u2460-\u24ff\u2600-\u27ff]','',s)
 s=re.sub('[\x00-\x08\x0b-\x1f\ufffd]','',s)
 s=re.sub(r'\s+',' ',s).strip()
 if re.match(r'^(?:Cours\s+\d+|DOCUMENT RÉSERVÉ|DALF C1|LETTRES ET SCIENCES|Page \d|https?://|www\.|\d{1,2}$)',s,re.I):return ''
 return s

def combine(lines,page,method):
 if not lines:return []
 lines=sorted(lines,key=lambda l:(round(l['y']/3),l['x']))
 # Coalesce word-level native spans and separately drawn line fragments by baseline.
 rows=[]
 for l in lines:
  if rows and abs(rows[-1]['y']-l['y'])<3:
   row=rows[-1];gap=l['x']-row['right'];row['text']+=(' 'if gap>1 else '')+l['text'];row['right']=max(row['right'],l['right']);row['bold']=max(row['bold'],l['bold'])
  else:rows.append(dict(l))
 for l in rows:l['text']=cleanup(l['text'])
 rows=[l for l in rows if l['text']]
 sizes=[l['size']for l in rows if len(l['text'])>35];body=statistics.median(sizes)if sizes else 12
 gaps=[b['y']-a['y']for a,b in zip(rows,rows[1:])if 3<b['y']-a['y']<body*3]
 gap=statistics.median(gaps)if gaps else body*1.3
 right=sorted(l['right']for l in rows)[int(len(rows)*.85)] if rows else 0
 out=[];previous=None
 for l in rows:
  t=l['text'];role='body'
  if re.match(r'^(?:[>»]\s*)?DOCUMENT\s*(?:N[°o]?\s*)?\d',t,re.I):role='document'
  elif re.match(r'^Thème de l[’\']exposé',t,re.I):role='label'
  elif l['bold']>.6 and len(t)<190:role='heading'
  elif len(t)<150 and l['size']>body*1.12:role='heading'
  elif re.match(r'^(?:\*|\d\s*[:.)])',t) and l['size']<body*.95:role='note'
  separate=not out or role!=out[-1]['role'] or role in ['label']
  if previous:
   distance=l['y']-previous['y']
   if distance>gap*1.42:separate=True
   if role=='body'and previous['right']<right-30 and re.search(r'[.!?:;»]$',previous['text']):separate=True
   if role=='body'and l['x']>previous['x']+12 and re.search(r'[.!?»]$',previous['text']):separate=True
  if not separate:
   if out[-1]['fr'].endswith('-')and re.match('[a-zà-ÿ]',t):out[-1]['fr']=out[-1]['fr'][:-1]+t
   else:out[-1]['fr']+=' '+t
  else:out.append({'fr':t,'role':role,'sourcePage':page,'extractionMethod':method})
  previous=l
 return out

def native(page):
 # The same broken ToUnicode value can mean either a plain letter or an accent.
 # Texttrace retains valid accents/capitals; recover only the missing glyphs from
 # the legacy character mapping and match the two streams by PDF coordinates.
 trace={}
 for span in page.get_texttrace():
  for code,glyph,origin,bbox in span['chars']:
   value=chr(code) if code not in [0xfffd,0] else None
   if value is None and 'Spectral' in span['font']:
    if 10<=glyph<=35:value=chr(glyph+55)
    elif 241<=glyph<=266:value=chr(glyph-144)
    else:value={73:'É',267:'à',269:'â',303:'è',305:'ê',337:'î',373:'ô',430:'ù',432:'û',434:'ü',859:',',860:';',863:'…',864:'-',868:'!',874:'‘',902:'/',920:'(',921:')',924:'[',925:']',1096:'%',1098:'+',1103:'=',1158:'ff',1161:'fi',1162:'ffi',1167:'fl',1168:'ffl',**{989+i:str(i)for i in range(10)}}.get(glyph)
   if value is not None:trace.setdefault((round(origin[0],2),round(origin[1],2)),[]).append(value)
 lines=[]
 for b in page.get_text('rawdict')['blocks']:
  for l in b.get('lines',[]):
   spans=[s for s in l['spans']if not any(x in s['font']for x in ['Hanzi','PingFang','STSong','Songti'])]
   if not spans:continue
   parts=[]
   for span in spans:
    for char in span['chars']:
     origin=char['origin'];values=trace.get((round(origin[0],2),round(origin[1],2)),[]);value=values.pop(0) if values else None
     if value is None:
      raw=char['c'];code=ord(raw)
      if code in SYMBOLS:value=SYMBOLS[code]
      elif 241<=code<=268:value=chr(code-144)
      elif code<=96 and raw!=' ':value=chr(code+29)
      else:value=decode(raw,span['font'])
     parts.append(value)
   text=''.join(parts).replace('ﬀ','ff').replace('ﬁ','fi').replace('ﬂ','fl').replace('ﬃ','ffi').replace('ﬄ','ffl')
   if not text.strip():continue
   count=sum(len(s['chars'])for s in spans)
   size=sum(s['size']*len(s['chars'])for s in spans)/max(1,count)
   bold=sum(len(s['chars'])for s in spans if any(x in s['font']for x in ['Bold','SemiBold']))/max(1,count)
   lines.append({'text':text,'x':l['bbox'][0],'y':l['bbox'][1],'right':l['bbox'][2],'size':size,'bold':bold})
 return lines

def ocr(img,psm):
 with tempfile.TemporaryDirectory()as tmp:
  path=Path(tmp)/'page.png';img.save(path)
  r=subprocess.run(['tesseract',str(path),'stdout','--tessdata-dir','/workspace/tooling/tessdata-best','-l','fra','--psm',str(psm),'-c','tessedit_create_tsv=1'],capture_output=True,text=True,check=True)
  words=[d for d in csv.DictReader(io.StringIO(r.stdout),delimiter='\t',quoting=csv.QUOTE_NONE)if d.get('text','').strip()and float(d['conf'])>=0]
  lines=collections.defaultdict(list)
  for w in words:lines[(w['block_num'],w['par_num'],w['line_num'])].append(w)
  out=[]
  for ws in lines.values():
   t=' '.join(w['text']for w in ws);conf=sum(float(w['conf'])*len(w['text'])for w in ws)/max(1,sum(len(w['text'])for w in ws))
   if conf<20:continue
   heights=[int(w['height'])for w in ws if len(w['text'])>2]
   out.append({'text':t,'x':min(int(w['left'])for w in ws),'y':min(int(w['top'])for w in ws),'right':max(int(w['left'])+int(w['width'])for w in ws),'size':statistics.median(heights)if heights else 14,'bold':0,'confidence':conf})
  tokens=[w for l in out for w in re.findall('[A-Za-zÀ-ÿœŒ]{2,}',l['text'])]
  good=sum(min(6,zipf_frequency(w.lower(),'fr'))for w in tokens)
  junk=sum(1 for w in tokens if zipf_frequency(w.lower(),'fr')<1)
  score=good-3*junk
  return out,score

def run(job):
 path,index=job;name=Path(path).name;dest=OUT/(hashlib.sha1((name+str(index)).encode()).hexdigest()[:16]+'.json')
 if dest.exists():return
 doc=fitz.open(path);page=doc[index]
 if len(page.get_text().strip())>=100:
  lines=native(page);paragraphs=combine(lines,index+1,'native-repaired');method='native-repaired';score=None
 else:
  # Read separate photographs separately, avoiding crossing the gap between them.
  regions=[r for im in page.get_images()for r in page.get_image_rects(im[0])if r.get_area()>page.rect.get_area()*.06]
  if len(regions)<2:regions=[page.rect]
  all_paras=[];score=[]
  for region in sorted(regions,key=lambda r:(r.y0,r.x0)):
   pix=page.get_pixmap(dpi=300,clip=region);rgb=Image.frombytes('RGB',(pix.width,pix.height),pix.samples)
   gray=Image.fromarray(np.asarray(rgb).max(axis=2));background=np.asarray(gray.filter(ImageFilter.GaussianBlur(22)),dtype=float)
   norm=np.minimum(255,np.asarray(gray,dtype=float)/(background+1)*255).astype('uint8')
   variants=[('original',ImageOps.autocontrast(gray)),('neutral-ink',Image.fromarray(np.where(norm<175,0,255).astype('uint8')))]
   choices=[]
   for variant,im in variants:
    ls,sc=ocr(im,6 if len(regions)>1 else 3);choices.append((sc,ls,variant))
   sc,ls,variant=max(choices,key=lambda x:x[0]);paragraphs=combine(ls,index+1,'ocr-best-'+variant)
   all_paras.extend(paragraphs);score.append({'variant':variant,'score':round(sc,2),'candidates':[(v,round(s,2))for s,_,v in choices]})
  paragraphs=all_paras;method='ocr-best'
 dest.write_text(json.dumps({'file':name,'page':index+1,'method':method,'paragraphs':paragraphs,'score':score},ensure_ascii=False,indent=2))
 print(name,index+1,method,len(paragraphs),flush=True)

if __name__=='__main__':
 jobs=[(f,i)for f in glob.glob('/workspace/attachments/*/*.pdf')if '写作'in f or '口语'in f for i in range(len(fitz.open(f)))]
 print('Revising',len(jobs),'writing and oral source pages',flush=True)
 with concurrent.futures.ThreadPoolExecutor(max_workers=4)as pool:list(pool.map(run,jobs))
 print('Done',flush=True)
