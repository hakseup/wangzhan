from common import ic, topnav, page

WAVE = ''.join(f'<i style="height:{h}px"></i>' for h in [8,14,22,12,26,18,30,16,10,22,28,14,20,9,24,30,18,12,26,16,8,20,28,12,18,24,10,16,22,14,26,12,8,18,24,16])

# ---------------------------------------------------------------- 首页 1 · 首屏
home1 = page('首页 · 首屏', topnav('home', clear=True) + f'''
<style>
.hero-bg{{position:absolute;inset:0;z-index:-2;background:url(../assets/paris-haze.png) 70% 40%/cover}}
.hero-veil{{position:absolute;inset:0;z-index:-1;background:linear-gradient(90deg,#fdf9f6f0 0%,#fbf6f3c4 40%,#f9f1ef30 72%,#f8ece410),linear-gradient(0deg,#fbf6f0f0 0%,#fbf6f000 34%),linear-gradient(180deg,#fffaf588,transparent 20%)}}
.topnav.clear{{background:#fffcf855;backdrop-filter:blur(6px)}}
.hero{{display:grid;grid-template-columns:1fr 430px;gap:60px;padding:70px 72px 0 96px;height:610px}}
.hero .hand.k{{font-size:30px;color:#a0687f;transform:rotate(-3deg);display:inline-block}}
.hero h1{{font-family:var(--serif-zh);font-size:54px;line-height:1.38;font-weight:600;color:#332432;letter-spacing:-.5px;margin:20px 0 14px}}
.hero h1 em{{font-style:normal;color:#7b5e7d;background:linear-gradient(transparent 68%,#f5dc9a99 68%,#f5dc9a99 92%,transparent 92%)}}
.hero .sub{{font:italic 22px/1.4 var(--serif-fr);color:#80627f}}
.hero .desc{{font-size:13px;line-height:2;color:#7a6b75;margin:16px 0 30px;max-width:520px}}
.hero .ctas{{display:flex;gap:12px}}
.levels{{display:flex;align-items:center;gap:0;margin-top:44px;width:520px}}
.levels span{{display:flex;flex-direction:column;align-items:center;gap:7px;flex:1;font-family:var(--hand);font-size:15px;color:#9a8792;position:relative}}
.levels span:before{{content:'';width:11px;height:11px;border-radius:50%;background:#fff;border:2px solid #d9c9d2;z-index:1}}
.levels span:after{{content:'';position:absolute;top:5px;left:50%;width:100%;height:1.5px;background:#dfd2d8}}
.levels span:last-child:after{{display:none}}
.levels span.live:before{{background:var(--honey);border-color:#fff6e3;box-shadow:0 0 0 4px #f3d79a66}}
.levels span.live.c1:before{{background:#8c6a8f;box-shadow:0 0 0 4px #d9c7e077}}
.levels small{{font:10px var(--sans);color:#a99aa3}}
.daily{{padding:30px 32px 26px;margin-top:40px;border-radius:22px 28px 20px 26px;transform:rotate(.6deg)}}
.daily .top{{display:flex;justify-content:space-between;align-items:center;color:#9a8592;font-size:11px}}
.daily .top .hand{{font-size:20px;color:#a0687f}}
.daily blockquote{{font-family:var(--hand);font-size:27px;line-height:1.5;color:#5f3f58;margin:20px 0 14px}}
.daily p{{font-size:13px;line-height:1.9;color:#6e5f69}}
.daily .src{{font-size:11px;color:#a59aa0;margin-top:14px;display:flex;align-items:center;gap:8px}}
.daily .acts{{display:flex;gap:8px;margin-top:18px}}
.mini-mods{{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-top:18px}}
.mini-mods a{{padding:13px 12px;border-radius:14px;background:#fffbf6b0;border:1px solid #fffffff0;backdrop-filter:blur(10px);font-size:11.5px;color:#5b4b57;display:flex;flex-direction:column;gap:8px}}
.mini-mods a svg{{color:var(--c)}}
.stats{{position:absolute;left:96px;right:72px;bottom:44px;display:grid;grid-template-columns:repeat(4,1fr);border-top:1px solid #e3d6d6;padding-top:22px}}
.stats div{{display:flex;align-items:baseline;gap:10px}}
.stats b{{font-family:var(--hand);font-size:32px;color:#6d5270}}
.stats span{{font-size:11.5px;color:#8b7b84}}
.star{{position:absolute;top:120px;left:700px;color:#f2cf6c;filter:drop-shadow(0 0 10px #fff2c7)}}
</style>
<div class="hero-bg"></div><div class="hero-veil"></div>
<svg class="star" width="46" height="46" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><path d="M12 2v6M12 16v6M2 12h6M16 12h6M5 5l4 4M15 15l4 4M5 19l4-4M15 9l4-4"/></svg>
<section class="hero">
  <div>
    <span class="hand k">Bienvenue chez Noix</span>
    <h1>把法语，<em>一步一步</em><br>学成自己的语言</h1>
    <div class="sub">Un petit pas chaque jour — de A1 jusqu’au C1.</div>
    <p class="desc">系统讲解语法与主题词汇，每天推送地道法语新闻与原声音频，DELF / DALF 真题题库随时刷题，还可以预约母语老师一对一练口语。</p>
    <div class="ctas"><a class="btn dark">开始系统学习 {ic('arrow',14)}</a><a class="btn ghost">{ic('library',14)} 进入题库练习</a></div>
    <div class="levels">
      <span>A1<small>入门</small></span><span>A2<small>即将上线</small></span><span>B1<small>即将上线</small></span>
      <span class="live">B2<small>313 组真题</small></span><span class="live c1">C1<small>252 组真题</small></span>
    </div>
  </div>
  <div>
    <div class="glass daily">
      <div class="top"><span class="hand">La phrase du jour</span><span>11 月 19 日 · 周四</span></div>
      <blockquote>« Le lien affectif est le premier levier pour la réussite scolaire. »</blockquote>
      <p>情感纽带是促进学业成功的首要因素。</p>
      <div class="src">{ic('book',13)}摘自 C1 阅读 · Enseignants : le droit d’aimer</div>
      <div class="acts"><span class="chip line">{ic('volume',12)} 朗读</span><span class="chip line">{ic('bookmark',12)} 收藏</span><span class="chip line">{ic('note',12)} 加入生词</span></div>
    </div>
    <div class="mini-mods">
      <a style="--c:var(--sage)">{ic('grammar',17)}系统学习</a>
      <a style="--c:var(--blue)">{ic('headphones',17)}阅读精听</a>
      <a style="--c:var(--plum)">{ic('library',17)}题库练习</a>
      <a style="--c:var(--rose)">{ic('users',17)}找老师</a>
    </div>
  </div>
</section>
<div class="stats">
  <div><b>565</b><span>组 DELF / DALF 真题练习</span></div>
  <div><b>49</b><span>段考试原声录音</span></div>
  <div><b>12</b><span>个主题词汇单元</span></div>
  <div><b>4</b><span>个学习板块，一个账号同步</span></div>
</div>
''')

# ---------------------------------------------------------------- 首页 2 · 四大板块
MODS = [
    ('sage', 'grammar', '系统学习', 'Apprendre pas à pas', '语法从零讲透，主题词汇按场景记牢；每个知识点后面都有配套练习。', ['分级语法课 · A1 – C1', '主题词汇 + 记忆卡片', '讲解后立即配套练习'], '86 节语法课', 'paris-haze.png', '20% 70%', 'Le subjonctif'),
    ('blue', 'headphones', '阅读精听', 'Lire &amp; écouter', '每日精选地道法语新闻与原声音频，点词即查，划线标注，生词自动进本。', ['每日新闻 · 按难度分级', '逐句精听 · 听写模式', '点词查义 · 生词本复习'], '每日更新 3 篇', 'arc-haze.png', '85% 30%', 'Le journal du jour'),
    ('plum', 'library', '题库练习', 'S’exercer', 'DELF B2 与 DALF C1 真题题库完整收录，A2、B1 陆续补充，错题自动归档。', ['B2 · 313 组 &nbsp; C1 · 252 组', '听力 / 阅读 / 写作 / 口语', '复盘解析 · 原文定位'], '565 组真题', 'paris-haze.png', '75% 20%', 'DELF · DALF'),
    ('rose', 'users', '找老师', 'Trouver un prof', '像逛书店一样挑老师：看视频介绍、读学员评价，选好时间直接预约一对一。', ['母语老师 · 中文老师', '试听课 · 考试冲刺课', '课后笔记同步到学习记录'], '一对一在线课', 'arc-haze.png', '10% 80%', 'En tête-à-tête'),
]
cards = ''
for i, (c, icon, zh, fr, desc, feats, stat, img, pos, tag) in enumerate(MODS, 1):
    lis = ''.join(f'<li>{ic("check",13)}{f}</li>' for f in feats)
    cards += f'''<article class="mod" style="--c:var(--{c});--s:var(--{c}-soft)">
  <div class="pic" style="background-image:url(../assets/{img});background-position:{pos}"><span class="num hand">0{i}</span><span class="tag hand">{tag}</span></div>
  <div class="body">
    <span class="mi">{ic(icon,18)}</span>
    <h3>{zh}</h3><div class="fr">{fr}</div>
    <p>{desc}</p><ul>{lis}</ul>
    <div class="foot"><span>{stat}</span><b>{ic('arrow',15)}</b></div>
  </div></article>'''
home2 = page('首页 · 四个板块', topnav('home') + f'''
<style>
body{{background:linear-gradient(180deg,#fbf8f4,#f7f1ec)}}
.wrap{{padding:46px 72px 0}}
.head{{display:flex;align-items:flex-end;justify-content:space-between;margin-bottom:30px}}
.head .hand{{font-size:30px;color:#a0687f}}
.head h2{{font-family:var(--serif-zh);font-size:36px;font-weight:600;color:#33262f;margin-top:6px}}
.head p{{font-size:13px;color:var(--muted);line-height:1.9;max-width:420px;text-align:right}}
.mods{{display:grid;grid-template-columns:repeat(4,1fr);gap:22px}}
.mod{{background:#fffdfb;border:1px solid var(--line);border-radius:20px;overflow:hidden;box-shadow:0 10px 40px #5a3b4c0a}}
.mod .pic{{height:190px;background-size:340%;position:relative}}
.mod .pic:after{{content:'';position:absolute;inset:0;background:linear-gradient(180deg,#fffdfb00 35%,#fffdfbf2 96%)}}.mod .pic:before{{content:'';position:absolute;inset:0;background:var(--s);mix-blend-mode:multiply;opacity:.55}}
.mod .num{{position:absolute;top:16px;left:20px;z-index:1;font-size:13px;color:#fff;background:#3a2c3755;border-radius:20px;padding:2px 10px}}
.mod .tag{{position:absolute;bottom:22px;left:22px;z-index:1;font-size:27px;color:var(--c);transform:rotate(-2deg)}}
.mod .body{{padding:6px 24px 22px;position:relative}}
.mod .mi{{position:absolute;right:22px;top:-26px;width:46px;height:46px;border-radius:14px;display:grid;place-items:center;background:var(--s);color:var(--c);border:3px solid #fffdfb;z-index:2}}
.mod h3{{font-family:var(--serif-zh);font-size:24px;font-weight:600;color:#33262f}}
.mod .fr{{font-size:14px;color:var(--c);margin-top:4px}}
.mod p{{font-size:12.5px;line-height:1.9;color:#7a6c75;margin:14px 0 16px;min-height:72px}}
.mod ul{{list-style:none;display:flex;flex-direction:column;gap:9px;padding-top:16px;border-top:1px dashed var(--line-2)}}
.mod li{{display:flex;gap:8px;align-items:center;font-size:12px;color:#5c4e57}}
.mod li svg{{color:var(--c)}}
.mod .foot{{display:flex;justify-content:space-between;align-items:center;margin-top:22px}}
.mod .foot span{{font-family:var(--hand);font-size:15px;color:var(--c)}}
.mod .foot b{{width:38px;height:38px;border-radius:50%;display:grid;place-items:center;background:var(--c);color:#fff}}
.flow{{display:flex;align-items:center;justify-content:center;gap:16px;margin-top:30px;font-size:12px;color:var(--muted)}}
.flow i{{font-style:normal;font-family:var(--hand);color:#a0687f;font-size:15px}}
.flow span{{display:flex;align-items:center;gap:8px}}
</style>
<div class="wrap">
  <div class="head"><div><span class="hand">Quatre chemins</span><h2>四个板块，陪你走完整条法语路</h2></div>
  <p>先学会，再读懂，然后刷题检验，最后和老师开口说。四个板块共用一个生词本和学习记录。</p></div>
  <div class="mods">{cards}</div>
  <div class="flow"><span><i>apprendre</i> 学</span>{ic('arrow',14)}<span><i>comprendre</i> 读听</span>{ic('arrow',14)}<span><i>s’entraîner</i> 练</span>{ic('arrow',14)}<span><i>parler</i> 说</span></div>
</div>''')

# ---------------------------------------------------------------- 首页 3 · 今日学习
home3 = page('首页 · 今日学习', topnav('home') + f'''
<style>
.wrap{{padding:40px 72px 44px;height:828px;display:grid;grid-template-columns:1.25fr 1fr 360px;grid-template-rows:auto 1fr 1fr;gap:22px}}
.news{{display:flex;flex-direction:column}}.news .b{{flex:1;display:flex;flex-direction:column}}.news .player{{margin-top:auto}}
.wrap>.sec-title{{grid-column:1/-1;margin-bottom:-4px}}
.news{{grid-row:span 2;border-radius:20px;overflow:hidden;background:#fffdfb;border:1px solid var(--line)}}
.news .pic{{height:300px;background:url(../assets/arc-haze.png) 40% 60%/cover;position:relative}}
.news .pic .chip{{position:absolute;top:18px;left:18px;background:#fffbf3e6}}
.news .pic .lvl{{position:absolute;top:18px;right:18px;font-family:var(--hand);font-size:18px;color:#fff;background:#56473a99;padding:2px 12px;border-radius:20px}}
.news .b{{padding:22px 26px}}
.news h3{{font-family:var(--serif-fr);font-size:26px;line-height:1.3;color:#2f2630;font-weight:400}}
.news .zh{{font-size:13px;color:var(--muted);margin:8px 0 14px}}
.news .ex{{font-size:13.5px;line-height:1.9;color:#4c4049;font-family:var(--serif-fr)}}
.news .ex u{{text-decoration:none;border-bottom:2px solid #9bb1d0}}
.player{{display:flex;align-items:center;gap:14px;margin-top:18px;padding:12px 14px;border-radius:14px;background:var(--blue-soft)}}
.player .pb{{width:40px;height:40px;border-radius:50%;background:var(--blue);color:#fff;display:grid;place-items:center}}
.wave{{display:flex;align-items:center;gap:3px;flex:1}}.wave i{{width:3px;border-radius:3px;background:#a9b9d2}}.wave i:nth-child(-n+13){{background:var(--blue)}}
.player small{{font-size:11px;color:var(--blue)}}
.tile{{padding:22px 24px;border-radius:20px;background:#fffdfb;border:1px solid var(--line);position:relative}}
.tile .k{{display:flex;justify-content:space-between;align-items:center;font-size:11px;color:var(--muted)}}
.tile .k .hand{{font-size:19px}}
.gram{{background:linear-gradient(140deg,#eef3ea,#fbfaf6)}}
.gram h4{{font-family:var(--serif-fr);font-style:italic;font-size:24px;color:#3e4d3a;margin:14px 0 6px;font-weight:400}}
.gram p{{font-size:12.5px;color:#6a7466;line-height:1.85}}
.gram .ex{{margin-top:12px;padding:12px 14px;border-radius:12px;background:#ffffffb8;font-family:var(--serif-fr);font-size:14px;color:#3e4d3a;line-height:1.7}}
.gram .ex b{{color:var(--sage)}}
.word h4{{font-family:var(--hand);font-size:34px;color:#5f3f58;margin:12px 0 2px}}
.word .ph{{font-size:12px;color:var(--faint)}}
.word p{{font-size:12.5px;line-height:1.85;color:#6e5f69;margin-top:8px}}
.word .fr-ex{{font:italic 13px/1.7 var(--serif-fr);color:#7b6276;margin-top:8px}}
.me{{grid-row:span 2;display:flex;flex-direction:column;gap:18px}}.me .cont{{flex:1}}
.streak{{padding:24px;border-radius:20px;background:linear-gradient(150deg,#3e2f3c,#5a4357);color:#fff}}
.streak .hand{{font-size:18px;color:#f3cf86}}
.streak .n{{display:flex;align-items:baseline;gap:8px;margin:10px 0 16px}}
.streak .n b{{font-family:var(--hand);font-size:52px;line-height:1}}
.streak .n span{{font-size:12px;color:#d8c8d4}}
.days{{display:grid;grid-template-columns:repeat(7,1fr);gap:6px;text-align:center;font-size:10px;color:#cbb9c6}}
.days i{{display:block;height:28px;border-radius:8px;background:#ffffff1c;margin-top:5px}}
.days i.on{{background:#f3cf86}}
.goal{{display:flex;gap:18px;align-items:center}}
.ring{{width:84px;height:84px;border-radius:50%;background:conic-gradient(var(--plum) 0 68%,#efe8f0 68%);display:grid;place-items:center}}
.ring b{{width:66px;height:66px;border-radius:50%;background:#fffdfb;display:grid;place-items:center;font-family:var(--hand);font-size:20px;color:var(--plum)}}
.goal ul{{list-style:none;font-size:12px;color:#6c5e67;display:flex;flex-direction:column;gap:7px}}
.goal li{{display:flex;align-items:center;gap:8px}}
.cont .t{{font-family:var(--serif-fr);font-size:17px;color:#33262f;margin:10px 0 4px}}
.gram .quiz{{margin-top:14px;padding-top:14px;border-top:1px dashed #cfdac9}}.gram .quiz small,.word .rel small,.news .vocab small{{font-size:10.5px;color:var(--faint);display:block;margin-bottom:8px}}.gram .quiz p{{font:14px/1.7 var(--serif-fr);color:#3e4d3a}}.gram .opts{{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-top:10px}}.gram .opts span{{display:flex;justify-content:center;align-items:center;gap:4px;height:32px;border-radius:10px;background:#fff;border:1px solid #dfe6da;font:13px var(--serif-fr);color:#55604f}}.gram .opts .ok{{background:#e1ebdb;border-color:#b7c9ad;color:var(--sage)}}.word .rel{{margin-top:16px}}.word .rel div,.word .acts{{display:flex;gap:6px;flex-wrap:wrap}}.word .acts{{margin-top:14px}}.news .vocab{{display:flex;gap:6px;align-items:center;margin:14px 0}}.news .vocab small{{margin:0 6px 0 0}}.recent{{list-style:none;margin-top:16px;border-top:1px dashed var(--line-2);padding-top:10px}}.recent li{{display:flex;align-items:center;gap:9px;font-size:11.5px;color:#5f515a;padding:6px 0}}.recent small{{margin-left:auto;font-size:10.5px;color:var(--faint)}}
.cont small{{font-size:11px;color:var(--muted)}}
.cont .bar{{margin:12px 0 4px}}
</style>
<div class="wrap">
  <div class="sec-title"><span class="hand">Aujourd’hui</span><h2>今日学习</h2><span style="font-size:12px;color:var(--muted)">每天 20 分钟：一则新闻、一个语法点、一个词</span><a class="more">学习计划设置 {ic('chev',13)}</a></div>
  <article class="news">
    <div class="pic"><span class="chip blue">{ic('news',12)} 今日新闻 · 城市</span><span class="lvl">B1</span></div>
    <div class="b">
      <h3>À Paris, les cafés s’installent sur les trottoirs pour l’hiver</h3>
      <div class="zh">巴黎咖啡馆的露天座位，今年冬天也不收起来了</div>
      <p class="ex">Les terrasses éphémères, nées pendant la crise sanitaire, sont désormais <u>pérennisées</u>. Les riverains, eux, s’inquiètent du bruit…</p>
      <div class="vocab"><small>本篇生词 6</small><span class="chip blue">pérenniser</span><span class="chip blue">éphémère</span><span class="chip blue">le riverain</span><span class="chip line">+3</span></div>
      <div class="player"><span class="pb">{ic('play',14)}</span><div class="wave">{WAVE}</div><small>01:12 / 03:40</small></div>
    </div>
  </article>
  <div class="tile gram">
    <div class="k"><span class="hand" style="color:var(--sage)">Point de grammaire</span><span class="chip sage">B2 · 语法</span></div>
    <h4>bien que + subjonctif</h4>
    <p>表示让步“尽管……”。从句动词必须用虚拟式，主从句主语可以不同。</p>
    <div class="ex">Bien qu’il <b>fasse</b> froid, les terrasses restent pleines.</div>
    <div class="quiz"><small>配套练习 · 1 / 5</small><p>Bien qu’elle ______ fatiguée, elle continue de réviser.</p>
      <div class="opts"><span>est</span><span class="ok">soit {ic('check',12)}</span><span>sera</span><span>était</span></div></div>
  </div>
  <div class="me">
    <div class="streak"><span class="hand">Série en cours</span>
      <div class="n"><b>12</b><span>天连续打卡 · 最长 31 天</span></div>
      <div class="days"><span>一<i class="on"></i></span><span>二<i class="on"></i></span><span>三<i class="on"></i></span><span>四<i class="on"></i></span><span>五<i></i></span><span>六<i></i></span><span>日<i></i></span></div>
    </div>
    <div class="tile goal"><div class="ring"><b>68%</b></div><ul>
      <li style="color:var(--sage)">{ic('check',13)}<span style="color:#6c5e67">语法课 1 / 1</span></li>
      <li style="color:var(--blue)">{ic('check',13)}<span style="color:#6c5e67">精听 3:40 / 10 分钟</span></li>
      <li style="color:var(--faint)">{ic('target',13)}<span>刷题 0 / 1 组</span></li>
      <li style="color:var(--faint)">{ic('repeat',13)}<span>复习生词 6 / 20</span></li></ul></div>
    <div class="tile cont"><div class="k"><span class="hand" style="color:var(--plum)">Reprendre</span><span class="chip plum">C1 阅读</span></div>
      <div class="t">Enseignants : le droit d’aimer</div><small>教师也有表达关爱的权利 · 上次停在第 3 题</small>
      <div class="bar"><span style="width:38%;background:var(--plum)"></span></div>
      <a class="btn dark sm" style="margin-top:12px">继续作答 {ic('arrow',13)}</a>
      <ul class="recent"><li><span class="dot" style="background:var(--amber)"></span>B2 短听力 · Le retour du troc ?<small>8 / 10</small></li><li><span class="dot" style="background:var(--sage)"></span>语法 · 关系代词 dont<small>已完成</small></li><li><span class="dot" style="background:var(--blue)"></span>精听 · 晨间新闻快讯<small>听写中</small></li></ul></div>
  </div>
  <div class="tile word">
    <div class="k"><span class="hand" style="color:#a0687f">Le mot du jour</span><span class="chip rose">主题 · 城市生活</span></div>
    <h4>la flânerie</h4><div class="ph">[flɑnʁi] n.f.</div>
    <p>闲逛、漫步；带着好奇心在城市里无目的地散步。</p>
    <div class="fr-ex">« Paris se découvre par la flânerie. »</div>
    <div class="rel"><small>同主题词汇</small><div><span class="chip line">le trottoir 人行道</span><span class="chip line">la terrasse 露天座</span><span class="chip line">le riverain 沿街居民</span></div></div>
    <div class="acts"><span class="chip rose">{ic('plus',12)} 加入生词本</span><span class="chip line">{ic('volume',12)} 发音</span><span class="chip line">{ic('cards',12)} 进入「城市生活」词汇单元</span></div>
  </div>
</div>''')

# ---------------------------------------------------------------- 首页 4 · 题库与老师
TEACH = [
    ('CD','Camille Durand', '法国 · 里昂', '#e9d6cf', '#a65f58', '4.98', '1 240', '¥ 188', 'DELF 阅卷官经历 · 口语冲刺', ['口语', 'B2–C1', '考试']),
    ('王','王思敏', '中国 · 上海', '#dfe6dc', '#5f7759', '4.95', '860', '¥ 128', '中文讲解语法 · 零基础友好', ['语法', 'A1–B1', '中文']),
    ('LM','Léa Martin', '法国 · 波尔多', '#e2e6f1', '#566d8e', '4.92', '530', '¥ 158', '新闻精读 · 发音纠正', ['发音', '阅读', '会话']),
]
QUOTES={'CD':'“模拟口试后她逐条写反馈，考场上我一点都不慌。”','王':'“虚拟式终于讲明白了，中文解释特别清楚。”','LM':'“每节课一篇新闻，读完再讨论，进步很快。”'}
tcards = ''
for init, name, place, bg, fg, rate, n, price, line, tags in TEACH:
    quote = QUOTES[init]
    tg = ''.join(f'<span class="chip line">{t}</span>' for t in tags)
    tcards += f'''<div class="t"><div class="ph" style="background:{bg};color:{fg}"><span class="hand">{init}</span><i>{ic('video',12)} 1:20</i></div>
<div class="tb"><div class="nm"><b>{name}</b><span>{ic('star',12,'fill:#e5b04a;stroke:#e5b04a')} {rate}</span></div><small>{place} · {n} 节课</small><p>{line}</p><div class="tg">{tg}</div><blockquote>{quote}</blockquote>
<div class="pr"><span><b>{price}</b> / 50 分钟</span><a class="btn ghost sm">预约试听</a></div></div></div>'''
home4 = page('首页 · 题库与老师', topnav('home') + f'''
<style>
.wrap{{padding:56px 72px 0;display:grid;grid-template-columns:600px 1fr;gap:40px}}
.lv{{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:22px}}
.lv .l{{border-radius:18px;padding:18px 20px;border:1px solid var(--line);background:#fffdfb;position:relative;overflow:hidden;min-height:166px}}
.lv .l .big{{font-family:var(--hand);font-size:40px;line-height:1}}
.lv .l small{{display:block;font-size:11.5px;color:var(--muted);margin-top:8px}}
.lv .l.soon{{background:repeating-linear-gradient(135deg,#fbf8f4 0 10px,#f6f1ec 10px 20px);color:#b3a7ad}}
.lv .l.soon .chip{{position:absolute;right:16px;top:16px}}
.lv .l.live{{min-height:292px;color:#fff;border:0}}
.lv .l.live:before{{content:'';position:absolute;inset:0;background:var(--img) center/cover;z-index:0}}
.lv .l.live:after{{content:'';position:absolute;inset:0;background:var(--veil);z-index:0}}
.lv .l.live>*{{position:relative;z-index:1}}
.lv .l.live .fr{{font-size:15px;opacity:.95;margin-top:6px}}
.lv .l.live ul{{list-style:none;display:grid;grid-template-columns:1fr 1fr;gap:4px 14px;margin-top:16px;font-size:11.5px}}
.lv .l.live ul b{{font-family:var(--hand);font-size:14px;margin-left:4px}}
.lv .l.live .go{{position:absolute;right:18px;bottom:18px;width:36px;height:36px;border-radius:50%;background:#fff;color:var(--c);display:grid;place-items:center}}
.ts{{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-top:22px}}
.t{{border-radius:18px;background:#fffdfb;border:1px solid var(--line);overflow:hidden}}
.t .ph{{height:214px;display:grid;place-items:center;position:relative}}
.t .ph .hand{{font-size:46px}}
.t .ph i{{position:absolute;right:12px;bottom:12px;font-style:normal;font-size:10.5px;background:#ffffffd0;color:#5c4e57;border-radius:20px;padding:3px 9px;display:flex;gap:4px;align-items:center}}
.t .tb{{padding:16px 18px}}
.t .nm{{display:flex;justify-content:space-between;align-items:center}}
.t .nm b{{font-size:15px;font-weight:600;color:#33262f}}
.t .nm span{{font-size:12px;color:#8b6c35;display:flex;gap:3px;align-items:center}}
.t small{{font-size:11px;color:var(--faint)}}
.t p{{font-size:12px;color:#6c5e67;margin:9px 0}}
.t .tg{{display:flex;gap:5px}}.t blockquote{{font:italic 12px/1.8 var(--serif-fr);color:#8b6f7f;margin-top:12px;padding-left:10px;border-left:2px solid var(--line-2)}}
.t .pr{{display:flex;justify-content:space-between;align-items:center;margin-top:14px;padding-top:12px;border-top:1px dashed var(--line-2);font-size:11px;color:var(--muted)}}
.t .pr b{{font-family:var(--serif-fr);font-size:17px;color:#33262f;font-weight:400}}
footer{{position:absolute;left:0;right:0;bottom:0;height:138px;background:#3a2c37;color:#d8c9d3;display:flex;align-items:center;padding:0 72px;gap:60px}}
footer .fb{{display:flex;align-items:center;gap:12px}}
footer .fb img{{width:46px;height:46px;background:#fffaf2;border-radius:50%;padding:3px}}
footer .fb b{{font-family:var(--serif-zh);font-size:18px;color:#f3d79a;display:block}}
footer .fb .hand{{font-size:13px;color:#bfa9b8}}
footer nav{{display:flex;gap:46px;font-size:12px}}
footer nav div{{display:flex;flex-direction:column;gap:6px}}
footer nav b{{color:#fff;font-weight:500;margin-bottom:2px}}
footer .r{{margin-left:auto;text-align:right;font-size:11px;color:#a8949f;line-height:1.9}}
footer .r .hand{{font-size:20px;color:#f3cf86;display:block}}
</style>
<div class="wrap">
  <section>
    <div class="sec-title"><span class="hand">Banque d’exercices</span><h2>真题题库</h2><a class="more">全部题库 {ic('chev',13)}</a></div>
    <div class="lv">
      <div class="l live" style="--img:url(../assets/arc-haze.png);--veil:linear-gradient(160deg,#b57b2ccc,#6d4a1fd9);--c:var(--amber)"><span class="big">DELF B2</span><div class="fr">Le café au pied de l’Arc</div>
        <ul><li>长听力<b>17</b></li><li>短听力<b>17</b></li><li>阅读<b>34</b></li><li>写作<b>17</b></li><li>口语<b>228</b></li><li>考频表同步</li></ul><span class="go">{ic('arrow',15)}</span></div>
      <div class="l live" style="--img:url(../assets/paris-haze.png);--veil:linear-gradient(160deg,#8a6a8fcc,#4a344cd9);--c:var(--plum)"><span class="big">DALF C1</span><div class="fr">Brume sur la Seine</div>
        <ul><li>长听力<b>20</b></li><li>短听力<b>36</b></li><li>阅读<b>28</b></li><li>写作<b>28</b></li><li>口语<b>140</b></li><li>36 段原声</li></ul><span class="go">{ic('arrow',15)}</span></div>
      <div class="l soon"><span class="big">A2</span><small>DELF A2 · 题库整理中</small><span class="chip">即将上线</span></div>
      <div class="l soon"><span class="big">B1</span><small>DELF B1 · 题库整理中</small><span class="chip">即将上线</span></div>
    </div>
  </section>
  <section>
    <div class="sec-title"><span class="hand" style="color:var(--rose)">Nos professeurs</span><h2>找一位合适的老师</h2><a class="more">浏览全部老师 {ic('chev',13)}</a></div>
    <div class="ts">{tcards}</div>
  </section>
</div>
<footer>
  <div class="fb"><img src="../assets/hutao-logo.png" alt=""><div><b>胡桃法语</b><span class="hand">Noix · le français</span></div></div>
  <nav><div><b>学习</b><span>系统学习</span><span>阅读精听</span></div><div><b>练习</b><span>DELF B2</span><span>DALF C1</span></div><div><b>老师</b><span>找老师</span><span>成为老师</span></div><div><b>账号</b><span>学习备份</span><span>帮助中心</span></div></nav>
  <div class="r"><span class="hand">Un petit pas chaque jour</span>学习记录、生词本与笔记在四个板块间同步</div>
</footer>''')

PAGES = {
    '01-home-hero': home1,
    '02-home-modules': home2,
    '03-home-today': home3,
    '04-home-exams-tutors': home4,
}
