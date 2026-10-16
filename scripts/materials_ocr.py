"""Recover body lines hidden by watermark-aware thresholding on photographed pages."""
import concurrent.futures,glob,json,os,subprocess,tempfile
from pathlib import Path
import fitz
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'data/materials';OUT.mkdir(parents=True,exist_ok=True)
os.environ['OMP_THREAD_LIMIT']='1'
files={Path(p).name:p for p in glob.glob('/workspace/attachments/*/*.pdf')}
jobs=[]
for f in (ROOT/'data/extracted').glob('*.json'):
 d=json.loads(f.read_text());n=d['file'];p=d['page']
 if d['method']!='ocr':continue
 needed=('写作'in n) or ('阅读'in n and p<=2) or ('长听力'in n and p>=3 and p<d['pages']) or ('口语'in n)
 if needed:jobs.append((f,d))
def run(job):
 f,meta=job;dest=OUT/f.name
 if dest.exists():return
 d=fitz.open(files[meta['file']]);page=d[meta['page']-1]
 with tempfile.TemporaryDirectory() as tmp:
  img=Path(tmp)/'p.png';page.get_pixmap(dpi=250).save(img)
  r=subprocess.run(['tesseract',str(img),'stdout','--tessdata-dir','/workspace/tooling/tessdata','-l','fra','--psm','3' if '口语'in meta['file'] else '6'],capture_output=True,text=True,check=True)
  text=r.stdout
  if len(text.strip())<150 and page.get_images():
   parts=[]
   rects=[rect for im in page.get_images() for rect in page.get_image_rects(im[0])]
   for rect in sorted(rects,key=lambda r:(r.y0,r.x0)):
    if rect.get_area()<page.rect.get_area()*.03:continue
    page.get_pixmap(dpi=280,clip=rect).save(img)
    r=subprocess.run(['tesseract',str(img),'stdout','--tessdata-dir','/workspace/tooling/tessdata','-l','fra','--psm','6'],capture_output=True,text=True,check=True)
    parts.append(r.stdout)
   text='\n\n'.join(parts)
  dest.write_text(json.dumps({**meta,'text':text},ensure_ascii=False))
 print(meta['file'],meta['page'],flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:list(pool.map(run,jobs))
