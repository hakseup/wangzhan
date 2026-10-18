"""Reapply the reviewed editorial changes and regenerate references (optional maintenance)."""
from pathlib import Path
import json,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
p=ROOT/'public/content.json';bank=json.loads(p.read_text());corrections=json.loads((ROOT/'data/content-corrections.json').read_text())
for e in bank['exercises']:
 if e['id'] in corrections:e.update(corrections[e['id']])
p.write_text(json.dumps(bank,ensure_ascii=False,separators=(',',':')))
for script in ['build_references.py','attach_explanations.py','merge_references.py']:
 subprocess.run([sys.executable,str(ROOT/'scripts'/script)],check=True,cwd=ROOT)
