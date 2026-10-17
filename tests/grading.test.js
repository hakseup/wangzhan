import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync,existsSync} from 'node:fs';
import {gradeQuestion,gradeExercise,annotationParts,wordCount,validImport,EMPTY_STATE} from '../src/lib.js';

const bank=JSON.parse(readFileSync(new URL('../public/content.json',import.meta.url)));
test('every imported document has an exercise; every objective question has a valid answer',()=>{
 assert.equal(bank.exercises.length,176);
 assert.equal(new Set(bank.exercises.flatMap(e=>e.sourceFiles)).size,117);
 assert.deepEqual(Object.fromEntries(['long','short','reading','writing','speaking'].map(c=>[c,bank.exercises.filter(e=>e.category===c).length])),{long:14,short:22,reading:27,writing:28,speaking:85});
 const ids=new Set();
 for(const e of bank.exercises){
  assert.ok(!ids.has(e.id),e.id);ids.add(e.id);
  assert.ok(e.title&&e.titleZh&&e.paragraphs.length,e.id);
  assert.ok(e.paragraphs.every(p=>typeof p.zh==='string'&&p.zh.trim().length>0),e.id+' translation');
  assert.ok(!/\d{4}年|场次/.test(e.title+e.titleZh),e.id);
  assert.ok(!/法语课代表|大脸法语/.test(JSON.stringify(e)),e.id);
  assert.ok(e.questions.length||['writing','speaking'].includes(e.category),e.id);
  if(e.category==='long'||e.category==='short')assert.ok(existsSync(new URL('../public'+e.audio,import.meta.url)),e.id);
  for(const q of e.questions){
   assert.ok(q.prompt.length>6,e.id+q.id);
   if(q.type==='choice'){
    assert.deepEqual(q.options.map(o=>o.id).sort(),['A','B','C'],e.id+q.id);
    assert.ok(q.options.some(o=>o.id===q.answer?.value),e.id+q.id);
   }
  }
 }
});
test('unanswered questions remain distinct from wrong answers and unknown references',()=>{
 const q={type:'choice',answer:{value:'B',reference:'B'}};
 assert.equal(gradeQuestion(q,'').status,'unanswered');
 assert.equal(gradeQuestion(q,'A').status,'incorrect');
 assert.equal(gradeQuestion(q,'B').status,'correct');
 assert.equal(gradeQuestion({type:'text'},'Une réponse').status,'review');
 const result=gradeExercise({questions:[{...q,id:'q1'},{...q,id:'q2'}]},{q1:{value:'B'}});
 assert.equal(result.q1.status,'correct');assert.equal(result.q2.status,'unanswered');
});
test('free answers accept reviewed variants without failing semantically different wording',()=>{
 const q={type:'text',answer:{reference:'Trois millions d’euros.',accepted:['3 millions d’euros','trois millions d’euros']}};
 assert.equal(gradeQuestion(q,'3 millions d’euros').status,'correct');
 assert.equal(gradeQuestion(q,'TROIS MILLIONS D’EUROS !').status,'correct');
 assert.equal(gradeQuestion(q,'5 millions').status,'review');
});
test('true/false justification is not silently awarded a semantic mark',()=>{
 const q={type:'tf',answer:{value:'Vrai',reference:'Un passage du texte.'}};
 assert.equal(gradeQuestion(q,'Faux').status,'incorrect');
 assert.equal(gradeQuestion(q,'Vrai').status,'review');
 assert.equal(gradeQuestion(q,'Vrai','Une citation différente.').choiceCorrect,true);
});
test('overlapping highlights preserve every character and apply the strongest color',()=>{
 const text='une pensée collaborative';
 const parts=annotationParts(text,[{start:4,end:10,level:1},{start:8,end:16,level:3,note:'mon commentaire'},{start:-2,end:200,level:2}]);
 assert.equal(parts.map(p=>p.text).join(''),text);
 assert.ok(parts.some(p=>p.level===3&&p.notes.length===1));
 assert.ok(parts.every(p=>p.level!==2));
});
test('backups reject malformed answers instead of crashing the next session',()=>{
 assert.equal(validImport(structuredClone(EMPTY_STATE)),true);
 assert.equal(validImport({...structuredClone(EMPTY_STATE),answers:{one:{q1:{value:42}}}}),false);
 assert.equal(validImport({...structuredClone(EMPTY_STATE),drafts:{one:{essai:[]}}}),false);
 assert.equal(validImport({...structuredClone(EMPTY_STATE),annotations:{one:[{id:'1',pid:'p0',text:'mot',start:4,end:1,level:1}]}}),false);
});
test('French contractions and hyphenated words count as one word',()=>{
 assert.equal(wordCount('L’éducation fait-elle grandir nos idées ?'),5);
 assert.equal(wordCount(''),0);
});

test('revised writing/oral material preserves readable text and stable, unique paragraph anchors',()=>{
 const revised=bank.exercises.filter(e=>['writing','speaking'].includes(e.category));
 assert.equal(revised.length,113);
 for(const e of revised){
  assert.equal(e.materialRevision,'pdf-rechecked-2026-10-17',e.id);
  assert.equal(new Set(e.paragraphs.map(p=>p.id)).size,e.paragraphs.length,e.id+' unique paragraph anchors');
  for(const p of e.paragraphs){
   assert.ok(!/[\u0300-\u05ff\u3400-\u9fff\ufffd]/u.test(p.fr),e.id+' broken glyphs');
   assert.ok(['heading','body','document','label','note','source'].includes(p.role),e.id+' paragraph role');
   assert.ok(p.sourcePage>0,e.id+' page provenance');
  }
 }
 const oral=bank.exercises.find(e=>e.id==='speaking-1-17').paragraphs.map(p=>p.fr).join(' ');
 for(const word of ['diplômé','goût','Mes amis','même','qualification'])assert.ok(oral.includes(word),'repaired font glyph: '+word);
 const writing=bank.exercises.find(e=>e.id==='writing-2024-6-cn');
 assert.ok(writing.paragraphs.some(p=>p.fr==='Les devoirs du soir sont source d’inégalités'));
 assert.ok(!writing.paragraphs.some(p=>p.fr.startsWith('Vous écrivez à la rédaction')));
 assert.ok(writing.tasks.some(t=>t.fr.startsWith('Vous écrivez à la rédaction')));
});
