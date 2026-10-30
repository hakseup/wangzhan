import {sentenceRanges,alignSentences} from './sentence-alignment.js';
// Keep all source/translation characters and original annotation coordinates.
export function buildReviewParagraphs(exercise,lexicon){
 return exercise.paragraphs.map((paragraph,index)=>{
  const pairs=(exercise.reviewPassages||[]).filter(p=>p.pid===paragraph.id);
  const quotes=exercise.questions.flatMap(q=>(q.explanation?.evidence||[]).filter(x=>x.pid===paragraph.id).map(x=>({start:paragraph.fr.indexOf(x.quote),end:paragraph.fr.indexOf(x.quote)+x.quote.length,number:q.number,candidate:x.confirmed===false}))).filter(x=>x.start>=0);
  const sentences=sentenceRanges(paragraph.fr,'fr'),seen=new Set();
  const units=sentences.map(sentence=>{
   const evidenceIds=pairs.filter(p=>p.start>=sentence.start&&p.start<sentence.end).map(p=>p.id);
   const bounds=[...new Set([sentence.start,sentence.end,...quotes.flatMap(q=>[q.start,q.end]).filter(x=>x>sentence.start&&x<sentence.end)])].sort((a,b)=>a-b);
   const runs=bounds.slice(0,-1).map((start,i)=>{const end=bounds[i+1],numbers=[...new Set(quotes.filter(q=>q.start<end&&q.end>start).map(q=>q.number))],labels=numbers.filter(n=>!seen.has(n));labels.forEach(n=>seen.add(n));return {start,text:paragraph.fr.slice(start,end),answer:numbers.length>0,candidate:numbers.length>0&&quotes.filter(q=>q.start<end&&q.end>start).every(q=>q.candidate),labels};});
   return {...sentence,id:evidenceIds[0]||`${exercise.id}:${paragraph.id}:sentence:${sentence.start}`,pairId:evidenceIds[0],evidenceIds,runs};
  });
  let translation=sentenceRanges(paragraph.zh||'','zh').map(t=>({...t,id:`${exercise.id}:${paragraph.id}:zh:${t.start}`}));
  const hints=units.map(u=>pairs.find(p=>p.fr.trim()===u.text.trim())?.zh||'');
  let alignment;
  if(!paragraph.translationReviewed&&paragraph.sentenceTranslations?.length===units.length){let offset=0;translation=paragraph.sentenceTranslations.map((s,i)=>{const start=offset;offset+=s.zh.length;return {start,end:offset,text:s.zh,id:`${exercise.id}:${paragraph.id}:zh:${i}`};});alignment={forward:units.map((_,i)=>i),backward:units.map((_,i)=>i)};}else alignment=alignSentences(units,translation,hints,lexicon);
  units.forEach((u,i)=>{u.translationId=translation[alignment.forward[i]]?.id;});
  translation.forEach((t,i)=>{t.sourceId=units[alignment.backward[i]]?.id;t.pairId=t.sourceId;});
  return {...paragraph,index,pairs,units,translation};
 });
}
export function activeSentenceLinks(paragraph,active){
 const source=paragraph.units.find(u=>u.id===active||u.evidenceIds.includes(active));
 if(source)return {sourceId:source.id,translationId:source.translationId};
 const translation=paragraph.translation.find(t=>t.id===active);
 return translation?{sourceId:translation.sourceId,translationId:translation.id}:{};
}

