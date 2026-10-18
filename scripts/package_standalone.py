"""Make one offline HTML file containing the app, complete bank and all audio."""
from pathlib import Path
import base64,json,re,shutil

ROOT=Path(__file__).resolve().parents[1]
DIST=ROOT/'dist'
OUT=ROOT.parent/'wangzhan-release'/'胡桃法语-DALF-C1-双击打开.html'
html=(DIST/'index.html').read_text()
bank=json.loads((DIST/'content.json').read_text())
for e in bank['exercises']:
    if e.get('audio'):
        path=DIST/e['audio'].lstrip('/')
        mime='audio/mpeg' if path.suffix=='.mp3' else 'audio/mp4'
        e['audio']='data:'+mime+';base64,'+base64.b64encode(path.read_bytes()).decode('ascii')
css_match=re.search(r'<link rel="stylesheet"[^>]*href="([^"]+)"[^>]*>',html)
js_match=re.search(r'<script type="module"[^>]*src="([^"]+)"[^>]*></script>',html)
assert css_match and js_match
css=(DIST/css_match[1].lstrip('/')).read_text()
js=(DIST/js_match[1].lstrip('/')).read_text()
payload=json.dumps(bank,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')
html=html.replace(css_match[0],'<style>'+css+'</style>')
html=html.replace(js_match[0],'')
embedded='<script>window.__NOIX_EMBEDDED_BANK__='+payload+';</script>'
lexicon=(DIST/'lexicon.json').read_text().replace('<','\\u003c')
embedded+='<script type="application/json" id="noix-lexicon">'+lexicon+'</script>'
app='<script type="module">'+js.replace('</script','<\\/script')+'</script>'
html=html.replace('</body>',embedded+app+'</body>')
OUT.parent.mkdir(exist_ok=True)
OUT.write_text(html)
shutil.copyfile(OUT,ROOT/OUT.name)
assert len(bank['exercises'])==176
assert sum(bool(e.get('audio')) for e in bank['exercises'])==36
print(f'{OUT} ({OUT.stat().st_size/1024/1024:.1f} MiB; 176 exercise sets and 36 embedded audio files)')
