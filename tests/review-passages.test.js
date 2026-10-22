import test from 'node:test';
import assert from 'node:assert/strict';
import {loadBankFixture} from './bank-fixture.js';
const bank=loadBankFixture();
test('review pairs are exact source sentences with locally reviewed translations and bidirectional question references',()=>{
 let questions=0;
 for(const e of bank.exercises.filter(e=>['long','short','reading'].includes(e.category))){
  const pairs=new Map(e.reviewPassages.map(p=>[p.id,p]));assert.equal(pairs.size,e.reviewPassages.length);
  for(const pair of pairs.values()){
   const p=e.paragraphs.find(p=>p.id===pair.pid);assert.equal(p.fr.slice(pair.start,pair.start+pair.fr.length),pair.fr);
   assert.match(pair.zh,/[\u4e00-\u9fff]/);assert.ok(pair.questionIds.length);assert.equal(pair.paragraphNumber,e.paragraphs.indexOf(p)+1);
   for(const qid of pair.questionIds)assert.ok(e.questions.find(q=>q.id===qid).explanation.evidence.some(x=>x.pairIds.includes(pair.id)));
  }
  for(const q of e.questions){questions++;for(const x of q.explanation.evidence){assert.ok(x.pairIds.length);const source=e.paragraphs.find(p=>p.id===x.pid),start=source.fr.indexOf(x.quote),end=start+x.quote.length;for(const id of x.pairIds){const p=pairs.get(id);assert.ok(p.questionIds.includes(q.id));assert.equal(p.pid,x.pid);assert.ok(p.start<end&&p.start+p.fr.length>start);}}}
 }assert.equal(questions,547);
});
test('known sentence-alignment and source-selection errors do not return',()=>{
 const e=bank.exercises.find(e=>e.id==='long-2021-3-cn'),pair=e.reviewPassages.find(p=>p.fr.startsWith('Mais surtout, heu'));
 assert.match(pair.zh,/分享知识/);assert.doesNotMatch(pair.zh,/原型/);
 const q=bank.exercises.find(e=>e.id==='reading-2024-5-fr').questions[2];assert.ok(q.explanation.evidence.every(x=>x.pid==='p6'));assert.match(q.explanation.reason,/辅助智能/);
});
