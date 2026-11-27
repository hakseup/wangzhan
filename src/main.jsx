import React,{useEffect,useMemo,useState} from 'react';
import {createRoot} from 'react-dom/client';
import {Search,Volume2,Plus,Layers,FileText,Headphones,Users,ArrowRight,Lock,Menu,X,BookOpen,Repeat,Mic,Clock,PlayCircle,Video,CalendarDays,PenLine,Sparkles} from 'lucide-react';
import {AccountProvider,useAccount} from './account.jsx';
import {NAV,HERO,TODAY,BANKS,UPCOMING_BANKS,LEVELS,LEARN,READ,TEACHERS} from './site.js';
import {overview} from './progress.js';
import './portal.css';

const ICONS={book:BookOpen,layers:Layers,repeat:Repeat,mic:Mic};
const useRoute=()=>{const get=()=>location.hash.replace(/^#\/?/,'').split(/[/?]/)[0];const [r,setR]=useState(get);useEffect(()=>{const f=()=>{setR(get());window.scrollTo(0,0);};addEventListener('hashchange',f);return()=>removeEventListener('hashchange',f);},[]);return r;};
const go=id=>{location.hash='#/'+id;};
const frDate=()=>new Date().toLocaleDateString('fr-FR',{weekday:'short',day:'numeric',month:'short'});

// 占位标记：之后替换为正式内容时，把 site.js 里对应条目的 sample 去掉即可。
const Sample=({on,children='示例'})=>on?<span className="sample-tag" title="版式占位，内容待填充">{children}</span>:null;

function Header({route}){
 const account=useAccount(),[open,setOpen]=useState(false),[q,setQ]=useState('');
 useEffect(()=>setOpen(false),[route]);
 const initial=(account.user?.email||'').slice(0,1).toUpperCase()||'N';
 return <header className="site-header">
  <a className="brand" href="#/" aria-label="胡桃法语首页"><img src="/images/logo.png" alt="" width="46" height="46"/><span><b>胡桃法语</b><small className="hand">Noix · le français</small></span></a>
  <button className="icon-btn nav-toggle" aria-label={open?'关闭导航':'打开导航'} aria-expanded={open} onClick={()=>setOpen(v=>!v)}>{open?<X size={20}/>:<Menu size={20}/>}</button>
  <nav className={'main-nav'+(open?' open':'')} aria-label="主导航">
   {NAV.map(n=><a key={n.id} href={'#/'+n.id} className={route===n.id?'active':''} aria-current={route===n.id?'page':undefined}>{n.zh}<small className="hand">{n.fr}</small></a>)}
  </nav>
  <form className="search" role="search" onSubmit={e=>{e.preventDefault();location.hash='#/recherche?q='+encodeURIComponent(q.trim());}}>
   <Search size={16} aria-hidden="true"/><input aria-label="搜索" placeholder="搜索语法、词汇、文章" value={q} onChange={e=>setQ(e.target.value)}/>
  </form>
  <button className="avatar" aria-label={account.user?'我的账号':'登录'} onClick={()=>account.open(account.user?'account':'login')}>{account.user?initial:<span className="hand">N</span>}</button>
 </header>;
}

function Hero({title,subtitle,kicker,aside}){
 return <section className="hero"><div className="wrap hero-inner">
  <div>{kicker&&<p className="hand hero-kicker">{kicker}</p>}<h1 className="hand">{title}</h1>{subtitle&&<p className="hero-sub">{subtitle}</p>}</div>
  {aside&&<div className="hero-aside">{aside}</div>}
 </div></section>;
}

function BankTile({bank,practiced}){
 return <a className="bank-tile" href={bank.href} style={{'--img':`url(${bank.image})`}}>
  <span className="hand bank-name">{bank.exam} {bank.level}</span>
  <span className="bank-meta"><b className="hand">{bank.total}</b> 组 · 已练 {practiced}</span>
 </a>;
}
const SoonTile=({b})=><div className="bank-tile soon" aria-disabled="true"><span className="hand bank-name">{b.level}</span><small>即将上线</small><span className="bank-meta">{b.exam} {b.level} · 题库整理中</span></div>;

function Home(){
 const account=useAccount(),[tab,setTab]=useState('word');
 const stats=useMemo(()=>overview(BANKS,account.user?.id),[account.user?.id]);
 const name=account.user?.email?.split('@')[0];
 return <>
  <Hero title={<>{HERO.line1}<br/>{HERO.line2}</>} subtitle={`你好${name?' '+name:''}，今天想从哪里开始？`}
   aside={<><p className="hand hero-date">{frDate()}</p><p>连续学习 {stats.streak} 天 · 本周学习 {stats.thisWeek} 天 · 已练 {stats.practiced} 组题</p></>}/>
  <main className="grid-bg"><div className="wrap home-grid">
   <section className="card bank-card">
    <p className="hand kicker">Banque d’exercices</p><h2>题库练习</h2>
    <p className="muted">DELF / DALF 真题，听力、阅读、写作、口语四项都有。做完看复盘解析和原文定位。</p>
    <div className="bank-tiles">{BANKS.map(b=><BankTile key={b.id} bank={b} practiced={stats.per[b.id].practiced}/>)}{UPCOMING_BANKS.map(b=><SoonTile key={b.level} b={b}/>)}</div>
   </section>
   <section className="card today-card">
    <div className="today-main">
     <div className="today-head"><p className="hand kicker green">Aujourd’hui · <span>今日推送</span></p>
      <div className="tabs" role="tablist">{[['word','一词'],['sentence','一句'],['news','新闻']].map(([id,l])=><button key={id} role="tab" aria-selected={tab===id} className={tab===id?'active':''} onClick={()=>setTab(id)}>{l}</button>)}</div></div>
     {tab==='word'&&<div className="today-body"><p className="hand word">{TODAY.word.fr}<Sample on={TODAY.word.sample}/></p><p className="muted small">{TODAY.word.ipa} {TODAY.word.pos} · {TODAY.word.theme}</p><p>{TODAY.word.zh}</p><p className="example">{TODAY.word.example}</p></div>}
     {tab==='sentence'&&<div className="today-body"><p className="quote">{TODAY.sentence.fr}<Sample on={TODAY.sentence.sample}/></p><p>{TODAY.sentence.zh}</p><p className="muted small">{TODAY.sentence.note}</p></div>}
     {tab==='news'&&<div className="today-body"><p className="muted">每日新闻精读将放在「阅读精听」板块。</p><a className="link" href="#/lire">去阅读精听 <ArrowRight size={14}/></a></div>}
     <div className="today-actions"><button type="button" disabled title="待接入"><Volume2 size={16}/> 听发音</button><button type="button" disabled title="待接入"><Plus size={16}/> 加入生词本</button><a href="#/apprendre"><Layers size={16}/> 「{TODAY.word.theme}」词汇单元</a></div>
    </div>
    <aside className="today-news"><p className="hand kicker orange">{TODAY.news.length} articles · <span>今日新闻</span><Sample on={TODAY.news.some(n=>n.sample)}/></p>
     {TODAY.news.map((n,i)=><a key={i} className="news-line" href="#/lire"><span className="serif">{n.title}</span><small>{n.level} · {n.minutes} 分钟{n.audio?' · 附音频':''}</small></a>)}
    </aside>
   </section>
   <SectionCard to="apprendre" icon={FileText} tone="green" fr="Apprendre" zh="系统学习" desc="分级语法课和主题词汇，学完马上练。" foot={<>即将开课 · <span className="hand orange">A1 → C2</span></>}/>
   <SectionCard to="lire" icon={Headphones} tone="blue" fr="Lire & écouter" zh="阅读精听" desc="新闻精读、逐句听写，点词就能查。" foot={<>今日 <b className="hand orange">{TODAY.news.length}</b> 篇 · 内容待更新</>}/>
   <SectionCard to="professeurs" icon={Users} tone="red" fr="Professeurs" zh="找老师" desc="看视频挑老师，约一节一对一。" foot={<>老师招募中 · <span className="hand orange">bientôt</span></>}/>
  </div>
  <div className="wrap"><QuickBar stats={stats}/></div></main>
 </>;
}

const SectionCard=({to,icon:Icon,tone,fr,zh,desc,foot})=><a className="card section-card" href={'#/'+to}>
 <span className={'icon-bubble '+tone}><Icon size={20}/></span><p className={'hand kicker '+tone}>{fr}</p><h2>{zh}</h2><p className="muted">{desc}</p><p className="small foot">{foot}</p>
</a>;

function QuickBar({stats}){
 const items=[
  ...BANKS.map(b=>({href:b.href,label:`${b.exam} ${b.level} 题库`,n:b.total})),
  {href:'#/exercer',label:'错题回顾'},
  {href:'#/exercer',label:'生词本',n:stats.words||null},
  {href:'#/exercer',label:'我的收藏',n:stats.bookmarks||null},
  {href:'#/professeurs',label:'我的课程'},
 ];
 return <nav className="quick-bar" aria-label="快速入口"><span className="hand">Accès rapide</span><div>{items.map(i=><a key={i.label} href={i.href}>{i.label}{i.n!=null&&<b className="hand">{i.n}</b>}</a>)}</div></nav>;
}

/* ---------- 题库练习 ---------- */
function Exercises(){
 const account=useAccount(),stats=useMemo(()=>overview(BANKS,account.user?.id),[account.user?.id]);
 return <>
  <Hero kicker="Banque d’exercices" title="S’exercer" subtitle="DELF / DALF 真题题库：听力、阅读、写作、口语，做完看复盘解析和原文定位。"
   aside={<p>共 {BANKS.reduce((n,b)=>n+b.total,0)} 组练习 · 已练 {stats.practiced} 组</p>}/>
  <main className="grid-bg"><div className="wrap stack">
   {BANKS.map(b=><section key={b.id} className="card bank-row">
    <a className="bank-cover" href={b.href} style={{'--img':`url(${b.image})`}}><span className="hand">{b.exam} {b.level}</span></a>
    <div className="bank-info">
     <p className="hand kicker orange">{b.exam} {b.level} · Banque complète</p>
     <h2>{b.exam} {b.level} 题库 <small className="muted">{b.total} 组</small></h2>
     <p className="muted small">{b.note}</p>
     <ul className="parts">{b.parts.map(([k,l])=><li key={k}><span>{l}</span><b className="hand">{b.categories[k]||0}</b></li>)}</ul>
     <div className="row-actions">
      <a className="btn primary" href={b.href}>进入题库 <ArrowRight size={16}/></a>
      <a className="btn" href={b.href+'?view=mistakes'}>错题回顾</a>
      <a className="btn" href={b.href+'?view=bookmarks'}>我的收藏</a>
      <a className="btn" href={b.href+'?view=notes'}>单词笔记</a>
      {b.id==='b2'&&<a className="btn" href="/b2/?view=downloads">PDF 下载</a>}
      {b.id==='b2'&&!account.entitled&&<button className="btn ghost" onClick={()=>account.open(account.user?'redeem':'login')}><Lock size={14}/> {account.user?'输入兑换码开通':'登录后开通'}</button>}
     </div>
     <p className="small muted">本机已练 {stats.per[b.id].practiced} 组 · 收藏 {stats.per[b.id].bookmarks} 组</p>
    </div>
   </section>)}
   <div className="soon-row">{UPCOMING_BANKS.map(b=><div key={b.level} className="card soon-card"><span className="hand big">{b.level}</span><p>{b.exam} {b.level} 题库</p><small className="muted">题库整理中 · 即将上线</small></div>)}</div>
  </div></main>
 </>;
}

/* ---------- 系统学习（版式） ---------- */
function Learn(){
 const [level,setLevel]=useState('B1');
 return <>
  <Hero kicker="Apprendre" title="Pas à pas." subtitle="分级语法课和主题词汇，学完马上练。" aside={<div className="level-pills" role="tablist" aria-label="选择等级">{LEVELS.map(l=><button key={l} role="tab" aria-selected={level===l} className={level===l?'active':''} onClick={()=>setLevel(l)}>{l}</button>)}</div>}/>
  <main className="grid-bg"><div className="wrap stack">
   <div className="track-grid">{LEARN.tracks.map(t=>{const I=ICONS[t.icon];return <article key={t.id} className="card track"><span className="icon-bubble green"><I size={20}/></span><p className="hand kicker green">{t.fr}</p><h3>{t.zh}</h3><p className="muted small">{t.desc}</p><span className="small foot">{level} · 课程待上线</span></article>;})}</div>
   <section className="card">
    <div className="section-head"><div><p className="hand kicker green">Cours · {level}</p><h2>{level} 语法课程</h2></div><span className="sample-tag">版式占位</span></div>
    <ol className="lesson-list">{LEARN.lessons.map(l=><li key={l.no}><span className="hand lesson-no">{l.no}</span><div><b>{l.fr}</b><span className="muted">{l.zh}</span></div><small className="muted"><Clock size={13}/> {l.minutes} 分钟</small><span className="pill">待开放</span></li>)}</ol>
   </section>
   <section className="card">
    <div className="section-head"><div><p className="hand kicker orange">Vocabulaire</p><h2>主题词汇单元</h2></div><span className="sample-tag">版式占位</span></div>
    <div className="unit-grid">{LEARN.units.map(u=><div key={u.name} className="unit"><b>{u.name}</b><small className="muted">词汇待添加</small></div>)}</div>
   </section>
  </div></main>
 </>;
}

/* ---------- 阅读精听（版式） ---------- */
function Read(){
 const [filter,setFilter]=useState('全部');
 return <>
  <Hero kicker="Lire & écouter" title="Lire, écouter, comprendre." subtitle="新闻精读、逐句听写，点词就能查。" aside={<p>每日更新 · 按 B1 / B2 / C1 分级</p>}/>
  <main className="grid-bg"><div className="wrap read-layout">
   <section className="card">
    <div className="section-head"><div><p className="hand kicker blue">Articles</p><h2>新闻精读</h2></div><span className="sample-tag">版式占位</span></div>
    <div className="chips">{READ.filters.map(f=><button key={f} className={filter===f?'active':''} onClick={()=>setFilter(f)}>{f}</button>)}</div>
    <div className="article-list">{READ.articles.map(a=><article key={a.id} className="article"><div className="thumb" aria-hidden="true"/><div><p className="serif">{a.title}</p><p className="muted small">{a.zh}</p><small className="muted">{a.level} · {a.minutes} 分钟 · {a.topic}{a.audio?' · 附音频':''}</small></div></article>)}</div>
   </section>
   <aside className="stack">
    <section className="card"><p className="hand kicker orange">Dictée</p><h2>逐句听写</h2><p className="muted small">一句一句听，写完对照原文。</p>
     <ul className="dictation-list">{READ.dictations.map(d=><li key={d.id}><PlayCircle size={18}/><span>{d.title}</span><small className="muted">待添加音频</small></li>)}</ul></section>
    <section className="card"><p className="hand kicker green">Outils</p><h2>阅读工具</h2>
     <ul className="tool-list"><li><Sparkles size={16}/> 点词查义</li><li><Headphones size={16}/> 逐句跟读</li><li><PenLine size={16}/> 标注与笔记</li></ul><p className="muted small">功能设计中，内容填充后开放。</p></section>
   </aside>
  </div></main>
 </>;
}

/* ---------- 找老师（版式） ---------- */
function Teachers(){
 const [filter,setFilter]=useState('全部');
 return <>
  <Hero kicker="Professeurs" title="Trouver son prof." subtitle="看视频挑老师，约一节一对一。" aside={<p>老师招募中 · 即将开放预约</p>}/>
  <main className="grid-bg"><div className="wrap stack">
   <ol className="steps">{TEACHERS.steps.map(([t,d],i)=><li key={t} className="card"><span className="hand step-no">{i+1}</span><b>{t}</b><small className="muted">{d}</small></li>)}</ol>
   <section className="card">
    <div className="section-head"><div><p className="hand kicker red">Nos professeurs</p><h2>老师列表</h2></div><span className="sample-tag">版式占位</span></div>
    <div className="chips">{TEACHERS.filters.map(f=><button key={f} className={filter===f?'active':''} onClick={()=>setFilter(f)}>{f}</button>)}</div>
    <div className="teacher-grid">{TEACHERS.list.map(t=><article key={t.id} className="teacher">
     <div className="video" aria-hidden="true"><Video size={26}/></div>
     <div className="teacher-body"><b>{t.name}</b><p className="muted small">{t.tagline}</p><div className="tags">{t.tags.map((g,i)=><span key={i}>{g}</span>)}</div><small className="muted">{t.languages}</small></div>
     <div className="teacher-foot"><span className="muted small">价格待定</span><button className="btn" disabled><CalendarDays size={14}/> 预约</button></div>
    </article>)}</div>
   </section>
  </div></main>
 </>;
}

/* ---------- 搜索（版式） ---------- */
function SearchPage(){
 const q=decodeURIComponent((location.hash.split('?q=')[1]||''));
 return <>
  <Hero kicker="Recherche" title="Chercher." subtitle={q?`“${q}” 的搜索结果`:'搜索语法、词汇、文章'}/>
  <main className="grid-bg"><div className="wrap stack"><section className="card">
   <p className="muted">全站搜索将在系统学习与阅读精听内容填充后接入。题目搜索目前可在各题库内使用：</p>
   <div className="row-actions">{BANKS.map(b=><a key={b.id} className="btn" href={b.href}>{b.exam} {b.level} 题库内搜索 <ArrowRight size={14}/></a>)}</div>
  </section></div></main>
 </>;
}

function Footer(){return <footer className="site-footer"><div className="wrap"><span className="hand">Noix · le français</span><span>胡桃法语 · 题库与学习记录由账号云端同步</span></div></footer>;}

function App(){
 const route=useRoute();
 const Page={'':Home,exercer:Exercises,apprendre:Learn,lire:Read,professeurs:Teachers,recherche:SearchPage}[route]||Home;
 useEffect(()=>{const n=NAV.find(n=>n.id===route);document.title=n&&n.id?`${n.zh} · 胡桃法语`:'胡桃法语 · Noix le français';},[route]);
 return <><Header route={route}/><Page/><Footer/></>;
}

createRoot(document.getElementById('root')).render(<AccountProvider><App/></AccountProvider>);
