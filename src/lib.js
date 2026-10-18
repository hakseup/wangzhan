export const CATEGORIES = [
  {id:'all',name:'全部练习',fr:'La bibliothèque',color:'cream'},
  {id:'long',name:'长听力',fr:'Écoute longue',color:'lavender',icon:'headphones'},
  {id:'short',name:'短听力',fr:'Écoute courte',color:'blue',icon:'audio'},
  {id:'reading',name:'阅读',fr:'Compréhension écrite',color:'green',icon:'book'},
  {id:'writing',name:'写作',fr:'Production écrite',color:'pink',icon:'pen'},
  {id:'speaking',name:'口语',fr:'Production orale',color:'yellow',icon:'mic'},
];
export const TOPICS=['全部主题','教育与成长','科技与社会','语言与文化','社会与生活','健康与科学','工作与经济','城市与环境'];
export const EMPTY_STATE={version:1,answers:{},attempts:{},drafts:{},annotations:{},bookmarks:[],activity:[],rubrics:{},vocabProgress:{},vocabDaily:{},vocabDefinitions:{},fontSize:18};
export const STORAGE_KEY='noix-dalf-c1-v1';
export function normalize(s){return String(s??'').normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase().replace(/[^\p{L}\p{N}]/gu,'');}
export function wordCount(s){return (s.trim().match(/[\p{L}\p{N}]+(?:[’'\-][\p{L}\p{N}]+)*/gu)||[]).length;}
export function gradeQuestion(q,value,justification=''){
  if(!String(value??'').trim())return {status:'unanswered'};
  if(!q.answer)return {status:'review',message:'原资料未提供可核实的标准答案，请结合原文自评。'};
  const ref=q.answer.reference||'';
  if(q.type==='choice' && q.answer.value){return {status:value===q.answer.value?'correct':'incorrect',reference:ref,expected:q.answer.value};}
  if(q.type==='tf'&&q.answer.value){
    if(value!==q.answer.value)return {status:'incorrect',reference:ref,expected:q.answer.value};
    return justification.trim()?{status:'review',choiceCorrect:true,reference:ref,message:'判断选项正确；引用依据需对照参考答案核实。'}:{status:'review',choiceCorrect:true,reference:ref,message:'判断选项正确，请补充原文依据后自评。'};
  }
  const accepted=[...(q.answer.accepted||[]),ref,ref.split(/[\u4e00-\u9fff]/u)[0].trim()].filter(Boolean);
  if(accepted.some(x=>normalize(x)===normalize(value)))return {status:'correct',reference:ref};
  return {status:'review',reference:ref,message:'开放回答可以有不同表述，请对照参考答案自评。'};
}
export function gradeExercise(exercise,answers){
  return Object.fromEntries(exercise.questions.map(q=>[q.id,gradeQuestion(q,answers?.[q.id]?.value,answers?.[q.id]?.justification)]));
}
export function annotationParts(text,annotations=[]){
  const valid=annotations.filter(a=>a.start>=0&&a.end<=text.length&&a.end>a.start);
  const bounds=[...new Set([0,text.length,...valid.flatMap(a=>[a.start,a.end])])].sort((a,b)=>a-b);
  return bounds.slice(0,-1).map((start,i)=>{
    const end=bounds[i+1],cover=valid.filter(a=>a.start<=start&&a.end>=end);
    return {start,end,text:text.slice(start,end),level:Math.max(0,...cover.map(a=>a.level||0)),notes:cover.filter(a=>a.note),annotation:cover.at(-1)};
  });
}
export function readStored(){
  try{const x=JSON.parse(localStorage.getItem(STORAGE_KEY)||'null');return x&&validImport({...EMPTY_STATE,...x})?{...EMPTY_STATE,...x,fontSize:Math.max(14,Math.min(26,Number(x.fontSize)||18))}:structuredClone(EMPTY_STATE);}catch{return structuredClone(EMPTY_STATE);}
}
export function validImport(x){
  if(!x||x.version!==1)return false;
  for(const k of ['answers','attempts','drafts','annotations','rubrics'])if(!x[k]||typeof x[k]!=='object'||Array.isArray(x[k]))return false;
  if(!Array.isArray(x.bookmarks)||!x.bookmarks.every(v=>typeof v==='string')||!Array.isArray(x.activity))return false;
  const record=v=>v&&typeof v==='object'&&!Array.isArray(v);
  if(!Object.values(x.answers).every(v=>record(v)&&Object.values(v).every(a=>record(a)&&[a.value,a.justification].every(t=>t===undefined||typeof t==='string'))))return false;
  if(!Object.values(x.drafts).every(v=>record(v)&&Object.values(v).every(t=>typeof t==='string')))return false;
  if(!Object.values(x.attempts).every(v=>record(v)&&record(v.results)&&Object.values(v.results).every(r=>record(r)&&['correct','incorrect','review','unanswered'].includes(r.status))))return false;
  if(!Object.values(x.rubrics).every(v=>Array.isArray(v)&&v.every(n=>Number.isInteger(n)&&n>=0&&n<10)))return false;
  if(x.vocabProgress!==undefined&&(!record(x.vocabProgress)||!Object.values(x.vocabProgress).every(p=>record(p)&&Number.isInteger(p.step)&&p.step>=-1&&p.step<=6&&Number.isFinite(p.due)&&p.due>=0&&Number.isFinite(p.lastReviewed)&&Number.isInteger(p.reviews)&&p.reviews>=0&&Number.isInteger(p.lapses)&&p.lapses>=0)))return false;
  if(x.vocabDefinitions!==undefined&&(!record(x.vocabDefinitions)||!Object.values(x.vocabDefinitions).every(v=>typeof v==='string')))return false;
  if(x.vocabDaily!==undefined&&(!record(x.vocabDaily)||!Object.entries(x.vocabDaily).every(([day,p])=>/^\d{4}-\d{2}-\d{2}$/.test(day)&&record(p)&&Array.isArray(p.newIds)&&p.newIds.every(id=>typeof id==='string')&&Number.isInteger(p.reviewed)&&p.reviewed>=0)))return false;
  if(!x.activity.every(d=>typeof d==='string'&&/^\d{4}-\d{2}-\d{2}$/.test(d)))return false;
  return Object.values(x.annotations).every(v=>Array.isArray(v)&&v.every(a=>record(a)&&typeof a.id==='string'&&typeof a.pid==='string'&&typeof a.text==='string'&&Number.isInteger(a.start)&&Number.isInteger(a.end)&&a.end>a.start&&a.start>=0&&[0,1,2,3].includes(a.level)&&(!a.note||typeof a.note==='string')));
}
export function dateKey(){return new Date().toLocaleDateString('en-CA');}
export function streak(activity){
  const dates=new Set(activity),d=new Date();let n=0;
  if(!dates.has(d.toLocaleDateString('en-CA')))d.setDate(d.getDate()-1);
  while(dates.has(d.toLocaleDateString('en-CA'))){n++;d.setDate(d.getDate()-1);}return n;
}
export function downloadJson(data,name){const url=URL.createObjectURL(new Blob([JSON.stringify(data,null,2)],{type:'application/json'}));const a=document.createElement('a');a.href=url;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);}
export function downloadText(text,name){const url=URL.createObjectURL(new Blob([text],{type:'text/plain;charset=utf-8'}));const a=document.createElement('a');a.href=url;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);}
