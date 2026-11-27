// 本地预览服务器：只用于在自己电脑上查看 web-dist，不连接 Supabase。
// 账号接口为内存模拟（任意邮箱 + 10 位以上密码即可“登录”），B2 私有题库直接读取 apps/b2/public。
// 正式部署请使用 Vercel（api/handler.mjs + Supabase），切勿把本脚本当作线上后端。
import http from 'node:http';
import {readFileSync,existsSync,statSync,createReadStream} from 'node:fs';
import {resolve,extname,normalize} from 'node:path';

const ROOT=process.cwd(),DIST=resolve(ROOT,'web-dist'),B2=resolve(ROOT,'apps/b2/public');
const PORT=Number(process.env.PORT||4173);
if(!existsSync(DIST))throw Error('请先运行 npm run build');
const types={'.html':'text/html; charset=utf-8','.js':'text/javascript','.css':'text/css','.json':'application/json; charset=utf-8','.png':'image/png','.jpg':'image/jpeg','.webp':'image/webp','.svg':'image/svg+xml','.ttf':'font/ttf','.woff2':'font/woff2','.m4a':'audio/mp4','.mp3':'audio/mpeg','.mp4':'video/mp4','.pdf':'application/pdf','.webmanifest':'application/manifest+json','.txt':'text/plain; charset=utf-8'};
const sessions=new Map(),progress=new Map(),study=new Map();
const read=path=>JSON.parse(readFileSync(path,'utf8'));
const cookie=req=>(req.headers.cookie||'').match(/noix-local=([\w-]+)/)?.[1];

function file(res,path,req){
 if(!existsSync(path)||!statSync(path).isFile())return false;
 const size=statSync(path).size,range=req.headers.range?.match(/bytes=(\d*)-(\d*)/);
 const head={'Content-Type':types[extname(path)]||'application/octet-stream','Accept-Ranges':'bytes','Cache-Control':'no-cache'};
 if(range){const start=Number(range[1]||0),end=range[2]?Number(range[2]):size-1;res.writeHead(206,{...head,'Content-Range':`bytes ${start}-${end}/${size}`,'Content-Length':end-start+1});createReadStream(path,{start,end}).pipe(res);}
 else{res.writeHead(200,{...head,'Content-Length':size});if(req.method==='HEAD')res.end();else createReadStream(path).pipe(res);}
 return true;
}
async function api(req,res,route,url){
 const send=(data,status=200,headers={})=>{res.writeHead(status,{'Content-Type':'application/json; charset=utf-8',...headers});res.end(JSON.stringify(data));};
 let body={};if(!['GET','HEAD'].includes(req.method)){let raw='';for await(const chunk of req)raw+=chunk;try{body=JSON.parse(raw||'{}');}catch{return send({error:'请求格式错误。'},400);}}
 const user=sessions.get(cookie(req));
 if(route==='catalog')return send(read(resolve(ROOT,'cloud/catalog.json')));
 if(route==='news')return send({notices:[],release:{version:'本地预览',notes:'',build:'local'}});
 if(route==='session')return send(user?{user,entitled:true,expires:253402300799000}:{user:null,entitled:false});
 if(route==='login'){if(!/^\S+@\S+\.\S+$/.test(body.email||'')||String(body.password||'').length<10)return send({error:'本地预览：请输入邮箱和至少 10 位密码。'},400);const id='local-'+Buffer.from(body.email).toString('hex').slice(0,16),sid=crypto.randomUUID();sessions.set(sid,{id,email:body.email.toLowerCase(),verified:true,admin:false});return send({ok:true},200,{'Set-Cookie':`noix-local=${sid}; Path=/; HttpOnly; SameSite=Lax`});}
 if(route==='register'||route==='forgot')return send({message:'本地预览不发送邮件，请直接登录。'});
 if(!user)return send({error:'请先登录并验证邮箱。'},401);
 if(route==='logout'){sessions.delete(cookie(req));return send({ok:true},200,{'Set-Cookie':'noix-local=; Path=/; Max-Age=0'});}
 if(route==='progress'){const cur=progress.get(user.id)||{revision:0,state:null};if(req.method==='GET')return send(cur);if(body.revision!==cur.revision)return send({error:'Progress conflict'},409);progress.set(user.id,{revision:cur.revision+1,state:body.state});return send({revision:cur.revision+1});}
 if(route==='study'){const cur=study.get(user.id)||{state:null,version:0,updatedAt:null};if(req.method==='GET')return send(cur);if(body.expectedVersion!==cur.version)return send({error:'conflict',current:cur},409);const next={state:body.state,version:cur.version+1,updatedAt:Date.now()};study.set(user.id,next);return send({version:next.version,updatedAt:next.updatedAt});}
 if(route==='content-revisions'){const part=url.searchParams.get('category');return send(read(resolve(ROOT,'cloud/'+(part?'revisions-'+part:'content-revisions')+'.json')));}
 return send({error:'本地预览未提供此接口：'+route},404);
}
http.createServer(async(req,res)=>{
 try{
  const url=new URL(req.url,'http://localhost'),path=decodeURIComponent(url.pathname);
  if(path.startsWith('/api/'))return await api(req,res,path.slice(5),url);
  if(path==='/content.json'||/^\/(audio|pdfs|dictionary)\//.test(path)){
   if(!sessions.get(cookie(req))){res.writeHead(401,{'Content-Type':'application/json'});return res.end('{"error":"请先登录"}');}
   const target=normalize(resolve(B2,'.'+path));if(target.startsWith(B2)&&file(res,target,req))return;
   res.writeHead(404);return res.end();
  }
  const target=normalize(resolve(DIST,'.'+path));if(!target.startsWith(DIST)){res.writeHead(403);return res.end();}
  if(file(res,target,req)||file(res,resolve(target,'index.html'),req))return;
  const app=['/b2/','/c1/'].find(p=>path.startsWith(p));if(file(res,resolve(DIST,app?app.slice(1):'','index.html'),req))return;
  res.writeHead(404);res.end();
 }catch(error){console.error(error);if(!res.headersSent)res.writeHead(500);res.end();}
}).listen(PORT,'0.0.0.0',()=>console.log(`本地预览：http://localhost:${PORT}/  （账号为本地模拟，不连接 Supabase）`));
