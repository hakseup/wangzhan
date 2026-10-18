"""Exercise reference tabs, rich editing and offline persistence in a real browser."""
import os,json
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
BASE=os.environ.get('NOIX_TEST_URL','http://127.0.0.1:5173').rstrip('/')
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
 page=browser.new_page(viewport={'width':1440,'height':1080});errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto(BASE+'#reading-2021-10-fr');page.wait_for_selector('.question')
 button=page.get_by_role('button',name='参考答案释义',exact=True);expect(button).to_be_disabled()
 page.get_by_label('第1题答案',exact=True).fill('Une réponse personnelle.')
 page.get_by_role('button',name='提交并核对答案',exact=True).click();expect(button).to_be_enabled();button.click()
 expect(page.locator('.answer-explanations article')).to_have_count(11)
 expect(page.locator('.answer-explanations')).to_contain_text('答案原因')
 page.locator('.answer-explanations a').first.click();expect(page.locator('.reader-content')).to_be_visible()
 page.reload();page.get_by_role('button',name='参考答案释义',exact=True).click();expect(page.locator('.answer-explanations')).to_be_visible()
 page.goto(BASE+'#long-2021-3-cn');page.wait_for_selector('.question');page.locator('.question').first.locator('.option').first.click()
 page.get_by_role('button',name='提交并核对答案',exact=True).click();page.get_by_role('button',name='查看参考答案释义',exact=True).click();expect(page.locator('.answer-explanations article')).to_have_count(11)
 for id,time in [('writing-2021-10-fr','150:00'),('reading-2021-10-fr','50:00'),('speaking-1-1','30:00')]:
  page.goto(BASE+'#'+id);expect(page.get_by_role('timer')).to_have_text(time)
 page.locator('.reader-tabs button').filter(has_text='范文').click();expect(page.locator('.model-editor h4')).to_have_count(6)
 page.get_by_role('tab',name='Débat · 考官追问',exact=True).click();expect(page.locator('.model-editor h4')).to_have_count(6)
 expect(page.locator('.model-editor')).to_contain_text('Concrètement')
 page.goto(BASE+'#writing-2021-10-fr');page.locator('.reader-tabs button').filter(has_text='范文').click()
 synthesis=page.locator('.model-editor').inner_text();assert 200<=len(synthesis.split())<=240
 page.get_by_role('tab',name='Essai · 议论文',exact=True).click();expect(page.locator('.model-editor')).to_contain_text('lettre ouverte')
 original=page.locator('.model-editor').inner_text();page.get_by_role('button',name='编辑范文',exact=True).click()
 editor=page.locator('.model-editor');editor.press('Control+End');editor.press('Enter');editor.press_sequentially('Mon ajout personnel.')
 def select_added():
  editor.evaluate('''el=>{const w=document.createTreeWalker(el,NodeFilter.SHOW_TEXT);let n;while(n=w.nextNode()){const i=n.textContent.indexOf('Mon ajout personnel.');if(i>=0){const r=document.createRange();r.setStart(n,i);r.setEnd(n,i+20);const s=getSelection();s.removeAllRanges();s.addRange(r);el.dispatchEvent(new MouseEvent('mouseup',{bubbles:true}));return;}}throw Error('added text missing');}''')
 select_added();page.get_by_role('button',name='加粗',exact=True).click()
 select_added();page.get_by_role('button',name='下划线',exact=True).click()
 select_added();page.get_by_role('button',name='黄色高亮',exact=True).click()
 assert editor.locator('b,strong').count()>0;assert editor.locator('u').count()>0;assert editor.locator('[style*=background]').count()>0
 select_added();page.get_by_role('button',name='删除高亮',exact=True).click()
 assert editor.locator('[style*=background]').count()==0;assert editor.locator('b,strong').count()>0;assert editor.locator('u').count()>0
 select_added();page.get_by_role('button',name='黄色高亮',exact=True).click()
 page.get_by_role('button',name='完成编辑',exact=True).click();page.reload();page.locator('.reader-tabs button').filter(has_text='范文').click();page.get_by_role('tab',name='Essai · 议论文',exact=True).click()
 expect(page.locator('.model-editor')).to_contain_text('Mon ajout personnel.');assert page.locator('.model-editor b,.model-editor strong').count()>0
 page.get_by_role('tab',name='Synthèse · 综合写作',exact=True).click();assert page.locator('.model-editor').inner_text()==synthesis
 page.get_by_role('tab',name='Essai · 议论文',exact=True).click();page.get_by_role('button',name='编辑范文',exact=True).click();editor=page.locator('.model-editor');editor.press('Control+A');editor.press('Backspace');page.get_by_role('button',name='完成编辑',exact=True).click()
 page.reload();page.locator('.reader-tabs button').filter(has_text='范文').click();page.get_by_role('tab',name='Essai · 议论文',exact=True).click();expect(page.locator('.model-editor')).to_be_empty()
 page.get_by_role('button',name='恢复原范文',exact=True).click();page.get_by_role('button',name='确认恢复',exact=True).click();assert page.locator('.model-editor').inner_text()==original
 # Imported HTML may contain only safe formatting; this is a local backup, not executable content.
 page.evaluate('''()=>{let x=JSON.parse(localStorage.getItem('noix-dalf-c1-v1'));x.modelEdits['writing-2021-10-fr:essai']='<p onclick="alert(1)">Texte sûr<img src=x onerror="alert(1)"><script>alert(1)</script><u>suite</u></p>';localStorage.setItem('noix-dalf-c1-v1',JSON.stringify(x));}''')
 page.reload();page.locator('.reader-tabs button').filter(has_text='范文').click();page.get_by_role('tab',name='Essai · 议论文',exact=True).click();expect(page.locator('.model-editor')).to_have_text('Texte sûrsuite');assert page.locator('.model-editor img,.model-editor script,.model-editor [onclick]').count()==0
 page.set_viewport_size({'width':390,'height':844});assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
 page.screenshot(path='/tmp/noix-reference-mobile.png')
 assert not errors,errors
 print('PASS: explanation gating/evidence/persistence, 3 timers, both speaking/writing model tabs, rich formatting/edit/delete/restore, isolated saves, imported HTML sanitization, mobile overflow.')
 browser.close()
