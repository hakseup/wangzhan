"""Exercise real submit gates, compact fullscreen, aligned review and source annotations."""
import json,os
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
ROOT=Path(__file__).resolve().parents[1]
BANK=json.loads((ROOT/'public/content.json').read_text());BASE=os.environ.get('NOIX_TEST_URL','http://127.0.0.1:4173')
def select(page,selector,text):
 page.locator(selector).first.scroll_into_view_if_needed()
 page.evaluate('''({selector,text})=>{const el=document.querySelector(selector),w=document.createTreeWalker(el,NodeFilter.SHOW_TEXT);let n;while(n=w.nextNode()){const start=n.textContent.indexOf(text);if(start>=0){const r=document.createRange();r.setStart(n,start);r.setEnd(n,start+text.length);getSelection().removeAllRanges();getSelection().addRange(r);el.dispatchEvent(new MouseEvent('mouseup',{bubbles:true}));return;}}throw Error('Missing word '+text);}''',{'selector':selector,'text':text})
def fill(page,e):
 for q in e['questions']:
  el=page.locator('#question-'+q['id']);answer=q.get('answer',{})
  if q['type']=='choice':el.locator('input[type=radio]').nth(next((i for i,o in enumerate(q['options'])if o['id']==answer.get('value')),0)).check()
  elif q['type']=='tf':el.locator('input[type=radio]').nth(0 if answer.get('value')=='Vrai'else 1).check();el.locator('textarea').fill('Un passage du texte.')
  else:el.locator('textarea').fill(answer.get('reference')or'Une réponse à vérifier.')
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox']);page=b.new_page(viewport={'width':1440,'height':900});errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 e=next(e for e in BANK['exercises']if e['id']=='reading-2021-10-fr')
 page.goto(BASE+'#'+e['id']);page.wait_for_selector('.question')
 expect(page.get_by_role('button',name='中文参考译文',exact=False)).to_have_count(0)
 expect(page.locator('.evidence-reader,.answer-explanations,.translation-content')).to_have_count(0)
 expect(page.locator('.panel-heading')).to_have_count(0)
 timer=page.locator('.practice-timer').bounding_box();full=page.locator('.fullscreen-btn').bounding_box();assert timer['x']+timer['width']<=full['x']+1
 page.get_by_role('button',name='全屏刷题',exact=True).click();page.wait_for_function('!!document.fullscreenElement||!!document.querySelector(".is-focused")')
 page.wait_for_timeout(100)
 for selector in ['.material-scroll','.answer-scroll']:
  box=page.locator(selector).bounding_box();assert box['height']>page.viewport_size['height']*.73,(selector,box)
 assert page.locator('.detail-heading').bounding_box()['height']<100
 page.screenshot(path='/workspace/work/reading-fullscreen.png')
 page.get_by_role('button',name='退出全屏',exact=True).click()
 # A source mark made before submission must survive inside its excerpt afterward.
 select(page,'.reader-content [data-paragraph="p1"]','affectif');page.get_by_role('button',name='高亮',exact=True).click()
 fill(page,e);page.get_by_role('button',name='提交并核对答案',exact=True).click();page.wait_for_url('**/review')
 expect(page.locator('.review-question')).to_have_count(len(e['questions']))
 expect(page.locator('.review-paragraph')).to_have_count(len(e['paragraphs']))
 for paragraph in e['paragraphs']:
  block=page.locator('.review-paragraph[data-paragraph="'+paragraph['id']+'"]')
  assert block.locator('.evidence-fr [data-annotation]').evaluate_all('(nodes)=>nodes.map(n=>n.dataset.annotationText).join("")')==paragraph['fr']
  assert block.locator('.evidence-zh').inner_text()==paragraph['zh']
 for q in e['questions']:
  if q['type']!='choice':continue
  options=page.locator('#question-'+q['id']+' .review-option')
  expect(options).to_have_count(len(q['options']))
  for i,o in enumerate(q['options']):
   expect(options.nth(i)).to_contain_text(o['text']);expect(options.nth(i)).to_contain_text(o['zh'])
 expect(page.locator('.evidence-reader mark.level-1')).to_have_text('affectif')
 expect(page.locator('.review-question input,.review-question textarea')).to_have_count(0)
 targetPair=next(p for p in e['reviewPassages']if 'premier levier' in p['fr'])
 source=page.locator('[data-evidence-id="'+targetPair['id']+'"]')
 source.hover();expect(source).to_have_class('review-source-unit is-linked')
 assert source.evaluate('(e)=>getComputedStyle(e).textDecorationLine')=='underline'
 chinese=source.locator('xpath=ancestor::article').locator('.review-translation-unit.is-linked')
 expect(chinese).to_have_count(1)
 assert chinese.evaluate('(e)=>getComputedStyle(e).textDecorationColor')=='rgb(95, 157, 113)'
 chinese.focus();expect(source).to_have_class('review-source-unit is-linked')
 assert source.locator('.answer-source').first.evaluate('(e)=>getComputedStyle(e).backgroundColor')=='rgb(255, 240, 187)'
 assert source.locator('.answer-source').first.inner_text().strip() in targetPair['fr']
 # Reproduce the reported bug on each sentence of a mixed answer/context paragraph.
 paragraph=page.locator('.review-paragraph[data-paragraph="p1"]')
 expected=['这是一个禁忌话题。','与学生建立亲密联系','然而，研究表明','在新近出版的']
 sentences=paragraph.locator('.review-source-unit');expect(sentences).to_have_count(4)
 for i,prefix in enumerate(expected):
  sentences.nth(i).hover()
  expect(paragraph.locator('.review-source-unit.is-linked')).to_have_count(1)
  translated=paragraph.locator('.review-translation-unit.is-linked');expect(translated).to_have_count(1)
  assert translated.inner_text().startswith(prefix)
  assert paragraph.locator('.evidence-zh').evaluate('(e)=>getComputedStyle(e).textDecorationLine')=='none'
  assert paragraph.locator('.evidence-fr').evaluate('(e)=>getComputedStyle(e).textDecorationLine')=='none'
  # Enter from Chinese as well, verifying only its counterpart is underlined.
  translated.hover();expect(sentences.nth(i)).to_have_class('review-source-unit is-linked')
  expect(paragraph.locator('.review-source-unit.is-linked')).to_have_count(1)
  expect(paragraph.locator('.review-translation-unit.is-linked')).to_have_count(1)
  translated.focus();expect(sentences.nth(i)).to_have_class('review-source-unit is-linked')
 page.locator('.detail-heading h1').hover()
 # Locate from the final question, which is well below the first answer sentence.
 finalq=e['questions'][-1];target=finalq['explanation']['evidence'][0]['pairIds'][0]
 page.locator('#question-'+finalq['id']).get_by_role('button',name='定位',exact=True).first.click()
 page.wait_for_function('(id)=>document.querySelector(`[data-evidence-id="${id}"]`).classList.contains("is-linked")',arg=target)
 page.wait_for_function('''id=>{const e=document.querySelector(`[data-evidence-id="${id}"]`).getBoundingClientRect(),p=document.querySelector('.material-scroll').getBoundingClientRect();return e.top<p.bottom&&e.bottom>p.top;}''',arg=target)
 page.screenshot(path='/workspace/work/reading-review.png')
 # Excerpt selection uses source offsets rather than positions local to the excerpt.
 select(page,'.evidence-reader .evidence-fr [data-annotation-text*="levier"]','levier');page.get_by_role('button',name='高亮',exact=True).click()
 data=page.evaluate('JSON.parse(localStorage.getItem("noix-dalf-c1-v1"))');mark=next(m for m in data['annotations'][e['id']]if m['text']=='levier');source=next(p for p in e['paragraphs']if p['id']==mark['pid']);assert source['fr'][mark['start']:mark['end']]=='levier'
 page.reload();expect(page.locator('.evidence-reader')).to_be_visible();expect(page.locator('.evidence-reader mark')).to_have_count(2)
 page.get_by_role('button',name='返回修改答案',exact=True).click();expect(page.locator('.evidence-reader,.translation-content')).to_have_count(0);expect(page.get_by_role('button',name='中文参考译文',exact=False)).to_have_count(0)
 expect(page.locator('.reader-content mark')).to_have_count(2)
 page.locator('.question input[type=radio]:not(:checked)').first.check();page.evaluate("location.hash=location.hash+'/review'");expect(page.locator('.evidence-reader')).to_have_count(0)
 # Short and long listening remain transcript-gated; the same paired review opens after submission.
 for category in ['long','short']:
  e=next(e for e in BANK['exercises']if e['category']==category)
  page.goto(BASE+'#'+e['id']);page.wait_for_selector('.listening-cover');expect(page.locator('.evidence-reader,.translation-content')).to_have_count(0)
  fill(page,e);page.get_by_role('button',name='提交并进入复盘',exact=True).click();expect(page.locator('.evidence-reader')).to_be_visible();expect(page.locator('.review-question')).to_have_count(len(e['questions']))
  expect(page.locator('.review-paragraph')).to_have_count(len(e['paragraphs']))
  for q in e['questions']:
   if q['type']=='choice':expect(page.locator('#question-'+q['id']+' .review-option')).to_have_count(len(q['options']))
  page.reload();expect(page.locator('.evidence-reader')).to_be_visible()
  page.get_by_role('button',name='返回修改答案',exact=True).click();expect(page.locator('.listening-cover')).to_be_visible()
 # Mobile must retain scrollable panes without horizontal document overflow.
 page.set_viewport_size({'width':390,'height':844});page.wait_for_timeout(100);assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
 assert not errors,errors
 b.close();print('PASS: compact fullscreen >73% pane height, relocated timer, submit gates for reading/long/short, complete paragraph pairs/inline evidence/all translated options/green focus, locate, source-offset highlights, reload, stale-review invalidation and mobile.')
