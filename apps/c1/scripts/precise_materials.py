"""Re-extract materials using PDF trace characters and column-aware reading order.
The previous rawdict/trace positional pairing could skip the second letter of fi/fl.
All changed source paragraphs retain page provenance; uncertain OCR is recorded.
"""
import sys,glob,json,re,hashlib,collections,statistics,subprocess,tempfile,csv,io,os
from pathlib import Path
sys.path.insert(0,'/workspace/work/python-refinements')
import fitz
from PIL import Image,ImageFilter,ImageOps
import numpy as np
from wordfreq import zipf_frequency
ROOT=Path(__file__).resolve().parents[1];CACHE=Path(os.environ.get('NOIX_PRECISE_PAGES','/workspace/work/precise-pages'));CACHE.mkdir(exist_ok=True)
os.environ['OMP_THREAD_LIMIT']='1'
SYMBOLS={73:'É',267:'à',269:'â',303:'è',305:'ê',337:'î',373:'ô',430:'ù',432:'û',434:'ü',859:',',860:';',863:'…',864:'-',868:'!',874:'‘',902:'/',920:'(',921:')',924:'[',925:']',1096:'%',1098:'+',1103:'=',1158:'ff',1161:'fi',1162:'ffi',1167:'fl',1168:'ffl',**{989+i:str(i)for i in range(10)}}
def repair(code,gid,font):
 if code not in [0xfffd,0]:return chr(code)
 if 'Spectral' in font:
  if 10<=gid<=35:return chr(gid+55)
  if 241<=gid<=266:return chr(gid-144)
  return SYMBOLS.get(gid,'�')
 if 3<=gid<=96:return chr(gid+29)
 return {106:'à',107:'â',108:'ä',111:'ç',112:'é',113:'è',114:'ê',115:'ë',118:'î',119:'ï',123:'ô',124:'ö',127:'ù',128:'û',129:'ü',182:'’',191:'fi',192:'fl'}.get(gid,'�')
def tidy(s):
 s=s.replace('\u00ad','').replace('ﬁ','fi').replace('ﬂ','fl').replace('ﬀ','ff').replace('ﬃ','ffi').replace('ﬄ','ffl')
 s=re.sub(r'\s+',' ',s).strip()
 return s

def trace_lines(page):
 chars=[]
 for span in page.get_texttrace():
  if any(x in span['font']for x in ['Hanzi','PingFang','STSong','Songti']):continue
  for code,gid,origin,bbox in span['chars']:
   ch=repair(code,gid,span['font']);chars.append({'text':ch,'origin':origin,'bbox':bbox,'font':span['font'],'size':span['size'],'bold':any(x in span['font']for x in ['Bold','SemiBold'])})
 lines=[]
 for block in page.get_text('dict')['blocks']:
  for line in block.get('lines',[]):
   box=line['bbox'];baselines=[span['origin'][1]for span in line['spans']];selected=[c for c in chars if box[0]-.5<=c['origin'][0]<=box[2]+.5 and min(abs(c['origin'][1]-y)for y in baselines)<.65]
   # Stable sorting preserves both characters of a ligature at shared coordinates.
   if not selected:continue
   selected.sort(key=lambda c:c['origin'][0]);text=''.join(c['text']for c in selected)
   text=tidy(text)
   if not text:continue
   lines.append({'fr':text,'x':box[0],'y':box[1],'right':box[2],'bottom':box[3],'size':statistics.median(c['size']for c in selected),'bold':sum(c['bold']for c in selected)/len(selected)})
 # A draw layer may expose the same physical line twice.
 return list({(round(l['x'],1),round(l['y'],1),l['fr']):l for l in lines}.values())
def cleanline(t):
 t=tidy(t)
 if re.search('[\u3400-\u9fff]',t):t=re.sub('[\u3400-\u9fff]','',t).strip()
 if not t or re.match(r'^(?:Cours\s+\d+|DOCUMENT RÉSERVÉ|ÉPREUVES COLLECTIVES|LETTRES ET SCIENCES|Page\s+\d|\d{1,3}$|DALF\s+C1\s*$)',t,re.I):return ''
 if re.search(r'DELF.{0,4}DALF.{0,20}(?:É|E|R|C1)|EXAMEN DU|DOCUMENT.{0,30}CANDIDAT',t,re.I):return ''
 return t

def ordered(lines,width):
 lines=[dict(l,fr=cleanline(l['fr']))for l in lines];lines=[l for l in lines if l['fr']]
 body=statistics.median(l['size']for l in lines if len(l['fr'])>25)if any(len(l['fr'])>25 for l in lines)else 11
 mid=width/2;right=[l for l in lines if l['x']>mid-10];right_start=statistics.median(l['x']for l in right)if right else mid+10;left=[l for l in lines if l['x']<mid-30 and l['right']<right_start-3]
 if len(left)<5 or len(right)<5:return sorted(lines,key=lambda l:(round(l['y']/3),l['x'])),False
 full=[l for l in lines if l not in left and l not in right]
 # Full-width headings/intros separate horizontal bands; within each band read
 # the entire left column before the right, never alternating line by line.
 result=[];remaining=[l for l in lines if l not in full]
 for line in sorted(full,key=lambda l:l['y']):
  before=[l for l in remaining if l['y']<line['y']-2];remaining=[l for l in remaining if l not in before]
  result+=sorted(before,key=lambda l:(0 if l['x']<mid else 1,l['y']))
  result.append(line)
 result+=sorted(remaining,key=lambda l:(0 if l['x']<mid else 1,l['y']))
 return result,True

def paragraphs(lines,page,method):
 if not lines:return []
 body=statistics.median(l['size']for l in lines if len(l['fr'])>35)if any(len(l['fr'])>35 for l in lines)else 11
 gaps=[b['y']-a['y']for a,b in zip(lines,lines[1:])if 3<b['y']-a['y']<body*2.5 and abs(a['x']-b['x'])<20]
 gap=statistics.median(gaps)if gaps else body*1.3;out=[];previous=None
 for l in lines:
  t=l['fr'];role='body'
  if re.match(r'^(?:[>»]\s*)?DOCUMENT\s*(?:N[°o]?\s*)?[12]\b',t,re.I):role='document'
  elif re.match(r'^Thème de l[’\']exposé',t,re.I):role='label'
  elif (l['bold']>.65 or l['size']>body*1.15)and len(t)<210:role='heading'
  elif l['size']<body*.86 and re.match(r'^(?:\*|[¹²³]|\d\s*[.)])',t):role='note'
  elif re.search(r'^(?:D.après|Source\s*:)|www\.|https?://',t)and len(t)<180:role='source'
  separate=not out or role!=out[-1]['role'] or role in ['document','label','source']
  if previous:
   if l['y']<previous['y']-3 or abs(l['x']-previous['x'])>80:separate=not(role=='body' and out and out[-1]['role']=='body' and not re.search(r'[.!?;»]$',out[-1]['fr']))
   if l['y']-previous['y']>gap*1.48:separate=True
   if role=='heading' and out and out[-1]['role']=='heading' and re.match('[a-zà-ÿœ]',t) and not re.search(r'[.!?;»]$',out[-1]['fr']) and l['y']-previous['y']<l['size']*1.8:separate=False
   if role=='body'and previous['right']<l['right']-25 and re.search(r'[.!?;»]$',previous['fr']):separate=True
  if not separate:
   prev=out[-1]['fr'];out[-1]['fr']=prev[:-1]+t if prev.endswith('-')and re.match('[a-zà-ÿ]',t)else prev+' '+t
  else:out.append({'fr':t,'role':role,'sourcePage':page,'extractionMethod':method})
  previous=l
 for p in out:
  if p['role']=='heading'and len(p['fr'])>300:p['role']='body'
 return out

def ocr_lines(page):
 pix=page.get_pixmap(dpi=300);rgb=np.frombuffer(pix.samples,dtype=np.uint8).reshape(pix.height,pix.width,3)
 gray=Image.fromarray(rgb.max(axis=2));background=np.asarray(gray.filter(ImageFilter.GaussianBlur(22)),dtype=float);norm=np.minimum(255,np.asarray(gray,dtype=float)/(background+1)*255).astype('uint8');img=Image.fromarray(np.where(norm<175,0,255).astype('uint8'))
 with tempfile.TemporaryDirectory()as tmp:
  path=Path(tmp)/'page.png';img.save(path)
  p=subprocess.run(['tesseract',str(path),'stdout','--tessdata-dir','/workspace/work/tessdata-best','-l','fra','--psm','3','-c','tessedit_create_tsv=1'],capture_output=True,text=True,check=True)
  groups=collections.defaultdict(list)
  for w in csv.DictReader(io.StringIO(p.stdout),delimiter='\t',quoting=csv.QUOTE_NONE):
   if w.get('text','').strip() and float(w.get('conf',-1))>=25:groups[(w['block_num'],w['par_num'],w['line_num'])].append(w)
  scale=page.rect.width/pix.width;out=[]
  for ws in groups.values():
   text=tidy(' '.join(w['text']for w in ws));heights=[int(w['height'])for w in ws if len(w['text'])>2]
   out.append({'fr':text,'x':min(int(w['left'])for w in ws)*scale,'y':min(int(w['top'])for w in ws)*scale,'right':max(int(w['left'])+int(w['width'])for w in ws)*scale,'bottom':max(int(w['top'])+int(w['height'])for w in ws)*scale,'size':statistics.median(heights)*scale if heights else 10,'bold':0})
  return out

def process(job):
 file,pageno=job;dest=CACHE/(hashlib.sha1((file+str(pageno)).encode()).hexdigest()+'.json')
 if dest.exists():return json.loads(dest.read_text())
 doc=fitz.open(glob.glob('/workspace/attachments/*/'+file)[0]);page=doc[pageno-1]
 native=len(page.get_text().strip())>100
 method='trace-characters';lines=trace_lines(page)if native else ocr_lines(page)
 if not native:method='ocr-fra-best-300dpi'
 elif any(re.search(r'[{}¶�]|\b(?:rrves|pveillp|refeet|artiÀcielle)\b',l['fr'])for l in lines):
  lines=ocr_lines(page);method='ocr-fra-best-300dpi-legacy-encoding'
 ls,columns=ordered(lines,page.rect.width);ps=paragraphs(ls,pageno,method)
 result={'file':file,'page':pageno,'columns':columns,'method':method,'paragraphs':ps,'lines':ls}
 dest.write_text(json.dumps(result,ensure_ascii=False,indent=2));print(file,pageno,method,len(ps),flush=True);return result
if __name__=='__main__':
 import concurrent.futures
 bank=json.loads((ROOT/'public/content.json').read_text());jobs=sorted(set((e['sourceFiles'][0],p['sourcePage'])for e in bank['exercises']if e['category']in ['writing','speaking']for p in e['paragraphs']))
 if '--sample'in sys.argv:jobs=[j for j in jobs if j[0].startswith('C1第一')and j[1]in[1,2,3,4,69,70]]
 with concurrent.futures.ThreadPoolExecutor(max_workers=4)as pool:results=list(pool.map(process,jobs))
 print('Rechecked source pages',len(results),flush=True)
