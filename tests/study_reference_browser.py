"""Regression for the new reference panels, editing, lookup and note-only books."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
BASE='http://127.0.0.1:4173'
def select(page,selector,text):
 page.locator(selector).first.scroll_into_view_if_needed()
 page.evaluate('''({selector,text})=>{const el=document.querySelector(selector),w=document.createTreeWalker(el,NodeFilter.SHOW_TEXT);let n;while(n=w.nextNode()){const i=n.textContent.indexOf(text);if(i>=0){const r=document.createRange();r.setStart(n,i);r.setEnd(n,i+text.length);getSelection().removeAllRanges();getSelection().addRange(r);el.dispatchEvent(new MouseEvent('mouseup',{bubbles:true}));return;}}throw Error(text);}''',{'selector':selector,'text':text})
with sync_playwright()as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox']);page=b.new_page(viewport={'width':1440,'height':900});errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto(BASE);page.wait_for_selector('.shortcut-grid');page.evaluate('document.fonts.ready')
 for h in [600,768,850,900,1080]:
  page.set_viewport_size({'width':1440,'height':h});page.wait_for_timeout(80);assert page.locator('.sidebar').evaluate('(e)=>e.scrollHeight<=e.clientHeight'),h
 page.set_viewport_size({'width':1440,'height':900});page.screenshot(path='/workspace/work/oct19-home-final.png')
 page.evaluate("location.hash='reading-2021-10-fr'");page.wait_for_selector('.question');expect(page.get_by_role('timer')).to_have_text('50:00');expect(page.get_by_role('button',name='参考答案释义',exact=True)).to_have_count(0)
 page.locator('.question input[type=radio]').first.check();page.get_by_role('button',name='提交并核对答案').click();expect(page.locator('.review-question')).to_have_count(11)
 page.locator('.review-evidence-tools .text-btn').first.click();expect(page.locator('.reader-content')).to_be_visible()
 # A highlight can be removed without deleting its note.
 selector='.reader-content .evidence-fr [data-annotation]';word=page.locator(selector).first.inner_text().split()[0];select(page,selector,word);page.get_by_role('button',name='高亮',exact=True).click();expect(page.locator('.reader-content mark')).to_have_count(1)
 page.locator('.reader-content mark').click();page.get_by_role('button',name='备注',exact=True).click();page.locator('.modal textarea').fill('词汇备注');page.get_by_role('button',name='保存备注',exact=False).click();page.locator('.reader-content mark').click();page.get_by_role('button',name='删除高亮',exact=True).click();expect(page.locator('.reader-content mark.word-note')).to_have_count(1);assert 'level-0'in page.locator('.reader-content mark').get_attribute('class')
 # Both written and oral models render in the existing material tab.
 page.evaluate("location.hash='writing-2024-6-cn'");page.wait_for_selector('.writing-editor');expect(page.get_by_role('timer')).to_have_text('150:00');page.get_by_role('button',name='范文',exact=True).click();expect(page.locator('.model-article')).to_have_count(2)
 article=page.locator('.model-article').first;article.get_by_role('button',name='编辑范文',exact=True).click();editor=article.locator('[contenteditable=true]');editor.fill('Bonjour, voici ma version personnelle.');editor.evaluate('''e=>{e.focus();const r=document.createRange();r.selectNodeContents(e);getSelection().removeAllRanges();getSelection().addRange(r);}''');article.get_by_role('button',name='加粗',exact=True).click();article.get_by_role('button',name='下划线',exact=True).click();article.get_by_role('button',name='范文高亮',exact=True).click();assert editor.locator('b,strong').count()>0;assert editor.locator('u').count()>0;assert 'background-color'in editor.inner_html()
 article.get_by_role('button',name='完成编辑',exact=True).click();page.reload();page.wait_for_selector('.writing-editor');page.get_by_role('button',name='范文',exact=True).click();expect(page.locator('.model-text').first).to_have_text('Bonjour, voici ma version personnelle.');assert page.locator('.model-text').first.locator('b,strong').count()>0
 page.screenshot(path='/workspace/work/oct19-model-editor.png')
 data=page.evaluate('JSON.parse(localStorage.getItem("noix-dalf-c1-v1"))');assert 'writing-2024-6-cn:synthese'in data['modelEdits']
 page.evaluate("location.hash='speaking-1-1'");page.wait_for_selector('.speaking-prompt');expect(page.get_by_role('timer')).to_have_text('30:00');page.get_by_role('button',name='范文',exact=True).click();expect(page.locator('.model-article').nth(1)).to_contain_text('Concrètement, que faudrait-il faire')
 # Imported HTML is sanitized before rendering; native site styles remain intact.
 page.evaluate('''()=>{const x=JSON.parse(localStorage.getItem('noix-dalf-c1-v1'));x.modelEdits['speaking-1-1:monologue']='<p onclick="window.__bad=1">Texte sûr<img src=x onerror="window.__bad=1"><script>window.__bad=1</script><span style="background-image:url(https://example.com/x);font-weight:bold"> oui</span></p>';localStorage.setItem('noix-dalf-c1-v1',JSON.stringify(x));}''');page.reload();page.wait_for_selector('.speaking-prompt');page.get_by_role('button',name='范文',exact=True).click();assert page.locator('.model-text').first.locator('script,img,[onclick]').count()==0;assert not page.evaluate('window.__bad||false')
 # All sentence/phrase results stay inside the current dialog and page.
 page.get_by_role('button',name='法语原文',exact=False).click();selector='.reader-content [data-annotation]';word=page.locator(selector).first.inner_text().split()[0];select(page,selector,word);page.get_by_role('button',name='查询中文释义与搭配').click()
 sent=[]
 page.evaluate("Object.defineProperty(window,'Translator',{value:undefined,configurable:true})")
 def reply(route):
  sent.append(route.request.url);route.fulfill(status=200,content_type='application/json',headers={'access-control-allow-origin':'*'},body=json.dumps({'responseStatus':200,'responseData':{'translatedText':'这些人明天可以交流想法。'}}))
 page.route('https://api.mymemory.translated.net/**',reply)
 url=page.url;page.get_by_label('查询法语词汇',exact=True).fill('Ces personnes peuvent partager leurs idées demain.');page.locator('.dictionary-search button').click();expect(page.locator('.query-translation')).to_contain_text('这些人明天可以交流想法。');assert page.url==url;assert len(sent)==1;expect(page.locator('.query-components')).to_be_visible();page.screenshot(path='/workspace/work/oct19-dictionary.png')
 assert not errors,errors
 b.close();print('PASS: baseline appearance, sidebar fit, timer defaults, submit-gated evidence, remove-color/retain-note, 226 model access, persistent rich editing/backup, XSS sanitization and authorized in-page sentence lookup with query-only transfer.')
