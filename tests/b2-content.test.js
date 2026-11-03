import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {wordCount,STORAGE_KEY,gradeQuestion} from '../src/lib.js';
import {buildReviewParagraphs} from '../src/review-paragraphs.js';
import {makeBooks} from '../src/vocabulary.js';
import {lookupWord} from '../src/dictionary.js';
const bank=JSON.parse(fs.readFileSync(new URL('../public/content.json',import.meta.url)));
test('B2 corpus has independent identity, valid answer options, all sources and five requested categories',()=>{
 assert.equal(bank.level,'DELF B2');assert.equal(bank.exercises.length,297);
 assert.match(STORAGE_KEY,/b2/);assert.ok(!STORAGE_KEY.includes('dalf'));
 assert.equal(new Set(bank.exercises.map(e=>e.id)).size,297);
 assert.deepEqual(Object.fromEntries(['long','short','reading1','reading2','writing','speaking'].map(c=>[c,bank.exercises.filter(e=>e.category===c).length])),{long:17,short:17,reading1:17,reading2:17,writing:17,speaking:212});
 for(const e of bank.exercises){
  assert.ok(e.title&&e.titleZh&&e.source&&e.paragraphs.length,e.id);
  if(e.audio)assert.ok(fs.existsSync(new URL('../public'+e.audio,import.meta.url)));assert.ok(!/DALF C1/.test(JSON.stringify(e)),e.id);
  for(const q of e.questions){
   assert.ok(q.prompt.length>6,e.id+q.id);
   if(q.type==='choice'){assert.deepEqual(q.options.map(o=>o.id),['A','B','C'],e.id+q.id);if(q.answer?.value)assert.ok(q.options.some(o=>o.id===q.answer.value),e.id+q.id);}
  }
 }
});
test('writing uses the B2 250-word task and complete models; oral has all seven themes and two model sections',()=>{
 const oral=bank.exercises.filter(e=>e.category==='speaking');
 assert.equal(new Set(oral.map(e=>e.topic)).size,7);
 for(const e of bank.exercises){
  if(e.category==='writing'){assert.equal(e.tasks[0].minWords,250);assert.equal(e.tasks[0].id,'essai');assert.ok(wordCount(e.studyModels[0].paragraphs.join(' '))>=250,e.id);}
  if(e.category==='speaking'){assert.equal(e.studyModels.length,2);assert.ok(e.studyModels[0].paragraphs.every(p=>!p.includes('XXX')),e.id);}
 }
});
test('frequency dates preserve repeat sittings and distinguish unmarked overseas material',()=>{
 const social=bank.exercises.find(e=>e.titleZh==='社交网络依赖与影响');assert.equal(social.source,'中国场次 2022年3月；中国场次 2026年6月');
 assert.equal(bank.exercises.find(e=>e.titleZh==='招聘测试的类型与应对').source,'国外考过，国内暂未考过');
 const oral=bank.exercises.filter(e=>e.category==='speaking');assert.equal(oral.filter(e=>e.source==='2026年6月场').length,12);assert.equal(oral.filter(e=>e.source==='国外考过，国内暂未考过').length,200);const audit=JSON.parse(fs.readFileSync(new URL('../data/2026-06-speaking-session-audit.json',import.meta.url)));assert.deepEqual(oral.filter(e=>e.examSessionLabel).map(e=>e.id).sort(),audit.matched.map(e=>e.id).sort());assert.equal(audit.unmatched.length,3);
});
test('review keeps complete source characters and dictionary books point to B2 exercises',()=>{
 for(const e of bank.exercises.filter(e=>e.questions.length)){
  const paragraphs=buildReviewParagraphs(e,bank.lexicon);
  for(const p of paragraphs){assert.equal(p.units.map(u=>u.runs.map(r=>r.text).join('')).join(''),p.fr,e.id);assert.ok(p.zh);}
 }
 const books=makeBooks(bank.exercises,{annotations:{}},bank.lexicon);
 for(const id of ['listening','reading','writing','speaking']){assert.ok(books[id].length>100);assert.ok(books[id].every(w=>w.sources.every(s=>s.id.startsWith('b2-'))));}
 assert.ok(lookupWord(bank.lexicon,'travail'));
});
test('missing source answers remain self-evaluation rather than incorrect automatic marks',()=>{
 const e=bank.exercises.find(e=>e.titleZh==='家庭作业争议');assert.ok(e.questions.every(q=>!q.answer));
 assert.equal(gradeQuestion(e.questions[0],'A').status,'review');
});
