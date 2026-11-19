from common import ic, topnav, page, rail

WAVE_H = [10,18,26,14,30,22,36,20,12,28,34,16,24,10,30,38,22,14,32,20,10,26,34,14,22,30,12,20,28,16,32,14,10,22,30,20,12,26,36,18,10,24,32,14,20,28,12,22,30,16,26,34,12,18,28,22,10,30,20,14]
def wave(n_on, h=1.0, gap=3, w=3):
    return ''.join(f'<i class="{"on" if k < n_on else ""}" style="height:{int(v*h)}px;width:{w}px;margin-right:{gap}px"></i>' for k, v in enumerate(WAVE_H))

READ_RAIL = [('h', 'Le kiosque', '今日报亭'),
             ('a', 'spark', '今日推荐', '', True), ('a', 'news', '法语新闻', '128', False), ('a', 'headphones', '原声音频', '64', False),
             ('a', 'wave', '慢速法语', '40', False), ('a', 'bookmark', '我的收藏', '17', False),
             ('sep',), ('h', 'Mes mots', '我的词'),
             ('a', 'note', '生词本', '312', False), ('a', 'repeat', '今日复习', '20', False), ('a', 'clock', '阅读记录', '', False)]

# ------------------------------------------------------------ 1 · 报亭首页
items = [
    ('Société', 'B2', 'Le télétravail redessine les villes moyennes', '远程办公正在重塑中等城市', '6 分钟', 'news', '#e7ecf5'),
    ('Culture', 'B1', 'Pourquoi les Français aiment tant les librairies', '法国人为什么这么爱逛书店', '4 分钟', 'news', '#f7ecd6'),
    ('Sciences', 'C1', 'Sommeil : ce que la recherche a vraiment prouvé', '关于睡眠，研究到底证明了什么', '8 分钟', 'headphones', '#efe8f3'),
    ('Environnement', 'B2', 'Les forêts françaises face à la sécheresse', '干旱中的法国森林', '5 分钟', 'headphones', '#e8eee4'),
]
lst = ''
for cat, lv, fr, zh, t, kind, bg in items:
    lst += f'''<div class="it"><div class="th" style="background:{bg}">{ic(kind,20)}</div><div class="tx"><div class="m"><span>{cat}</span><b>{lv}</b></div><h4>{fr}</h4><small>{zh} · {t}</small></div></div>'''
aud = [('Journal de 8 h', '晨间新闻 · 慢速', '05:12', 'B1', '#566d8e'), ('Une rencontre, un métier', '职业访谈', '09:40', 'B2', '#a6752f'),
       ('Le mot de la semaine', '每周一词', '03:05', 'A2', '#5f7759'), ('Débat : faut-il tout noter ?', '辩论 · 口语素材', '12:30', 'C1', '#735a78')]
au = ''
for fr, zh, d, lv, c in aud:
    au += f'''<div class="au" style="--c:{c}"><span class="pb">{ic('play',13)}</span><div><b>{fr}</b><small>{zh} · {d}</small></div><span class="lv hand">{lv}</span></div>'''
read1 = page('阅读精听 · 今日报亭', topnav('read') + '<div class="shell">' + rail(READ_RAIL, '<span class="hand">Rythme</span>每天一篇新闻 + 10 分钟精听，坚持 30 天，听力材料就不再陌生。') + f'''
<main class="main">
<style>
.lay{{display:grid;grid-template-columns:1fr 430px;gap:26px}}
.feat{{border-radius:20px;overflow:hidden;background:#fffdfb;border:1px solid var(--line)}}
.feat .pic{{height:290px;background:url(../assets/paris-haze.png) 50% 70%/cover;position:relative}}
.feat .pic:after{{content:'';position:absolute;inset:0;background:linear-gradient(0deg,#25303fcc,transparent 60%)}}
.feat .pic .cap{{position:absolute;left:26px;right:26px;bottom:22px;z-index:1;color:#fff}}
.feat .pic .cap .chip{{background:#ffffffe0;color:var(--blue)}}
.feat .pic h2{{font:400 30px/1.25 var(--serif-fr);margin-top:12px}}
.feat .pic p{{font-size:13px;color:#e9eef6;margin-top:6px}}
.feat .b{{padding:18px 26px;display:flex;gap:20px;align-items:center}}
.feat .b p{{font:14px/1.85 var(--serif-fr);color:#4c4049;flex:1}}
.feat .b .btn{{background:var(--blue);color:#fff}}
.meta{{display:flex;gap:14px;font-size:11.5px;color:var(--muted);padding:0 26px 18px}}
.meta span{{display:flex;gap:5px;align-items:center}}
.it{{display:flex;gap:14px;padding:13px 0;border-bottom:1px solid var(--line)}}
.it .th{{width:62px;height:62px;border-radius:14px;display:grid;place-items:center;color:#6c6470;flex-shrink:0}}
.it .m{{display:flex;justify-content:space-between;font-size:10.5px;color:var(--faint);letter-spacing:1px;text-transform:uppercase}}
.it .m b{{font-family:var(--hand);font-size:13px;color:var(--blue);letter-spacing:0}}
.it h4{{font:400 16px/1.35 var(--serif-fr);color:#2f2630;margin:3px 0}}
.it small{{font-size:11.5px;color:var(--muted)}}
.aus{{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-top:22px}}
.au{{display:flex;gap:12px;align-items:center;padding:14px 16px;border-radius:16px;background:#fffdfb;border:1px solid var(--line);position:relative}}
.au .pb{{width:38px;height:38px;border-radius:50%;background:var(--c);color:#fff;display:grid;place-items:center;flex-shrink:0}}
.au b{{display:block;font:400 14px var(--serif-fr);color:#2f2630}}
.au small{{font-size:11px;color:var(--muted)}}
.au .lv{{position:absolute;right:14px;top:10px;font-size:13px;color:var(--c)}}
</style>
<div class="crumb">阅读精听 {ic('chev',11)} <span>今日推荐</span></div>
<div class="page-h" style="margin-bottom:18px"><div><span class="hand">Le kiosque du jour</span><h1>今日报亭</h1><p>11 月 19 日 · 3 篇新闻、4 段音频，按你的水平 B2 推荐</p></div>
<div class="right"><div class="seg"><a>全部</a><a>A2</a><a>B1</a><a class="on">B2</a><a>C1</a></div><a class="btn ghost sm">{ic('filter',13)} 主题</a></div></div>
<div class="lay">
  <article class="feat"><div class="pic"><div class="cap"><span class="chip">{ic('news',11)} 头条 · 社会 · B2</span><h2>À Paris, les cafés s’installent sur les trottoirs pour l’hiver</h2><p>巴黎咖啡馆的露天座位，今年冬天也不收起来了</p></div></div>
  <div class="b"><p>Les terrasses éphémères, nées pendant la crise sanitaire, sont désormais pérennisées. Les riverains, eux, s’inquiètent…</p><a class="btn">开始精读 {ic('arrow',13)}</a></div>
  <div class="meta"><span>{ic('clock',12)} 6 分钟</span><span>{ic('headphones',12)} 配音频 3:40</span><span>{ic('note',12)} 预计生词 9 个</span><span>{ic('eye',12)} 2.4k 人读过</span></div></article>
  <section><div class="sec-title" style="margin-bottom:4px"><span class="hand" style="color:var(--blue)">À lire aussi</span><h2 style="font-size:19px">更多推荐</h2><a class="more">全部 {ic('chev',12)}</a></div>{lst}</section>
</div>
<div class="sec-title" style="margin-top:22px"><span class="hand" style="color:var(--blue)">À écouter</span><h2 style="font-size:19px">今日音频</h2><a class="more">音频库 {ic('chev',12)}</a></div>
<div class="aus" style="margin-top:12px">{au}</div>
</main></div>''', mod='m-read')

# ------------------------------------------------------------ 2 · 文章精读 + 点词查义
read2 = page('阅读精听 · 文章精读', topnav('read') + f'''
<style>
.rd{{display:grid;grid-template-columns:1fr 340px;height:828px}}
.art{{padding:30px 0 0;overflow:hidden;position:relative}}
.tool{{display:flex;align-items:center;gap:10px;padding:0 120px 18px;font-size:12px;color:var(--muted)}}
.tool .seg{{margin-left:auto}}
.inner{{padding:0 120px}}
.inner .k{{display:flex;gap:8px}}
.inner h1{{font:400 36px/1.3 var(--serif-fr);color:#2f2630;margin:14px 0 6px}}
.inner .zh{{font-family:var(--serif-zh);font-size:17px;color:#6c7d96}}
.mini{{display:flex;align-items:center;gap:12px;margin:18px 0 22px;padding:10px 14px;border-radius:14px;background:var(--blue-soft)}}
.mini .pb{{width:34px;height:34px;border-radius:50%;background:var(--blue);color:#fff;display:grid;place-items:center}}
.mini .w{{display:flex;align-items:center;flex:1}}.mini .w i{{border-radius:3px;background:#b6c3d6}}.mini .w i.on{{background:var(--blue)}}
.mini small{{font-size:11px;color:var(--blue)}}
.inner p{{font:19px/1.95 var(--serif-fr);color:#262626;margin-bottom:18px}}
.inner p .cur{{background:#eef2f9;box-shadow:0 0 0 4px #eef2f9;border-radius:3px}}
.w1{{border-bottom:2px solid #9bb1d0;cursor:pointer}}
.pop{{position:absolute;left:618px;top:402px;width:330px;background:#fff;border:1px solid #dfe4ee;border-radius:16px;box-shadow:0 24px 60px #2c3a5526;padding:18px 20px;z-index:3}}
.pop:before{{content:'';position:absolute;left:40px;top:-7px;width:12px;height:12px;background:#fff;border-left:1px solid #dfe4ee;border-top:1px solid #dfe4ee;transform:rotate(45deg)}}
.pop .h{{display:flex;align-items:baseline;gap:10px}}
.pop .h b{{font-family:var(--hand);font-size:26px;color:#33445f}}
.pop .h small{{font-size:11px;color:var(--faint)}}
.pop .h span{{margin-left:auto;color:var(--blue)}}
.pop ol{{margin:10px 0 0 18px;font-size:12.5px;line-height:1.85;color:#4c4049}}
.pop .ex{{font:italic 12.5px/1.7 var(--serif-fr);color:#6c7d96;margin-top:8px}}
.pop .marks{{display:flex;gap:6px;margin-top:14px;align-items:center;padding-top:12px;border-top:1px solid #eef0f4}}
.pop .marks i{{width:20px;height:20px;border-radius:50%;border:2px solid #fff;box-shadow:0 0 0 1px #ddd}}
.pop .marks .btn{{margin-left:auto;background:var(--blue);color:#fff;height:30px;padding:0 12px;font-size:11.5px}}
.side{{border-left:1px solid var(--line);background:#fcfbf9;padding:26px 24px}}
.side .hand{{font-size:17px;color:var(--blue)}}
.side .wl{{margin-top:10px;display:flex;flex-direction:column}}
.side .wl div{{display:flex;justify-content:space-between;align-items:center;padding:10px 0;border-bottom:1px solid var(--line);font-size:12px;color:var(--muted)}}
.side .wl b{{font:400 15px var(--serif-fr);color:#2f2630}}
.side .q{{margin-top:22px;padding:16px 18px;border-radius:14px;background:#fff;border:1px solid var(--line)}}
.side .q p{{font-size:12.5px;line-height:1.8;color:#4c4049;margin:6px 0 10px}}
.side .q .o{{display:flex;flex-direction:column;gap:6px}}
.side .q .o span{{padding:8px 12px;border-radius:10px;border:1px solid var(--line);font:13px var(--serif-fr);color:#4c4049}}
</style>
<div class="rd m-read">
<section class="art">
  <div class="tool"><a style="display:flex;gap:5px;align-items:center">{ic('chevl',13)} 今日报亭</a><span style="margin-left:18px">{ic('highlighter',14)} 划线标注</span><span>{ic('type',14)} 字号</span>
  <div class="seg"><a class="on">法文</a><a>双语对照</a><a>中文参考</a></div></div>
  <div class="inner">
    <div class="k"><span class="chip blue">社会 · B2</span><span class="chip line">{ic('clock',11)} 6 分钟</span><span class="chip line">示例新闻</span></div>
    <h1>À Paris, les cafés s’installent sur les trottoirs pour l’hiver</h1>
    <div class="zh">巴黎咖啡馆的露天座位，今年冬天也不收起来了</div>
    <div class="mini"><span class="pb">{ic('pause',13)}</span><div class="w">{wave(22,0.55,3,2)}</div><small>01:12 / 03:40 · 1.0×</small></div>
    <p><span class="cur">Les terrasses éphémères, nées pendant la crise sanitaire, sont désormais <span class="w1">pérennisées</span>.</span> Chaque hiver, elles accueillent des clients emmitouflés sous des <span class="mk1">couvertures en laine</span>, autour de radiateurs d’appoint.</p>
    <p>Les <span class="wordnote">riverains</span>, eux, s’inquiètent du bruit et de l’<span class="mk2">encombrement des trottoirs</span>. « On ne peut plus passer avec une poussette », regrette une habitante du onzième arrondissement.</p>
    <p>La mairie promet un <span class="mk3">cahier des charges plus strict</span> : chauffage électrique interdit, fermeture à vingt-deux heures…</p>
  </div>
  <div class="pop"><div class="h"><b>pérenniser</b><small>[peʁenize] v.t.</small><span>{ic('volume',16)}</span></div>
  <ol><li>使长久存在，使永久化</li><li>（临时措施）转为长期、常态化</li></ol>
  <div class="ex">« pérenniser un dispositif » 把一项措施固定下来</div>
  <div class="marks"><i style="background:#fff29b"></i><i style="background:#dfc3f3"></i><i style="background:#f4a8ae"></i><span style="font-size:11px;color:var(--faint);margin-left:4px">高亮</span><a class="btn">{ic('plus',12)} 加入生词本</a></div></div>
</section>
<aside class="side"><span class="hand">Mots de l’article</span><span style="font-size:11px;color:var(--faint);margin-left:8px">本文生词 · 已加入 3</span>
<div class="wl"><div><b>pérenniser</b><span>使常态化</span></div><div><b>éphémère</b><span>短暂的</span></div><div><b>le riverain</b><span>沿街居民</span></div><div><b>emmitouflé</b><span>裹得严实的</span></div><div><b>un cahier des charges</b><span>规范细则</span></div><div><b>d’appoint</b><span>辅助的</span></div></div>
<div class="q"><span class="hand">Compréhension</span><p>读后小测 1 / 3：Que reprochent les riverains aux terrasses ?</p>
<div class="o"><span>A. Leurs prix trop élevés</span><span style="border-color:#b8c6dc;background:#f2f5fa">B. Le bruit et l’encombrement</span><span>C. Le manque de chauffage</span></div></div>
</aside></div>''', mod='m-read')

# ------------------------------------------------------------ 3 · 逐句精听 / 听写
sents = [
    ('00:00', 'Bonjour à toutes et à tous, il est huit heures, voici le journal.', 'done'),
    ('00:05', 'À la une ce matin : le gouvernement annonce de nouveaux trains de nuit vers l’Italie.', 'done'),
    ('00:12', 'Les premières liaisons seront ouvertes dès le printemps prochain.', 'cur'),
    ('00:18', 'Une bonne nouvelle pour les voyageurs soucieux de leur empreinte carbone.', ''),
    ('00:25', 'Mais le prix des billets reste une question sensible…', ''),
]
tr = ''
for t, s, st in sents:
    tr += f'<div class="s {st}"><small>{t}</small><p>{s if st != "cur" else "<span class=blur>Les premières liaisons seront ouvertes dès le printemps prochain.</span>"}</p></div>'
read3 = page('阅读精听 · 逐句精听', topnav('read') + f'''
<style>
.wrap{{padding:28px 60px 0;display:grid;grid-template-columns:1fr 360px;gap:36px}}
.top{{display:flex;align-items:flex-end;gap:16px;margin-bottom:18px}}
.top h1{{font:400 30px var(--serif-fr);color:#2f2630}}
.top .zh{{font-size:13px;color:var(--muted);margin-top:4px}}
.top .seg{{margin-left:auto}}
.pl{{border-radius:20px;padding:22px 26px;background:linear-gradient(120deg,#e3e9f3,#eef1f6 60%,#f6f2ee);border:1px solid #e1e6ef}}
.pl .w{{display:flex;align-items:center;height:70px}}.pl .w i{{border-radius:3px;background:#bac6d8}}.pl .w i.on{{background:var(--blue)}}
.pl .w i.loop{{background:#d39a3a}}
.pl .ctr{{display:flex;align-items:center;gap:18px;margin-top:12px;color:#55667f;font-size:12px}}
.pl .big{{width:50px;height:50px;border-radius:50%;background:var(--blue);color:#fff;display:grid;place-items:center}}
.pl .ctr .r{{margin-left:auto;display:flex;gap:8px}}
.tr{{margin-top:20px}}
.s{{display:flex;gap:18px;padding:12px 16px;border-radius:12px}}
.s small{{font-size:11px;color:var(--faint);width:40px;padding-top:6px}}
.s p{{font:18px/1.7 var(--serif-fr);color:#9a949a}}
.s.done p{{color:#4c4049}}
.s.cur{{background:#fff;border:1px solid #d6deea;box-shadow:0 10px 30px #3d557014}}
.s.cur p{{color:#2f2630}}
.blur{{filter:blur(6px);user-select:none}}
.dict{{margin:8px 0 0 74px;padding:16px 18px;border-radius:14px;background:#fff;border:1px solid var(--line)}}
.dict .lb{{font-size:11px;color:var(--faint);display:flex;justify-content:space-between}}
.dict .in{{font:18px/1.8 var(--serif-fr);color:#2f2630;margin-top:8px;padding:8px 12px;border-radius:10px;background:#fbfaf8;border:1px solid #ece7e5}}
.dict .in .ok{{color:var(--sage);border-bottom:2px solid #b8cfb0}}
.dict .in .bad{{color:#b46a5f;text-decoration:line-through}}
.dict .in .fix{{color:var(--sage);font-weight:700}}
.dict .in .miss{{color:#d39a3a;border-bottom:2px dashed #e6c58a}}
.dict .res{{display:flex;gap:16px;margin-top:10px;font-size:11.5px;color:var(--muted)}}
.sd{{display:flex;flex-direction:column;gap:14px}}
.sd .card{{padding:18px 20px}}
.sd .hand{{font-size:16px;color:var(--blue)}}
.modes{{display:flex;flex-direction:column;gap:8px;margin-top:10px}}
.modes div{{display:flex;gap:12px;align-items:center;padding:10px 12px;border-radius:12px;border:1px solid var(--line);font-size:12.5px;color:#4c4049}}
.modes div small{{display:block;font-size:11px;color:var(--faint)}}
.modes div.on{{border-color:#b8c6dc;background:#f2f5fa}}
.modes svg{{color:var(--blue)}}
.stat{{display:grid;grid-template-columns:1fr 1fr 1fr;text-align:center;margin-top:10px}}
.stat b{{display:block;font-family:var(--hand);font-size:24px;color:var(--blue)}}
.stat small{{font-size:11px;color:var(--muted)}}
</style>
<div class="wrap m-read"><div>
<div class="crumb">阅读精听 {ic('chev',11)} 原声音频 {ic('chev',11)} <span>Journal de 8 h</span></div>
<div class="top"><div><h1>Journal de 8 h · Trains de nuit</h1><div class="zh">晨间新闻：开往意大利的夜车 · 慢速 · B1 · 05:12</div></div><div class="seg"><a>盲听</a><a class="on">逐句听写</a><a>跟读</a><a>原文</a></div></div>
<div class="pl"><div class="w">{wave(18,1.5,9,5).replace('style="height:', 'class="x" style="height:')}</div>
<div class="ctr"><span>{ic('back15',18)}</span><span class="big">{ic('play',18)}</span><span>{ic('fwd15',18)}</span><span>00:12 / 05:12</span><span class="chip" style="background:#f6e7c8;color:#9a6c26">{ic('repeat',11)} 单句循环 · 第 3 句</span>
<div class="r"><span class="chip line">0.75×</span><span class="chip line">自动暂停</span></div></div></div>
<div class="tr">{tr.replace('<div class="s cur">', '<div class="s cur">', 1)}</div>
</div>
<aside class="sd" style="padding-top:34px">
<div class="card"><span class="hand">Mode d’écoute</span><div class="modes">
<div>{ic('headphones',16)}<span>盲听整段<small>先抓大意，不看原文</small></span></div>
<div class="on">{ic('pen',16)}<span>逐句听写<small>每句自动暂停，写完再核对</small></span></div>
<div>{ic('mic',16)}<span>影子跟读<small>录音对比原声语调</small></span></div></div></div>
<div class="card"><span class="hand">Ce matin</span><div class="stat"><div><b>2 / 9</b><small>已听写</small></div><div><b>86%</b><small>准确率</small></div><div><b>4</b><small>新生词</small></div></div></div>
<div class="card" style="font-size:12px;color:var(--muted);line-height:1.8">{ic('note',14)} 听写错的单词会自动加入生词本，并标注出处音频与时间点，复习时可回放原句。</div>
</aside></div>''', mod='m-read')
# insert dictation box after the current sentence
read3 = read3.replace('</span></p></div><div class="s ">', '''</span></p></div>
<div class="dict"><div class="lb"><span>你的听写 · 第 3 句</span><span>Entrée 核对</span></div>
<div class="in"><span class="ok">Les premières</span> <span class="bad">liaison</span> <span class="fix">liaisons</span> <span class="ok">seront ouvertes</span> <span class="miss">dès</span> <span class="ok">le printemps prochain.</span></div>
<div class="res"><span style="color:var(--sage)">{ok} 7 词正确</span><span style="color:#b46a5f">1 处拼写 · 复数 -s</span><span style="color:#b98330">1 处漏听 · dès</span></div></div><div class="s ">'''.replace('{ok}', ic('check', 12)), 1)

# ------------------------------------------------------------ 4 · 生词本
wb = [
    ('pérenniser', 'v.t.', '使常态化', '« …sont désormais pérennisées. »', 'Les cafés sur les trottoirs', '阅读', 'mk1', '今天'),
    ('le riverain', 'n.m.', '沿街居民', '« Les riverains s’inquiètent du bruit. »', 'Les cafés sur les trottoirs', '阅读', 'mk2', '今天'),
    ('la liaison', 'n.f.', '线路；连接', '« Les premières liaisons seront ouvertes… »', 'Journal de 8 h', '听力 00:12', 'mk3', '明天'),
    ('le levier', 'n.m.', '杠杆；手段', '« …le premier levier pour la réussite scolaire. »', 'C1 阅读 · Enseignants', '题库', 'mk1', '3 天后'),
    ('la nomophobie', 'n.f.', '无手机恐惧症', '« La nomophobie touche surtout les jeunes. »', 'C1 长听力 · La nomophobie', '题库', 'mk2', '5 天后'),
    ('le troc', 'n.m.', '以物易物', '« Le retour du troc ? »', 'B2 短听力', '题库', 'mk1', '1 周后'),
]
wr = ''
for w, p, m, ex, src, kind, mk, nxt in wb:
    wr += f'<tr><td><b class="w">{w}</b><small>{p}</small></td><td>{m}</td><td class="ex"><span class="{mk}">{ex}</span></td><td><span class="src">{src}</span><small>{kind}</small></td><td class="nx">{nxt}</td></tr>'
read4 = page('阅读精听 · 生词本', topnav('read') + '<div class="shell">' + rail([('h', 'Mes mots', '我的词'),
    ('a', 'note', '全部生词', '312', True), ('a', 'repeat', '今日复习', '20', False), ('a', 'star', '重点标记', '41', False), ('a', 'check', '已掌握', '128', False),
    ('sep',), ('h', 'Sources', '来源'), ('a', 'news', '新闻阅读', '146', False), ('a', 'headphones', '听力听写', '52', False),
    ('a', 'library', '题库练习', '97', False), ('a', 'grammar', '系统学习', '17', False)], '<span class="hand">Révision</span>按遗忘曲线安排复习：1 天、3 天、7 天、15 天各一次。') + f'''
<main class="main">
<style>
.top{{display:grid;grid-template-columns:1.1fr 1fr 1fr;gap:16px;margin-bottom:20px}}
.rev{{border-radius:18px;padding:20px 24px;background:linear-gradient(125deg,#3d4d66,#566d8e);color:#fff;display:flex;align-items:center;gap:20px}}
.rev .hand{{font-size:16px;color:#cfdcf0}}
.rev b{{font-family:var(--hand);font-size:46px;display:block;line-height:1.1}}
.rev small{{font-size:12px;color:#d5e0ee}}
.rev .btn{{margin-left:auto;background:#fff;color:var(--blue)}}
.sm{{padding:18px 22px}}
.sm .hand{{font-size:15px;color:var(--blue)}}
.bars{{display:flex;gap:8px;align-items:flex-end;height:58px;margin-top:10px}}
.bars span{{flex:1;background:#d7e0ec;border-radius:5px 5px 2px 2px}}.bars span.on{{background:var(--blue)}}
.mix{{display:flex;height:12px;border-radius:8px;overflow:hidden;margin:16px 0 10px}}
.lg{{display:flex;gap:14px;font-size:11px;color:var(--muted)}}
.tb{{display:flex;align-items:center;gap:10px;margin-bottom:10px}}
.tb .searchpill{{width:260px;background:#fff}}
.tb .r{{margin-left:auto;display:flex;gap:8px}}
table{{width:100%;border-collapse:collapse}}
th{{text-align:left;font-weight:500;font-size:11px;color:var(--faint);padding:8px 12px;border-bottom:1px solid var(--line)}}
td{{padding:11px 12px;border-bottom:1px solid #f1ebe9;font-size:12.5px;color:#5a4d55;vertical-align:middle}}
td .w{{font:400 16px var(--serif-fr);color:#2f2630;margin-right:6px;font-weight:400}}
td small{{font-size:11px;color:var(--faint);display:block}}
td.ex{{font:13px var(--serif-fr);color:#4c4049}}
td .src{{font:italic 12.5px var(--serif-fr);color:var(--blue)}}
td.nx{{font-size:11.5px;color:var(--muted)}}
</style>
<div class="crumb">阅读精听 {ic('chev',11)} <span>生词本</span></div>
<div class="page-h" style="margin-bottom:16px"><div><span class="hand">Mon carnet de mots</span><h1>生词本</h1><p>四个板块里点过、划过、听错的词，都会带着原句和出处收进这里。</p></div><div class="right"><a class="btn ghost sm">{ic('download',13)} 导出 Anki / CSV</a></div></div>
<div class="top">
  <div class="rev"><div><span class="hand">À réviser aujourd’hui</span><b>20</b><small>个单词待复习 · 约 6 分钟</small></div><a class="btn">开始复习 {ic('arrow',13)}</a></div>
  <div class="card sm"><span class="hand">Cette semaine</span><span style="font-size:11px;color:var(--faint);margin-left:6px">新增 38 词</span><div class="bars"><span class="on" style="height:40%"></span><span class="on" style="height:70%"></span><span class="on" style="height:55%"></span><span class="on" style="height:100%"></span><span style="height:10%"></span><span style="height:10%"></span><span style="height:10%"></span></div></div>
  <div class="card sm"><span class="hand">Maîtrise</span><div class="mix"><span style="width:41%;background:var(--sage)"></span><span style="width:33%;background:#d9b46f"></span><span style="width:26%;background:#d8dfe9"></span></div>
  <div class="lg"><span><i class="dot" style="background:var(--sage)"></i> 已掌握 128</span><span><i class="dot" style="background:#d9b46f"></i> 学习中 102</span><span><i class="dot" style="background:#d8dfe9"></i> 新词 82</span></div></div>
</div>
<div class="tb"><div class="searchpill">{ic('search',13)}搜索单词或释义</div><span class="chip blue">全部</span><span class="chip line">本周</span><span class="chip line">带高亮</span><div class="r"><span class="chip line">按下次复习排序 {ic('chevd',11)}</span></div></div>
<table><tr><th>单词</th><th>释义</th><th>原句（保留你的高亮颜色）</th><th>出处</th><th>下次复习</th></tr>{wr}</table>
</main></div>''', mod='m-read')

PAGES = {
    '21-read-kiosk': read1,
    '22-read-article': read2,
    '23-read-listening': read3,
    '24-read-wordbook': read4,
}
