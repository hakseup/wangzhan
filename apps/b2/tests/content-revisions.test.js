import test from 'node:test';import assert from 'node:assert/strict';
import {compileContentRevisions,cleanChinese} from '../scripts/compile-content-revisions.mjs';
import {loadBankFixture} from './bank-fixture.js';import {buildReviewParagraphs} from '../src/review-paragraphs.js';
test('the complete corpus has reviewed translations and source-verified repair records without changing question identities or answers',()=>{
 const {bank,audit,parts}=compileContentRevisions(),before=loadBankFixture();
 assert.equal(audit.oldMachineParagraphs,210);assert.equal(audit.otherArticlesReviewed,245);assert.equal(audit.questionTranslations,673);assert.equal(audit.paragraphs,511);
 assert.equal(audit.dictionaryEntriesRepaired,53);assert.doesNotMatch(JSON.stringify(bank.lexicon.entries.pair),/[⁇�]/);
 for(const part of parts)assert.ok(Buffer.byteLength(JSON.stringify(part))<4_400_000,'Private revision parts must fit the function response limit');
 for(const [i,e]of bank.exercises.entries()){
  assert.equal(e.id,before.exercises[i].id);assert.deepEqual(e.questions.map(q=>[q.id,q.answer?.value,q.answer?.variants]),before.exercises[i].questions.map(q=>[q.id,q.answer?.value,q.answer?.variants]));
  for(const p of e.paragraphs){assert.equal(p.translationReviewed,true);assert.ok(p.zh);assert.doesNotMatch(p.zh,/[⁇�]|&(?:quot|amp|nbsp);/);}
  for(const q of e.questions){assert.ok(q.zh);for(const o of q.options)assert.ok(o.zh);for(const v of q.explanation?.evidence||[])assert.ok(e.paragraphs.find(p=>p.id===v.pid)?.fr.includes(v.quote));}
  for(const p of buildReviewParagraphs(e,bank.lexicon))assert.equal(p.units.flatMap(u=>u.runs.map(r=>r.text)).join(''),p.fr);
 }
 const generation=bank.exercises.find(e=>e.id==='b2-reading-2f07f29b04');assert.ok(generation.paragraphs[0].zh.includes('工作'));assert.doesNotMatch(generation.paragraphs.map(p=>p.zh).join(''),/难民身份|how to manage|Company Committees/);
 assert.ok(bank.exercises.find(e=>e.id==='b2-reading-f0dcfe81f1').paragraphs[0].sourceRepair);
 assert.equal(cleanChinese('&amp;quot;成⻓ 与 ⻉壳“例句”'),'"成长与贝壳“例句”');
});
