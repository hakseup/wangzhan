import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync,existsSync} from 'node:fs';
import {gradeQuestion,gradeExercise,annotationParts,wordCount,validImport,EMPTY_STATE} from '../src/lib.js';

const bank=JSON.parse(readFileSync(new URL('../public/content.json',import.meta.url)));
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

