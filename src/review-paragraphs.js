// Keep every source character and full paragraph translation; evidence is an overlay.
const normalized=s=>s.normalize('NFC').toLowerCase().replace(/[\s\p{P}\p{S}]/gu,'');
const grams=s=>{const chars=Array.from(normalized(s));return new Set(chars.slice(0,-1).map((c,i)=>c+chars[i+1]));};
function similarity(a,b){const x=grams(a),y=grams(b);return x.size+y.size?2*[...x].filter(g=>y.has(g)).length/(x.size+y.size):0;}
function chineseMatches(text,pairs){
 const units=[...text.matchAll(/[^。！？]+[。！？]?/gu)].map(m=>({start:m.index,end:m.index+m[0].length})),matches=[];
 for(const pair of pairs){
  const candidates=[];
  for(let i=0;i<units.length;i++)for(let j=i;j<Math.min(i+3,units.length);j++){
   const start=units[i].start,end=units[j].end,s=text.slice(start,end),ratio=normalized(s).length/Math.max(1,normalized(pair.zh).length);
   if(ratio<.55||ratio>1.8)continue;
   candidates.push({start,end,id:pair.id,score:similarity(s,pair.zh)});
  }
  candidates.sort((a,b)=>b.score-a.score);
  const best=candidates[0];
  // Wording must strongly agree; never pair sentences merely by their count or position.
  if(best?.score>=.68&&best.score-(candidates[1]?.score||0)>=.08&&!matches.some(m=>m.start<best.end&&m.end>best.start))matches.push(best);
 }
 const bounds=[...new Set([0,text.length,...matches.flatMap(m=>[m.start,m.end])])].sort((a,b)=>a-b);
 return bounds.slice(0,-1).map((start,i)=>({start,text:text.slice(start,bounds[i+1]),pairId:matches.find(m=>m.start<=start&&m.end>=bounds[i+1])?.id}));
}
export function buildReviewParagraphs(exercise){
 return exercise.paragraphs.map((paragraph,index)=>{
  const pairs=(exercise.reviewPassages||[]).filter(p=>p.pid===paragraph.id);
  const quotes=exercise.questions.flatMap(q=>(q.explanation?.evidence||[]).filter(x=>x.pid===paragraph.id).map(x=>({start:paragraph.fr.indexOf(x.quote),end:paragraph.fr.indexOf(x.quote)+x.quote.length,number:q.number}))).filter(x=>x.start>=0);
  const bounds=[...new Set([0,paragraph.fr.length,...pairs.flatMap(p=>[p.start,p.start+p.fr.length]),...quotes.flatMap(q=>[q.start,q.end])])].sort((a,b)=>a-b);
  const seen=new Set(),units=[];
  for(let i=0;i<bounds.length-1;i++){
   const start=bounds[i],end=bounds[i+1],pair=pairs.find(p=>p.start<=start&&p.start+p.fr.length>=end),id=pair?.id||`${exercise.id}:${paragraph.id}:context:${start}`;
   const covering=quotes.filter(q=>q.start<end&&q.end>start),numbers=[...new Set(covering.map(q=>q.number))],labels=numbers.filter(n=>!seen.has(n));labels.forEach(n=>seen.add(n));
   const run={start,text:paragraph.fr.slice(start,end),answer:numbers.length>0,labels};
   if(units.at(-1)?.id===id)units.at(-1).runs.push(run);else units.push({id,pairId:pair?.id,runs:[run]});
  }
  return {...paragraph,index,contextId:`${exercise.id}:${paragraph.id}:paragraph`,pairs,units,translation:chineseMatches(paragraph.zh||'',pairs)};
 });
}
