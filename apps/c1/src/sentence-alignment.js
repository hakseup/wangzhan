// Sentence-only alignment. Never use a paragraph element as a fallback target.
const normalize=s=>String(s||'').normalize('NFC').toLowerCase().replace(/[\s\p{P}\p{S}]/gu,'');
const grams=s=>{const a=Array.from(normalize(s));return new Set(a.slice(0,-1).map((c,i)=>c+a[i+1]));};
const dice=(a,b)=>a.size+b.size?2*[...a].filter(x=>b.has(x)).length/(a.size+b.size):0;
const stop=new Set('avec dans pour plus moins aussi ainsi mais même être avoir faire cette celui celle nous vous leurs elles ils une des les aux par qui que pas sur est sont ses son ces tout tous toute comme sans entre parce dont alors très autre après avant'.split(' '));
export function sentenceRanges(text,language){
 if(!text)return [];
 if(typeof Intl.Segmenter==='function')return [...new Intl.Segmenter(language,{granularity:'sentence'}).segment(text)].map(s=>({start:s.index,end:s.index+s.segment.length,text:s.segment}));
 const boundary=language==='fr'?/[.!?…](?:\s*[»”")])?\s+(?=[A-ZÀ-ÖØ-Þ«“])/gu:/[。！？!?](?:[”」』"])?\s*/gu;
 const out=[];let start=0;for(const m of text.matchAll(boundary)){const end=m.index+m[0].length;out.push({start,end,text:text.slice(start,end)});start=end;}if(start<text.length)out.push({start,end:text.length,text:text.slice(start)});return out;
}
function vocabulary(text,lexicon){
 const terms=new Set();
 for(const raw of text.toLowerCase().replaceAll('’',"'").match(/[\p{L}]+(?:[-'][\p{L}]+)*/gu)||[]){
  const word=raw.replace(/^(?:l|d|s|n|qu|c|j|m|t)'/,'');if(word.length<3||stop.has(word))continue;
  const candidates=[word,lexicon?.aliases?.[word],...(lexicon?.formLemmas?.[word]||[])],entry=candidates.map(w=>lexicon?.entries?.[w]).find(Boolean);
  for(const definition of [entry?.zh,...(entry?.senses||[]).slice(0,3).map(s=>s.zh)])for(const term of definition?.match(/[\p{Script=Han}]{2,8}/gu)||[])terms.add(term);
 }
 return [...terms];
}
export function alignSentences(source,target,hints,lexicon){
 const n=source.length,m=target.length;if(!n||!m)return {forward:source.map(()=>null),backward:target.map(()=>null)};
 const refs=hints.map(x=>grams(x)),targets=target.map(t=>({normal:normalize(t.text),grams:grams(t.text)}));
 const terms=source.map(s=>vocabulary(s.text,lexicon));
 const semantic=source.map((s,i)=>target.map((t,j)=>{
  const reference=dice(refs[i],targets[j].grams);
  const hits=terms[i].filter(term=>targets[j].normal.includes(term)).length;
  const lexical=terms[i].length?Math.min(1,hits/Math.min(terms[i].length,8)):0;
  const names=[...s.text.matchAll(/\b(?:[A-ZÀ-ÖØ-Þ][\p{L}]{2,}|\d+(?:[.,]\d+)?)\b/gu)].map(x=>normalize(x[0]));
  const anchors=names.filter(x=>targets[j].normal.includes(x)).length/Math.max(1,names.length);
  return Math.max(reference,.65*lexical)+.12*anchors;
 }));
 // Align by text evidence and relative translated length, allowing one sentence
 // to have been split or merged in the existing translation. Counts alone do not
 // establish correspondence, and the hover target is always a single sentence.
 const lengths=sentences=>sentences.map(s=>Math.max(1,normalize(s.text).length));
 const fl=lengths(source),zl=lengths(target),ratio=fl.reduce((a,b)=>a+b,0)/zl.reduce((a,b)=>a+b,0);
 const cost=Array.from({length:n+1},()=>Array(m+1).fill(Infinity)),previous=Array.from({length:n+1},()=>Array(m+1));cost[0][0]=0;
 const shapes=[[1,1],...Array.from({length:n-1},(_,i)=>[i+2,1]),...Array.from({length:m-1},(_,i)=>[1,i+2])];
 for(let i=1;i<=n;i++)for(let j=1;j<=m;j++)for(const [a,b] of shapes){
  if(a>i||b>j)continue;
  const f=fl.slice(i-a,i).reduce((x,y)=>x+y,0),z=zl.slice(j-b,j).reduce((x,y)=>x+y,0)*ratio;
  let evidence=0;for(let x=i-a;x<i;x++)evidence+=Math.max(...semantic[x].slice(j-b,j));evidence/=a;
  const candidate=cost[i-a][j-b]+1.5*Math.abs(Math.log((f+8)/(z+8)))+.23*(a+b-2)-.6*evidence;
  if(candidate<cost[i][j]){cost[i][j]=candidate;previous[i][j]=[a,b];}
 }
 const path=[];let i=n,j=m;while(i&&j){const [a,b]=previous[i][j];for(let x=i-a;x<i;x++)for(let y=j-b;y<j;y++)path.push([x,y]);i-=a;j-=b;}
 function choose(candidates,scores,position,references){
  const ranked=references.map((score,index)=>({score,index})).sort((a,b)=>b.score-a.score);
  // Only independently translated sentence text can override the monotone path.
  if(ranked[0].score>=.55&&ranked[0].score-(ranked[1]?.score||0)>=.1)return ranked[0].index;
  return candidates.sort((a,b)=>(scores[b]-.12*Math.abs(position-(b+.5)/scores.length))-(scores[a]-.12*Math.abs(position-(a+.5)/scores.length)))[0];
 }
 return {forward:source.map((_,i)=>choose(path.filter(p=>p[0]===i).map(p=>p[1]),semantic[i],(i+.5)/n,targets.map(t=>dice(refs[i],t.grams)))),backward:target.map((_,j)=>choose(path.filter(p=>p[1]===j).map(p=>p[0]),source.map((_,i)=>semantic[i][j]),(j+.5)/m,source.map((_,i)=>dice(refs[i],targets[j].grams))))};
}
