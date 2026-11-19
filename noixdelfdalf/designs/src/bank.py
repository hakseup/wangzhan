from common import ic, topnav, page, rail

# ------------------------------------------------------------ 1 · 选择等级
bank1 = page('题库练习 · 选择等级', topnav('bank') + f'''
<style>
.wrap{{padding:28px 72px 0}}
.head{{display:flex;align-items:flex-end;margin-bottom:24px}}
.head .hand{{font-size:28px;color:var(--plum)}}
.head h1{{font-family:var(--serif-zh);font-size:32px;font-weight:600;color:#33262f;margin-top:4px}}
.head p{{font-size:13px;color:var(--muted);margin-top:8px}}
.head .r{{margin-left:auto;display:flex;gap:10px}}
.lv{{display:grid;grid-template-columns:200px 200px 1fr 1fr;gap:18px;height:398px}}
.soon{{border-radius:22px;border:1px dashed #dccfd3;background:repeating-linear-gradient(135deg,#fbf8f4 0 12px,#f6f1ec 12px 24px);padding:24px 22px;display:flex;flex-direction:column;color:#b3a7ad}}
.soon .big{{font-family:var(--hand);font-size:54px;line-height:1}}
.soon b{{font-size:13px;color:#8b7e86;font-weight:500;margin-top:10px}}
.soon p{{font-size:11.5px;line-height:1.8;margin-top:8px}}
.soon .chip{{margin-top:auto;align-self:flex-start}}
.live{{border-radius:22px;position:relative;overflow:hidden;color:#fff;padding:30px 30px;display:flex;flex-direction:column}}
.live:before{{content:'';position:absolute;inset:0;background:var(--img);background-size:cover;z-index:-2}}
.live:after{{content:'';position:absolute;inset:0;background:var(--veil);z-index:-1}}
.live{{isolation:isolate}}
.live .big{{font-family:var(--hand);font-size:60px;line-height:1}}
.live .fr{{font-size:17px;margin-top:6px;opacity:.95}}
.live p{{font-size:12.5px;line-height:1.9;margin-top:12px;max-width:380px;opacity:.92}}
.live .cats{{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-top:auto}}
.live .cats div{{padding:11px 14px;border-radius:14px;background:#ffffff26;border:1px solid #ffffff38;backdrop-filter:blur(8px)}}
.live .cats b{{display:block;font-family:var(--hand);font-size:22px}}
.live .cats small{{font-size:11px;opacity:.9}}
.live .prog{{display:flex;align-items:center;gap:14px;margin-top:16px;font-size:11.5px}}
.live .prog .bar{{flex:1;background:#ffffff40}}
.live .prog .btn{{background:#fff;color:var(--c)}}
.bottom{{display:grid;grid-template-columns:1fr 1fr;gap:18px;margin-top:20px}}
.bottom .card{{padding:18px 22px}}
.bottom .hand{{font-size:16px;color:var(--plum)}}
.rec{{display:flex;flex-direction:column;margin-top:6px}}
.rec div{{display:flex;align-items:center;gap:12px;padding:9px 0;border-bottom:1px solid var(--line);font-size:12px;color:var(--muted)}}
.rec div:last-child{{border:0}}
.rec b{{font:400 14px var(--serif-fr);color:#2f2630}}
.rec .s{{margin-left:auto;font-family:var(--hand);font-size:15px}}
.hm{{display:grid;grid-template-columns:repeat(24,1fr);gap:4px;margin-top:12px}}
.hm i{{aspect-ratio:1;border-radius:3px;background:#efe8ee}}
</style>
<div class="wrap">
<div class="head"><div><span class="hand">Banque d’exercices</span><h1>题库练习</h1><p>DELF / DALF 历年真题，按等级、题型和主题整理。练习记录、收藏、错题与生词在各等级间同步。</p></div>
<div class="r"><a class="btn ghost sm">{ic('rotate',13)} 错题回顾 · 23</a><a class="btn ghost sm">{ic('bookmark',13)} 我的收藏 · 14</a></div></div>
<div class="lv">
  <div class="soon"><span class="big">A2</span><b>DELF A2</b><p>听力、阅读、写作、口语四项真题整理中。</p><span class="chip line">即将上线</span></div>
  <div class="soon"><span class="big">B1</span><b>DELF B1</b><p>上线后会提醒你。可以先在「系统学习」打好 B1 语法基础。</p><span class="chip line">{ic('bell',11)} 上线提醒我</span></div>
  <div class="live" style="--img:url(../assets/arc-haze.png) 30% 60%;--veil:linear-gradient(165deg,#c48a3cd9 0%,#8a5d24e6 55%,#5c3d17f0);--c:var(--amber)">
    <span class="big">DELF B2</span><div class="fr fr">Le café au pied de l’Arc</div>
    <p>313 组练习、673 个可独立作答项。考试场次依据考频表，12 段原声录音，提交后开放原文与复盘解析。</p>
    <div class="cats"><div><b>17 · 17</b><small>长听力 · 短听力</small></div><div><b>17 · 17</b><small>阅读 1 · 阅读 2</small></div><div><b>17 · 228</b><small>写作 · 口语</small></div></div>
    <div class="prog">已练习 46 / 313<div class="bar"><span style="width:15%;background:#fff"></span></div><a class="btn sm">进入 B2 {ic('arrow',13)}</a></div></div>
  <div class="live" style="--img:url(../assets/paris-haze.png) 70% 50%;--veil:linear-gradient(165deg,#9a7aa0d9 0%,#6a4d6fe6 55%,#3f2c42f0);--c:var(--plum)">
    <span class="big">DALF C1</span><div class="fr fr">Brume sur la Seine</div>
    <p>252 组练习、682 道听读题，含 28 组写作与 140 组口语。36 段原声录音，法中参考译文与逐句高亮对照。</p>
    <div class="cats"><div><b>20 · 36</b><small>长听力 · 短听力</small></div><div><b>28</b><small>阅读</small></div><div><b>28 · 140</b><small>写作 · 口语</small></div></div>
    <div class="prog">已练习 88 / 252<div class="bar"><span style="width:35%;background:#fff"></span></div><a class="btn sm">进入 C1 {ic('arrow',13)}</a></div></div>
</div>
<div class="bottom">
  <div class="card"><span class="hand">Récemment</span><span style="font-size:11px;color:var(--faint);margin-left:8px">最近练习</span>
  <div class="rec"><div><span class="chip plum">C1 阅读</span><b>Enseignants : le droit d’aimer</b><span class="s" style="color:var(--plum)">3 / 11</span></div>
  <div><span class="chip amber">B2 短听力</span><b>Le retour du troc ?</b><span class="s" style="color:var(--amber)">8 / 10</span></div>
  <div><span class="chip plum">C1 长听力</span><b>La nomophobie</b><span class="s" style="color:var(--plum)">9 / 11</span></div></div></div>
  <div class="card"><span class="hand">Régularité</span><span style="font-size:11px;color:var(--faint);margin-left:8px">近 12 周刷题记录 · 共 134 组</span>
  <div class="hm">{''.join(f'<i style="background:{c}"></i>' for c in (['#efe8ee','#e2d3e4','#c8aecd','#9e7fa5','#efe8ee','#e2d3e4','#f2e3c4','#d8b26e','#efe8ee','#c8aecd','#e2d3e4','#efe8ee']*6)[:72])}</div></div>
</div></div>''', mod='m-bank')

# ------------------------------------------------------------ 2 · C1 题库列表
C1 = [
    ('阅读', 'pink', 'Enseignants : le droit d’aimer', '教师也有表达关爱的权利', '教育与成长', '2021 年 10 月 · 法国场次', '11 题', True),
    ('长听力', '', 'La nomophobie', '离开手机的焦虑', '科技与社会', '2024 年 11 月 · 中国场次', '11 题 · 音频', True),
    ('阅读', 'pink', 'Les fonctions du rêve', '梦的功能', '健康与科学', '2021 年 3 月 · 中国场次', '13 题', False),
    ('短听力', 'blue', 'L’Espresso Book Machine', '一杯咖啡的时间，印一本书', '语言与文化', '2022 年 6 月 · 中国场次', '4 题 · 音频', False),
    ('长听力', '', 'Nos relations avec les robots', '我们与机器人的关系', '科技与社会', '2022 年 11 月 · 中国场次', '11 题 · 音频', False),
    ('写作', 'yellow', 'Le congé de paternité', '父亲也需要育儿假', '社会与生活', '2021 年 10 月 · 法国场次', '综合 + 议论', False),
    ('口语', 'green', 'Faut-il tout noter ?', '所有事物都需要被评分吗？', '社会与生活', '口语主题材料 1 · 第 36 题', '陈述 + 辩论', True),
    ('短听力', 'blue', 'Apprendre le français au Petit Palais', '在小皇宫博物馆学法语', '语言与文化', '2021 年 6 月 · 中国场次', '3 题 · 音频', False),
    ('口语', 'green', 'Quel avenir pour l’industrie musicale ?', '音乐产业的未来在哪里？', '语言与文化', '口语主题材料 2 · 第 10 题', '陈述 + 辩论', False),
]
cards = ''
for t, cl, fr, zh, topic, src, n, done in C1:
    cards += f'''<div class="ex"><div class="tp"><span class="ty {cl}">{t}</span><span class="to">{topic}</span><span class="bk">{ic('bookmark',14)}</span></div>
<h3>{fr}</h3><p>{zh}</p><div class="bt"><span>{src}</span><span>{n}</span>{'<span class="dn">已练习</span>' if done else ''}<b>{ic('arrowup',13)}</b></div></div>'''
bank2 = page('题库练习 · DALF C1', topnav('bank') + '<div class="shell">' + rail([
    ('h', 'DALF C1', '252 组'),
    ('a', 'grid', '全部练习', '252', True), ('a', 'headphones', '长听力', '20', False), ('a', 'wave', '短听力', '36', False),
    ('a', 'book', '阅读', '28', False), ('a', 'pen', '写作', '28', False), ('a', 'mic', '口语', '140', False),
    ('sep',), ('h', 'Mon espace', '我的'),
    ('a', 'bookmark', '我的收藏', '9', False), ('a', 'rotate', '错题回顾', '15', False), ('a', 'clock', '练习记录', '', False),
], '<span class="hand">Changer de niveau</span><span style="display:flex;gap:6px;margin-top:6px"><span class="chip amber">B2</span><span class="chip plum">C1 ✓</span><span class="chip line">A2 · B1 即将上线</span></span>') + f'''
<main class="main">
<style>
.ban{{height:126px;border-radius:20px;position:relative;overflow:hidden;padding:26px 30px;display:flex;align-items:flex-end;margin-bottom:22px;isolation:isolate}}
.ban:before{{content:'';position:absolute;inset:0;background:url(../assets/paris-haze.png) 60% 45%/cover;z-index:-2}}
.ban:after{{content:'';position:absolute;inset:0;background:linear-gradient(90deg,#fbf8fbf2,#f8f2f7c0 50%,#f3eaf130);z-index:-1}}
.ban .hand{{font-size:38px;color:#7b5e7d;line-height:1}}
.ban p{{font-size:12.5px;color:#7a6b75;margin-top:8px}}
.ban .st{{margin-left:auto;display:flex;gap:30px}}
.ban .st b{{display:block;font-family:var(--hand);font-size:26px;color:#6d5270}}
.ban .st small{{font-size:11px;color:#8b7b84}}
.fl{{display:flex;align-items:center;gap:8px;margin-bottom:12px}}
.fl .ct{{padding:8px 13px;border-radius:8px;border:1px solid #e2d9e8;background:#fff9;color:#8e7d97;font-size:11.5px}}
.fl .ct.on{{background:#e9dfef;color:#735982;border-color:#d6c6df}}
.fl .ct small{{color:#aa96b5;margin-left:4px}}
.fl .searchpill{{margin-left:auto;background:#fff;width:250px}}
.tr{{display:flex;gap:6px;margin-bottom:14px}}
.grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}}
.ex{{background:#fffffff0;border:1px solid #e8dfee;border-radius:12px;padding:14px 20px;min-height:150px;display:flex;flex-direction:column}}
.ex .tp{{display:flex;align-items:center;gap:8px}}
.ty{{font-size:10px;padding:3px 8px;border-radius:4px;color:#8d719b;background:#ede5f3}}
.ty.blue{{background:#e7ecf6;color:#8291ad}}.ty.pink{{background:#f4e7ed;color:#b28b9d}}.ty.yellow{{background:#f5efd9;color:#ab9866}}.ty.green{{background:#e7eee4;color:#839b7c}}
.to{{font-size:10.5px;color:#917b9b}}
.bk{{margin-left:auto;color:#baa8c4}}
.ex h3{{font:400 19px/1.35 var(--serif-fr);color:#6a527a;margin:9px 0 3px}}
.ex p{{font-size:12px;color:#7f6d8a}}
.ex .bt{{margin-top:auto;padding-top:12px;border-top:1px solid #eee7f1;display:flex;gap:12px;align-items:center;font-size:10.5px;color:#94839c}}
.ex .bt .dn{{background:#efe8f3;color:#a58daf;padding:2px 7px;border-radius:4px}}
.ex .bt b{{margin-left:auto;width:28px;height:28px;border-radius:50%;background:#f2ecf6;border:1px solid #e3d8ea;color:#a58bb1;display:grid;place-items:center}}
</style>
<div class="crumb">题库练习 {ic('chev',11)} DALF C1 {ic('chev',11)} <span>全部练习</span></div>
<div class="ban"><div><span class="hand">DALF C1 · Brume sur la Seine</span><p>252 组练习 · 682 道听读题 · 36 段原声录音 · 法语标题、中文释义与主题标签</p></div>
<div class="st"><div><b>88</b><small>已练习</small></div><div><b>76%</b><small>客观题正确率</small></div><div><b>15</b><small>待回顾错题</small></div></div></div>
<div class="fl"><span class="ct on">全部<small>252</small></span><span class="ct">长听力<small>20</small></span><span class="ct">短听力<small>36</small></span><span class="ct">阅读<small>28</small></span><span class="ct">写作<small>28</small></span><span class="ct">口语<small>140</small></span>
<div class="searchpill">{ic('search',13)}法语或中文关键词</div><span class="chip line">最新场次 {ic('chevd',11)}</span></div>
<div class="tr"><span class="chip plum">全部主题</span><span class="chip line">教育与成长</span><span class="chip line">科技与社会</span><span class="chip line">社会与生活</span><span class="chip line">健康与科学</span><span class="chip line">城市与环境</span><span class="chip line">语言与文化</span><span class="chip line">工作与经济</span></div>
<div class="grid">{cards}</div>
</main></div>''', mod='m-bank')

# ------------------------------------------------------------ 3 · 练习工作台（沿用 C1 双栏）
paras = [
    ('C’est un tabou. Les enseignants qui se lient à leurs élèves sont vus par leurs collègues comme des âmes trop sensibles. Pourtant, les études montrent que <span class="mk1">le lien affectif est le premier levier pour la réussite scolaire</span>. Dans son ouvrage qui vient de paraître, <i>Quand les profs aiment les élèves</i>, Maël Virat invite à un changement profond des mentalités.'),
    ('Évidemment, le titre de cet essai frappe. Et pas forcément au bon endroit. D’emblée, on imagine des amours coupables. C’est tout l’inverse, bien sûr, que défend Maël Virat, chercheur en psychologie qui montre à quel point l’<span class="wordnote">investissement affectif</span> de l’enseignant est vertueux. Ce lien qu’il appelle « <span class="mk2">amour compassionnel</span> », et qui doit s’inscrire dans une « relation asymétrique » pour éviter toute ambiguïté, rend les deux parties plus heureuses et, surtout, favorise l’apprentissage.'),
    ('« On les voit en masse dans les séries, les films et les émissions. On les voit et on les aime ces enseignants qui nouent avec leurs élèves des liens si puissants que les jeunes se subliment pour réussir leur formation. Sauf que, dans la réalité, le système réprouve cet investissement affectif… »'),
]
pp = ''.join(f'<p>{x}</p>' for x in paras)
qn = ''.join(f'<button class="{c}">{i}</button>' for i, c in enumerate(['answered', 'answered', 'current', '', '', '', '', '', '', '', ''], 1))
bank3 = page('题库练习 · 练习工作台', f'''
<style>
body{{background:#fff}}
.pbar{{height:60px;display:flex;align-items:center;gap:18px;padding:0 27px;border-bottom:1px solid #ececec}}
.pbar img{{width:38px;height:38px}}
.pbar .t{{font-size:14px;color:#6a321b;font-weight:600}}
.pbar .t small{{font:11px var(--serif-fr);color:#a98136;font-weight:400;border-left:1px solid #e4d8ce;padding-left:10px;margin-left:10px}}
.pbar .bc{{font-size:10.5px;color:#999;margin-right:auto}}
.pbar .bc b{{color:#777;font-weight:400}}
.pbar .hand{{font-size:12px;color:#aaa;letter-spacing:1px}}
.dp{{padding:15px 26px 0;height:840px;display:flex;flex-direction:column}}
.meta{{display:flex;gap:17px;align-items:center;font-size:11px;color:#777}}
.meta .src{{color:#aaa;font-size:10.5px}}
.meta .tp{{color:#aaa;font-size:10.5px;border-left:1px solid #e5e5e5;padding-left:15px}}
.dh{{display:flex;align-items:center;gap:20px;margin:10px 0 12px}}
.dh h1{{font:600 23px Arial,var(--sans);color:#292929}}
.dh p{{font-size:11px;color:#949494;margin-top:4px}}
.dh .tools{{margin-left:auto;display:flex;gap:8px}}
.tb{{display:inline-flex;align-items:center;gap:6px;border:1px solid #ddd3e3;background:#fff;color:#765d83;padding:7px 11px;border-radius:5px;font-size:11px}}
.timer{{display:inline-flex;align-items:center;gap:6px;border:1px solid #e7e7e7;color:#777;border-radius:5px;padding:5px 9px;font-size:11px}}
.timer b{{color:#555;font-size:12px}}
.split{{flex:1;display:grid;grid-template-columns:1fr 12px 1fr;border-top:1px solid #e5e5e5;min-height:0}}
.ph{{height:42px;padding:9px 21px;border-bottom:1px solid #eee;display:flex;align-items:center;gap:8px;font-size:11px;color:#555}}
.ph span{{margin-left:auto;color:#aaa;font-size:10px}}
.rt{{display:flex;gap:25px;padding:0 23px;border-bottom:1px solid #eee}}
.rt a{{font-size:11px;color:#aaa;padding:12px 0 10px}}
.rt a.on{{color:#67516f;border-bottom:2px solid #9e83a9}}
.hint{{padding:12px 24px 0;color:#aaa;font-size:9.5px}}
.rc{{padding:20px 27px;font:18px/1.72 Arial,var(--sans);color:#222;overflow:hidden;height:560px}}
.rc h4{{font-size:1.16em;font-weight:700;margin-bottom:.65em}}
.rc p{{margin-bottom:1.1em}}
.hd{{position:relative;display:flex;align-items:center;justify-content:center}}
.hd:before{{content:'';position:absolute;top:0;bottom:0;left:5px;width:1px;background:#d1d1d1}}
.hd span{{z-index:1;border:1px solid #bbb;background:#fff;font-size:13px;width:25px;height:26px;display:grid;place-items:center;color:#aaa}}
.q{{border-bottom:1px solid #eee;padding:22px 25px 24px}}
.qm{{display:flex;gap:10px;align-items:center;margin-bottom:11px}}
.qm b{{width:28px;height:27px;display:grid;place-items:center;border:1px solid #9baebe;color:#444;font-weight:500;font-size:15px}}
.qm small{{font-size:9.5px;color:#aaa}}
.q h3{{font:400 17px/1.65 Arial,var(--sans);color:#222;margin-bottom:14px}}
.q textarea{{width:100%;height:84px;border:1px solid #dedede;border-radius:4px;padding:10px 12px;font:16px/1.7 Georgia,serif;color:#333;resize:none}}
.op{{display:flex;gap:11px;align-items:flex-start;padding:9px;border:1px solid transparent;border-radius:3px;font:15px/1.7 Arial,var(--sans);color:#333}}
.op i{{width:16px;height:16px;border-radius:50%;border:1.5px solid #888;margin-top:5px;flex-shrink:0}}
.op.ch{{border-color:#ddd3e3}}.op.ch i{{border:5px solid #7e628a}}
.op small{{display:block;font-size:11px;color:#aaa}}
.ft{{height:61px;display:flex;align-items:center;gap:13px;border-top:1px solid #e5e5e5;padding:0 4px}}
.ft .nav{{display:flex;gap:5px;flex:1}}
.ft .nav button{{min-width:27px;height:29px;border-radius:3px;font-size:11px;color:#aaa;border:1px solid transparent}}
.ft .nav .answered{{background:#f0eaf5;color:#8c6ea0}}
.ft .nav .current{{border-color:#9d84ae;color:#735388;box-shadow:inset 0 0 0 1px #d8c9e1}}
.ft .sc{{font-size:10px;color:#aaa}}
.ft .btn{{background:#392b37;color:#fff;border-radius:5px;height:36px;font-size:11px}}
</style>
<div class="pbar"><img src="../assets/hutao-logo.png" alt=""><span class="t">胡桃法语<small>DALF C1</small></span><span class="bc">题库练习 › C1 › 阅读 › <b>Enseignants : le droit d’aimer</b></span><span class="hand">UN PETIT PAS CHAQUE JOUR</span><span class="avatar">H</span></div>
<div class="dp">
<div class="meta"><span>{ic('chevl',12)} 返回题库</span><span class="src">2021 年 10 月 · 法国场次</span><span class="tp">教育与成长</span></div>
<div class="dh"><div><h1>Enseignants : le droit d’aimer</h1><p>教师也有表达关爱的权利 · 阅读理解 · 11 题</p></div>
<div class="tools"><span class="timer">{ic('clock',13)} 倒计时 <b>48:12</b></span><span class="tb">{ic('bookmark',13)} 收藏</span><span class="tb">{ic('maximize',13)} 全屏专注</span></div></div>
<div class="split">
  <div style="display:flex;flex-direction:column;min-height:0"><div class="ph">{ic('book',14)} 阅读材料<span>A− A A+</span></div>
  <div class="rt"><a class="on">法语原文</a><a>中文参考译文</a><a>双语对照</a></div>
  <div class="hint">选中词句可高亮（黄 → 紫 → 红），或添加单词备注并收入生词本。</div>
  <div class="rc"><h4>Enseignants : le droit d’aimer</h4>{pp}</div></div>
  <div class="hd"><span>‹›</span></div>
  <div style="display:flex;flex-direction:column;min-height:0"><div class="ph">{ic('pen',14)} 作答区<span>已答 2 / 11</span></div>
  <div class="q"><div class="qm"><b>1</b><small>简答</small></div><h3>À quel paradoxe font face les enseignants dans l’article ?</h3>
  <textarea>Le lien affectif favorise la réussite scolaire, mais il reste un tabou dans la profession.</textarea></div>
  <div class="q"><div class="qm"><b>2</b><small>单选</small></div><h3>Pour Maël Virat, les jeunes enseignants se montrent… à l’idée de développer un rapport affectif avec leurs élèves.</h3>
  <div class="op ch"><i></i><span>prudents<small>谨慎</small></span></div><div class="op"><i></i><span>indifférents<small>无所谓</small></span></div><div class="op"><i></i><span>enthousiastes<small>热情期待</small></span></div></div></div>
</div>
<div class="ft"><div class="nav">{qn}</div><span class="sc">已作答 2 / 11</span><span class="tb">{ic('chevl',12)}</span><span class="tb">{ic('chev',12)}</span><a class="btn">提交并查看复盘</a></div>
</div>''', mod='m-bank')

# ------------------------------------------------------------ 4 · B2 复盘
bank4 = page('题库练习 · B2 复盘', topnav('bank') + f'''
<style>
.wrap{{padding:24px 48px 0;display:grid;grid-template-columns:1fr 540px;gap:30px}}
.sum{{grid-column:1/-1;display:flex;align-items:center;gap:30px;padding:20px 28px;border-radius:20px;background:linear-gradient(110deg,#f8ead0,#fbf3e4 55%,#fdf9f2);border:1px solid #f0dfbf}}
.sum .sc{{width:92px;height:92px;border-radius:50%;background:conic-gradient(var(--amber) 0 72%,#f1e2c4 72%);display:grid;place-items:center}}
.sum .sc b{{width:74px;height:74px;border-radius:50%;background:#fdf8ef;display:grid;place-items:center;font-family:var(--hand);font-size:22px;color:var(--amber)}}
.sum h1{{font:400 24px var(--serif-fr);color:#4f3a1c}}
.sum p{{font-size:12px;color:#8a7552;margin-top:6px}}
.sum .ks{{margin-left:auto;display:flex;gap:28px}}
.sum .ks div{{text-align:center}}
.sum .ks b{{display:block;font-family:var(--hand);font-size:24px}}
.sum .ks small{{font-size:11px;color:#8a7552}}
.txt{{padding-top:4px}}
.txt .hd{{display:flex;align-items:center;gap:10px;font-size:12px;color:var(--muted);margin-bottom:10px}}
.txt .hd .seg{{margin-left:auto}}
.txt p{{font:17px/1.85 var(--serif-fr);color:#2f2630;margin-bottom:14px}}
.ev{{background:#fbefd6;border-bottom:2px solid #c9923f;padding:1px 2px}}
.ev.cand{{background:none;border-bottom:2px dashed #c9923f}}
.ev sup{{font:600 9px var(--sans);color:#fff;background:var(--amber);border-radius:8px;padding:1px 5px;margin-left:3px}}
.qs{{display:flex;flex-direction:column;gap:12px}}
.qc{{border-radius:16px;border:1px solid var(--line);background:#fffdfb;padding:16px 20px}}
.qc .t{{display:flex;align-items:center;gap:10px;font-size:11px;color:var(--faint)}}
.qc .t b{{width:26px;height:26px;border-radius:8px;display:grid;place-items:center;font-size:13px;color:#fff}}
.qc .t .st{{margin-left:auto}}
.qc h4{{font:400 15px/1.6 var(--serif-fr);color:#2f2630;margin:10px 0 8px}}
.qc .ans{{display:flex;gap:10px;font-size:12px;color:var(--muted);flex-wrap:wrap}}
.qc .ans span b{{font-family:var(--serif-fr);font-weight:400;color:#2f2630}}
.qc .why{{margin-top:10px;padding:10px 12px;border-radius:10px;background:#faf6ee;font-size:12px;line-height:1.85;color:#6b5a3e}}
.qc .why i{{font-style:normal;color:var(--amber);font-weight:600}}
.qc .self{{display:flex;gap:8px;margin-top:10px;align-items:center;font-size:11px;color:var(--faint)}}
.ok{{background:var(--sage)}}.bad{{background:#c07a6f}}.rev{{background:#b49ab9}}
</style>
<div class="wrap m-bank">
<div class="sum"><div class="sc"><b>8 / 11</b></div><div><span class="chip amber">DELF B2 · 阅读 2 · 复盘</span><h1 style="margin-top:8px">Faut-il être beau pour faire de l’information ?</h1><p>做新闻需要好看吗 · 科技影响 · 国外考过，国内暂未考过 · 用时 34 分 20 秒</p></div>
<div class="ks"><div><b style="color:var(--sage)">8</b><small>正确</small></div><div><b style="color:#c07a6f">2</b><small>错误</small></div><div><b style="color:#9b7fa1">1</b><small>待自评</small></div><a class="btn dark sm" style="align-self:center;background:var(--amber)">{ic('repeat',12)} 重做错题</a></div></div>
<section class="txt"><div class="hd">{ic('book',14)} 原文定位 · 实线为已核对引文，虚线为候选位置<div class="seg"><a class="on">法文</a><a>双语</a></div></div>
<p>La sur-importance du physique et du style à la télévision fait couler de l’encre. Le magazine du <i>Monde</i> titrait il y a peu « Le Journal télévisé : nouveau concours de beauté ». Ce constat est-il vraiment nouveau ?</p>
<p>La récente charte vestimentaire de France 3 semble confirmer cette tendance. « Évitez les jeans délavés ou troués », « la jupe se porte au niveau du genou ». <span class="ev">La charte vestimentaire de la chaîne envoyée à tous les présentateurs va bien au-delà des impératifs techniques et visuels<sup>2 · 3</sup></span>, ceux qui permettent d’éviter un mélange de couleurs susceptible de produire des vibrations à l’écran.</p>
<p>« Les vêtements sont un langage, au même titre que le logo de la chaîne ou les décors », justifie le directeur. <span class="ev cand">Et c’est parfois toute l’apparence physique qui est contrôlée.<sup>1 ?</sup></span></p></section>
<section class="qs">
<div class="qc"><div class="t"><b class="ok">1</b>单选<span class="st chip sage">{ic('check',11)} 正确</span></div><h4>Le texte évoque le sujet… des présentateurs de journaux télévisés.</h4>
<div class="ans"><span>你的答案 <b>A · de l’apparence physique</b></span></div></div>
<div class="qc"><div class="t"><b class="rev">2</b>简答 · 自评<span class="st chip plum">待自评</span></div><h4>Quel est le document que France 3 a diffusé auprès de ses présentateurs ?</h4>
<div class="ans"><span>你的答案 <b>un règlement sur les vêtements</b></span><span>参考 <b>une charte (vestimentaire)</b></span></div>
<div class="self">同义表达可以算对：<span class="chip sage">{ic('check',11)} 我答对了</span><span class="chip line">部分正确</span><span class="chip line">答错了</span></div></div>
<div class="qc"><div class="t"><b class="bad">3</b>判断<span class="st chip rose">{ic('x',11)} 错误</span></div><h4>D’après le document, les présentateurs doivent uniquement éviter les tenues qui posent des problèmes techniques.</h4>
<div class="ans"><span>你的答案 <b>Vrai</b></span><span>正确 <b>Faux</b></span></div>
<div class="why"><i>依据</i> « …va bien au-delà des impératifs techniques et visuels » —— 着装规定远远超出技术要求，所以「只需避免技术问题」是错误的。</div>
<div class="self"><span class="chip amber">{ic('note',11)} 已加入错题本</span><span class="chip line">{ic('plus',11)} 把 « impératif » 加入生词本</span></div></div>
</section></div>''', mod='m-bank')

PAGES = {
    '31-bank-levels': bank1,
    '32-bank-c1-library': bank2,
    '33-bank-practice': bank3,
    '34-bank-b2-review': bank4,
}
