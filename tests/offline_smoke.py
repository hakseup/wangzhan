"""Verify the self-contained release with every external asset/API request blocked."""
import json,os
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
URL=os.environ.get('NOIX_OFFLINE_URL','http://127.0.0.1:4180/胡桃法语-DALF-C1-双击打开.html')
ROOT=Path(__file__).resolve().parents[1]
e=next(e for e in json.loads((ROOT/'public/content.json').read_text())['exercises']if e['id']=='long-2021-3-cn')
with sync_playwright()as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
 page=b.new_page(viewport={'width':1440,'height':1000});blocked=[];errors=[]
 def route(r):
  if r.request.is_navigation_request()and r.request.resource_type=='document':r.continue_()
  else:blocked.append(r.request.url);r.abort()
 page.route('**/*',route);page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto(URL);page.wait_for_selector('.exercise-card')
 assert page.locator('html').get_attribute('data-noix-offline')is not None
 assert page.evaluate('window.__NOIX_EMBEDDED_BANK__.exercises.length')==176
 for sel in ['.brand .walnut-logo','.paris-background']:
  assert page.locator(sel).evaluate('(a)=>a.complete && a.naturalWidth>0 && a.src.startsWith("data:image/")')
 page.locator('.card-main').first.click();expect(page.locator('.reader-content')).to_have_count(0)
 for q in e['questions']:
  question=page.locator('#question-'+q['id'])
  if q['type']=='choice':question.locator('input[type=radio]').first.check()
  elif q['type']=='tf':question.locator('input[type=radio]').first.check();question.locator('textarea').fill('Un passage à vérifier.')
  else:question.locator('textarea').fill('Une réponse à vérifier.')
 page.get_by_role('button',name='提交并进入复盘',exact=True).click();expect(page.locator('.reader-content')).to_be_visible()
 assert page.locator('.reader-content').evaluate('(a)=>getComputedStyle(a).fontFamily').startswith('Arial')
 page.wait_for_function('document.querySelector("audio").duration>0')
 assert page.locator('audio').evaluate('(a)=>a.src.startsWith("data:audio/")')
 page.get_by_role('button',name='播放音频',exact=True).click();page.wait_for_function('document.querySelector("audio").currentTime>0');page.get_by_role('button',name='暂停',exact=True).click()
 page.get_by_role('button',name='全屏刷题',exact=True).click();expect(page.get_by_role('button',name='退出全屏',exact=True)).to_be_visible();page.get_by_role('button',name='退出全屏',exact=True).click()
 page.evaluate("location.hash='writing-2024-6-cn'");expect(page.locator('.reader-content')).to_contain_text('Les devoirs du soir sont source d’inégalités')
 assert not blocked,blocked
 assert not errors,errors
 b.close()
 print('PASS: complete offline bank, embedded Paris/logo, audio playback, review gate, Arial and fullscreen; no external asset/API requests.')
