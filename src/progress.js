// 从两个题库各自的本机存储读取学习统计（只读，不修改题库数据）。
// 登录后题库使用 “存储键:user:账号ID” 保存，未登录时使用原存储键。
const read=key=>{try{return JSON.parse(localStorage.getItem(key)||'null');}catch{return null;}};
function stateFor(base,userId){
 const keys=[...(userId?[base+':user:'+userId]:[]),base];
 for(const k of keys){const x=read(k),s=x?.state||x;if(s&&typeof s==='object'&&s.attempts)return s;}
 return null;
}
export function bankProgress(base,userId){
 const s=stateFor(base,userId);
 return {practiced:s?Object.keys(s.attempts||{}).length:0,bookmarks:s?.bookmarks?.length||0,words:s?Object.keys(s.vocabProgress||{}).length:0,activity:s?.activity||[]};
}
export function overview(banks,userId){
 const per=Object.fromEntries(banks.map(b=>[b.id,bankProgress(b.storageKey,userId)]));
 const days=new Set(Object.values(per).flatMap(p=>p.activity));
 const key=d=>d.toLocaleDateString('en-CA');
 let streak=0;const d=new Date();if(!days.has(key(d)))d.setDate(d.getDate()-1);
 while(days.has(key(d))){streak++;d.setDate(d.getDate()-1);}
 const monday=new Date();monday.setDate(monday.getDate()-((monday.getDay()+6)%7));
 const thisWeek=[...days].filter(k=>k>=key(monday)).length;
 const sum=f=>Object.values(per).reduce((n,p)=>n+p[f],0);
 return {per,streak,thisWeek,practiced:sum('practiced'),bookmarks:sum('bookmarks'),words:sum('words')};
}
