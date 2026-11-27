import React,{createContext,useContext,useEffect,useState,useCallback} from 'react';
import {X} from 'lucide-react';

// 统一账号：沿用 B2 已建立的 Supabase 登录（/api/login、/api/session 等，HttpOnly Cookie 会话）。
// 在门户登录后，进入 /b2/ 与 /c1/ 时是同一个账号。
export async function api(path,body,method=body?'POST':'GET'){
 const r=await fetch('/api/'+path,{method,credentials:'same-origin',cache:'no-store',headers:body?{'Content-Type':'application/json'}:{},body:body?JSON.stringify(body):undefined});
 const data=await r.json().catch(()=>({}));
 if(!r.ok)throw Object.assign(Error(data.error||'暂时无法连接账号服务，请稍后重试。'),{status:r.status});
 return data;
}

const Ctx=createContext(null);
export const useAccount=()=>useContext(Ctx);

export function AccountProvider({children}){
 const [session,setSession]=useState({user:null,entitled:false}),[ready,setReady]=useState(false),[offline,setOffline]=useState(false),[modal,setModal]=useState('');
 const refresh=useCallback(async()=>{try{const s=await api('session');setSession(s);setOffline(false);return s;}catch{setOffline(true);return null;}finally{setReady(true);}},[]);
 useEffect(()=>{
  // 邮箱验证 / 重设密码链接会带着 #access_token 回到首页。
  const fragment=new URLSearchParams(location.hash.slice(1));
  if(fragment.has('access_token')){
   const credentials={access_token:fragment.get('access_token'),refresh_token:fragment.get('refresh_token')},recovery=fragment.get('type')==='recovery';
   history.replaceState(null,'',location.pathname);
   api('verify',credentials).then(()=>refresh()).then(()=>setModal(recovery?'reset':'account')).catch(()=>{refresh();setModal('login');});
  }else refresh();
 },[refresh]);
 return <Ctx.Provider value={{...session,ready,offline,refresh,open:setModal}}>{children}{modal&&<AccountModal mode={modal} setMode={setModal}/>}</Ctx.Provider>;
}

const TITLES={login:'欢迎回来',register:'建立你的学习账号',forgot:'重设密码',reset:'设置新密码',redeem:'开通 DELF B2 题库',account:'我的学习账号'};

function AccountModal({mode,setMode}){
 const account=useAccount(),[busy,setBusy]=useState(false),[message,setMessage]=useState(''),[error,setError]=useState('');
 useEffect(()=>{setMessage('');setError('');},[mode]);
 useEffect(()=>{const key=e=>{if(e.key==='Escape')setMode('');};addEventListener('keydown',key);return()=>removeEventListener('keydown',key);},[setMode]);
 const submit=async event=>{
  event.preventDefault();if(busy)return;const b=Object.fromEntries(new FormData(event.currentTarget));setBusy(true);setError('');setMessage('');
  try{
   if(mode==='login'){await api('login',b);await account.refresh();setMode('account');}
   else if(mode==='register')setMessage((await api('register',b)).message);
   else if(mode==='forgot')setMessage((await api('forgot',b)).message);
   else if(mode==='reset'){setMessage((await api('reset',b)).message);}
   else if(mode==='redeem'){await api('redeem',{code:b.code});await account.refresh();setMessage('开通成功，现在可以进入 DELF B2 题库了。');}
  }catch(e){setError(e.message);}finally{setBusy(false);}
 };
 const logout=async()=>{setBusy(true);try{await api('logout',{});await account.refresh();setMode('');}catch(e){setError(e.message);}finally{setBusy(false);}};
 const u=account.user;
 return <div className="modal-shade" role="presentation" onMouseDown={e=>{if(e.target===e.currentTarget)setMode('');}}>
  <section className="modal card" role="dialog" aria-modal="true" aria-label={TITLES[mode]}>
   <button className="modal-close" aria-label="关闭" onClick={()=>setMode('')}><X size={18}/></button>
   <p className="kicker">Mon espace Noix</p><h2>{TITLES[mode]}</h2>
   {mode==='account'&&u?<>
    <p className="muted">{u.email}</p>
    <ul className="account-facts">
     <li><span>DELF B2 题库</span><b>{account.entitled?(account.expires>=253402300799000?'已开通（永久）':'已开通，至 '+new Date(account.expires).toLocaleDateString('zh-CN')):'未开通'}</b></li>
     <li><span>DALF C1 题库</span><b>开放使用，登录后自动备份</b></li>
     <li><span>学习记录</span><b>登录后在各题库内自动云端同步</b></li>
    </ul>
    <div className="modal-actions">
     {!account.entitled&&<button className="btn primary" onClick={()=>setMode('redeem')}>输入兑换码</button>}
     {u.admin&&<a className="btn" href="/b2/?panel=admin">管理后台</a>}
     <button className="btn" onClick={()=>setMode('reset')}>修改密码</button>
     <button className="btn ghost" disabled={busy} onClick={logout}>退出登录</button>
    </div>
   </>:mode==='account'?<p className="muted">请先登录。</p>:
   <form onSubmit={submit} className="form">
    {['login','register','forgot'].includes(mode)&&<label>邮箱<input type="email" name="email" required autoComplete="email" maxLength={254}/></label>}
    {['login','register','reset'].includes(mode)&&<label>{mode==='reset'?'新密码':'密码'}<input type="password" name="password" required minLength={10} maxLength={256} autoComplete={mode==='login'?'current-password':'new-password'}/></label>}
    {mode==='redeem'&&<label>兑换码<input name="code" required maxLength={100} placeholder="NOIX-…" autoComplete="off"/></label>}
    {mode==='register'&&<small className="muted">密码至少 10 个字符。注册后请前往邮箱完成验证。</small>}
    <button className="btn primary" disabled={busy}>{busy?'请稍候…':({login:'登录',register:'注册',forgot:'发送重设邮件',reset:'保存新密码',redeem:'开通'})[mode]}</button>
    <div className="form-links">
     {mode==='login'&&<><button type="button" onClick={()=>setMode('register')}>还没有账号？注册</button><button type="button" onClick={()=>setMode('forgot')}>忘记密码</button></>}
     {mode!=='login'&&mode!=='redeem'&&mode!=='reset'&&<button type="button" onClick={()=>setMode('login')}>已有账号，去登录</button>}
     {mode==='redeem'&&<button type="button" onClick={()=>setMode('account')}>返回账号</button>}
    </div>
   </form>}
   {message&&<p className="notice" role="status">{message}</p>}
   {error&&<p className="error" role="alert">{error}</p>}
  </section>
 </div>;
}
