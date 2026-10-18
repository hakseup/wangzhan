import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {lookup,wordEntries} from '../src/lookup.js';
import {removeHighlights,removeAnnotationNote,savedVocabulary,validImport,EMPTY_STATE} from '../src/lib.js';
const bank=JSON.parse(readFileSync(new URL('../public/lexicon.json',import.meta.url)));
test('dictionary keeps POS senses separate and resolves conjugation, gender, plurals and elision',()=>{
 for(const pos of ['adv','adj','n'])assert.ok(lookup(bank,'bien').entryResults.some(r=>r.entries.some(e=>e.pos===pos)),'bien '+pos);
 for(const [form,lemma] of [['étaient','être'],['maisons','maison'],['couraient','courir'],['l’environnement','environnement']])assert.ok(wordEntries(bank,form).some(r=>r.lemma===lemma),form);
 assert.ok(lookup(bank,'pouvoir').entryResults[0].entries.some(e=>e.pos==='n'&&e.senses.some(s=>s.includes('权力'))));
 assert.doesNotThrow(()=>lookup(bank,'constructor'));
 assert.ok(wordEntries(bank,'orange').some(r=>r.entries.some(e=>e.pos==='n'&&e.senses.some(s=>/橙|桔/.test(s)))),'a capitalized place name must not erase the common noun');
 assert.deepEqual(wordEntries(bank,'de').map(r=>r.lemma),['de'],'a functional word does not inherit unrelated headwords');
 assert.deepEqual(wordEntries(bank,'Paris').map(r=>r.lemma),['paris'],'the city is distinct from lowercase paris, the plural of pari');
 assert.notDeepEqual(wordEntries(bank,'pêche').map(r=>r.lemma),wordEntries(bank,'péché').map(r=>r.lemma));
});
test('idioms resolve inflected verbs without treating every noun as a verb; components retain article meaning',()=>{
 for(const text of ['prendre en compte','pris en compte','a pris en compte'])assert.ok(lookup(bank,text).entryResults.some(r=>r.lemma==='prendre en compte'),text);
 const phrase=lookup(bank,'prendre en compte');assert.equal(phrase.components.length,3);assert.ok(phrase.entryResults[0].entries[0].senses[0].includes('考虑'));
 assert.ok(lookup(bank,'Il faut tenir compte des différences').translation.includes('差异'));
 assert.ok(lookup(bank,'développement').related.some(r=>r.word==='développer'));
 assert.ok(wordEntries(bank,"l'")[0].entries.some(e=>e.pos==='article'));
});
test('removing partial overlapping highlights preserves full note and outside highlight spans',()=>{
 const marks=[{id:'a',pid:'p0',start:0,end:10,text:'abcdefghij',level:2,note:'释义'},{id:'b',pid:'p0',start:4,end:8,text:'efgh',level:1,note:''}];
 const next=removeHighlights(marks,[{pid:'p0',start:3,end:7}]);
 assert.equal(next.find(a=>a.id==='a').note,'释义');assert.equal(next.find(a=>a.id==='a').level,0);
 assert.deepEqual(next.filter(a=>a.level).map(a=>[a.start,a.end,a.text]),[[0,3,'abc'],[7,10,'hij'],[7,8,'h']]);
 assert.equal(removeHighlights(marks,[{pid:'p0',start:0,end:10}]).length,1);
 assert.equal(removeAnnotationNote(marks,'a').find(a=>a.id==='a').level,2);
 assert.equal(removeAnnotationNote([{...marks[0],level:0}],'a').length,0);
 assert.equal(savedVocabulary([{id:'e'}],{e:[...marks,{...marks[1],id:'c',note:'  '}]}).length,1);
 assert.equal(validImport({...structuredClone(EMPTY_STATE),annotations:{e:next}}),true);
});
