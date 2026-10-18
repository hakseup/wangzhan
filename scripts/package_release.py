"""Package the built static website and the editable source, excluding uploaded PDFs."""
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED,ZIP_STORED
import json
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT.parent/'wangzhan-release';OUT.mkdir(exist_ok=True)
def add(archive,path,name):
 archive.write(path,name,compress_type=ZIP_STORED if path.suffix in ['.m4a','.mp3']else ZIP_DEFLATED,compresslevel=5)
site=OUT/'noix-dalf-c1-site.zip';source=OUT/'noix-dalf-c1-source.zip'
with ZipFile(site,'w')as z:
 for p in sorted((ROOT/'dist').rglob('*')):
  if p.is_file():add(z,p,str(p.relative_to(ROOT/'dist')))
 add(z,ROOT/'README.md','部署与使用说明.md');add(z,ROOT/'CONTENT_SOURCES.md','材料与参考译文说明.md')
 add(z,ROOT/'data/dictionary/NOTICE.md','dictionary-NOTICE.md');add(z,ROOT/'data/dictionary/CC-BY-SA-4.0.txt','dictionary-CC-BY-SA-4.0.txt')
with ZipFile(source,'w')as z:
 for name in ['package.json','package-lock.json','index.html','.gitignore','README.md','CONTENT_SOURCES.md']:
  add(z,ROOT/name,'noix-dalf-c1/'+name)
 for directory in ['src','public','scripts','tests','data/templates']:
  for p in sorted((ROOT/directory).rglob('*')):
   if p.is_file()and'__pycache__'not in p.parts:add(z,p,'noix-dalf-c1/'+str(p.relative_to(ROOT)))
 for name in ['overrides.json','translations.json','audio-supplements.json','writing-tasks.json','import-audit.json','validation-report.json','content-corrections.json','model-profiles.tsv','oral-causes.json','synthese-notes.tsv','explanation-reasons.json','evidence-locations.json','translation-edits.json','question-translations.tsv','option-translations.tsv','paragraph-translations.tsv','name-variants.tsv','revised-translations.json','name-glossary.json','protected-names.json','evidence-audit.json','model-audit.json','unreadable-paragraphs.json']:
  add(z,ROOT/'data'/name,'noix-dalf-c1/data/'+name)
 for pattern in ['*.tsv','*.md','*.txt']:
  for p in sorted((ROOT/'data/dictionary').glob(pattern)):add(z,p,'noix-dalf-c1/data/dictionary/'+p.name)
for path in [site,source]:
 with ZipFile(path)as z:
  assert z.testzip()is None
  assert not any(n.endswith('.pdf')or'node_modules/'in n or'/.git/'in n for n in z.namelist())
  bank=json.loads(z.read('content.json'if path==site else'noix-dalf-c1/public/content.json'))
  assert len(bank['exercises'])==176
  assert len([n for n in z.namelist()if n.endswith(('.m4a','.mp3'))])==36
 print(path.name,round(path.stat().st_size/1024/1024,1),'MiB; integrity verified')
