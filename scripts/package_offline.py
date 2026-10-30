"""Build the self-contained B2 HTML from the current dist assets."""
from pathlib import Path
import base64,json,re,sys
ROOT=Path(__file__).resolve().parents[1];DIST=ROOT/'dist'
OUT=Path(sys.argv[1]) if len(sys.argv)>1 else ROOT/'downloads/胡桃法语-DELF-B2-双击打开.html'
html=(DIST/'index.html').read_text().replace('<html lang="zh-CN">','<html lang="zh-CN" data-noix-offline>')
bank=json.loads((DIST/'content.json').read_text())
css_match=re.search(r'<link rel="stylesheet"[^>]*href="([^"]+)"[^>]*>',html)
js_match=re.search(r'<script type="module"[^>]*src="([^"]+)"[^>]*></script>',html)
assert css_match and js_match
css=(DIST/css_match[1].lstrip('/')).read_text();js=(DIST/js_match[1].lstrip('/')).read_text()
for font in (DIST/'fonts').glob('*.ttf'):
 css=css.replace('/fonts/'+font.name,'data:font/ttf;base64,'+base64.b64encode(font.read_bytes()).decode())
images={p.name:'data:image/'+('svg+xml' if p.suffix=='.svg' else 'png')+';base64,'+base64.b64encode(p.read_bytes()).decode() for p in (DIST/'images').iterdir() if p.suffix in ['.png','.svg']}
payload=json.dumps(bank,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')
html=html.replace(css_match[0],'<style>'+css+'</style>').replace(js_match[0],'')
embedded='<script>window.__NOIX_EMBEDDED_IMAGES__='+json.dumps(images,separators=(',',':'))+';window.__NOIX_EMBEDDED_BANK__='+payload+';</script>'
app='<script type="module">'+js.replace('</script','<\\/script')+'</script>'
html=html.replace('</body>',embedded+app+'</body>')
OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(html)
assert len(bank['exercises'])==297
assert not any(e.get('audio') for e in bank['exercises'])
assert '/fonts/Journal.ttf' not in css
assert 'imageAsset' not in js
print(f'{OUT.name}: {OUT.stat().st_size/1024/1024:.1f} MiB, {len(bank["exercises"])} exercises')
