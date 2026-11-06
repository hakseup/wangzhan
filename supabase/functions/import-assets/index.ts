// This function authenticates every request itself, before using its internal service credential.
import manifest from './manifest.json' with {type:'json'};
const source='https://raw.githubusercontent.com/hakseup/wangzhan/21fd374b1406e7f6bb8201562612d28d53d90856/public/';
Deno.serve(async req=>{
 const reply=(body:unknown,status=200)=>new Response(JSON.stringify(body),{status,headers:{'Content-Type':'application/json','Cache-Control':'no-store'}});
 try{
  if(req.method!=='POST')return reply({error:'Method not allowed'},405);
  const authorization=req.headers.get('Authorization');if(!authorization?.startsWith('Bearer '))return reply({error:'Login required'},401);
  const root=Deno.env.get('SUPABASE_URL')!,key=Deno.env.get('SUPABASE_ANON_KEY')!;
  const authHeaders={apikey:key,Authorization:authorization,'Content-Type':'application/json'};
  const user=await fetch(root+'/auth/v1/user',{headers:authHeaders});if(!user.ok)return reply({error:'Login required'},401);
  const session=await fetch(root+'/rest/v1/rpc/noix_session',{method:'POST',headers:authHeaders,body:'{}'});
  if(!session.ok||!(await session.json()).admin)return reply({error:'Administrator required'},403);
  const {index}=await req.json();
  if(index===undefined)return reply({total:manifest.length});
  if(!Number.isInteger(index)||index<0||index>=manifest.length)return reply({error:'Invalid index'},400);
  const item=manifest[index],remote=await fetch(source+item.path.split('/').map(encodeURIComponent).join('/'));
  if(!remote.ok)return reply({error:'Source unavailable'},502);
  const bytes=await remote.arrayBuffer();const hash=Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',bytes)),x=>x.toString(16).padStart(2,'0')).join('');
  if(hash!==item.sha256)return reply({error:'Source checksum mismatch'},502);
  const type=item.path.endsWith('.pdf')?'application/pdf':item.path.endsWith('.json')?'application/json':item.path.endsWith('.mp3')?'audio/mpeg':'audio/mp4';
  const uploaded=await fetch(root+'/storage/v1/object/noix-private/'+item.path.split('/').map(encodeURIComponent).join('/'),{method:'POST',headers:{Authorization:'Bearer '+Deno.env.get('SUPABASE_SERVICE_ROLE_KEY'),apikey:Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!,'Content-Type':type,'x-upsert':'true'},body:bytes});
  if(!uploaded.ok)return reply({error:'Storage upload failed'},502);
  return reply({ok:true,index,path:item.path,total:manifest.length});
 }catch{return reply({error:'Import failed; safe to retry'},503);}
});
