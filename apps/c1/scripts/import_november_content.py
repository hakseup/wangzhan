"""Import reviewed November assets without changing existing exercise identities/content.

Run only after preparing data/imports/2026-11/new-exercises.json. PDF originals are
not published. Duplicate sources attach to their canonical existing exercises.
"""
import collections,hashlib,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/'data/imports/2026-11'
IMPORT_ID='2026-11-twenty-sets'
def read(name):return json.loads((ASSETS/name).read_text())
def dump(path,value):path.write_text(json.dumps(value,ensure_ascii=False,separators=(',',':')))
bank=json.loads((ROOT/'public/content.json').read_text())
new=read('new-exercises.json')
assert len(new)==76, 'All21 written and55 oral exercises must be reviewed before importing.'
assert len({e['id']for e in new})==len(new)
new_ids={e['id']for e in new}
baseline=[e for e in bank['exercises']if e['id']not in new_ids]
assert len(baseline)==176, 'Unexpected baseline: review the branch before importing.'
by_id={e['id']:e for e in baseline}
for row in read('written-duplicates.json'):
 for eid in row['existingExerciseIds']:
  e=by_id[eid];e['sourceFiles']=list(dict.fromkeys(e['sourceFiles']+row['sourceFiles']))
oral_audit=read('oral-source-audit.json')
for row in oral_audit['topics']:
 if row['status']=='existing_duplicate':
  e=by_id[row['closestExistingMatches'][0]['id']]
  e['sourceFiles']=list(dict.fromkeys(e['sourceFiles']+[row['sourceFile']]))
topics=read('oral-topics.json')
for eid,topic in topics.items():by_id[eid]['topic']=topic
upgrades=read('canonical-upgrades.json')
assert len(upgrades)==3
for e in upgrades:
 old=by_id[e['id']]
 assert e.get('audio')==old.get('audio'),e['id']
 e['sourceFiles']=list(dict.fromkeys(old['sourceFiles']+e['sourceFiles']))
 by_id[e['id']]=e
baseline=[by_id[e['id']]for e in baseline]
allowed_topics=set(topics.values())
for e in new+upgrades:
 assert e['topic']in allowed_topics,e['id']
 assert e['paragraphs']and e['sourceFiles']and e['titleZh'],e['id']
 assert e['category']in ['long','short','reading','speaking']
 e.pop('sourcePath',None)
 if e['category']in ['long','short']and e['id']in new_ids:
  assert not e.get('audio'), 'No new recording was attached.'
  e['audioMissing']=True
  e['materialNote']='本次附件未提供录音；本题以听力原文进行文字练习。'
 else:e.pop('audioMissing',None)
 e['importId']=IMPORT_ID
 e['translationKind']='source-reviewed'
 for p in e['paragraphs']:
  assert isinstance(p.get('zh'),str)and p['zh'].strip(),(e['id'],p['id'])
  assert not re.search(r'[\ufffd\x00-\x08\x0b\x0c\x0e-\x1f]',p['fr']+p['zh']),(e['id'],p['id'])
  p['translationReviewed']=True
 for q in e['questions']:
  assert q['zh']and q['explanation']['reason'],(e['id'],q['id'])
  for o in q.get('options',[]):assert o['zh'],(e['id'],q['id'],o['id'])
  for x in q['explanation']['evidence']:
   p=next(p for p in e['paragraphs']if p['id']==x['pid'])
   assert x['quote']in p['fr'],(e['id'],q['id'],x)
 bank_evidence=e['category']in ['long','short','reading']
 assert bool(e['questions'])==bank_evidence,e['id']
bank['exercises']=baseline+new
sources=set(n for e in bank['exercises']for n in e['sourceFiles'])
bank['sourceFileCount']=len(sources)
bank['pdfCount']=sum(n.lower().endswith('.pdf')for n in sources)
bank['pageCount']=486+605
record={
 'id':IMPORT_ID,'receivedPdfFiles':60,'processedPdfFiles':59,
 'missingPdfFiles':[{'file':'C1第八套口语真题（12篇）.pdf','reason':'附件超过当前读取工具32 MiB上限，等待压缩或拆分文件；未猜测补写。'}],
 'processedWrittenSets':list(range(1,21)),
 'processedOralSets':[n for n in range(1,21)if n!=8],
 'addedExerciseIds':[e['id']for e in new],
 'addedCounts':dict(collections.Counter(e['category']for e in new)),
 'addedQuestions':sum(len(e['questions'])for e in new),
 'baselineExercises':176,'baselineQuestions':547,
 'upgradedExerciseIds':[e['id']for e in upgrades],
 'upgradedQuestionDelta':9,
 'paragraphCount':sum(len(e['paragraphs'])for e in bank['exercises']),
 'totalExercises':len(bank['exercises']),
 'totalQuestions':sum(len(e['questions'])for e in bank['exercises']),
 'counts':dict(collections.Counter(e['category']for e in bank['exercises'])),
 'retainedExistingIds':list(by_id),
 'note':'按正文与题目去重；同主题、不同材料保留。保留原有练习ID；三组原文/题目不完整的旧练习补齐原题，题意与选项改变的题目使用独立编号。其余旧题正文与评分保持不变，补充来源并调整口语主题。第20套笔试按实际附件收录，未虚构不存在的写作材料。'
}
bank['imports']=[x for x in bank.get('imports',[])if x['id']!=IMPORT_ID]+[record]
dump(ROOT/'public/content.json',bank)
(ASSETS/'import-report.json').write_text(json.dumps(record,ensure_ascii=False,indent=2))
print('Imported',len(new),'reviewed new exercises;',record['totalQuestions'],'questions total;',record['counts'])
