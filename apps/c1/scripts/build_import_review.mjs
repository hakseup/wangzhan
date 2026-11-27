// Build complete answer-sentence pairs only for newly reviewed source assets.
// Existing exercise paragraphs, offsets, highlights and review pairs are untouched.
import fs from 'node:fs';
import {sentenceRanges,alignSentences} from '../src/sentence-alignment.js';
import {mergeLexiconParts} from '../src/bank.js';
const root=new URL('../',import.meta.url),path=new URL('data/imports/2026-11/new-exercises.json',root);
let bank=JSON.parse(fs.readFileSync(new URL('public/content.json',root),'utf8'));
bank=mergeLexiconParts(bank,(bank.lexiconFiles||[]).map(p=>JSON.parse(fs.readFileSync(new URL('public'+p,root),'utf8'))));
const paths=[path,new URL('data/imports/2026-11/canonical-upgrades.json',root)],groups=paths.map(p=>JSON.parse(fs.readFileSync(p,'utf8'))),exercises=groups.flat(),audit=[];
for(const e of exercises){
 if(!['long','short','reading'].includes(e.category))continue;
 const overrides=JSON.parse(fs.readFileSync(new URL('data/imports/2026-11/review-sentence-translations.json',root),'utf8'));
 const pairs=new Map();
 for(const [index,p]of e.paragraphs.entries()){
  const sentences=sentenceRanges(p.fr,'fr'),translations=sentenceRanges(p.zh,'zh');
  const evidence=e.questions.flatMap(q=>q.explanation.evidence.filter(v=>v.pid===p.id).map(v=>({q,v,start:p.fr.indexOf(v.quote),end:p.fr.indexOf(v.quote)+v.quote.length})));
  const hints=sentences.map(s=>overrides[s.text.trim()]||evidence.find(x=>x.v.quote.trim()===s.text.trim())?.v.zh||'');
  const alignment=alignSentences(sentences,translations,hints,bank.lexicon);
  for(const {q,v,start,end}of evidence){
   if(start<0)throw Error(e.id+': invalid quote');
   const overlapped=sentences.map((s,i)=>({...s,i})).filter(s=>s.start<end&&s.end>start);if(!overlapped.length)throw Error(e.id+': quote has no sentence');
   v.pairIds=[];
   for(const s of overlapped){
    const lead=s.text.length-s.text.trimStart().length,fr=s.text.trim(),pos=s.start+lead,id=`${e.id}:${p.id}:${pos}`;
    if(p.fr.slice(pos,pos+fr.length)!==fr)throw Error('Invalid exact sentence');
    const exact=v.quote.trim()===fr;
    const zh=overrides[fr]||(exact?v.zh:translations[alignment.forward[s.i]]?.text);
    if(!zh||!/[\u4e00-\u9fff]/.test(zh))throw Error(e.id+': untranslated sentence');
    if(!pairs.has(id))pairs.set(id,{id,pid:p.id,start:pos,fr,zh:zh.trim(),questionIds:[],paragraphNumber:index+1});
    const pair=pairs.get(id);if(!pair.questionIds.includes(q.id))pair.questionIds.push(q.id);v.pairIds.push(id);
    if(!exact)audit.push({exercise:e.id,question:q.id,fr,zh:pair.zh,quote:v.quote,quoteZh:v.zh});
   }
   // The UI displays and highlights whole answer sentences for newly supplied exercises.
   if(v.quote.length<=20){const first=overlapped[0],last=overlapped.at(-1);v.quote=p.fr.slice(first.start,last.end).trim();}
  }
 }
 e.reviewPassages=[...pairs.values()].sort((a,b)=>a.paragraphNumber-b.paragraphNumber||a.start-b.start);
}
paths.forEach((p,i)=>fs.writeFileSync(p,JSON.stringify(groups[i])));
fs.writeFileSync(new URL('data/imports/2026-11/review-alignment-audit.json',root),JSON.stringify(audit,null,2));
console.log('Built',exercises.reduce((n,e)=>n+(e.reviewPassages?.length||0),0),'exact full source-sentence pairs.');
