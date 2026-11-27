from common import ic
from fcommon import nav, head, tabs, fpage, hb

SEG = f'<span class="seg"><a>A1</a><a>A2</a><a>B1</a><a class="on">B2</a><a>C1</a>{hb()}</span>'

# ------------------------------------------------------------ 1 · 学习总览
units = [('01', 'Les temps du passé', '过去时态的配合', '复合过去时 · 未完成过去时 · 愈过去时', 100),
         ('02', 'Le subjonctif', '虚拟式', '情感、意愿、让步与目的', 60),
         ('03', 'Les pronoms relatifs composés', '复合关系代词', 'lequel · auquel · duquel · dont', 0),
         ('04', 'Le discours rapporté', '间接引语', '时态转换 · 时间副词变化', 0),
         ('05', 'La cause et la conséquence', '原因与结果', 'puisque · faute de · si bien que', 0)]
ul = ''
for n, fr, zh, sub, p in units:
    st = '<span class="pill mint">' + ic('check', 11) + ' 已完成</span>' if p == 100 else ('<span class="pill butter">学习中</span>' if p else '<span class="pill ghost">8 课' + hb('#cfc6bb') + '</span>')
    ul += f'''<div class="box u">{hb('var(--orange)' if 0 < p < 100 else None)}<span class="n num">{n}</span><div class="ut"><div class="it" style="font-size:13px;color:var(--green)">{fr}</div>
<b class="zh">{zh}</b> <small>{sub}</small><div class="bar" style="margin-top:9px;width:70%;--bcol:var(--green)"><span style="width:{p}%"></span></div></div>{st}</div>'''
themes = [('Éducation', '教育与成长', 96, 72, 'mint'), ('Travail', '职业职场', 120, 40, 'butter'), ('Écologie', '生态环境', 108, 55, 'mint'),
          ('Technologie', '科技与社会', 88, 18, 'sky'), ('Santé', '健康与科学', 92, 0, 'blush'), ('Ville', '城市生活', 74, 9, 'lav')]
tg = ''.join(f'<div class="flat th" style="background:var(--{c})"><span class="fr" style="font-size:21px">{fr}</span><b class="zh">{zh}</b><small>{n} 词 · 6 组练习</small><span class="pc num">{p}%</span></div>' for fr, zh, n, p, c in themes)
learn1 = fpage('系统学习 · 总览', nav('learn') + head('Apprendre pas à pas', '系统学习', '按等级排好的语法路线和主题词汇，每个知识点都配有练习。', SEG) + f'''
<div class="wrap">
<div class="flat cont"><div><span class="fr" style="color:var(--green);font-size:16px">Reprendre la leçon</span><div class="it" style="font-size:22px;margin:2px 0">Le subjonctif après « bien que »</div><small>B2 语法 · 第 2 单元第 5 课 · 已学 12 分钟 · 配套练习 <span class="num">6 / 10</span></small></div><a class="btn solid">{ic('play',12)} 继续学习</a></div>
<div class="lay"><section><div class="secth"><span class="label">Grammaire</span><h2 class="t">B2 语法路线</h2><span class="more">共 19 个单元 ›</span></div>{ul}</section>
<section><div class="secth"><span class="label">Vocabulaire</span><h2 class="t">主题词汇</h2><span class="more">全部 12 个主题 ›</span></div><div class="ths">{tg}</div></section></div></div>''', 'm-learn', '''
.cont{display:flex;align-items:center;gap:20px;padding:18px 26px;background:var(--mint);margin-bottom:22px}
.cont small{font-size:12px;color:var(--ink2)}.cont .btn{margin-left:auto}
.lay{display:grid;grid-template-columns:1fr 470px;gap:30px}
.u{display:flex;align-items:center;gap:18px;padding:16px 20px;margin-bottom:12px}
.u .n{font-size:26px;width:38px}.u .ut{flex:1}.u b{font-size:18px}.u small{font-size:12px;color:var(--soft)}
.ths{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.th{padding:18px 20px;position:relative;min-height:132px}.th b{display:block;font-size:16px;margin-top:2px}.th small{font-size:11.5px;color:var(--ink2)}
.th .pc{position:absolute;right:16px;bottom:12px;font-size:20px}''')

# ------------------------------------------------------------ 2 · 语法课
ol = [('1', '什么时候用虚拟式', 'd'), ('2', '规则变位', 'd'), ('3', '不规则动词', 'd'), ('4', '意愿与情感', 'd'), ('5', '让步：bien que, quoique', 'on'),
      ('6', '目的：pour que, afin que', ''), ('7', '虚拟式还是直陈式', ''), ('8', '单元测验', '')]
oh = ''.join(f'<a class="{s}">{ic("check",13) if s=="d" else "<i></i>"}<span>{n}. {t}</span>{hb("var(--orange)") if s=="on" else ""}</a>' for n, t, s in ol)
learn2 = fpage('系统学习 · 语法课', nav('learn') + f'''
<div class="g"><aside class="ol"><div class="crumb">系统学习 › B2 语法路线</div><span class="fr" style="color:var(--green);font-size:17px">Unité 02</span><h2 class="t">虚拟式</h2><small>8 课 · 已完成 4 课</small>
<div class="bar" style="margin:10px 0 16px;--bcol:var(--green)"><span style="width:55%"></span></div>{oh}</aside>
<article class="les"><div style="display:flex;gap:8px"><span class="pill mint">B2 · 第 5 课</span><span class="pill ghost">{ic('clock',11)} 约 15 分钟{hb('#cfc6bb')}</span></div>
<h1 class="it">Le subjonctif après « bien que »</h1><div class="zh sub">让步从句：尽管……，虽然……</div>
<p class="lead"><b>bien que</b>、<b>quoique</b>、<b>encore que</b> 引导的让步从句，动词一律用<span class="uline" style="--uc:var(--green)">虚拟式</span>。说话人承认一个事实，但认为它并不妨碍主句的结果。</p>
<div class="secth" style="margin-top:22px"><span class="label">1</span><h2 class="t" style="font-size:18px">常见让步连词</h2></div>
<table><tr><th>连接词</th><th>语域</th><th>例句</th></tr><tr><td class="it fx"><b>bien que</b></td><td>通用</td><td class="fx">Bien qu’il <b>pleuve</b>, nous sortons.</td></tr>
<tr><td class="it fx"><b>quoique</b></td><td>书面</td><td class="fx">Quoiqu’elle <b>soit</b> jeune, elle dirige l’équipe.</td></tr><tr><td class="it fx"><b>encore que</b></td><td>正式</td><td class="fx">C’est utile, encore que ce <b>soit</b> coûteux.</td></tr></table>
<div class="secth" style="margin-top:22px"><span class="label">2</span><h2 class="t" style="font-size:18px">听一听，跟读</h2></div>
<div class="ex box">{hb('#cfc6bb')}<span class="pl">{ic('play',11)}</span><div><p>Bien que les terrasses <b>soient</b> pleines, le service reste rapide.</p><small>尽管露天座坐满了，上菜依然很快。</small></div></div>
<div class="ex box">{hb('#cfc6bb')}<span class="pl">{ic('play',11)}</span><div><p>Quoiqu’il <b>ait</b> beaucoup révisé, il redoute l’épreuve orale.</p><small>虽然他复习了很多，仍然害怕口试。（过去虚拟式）</small></div></div></article>
<aside class="sd"><div class="flat c1" style="background:var(--butter)"><span class="fr" style="color:#7a5a18">À retenir</span><ul><li>bien que / quoique + 虚拟式</li><li>主语相同时可省略为 <i>bien que fatiguée</i></li><li>动作已完成用过去虚拟式</li></ul></div>
<div class="flat c1" style="background:var(--blush)"><span class="fr" style="color:var(--red)">Erreur fréquente</span><p><s>Bien qu’il est tard</s><br>→ Bien qu’il <b>soit</b> tard</p><small>写作里最常被扣分的语法错误之一。</small></div>
<div class="flat c1" style="background:var(--green);color:var(--cream)"><span class="fr" style="color:#cfe6d6">Exercices</span><b class="zh" style="display:block;font-size:20px;margin:4px 0">配套练习 · <span style="font-family:var(--fr)">10</span> 题</b><small style="color:#d8ebde">填空 · 选择 · 句型转换 · 约 8 分钟</small><a class="btn" style="background:var(--cream);color:var(--green);margin-top:12px;width:100%;justify-content:center">开始练习 {ic('arrow',13)}</a></div></aside></div>''', 'm-learn', '''
.g{display:grid;grid-template-columns:250px 1fr 290px;gap:40px;padding:26px 64px 0;height:828px}
.ol small{font-size:11.5px;color:var(--soft)}
.ol a{display:flex;align-items:center;gap:10px;padding:9px 12px;border-radius:12px;font-size:13px;color:var(--ink2);position:relative;font-family:var(--zh)}
.ol a svg{color:var(--green)}.ol a i{width:13px;height:13px;border-radius:50%;border:1.5px solid #cfc6bb}
.ol a.on{color:var(--navy);background:var(--paper)}.ol a.on i{background:var(--orange);border-color:var(--orange)}
.les h1{font-size:36px;font-weight:400;margin:14px 0 4px;line-height:1.25}
.les .sub{font-size:18px;color:var(--green);margin-bottom:16px}
.lead{font-size:14px;line-height:2;color:var(--ink2);padding:14px 18px;background:var(--mint);border-radius:14px}
.fx{font-family:var(--serif);font-size:15px;color:var(--navy)}.fx b{color:var(--green)}
.ex{display:flex;gap:14px;align-items:flex-start;padding:13px 16px;margin-bottom:10px}
.ex .pl{width:30px;height:30px;border-radius:50%;background:var(--mint);color:var(--green);display:grid;place-items:center;flex-shrink:0}
.ex p{font:16px/1.6 var(--serif)}.ex p b{color:var(--green)}.ex small{font-size:12px;color:var(--soft)}
.sd{display:flex;flex-direction:column;gap:14px}
.c1{padding:18px 20px}.c1 .fr{font-size:17px}
.c1 ul{list-style:none;margin-top:8px;display:flex;flex-direction:column;gap:7px;font-size:12.5px;line-height:1.7;color:var(--ink2)}
.c1 li:before{content:'· ';color:var(--orange);font-weight:700}
.c1 p{font:15px/1.7 var(--serif);margin:6px 0}.c1 p s{color:var(--red)}.c1 small{font-size:11.5px;color:var(--ink2)}''')

# ------------------------------------------------------------ 3 · 配套练习（专注模式）
grid = ''.join(f'<span class="{c}">{i}</span>' for i, c in enumerate(['ok', 'ok', 'bad', 'ok', 'cur', '', '', '', '', ''], 1))
learn3 = fpage('系统学习 · 配套练习', f'''
<header class="pbar"><img src="../assets/hutao-logo.png" alt=""><span class="zh" style="font-size:16px;font-weight:700;color:#7a4b2e">胡桃法语</span><span class="fr" style="color:var(--green);font-size:15px;margin-left:6px">Exercices · bien que + subjonctif</span>
<div class="pg"><span class="num">5 / 10</span><div class="bar" style="flex:1;--bcol:var(--green)"><span style="width:50%"></span></div><span>正确 <b class="num">3</b></span></div>
<span class="tm">{ic('clock',14)} <b class="num" style="color:var(--navy)">04:18</b></span><span class="me x">{ic('x',14)}{hb()}</span></header>
<div class="g"><section class="q"><div class="meta"><b class="num">5</b> 动词变位填空 · 让步从句</div><h3 class="zh">用括号中动词的正确形式填空：</h3>
<div class="sent">Bien que le musée <span class="blank">soit</span> gratuit le dimanche, peu de touristes le savent. <span style="color:var(--faint);font-size:18px">(être)</span></div>
<div class="kb">{''.join(f'<span>{c}{hb("#cfc6bb")}</span>' for c in 'éèêàçôîœ')}</div>
<div class="flat fb"><div class="h"><i>{ic('check',13)}</i>回答正确</div><p><b>bien que</b> 后接虚拟式。être 的虚拟式现在时：que je sois, que tu sois, qu’il <b>soit</b>…<br>主句 « peu de touristes le savent » 用直陈式，表达真实情况。</p>
<div style="display:flex;gap:8px;margin-top:10px"><span class="pill" style="background:var(--paper);color:var(--green)">{ic('grammar',11)} 回看第 5 课</span><span class="pill" style="background:var(--paper)">{ic('bookmark',11)} 收藏本题</span></div></div>
<div class="box prev">{hb('#e9a587')}<small>第 3 题 · 你的错误</small><p>Quoiqu’elle <s>a</s> → <b>ait</b> beaucoup voyagé, elle n’a jamais vu la mer.</p></div></section>
<aside class="sd"><span class="fr" style="color:var(--green);font-size:18px">Progression</span><div class="gr">{grid}</div>
<div class="ty"><div>动词变位填空<b class="num">4</b></div><div>选择正确连词<b class="num">3</b></div><div>句型转换<b class="num">2</b></div><div>翻译：中 → 法<b class="num">1</b></div></div>
<div class="flat" style="background:var(--butter);padding:16px 18px;margin-top:22px"><span class="fr" style="color:#7a5a18">Rappel</span><p style="font-size:12.5px;line-height:1.8;color:var(--ink2);margin-top:4px">正确率达到 80% 解锁第 6 课「目的从句」。答错的题自动进入「我的错题」，三天后提醒复习。</p></div></aside></div>
<div class="foot"><a class="btn line sm">{ic('chevl',12)} 上一题{hb()}</a><span style="font-size:12px;color:var(--faint)">Enter 提交 · → 下一题</span><a class="btn solid" style="margin-left:auto;background:var(--green)">下一题 {ic('arrow',13)}</a></div>''', 'm-learn', '''
.pbar{height:64px;display:flex;align-items:center;gap:10px;padding:0 32px;background:var(--peach)}
.pbar img{width:36px}.pbar .pg{flex:1;max-width:420px;margin:0 auto;display:flex;align-items:center;gap:12px;font-size:12px;color:var(--ink2)}
.pbar .tm{display:flex;gap:6px;align-items:center;font-size:13px;margin-right:12px}
.me{width:34px;height:34px;border-radius:50%;display:grid;place-items:center;position:relative;background:var(--paper)}
.g{display:grid;grid-template-columns:1fr 380px;height:760px}
.q{padding:40px 90px 0 110px}
.q .meta{display:flex;gap:10px;align-items:center;font-size:12px;color:var(--soft);font-family:var(--zh)}.q .meta b{font-size:26px}
.q h3{font-size:15px;color:var(--ink2);font-weight:400;margin:16px 0 8px}
.sent{font:27px/1.8 var(--serif)}
.blank{display:inline-block;min-width:150px;color:var(--green);font-style:italic;position:relative;text-align:center;border-bottom:2.5px solid var(--orange)}
.kb{display:flex;gap:8px;margin-top:24px}.kb span{width:40px;height:40px;border-radius:10px;display:grid;place-items:center;font:16px var(--serif);position:relative;background:var(--paper)}
.fb{margin-top:28px;background:var(--mint);padding:18px 22px}
.fb .h{display:flex;align-items:center;gap:8px;color:var(--green);font-family:var(--zh);font-size:16px;font-weight:700}
.fb .h i{width:24px;height:24px;border-radius:50%;background:var(--green);color:#fff;display:grid;place-items:center}
.fb p{font-size:13px;line-height:1.95;color:var(--ink2);margin-top:8px}.fb p b{font-family:var(--serif);color:var(--navy)}
.prev{margin-top:18px;padding:14px 18px}.prev small{font-size:11.5px;color:var(--red);font-family:var(--zh)}.prev p{font:15px/1.7 var(--serif);margin-top:4px}.prev s{color:var(--red)}.prev b{color:var(--green)}
.sd{padding:36px 40px;border-left:1.5px dashed var(--rule)}
.gr{display:grid;grid-template-columns:repeat(5,1fr);gap:8px;margin:14px 0 24px}
.gr span{height:40px;border-radius:10px;display:grid;place-items:center;font-family:var(--fr);font-weight:700;font-size:15px;color:var(--faint);background:var(--paper)}
.gr .ok{background:var(--mint);color:var(--green)}.gr .bad{background:var(--blush);color:var(--red)}.gr .cur{background:var(--orange);color:#fff}
.ty{display:flex;flex-direction:column;gap:10px;font-size:13px;color:var(--ink2);font-family:var(--zh)}.ty div{display:flex;justify-content:space-between}
.foot{position:absolute;left:0;right:380px;bottom:0;height:76px;display:flex;align-items:center;gap:14px;padding:0 110px;border-top:1.5px dashed var(--rule)}''')

# ------------------------------------------------------------ 4 · 主题词汇
words = [('la transition écologique', 'n.f.', '生态转型', 'm'), ('le réchauffement climatique', 'n.m.', '全球变暖', 'm'), ('la biodiversité', 'n.f.', '生物多样性', 'l'),
         ('l’empreinte carbone', 'n.f.', '碳足迹', 'l'), ('recycler', 'v.t.', '回收利用', 'm'), ('le gaspillage', 'n.m.', '浪费', 'n'),
         ('durable', 'adj.', '可持续的', 'l'), ('la sobriété énergétique', 'n.f.', '能源节制', 'n'), ('sensibiliser qqn à qqch', 'loc.', '提高某人对……的意识', 'n')]
pmap = {'m': '<span class="pill mint">已掌握</span>', 'l': '<span class="pill butter">学习中</span>', 'n': '<span class="pill blush">新词</span>'}
rows = ''.join(f'<tr><td class="w">{w}</td><td class="it" style="color:var(--soft)">{p}</td><td class="zh" style="font-size:14px;color:var(--navy)">{m}</td><td>{pmap[s]}</td><td>{ic("volume",14)}</td></tr>' for w, p, m, s in words)
learn4 = fpage('系统学习 · 主题词汇', nav('learn') + f'''
<div class="wrap" style="padding-top:24px"><div class="crumb">系统学习 › 主题词汇 › 生态环境</div>
<div class="flat hero"><div><span class="fr" style="font-size:46px;color:var(--green);line-height:1">Écologie</span><h1 class="zh">生态环境 · 主题词汇</h1><p>108 词 · 12 个场景 · 摘自 B2 / C1 真题里的环保与能源话题</p></div>
<div class="st"><div><b class="num">55%</b><small>已掌握</small></div><div><b class="num">18</b><small>学习中</small></div><div><b class="num">6</b><small>组配套练习</small></div></div></div></div>
{tabs(['词表', '记忆卡片', '配套练习', '单元测验', '真题原文出处'])}
<div class="wrap lay"><table><tr><th>单词 / 表达</th><th>词性</th><th>释义</th><th>状态</th><th></th></tr>{rows}</table>
<div><div class="box fc">{hb(None,'thick')}<small class="zh">记忆卡片 · <span class="num">14 / 108</span></small><div class="fr w">l’empreinte carbone</div><div style="font-size:12px;color:var(--soft)">[ɑ̃pʁɛ̃t kaʁbɔn] n.f.</div>
<div class="ex it">« Réduire son empreinte carbone commence dans l’assiette. »</div><small style="font-size:11.5px;color:var(--soft)">{ic('repeat',12)} 点击翻面看释义</small></div>
<div class="rate"><span style="background:var(--blush);color:var(--red)">不认识</span><span style="background:var(--butter);color:#7a5a18">模糊</span><span style="background:var(--mint);color:var(--green)">认识</span></div></div></div>''', 'm-learn', '''
.hero{display:flex;align-items:flex-end;gap:24px;padding:22px 28px;background:var(--mint);margin-bottom:20px}
.hero h1{font-family:var(--zh);font-size:24px;margin:8px 0 4px}.hero p{font-size:12.5px;color:var(--ink2)}
.hero .st{margin-left:auto;display:flex;gap:34px;text-align:center}.hero .st b{display:block;font-size:30px}.hero .st small{font-size:12px;color:var(--ink2);font-family:var(--zh)}
.lay{display:grid;grid-template-columns:1fr 380px;gap:30px}
td.w{font:16px var(--serif);color:var(--navy)}
.fc{padding:28px 26px;text-align:center}.fc .w{font-size:34px;color:var(--green);margin:18px 0 4px}
.fc .ex{font-size:14px;line-height:1.8;color:var(--ink2);margin:18px 0 12px;padding:12px;border-radius:12px;background:var(--mint)}
.rate{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-top:16px}.rate span{height:42px;border-radius:14px;display:grid;place-items:center;font-family:var(--zh);font-size:14px}''')

PAGES = {'f11-learn-overview': learn1, 'f12-learn-grammar-lesson': learn2, 'f13-learn-grammar-practice': learn3, 'f14-learn-theme-vocabulary': learn4}
