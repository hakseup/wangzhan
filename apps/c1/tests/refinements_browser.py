"""Exercise the real annotation/dictionary/editor interactions and unchanged layout."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
BASE='http://127.0.0.1:4173'
def select_text(page,selector,word):
 page.locator(selector).first.scroll_into_view_if_needed()
 page.evaluate('''({selector,word})=>{const el=document.querySelector(selector);const walk=document.createTreeWalker(el,NodeFilter.SHOW_TEXT);let node;while(node=walk.nextNode()){const i=node.textContent.indexOf(word);if(i>=0){const r=document.createRange();r.setStart(node,i);r.setEnd(node,i+word.length);const s=getSelection();s.removeAllRanges();s.addRange(r);el.dispatchEvent(new MouseEvent('mouseup',{bubbles:true}));return;}}throw Error('selection not found: '+word);}''',{'selector':selector,'word':word})
with sync_playwright()as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox']);page=b.new_page(viewport={'width':1440,'height':768});errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto(BASE);page.wait_for_selector('.shortcut-grid');page.evaluate('document.fonts.ready')
 expect(page.locator('.sidebar-bottom')).to_have_count(0)
 assert page.locator('.sidebar').evaluate('(e)=>e.scrollHeight<=e.clientHeight')
 page.screenshot(path='/workspace/work/refined-home.png')
 page.locator('.shortcut').first.click();page.locator('.card-main').first.click();expect(page.get_by_role('timer')).to_have_text('07:00')
 q=page.locator('.question').first;qid=q.get_attribute('id');option=q.locator('h3').first;pid=option.get_attribute('data-annotation')
 select_text(page,f'[data-annotation="{pid}"]','fabricants')
 page.get_by_role('button',name='查询中文释义与搭配').click();expect(page.locator('.dictionary-panel h3')).to_have_text('fabricant');expect(page.locator('.dictionary-meaning')).to_contain_text('制造商');expect(page.locator('.dictionary-phrases')).to_contain_text('fabricant de voitures')
 page.get_by_role('button',name='将释义与搭配记入备注').click();page.get_by_role('button',name='保存备注',exact=False).click();expect(option.locator('mark.word-note')).to_have_count(1)
 expect(q.locator('input:checked')).to_have_count(0)
 prompt=q.locator('.option span[lang=fr]').nth(1);word='technologies';select_text(page,'#'+qid+' .option:nth-child(2) span[lang=fr]',word);page.get_by_role('button',name='高亮',exact=True).click();expect(prompt.locator('mark.level-1')).to_have_count(1)
 # A different open question supports selection inside its editable textarea.
 area=page.locator('.question textarea.answer-input').first;area.scroll_into_view_if_needed();area.fill('Les fabricants travaillent ensemble.');area.evaluate('(e)=>{e.focus();e.setSelectionRange(4,14);e.dispatchEvent(new MouseEvent("mouseup",{bubbles:true}));}')
 page.get_by_role('button',name='高亮',exact=True).click();expect(area.locator('..').locator('mark.level-1')).to_have_text('fabricants')
 area.fill('Aujourd’hui, les fabricants travaillent ensemble.');expect(area.locator('..').locator('mark.level-1')).to_have_text('fabricants')
 assert area.evaluate('(e)=>getComputedStyle(e).caretColor')!='rgba(0, 0, 0, 0)'
 page.reload();expect(page.get_by_role('timer')).to_have_text('07:00');expect(page.locator(f'[data-annotation="{pid}"] mark.word-note')).to_have_count(1)
 area=page.locator('.question textarea.answer-input').first;expect(area.locator('..').locator('mark.level-1')).to_have_text('fabricants')
 page.evaluate("location.hash='short-2024-6-cn-1'");expect(page.get_by_role('timer')).to_have_text('03:00')
 page.evaluate("location.hash='writing-2024-6-cn'");expect(page.get_by_role('timer')).to_have_text('150:00');page.wait_for_selector('.paragraph-heading')
 assert page.locator('.paragraph-heading').first.evaluate('(e)=>getComputedStyle(e).backgroundColor')in['rgba(0, 0, 0, 0)','rgb(255, 255, 255)']
 assert page.locator('.paragraph-heading').first.evaluate('(e)=>parseInt(getComputedStyle(e).fontWeight)')>=700
 page.get_by_role('button',name='返回题库',exact=True).click();page.get_by_role('button',name='单词与笔记',exact=False).first.click();expect(page.locator('.wordbook')).to_have_count(5)
 counts=[int(page.locator('.wordbook').nth(i).locator('span').inner_text().split()[0])for i in range(4)];assert len(set(counts))==4 and min(counts)>300
 page.get_by_label('搜索本词书',exact=True).fill('fabricants');expect(page.locator('.word-row')).to_contain_text('fabricant')
 for h in [600,768,900]:
  page.goto(BASE);page.wait_for_selector('.shortcut-grid');page.set_viewport_size({'width':1440,'height':h});page.wait_for_function('document.querySelector(".sidebar").scrollHeight<=document.querySelector(".sidebar").clientHeight')
 assert not errors,errors
 print('PASS: timer defaults, sidebar fit, plain headings, question/option/editor annotations, rebasing, reload, in-page definitions/collocations, and four independent corpus-based books.')
 b.close()
