"""Read question sheets as a single column so blank answer areas don't hide stems."""
import concurrent.futures,glob,hashlib,json,os,subprocess,tempfile
from pathlib import Path
import fitz,numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'data/questions';OUT.mkdir(parents=True,exist_ok=True)
os.environ['OMP_THREAD_LIMIT']='1'
files={Path(p).name:p for p in glob.glob('/workspace/attachments/*/*.pdf')}
jobs=[]
for f in (ROOT/'data/extracted').glob('*.json'):
 d=json.loads(f.read_text());n=d['file'];p=d['page']
 if d['method']!='ocr':continue
 needed=('长听力'in n and p<=2) or ('阅读'in n and 2<=p<=4) or ('短听力'in n)
 if needed:jobs.append((n,p))
def run(job):
 n,p=job;key=hashlib.sha1((n+str(p)).encode()).hexdigest()[:16];out=OUT/(key+'.json')
 if out.exists():return
 d=fitz.open(files[n]);pix=d[p-1].get_pixmap(dpi=240)
 a=np.array(Image.frombytes('RGB',(pix.width,pix.height),pix.samples));b=a.astype('int16')
 a[(b.max(2)-b.min(2)>35)&(b.mean(2)>115)]=255
 with tempfile.TemporaryDirectory() as tmp:
  img=Path(tmp)/'q.png';Image.fromarray(a).save(img)
  r=subprocess.run(['tesseract',str(img),'stdout','--tessdata-dir','/workspace/tooling/tessdata','-l','fra','--psm','6'],capture_output=True,text=True,check=True)
  out.write_text(json.dumps({'file':n,'page':p,'text':r.stdout},ensure_ascii=False))
 print(n,p,flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:list(pool.map(run,jobs))
