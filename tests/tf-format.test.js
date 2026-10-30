import test from 'node:test';import assert from 'node:assert/strict';import fs from 'node:fs';import {gradeQuestion} from '../src/lib.js';
const bank=JSON.parse(fs.readFileSync(new URL('../public/content.json',import.meta.url)));
test('all reading judgement statements have independent Vrai/Faux values and clean prompts',()=>{
 const reading=bank.exercises.filter(e=>e.category.startsWith('reading'));
 const groups=new Map();let count=0;
 for(const e of reading)for(const q of e.questions){
  if(q.type==='tf'){count++;assert.ok(['Vrai','Faux'].includes(q.answer?.value),e.id+' '+q.number);assert.ok(!/Cochez|[Jj]?ustification|VRAI|FAUX|[\x00-\x1f\ufffd]|PRES?\b/.test(q.prompt),q.prompt);assert.equal(gradeQuestion(q,q.answer.value,'Une citation.').status,'review');assert.equal(gradeQuestion(q,q.answer.value==='Vrai'?'Faux':'Vrai','').status,'incorrect');}
  assert.ok(!/^Vrai ou faux/i.test(q.prompt),'unconverted judgement '+q.id);
  if(q.parentQuestionId){assert.equal(q.type,'tf');groups.set(q.parentQuestionId,(groups.get(q.parentQuestionId)||0)+1);}
 }
 assert.ok(count>80);assert.equal(groups.size,9);assert.ok([...groups.values()].every(n=>n===2||n===3));
});
test('office example retains original numbering and separate graded subquestions',()=>{
 const e=bank.exercises.find(e=>e.titleZh==='办公室的终结');const a=e.questions.find(q=>q.number==='7a'),b=e.questions.find(q=>q.number==='7b');assert.equal(a.answer.value,'Vrai');assert.equal(b.answer.value,'Faux');assert.notEqual(a.id,b.id);assert.equal(e.questions.find(q=>q.number===6).prompt,"Quelles sont les deux modalités d'horaires de travail possibles pour le télétravailleur selon les entreprises ?");
});
test('French question and option text contains no scan control characters or Chinese OCR debris',()=>{
 for(const e of bank.exercises)for(const q of e.questions)for(const text of [q.prompt,...q.options.map(o=>o.text)])assert.ok(!/[\x00-\x1f\ufffd\u4e00-\u9fff]/.test(text),e.id+' '+q.number+' '+text);
});
