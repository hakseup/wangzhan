"""Extract selectable text from supplied PDFs; OCR image-only pages. No PDF images are served."""
import concurrent.futures, glob, hashlib, json, os, re, subprocess, tempfile
from pathlib import Path
import fitz
import numpy as np
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
CACHE=ROOT/'data'/'extracted'
CACHE.mkdir(parents=True,exist_ok=True)
os.environ['OMP_THREAD_LIMIT']='1'

def repair_span(s):
    if '\x03' in s:
        accents={'j':'à','k':'â','p':'é','q':'è','r':'ê','s':'ë','v':'î','w':'ï','{':'ô','|':'ö','\u007f':'ù','\u0080':'û','¶':'’','¿':'fi','À':'fl','±':'—','«':'«','»':'»'}
        return ''.join(' ' if c==' ' else chr(ord(c)+29) if ord(c)<=96 else accents.get(c,c) for c in s)
    if sum(s.count(c) for c in 'þõñĄĂă÷')>0 or (len(s)==1 and 241<=ord(s)<=268):
        return ''.join(chr(ord(c)-144) if 241<=ord(c)<=268 else c for c in s)
    return s

def clean(s):
    s=re.sub(r'法语课代表|大脸法语|微信公众号[^\n]*|扫描全能王[^\n]*','',s)
    return re.sub(r'[\x00-\x08\x0b-\x1f]','',s)

def extract(job):
    p,i=job
    key=hashlib.sha1((Path(p).name+str(i)).encode()).hexdigest()[:16]
    out=CACHE/(key+'.json')
    if out.exists(): return
    doc=fitz.open(p); page=doc[i]
    text=page.get_text(sort=True)
    method='native'
    native_lines=[]
    for b in page.get_text('dict')['blocks']:
        for line in b.get('lines',[]):
            parts=[]
            for span in line['spans']:
                raw=span['text']; fixed=repair_span(raw)
                parts.append(fixed)
            native_lines.append({'bbox':line['bbox'],'text':''.join(parts)})
    if len(text.strip())>=90 and '口语' in Path(p).name:
        blocks=[]
        for b in page.get_text('dict')['blocks']:
            lines=[]
            for line in b.get('lines',[]):
                lines.append(''.join(repair_span(s['text']) for s in line['spans']))
            if lines:blocks.append('\n'.join(lines))
        text='\n\n'.join(blocks)
    elif len(text.strip())>=90:
        rows=[]
        for l in sorted(native_lines,key=lambda x:(round(x['bbox'][1]/3),x['bbox'][0])):
            if rows and abs(rows[-1]['y']-l['bbox'][1])<4:
                rows[-1]['parts'].append(l)
            else:rows.append({'y':l['bbox'][1],'parts':[l]})
        lines=[];previous=None
        for row in rows:
            if previous is not None and row['y']-previous>19:lines.append('')
            lines.append(' '.join(l['text'] for l in sorted(row['parts'],key=lambda x:x['bbox'][0])))
            previous=row['y']
        text='\n'.join(lines)
    if len(re.sub(r'\s','',text))<90:
        method='ocr'
        with tempfile.TemporaryDirectory() as tmp:
            img=Path(tmp)/'page.png'
            pix=page.get_pixmap(dpi=230)
            a=np.array(Image.frombytes('RGB',(pix.width,pix.height),pix.samples)).astype('int16')
            mask=(a.max(2)-a.min(2)<40)&(a.mean(2)<180)
            Image.fromarray(np.where(mask,0,255).astype('uint8')).save(img)
            result=subprocess.run(['tesseract',str(img),'stdout','--tessdata-dir','/workspace/tooling/tessdata','-l','fra','--psm','3'],capture_output=True,text=True,check=True)
            text=result.stdout
            if len(text.strip())<150:
                pix.save(img)
                result=subprocess.run(['tesseract',str(img),'stdout','--tessdata-dir','/workspace/tooling/tessdata','-l','fra','--psm','3'],capture_output=True,text=True,check=True)
                text=result.stdout
    out.write_text(json.dumps({'file':Path(p).name,'page':i+1,'pages':len(doc),'method':method,'text':clean(text)},ensure_ascii=False))

if __name__=='__main__':
    pdfs={Path(p).name:p for p in glob.glob('/workspace/attachments/*/*.pdf')}
    jobs=[(p,i) for p in pdfs.values() for i in range(len(fitz.open(p)))]
    print(f'Extracting {len(pdfs)} PDFs / {len(jobs)} pages',flush=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
        for n,_ in enumerate(pool.map(extract,jobs),1):
            if n%20==0: print(f'{n}/{len(jobs)} pages',flush=True)
    print('Extraction complete',flush=True)
