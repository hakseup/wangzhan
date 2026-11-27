import fs from'node:fs';import{sentenceRanges}from'../src/sentence-alignment.js';
const root=new URL('../',import.meta.url),folder=new URL('data/imports/2026-11/',root),paths=['new-exercises.json','canonical-upgrades.json'];
const choices={...JSON.parse(fs.readFileSync(new URL('review-link-choices.json',folder))),...JSON.parse(fs.readFileSync(new URL('review-link-corrections.json',folder)))};
const normalize=s=>s.normalize('NFC').toLowerCase().replace(/[\s\p{P}\p{S}]/gu,'');
const grams=s=>{const a=Array.from(normalize(s));return new Set(a.slice(0,-1).map((c,i)=>c+a[i+1]));};
const score=(a,b)=>{const x=grams(a),y=grams(b);return x.size+y.size?2*[...x].filter(x=>y.has(x)).length/(x.size+y.size):0;};
let count=0;
for(const name of paths){const file=new URL(name,folder),items=JSON.parse(fs.readFileSync(file));
 for(const e of items){
  if(!e.reviewPassages)continue;
  for(const p of e.paragraphs){const pairs=e.reviewPassages.filter(q=>q.pid===p.id);if(!pairs.length)continue;p.reviewLinks=[];
   const sources=sentenceRanges(p.fr,'fr'),targets=sentenceRanges(p.zh,'zh');
   for(const pair of pairs){
    const source=sources.find(s=>s.start<=pair.start&&s.end>pair.start&&s.text.trim()===pair.fr);if(!source)throw Error('Source changed: '+pair.id);
    const chosen=choices[pair.id];
    const target=chosen!==undefined?targets.find(t=>t.start===chosen):[...targets].sort((a,b)=>score(pair.zh,b.text)-score(pair.zh,a.text))[0];
    if(!target)throw Error('Translation changed: '+pair.id);
    p.reviewLinks.push({frStart:pair.start,fr:pair.fr,zhStart:target.start,zh:target.text.trim()});count++;
   }
  }
 }
 fs.writeFileSync(file,JSON.stringify(items));
}
console.log('Stored',count,'verified links to individual Chinese sentences.');
