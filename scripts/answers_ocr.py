import concurrent.futures,glob,hashlib,json,os,subprocess,tempfile
from pathlib import Path
import fitz
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'answers';OUT.mkdir(parents=True,exist_ok=True)
os.environ['OMP_THREAD_LIMIT']='1'
def run(p):
 d=fitz.open(p);name=Path(p).name;out=OUT/(hashlib.sha1(name.encode()).hexdigest()[:14]+'.json')
 if out.exists():return
 with tempfile.TemporaryDirectory() as tmp:
  img=Path(tmp)/'page.png';d[-1].get_pixmap(dpi=280).save(img)
  r=subprocess.run(['tesseract',str(img),'stdout','--tessdata-dir','/workspace/tooling/tessdata','-l','fra+chi_sim','--psm','6'],capture_output=True,text=True,check=True)
  out.write_text(json.dumps({'file':name,'page':len(d),'text':r.stdout},ensure_ascii=False))
 print(name,flush=True)
files={Path(p).name:p for p in glob.glob('/workspace/attachments/*/*.pdf') if ('阅读' in p or '长听力' in p or '短听力' in p)}
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:list(pool.map(run,files.values()))
