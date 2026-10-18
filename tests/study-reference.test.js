import {loadBankFixture} from './bank-fixture.js';
import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {makePersonalWords,buildQueue} from '../src/vocabulary.js';
import {removeHighlight} from '../src/annotation-utils.js';
import {lookupWord,queryParts,translateSelection,restoreQueryNames} from '../src/dictionary.js';
import {EMPTY_STATE,validImport} from '../src/lib.js';
const bank=loadBankFixture();
test('all 547 comprehension questions have a reason and exact source evidence',()=>{
 let count=0;for(const e of bank.exercises.filter(e=>['long','short','reading'].includes(e.category)))for(const q of e.questions){count++;assert.ok(q.explanation.reason?.length>8,e.id+q.id);assert.ok(q.explanation.evidence.length>0,e.id+q.id);for(const x of q.explanation.evidence){const p=e.paragraphs.find(p=>p.id===x.pid);assert.ok(p?.fr.includes(x.quote),e.id+q.id);assert.ok(x.quote.length>20);}}
 assert.equal(count,547);
});
test('every writing/oral set has complete templates, word limits and a six-question debate',()=>{
 let count=0;for(const e of bank.exercises.filter(e=>['writing','speaking'].includes(e.category))){assert.equal(e.studyModels.length,2,e.id);for(const m of e.studyModels){count++;const text=m.paragraphs.join(' '),words=text.split(/\s+/).length;assert.ok(!/\[(?:主题|THÈME|原因|措施|phénomène|argument)\]/.test(text));if(m.id==='synthese'){assert.ok(words>=200&&words<=240,e.id+':'+words);assert.ok(!/\bje pense|\bselon moi/i.test(text));}if(m.id==='essai')assert.ok(words>=250);if(m.id==='monologue'){assert.ok(words>650);assert.match(text,/Problématique et plan/);assert.match(text,/Conclusion/);}if(m.id==='debat')assert.equal(m.paragraphs.filter(x=>/^\d+\./.test(x)).length,6);}}
 assert.equal(count,226);
});
test('only noted short vocabulary enters personal book, and new study queues have no daily cap',()=>{
 const notes=[{id:'a',text:'confiance',note:'信任',level:0},{id:'b',text:'partager',note:'',level:1},{id:'c',text:'Les gens partagent leurs connaissances.',note:'人们分享知识',level:1},{id:'d',text:'Je vous remercie de votre attention',note:'感谢',level:1}];
 assert.deepEqual(makePersonalWords([],{annotations:{a:notes}}).map(w=>w.fr),['confiance']);const words=Array.from({length:900},(_,i)=>({id:'w'+i,fr:'w'+i,zh:'词'+i}));assert.equal(buildQueue(words,{},'choice',1).length,900);
});
test('removing only the selected color preserves attached notes and outside highlights',()=>{
 const mark={id:'x',pid:'p',start:0,end:10,text:'abcdefghij',level:2,note:'备注'};const result=removeHighlight([mark],[{pid:'p',start:2,end:5}]);assert.deepEqual(result.map(x=>[x.start,x.end,x.level]),[[0,2,2],[2,5,0],[5,10,2]]);assert.ok(result.every(x=>x.note==='备注'));assert.deepEqual(removeHighlight([{...mark,note:''}],[{pid:'p',start:0,end:10}]),[]);
});
test('dictionary supports conjugations, POS senses, word families and phrase components',()=>{
 const e=lookupWord(bank.lexicon,'étaient');assert.ok(e?.senses.some(s=>s.pos==='v'));const f=lookupWord(bank.lexicon,'fabricants');assert.equal(f.fr,'fabricant');assert.ok(f.senses.some(s=>s.pos==='n'));assert.ok(queryParts(bank.lexicon,'mettre en évidence').every(p=>p.entry));assert.ok(lookupWord(bank.lexicon,'pollution')?.related?.length);
});
test('explicitly enabled online fallback sends only the current query and handles quota limits',async()=>{
 const before=globalThis.fetch;let called;
 globalThis.fetch=async(url,options)=>{called={url:new URL(url),options};return {ok:true,json:async()=>({responseStatus:200,responseData:{translatedText:'这是经授权的补充译文。'}})};};
 try{await assert.rejects(translateSelection('Une phrase encore inconnue.',{lexicon:{},allowOnline:false}),/尚未收录/);assert.equal(called,undefined);const r=await translateSelection('Une phrase encore inconnue.',{lexicon:{},allowOnline:true});assert.equal(r.text,'这是经授权的补充译文。');assert.equal(called.url.searchParams.get('q'),'Une phrase encore inconnue.');assert.equal(called.options.credentials,'omit');assert.equal(called.options.referrerPolicy,'no-referrer');globalThis.fetch=async()=>({ok:true,json:async()=>({responseStatus:429,responseDetails:'LIMIT'})});await assert.rejects(translateSelection('Une requête différente.',{lexicon:{},allowOnline:true}),/额度/);}finally{globalThis.fetch=before;}
});
test('sentence translation stays on device and never sends query text through fetch',async()=>{
 const oldTranslator=globalThis.Translator,oldFetch=globalThis.fetch;let called=false;
 globalThis.fetch=()=>{called=true;throw Error('must not send text');};
 globalThis.Translator={availability:async()=> 'available',create:async()=>({translate:async text=>text.includes('temps')?'我们需要更多时间。':'新的本地译文。'})};
 try{const r=await translateSelection('Nous avons besoin de plus de temps.',{lexicon:{}});assert.equal(r.text,'我们需要更多时间。');assert.equal(called,false);}finally{globalThis.Translator=oldTranslator;globalThis.fetch=oldFetch;}
});
test('model edits survive backups while malformed rich content state is rejected',()=>{const x=structuredClone(EMPTY_STATE);x.modelEdits={sample:'<p><strong>Bonjour</strong></p>'};assert.ok(validImport(x));x.modelEdits.sample={html:'bad'};assert.equal(validImport(x),false);assert.equal(restoreQueryNames('Paris et France','巴黎和法国',[['Paris','巴黎'],['France','法国']]),'Paris和France');});
