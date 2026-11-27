import json
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
bank=json.loads(Path('public/content.json').read_text())
with sync_playwright()as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox']);page=b.new_page(viewport={'width':1440,'height':900});page.goto('http://127.0.0.1:4173');page.wait_for_selector('.shortcut-grid')
 for caption in page.locator('.side-section-label>span').all():assert caption.evaluate('(e)=>e.getBoundingClientRect().height<=parseFloat(getComputedStyle(e).lineHeight)*1.1')
 for category in ['long','short','reading']:
  e=next(e for e in bank['exercises']if e['category']==category);page.goto('http://127.0.0.1:4173#'+e['id']);page.wait_for_selector('.question')
  submit=page.get_by_role('button',name='提交并进入复盘'if category!='reading'else'提交并核对答案',exact=True);expect(submit).to_be_enabled();submit.click();expect(page.locator('.review-question')).to_have_count(len(e['questions']));expect(page.locator('.question-status.unanswered')).to_have_count(len(e['questions']));page.reload();expect(page.locator('.evidence-reader')).to_be_visible()
 b.close();print('PASS: sidebar captions remain one line; blank long/short/reading submissions open and restore review, with unanswered statuses preserved.')
