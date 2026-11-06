import {readFileSync} from 'node:fs';
import {gateway,fail,identity,setSession,sameOrigin,privatePath} from '../cloud/supabase.mjs';
const catalog=JSON.parse(readFileSync(new URL('../cloud/catalog.json',import.meta.url)));
const build=JSON.parse(readFileSync(new URL('../cloud/build.json',import.meta.url)));
const defaultRelease={version:'1.0.0',notes:'邮箱账号、兑换码与云端学习记录。',build:build.id};
export default async function handler(req,res){
 res.setHeader('Cache-Control','private, no-store');res.setHeader('X-Content-Type-Options','nosniff');
 const send=(data,status=200)=>{res.statusCode=status;res.setHeader('Content-Type','application/json; charset=utf-8');res.end(JSON.stringify(data));};
 try{
  const url=new URL(req.url,'https://'+req.headers.host);const path=url.searchParams.get('route')||url.pathname.replace(/^\/api\//,'');const method=req.method;
  if(!['GET','POST','PUT','HEAD'].includes(method))fail('不支持此操作。',405);
  if(!['GET','HEAD'].includes(method)){sameOrigin(req);if(!String(req.headers['content-type']).startsWith('application/json'))fail('请求格式错误。',415);}
  let body=req.body||{};if(typeof body==='string'){if(Buffer.byteLength(body)>4100000)fail('内容过大。',413);body=JSON.parse(body);}
  const sb=gateway();const rpc=(name,args={},token)=>sb('/rest/v1/rpc/'+name,{method:'POST',body:args,token});
  const news=async token=>{const [notices,settings]=await Promise.all([sb('/rest/v1/noix_notices?select=*&order=published_at.desc&limit=50',{token}),sb('/rest/v1/noix_settings?select=value&key=eq.release',{token})]);return {notices:notices.map(n=>({...n,published:Date.parse(n.published_at)})),release:{...defaultRelease,...settings[0]?.value,build:build.id}};};
  if(path==='catalog'&&method==='GET')return send(catalog);
  if(path==='news'&&method==='GET')return send(await news());
  if(['register','forgot','login'].includes(path)&&method==='POST'){
   if(typeof body.email!=='string'||!/^\S+@\S+\.\S+$/.test(body.email)||body.email.length>254)fail('请输入有效邮箱。');
   const email=body.email.trim().toLowerCase(),redirect='https://'+req.headers.host+'/';
   if(path!=='forgot'&&(typeof body.password!=='string'||body.password.length<10||body.password.length>256))fail('密码需为10至256个字符。');
   if(path==='register'){await sb('/auth/v1/signup?redirect_to='+encodeURIComponent(redirect),{method:'POST',body:{email,password:body.password}});return send({message:'请前往邮箱完成验证，然后返回应用登录。'});}
   if(path==='forgot'){await sb('/auth/v1/recover?redirect_to='+encodeURIComponent(redirect),{method:'POST',body:{email}});return send({message:'如果此邮箱已注册，你将收到重设密码邮件。'});}
   const session=await sb('/auth/v1/token?grant_type=password',{method:'POST',body:{email,password:body.password}});if(!session.user?.email_confirmed_at)fail('请先验证邮箱。',403);setSession(res,session);return send({ok:true});
  }
  if(path==='verify'&&method==='POST'){
   if(typeof body.access_token!=='string'||typeof body.refresh_token!=='string')fail('验证链接无效。');
   const user=await sb('/auth/v1/user',{token:body.access_token});if(!user.email_confirmed_at)fail('邮箱尚未验证。',403);
   setSession(res,body);return send({message:'邮箱验证成功。'});
  }
  const auth=await identity(req,res,sb);
  if(path==='session'&&method==='GET'){
   if(!auth)return send({user:null,entitled:false});
   const access=await rpc('noix_session',{},auth.token);return send({user:{id:auth.user.id,email:auth.user.email,verified:!!auth.user.email_confirmed_at,admin:access.admin},entitled:access.entitled,expires:access.entitled?(access.expires_at?Date.parse(access.expires_at):253402300799000):null});
  }
  if(!auth?.user.email_confirmed_at)fail('请先登录并验证邮箱。',401);
  const token=auth.token;
  if(path==='logout'&&method==='POST'){await sb('/auth/v1/logout?scope=local',{method:'POST',token});setSession(res,null);return send({ok:true});}
  if(path==='reset'&&method==='POST'){if(typeof body.password!=='string'||body.password.length<10||body.password.length>256)fail('密码需为10至256个字符。');await sb('/auth/v1/user',{method:'PUT',token,body:{password:body.password}});return send({message:'密码已更新。'});}
  if(path==='redeem'&&method==='POST'){if(typeof body.code!=='string'||body.code.length>100)fail('兑换码无效。');await rpc('noix_redeem',{raw_code:body.code},token);return send({ok:true});}
  if(path==='admin/dashboard'&&method==='GET')return send({...await rpc('noix_dashboard',{},token),release:(await news(token)).release});
  if(path==='admin/codes'&&method==='POST')return send({codes:await rpc('noix_generate_codes',{quantity:body.count,valid_days:body.days},token)});
  if(path==='admin/import'&&method==='POST'){
   if(!(await rpc('noix_session',{},token)).admin)fail('需要管理员权限。',403);
   return send(await sb('/functions/v1/import-assets',{method:'POST',token,body:body.index===undefined?{}:{index:body.index},timeoutMs:55000}));
  }
  if(path==='admin/notices'&&method==='POST'){await sb('/rest/v1/noix_notices',{method:'POST',token,body:{title:body.title,body:body.body}});return send({ok:true});}
  if(path==='admin/settings'&&method==='PUT'){const r=body.release;if(!r||typeof r.version!=='string'||r.version.length>40||typeof r.notes!=='string'||r.notes.length>10000)fail('版本说明格式无效。');await sb('/rest/v1/noix_settings?on_conflict=key',{method:'POST',token,headers:{Prefer:'resolution=merge-duplicates'},body:{key:'release',value:{version:r.version,notes:r.notes}}});return send({ok:true});}
  if(path==='progress'&&method==='GET'){const rows=await sb('/rest/v1/noix_progress?select=revision,state&user_id=eq.'+encodeURIComponent(auth.user.id),{token});return send(rows[0]||{revision:0,state:null});}
  if(path==='progress'&&method==='PUT'){if(!Number.isSafeInteger(body.revision)||body.revision<0)fail('进度版本无效。');return send({revision:await rpc('noix_save_progress',{expected_revision:body.revision,new_state:body.state},token)});}
  const access=await rpc('noix_session',{},token);if(!access.entitled)fail('请输入有效兑换码开通题库。',403);
  const asset=privatePath('/'+path);
  if(asset&&['GET','HEAD'].includes(method)){
   const signed=await sb('/storage/v1/object/sign/noix-private/'+asset.split('/').map(encodeURIComponent).join('/'),{method:'POST',token,body:{expiresIn:120}});
   res.statusCode=302;res.setHeader('Location',process.env.SUPABASE_URL+'/storage/v1'+signed.signedURL);return res.end();
  }
  fail('未找到此内容。',404);
 }catch(error){send({error:error.status?error.message:'服务暂时无法连接，请稍后重试。'},error.status||503);}
}
