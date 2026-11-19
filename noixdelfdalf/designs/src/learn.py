from common import ic, topnav, page, rail

LEVEL_RAIL = [('sep',), ('h', 'Niveaux', '难度'),
              ('a', 'layers', 'A1 入门', '14', False), ('a', 'layers', 'A2 基础', '18', False),
              ('a', 'layers', 'B1 进阶', '20', False), ('a', 'layers', 'B2 中高级', '19', True),
              ('a', 'layers', 'C1 高级', '15', False)]

# ------------------------------------------------------------ 1 · 总览
units = [
    ('01', 'Les temps du passé', '过去时态的配合', '复合过去时 · 未完成过去时 · 愈过去时', 100, 'done'),
    ('02', 'Le subjonctif', '虚拟式', '情感、意愿、让步与目的', 60, 'now'),
    ('03', 'Les pronoms relatifs composés', '复合关系代词', 'lequel · auquel · duquel · dont', 0, ''),
    ('04', 'Le discours rapporté', '间接引语', '时态转换 · 时间副词变化', 0, ''),
]
ul = ''
for n, fr, zh, sub, pct, st in units:
    badge = {'done': f'<span class="chip sage">{ic("check",11)} 已完成</span>', 'now': '<span class="chip" style="background:var(--sage);color:#fff">学习中</span>'}.get(st, '<span class="chip line">8 课时</span>')
    ul += f'''<div class="unit {st}"><span class="n hand">{n}</span><div class="ut"><div class="fr">{fr}</div><b>{zh}</b><small>{sub}</small>
<div class="bar"><span style="width:{pct}%;background:var(--sage)"></span></div></div>{badge}</div>'''

themes = [
    ('Éducation', '教育与成长', 96, 72, '#e8eee4', '#5f7759'), ('Travail', '职业职场', 120, 40, '#f7ecd6', '#a6752f'),
    ('Écologie', '生态环境', 108, 55, '#e3eee9', '#4f7a6a'), ('Technologie', '科技与社会', 88, 18, '#e7ecf5', '#566d8e'),
    ('Santé', '健康与科学', 92, 0, '#f6e7e3', '#a65f58'), ('Ville', '城市生活', 74, 9, '#efe8f3', '#735a78'),
]
tg = ''
for fr, zh, n, pct, bg, fg in themes:
    tg += f'''<div class="th" style="background:{bg};--c:{fg}"><span class="hand">{fr}</span><b>{zh}</b><small>{n} 词 · 6 组练习</small>
<div class="ring" style="background:conic-gradient({fg} 0 {pct}%,#ffffffa0 {pct}%)"><i>{pct}%</i></div></div>'''

learn1 = page('系统学习 · 总览', topnav('learn') + '<div class="shell">' + rail([
    ('h', 'Mon parcours', '我的学习'),
    ('a', 'home', '学习总览', '', True), ('a', 'grammar', '语法课程', '86', False), ('a', 'cards', '主题词汇', '12', False),
    ('a', 'target', '配套练习', '', False), ('a', 'rotate', '我的错题', '23', False), ('a', 'note', '学习笔记', '', False),
] + LEVEL_RAIL, '<span class="hand">Conseil</span>先学完一课语法，再做 10 道配套练习，正确率达到 80% 自动解锁下一课。') + f'''
<main class="main">
<style>
.lay{{display:grid;grid-template-columns:1fr 470px;gap:28px}}
.cont{{display:flex;align-items:center;gap:22px;padding:16px 24px;border-radius:18px;background:linear-gradient(110deg,#e4ece0,#f4f1e8 70%);margin-bottom:20px;position:relative;overflow:hidden}}
.cont:after{{content:'';position:absolute;right:-40px;top:-60px;width:220px;height:220px;border-radius:50%;background:#ffffff55}}
.cont .hand{{font-size:15px;color:var(--sage)}}
.cont h3{{font:italic 24px var(--serif-fr);color:#33402f;font-weight:400;margin:2px 0}}
.cont p{{font-size:12px;color:#6a7466}}
.cont .btn{{margin-left:auto;background:var(--sage);color:#fff;z-index:1}}
.unit{{display:flex;align-items:center;gap:18px;padding:13px 20px;border-radius:16px;border:1px solid var(--line);background:#fffdfb;margin-bottom:10px}}
.unit .n{{font-size:24px;color:#c6d1c1;width:34px}}
.unit.now{{border-color:#c8d6c0;box-shadow:0 8px 26px #5f775914}}
.unit.now .n,.unit.done .n{{color:var(--sage)}}
.unit .ut{{flex:1}}
.unit .fr{{font:italic 13px var(--serif-fr);color:var(--sage)}}
.unit b{{font-family:var(--serif-zh);font-size:17px;font-weight:600;color:#33262f;margin-right:10px}}
.unit small{{font-size:11.5px;color:var(--muted)}}
.unit .bar{{margin-top:10px;width:70%}}
.ths{{display:grid;grid-template-columns:1fr 1fr;gap:12px}}
.th{{border-radius:16px;padding:14px 18px;position:relative;min-height:96px}}
.th .hand{{font-size:20px;color:var(--c);display:block}}
.th b{{display:block;font-family:var(--serif-zh);font-size:15px;color:#33262f;margin-top:4px}}
.th small{{font-size:11px;color:#7c7077}}
.th .ring{{position:absolute;right:14px;bottom:14px;width:44px;height:44px;border-radius:50%;display:grid;place-items:center}}
.th .ring i{{width:34px;height:34px;border-radius:50%;background:#fffdfbe0;display:grid;place-items:center;font:600 10px var(--sans);font-style:normal;color:var(--c)}}
.week{{margin-top:12px;padding:12px 18px}}
.week .row{{display:flex;justify-content:space-between;align-items:center;font-size:12px;color:var(--muted)}}
.cols{{display:flex;align-items:flex-end;gap:10px;height:34px;margin-top:8px}}
.cols span{{flex:1;border-radius:6px 6px 3px 3px;background:#dfe7da}}.cols span.on{{background:var(--sage)}}
.days{{display:flex;gap:10px;margin-top:6px}}.days i{{flex:1;text-align:center;font-style:normal;font-size:10px;color:var(--faint)}}
</style>
<div class="crumb">系统学习 {ic('chev',11)} <span>学习总览</span></div>
<div class="page-h" style="margin-bottom:16px"><div><span class="hand">Apprendre pas à pas</span><h1>系统学习</h1><p>按等级排好的语法路线和主题词汇单元，每个知识点都配有练习题。</p></div>
<div class="right"><div class="seg"><a>A1</a><a>A2</a><a>B1</a><a class="on">B2</a><a>C1</a></div></div></div>
<div class="cont"><div><span class="hand">Reprendre la leçon</span><h3>Le subjonctif après « bien que »</h3><p>B2 语法 · 第 2 单元第 5 课 · 已学 12 分钟 · 配套练习 6 / 10</p></div><a class="btn">{ic('play',12)} 继续学习</a></div>
<div class="lay">
  <section><div class="sec-title" style="margin-bottom:14px"><span class="hand" style="color:var(--sage)">Grammaire</span><h2 style="font-size:20px">B2 语法路线</h2><a class="more">共 19 个单元 {ic('chev',12)}</a></div>{ul}</section>
  <section><div class="sec-title" style="margin-bottom:14px"><span class="hand" style="color:var(--sage)">Vocabulaire</span><h2 style="font-size:20px">主题词汇</h2><a class="more">全部 12 个主题 {ic('chev',12)}</a></div>
    <div class="ths">{tg}</div>
  </section>
</div>
</main></div>''', mod='m-learn')

# ------------------------------------------------------------ 2 · 语法课
outline = [('1', '什么时候用虚拟式', 'done'), ('2', '规则变位', 'done'), ('3', '不规则动词', 'done'), ('4', '意愿与情感', 'done'),
           ('5', '让步：bien que, quoique', 'on'), ('6', '目的：pour que, afin que', ''), ('7', '虚拟式 vs. 直陈式', ''), ('8', '单元测验', '')]
ol = ''.join(f'<a class="{st if st=="on" else ""}">{ic("check",14) if st=="done" else (ic("play",11) if st=="on" else "<i class=o></i>")}<span>{n}. {t}</span></a>' for n, t, st in outline)
learn2 = page('系统学习 · 语法课', topnav('learn') + f'''<div class="shell">
<style>
.ol{{width:256px;flex-shrink:0;border-right:1px solid var(--line);padding:26px 22px;background:#fffdfbcc}}
.ol .back{{font-size:11.5px;color:var(--muted);display:flex;gap:6px;align-items:center}}
.ol .unit{{margin:18px 0 18px;padding:16px;border-radius:14px;background:var(--sage-soft)}}
.ol .unit .hand{{font-size:15px;color:var(--sage)}}
.ol .unit b{{display:block;font-family:var(--serif-zh);font-size:18px;color:#33402f;margin:4px 0 10px}}
.ol .unit small{{font-size:11px;color:#6a7466}}
.ol a{{display:flex;align-items:center;gap:10px;padding:10px 10px;border-radius:9px;font-size:12.5px;color:#7a7076}}
.ol a svg{{color:var(--sage)}}
.ol a i.o{{width:14px;height:14px;border-radius:50%;border:1.5px solid #d5dccf}}
.ol a.on{{background:#fff;border:1px solid #d6e0cf;color:#33402f;box-shadow:0 4px 14px #5f77590f}}
.les{{flex:1;padding:30px 54px 0;overflow:hidden;display:grid;grid-template-columns:1fr 290px;gap:44px}}
.les .k{{display:flex;gap:8px;align-items:center;margin-bottom:12px}}
.les h1{{font:400 38px/1.25 var(--serif-fr);color:#2f2630}}
.les .zh{{font-family:var(--serif-zh);font-size:18px;color:#5f6e5a;margin:6px 0 18px}}
.les .lead{{font-size:14px;line-height:2;color:#4c4049;padding:16px 20px;border-left:3px solid var(--sage);background:#f6f8f3;border-radius:0 12px 12px 0}}
.les h2{{display:flex;align-items:center;gap:10px;font-family:var(--serif-zh);font-size:19px;font-weight:600;color:#33262f;margin:24px 0 12px}}
.les h2 span{{font-family:var(--hand);font-size:16px;color:var(--sage)}}
table{{width:100%;border-collapse:collapse;font-size:13px}}
th{{text-align:left;font-weight:500;font-size:11px;color:var(--faint);padding:8px 14px;border-bottom:1px solid var(--line)}}
td{{padding:11px 14px;border-bottom:1px solid #f1ebe9;color:#4c4049}}
td.fr{{font-family:var(--serif-fr);font-size:15px;color:#2f2630}}
td.fr b{{color:var(--sage)}}
.exs{{display:flex;flex-direction:column;gap:10px}}
.ex{{display:flex;gap:14px;align-items:flex-start;padding:14px 16px;border-radius:12px;border:1px solid var(--line);background:#fffdfb}}
.ex .pl{{width:30px;height:30px;border-radius:50%;background:var(--sage-soft);color:var(--sage);display:grid;place-items:center;flex-shrink:0}}
.ex p{{font:16px/1.6 var(--serif-fr);color:#2f2630}}
.ex p b{{color:var(--sage);border-bottom:2px solid #c6d6bd}}
.ex small{{display:block;font-size:12px;color:var(--muted);margin-top:3px}}
.side{{display:flex;flex-direction:column;gap:14px}}
.side .card{{padding:18px 20px}}
.side .hand{{font-size:16px;color:var(--sage)}}
.side ul{{list-style:none;margin-top:10px;display:flex;flex-direction:column;gap:9px;font-size:12.5px;color:#4c4049;line-height:1.7}}
.side li{{display:flex;gap:8px}}
.side li:before{{content:'';width:6px;height:6px;border-radius:50%;background:var(--sage);margin-top:8px;flex-shrink:0}}
.go{{background:var(--sage)!important;color:#fff;border:0!important}}
.go .hand{{color:#e7f0df!important}}
.go b{{display:block;font-family:var(--serif-zh);font-size:19px;margin:6px 0 4px}}
.go small{{font-size:11.5px;color:#dfe8d9}}
.go .btn{{background:#fff;color:var(--sage);margin-top:14px;width:100%;justify-content:center}}
.warn{{background:#fbf3e6!important;border-color:#f0e0bf!important}}
.warn .hand{{color:var(--amber)!important}}
.warn p{{font-size:12.5px;line-height:1.8;color:#6b5733;margin-top:8px}}
.warn p s{{color:#b46a5f}}
</style>
<aside class="ol"><a class="back" style="padding:0">{ic('chevl',13)} 返回 B2 语法路线</a>
<div class="unit"><span class="hand">Unité 02</span><b>虚拟式</b><small>8 课 · 已完成 4 课</small><div class="bar" style="margin-top:10px;background:#fff"><span style="width:55%;background:var(--sage)"></span></div></div>{ol}</aside>
<article class="les"><div>
  <div class="k"><span class="chip sage">B2 · 第 5 课</span><span class="chip line">{ic('clock',11)} 约 15 分钟</span><span class="chip line">{ic('volume',11)} 例句均有真人朗读</span></div>
  <h1>Le subjonctif après « bien que »</h1>
  <div class="zh">让步从句：尽管……，虽然……</div>
  <p class="lead"><b>bien que</b>、<b>quoique</b>、<b>encore que</b> 引导的让步从句，动词一律用<b>虚拟式</b>。说话人承认一个事实，但认为它并不妨碍主句的结果。</p>
  <h2><span>1</span>常见让步连词</h2>
  <table><tr><th>连接词</th><th>语域</th><th>例句</th></tr>
  <tr><td class="fr"><b>bien que</b></td><td>通用</td><td class="fr">Bien qu’il <b>pleuve</b>, nous sortons.</td></tr>
  <tr><td class="fr"><b>quoique</b></td><td>书面</td><td class="fr">Quoiqu’elle <b>soit</b> jeune, elle dirige l’équipe.</td></tr>
  <tr><td class="fr"><b>encore que</b></td><td>正式 · 补充保留</td><td class="fr">C’est utile, encore que ce <b>soit</b> coûteux.</td></tr></table>
  <h2><span>2</span>听一听，跟读</h2>
  <div class="exs">
    <div class="ex"><span class="pl">{ic('play',11)}</span><div><p>Bien que les terrasses <b>soient</b> pleines, le service reste rapide.</p><small>尽管露天座坐满了，上菜依然很快。</small></div></div>
    <div class="ex"><span class="pl">{ic('play',11)}</span><div><p>Quoiqu’il <b>ait</b> beaucoup révisé, il redoute l’épreuve orale.</p><small>虽然他复习了很多，仍然害怕口试。（过去虚拟式）</small></div></div>
  </div>
</div>
<aside class="side">
  <div class="card"><span class="hand">À retenir</span><ul><li>bien que / quoique + 虚拟式</li><li>主从句主语相同时，可以省略为 bien que + 形容词：<i>bien que fatiguée</i></li><li>动作已完成用过去虚拟式 avoir / être + 过去分词</li></ul></div>
  <div class="card warn"><span class="hand">Erreur fréquente</span><p><s>Bien qu’il est tard</s><br>→ Bien qu’il <b>soit</b> tard<br>考试写作中最常被扣分的语法错误之一。</p></div>
  <div class="card go"><span class="hand">Exercices</span><b>配套练习 · 10 题</b><small>填空 · 选择 · 句型转换 · 约 8 分钟</small><a class="btn">开始练习 {ic('arrow',13)}</a></div>
  <div class="card" style="display:flex;gap:10px;align-items:center;font-size:12px;color:var(--muted)">{ic('note',15)} 我的笔记 2 条 <span style="margin-left:auto">{ic('chev',13)}</span></div>
</aside></article></div>''', mod='m-learn')

# ------------------------------------------------------------ 3 · 配套练习（专注模式）
qnav = ''.join(f'<span class="{c}">{i}</span>' for i, c in enumerate(['ok', 'ok', 'bad', 'ok', 'cur', '', '', '', '', ''], 1))
learn3 = page('系统学习 · 配套练习', f'''
<style>
body{{background:#fff}}
.pbar{{height:60px;display:flex;align-items:center;gap:18px;padding:0 28px;border-bottom:1px solid #eee}}
.pbar img{{width:36px;height:36px}}
.pbar .t{{font-size:13px;color:#4d3a2b;font-weight:600}}
.pbar .t small{{font:italic 11px var(--serif-fr);color:var(--sage);font-weight:400;margin-left:10px;padding-left:10px;border-left:1px solid #e6e1d8}}
.pbar .prog{{flex:1;max-width:420px;margin:0 auto;display:flex;align-items:center;gap:12px;font-size:11px;color:var(--muted)}}
.pbar .prog .bar{{flex:1}}
.pbar .r{{display:flex;gap:10px;align-items:center;font-size:12px;color:var(--muted)}}
.wrap{{display:grid;grid-template-columns:1fr 380px;height:780px}}
.q{{padding:42px 90px 0 110px;border-right:1px solid #eee}}
.q .meta{{display:flex;gap:10px;align-items:center;font-size:11px;color:var(--faint)}}
.q .meta b{{width:30px;height:30px;border:1px solid #9baebe;color:#444;display:grid;place-items:center;font-size:15px;font-weight:500}}
.q h3{{font-size:13px;color:var(--muted);font-weight:400;margin:22px 0 10px}}
.q .sent{{font:400 27px/1.8 var(--serif-fr);color:#262626}}
.q .blank{{display:inline-flex;align-items:center;min-width:150px;height:44px;border-bottom:2px solid var(--sage);color:var(--sage);padding:0 10px;font-style:italic;vertical-align:baseline;background:#f4f8f1;border-radius:6px 6px 0 0}}
.q .hint{{font-size:12px;color:var(--muted);margin-top:6px}}
.kb{{display:flex;gap:8px;margin-top:28px}}
.kb span{{width:40px;height:40px;border-radius:10px;border:1px solid #e3e3e3;display:grid;place-items:center;font:16px var(--serif-fr);color:#555}}
.fb{{margin-top:34px;border:1px solid #d5e2cf;background:#f8fbf6;border-radius:14px;padding:20px 22px}}
.fb .h{{display:flex;align-items:center;gap:8px;color:#4f6b47;font-size:14px;font-weight:600}}
.fb .h i{{width:24px;height:24px;border-radius:50%;background:var(--sage);color:#fff;display:grid;place-items:center}}
.fb p{{font-size:13px;line-height:1.95;color:#56604f;margin-top:10px}}
.fb p b{{font-family:var(--serif-fr);color:#2f3b2b}}
.fb .lnk{{display:flex;gap:8px;margin-top:12px}}
.prev{{margin-top:22px;padding:16px 20px;border-radius:14px;border:1px dashed #e2c9c7;background:#fdf8f7}}
.prev small{{font-size:11px;color:#b07c76}}
.prev p{{font:15px/1.7 var(--serif-fr);color:#4d3a3a;margin-top:6px}}
.prev p s{{color:#c0817c}}
.prev p b{{color:var(--sage)}}
.sd{{padding:30px 30px;background:#fcfbf9}}
.sd .hand{{font-size:17px;color:var(--sage)}}
.sd .grid{{display:grid;grid-template-columns:repeat(5,1fr);gap:8px;margin:14px 0 24px}}
.sd .grid span{{height:40px;border-radius:9px;display:grid;place-items:center;font-size:13px;color:#aaa;border:1px solid #eee;background:#fff}}
.sd .grid .ok{{background:#eef5ea;color:var(--sage);border-color:#dbe7d4}}
.sd .grid .bad{{background:#fbefee;color:#b46a5f;border-color:#f1d8d5}}
.sd .grid .cur{{border:1.5px solid var(--sage);color:var(--sage);font-weight:600}}
.sd .types{{display:flex;flex-direction:column;gap:10px;font-size:12px;color:#6c5e67}}
.sd .types div{{display:flex;justify-content:space-between}}
.sd .rule{{margin-top:24px;padding:16px 18px;border-radius:14px;background:#fff;border:1px solid #eee}}
.sd .rule p{{font-size:12px;line-height:1.85;color:#5c5257;margin-top:6px}}
.foot{{position:absolute;left:0;right:380px;bottom:0;height:76px;border-top:1px solid #eee;display:flex;align-items:center;gap:12px;padding:0 110px;background:#fff}}
.foot .btn.dark{{margin-left:auto;background:var(--sage)}}
</style>
<div class="pbar m-learn"><img src="../assets/hutao-logo.png" alt=""><span class="t">胡桃法语<small>Exercices · bien que + subjonctif</small></span>
<div class="prog">5 / 10<div class="bar"><span style="width:50%;background:var(--sage)"></span></div>正确 3</div>
<div class="r">{ic('clock',14)} 04:18 <span class="iconbtn">{ic('x',14)}</span></div></div>
<div class="wrap">
<section class="q">
  <div class="meta"><b>5</b>动词变位填空 · 让步从句</div>
  <h3>用括号中动词的正确形式填空：</h3>
  <div class="sent">Bien que le musée <span class="blank">soit</span> gratuit le dimanche, peu de touristes le savent. <span style="color:var(--faint);font-size:18px">(être)</span></div>
  <div class="kb"><span>é</span><span>è</span><span>ê</span><span>à</span><span>ç</span><span>ô</span><span>î</span><span>œ</span></div>
  <div class="fb"><div class="h"><i>{ic('check',13)}</i>回答正确</div>
  <p><b>bien que</b> 后接虚拟式。être 的虚拟式现在时：que je sois, que tu sois, qu’il <b>soit</b>…<br>主句 « peu de touristes le savent » 用直陈式，表达真实情况。</p>
  <div class="lnk"><span class="chip sage">{ic('grammar',11)} 回看第 5 课 · 让步连词</span><span class="chip line">{ic('bookmark',11)} 收藏本题</span><span class="chip line">{ic('note',11)} 写笔记</span></div></div>
  <div class="prev"><small>第 3 题 · 你的错误</small><p>Quoiqu’elle <s>a</s> → <b>ait</b> beaucoup voyagé, elle n’a jamais vu la mer.</p></div>
</section>
<aside class="sd"><span class="hand">Progression</span><div class="grid">{qnav}</div>
<div class="types"><div><span>动词变位填空</span><span>4 题</span></div><div><span>选择正确连词</span><span>3 题</span></div><div><span>句型转换</span><span>2 题</span></div><div><span>翻译：中 → 法</span><span>1 题</span></div></div>
<div class="rule"><span class="hand">Rappel</span><p>正确率 ≥ 80% 解锁第 6 课「目的从句」。答错的题会自动进入「我的错题」，三天后提醒复习。</p></div></aside>
</div>
<div class="foot"><a class="btn ghost sm">{ic('chevl',12)} 上一题</a><span style="font-size:11px;color:var(--faint)">Enter 提交 · → 下一题</span><a class="btn dark">下一题 {ic('arrow',13)}</a></div>
''', mod='m-learn')

# ------------------------------------------------------------ 4 · 主题词汇
words = [
    ('la transition écologique', 'n.f.', '生态转型', 'mastered'), ('le réchauffement climatique', 'n.m.', '全球变暖', 'mastered'),
    ('la biodiversité', 'n.f.', '生物多样性', 'learning'), ('l’empreinte carbone', 'n.f.', '碳足迹', 'learning'),
    ('recycler', 'v.t.', '回收利用', 'mastered'), ('le gaspillage', 'n.m.', '浪费', 'new'),
    ('durable', 'adj.', '可持续的', 'learning'), ('la sobriété énergétique', 'n.f.', '能源节制', 'new'),
    ('sensibiliser qqn à qqch', 'loc.', '提高某人对……的意识', 'new'),
]
st = {'mastered': ('已掌握', 'sage'), 'learning': ('学习中', 'amber'), 'new': ('新词', 'line')}
rows = ''.join(f'<tr><td class="w">{w}</td><td class="p">{p}</td><td>{m}</td><td><span class="chip {st[s][1]}">{st[s][0]}</span></td><td class="ic">{ic("volume",14)}</td></tr>' for w, p, m, s in words)
learn4 = page('系统学习 · 主题词汇', topnav('learn') + '<div class="shell">' + rail([
    ('h', 'Vocabulaire', '主题词汇'),
    ('a', 'cards', '教育与成长', '96', False), ('a', 'cards', '职业职场', '120', False), ('a', 'cards', '生态环境', '108', True),
    ('a', 'cards', '科技与社会', '88', False), ('a', 'cards', '健康与科学', '92', False), ('a', 'cards', '城市生活', '74', False),
    ('a', 'cards', '语言与文化', '81', False), ('sep',), ('h', 'Révision', '复习'),
    ('a', 'repeat', '今日待复习', '20', False), ('a', 'note', '我的生词本', '312', False),
], '<span class="hand">Astuce</span>词汇来自 DELF / DALF 真题文章的高频词，学完可直接去题库读原文。') + f'''
<main class="main">
<style>
.hero{{display:flex;align-items:flex-end;gap:24px;padding:24px 28px;border-radius:20px;background:linear-gradient(115deg,#dde9e2,#eef3ea 55%,#f6f3ea);margin-bottom:20px;position:relative;overflow:hidden}}
.hero .hand.big{{font-size:40px;color:#4f7a6a;line-height:1}}
.hero h1{{font-family:var(--serif-zh);font-size:24px;color:#2f3b33;margin:8px 0 6px;font-weight:600}}
.hero p{{font-size:12px;color:#5f6f66}}
.hero .st{{margin-left:auto;display:flex;gap:28px}}
.hero .st div{{text-align:center}}
.hero .st b{{display:block;font-family:var(--hand);font-size:28px;color:#4f7a6a}}
.hero .st small{{font-size:11px;color:#6f7d74}}
.lay{{display:grid;grid-template-columns:1fr 380px;gap:24px}}
table{{width:100%;border-collapse:collapse}}
th{{text-align:left;font-weight:500;font-size:11px;color:var(--faint);padding:8px 12px;border-bottom:1px solid var(--line)}}
td{{padding:10px 12px;border-bottom:1px solid #f1ebe9;font-size:12.5px;color:#5a4d55}}
td.w{{font:16px var(--serif-fr);color:#2f2630}}
td.p{{font:italic 12px var(--serif-fr);color:var(--faint)}}
td.ic{{color:var(--faint)}}
.fc{{border-radius:22px;padding:30px 28px;background:#fffdfb;border:1px solid var(--line);box-shadow:0 18px 40px #4f7a6a14;text-align:center;position:relative}}
.fc:before,.fc:after{{content:'';position:absolute;left:16px;right:16px;height:12px;border-radius:0 0 18px 18px;border:1px solid var(--line);border-top:0;background:#fbf8f4}}
.fc:before{{bottom:-12px}}.fc:after{{bottom:-23px;left:30px;right:30px;z-index:-1}}
.fc small{{font-size:11px;color:var(--faint)}}
.fc .w{{font-family:var(--hand);font-size:36px;color:#3f5f53;margin:20px 0 4px}}
.fc .ph{{font-size:12px;color:var(--faint)}}
.fc .ex{{font:italic 14px/1.8 var(--serif-fr);color:#5f6f66;margin:18px 0;padding:12px;border-radius:12px;background:#f3f7f2}}
.fc .flip{{font-size:11px;color:var(--faint);display:flex;gap:6px;justify-content:center;align-items:center}}
.rate{{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-top:36px}}
.rate span{{height:42px;border-radius:12px;display:grid;place-items:center;font-size:12px;border:1px solid var(--line);background:#fff;color:#6c5e67}}
.rate span:nth-child(1){{color:#b46a5f;background:#fbf1ef;border-color:#f1d8d5}}
.rate span:nth-child(3){{color:var(--sage);background:#eef5ea;border-color:#dbe7d4}}
</style>
<div class="crumb">系统学习 {ic('chev',11)} 主题词汇 {ic('chev',11)} <span>生态环境</span></div>
<div class="hero"><div><span class="hand big">Écologie</span><h1>生态环境 · 主题词汇</h1><p>108 词 · 12 个场景 · 摘自 B2 / C1 真题中的环保与能源话题</p></div>
<div class="st"><div><b>55%</b><small>已掌握</small></div><div><b>18</b><small>学习中</small></div><div><b>6</b><small>组配套练习</small></div></div></div>
<div class="tabs"><a class="on">词表</a><a>记忆卡片</a><a>配套练习</a><a>单元测验</a><a>真题原文出处</a></div>
<div class="lay">
<div><table><tr><th>单词 / 表达</th><th>词性</th><th>释义</th><th>状态</th><th></th></tr>{rows}</table></div>
<div><div class="fc"><small>记忆卡片 · 14 / 108</small><div class="w">l’empreinte carbone</div><div class="ph">[ɑ̃pʁɛ̃t kaʁbɔn] n.f.</div>
<div class="ex">« Réduire son empreinte carbone commence dans l’assiette. »</div>
<div class="flip">{ic('repeat',13)} 点击翻面查看释义</div></div>
<div class="rate"><span>不认识</span><span>模糊</span><span>认识</span></div></div>
</div>
</main></div>''', mod='m-learn')

PAGES = {
    '11-learn-overview': learn1,
    '12-learn-grammar-lesson': learn2,
    '13-learn-grammar-practice': learn3,
    '14-learn-theme-vocabulary': learn4,
}
