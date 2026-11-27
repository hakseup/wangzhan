// Only the verified administrator invokes this routine; all API calls also check that role server-side.
export async function initializeResources(call,onProgress,stopped=()=>false){
 const status=await call('admin/import',{});
 const pending=[...status.pending].sort((a,b)=>a-b);
 let done=status.total-pending.length,bankReady=status.bankReady;
 const progress=phase=>{if(!stopped())onProgress({phase,done,total:status.total,bankReady});};
 progress(pending.length?'importing':'ready');
 for(const index of pending){
  if(stopped())return;
  await call('admin/import',{index});done++;
  if(index===0)bankReady=true;
  progress(done===status.total?'ready':'importing');
 }
}
