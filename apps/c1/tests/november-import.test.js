import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {createHash} from 'node:crypto';
const read=p=>JSON.parse(fs.readFileSync(new URL('../'+p,import.meta.url),'utf8'));
const bank=read('public/content.json'),report=read('data/imports/2026-11/import-report.json');
function stable(v){if(Array.isArray(v))return v.map(stable);if(v&&typeof v==='object')return Object.fromEntries(Object.keys(v).sort().map(k=>[k,stable(v[k])]));return v;}
test('the import preserves existing material and identifiers outside the three explicitly reviewed source-complete upgrades',()=>{
 const baseline=read('data/imports/2026-11/baseline-hashes.json');
 assert.equal(Object.keys(baseline).length,176);assert.equal(report.upgradedExerciseIds.length,3);
 for(const [id,digest]of Object.entries(baseline)){
  const e=bank.exercises.find(e=>e.id===id);assert.ok(e,id);
  if(report.upgradedExerciseIds.includes(id))continue;
  const value=Object.fromEntries(Object.entries(e).filter(([k])=>!['topic','sourceFiles'].includes(k)));
  const edit=read('data/audits/2026-11-24-oral-coverage.json').corrections.find(x=>x.id===id);
  if(edit){value.title=edit.before.title;value.titleZh=edit.before.titleZh;if(edit.before.searchAliases)value.searchAliases=edit.before.searchAliases;else delete value.searchAliases;}
  assert.equal(createHash('sha256').update(JSON.stringify(stable(value))).digest('hex'),digest,id);
 }
});
test('twenty written sets and nineteen readable oral PDFs have explicit coverage; the oversized file is not represented as processed',()=>{
 assert.equal(report.processedPdfFiles,59);assert.equal(report.receivedPdfFiles,60);
 assert.deepEqual(report.processedWrittenSets,Array.from({length:20},(_,i)=>i+1));
 assert.equal(report.processedOralSets.length,19);assert.ok(!report.processedOralSets.includes(8));
 assert.deepEqual(report.missingPdfFiles.map(x=>x.file),['C1第八套口语真题（12篇）.pdf']);
 assert.equal(report.addedExerciseIds.length,76);assert.deepEqual(report.addedCounts,{short:14,long:6,reading:1,speaking:55});
 assert.equal(report.totalQuestions,682);assert.equal(report.totalExercises,252);assert.equal(report.paragraphCount,4721);
});
test('oral theme corrections and new source material are complete without placeholder translations or broken glyphs',()=>{
 const topics=read('data/imports/2026-11/oral-topics.json');
 for(const [id,topic]of Object.entries(topics))assert.equal(bank.exercises.find(e=>e.id===id).topic,topic,id);
 const fresh=bank.exercises.filter(e=>report.addedExerciseIds.includes(e.id));
 const titles=new Set();
 for(const e of fresh){
  assert.ok(e.topic&&e.titleZh&&e.sourceFiles.length,e.id);
  assert.ok(!titles.has(e.id),e.id);titles.add(e.id);
  for(const p of e.paragraphs){assert.match(p.zh,/[\u4e00-\u9fff]/,p.id);assert.doesNotMatch(p.fr+p.zh,/[�⁇\u0000]/,p.id);assert.ok(p.sourcePage>0,p.id);}
 }
 assert.equal(bank.exercises.filter(e=>e.audio).length,36);
});

test('completed source upgrades retain French personal names, place names and book titles',()=>{
 const text=bank.exercises.filter(e=>report.upgradedExerciseIds.includes(e.id)).flatMap(e=>e.paragraphs.map(p=>p.zh)).join(' ');
 for(const name of ['Eric Delvaux','Valère Corréard','Marie-Lise Bertrand','Catherine Boullay','Eric Scherer','Joël de Rosnay','Etienne Klein','Cyril Dion','Paris','Porte de Vanves','La symphonie du vivant','A-t-on encore besoin des journalistes'])assert.ok(text.includes(name),name);
 assert.doesNotMatch(text,/埃里克·|瓦莱尔·|玛丽-莉丝·|若埃尔·|艾蒂安·|西里尔·|旺沃门|《生命的交响曲》/);
});
