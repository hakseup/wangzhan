import {EMPTY_STATE,STORAGE_KEY,validImport} from './lib.js';
const copy=x=>structuredClone(x),equal=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
const object=x=>x&&typeof x==='object'&&!Array.isArray(x);
export function mergeStudy(base,local,remote){
 let conflicts=0;
 function merge(b,l,r){
  if(equal(l,r)||equal(r,b))return copy(l);if(equal(l,b))return copy(r);
  if(object(l)&&object(r)&&(b===undefined||object(b))){const out={};for(const k of new Set([...Object.keys(b||{}),...Object.keys(l),...Object.keys(r)])){const v=merge(b?.[k],l[k],r[k]);if(v!==undefined)out[k]=v;}return out;}
  if(Array.isArray(l)&&Array.isArray(r)&&Array.isArray(b)){
   if([...b,...l,...r].every(x=>typeof x==='string'||typeof x==='number')){const removed=new Set(b.filter(x=>!l.includes(x)||!r.includes(x)));return [...new Set([...l,...r])].filter(x=>!removed.has(x));}
   if([...b,...l,...r].every(x=>object(x)&&typeof x.id==='string')){const map=a=>Object.fromEntries(a.map(x=>[x.id,x]));return Object.values(merge(map(b),map(l),map(r)));}
  }
  conflicts++;return copy(l);
 }
 return {state:merge(base,local,remote),conflicts};
}
const isEmpty=s=>equal(s,EMPTY_STATE);
export class StudyStore{
 constructor({storage,fetcher=fetch,enabled=false,delay=900}={}){
  this.storage=storage;this.fetcher=(...args)=>fetcher.call(globalThis,...args);this.enabled=enabled;this.delay=delay;this.listeners=new Set();this.key=STORAGE_KEY;this.epoch=0;this.version=0;this.base=copy(EMPTY_STATE);this.ready=false;
  this.snapshot={study:this.readStudy(STORAGE_KEY)||copy(EMPTY_STATE),storageKey:STORAGE_KEY,storageError:false,user:null,status:'local',error:'',savedAt:null,conflict:null,guestAvailable:false,enabled};
 }
 subscribe=fn=>{this.listeners.add(fn);return()=>this.listeners.delete(fn);};
 getSnapshot=()=>this.snapshot;
 emit=patch=>{this.snapshot={...this.snapshot,...patch};for(const fn of this.listeners)fn();};
 read(key){try{return JSON.parse(this.storage.getItem(key)||'null');}catch{return null;}}
 readStudy(key){const x=this.read(key),s=x?.state||x;return s&&validImport({...EMPTY_STATE,...s})?{...copy(EMPTY_STATE),...s,fontSize:Math.max(14,Math.min(26,Number(s.fontSize)||18))}:null;}
 persist(){try{this.storage.setItem(this.key,JSON.stringify(this.key===STORAGE_KEY?this.snapshot.study:{state:this.snapshot.study,base:this.base,version:this.version,conflict:this.snapshot.conflict}));if(this.snapshot.storageError)this.emit({storageError:false});}catch{this.emit({storageError:true});}}
 updateStudy=fn=>{const study=typeof fn==='function'?fn(this.snapshot.study):fn;this.emit({study});this.persist();this.schedule();};
 async request(path,{method='GET',body,account}={}){
  const r=await this.fetcher(path,{method,credentials:'same-origin',cache:'no-store',headers:{...(body?{'content-type':'application/json'}:{}),...(account?{'x-study-account':account}:{})},...(body?{body:JSON.stringify(body)}:{})});
  const data=await r.json().catch(()=>({}));if(!r.ok){const error=new Error(data.message||'暂时无法连接云端，请稍后重试。');error.status=r.status;error.data=data;throw error;}return data;
 }
 async init(){if(!this.enabled)return;try{const session=await this.request('/api/auth/get-session');if(session?.user)await this.activate(session.user);}catch{this.emit({status:'local',error:'暂时无法检查登录状态，本机记录仍会保存。'});}}
 async authenticate(mode,email,password){
  this.emit({error:'',status:'authenticating'});
  try{const data=await this.request('/api/auth/'+(mode==='register'?'sign-up/email':'sign-in/email'),{method:'POST',body:{email:email.trim().toLowerCase(),password,...(mode==='register'?{name:email.split('@')[0]}:{})}});await this.activate(data.user);}
  catch(error){this.emit({status:this.snapshot.user?'error':'local',error:({INVALID_EMAIL_OR_PASSWORD:'邮箱或密码不正确。',USER_ALREADY_EXISTS_USE_ANOTHER_EMAIL:'这个邮箱已注册，请直接登录。',PASSWORD_TOO_SHORT:'密码至少需要10个字符。',TOO_MANY_REQUESTS:'操作过于频繁，请稍后重试。'})[error.data?.code]||(error.status?'登录未完成，请检查邮箱和密码后重试。':'暂时无法连接，请检查网络后重试。')});throw error;}
 }
 async activate(user){
  if(!user?.id)throw Error('登录未完成，请重试。');const epoch=++this.epoch;this.expired=false;clearTimeout(this.timer);this.ready=false;this.emit({user,status:'loading',error:'',conflict:null});
  try{
   const remote=await this.request('/api/study',{account:user.id});if(epoch!==this.epoch)return;if(remote.state&&!validImport(remote.state))throw Error('INVALID_BACKUP');
   const key=STORAGE_KEY+':user:'+user.id,cached=this.read(key),guest=this.readStudy(STORAGE_KEY)||copy(EMPTY_STATE);this.key=key;this.base=remote.state||copy(EMPTY_STATE);this.version=remote.version;
   let study=this.base,conflict=null;
   if(cached?.conflict?.local&&validImport(cached.conflict.local)){study=cached.conflict.local;conflict={local:study,remote:this.base};}
   else if(cached?.state&&validImport(cached.state)&&cached.base&&validImport(cached.base)){const merged=mergeStudy(cached.base,cached.state,this.base);study=merged.state;if(merged.conflicts)conflict={local:cached.state,remote:this.base};}
   else if(!remote.state){study=guest;this.claimGuest=true;}
   this.ready=true;this.emit({study,storageKey:key,status:conflict?'conflict':'saved',conflict,savedAt:remote.updatedAt,guestAvailable:!!remote.state&&!isEmpty(guest)});this.persist();this.schedule();
  }catch(error){if(epoch===this.epoch)this.emit({status:'error',error:'云端记录暂未载入，本机记录已保留。请重试同步。'});}
 }
 schedule(){
  clearTimeout(this.timer);if(!this.enabled||!this.ready||!this.snapshot.user||this.snapshot.conflict)return;
  if(equal(this.snapshot.study,this.base)&&this.version>0)return;
  this.emit({status:'pending',error:''});this.timer=setTimeout(()=>this.flush(),this.delay);
 }
 async flush(){
  if(this.inFlight){this.pending=true;return;}if(!this.ready||!this.snapshot.user||this.snapshot.conflict)return;
  const epoch=this.epoch,user=this.snapshot.user,state=copy(this.snapshot.study);if(equal(state,this.base)&&this.version>0)return;
  this.inFlight=true;this.pending=false;this.emit({status:'saving',error:''});
  try{
   const saved=await this.request('/api/study',{method:'PUT',account:user.id,body:{state,expectedVersion:this.version}});if(epoch!==this.epoch)return;
   this.base=state;this.version=saved.version;
   if(this.claimGuest){this.storage.removeItem(STORAGE_KEY);this.claimGuest=false;this.emit({guestAvailable:false});}
   this.emit({status:equal(this.snapshot.study,state)?'saved':'pending',savedAt:saved.updatedAt});this.persist();
  }catch(error){
   if(epoch!==this.epoch)return;
   if(error.status===409&&error.data.current){const r=error.data.current;if(r.state&&!validImport(r.state)){this.emit({status:'error',error:'云端记录格式异常，本机记录已保留。'});return;}const remote=r.state||copy(EMPTY_STATE),merged=mergeStudy(this.base,this.snapshot.study,remote);this.base=remote;this.version=r.version;
    this.emit({study:merged.state,conflict:merged.conflicts?{local:this.snapshot.study,remote}:null,status:merged.conflicts?'conflict':'pending',error:merged.conflicts?'其他设备也修改了相同记录，请选择保留的版本。':''});this.persist();if(!merged.conflicts)this.pending=true;
   }else{if(error.status===401){this.expired=true;this.ready=false;}this.emit({status:'error',error:error.status===401?'登录已过期，请重新登录。本机记录已保留。':'云端备份暂未完成，本机记录已保留，联网后会重试。'});}
  }finally{this.inFlight=false;if(epoch===this.epoch&&(this.pending||this.snapshot.status==='pending'))this.schedule();}
 }
 resolveConflict=choice=>{const c=this.snapshot.conflict;if(!c)return;if(choice==='remote')this.claimGuest=false;this.emit({study:copy(choice==='local'?c.local:c.remote),conflict:null,error:'',status:'saved'});this.persist();this.schedule();};
 importGuest=()=>{const guest=this.readStudy(STORAGE_KEY);if(!guest)return;const merged=mergeStudy(EMPTY_STATE,guest,this.snapshot.study);this.claimGuest=true;this.emit({study:merged.state,conflict:merged.conflicts?{local:merged.state,remote:this.snapshot.study}:null,status:merged.conflicts?'conflict':'pending',error:merged.conflicts?'本机与云端有不同记录，请选择保留的版本。':''});this.persist();this.schedule();};
 retry=()=>this.ready?this.flush():this.snapshot.user?this.activate(this.snapshot.user):this.init();
 async signOut({clearDevice=false}={}){
  // Flush outstanding edits before a normal logout; never silently discard them.
  if(!clearDevice&&this.ready&&!this.snapshot.conflict){await this.flush();if(this.snapshot.status==='error'||this.snapshot.status==='pending'||this.inFlight)throw Error('还有记录等待备份，请先完成同步再退出。');}
  await this.request('/api/auth/sign-out',{method:'POST',body:{}});++this.epoch;clearTimeout(this.timer);this.ready=false;if(clearDevice)this.storage.removeItem(this.key);
  this.key=STORAGE_KEY;this.emit({study:this.readStudy(STORAGE_KEY)||copy(EMPTY_STATE),storageKey:STORAGE_KEY,user:null,status:'local',savedAt:null,error:'',conflict:null,guestAvailable:false});this.persist();
 }
 dispose(){clearTimeout(this.timer);++this.epoch;this.ready=false;}
}
