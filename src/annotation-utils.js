// Keep annotations aligned with edited answers, without discarding notebook entries.
export function rebaseMarks(marks,pid,before,after){
 let prefix=0;while(prefix<before.length&&prefix<after.length&&before[prefix]===after[prefix])prefix++;
 let suffix=0;while(suffix<before.length-prefix&&suffix<after.length-prefix&&before[before.length-1-suffix]===after[after.length-1-suffix])suffix++;
 const oldEnd=before.length-suffix,newEnd=after.length-suffix,delta=after.length-before.length;
 return marks.map(a=>{if(a.pid!==pid||a.detached)return a;
  if(a.end<=prefix)return a;
  if(a.start>=oldEnd)return {...a,start:a.start+delta,end:a.end+delta};
  const start=Math.min(a.start,prefix),end=a.end>=oldEnd?a.end+delta:newEnd;
  if(end<=start)return {...a,detached:true};
  return {...a,start,end,text:after.slice(start,end)};
 });
}
export function visibleMarks(marks,pid,text){return marks.filter(a=>a.pid===pid&&!a.detached&&a.start>=0&&a.end<=text.length&&text.slice(a.start,a.end)===a.text);}
export function reconcileAnnotations(exercises,annotations){
 const byId=new Map(exercises.map(e=>[e.id,e]));let changed=false;
 const result=Object.fromEntries(Object.entries(annotations).map(([id,marks])=>{
  const e=byId.get(id);if(!e)return[id,marks];
  return[id,marks.map(a=>{
   if(/^(?:question:|option:|answer:|draft:|task:|reference:)|^(?:exercise|speaking)-title$/.test(a.pid))return a;
   const current=e.paragraphs.find(p=>p.id===a.pid);
   if(current?.fr.slice(a.start,a.end)===a.text&&!a.detached)return a;
   const preferred=current?.fr.indexOf(a.text)??-1;
   let target=preferred>=0?{p:current,index:preferred}:null;
   if(!target){const matches=e.paragraphs.flatMap(p=>{const index=p.fr.indexOf(a.text);return index>=0?[{p,index}]:[];});if(matches.length===1)target=matches[0];}
   if(target){changed=true;return {...a,pid:target.p.id,start:target.index,end:target.index+a.text.length,detached:false};}
   if(!a.detached){changed=true;return {...a,detached:true};}return a;
  })];
 }));return changed?result:annotations;
}
