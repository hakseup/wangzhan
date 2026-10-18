"""Real-browser dictionary, note filtering and independent highlight removal checks.
The online provider is intercepted; no selected text leaves this test browser.
"""
import os,json
from urllib.parse import urlparse,parse_qs
from playwright.sync_api import sync_playwright,expect
BASE=os.environ.get('NOIX_TEST_URL','http://127.0.0.1:5173').rstrip('/')
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
 page=browser.new_page(viewport={'width':1440,'height':1080});errors=[];requests=[]
 page.on('pageerror',lambda e:errors.append(str(e)))
 def provider(route):
  text=parse_qs(urlparse(route.request.url).query)['q'][0];requests.append(text)
  if text=='Échec de réseau simulé':route.abort('failed');return
  definitions=[['noun',['测试新词']]] if text=='néologismetest' else None
  route.fulfill(status=200,content_type='application/json',body=json.dumps([[['这是一条仅供测试的中文翻译。']],definitions]))
 page.route('https://translate.googleapis.com/**',provider)
 page.goto(BASE+'#reading-2024-3-cn');page.wait_for_selector('[data-paragraph="p0"]')
 def select(word,pid='p0'):
  page.evaluate('''({word,pid})=>{const p=document.querySelector(`[data-paragraph="${pid}"]`);const w=document.createTreeWalker(p,NodeFilter.SHOW_TEXT);let n;while(n=w.nextNode()){if(n.parentElement.closest('sup'))continue;const i=n.textContent.indexOf(word);if(i>=0){const r=document.createRange();r.setStart(n,i);r.setEnd(n,i+word.length);const s=getSelection();s.removeAllRanges();s.addRange(r);p.dispatchEvent(new MouseEvent('mouseup',{bubbles:true}));return;}}throw Error('word not found: '+word);}''',dict(word=word,pid=pid))
 select('marche');page.get_by_role('button',name='高亮',exact=True).click()
 select('sens');page.get_by_role('button',name='高亮',exact=True).click()
 page.locator('mark').filter(has_text='marche').click();page.get_by_role('button',name='查词 / 译句',exact=True).click()
 expect(page.locator('.lookup-entry').first).to_be_visible(timeout=30000)
 note=page.get_by_label('查词备注');note.fill('n. 步行；台阶。搭配：se mettre en marche。')
 page.get_by_role('button',name='保存备注',exact=True).click();expect(page.get_by_role('button',name='备注已保存')).to_be_visible()
 page.get_by_role('button',name='关闭对话框',exact=True).click()
 mark=page.locator('mark.word-note');mark.click();page.get_by_role('button',name='删除高亮',exact=True).click()
 expect(page.locator('mark.word-note.level-0')).to_have_count(1)
 page.get_by_role('button',name='单词与笔记',exact=True).click();expect(page.locator('.note-card')).to_have_count(1)
 expect(page.locator('.notebook-page')).not_to_contain_text('全部标注')
 page.get_by_role('button',name='编辑备注',exact=True).click();page.get_by_role('textbox',name='编辑词汇备注',exact=True).fill('n. 步行；台阶；运行。')
 page.get_by_role('button',name='保存修改',exact=True).click();expect(page.locator('.note-card')).to_contain_text('运行')
 page.get_by_role('button',name='打开词典',exact=True).click()
 field=page.get_by_label('查询法语单词、短语或句子')
 def query(text):field.fill(text);page.get_by_role('button',name='查询',exact=True).click()
 query('pouvoir');expect(page.locator('.lookup-entry')).to_contain_text('n. 名词');expect(page.locator('.lookup-entry')).to_contain_text('v. 动词')
 assert not requests,requests
 query('étaient');expect(page.locator('.lookup-entry').first).to_contain_text('être')
 query('a pris en compte');expect(page.locator('.lookup-entry')).to_contain_text('prendre en compte');expect(page.locator('.lookup-components')).to_contain_text('pris')
 query('Il faut tenir compte des différences.');expect(page.locator('.lookup-translation')).to_contain_text('必须考虑到各种差异')
 query('Cette combinaison volontairement inédite attend sa traduction complète');expect(page.locator('.lookup-translation')).to_contain_text('仅供测试')
 assert requests==['Cette combinaison volontairement inédite attend sa traduction complète'],requests
 page.locator('.lookup-network-switch input').uncheck()
 query('Une deuxième combinaison volontairement inédite');expect(page.locator('.lookup-missing')).to_be_visible();assert len(requests)==1
 page.get_by_role('button',name='联网翻译所选文字').click();expect(page.locator('.lookup-translation')).to_contain_text('仅供测试');assert len(requests)==2
 query('néologismetest');page.get_by_role('button',name='联网翻译所选文字').click();expect(page.locator('.lookup-entry')).to_contain_text('n. 名词');expect(page.locator('.lookup-entry')).to_contain_text('测试新词')
 query('Échec de réseau simulé');page.get_by_role('button',name='联网翻译所选文字').click();expect(page.locator('.lookup-network [role=alert]')).to_contain_text('联网查询失败')
 page.set_viewport_size({'width':390,'height':844});assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
 page.screenshot(path='/tmp/noix-lookup-mobile.png')
 page.get_by_role('button',name='关闭对话框',exact=True).click();page.reload();page.set_viewport_size({'width':1440,'height':1080});page.get_by_role('button',name='单词与笔记',exact=True).click();page.get_by_role('button',name='打开词典',exact=True).click();expect(page.locator('.lookup-network-switch input')).not_to_be_checked()
 query('néologismetest');expect(page.locator('.lookup-entry')).to_contain_text('测试新词');assert len(requests)==4
 page.get_by_role('button',name='关闭对话框',exact=True).click()
 page.set_viewport_size({'width':1440,'height':1080});page.goto(BASE+'#reading-2024-3-cn');page.locator('mark.word-note').click();page.get_by_role('button',name='切换颜色',exact=True).click();expect(page.locator('mark.word-note.level-1')).to_have_count(1)
 page.get_by_role('button',name='单词与笔记',exact=True).click();page.get_by_role('button',name='删除笔记',exact=True).click();page.get_by_role('button',name='删除',exact=True).click();expect(page.locator('.note-card')).to_have_count(0)
 page.goto(BASE+'#reading-2024-3-cn');expect(page.locator('mark.level-1')).to_have_count(2)
 assert not errors,errors
 print('PASS: dictionary POS/forms/idiom components/sentence translation; local-first automatic online fallback, manual fallback and saved preference; notes-only collection/edit/delete; highlight deletion preserves notes and note deletion preserves highlights; mobile overflow; no browser errors.')
 browser.close()
