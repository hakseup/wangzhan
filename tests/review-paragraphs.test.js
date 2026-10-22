import test from 'node:test';
import assert from 'node:assert/strict';
import {loadBankFixture} from './bank-fixture.js';
import {buildReviewParagraphs} from '../src/review-paragraphs.js';
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
