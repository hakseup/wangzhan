import {EMPTY_STATE} from './lib.js';
const normalize=state=>({...structuredClone(EMPTY_STATE),...state,version:1});
// Postgres JSONB may reorder keys; ordering must not create false progress conflicts.
const json=value=>JSON.stringify(value,(_key,item)=>item&&typeof item==='object'&&!Array.isArray(item)?Object.fromEntries(Object.keys(item).sort().map(key=>[key,item[key]])):item);
export function createProgressSync({call,initial,readPending,writePending,removePending,onState,onStatus,onConflict}){
 let state=normalize(initial),initialJSON=json(state),saved=null,revision=0,ready=false,paused=false,stopped=false,work=null,conflict=null;
 const cache=()=>{try{writePending(state);}catch{/* A full local cache must not prevent the cloud write. */}};
 const report=message=>{if(!stopped)onStatus(message);};
 const adopt=remote=>{state=normalize(remote.state);saved=json(state);revision=remote.revision;ready=true;try{removePending();}catch{}if(!stopped)onState(state);};
 const errorStatus=error=>error.status===401?'登录已失效，请重新登录后同步。':error.status===403?'当前账号无法访问云端存档，请重新登录后重试。':'云端同步暂未完成，将自动重试；此设备保留待同步记录。';
 const readConflict=async()=>{const remote=await call('progress');if(remote.state&&json(normalize(remote.state))===json(state)){adopt(remote);report('云端已同步');return false;}conflict=remote;paused=true;report('其他设备有新的学习记录，请选择继续使用的版本。');if(!stopped)onConflict(conflict);return true;};
 async function upload(){
  while(!stopped&&ready&&!paused&&json(state)!==saved){
   const snapshot=json(state);report('正在同步…');
   try{const result=await call('progress',{revision,state:JSON.parse(snapshot)},'PUT');revision=result.revision;saved=snapshot;if(json(state)===snapshot){try{removePending();}catch{}}else cache();}
   catch(error){cache();if(error.status===409){if(await readConflict())throw error;}else{report(errorStatus(error));throw error;}}
  }
  if(!paused&&!stopped)report('云端已同步');
 }
 async function cycle(){
  if(stopped)return;
  if(paused)throw Object.assign(Error('请先处理其他设备的进度。'),{status:409});
  try{
   if(!ready){
    const remote=await call('progress');if(stopped)return;
    const pending=readPending(),changed=json(state)!==initialJSON;
    if(pending&&!changed)state=normalize(pending);
    if(remote.state&&(pending||changed)&&json(normalize(remote.state))!==json(state)){cache();conflict=remote;paused=true;report('其他设备有新的学习记录，请选择继续使用的版本。');onConflict(remote);return;}
    revision=remote.revision;ready=true;
    if(remote.state&&!pending&&!changed)adopt(remote);
    else {saved=remote.state?json(normalize(remote.state)):null;if(!stopped)onState(state);}
   }else if(json(state)===saved){
    const remote=await call('progress');if(stopped)return;
    if(remote.revision>revision){if(json(state)===saved)adopt(remote);else{cache();conflict=remote;paused=true;onConflict(remote);return;}}
   }
   await upload();
  }catch(error){if(!paused)report(errorStatus(error));throw error;}
 }
 async function sync(){
  if(work){await work;if(!stopped&&ready&&!paused&&json(state)!==saved)return sync();return;}
  work=cycle();try{await work;}finally{work=null;}
 }
 return {
  setLocal(next){const normalized=normalize(next);if(json(normalized)===json(state))return false;state=normalized;if(!ready||json(state)!==saved){cache();report('等待同步…');}return true;},
  sync,
  async flush(){await sync();if(paused||!ready||json(state)!==saved)throw Error('学习记录尚未同步，请先处理同步提示。');},
  async resolve(useRemote){if(!conflict)return;revision=conflict.revision;ready=true;paused=false;if(useRemote)adopt(conflict);else saved=null;conflict=null;onConflict(null);await sync();},
  stop(){stopped=true;},
 };
}
