import http from 'node:http';
import {DatabaseSync} from 'node:sqlite';
import {randomBytes,createHash,scrypt,timingSafeEqual} from 'node:crypto';
import {promisify} from 'node:util';
import {readFileSync,existsSync,mkdirSync,createReadStream,statSync} from 'node:fs';
import {resolve,dirname,extname} from 'node:path';
const derive=promisify(scrypt),hash=s=>createHash('sha256').update(s).digest('hex'),token=()=>randomBytes(32).toString('hex');
export function createApp(options={}){
 const env={...process.env,...options.env},root=resolve(options.root||'.'),dbPath=options.dbPath||env.DB_PATH||'data/runtime/app.sqlite';mkdirSync(dirname(resolve(dbPath)),{recursive:true});
 const db=new DatabaseSync(dbPath);db.exec(`PRAGMA journal_mode=WAL; PRAGMA foreign_keys=ON;
 CREATE TABLE IF NOT EXISTS users(id TEXT PRIMARY KEY,email TEXT UNIQUE NOT NULL,password TEXT NOT NULL,verified INTEGER DEFAULT 0,created INTEGER);
 CREATE TABLE IF NOT EXISTS sessions(hash TEXT PRIMARY KEY,user TEXT REFERENCES users(id),expires INTEGER);
 CREATE TABLE IF NOT EXISTS tokens(hash TEXT PRIMARY KEY,user TEXT REFERENCES users(id),purpose TEXT,expires INTEGER);
 CREATE TABLE IF NOT EXISTS access(user TEXT PRIMARY KEY REFERENCES users(id),expires INTEGER NOT NULL);
 CREATE TABLE IF NOT EXISTS codes(hash TEXT PRIMARY KEY,label TEXT,days INTEGER,used_by TEXT,used_at INTEGER);
 CREATE TABLE IF NOT EXISTS progress(user TEXT PRIMARY KEY REFERENCES users(id),revision INTEGER,state TEXT,updated INTEGER);
 CREATE TABLE IF NOT EXISTS notices(id TEXT PRIMARY KEY,title TEXT,body TEXT,published INTEGER);
 CREATE TABLE IF NOT EXISTS settings(key TEXT PRIMARY KEY,value TEXT);
 `);
 const get=(sql,...args)=>db.prepare(sql).get(...args),run=(sql,...args)=>db.prepare(sql).run(...args),all=(sql,...args)=>db.prepare(sql).all(...args);
 const setting=(key,fallback)=>{const v=get('SELECT value FROM settings WHERE key=?',key);return v?JSON.parse(v.value):fallback;};
 const bankPath=existsSync(resolve(root,'public/content.json'))?resolve(root,'public/content.json'):resolve(root,'dist/content.json');
 const bank=JSON.parse(readFileSync(bankPath)),catalog={level:bank.level,exercises:bank.exercises.map(e=>({id:e.id,category:e.category,title:e.title,titleZh:e.titleZh,topic:e.topic,subtopic:e.subtopic,examSessionLabel:e.examSessionLabel,source:e.source,paragraphs:[],questions:[],studyModels:[],audio:null})),lexicon:{}};
 const origin=env.PUBLIC_URL||'http://localhost:3000',production=env.NODE_ENV==='production';if(production&&!origin.startsWith('https://'))throw Error('Production requires HTTPS PUBLIC_URL');
 const limits=new Map();const cleanup=setInterval(()=>{for(const [key,v] of limits)if(v.until<Date.now())limits.delete(key);run('DELETE FROM sessions WHERE expires<?',Date.now());run('DELETE FROM tokens WHERE expires<?',Date.now());},900000);cleanup.unref();function limit(key,max=12){const now=Date.now(),v=limits.get(key)||{n:0,until:now+900000};if(v.until<now){v.n=0;v.until=now+900000;}v.n++;limits.set(key,v);if(v.n>max)throw Object.assign(Error('操作太频繁，请稍后再试。'),{status:429});}
 const fail=(message,status=400)=>{throw Object.assign(Error(message),{status});};
 async function mail(user,purpose){const raw=token();run('INSERT INTO tokens VALUES(?,?,?,?)',hash(raw),user.id,purpose,Date.now()+3600000);const url=origin+'/?'+(purpose==='verify'?'verify':'reset')+'='+raw;
  if(options.deliver)return options.deliver({email:user.email,purpose,url});
  if(!env.RESEND_API_KEY||!env.MAIL_FROM)fail('邮件服务尚未配置，暂不能发送验证邮件。',503);
  const result=await fetch('https://api.resend.com/emails',{method:'POST',headers:{Authorization:'Bearer '+env.RESEND_API_KEY,'Content-Type':'application/json'},body:JSON.stringify({from:env.MAIL_FROM,to:user.email,subject:'胡桃法语 · '+(purpose==='verify'?'验证邮箱':'重设密码'),text:'请在一小时内打开链接：'+url})});if(!result.ok)fail('邮件暂时发送失败，请稍后重新发送。',503);
 }
 async function password(value,salt=randomBytes(16).toString('hex')){return salt+':'+Buffer.from(await derive(value,salt,64)).toString('hex');}
 async function check(value,stored){const [salt,digest]=stored.split(':');const actual=Buffer.from(await derive(value,salt,64));return timingSafeEqual(actual,Buffer.from(digest,'hex'));}
 const sessionUser=req=>{const raw=(req.headers.cookie||'').split(';').map(s=>s.trim()).find(s=>s.startsWith('noix_session='))?.slice(13);return raw?get('SELECT u.* FROM sessions s JOIN users u ON s.user=u.id WHERE s.hash=? AND s.expires>?',hash(raw),Date.now()):null;};
 const access=user=>!!user&&(user.email.toLowerCase()===env.ADMIN_EMAIL?.toLowerCase()&&!!user.verified||!!get('SELECT user FROM access WHERE user=? AND expires>?',user.id,Date.now()));
 const admin=user=>!!user?.verified&&user.email.toLowerCase()===env.ADMIN_EMAIL?.toLowerCase();
 function transaction(fn){db.exec('BEGIN IMMEDIATE');try{const result=fn();db.exec('COMMIT');return result;}catch(e){db.exec('ROLLBACK');throw e;}}
 function grant(user,days){const old=get('SELECT expires FROM access WHERE user=?',user);const expires=days===0||old?.expires===253402300799000?253402300799000:Math.min(253402300799000,Math.max(Date.now(),old?.expires||0)+days*86400000);run('INSERT INTO access VALUES(?,?) ON CONFLICT(user) DO UPDATE SET expires=excluded.expires',user,expires);}
 const buildFile=resolve(root,'dist/build.json');const build=existsSync(buildFile)?JSON.parse(readFileSync(buildFile)).id:(env.APP_BUILD||'development');
 const version=()=>({...setting('release',{version:'1.0.0',notes:'账号与云端学习版本'}),build});
 async function handle(req,res){
  res.setHeader('X-Content-Type-Options','nosniff');res.setHeader('Referrer-Policy','same-origin');res.setHeader('X-Frame-Options','DENY');res.setHeader('Cache-Control','no-store');
  const send=(value,status=200)=>{res.writeHead(status,{'Content-Type':'application/json; charset=utf-8'});res.end(JSON.stringify(value));};
  try{
   const ip=env.TRUST_PROXY==='1'?String(req.headers['x-forwarded-for']||req.socket.remoteAddress).split(',').at(-1).trim():req.socket.remoteAddress;const url=new URL(req.url,'http://local'),path=decodeURIComponent(url.pathname),method=req.method,user=sessionUser(req);if(path.includes('\\')||path.includes('\0')||path.split('/').some(v=>v==='..'||v==='.'))fail('路径无效。',400);let bytes=Buffer.alloc(0),body={};
   if(!['GET','HEAD'].includes(method)){
    if(req.headers.origin!==origin)fail('请求来源不匹配。',403);
    for await(const chunk of req){bytes=Buffer.concat([bytes,chunk]);if(bytes.length>8*1024*1024)fail('数据过大。',413);}
    {try{body=JSON.parse(bytes.toString()||'{}');}catch{fail('请求格式无效。');}}
   }
   if(path==='/api/catalog'&&method==='GET')return send(catalog);
   if(path==='/api/session'&&method==='GET')return send({user:user?{id:user.id,email:user.email,verified:!!user.verified,admin:admin(user)}:null,entitled:access(user),expires:user?get('SELECT expires FROM access WHERE user=?',user.id)?.expires:null});
   if(path==='/api/news'&&method==='GET')return send({notices:all('SELECT * FROM notices ORDER BY published DESC LIMIT 30'),release:version()});
   if(path==='/api/register'&&method==='POST'){
    limit('register:'+ip,6);const email=String(body.email||'').trim().toLowerCase(),pw=body.password;if(!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)||email.length>254||typeof pw!=='string'||pw.length<10||pw.length>256)fail('请输入有效邮箱及至少10位密码。');
    let u=get('SELECT * FROM users WHERE email=?',email);if(!u){u={id:token(),email};run('INSERT INTO users VALUES(?,?,?,?,?)',u.id,email,await password(pw),0,Date.now());}if(!u.verified)await mail(u,'verify');return send({message:'如果该邮箱可注册，验证邮件已发送，请检查收件箱。'});
   }
   if(path==='/api/login'&&method==='POST'){
    limit('login:'+ip);const email=String(body.email||'').trim().toLowerCase();limit('email:'+email,10);const u=get('SELECT * FROM users WHERE email=?',email);if(!u||typeof body.password!=='string'||body.password.length>256||!await check(body.password,u.password))fail('邮箱或密码不正确。',401);if(!u.verified)fail('请先验证邮箱，可在注册页重新发送验证邮件。',403);const raw=token();run('INSERT INTO sessions VALUES(?,?,?)',hash(raw),u.id,Date.now()+30*86400000);res.setHeader('Set-Cookie',`noix_session=${raw}; HttpOnly; SameSite=Lax; Path=/; Max-Age=2592000${production?'; Secure':''}`);return send({ok:true});
   }
   if(path==='/api/verify'&&method==='POST'){const t=get('SELECT * FROM tokens WHERE hash=? AND purpose=? AND expires>?',hash(String(body.token)), 'verify',Date.now());if(!t)fail('验证链接无效或已过期。');transaction(()=>{run('UPDATE users SET verified=1 WHERE id=?',t.user);run('DELETE FROM tokens WHERE user=? AND purpose=?',t.user,'verify');});return send({message:'邮箱验证成功，请登录。'});}
   if(path==='/api/forgot'&&method==='POST'){limit('forgot:'+ip,5);const u=get('SELECT * FROM users WHERE email=?',String(body.email||'').trim().toLowerCase());if(u)await mail(u,'reset');return send({message:'若邮箱已注册，重设链接已发送。'});}
   if(path==='/api/reset'&&method==='POST'){if(typeof body.password!=='string'||body.password.length<10||body.password.length>256)fail('密码须为10至256位。');const t=get('SELECT * FROM tokens WHERE hash=? AND purpose=? AND expires>?',hash(String(body.token)),'reset',Date.now());if(!t)fail('重设链接无效或已过期。');const pw=await password(body.password);transaction(()=>{run('UPDATE users SET password=?,verified=1 WHERE id=?',pw,t.user);run('DELETE FROM tokens WHERE user=?',t.user);run('DELETE FROM sessions WHERE user=?',t.user);});return send({message:'密码已重设，请重新登录。'});}
   if(path==='/api/logout'&&method==='POST'){const raw=(req.headers.cookie||'').match(/(?:^|;\s*)noix_session=([^;]+)/)?.[1];if(raw)run('DELETE FROM sessions WHERE hash=?',hash(raw));res.setHeader('Set-Cookie','noix_session=; HttpOnly; SameSite=Lax; Path=/; Max-Age=0');return send({ok:true});}
   if(path==='/api/redeem'&&method==='POST'){if(!user?.verified)fail('请先登录并验证邮箱。',401);limit('redeem:'+user.id,10);transaction(()=>{const code=get('SELECT * FROM codes WHERE hash=?',hash(String(body.code||'').toUpperCase().replace(/\s/g,'')));if(!code||code.used_by)fail('兑换码无效或已使用。');grant(user.id,code.days);run('UPDATE codes SET used_by=?,used_at=? WHERE hash=?',user.id,Date.now(),code.hash);});return send({ok:true});}
   if(path==='/api/progress'){if(!access(user))fail('需要开通题库。',403);if(method==='GET'){const p=get('SELECT * FROM progress WHERE user=?',user.id);return send({revision:p?.revision||0,state:p?JSON.parse(p.state):null});}if(method==='PUT'){if(!Number.isInteger(body.revision)||!body.state||body.state.version!==1)fail('进度格式无效。');const result=transaction(()=>{const current=get('SELECT revision FROM progress WHERE user=?',user.id)?.revision||0;if(current!==body.revision)fail('其他设备已更新进度，请选择保留的版本。',409);run('INSERT INTO progress VALUES(?,?,?,?) ON CONFLICT(user) DO UPDATE SET revision=excluded.revision,state=excluded.state,updated=excluded.updated',user.id,current+1,JSON.stringify(body.state),Date.now());return current+1;});return send({revision:result});}}
   if(path.startsWith('/api/admin/')){if(!admin(user))fail('需要管理员权限。',403);
    if(path==='/api/admin/dashboard'&&method==='GET')return send({users:all('SELECT id,email,verified,created FROM users ORDER BY created DESC LIMIT 200'),codes:all('SELECT label,days,used_by,used_at FROM codes'),release:version()});
    if(path==='/api/admin/codes'&&method==='POST'){const count=Number(body.count),days=Number(body.days);if(!Number.isInteger(count)||count<1||count>100||!Number.isInteger(days)||days<0||days>3650)fail('请填写1至100个兑换码和0至3650天有效期（0为永久）。');const codes=[];transaction(()=>{for(let i=0;i<count;i++){const code='NOIX-'+randomBytes(12).toString('hex').toUpperCase();run('INSERT INTO codes VALUES(?,?,?,?,?)',hash(code),code.slice(0,10)+'…',days,null,null);codes.push(code);}});return send({codes});}
    if(path==='/api/admin/notices'&&method==='POST'){if(!body.title?.trim()||!body.body?.trim()||body.title.length>150||body.body.length>10000)fail('请填写通知标题和正文。');run('INSERT INTO notices VALUES(?,?,?,?)',token(),body.title,body.body,Date.now());return send({ok:true});}
    if(path==='/api/admin/settings'&&method==='PUT'){if(body.release&&(!/^[\w.-]{1,60}$/.test(body.release.version)||typeof body.release.notes!=='string'||body.release.notes.length>10000))fail('版本设置无效。');for(const key of ['release'])if(body[key])run('INSERT INTO settings VALUES(?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value',key,JSON.stringify({...body[key],...(key==='release'?{build:env.APP_BUILD||'1.0.0'}:{})}));return send({ok:true});}
    fail('接口不存在。',404);
   }
   if(path.startsWith('/api/'))fail('接口不存在。',404);
   const protectedAsset=path==='/content.json'||path.startsWith('/audio/')||path.startsWith('/pdfs/')||path.startsWith('/dictionary/');if(protectedAsset&&!access(user))fail('需要开通题库。',403);
   const allowed=protectedAsset||path.startsWith('/assets/')||path.startsWith('/images/')||path.startsWith('/fonts/')||['/manifest.webmanifest','/sw.js','/icon.svg','/icon-192.png','/icon-512.png'].includes(path);
   const target=resolve(root,'dist','.'+(allowed?path:'/index.html')),base=resolve(root,'dist')+'/';if(!target.startsWith(base)||!existsSync(target)||!statSync(target).isFile())fail('文件不存在。',404);
   const types={'.html':'text/html; charset=utf-8','.js':'text/javascript','.json':'application/json','.webmanifest':'application/manifest+json','.css':'text/css','.svg':'image/svg+xml','.png':'image/png','.ttf':'font/ttf','.pdf':'application/pdf','.mp3':'audio/mpeg','.m4a':'audio/mp4'};const size=statSync(target).size;res.setHeader('Content-Type',types[extname(target)]||'application/octet-stream');res.setHeader('Accept-Ranges','bytes');let start=0,end=size-1,status=200;if(req.headers.range){const m=req.headers.range.match(/^bytes=(\d+)-(\d*)$/);if(!m||Number(m[1])>=size){res.writeHead(416,{'Content-Range':`bytes */${size}`});return res.end();}start=Number(m[1]);end=m[2]?Math.min(Number(m[2]),size-1):size-1;if(end<start)fail('范围无效。',416);status=206;res.setHeader('Content-Range',`bytes ${start}-${end}/${size}`);}res.setHeader('Content-Length',end-start+1);res.writeHead(status);if(method==='HEAD')return res.end();createReadStream(target,{start,end}).pipe(res);
  }catch(e){if(!res.headersSent)send({error:e.status?e.message:'服务暂时不可用。'},e.status||500);else res.destroy();}
 }
 return {server:http.createServer(handle),db,close(){clearInterval(cleanup);db.close();}};
}
