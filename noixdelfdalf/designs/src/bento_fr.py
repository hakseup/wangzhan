"""Round 3: option A (bento) with four sets of French details."""
from common import ic, topnav, page
from homes import BASE, quick

STAR = '<svg class="dd" viewBox="0 0 24 24" style="{s}"><path d="M12 2v6M12 16v6M2 12h6M16 12h6M5 5l4 4M15 15l4 4M5 19l4-4M15 9l4-4" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" fill="none"/></svg>'
HEART = '<svg class="dd" viewBox="0 0 24 24" style="{s}"><path d="M12 20s-7-4.4-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 5.6-7 10-7 10z" stroke="currentColor" stroke-width="1.8" fill="none" stroke-linecap="round"/></svg>'
def star(s): return STAR.format(s=s)
def heart(s): return HEART.format(s=s)

GRID = '''
.wrap{padding:24px 72px 30px;display:grid;grid-template-columns:1.25fr 1fr 1fr 1fr;grid-template-rows:auto 1.2fr .8fr auto;gap:16px;height:828px;position:relative}
.hi{grid-column:1/-1;display:flex;align-items:baseline;gap:16px;position:relative}
.hi .hand{font-size:24px;color:#a0687f}
.hi h1{font-family:var(--serif-zh);font-size:28px;font-weight:600;color:#33262f}
.hi .s{margin-left:auto;font-size:12px;color:var(--muted)}
.t{border-radius:22px;padding:22px 24px;position:relative;border:1px solid var(--line);background:#fffdfb}
.t .hand{font-size:17px}
.t h3{font-family:var(--serif-zh);font-size:21px;font-weight:600;margin:4px 0 6px;color:#33262f}
.t p{font-size:12px;color:var(--muted);line-height:1.8}
.bank{grid-row:2/4;display:flex;flex-direction:column}
.daily{grid-column:2/5}
.m{display:flex;flex-direction:column}
.m .meta{margin-top:auto}
.quick{grid-column:1/-1}
.dd{position:absolute;width:30px;height:30px;pointer-events:none}
.learn{--c:var(--sage);--s:var(--sage-soft)}.read{--c:var(--blue);--s:var(--blue-soft)}.tutor{--c:var(--rose);--s:var(--rose-soft)}
'''

GREET = '<div class="hi"><span class="hand">Bonjour, Hutao</span><h1>今天想从哪里开始？</h1><span class="s">{s}</span></div>'

# ====================================================================== 1 · Papeterie 手账文具
v1 = page('首页 A1 · 手账文具', topnav('home') + f'''
<style>{BASE}{GRID}
body{{background:radial-gradient(circle,#e3d8d6 1px,transparent 1.3px) 0 0/22px 22px,#fbf8f4}}
.t{{box-shadow:0 8px 24px #5a3b4c0d}}
.tape{{position:absolute;height:24px;width:96px;top:-11px;opacity:.88;clip-path:polygon(0 8%,4% 0,8% 10%,12% 0,16% 8%,100% 0,96% 50%,100% 100%,92% 92%,88% 100%,0 100%,4% 50%);z-index:2}}
.tape.st{{background:repeating-linear-gradient(90deg,#e8cdd8 0 7px,#f6e7ec 7px 14px)}}
.tape.dt{{background:radial-gradient(circle,#fff 2px,transparent 2.5px) 0 0/10px 10px,#c8d6c0}}
.tape.gg{{background:repeating-linear-gradient(0deg,#a8b8d03a 0 6px,transparent 6px 12px),repeating-linear-gradient(90deg,#a8b8d05a 0 6px,#eef2f8 6px 12px)}}
.tape.yl{{background:repeating-linear-gradient(45deg,#f3dc9e 0 6px,#f8ebc6 6px 12px)}}
.bank{{background:#fffdfb}}
.bank .hand{{color:var(--plum)}}
.tk{{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:16px;flex:1}}
.tk>div{{border-radius:16px;padding:16px;color:#fff;position:relative;overflow:hidden;display:flex;flex-direction:column;transform:rotate(var(--r))}}
.tk>div:before{{content:'';position:absolute;inset:0;background:var(--img);z-index:0}}.tk>div:after{{content:'';position:absolute;inset:0;background:var(--v);z-index:0}}
.tk>div>*{{position:relative;z-index:1}}
.tk b{{font-family:var(--hand);font-size:25px;font-weight:400;line-height:1;white-space:nowrap}}
.tk small{{font-size:11px;opacity:.92}}
.tk ul{{list-style:none;margin-top:auto;font-size:11px;display:grid;grid-template-columns:1fr 1fr;gap:3px 8px}}
.polaroid{{background:#fff;padding:8px 8px 26px;border-radius:3px;box-shadow:0 6px 18px #5a3b4c22}}
.sticker{{position:absolute;right:-8px;top:-10px;width:54px;height:54px;border-radius:50%;background:#f3dc9e;color:#7a5520;display:grid;place-items:center;text-align:center;font-family:var(--hand);font-size:11px;line-height:1.05;transform:rotate(12deg);box-shadow:0 3px 8px #0002;z-index:3}}
.daily{{background:repeating-linear-gradient(180deg,transparent 0 27px,#e6dcd8 27px 28px),#fffefa;padding-left:70px;border-radius:6px 22px 22px 6px}}
.daily:before{{content:'';position:absolute;left:52px;top:0;bottom:0;width:1.5px;background:#e6a8ae}}
.daily:after{{content:'';position:absolute;left:18px;top:24px;bottom:24px;width:14px;background:radial-gradient(circle,#efe6e0 5px,transparent 5.5px) 0 0/14px 34px}}
.daily .row{{display:grid;grid-template-columns:1fr 240px;gap:24px;height:100%}}
.daily .w{{font-family:var(--hand);font-size:42px;color:#5f3f58;line-height:1.1;margin:8px 0 2px}}
.daily .ph{{font-size:11px;color:#a08b7a}}
.daily .zh{{font-size:13px;color:#5c4e57;margin-top:6px}}
.daily .fx{{font-family:var(--hand);font-size:16px;color:#7b6276;margin-top:8px}}
.daily .nw{{border-left:1px dashed #d7c7c2;padding-left:20px;display:flex;flex-direction:column;gap:12px}}
.daily .nw b{{display:block;font:400 14px/1.4 var(--serif-fr);color:#3d2f3a}}
.daily .nw small{{font-size:10.5px;color:#a08b7a}}
.m .ico{{width:42px;height:42px;border-radius:50%;display:grid;place-items:center;background:var(--s);color:var(--c);margin-bottom:10px;border:2px dashed color-mix(in srgb,var(--c) 40%,transparent)}}
.m .hand{{color:var(--c)}}
.quick{{outline:1.5px dashed #ffffff40;outline-offset:-7px}}
</style>
<div class="wrap">
{GREET.format(s='连续学习 12 天 · 本周已练 9 组题')}
{star('color:#f1cd6c;left:318px;top:10px;width:24px;height:24px;transform:rotate(12deg)')}
<div class="t bank"><span class="tape st" style="left:26px;transform:rotate(-5deg)"></span><span class="hand">Banque d’exercices</span><h3>题库练习</h3><p>DELF / DALF 真题，听力、阅读、写作、口语四项。提交后看复盘解析与原文定位。</p>
<div class="tk">
<div class="polaroid" style="--r:-2deg;padding:8px 8px 30px;color:#5c4e57;background:#fff"><div style="flex:1;border-radius:2px;background:url(../assets/arc-haze.png) 30% 60%/cover;position:relative;padding:12px;color:#fff"><div style="position:absolute;inset:0;background:linear-gradient(170deg,#c08636b0,#6d4a1fd0)"></div><div style="position:relative"><b>DELF B2</b><br><small>313 组 · 已练 46</small></div></div><span style="position:absolute;left:10px;bottom:7px;font-family:var(--hand);font-size:14px;color:#8a5f2d">Le café de l’Arc</span></div>
<div class="polaroid" style="--r:2deg;padding:8px 8px 30px;color:#5c4e57;background:#fff"><div style="flex:1;border-radius:2px;background:url(../assets/paris-haze.png) 70% 40%/cover;position:relative;padding:12px;color:#fff"><div style="position:absolute;inset:0;background:linear-gradient(170deg,#97789db0,#4a344cd0)"></div><div style="position:relative"><b>DALF C1</b><br><small>252 组 · 已练 88</small></div></div><span style="position:absolute;left:10px;bottom:7px;font-family:var(--hand);font-size:14px;color:#735a78">Brume sur la Seine</span><span class="sticker">C’est<br>parti !</span></div>
</div>
<div style="display:flex;gap:8px;margin-top:14px"><span class="lvl soon">DELF A2 · bientôt</span><span class="lvl soon">DELF B1 · bientôt</span></div></div>
<div class="t daily"><span class="tape yl" style="right:40px;transform:rotate(4deg)"></span><div class="row"><div>
<div style="display:flex;justify-content:space-between;align-items:center"><span class="hand" style="color:#a0687f;font-size:19px">Aujourd’hui · 今日推送</span><div class="dtabs"><span class="on">一词</span><span>一句</span><span>新闻</span></div></div>
<div class="w">la flânerie</div><div class="ph">[flɑnʁi] n.f. · 城市生活</div><div class="zh">闲逛、漫步；带着好奇心在城里随意散步。</div><div class="fx">« Paris se découvre par la flânerie. »</div></div>
<div class="nw"><small>今日新闻 · 3 篇</small><div><b>Les cafés gardent leurs terrasses l’hiver</b><small>B1 · 3 分钟 · 附音频</small></div><div><b>Le télétravail redessine les villes moyennes</b><small>B2 · 6 分钟</small></div></div></div>
{heart('color:#d48ea0;right:300px;bottom:14px;width:26px;height:26px;transform:rotate(-12deg)')}</div>
<div class="t m learn"><span class="tape dt" style="left:30px;width:70px;transform:rotate(-4deg)"></span><span class="ico">{ic('grammar',18)}</span><span class="hand">Apprendre</span><h3>系统学习</h3><p>分级语法课与主题词汇，学完即练。</p><div class="meta"><span class="lvl" style="background:var(--sage-soft);color:var(--sage)">继续：bien que + 虚拟式</span></div></div>
<div class="t m read"><span class="tape gg" style="left:50%;margin-left:-35px;width:70px;transform:rotate(3deg)"></span><span class="ico">{ic('headphones',18)}</span><span class="hand">Lire &amp; écouter</span><h3>阅读精听</h3><p>新闻精读、逐句听写，点词即查。</p><div class="meta"><span class="lvl" style="background:var(--blue-soft);color:var(--blue)">今日 3 篇 · 4 段音频</span></div></div>
<div class="t m tutor"><span class="tape st" style="right:28px;width:70px;transform:rotate(6deg)"></span><span class="ico">{ic('users',18)}</span><span class="hand">Professeurs</span><h3>找老师</h3><p>看视频挑老师，预约一对一。</p><div class="meta"><span class="lvl" style="background:var(--rose-soft);color:var(--rose)">下节课 周一 19:30</span></div></div>
{quick()}
</div>''')

# ====================================================================== 2 · Bistrot 小酒馆
v2 = page('首页 A2 · 巴黎小酒馆', topnav('home') + f'''
<style>{BASE}{GRID}
body{{background:#fbf7f1}}
.awn{{height:30px;margin:-22px -24px 16px;border-radius:22px 22px 0 0;background:repeating-linear-gradient(90deg,var(--ac) 0 30px,#fbf3ea 30px 60px);position:relative}}
.awn:after{{content:'';position:absolute;left:0;right:0;bottom:-13px;height:14px;background:radial-gradient(circle at 15px 0,var(--ac) 14.5px,transparent 15px) 0 0/60px 14px,radial-gradient(circle at 45px 0,#fbf3ea 14.5px,transparent 15px) 0 0/60px 14px;background-repeat:repeat-x;filter:drop-shadow(0 2px 1px #0000000f)}}
.bank{{--ac:#8a6a8f}}
.bank .hand{{color:var(--plum)}}
.menu2{{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:16px;flex:1}}
.menu2>div{{border-radius:14px;padding:16px;color:#fff;position:relative;overflow:hidden;display:flex;flex-direction:column}}
.menu2>div:before{{content:'';position:absolute;inset:0;background:var(--img);z-index:0}}.menu2>div:after{{content:'';position:absolute;inset:0;background:var(--v);z-index:0}}
.menu2>div>*{{position:relative;z-index:1}}
.menu2 b{{font-family:var(--hand);font-size:25px;font-weight:400;white-space:nowrap}}
.menu2 ul{{list-style:none;margin-top:auto;font-size:11px;display:flex;flex-direction:column;gap:3px}}
.menu2 li{{display:flex;gap:4px}}.menu2 li:after{{content:'';flex:1;border-bottom:1px dotted #ffffff80;margin-bottom:4px;order:1}}.menu2 li span{{order:2}}
.tag{{position:absolute;right:-1px;top:auto;bottom:100px;background:#fffaf0;color:#5a4128;font-family:var(--hand);font-size:13px;padding:4px 10px 4px 16px;clip-path:polygon(10px 0,100% 0,100% 100%,10px 100%,0 50%);z-index:2}}
.daily{{background:#2f3833;color:#efe9de;border:10px solid #a7825c;border-radius:14px;box-shadow:inset 0 0 40px #0005,0 10px 26px #5a3b4c22;padding:18px 26px}}
.daily .row{{display:grid;grid-template-columns:auto 1fr 1fr;gap:26px;align-items:stretch;height:100%}}
.daily .ttl{{font-family:var(--hand);font-size:30px;color:#f6efe2;line-height:1.1;text-align:center;border-right:1px dashed #ffffff40;padding-right:22px;display:flex;flex-direction:column;justify-content:center}}
.daily .ttl small{{font-family:var(--sans);font-size:11px;color:#c9c2b4;margin-top:8px}}
.daily .c .k{{font-family:var(--hand);font-size:15px;color:#e9c98b}}
.daily .c .w{{font-family:var(--hand);font-size:32px;color:#fff;margin:6px 0 2px}}
.daily .c p{{font-size:12px;color:#d6d0c4;line-height:1.7}}
.daily .c .fx{{font-family:var(--hand);font-size:15px;color:#e8e1d3;margin-top:6px}}
.daily .chalk{{position:absolute;right:18px;bottom:8px;font-family:var(--hand);font-size:13px;color:#ffffff70}}
.m .hand{{color:var(--c)}}
.m{{--ac:var(--c)}}
.m .meta{{display:flex;align-items:center;justify-content:space-between}}
.price{{font-family:var(--hand);font-size:15px;color:var(--c);border-bottom:1.5px solid var(--c);padding-bottom:1px}}
.cup{{position:absolute;right:22px;top:46px;color:var(--c);opacity:.6}}
.quick{{border-radius:14px;background:repeating-linear-gradient(90deg,#3a2c37 0 30px,#41323d 30px 60px)}}
</style>
<div class="wrap">
{GREET.format(s='Le menu d’aujourd’hui · 今日学习套餐 20 分钟')}
<div class="t bank"><div class="awn"></div><span class="hand">Banque d’exercices</span><h3>题库练习</h3><p>DELF / DALF 真题四项全练，提交后看复盘解析。</p>
<div class="menu2">
<div style="--img:url(../assets/arc-haze.png) 30% 60%/cover;--v:linear-gradient(170deg,#c08636c8,#6d4a1fe6)"><span class="tag">313</span><b>DELF B2</b><small style="font-size:11px">Le café au pied de l’Arc</small><ul><li>Écoute<span>34</span></li><li>Lecture<span>34</span></li><li>Écrit<span>17</span></li><li>Oral<span>228</span></li></ul></div>
<div style="--img:url(../assets/paris-haze.png) 70% 40%/cover;--v:linear-gradient(170deg,#97789dc8,#4a344ce6)"><span class="tag">252</span><b>DALF C1</b><small style="font-size:11px">Brume sur la Seine</small><ul><li>Écoute<span>56</span></li><li>Lecture<span>28</span></li><li>Écrit<span>28</span></li><li>Oral<span>140</span></li></ul></div>
</div><div style="display:flex;gap:8px;margin-top:14px"><span class="lvl soon">A2 · bientôt</span><span class="lvl soon">B1 · bientôt</span></div></div>
<div class="t daily"><div class="row">
<div class="ttl">Menu<br>du jour<small>今日推送 · 11 月 26 日</small></div>
<div class="c"><span class="k">Entrée · 一词</span><div class="w">la flânerie</div><p>闲逛、漫步；带着好奇心在城里随意散步。</p><div class="fx">« Paris se découvre par la flânerie. »</div></div>
<div class="c"><span class="k">Plat · 一句 &amp; Dessert · 新闻</span><p style="font:15px/1.6 var(--serif-fr);color:#fff;margin:8px 0">« Bien qu’il fasse froid, les terrasses restent pleines. »</p><p>尽管天冷，露天座依然坐满了人。</p><p style="margin-top:8px;color:#e9c98b">☕ Les cafés gardent leurs terrasses l’hiver · B1</p></div>
</div><span class="chalk">bon appétit !</span></div>
<div class="t m learn"><div class="awn"></div><span class="hand">Apprendre</span><h3>系统学习</h3><p>分级语法课与主题词汇，学完即练。</p><div class="meta"><span class="price">Leçon 5</span><span style="font-size:11px;color:var(--muted)">bien que + 虚拟式</span></div></div>
<div class="t m read"><div class="awn"></div><span class="hand">Lire &amp; écouter</span><h3>阅读精听</h3><p>新闻精读、逐句听写，点词即查。</p><div class="meta"><span class="price">3 articles</span><span style="font-size:11px;color:var(--muted)">4 段音频</span></div></div>
<div class="t m tutor"><div class="awn"></div><span class="hand">Professeurs</span><h3>找老师</h3><p>看视频挑老师，预约一对一。</p><div class="meta"><span class="price">dès ¥ 39</span><span style="font-size:11px;color:var(--muted)">周一 19:30</span></div></div>
{quick()}
</div>''')

# ====================================================================== 3 · Carte postale & plaques de rue 明信片与路牌
def plaque(arr, name):
    return f'<div class="plq"><small>{arr}</small><b>{name}</b></div>'
v3 = page('首页 A3 · 明信片与路牌', topnav('home') + f'''
<style>{BASE}{GRID}
body{{background:#faf6f1}}
.plq{{display:inline-flex;flex-direction:column;align-items:center;background:#2b4a78;color:#fff;border-radius:9px;padding:4px 14px 6px;box-shadow:inset 0 0 0 2px #2b4a78,inset 0 0 0 3.5px #fff,0 3px 8px #2b4a7833;margin-bottom:10px}}
.plq small{{font-size:8.5px;letter-spacing:1px;opacity:.85}}
.plq b{{font:600 12px/1.2 var(--serif-fr);letter-spacing:1.2px;text-transform:uppercase;white-space:nowrap}}
.bank .hand{{color:var(--plum)}}
.tix{{display:flex;flex-direction:column;gap:12px;margin-top:16px;flex:1}}
.tix>div{{flex:1;display:grid;grid-template-columns:1fr 84px;border-radius:14px;overflow:hidden;position:relative;color:#fff}}
.tix .main{{padding:14px 16px;position:relative;display:flex;flex-direction:column}}
.tix .main:before{{content:'';position:absolute;inset:0;background:var(--img);z-index:0}}.tix .main:after{{content:'';position:absolute;inset:0;background:var(--v);z-index:0}}
.tix .main>*{{position:relative;z-index:1}}
.tix .main small{{font-size:9.5px;letter-spacing:2px;opacity:.85}}
.tix .main b{{font-family:var(--hand);font-size:28px;font-weight:400;line-height:1.1}}
.tix .main .rt{{margin-top:auto;font-size:11px;display:flex;gap:14px}}
.tix .stub{{background:var(--sb);color:var(--sc);display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;border-left:2px dashed #fffdfb;font-size:10px;line-height:1.4}}
.tix .stub b{{font-family:var(--hand);font-size:22px;font-weight:400}}
.tix>div:before,.tix>div:after{{content:'';position:absolute;right:76px;width:16px;height:16px;border-radius:50%;background:#fffdfb;z-index:2}}
.tix>div:before{{top:-8px}}.tix>div:after{{bottom:-8px}}
.daily{{background:#fffcf6;display:grid;grid-template-columns:1fr 1px 1fr;gap:24px}}
.daily .sep{{background:#e6dcd2}}
.daily .k{{display:flex;justify-content:space-between;align-items:center}}
.daily .w{{font-family:var(--hand);font-size:40px;color:#5f3f58;margin:10px 0 2px}}
.daily .zh{{font-size:12.5px;color:#5c4e57}}
.daily .fx{{font-family:var(--hand);font-size:16px;color:#7b6276;margin-top:10px}}
.daily .addr{{display:flex;flex-direction:column;justify-content:flex-end;gap:0;position:relative}}
.daily .addr .ln{{border-bottom:1px solid #e1d5ca;height:34px;display:flex;align-items:flex-end;padding-bottom:4px;font-family:var(--hand);font-size:15px;color:#6b5236}}
.stamp{{position:absolute;right:0;top:0;width:76px;height:92px;padding:6px;background:radial-gradient(circle at 5px 5px,#fffcf6 3.2px,transparent 3.7px) -5px -5px/10px 10px,#f3ddc9;transform:rotate(3deg)}}
.stamp div{{width:100%;height:100%;background:url(../assets/paris-haze.png) 72% 30%/600%;display:flex;align-items:flex-end;justify-content:center;font-family:var(--hand);font-size:11px;color:#fff;padding-bottom:4px;text-shadow:0 1px 3px #0006}}
.pm{{position:absolute;right:56px;top:16px;width:92px;height:92px;color:#a0687f;opacity:.75;transform:rotate(-14deg)}}
.m .hand{{color:var(--c)}}
.m .meta{{font-size:11.5px;color:var(--muted);display:flex;align-items:center;gap:6px}}
.quick a{{border-radius:8px}}
</style>
<div class="wrap">
{GREET.format(s='Paris, le 26 novembre · 连续学习 12 天')}
<div class="t bank"><span class="hand">Banque d’exercices</span><h3>题库练习</h3><p>真题就是你的车票：选一个等级，出发。</p>
<div class="tix">
<div style="--img:url(../assets/arc-haze.png) 30% 60%/cover;--v:linear-gradient(110deg,#b57b2ce0,#7a521fd0);--sb:var(--amber-soft);--sc:var(--amber)"><div class="main"><small>BILLET · ALLER SIMPLE</small><b>DELF B2</b><div class="rt"><span>听力 34</span><span>阅读 34</span><span>写作 17</span><span>口语 228</span></div></div><div class="stub">Voie<b>B2</b>313 组</div></div>
<div style="--img:url(../assets/paris-haze.png) 70% 40%/cover;--v:linear-gradient(110deg,#8a6a8fe0,#4a344cd0);--sb:var(--plum-soft);--sc:var(--plum)"><div class="main"><small>BILLET · ALLER SIMPLE</small><b>DALF C1</b><div class="rt"><span>听力 56</span><span>阅读 28</span><span>写作 28</span><span>口语 140</span></div></div><div class="stub">Voie<b>C1</b>252 组</div></div>
</div><div style="display:flex;gap:8px;margin-top:12px"><span class="lvl soon">Prochain départ · A2</span><span class="lvl soon">B1</span></div></div>
<div class="t daily"><div>
<div class="k"><span class="hand" style="color:#a0687f;font-size:19px">Carte du jour · 今日推送</span><div class="dtabs"><span class="on">一词</span><span>一句</span><span>新闻</span></div></div>
<div class="w">la flânerie</div><div class="zh">[flɑnʁi] n.f. · 闲逛、漫步；带着好奇心在城里随意散步。</div><div class="fx">« Paris se découvre par la flânerie. »</div></div>
<span class="sep"></span>
<div class="addr"><div class="stamp"><div>Paris</div></div>
<svg class="pm" viewBox="0 0 100 100" fill="none" stroke="currentColor" stroke-width="2"><circle cx="50" cy="50" r="40"/><circle cx="50" cy="50" r="30" stroke-width="1"/><text x="50" y="46" text-anchor="middle" font-size="12" fill="currentColor" stroke="none" font-family="Georgia">PARIS</text><text x="50" y="62" text-anchor="middle" font-size="9" fill="currentColor" stroke="none" font-family="Georgia">26·XI·2026</text><path d="M92 38c-6 4-10-4-16 0M92 50c-6 4-10-4-16 0M92 62c-6 4-10-4-16 0" stroke-width="1.6"/></svg>
<div class="ln">À : toi, apprenant·e de français</div><div class="ln">Les cafés gardent leurs terrasses l’hiver</div><div class="ln" style="font-family:var(--sans);font-size:11px;color:#a08b7a">今日新闻 · B1 · 3 分钟 · 附音频</div></div></div>
<div class="t m learn">{plaque('1<sup>er</sup> ARRt', 'Rue de la Grammaire')}<span class="hand">Apprendre</span><h3>系统学习</h3><p>分级语法课与主题词汇，学完即练。</p><div class="meta">{ic('grammar',13)} 继续：bien que + 虚拟式</div></div>
<div class="t m read">{plaque('5<sup>e</sup> ARRt', 'Quai des Lectures')}<span class="hand">Lire &amp; écouter</span><h3>阅读精听</h3><p>新闻精读、逐句听写，点词即查。</p><div class="meta">{ic('headphones',13)} 今日 3 篇 · 4 段音频</div></div>
<div class="t m tutor">{plaque('6<sup>e</sup> ARRt', 'Place des Profs')}<span class="hand">Professeurs</span><h3>找老师</h3><p>看视频挑老师，预约一对一。</p><div class="meta">{ic('calendar',13)} 下节课 周一 19:30</div></div>
{quick()}
</div>''')

# ====================================================================== 4 · Pâtisserie 甜品店
def macs(n, total, c):
    return ''.join(f'<i class="mac{" on" if k < n else ""}" style="--mc:{c}"></i>' for k in range(total))
v4 = page('首页 A4 · 甜品店', topnav('home') + f'''
<style>{BASE}{GRID}
body{{background:#fcf7f4}}
.t{{border:0;box-shadow:0 10px 30px #a0687f12}}
.t.scal{{-webkit-mask:radial-gradient(circle at 12px 0,transparent 8px,#000 8.5px) -12px 0/24px 100% repeat-x top,linear-gradient(#000,#000) 0 10px/100% calc(100% - 10px) no-repeat;mask:radial-gradient(circle at 12px 0,transparent 8px,#000 8.5px) -12px 0/24px 100% repeat-x top,linear-gradient(#000,#000) 0 10px/100% calc(100% - 10px) no-repeat}}
.rib{{display:inline-block;font-family:var(--hand);font-size:15px;color:#fff;background:var(--rc);padding:4px 22px;clip-path:polygon(0 0,100% 0,92% 50%,100% 100%,0 100%,8% 50%);margin-bottom:8px}}
.bank{{background:linear-gradient(180deg,#f6eef6,#fffdfb 40%)}}
.box{{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:14px;flex:1}}
.box>div{{border-radius:18px;padding:16px;display:flex;flex-direction:column;background:var(--bg);position:relative;overflow:hidden}}
.box .ph{{height:96px;border-radius:12px;background:var(--img);margin-bottom:12px}}
.box b{{font-family:var(--hand);font-size:24px;font-weight:400;color:var(--tc);white-space:nowrap}}
.box small{{font-size:11px;color:var(--muted)}}
.box .ms{{display:flex;gap:5px;margin-top:auto;flex-wrap:wrap}}
.mac{{width:20px;height:16px;border-radius:50%/50%;background:linear-gradient(180deg,#e8dfe4 0 40%,#fffaf6 40% 60%,#e8dfe4 60%);display:inline-block}}
.mac.on{{background:linear-gradient(180deg,var(--mc) 0 40%,#fffaf6 40% 60%,var(--mc) 60%)}}
.daily{{background:#fff7f2;display:grid;grid-template-columns:1fr 250px;gap:24px}}
.daily .w{{font-family:var(--hand);font-size:42px;color:#a0687f;margin:6px 0 2px}}
.daily .zh{{font-size:12.5px;color:#6c5e67}}
.daily .fx{{font:italic 13.5px/1.7 var(--serif-fr);color:#8b6f7f;margin-top:8px}}
.daily .lbl{{border:1.5px solid #e7c4cc;border-radius:16px;padding:16px;background:#fff;position:relative;display:flex;flex-direction:column;gap:10px}}
.daily .lbl:before{{content:'';position:absolute;left:50%;top:-30px;width:1.5px;height:30px;background:#d9a9b3}}
.daily .lbl:after{{content:'';position:absolute;left:50%;top:-6px;width:12px;height:12px;margin-left:-6px;border-radius:50%;border:1.5px solid #d9a9b3;background:#fff7f2}}
.daily .lbl b{{display:block;font:400 14px/1.4 var(--serif-fr);color:#3d2f3a}}
.daily .lbl small{{font-size:10.5px;color:#a08b9a}}
.m .ico{{width:46px;height:46px;border-radius:50%;display:grid;place-items:center;background:var(--s);color:var(--c);margin-bottom:6px;box-shadow:inset 0 -4px 0 color-mix(in srgb,var(--c) 18%,transparent)}}
.m{{background:#fffdfb}}
.m .meta{{display:flex;align-items:center;gap:8px;font-size:11px;color:var(--muted)}}
.quick{{border-radius:30px}}
.quick a{{background:#ffffff18}}
</style>
<div class="wrap">
{GREET.format(s='Une petite douceur par jour · 每天一点点')}
{heart('color:#e3a0b0;left:298px;top:-4px;width:24px;height:24px;transform:rotate(14deg)')}
<div class="t bank scal"><span class="rib" style="--rc:#a0687f">Banque d’exercices</span><h3>题库练习</h3><p>每做完一组题，就多一颗马卡龙。</p>
<div class="box">
<div style="--bg:var(--amber-soft);--tc:var(--amber);--img:url(../assets/arc-haze.png) 30% 60%/cover"><div class="ph"></div><b>DELF B2</b><small>313 组 · 已练 46</small><div class="ms" style="margin-top:12px">{macs(3,8,'#e2b36b')}</div></div>
<div style="--bg:var(--plum-soft);--tc:var(--plum);--img:url(../assets/paris-haze.png) 70% 40%/cover"><div class="ph"></div><b>DALF C1</b><small>252 组 · 已练 88</small><div class="ms" style="margin-top:12px">{macs(5,8,'#b997bf')}</div></div>
</div><div style="display:flex;gap:8px;margin-top:12px"><span class="lvl soon">A2 · bientôt</span><span class="lvl soon">B1 · bientôt</span></div></div>
<div class="t daily scal"><div><span class="rib" style="--rc:#d39a3a">La douceur du jour · 今日推送</span>
<div style="position:absolute;right:300px;top:26px"><div class="dtabs"><span class="on">一词</span><span>一句</span><span>新闻</span></div></div>
<div class="w">la flânerie</div><div class="zh">[flɑnʁi] n.f. · 闲逛、漫步；带着好奇心在城里随意散步。</div><div class="fx">« Paris se découvre par la flânerie. »</div></div>
<div class="lbl" style="margin-top:26px"><small>今日新闻 · 3 篇</small><div><b>Les cafés gardent leurs terrasses l’hiver</b><small>B1 · 3 分钟 · 附音频</small></div><div><b>Le télétravail redessine les villes</b><small>B2 · 6 分钟</small></div></div></div>
<div class="t m learn scal"><span class="ico">{ic('grammar',19)}</span><span class="rib" style="--rc:var(--sage);font-size:13px">Apprendre</span><h3>系统学习</h3><p>分级语法课与主题词汇，学完即练。</p><div class="meta">{macs(4,6,'#9fb592')} 本单元 4 / 6</div></div>
<div class="t m read scal"><span class="ico">{ic('headphones',19)}</span><span class="rib" style="--rc:var(--blue);font-size:13px">Lire &amp; écouter</span><h3>阅读精听</h3><p>新闻精读、逐句听写，点词即查。</p><div class="meta">{macs(1,3,'#9fb4d4')} 今日 1 / 3 篇</div></div>
<div class="t m tutor scal"><span class="ico">{ic('users',19)}</span><span class="rib" style="--rc:var(--rose);font-size:13px">Professeurs</span><h3>找老师</h3><p>看视频挑老师，预约一对一。</p><div class="meta">{ic('calendar',13)} 下节课 周一 19:30</div></div>
{quick()}
</div>''')

PAGES = {
    'r3-A1-papeterie': v1,
    'r3-A2-bistrot': v2,
    'r3-A3-carte-postale': v3,
    'r3-A4-patisserie': v4,
}
