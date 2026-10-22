import test from 'node:test';
import assert from 'node:assert/strict';
import {loadBankFixture} from './bank-fixture.js';
import {buildReviewParagraphs,activeSentenceLinks} from '../src/review-paragraphs.js';
import {sentenceRanges} from '../src/sentence-alignment.js';
const bank=loadBankFixture();
test('post-submit review preserves all paragraphs and full translations, with only evidence ranges highlighted',()=>{
 for(const exercise of bank.exercises.filter(e=>['long','short','reading'].includes(e.category))){
  const paragraphs=buildReviewParagraphs(exercise);assert.equal(paragraphs.length,exercise.paragraphs.length);
  for(const [index,p] of paragraphs.entries()){
   const original=exercise.paragraphs[index];assert.equal(p.id,original.id);assert.equal(p.units.flatMap(u=>u.runs).map(r=>r.text).join(''),original.fr);assert.equal(p.translation.map(t=>t.text).join(''),original.zh);
   for(const u of p.units)for(const r of u.runs){assert.equal(original.fr.slice(r.start,r.start+r.text.length),r.text);if(r.answer)assert.ok(exercise.questions.some(q=>q.explanation.evidence.some(v=>v.pid===p.id&&original.fr.indexOf(v.quote)<=r.start&&original.fr.indexOf(v.quote)+v.quote.length>=r.start+r.text.length)));}
  }
 }
});
test('a partial answer sentence stays inside the complete paragraph and keeps its original anchor',()=>{
 const exercise=bank.exercises.find(e=>e.id==='reading-2021-10-fr'),p=buildReviewParagraphs(exercise).find(p=>p.id==='p1');
 assert.ok(p.units.flatMap(u=>u.runs).some(r=>!r.answer&&r.text.includes('tabou')));
 const evidence=exercise.questions[0].explanation.evidence[0];assert.ok(p.units.some(u=>u.id===evidence.pairIds[0]));
 const translation=p.translation.find(t=>t.pairId===evidence.pairIds[0]);assert.match(translation.text,/研究表明/);
});

test('hover always targets one sentence in each language, including non-answer sentences and unequal sentence counts',()=>{
 for(const e of bank.exercises.filter(e=>['long','short','reading'].includes(e.category)))for(const p of buildReviewParagraphs(e,bank.lexicon)){
  assert.equal(p.units.length,sentenceRanges(p.fr,'fr').length);
  assert.equal(p.translation.length,sentenceRanges(p.zh,'zh').length);
  for(const u of p.units){const link=activeSentenceLinks(p,u.id);assert.equal(p.units.filter(s=>s.id===link.sourceId).length,1);assert.equal(p.translation.filter(t=>t.id===link.translationId).length,1);}
  for(const t of p.translation){const link=activeSentenceLinks(p,t.id);assert.equal(p.units.filter(s=>s.id===link.sourceId).length,1);assert.equal(p.translation.filter(s=>s.id===link.translationId).length,1);}
  assert.deepEqual(activeSentenceLinks(p,null),{});
 }
});
test('context sentences map to their own translation, rather than the entire paragraph or the next sentence',()=>{
 const e=bank.exercises.find(e=>e.id==='reading-2021-10-fr'),ps=buildReviewParagraphs(e,bank.lexicon),p1=ps.find(p=>p.id==='p1'),p2=ps.find(p=>p.id==='p2');
 for(const [fr,zh] of [['C’est un tabou.','这是一个禁忌话题。'],['Les enseignants qui se lient','与学生建立亲密联系']]){const s=p1.units.find(s=>s.text.startsWith(fr)),link=activeSentenceLinks(p1,s.id),t=p1.translation.find(t=>t.id===link.translationId);assert.ok(t.text.startsWith(zh));assert.notEqual(t.text,p1.zh);}
 const s=p2.units.find(s=>s.text.startsWith('D’emblée')),t=p2.translation.find(t=>t.id===activeSentenceLinks(p2,s.id).translationId);assert.equal(t.text,'人们很容易立刻想到不正当的恋情。');
});
