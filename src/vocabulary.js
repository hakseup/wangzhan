import {CORE_WORDS,WRITING_WORDS,SPEAKING_WORDS,parseWords} from './word-seeds.js';
export const BOOKS=[{id:'listening',name:'听力词'},{id:'reading',name:'阅读词'},{id:'writing',name:'写作词'},{id:'speaking',name:'口语词'},{id:'personal',name:'个人高亮收藏单词本'}];
export const canonical=s=>String(s).normalize('NFC').toLocaleLowerCase('fr').replace(/[’‘]/g,"'").replace(/\s+/g,' ').trim();
export const wordId=fr=>'word:'+canonical(fr);
const lexical=s=>canonical(s).normalize('NFD').replace(/[\u0300-\u036f]/g,'');
export function makeBooks(exercises,state,lexicon){
 if(lexicon?.books){const byId=new Map(exercises.map(e=>[e.id,e]));return {...Object.fromEntries(Object.entries(lexicon.books).map(([category,words])=>[category,words.map(fr=>{const e=lexicon.entries[fr];return {...e,fr,id:wordId(fr),sources:(e.sources||[]).map(id=>byId.get(id)).filter(e=>e&&(category==='listening'?['long','short'].includes(e.category):e.category===category)).map(e=>({id:e.id,title:e.titleZh}))};})])),personal:makePersonalWords(exercises,state)};}
 const core=parseWords(CORE_WORDS),byCategory=categories=>exercises.filter(e=>categories.includes(e.category));
 const fromCorpus=categories=>{
  const corpus=byCategory(categories).map(e=>({e,text:' '+lexical([e.title,...e.paragraphs.map(p=>p.fr),...e.questions.map(q=>q.prompt+' '+(q.options||[]).map(o=>o.text).join(' '))].join(' '))+' '}));
  return core.flatMap(w=>{const stem=lexical(w.fr),match=corpus.filter(({text})=>text.includes(stem)&&new RegExp('(^|[^a-z])'+stem.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')+'(?:s|es|e|x)?(?=[^a-z]|$)').test(text));return match.length?[{...w,id:wordId(w.fr),sources:match.map(({e})=>({id:e.id,title:e.titleZh}))}]:[];});
 };
 const output=(type,seed)=>{const all=[...parseWords(seed),...fromCorpus([type])];return [...new Map(all.map(w=>[canonical(w.fr),{...w,id:wordId(w.fr),sources:w.sources||[],usage:type==='writing'?'通用论证与篇章表达':'观点表达与互动讨论'}])).values()];};
 const personal=makePersonalWords(exercises,state);
 return {listening:fromCorpus(['long','short']),reading:fromCorpus(['reading']),writing:output('writing',WRITING_WORDS),speaking:output('speaking',SPEAKING_WORDS),personal};
}
export function makePersonalWords(exercises,state){
 return [...new Map(Object.entries(state.annotations).flatMap(([id,marks])=>marks.filter(m=>m.note?.trim()&&m.text?.trim()&&/^[\p{L}]+(?:[’'\-][\p{L}]+)*$/u.test(m.text.trim())).map(m=>({id:wordId(m.text),fr:m.text,zh:state.vocabDefinitions?.[wordId(m.text)]||m.note||'',sources:[{id,title:exercises.find(e=>e.id===id)?.titleZh||'个人标注'}]}))).map(w=>[w.id,w])).values()];
}
export const REVIEW_DAYS=[1,2,4,7,15,30,60];
export function scheduleReview(previous,correct,now=Date.now()){
 const step=correct?Math.min((previous?.step??-1)+1,REVIEW_DAYS.length-1):-1;
 return {step,due:now+(correct?REVIEW_DAYS[step]*86400000:600000),lastReviewed:now,reviews:(previous?.reviews||0)+1,lapses:(previous?.lapses||0)+(correct?0:1)};
}
export function buildQueue(words,progress,mode,now=Date.now(),newLimit=Infinity){
 const eligible=words.filter(w=>mode==='spelling'||w.zh?.trim());
 const due=eligible.filter(w=>progress[w.id]&&progress[w.id].due<=now).sort((a,b)=>progress[a.id].due-progress[b.id].due);
 const fresh=eligible.filter(w=>!progress[w.id]).slice(0,Math.max(0,newLimit));
 return [...due,...fresh];
}
export function choicesFor(word,words){
 const alternatives=[...new Set(words.filter(w=>w.zh&&w.zh!==word.zh).map(w=>w.zh))].sort(()=>Math.random()-.5).slice(0,3);
 return [word.zh,...alternatives].map(value=>({value,rank:Math.random()})).sort((a,b)=>a.rank-b.rank).map(x=>x.value);
}
