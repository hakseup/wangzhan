import json
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
ROOT=Path(__file__).resolve().parents[1]
bank=json.loads((ROOT/'public/content.json').read_text())
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
 page=browser.new_page(viewport={'width':1440,'height':900});page.clock.install();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto('http://127.0.0.1:4173');page.wait_for_selector('.shortcut-grid');page.evaluate('document.fonts.ready');page.clock.fast_forward(700)
 expect(page.locator('.shortcut-grid button')).to_have_count(6)
 expect(page.locator('.exercise-card')).to_have_count(0)
 assert page.evaluate('document.documentElement.scrollHeight<=innerHeight')
 assert page.locator('.paris-background').evaluate('(a)=>a.complete&&a.naturalWidth>0')
 expect(page.locator('.daily-note')).to_have_count(0)
 assert page.locator('.sidebar').inner_text().find('NOIX · FRANÇAIS')==-1
 assert '专属学习空间' not in page.locator('.sidebar').inner_text()
 assert '胡桃学习室' not in page.locator('.topbar').inner_text()
 page.screenshot(path='/workspace/work/journal-desktop.png');before=page.locator('.daily-phrase p[lang=fr]').inner_text();page.clock.fast_forward(120000);assert page.locator('.daily-phrase p[lang=fr]').inner_text()!=before
 page.locator('.shortcut').first.click();expect(page.locator('.exercise-card')).to_have_count(14)
 expect(page.locator('.paris-hero')).to_have_count(0)
 page.locator('.category-nav').nth(1).click();expect(page.locator('.exercise-card')).to_have_count(22)
 page.locator('.category-nav').nth(2).click();expect(page.locator('.exercise-card')).to_have_count(27)
 page.locator('.card-main').first.click();expect(page.locator('.reader-content')).to_be_visible();assert page.locator('.reader-content').evaluate('(e)=>getComputedStyle(e).fontFamily').startswith('Arial')
 page.screenshot(path='/workspace/work/journal-reading.png')
 page.get_by_role('button',name='返回题库',exact=True).click()
 page.get_by_role('button',name='单词与笔记',exact=True).click()
 expect(page.locator('.wordbook')).to_have_count(5)
 page.get_by_role('button',name='开始背词',exact=True).click();expect(page.locator('.flashcard')).to_be_visible();expect(page.locator('.vocab-options button')).to_have_count(4)
 word=page.locator('.flashcard h3').inner_text();page.locator('.vocab-options button').first.click();expect(page.locator('.vocab-feedback')).to_be_visible()
 data=page.evaluate('JSON.parse(localStorage.getItem("noix-dalf-c1-v1"))');assert len(data['vocabProgress'])==1
 page.get_by_role('button',name='下一个',exact=False).click();page.get_by_role('button',name='听力词',exact=False).first.click()
 page.get_by_label('背词模式').select_option('spelling');page.get_by_role('button',name='开始背词',exact=True).click()
 expect(page.get_by_label('法语拼写',exact=True)).to_be_visible();expect(page.locator('.flashcard h3')).to_have_count(0)
 page.get_by_label('法语拼写',exact=True).fill('incorrect');page.get_by_role('button',name='核对拼写',exact=False).click();expect(page.locator('.vocab-feedback')).to_be_visible()
 page.reload();page.wait_for_selector('.shortcut-grid');data=page.evaluate('JSON.parse(localStorage.getItem("noix-dalf-c1-v1"))');assert len(data['vocabProgress'])==2
 for width,height in [(390,844),(768,1024),(1440,600)]:
  page.set_viewport_size({'width':width,'height':height});assert page.evaluate('document.documentElement.scrollWidth<=innerWidth');assert page.evaluate('document.documentElement.scrollHeight<=innerHeight')
  for b in page.locator('.shortcut').all():
   box=b.bounding_box();assert box['y']>=0 and box['y']+box['height']<=height
  page.screenshot(path=f'/workspace/work/journal-{width}.png')
 assert not errors,errors
 print('Journal homepage, all five categories, wordbooks, both study modes, persistence and responsive layout passed.')
 browser.close()
