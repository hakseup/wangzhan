import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {wordCount,validImport,EMPTY_STATE} from '../src/lib.js';
const exercises=JSON.parse(readFileSync(new URL('../public/content.json',import.meta.url))).exercises;
const plain=html=>html.replace(/<[^>]+>/g,' ').replace(/&#39;/g,"'").replace(/&amp;/g,'&');
test('every comprehension answer has a specific reason and a quotation present in its source paragraph',()=>{
 let count=0;
 for(const e of exercises)for(const q of e.questions){
  assert.ok(q.explanation.reason.length>=15,e.id+q.id);
  assert.ok(q.explanation.evidence.length,e.id+q.id);
  for(const ev of q.explanation.evidence)assert.ok(e.paragraphs.find(p=>p.id===ev.pid)?.fr.includes(ev.quote),e.id+q.id+' source quote');
  count++;
 }
 assert.equal(count,547);
});
test('all production tasks have completed models in the requested formats and word limits',()=>{
 for(const e of exercises.filter(e=>['writing','speaking'].includes(e.category))){
  assert.deepEqual(e.models.map(m=>m.id),e.category==='writing'?['synthese','essai']:['monologue','debat']);
  for(const m of e.models){assert.ok(!/\[(?:THÈME|CONTEXTE|EXEMPLE|措施|主题)\]/i.test(m.html),e.id);assert.ok(wordCount(plain(m.html))>200,e.id);}
  if(e.category==='writing'){
   const n=wordCount(plain(e.models[0].html));assert.ok(n>=200&&n<=240,e.id+' synthesis length '+n);
   assert.ok(wordCount(plain(e.models[1].html))>=250,e.id+' essay length');
   assert.equal((e.models[0].html.match(/<p>/g)||[]).length,4);
  }else{
   assert.equal((e.models[0].html.match(/<h4>/g)||[]).length,6);
   assert.equal((e.models[1].html.match(/<h4>/g)||[]).length,6);
  }
 }
});
test('model changes round-trip with backups including an intentionally empty edited model',()=>{
 const state={...structuredClone(EMPTY_STATE),modelEdits:{'writing-1:essai':'<p><b>Mon texte</b></p>','speaking-1:debat':''}};
 assert.equal(validImport(JSON.parse(JSON.stringify(state))),true);
 assert.equal(validImport({...state,modelEdits:{a:{html:'bad shape'}}}),false);
 const old={...state};delete old.modelEdits;assert.equal(validImport(old),true);
});
