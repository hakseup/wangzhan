// No service-role credentials: every data operation runs with the signed-in user's JWT.
export const fail=(message,status=400)=>{throw Object.assign(Error(message),{status});};
export function gateway(env=process.env,fetcher=fetch){
 const root=env.SUPABASE_URL,key=env.SUPABASE_PUBLISHABLE_KEY;
 if(!root||!key)fail('账号服务尚未配置。',503);
 return async(path,{method='GET',body,token,headers={},timeoutMs=20000}={})=>{
  const response=await fetcher(root+path,{method,headers:{apikey:key,...(token?{Authorization:'Bearer '+token}:{}),...(body!==undefined?{'Content-Type':'application/json'}:{}),...headers},body:body!==undefined?JSON.stringify(body):undefined,signal:AbortSignal.timeout(timeoutMs)});
  const data=await response.json().catch(()=>null);
  if(!response.ok){const status=data?.code==='40001'?409:response.status;const messages={invalid_credentials:'邮箱或密码不正确。',email_not_confirmed:'请先验证邮箱。',email_address_not_authorized:'发信服务尚未开放，请联系管理员配置正式邮件服务。',over_email_send_rate_limit:'邮件发送频率已达上限，请稍后再试。'};fail(messages[data?.error_code||data?.code]||(status===409?'其他设备已更新学习记录。':status===401?'请重新登录。':'操作失败，请检查输入或稍后重试。'),status);}
  return data;
 };
}
export function cookies(req){return Object.fromEntries((req.headers.cookie||'').split(';').map(v=>{const at=v.indexOf('=');return at<0?[]:[v.slice(0,at).trim(),decodeURIComponent(v.slice(at+1))];}).filter(v=>v.length===2));}
export function setSession(res,session){
 const values=[['noix-access',session?.access_token],['noix-refresh',session?.refresh_token]];
 res.setHeader('Set-Cookie',values.map(([name,value])=>`${name}=${encodeURIComponent(value||'')}; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=${value?2592000:0}`));
}
export async function identity(req,res,sb){
 const c=cookies(req);if(!c['noix-access']&&!c['noix-refresh'])return null;
 let token=c['noix-access'];
 try {const user=await sb('/auth/v1/user',{token});return {user,token};}
 catch(e){if(e.status!==401&&e.status!==403)throw e;}
 if(!c['noix-refresh'])return null;
 try {const session=await sb('/auth/v1/token?grant_type=refresh_token',{method:'POST',body:{refresh_token:c['noix-refresh']}});setSession(res,session);return {user:session.user,token:session.access_token};}
 catch(e){if(e.status>=500)throw e;setSession(res,null);return null;}
}
export function sameOrigin(req){
 const origin=req.headers.origin;const host=req.headers.host;
 if(!origin||new URL(origin).protocol!=='https:'||new URL(origin).host!==host)fail('请求来源无效。',403);
 if(req.headers['sec-fetch-site']&& !['same-origin','none'].includes(req.headers['sec-fetch-site']))fail('请求来源无效。',403);
}
export function privatePath(path){
 if(path==='/content.json')return 'content.json';
 if(/^\/(audio|pdfs|dictionary)\/[\p{L}\p{N}_ .()【】《》：？!’,éèàçêôûîïäöü-]+\.(pdf|mp3|m4a|mp4|json)$/u.test(path)&&!path.includes('..'))return path.slice(1);
 return null;
}
