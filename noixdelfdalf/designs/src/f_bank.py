from common import ic
from fcommon import nav, head, tabs, fpage, hb

LIVE_CSS = '''
.lc{position:relative;border-radius:12px}
.lc .img{position:absolute;inset:6px;border-radius:8px;background:var(--img)}
.lc .tint{position:absolute;inset:6px;border-radius:8px;background:var(--tint)}
.lc .txt{position:absolute;left:6px;right:6px;bottom:6px;padding:18px 20px}
.lc b.fr{display:block;font-size:40px;line-height:1.05;color:var(--navy)}
.lc .it{font-size:15px;color:var(--navy)}
.lc em{font-style:normal;font-family:var(--fr);font-weight:700;color:var(--deep-orange)}
.soonc{position:relative;border-radius:14px;border:1px solid #e3ddd6;padding:18px 20px;background:repeating-linear-gradient(135deg,#f5f0ea 0 9px,#fbf8f3 9px 18px)}
.soonc b{display:block;font-family:var(--fr);font-weight:700;font-size:40px;color:#b9aeb4;line-height:1}
.soonc small{display:block;font-family:var(--zh);font-size:13px;color:#a59aa1;margin-top:10px}
.soonc .tag{position:absolute;right:14px;top:14px;font-family:var(--zh);font-size:12px;color:#9a8f96;background:#fbf8f3;border-radius:20px;padding:2px 10px}
'''

# ------------------------------------------------------------ 1 · 选择等级
def live(name, sub, img, tint, stats, prog, done, total):
    st = ''.join(f'<span>{a} <em>{b}</em></span>' for a, b in stats)
    return f'''<div class="lc" style="--img:{img};--tint:{tint}"><div class="img"></div><div class="tint"></div><div class="txt">
<b class="fr">{name}</b><div class="it">{sub}</div><div class="sts">{st}</div>
<div class="pr"><span class="zh">已练 <em>{done}</em> / {total}</span><div class="bar" style="flex:1;background:#ffffff90;--bcol:var(--deep-orange)"><span style="width:{prog}%"></span></div><a class="btn solid sm">进入 {ic('arrow',12)}</a></div></div>{hb('var(--orange)','thick')}</div>'''
bank1 = fpage('题库练习 · 选择等级', nav('bank') + head('Banque d’exercices', '题库练习', 'DELF / DALF 历年真题，按等级、题型和主题整理。收藏、错题和生词在各等级间同步。',
              f'<a class="btn line sm">{ic("rotate",13)} 错题回顾 <b class="num">23</b>{hb()}</a><a class="btn line sm">{ic("bookmark",13)} 我的收藏 <b class="num">14</b>{hb()}</a>') + f'''
<div class="wrap g">
{live('DELF B2', 'Le café au pied de l’Arc', 'url(../assets/arc-haze.png) 32% 60%/cover', '#fbe3bd80', [('长听力','17'),('短听力','17'),('阅读','34'),('写作','17'),('口语','228')], 15, 46, 313)}
{live('DALF C1', 'Brume sur la Seine', 'url(../assets/paris-haze.png) 70% 40%/cover', '#efe1f280', [('长听力','20'),('短听力','36'),('阅读','28'),('写作','28'),('口语','140')], 35, 88, 252)}
<div class="col"><div class="soonc"><b>A2</b><small>DELF A2 · 题库整理中</small><span class="tag">即将上线</span></div><div class="soonc"><b>B1</b><small>DELF B1 · 题库整理中</small><span class="tag">即将上线</span></div></div></div>
<div class="wrap low"><div class="box c">{hb()}<span class="label">Récemment</span><small class="zh" style="color:var(--soft);margin-left:6px">最近练习</small>
<div class="rec"><div><span class="pill lav">C1 阅读</span><b>Enseignants : le droit d’aimer</b><span class="num">3 / 11</span></div><div><span class="pill butter">B2 短听力</span><b>Le retour du troc ?</b><span class="num">8 / 10</span></div><div><span class="pill lav">C1 长听力</span><b>La nomophobie</b><span class="num">9 / 11</span></div></div></div>
<div class="box c">{hb()}<span class="label">Régularité</span><small class="zh" style="color:var(--soft);margin-left:6px">近 12 周刷题记录 · 共 <span class="num">134</span> 组</small>
<div class="hm">{''.join(f'<i style="background:{c}"></i>' for c in (['#efe8dd','#f6d6c2','#f0aa86','#e1653a','#efe8dd','#f6d6c2','#dbeadf','#f0aa86','#efe8dd','#e1653a','#f6d6c2','#efe8dd']*7)[:84])}</div></div></div>''', 'm-bank', LIVE_CSS + '''
.g{display:grid;grid-template-columns:1fr 1fr 300px;gap:20px;height:450px}
.g .lc .sts{display:grid;grid-template-columns:repeat(3,auto);justify-content:start;gap:4px 20px;margin-top:12px;font-family:var(--zh);font-size:13px;color:var(--navy)}
.g .lc .sts em{font-size:17px}
.g .lc .pr{display:flex;align-items:center;gap:12px;margin-top:14px;font-size:13px;color:var(--navy)}
.col{display:flex;flex-direction:column;gap:20px}.col .soonc{flex:1}
.low{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-top:20px}
.c{padding:16px 22px}
.rec div{display:flex;align-items:center;gap:12px;padding:12px 0;border-bottom:1px dashed var(--rule)}.rec div:last-child{border:0}.rec b{font:400 15px var(--serif)}.rec .num{margin-left:auto;font-size:16px}
.hm{display:grid;grid-template-columns:repeat(28,1fr);gap:4px;margin-top:12px}.hm i{aspect-ratio:1;border-radius:3px}''')

# ------------------------------------------------------------ 2 · DALF C1 题库
C1 = [('阅读', 'blush', 'Enseignants : le droit d’aimer', '教师也有表达关爱的权利', '教育与成长', '2021 年 10 月 · 法国场次', '11 题', 1),
      ('长听力', 'lav', 'La nomophobie', '离开手机的焦虑', '科技与社会', '2024 年 11 月 · 中国场次', '11 题 · 音频', 1),
      ('阅读', 'blush', 'Les fonctions du rêve', '梦的功能', '健康与科学', '2021 年 3 月 · 中国场次', '13 题', 0),
      ('短听力', 'sky', 'L’Espresso Book Machine', '一杯咖啡的时间，印一本书', '语言与文化', '2022 年 6 月 · 中国场次', '4 题 · 音频', 0),
      ('长听力', 'lav', 'Nos relations avec les robots', '我们与机器人的关系', '科技与社会', '2022 年 11 月 · 中国场次', '11 题 · 音频', 0),
      ('写作', 'butter', 'Le congé de paternité', '父亲也需要育儿假', '社会与生活', '2021 年 10 月 · 法国场次', '综合 + 议论', 0),
      ('口语', 'mint', 'Faut-il tout noter ?', '所有事物都需要被评分吗？', '社会与生活', '口语材料 1 · 第 36 题', '陈述 + 辩论', 1),
      ('短听力', 'sky', 'Apprendre le français au Petit Palais', '在小皇宫博物馆学法语', '语言与文化', '2021 年 6 月 · 中国场次', '3 题 · 音频', 0),
      ('口语', 'mint', 'Quel avenir pour l’industrie musicale ?', '音乐产业的未来在哪里？', '语言与文化', '口语材料 2 · 第 10 题', '陈述 + 辩论', 0)]
cards = ''.join(f'''<div class="box ex">{hb()}<div class="tp"><span class="pill {c}">{t}</span><span class="to">{tp}</span>{ic('bookmark',14,'margin-left:auto;color:var(--faint)')}</div><h3 class="it">{fr}</h3><p class="zh">{zh}</p>
<div class="bt"><span>{src}</span><span>{n}</span>{'<span class="pill mint" style="height:20px">已练习</span>' if d else ''}<b>{ic('arrowup',12)}</b></div></div>''' for t, c, fr, zh, tp, src, n, d in C1)
cats = ''.join(f'<a class="{"on" if i == 0 else ""}">{t} <span class="num">{n}</span></a>' for i, (t, n) in enumerate([('全部', '252'), ('长听力', '20'), ('短听力', '36'), ('阅读', '28'), ('写作', '28'), ('口语', '140')]))
bank2 = fpage('题库练习 · DALF C1', nav('bank') + f'''
<div class="wrap" style="padding-top:22px"><div class="crumb">题库练习 › DALF C1</div>
<div class="lc ban" style="--img:url(../assets/paris-haze.png) 60% 45%/cover;--tint:#efe1f2a8"><div class="img"></div><div class="tint"></div>
<div class="bt2"><div><b class="fr" style="font-size:38px">DALF C1</b><span class="it" style="font-size:16px;margin-left:12px">Brume sur la Seine</span><p class="zh">252 组练习 · 682 道听读题 · 36 段原声录音</p></div>
<div class="st"><div><b class="num">88</b><small>已练习</small></div><div><b class="num">76%</b><small>客观题正确率</small></div><div><b class="num">15</b><small>待回顾错题</small></div></div></div>{hb('var(--orange)','thick')}</div>
<div class="fl"><div class="cats">{cats}</div><span class="seg" style="margin-left:auto"><a style="font-family:var(--zh);font-size:12px">B2</a><a class="on" style="font-family:var(--zh);font-size:12px">C1</a>{hb()}</span>
<span class="sbox">{ic('search',13)}法语或中文关键词{hb()}</span></div>
<div class="tps">{''.join(f'<span class="pill {"peach" if i==0 else "ghost"}">{t}</span>' for i,t in enumerate(['全部主题','教育与成长','科技与社会','社会与生活','健康与科学','城市与环境','语言与文化','工作与经济']))}</div>
<div class="grid">{cards}</div></div>''', 'm-bank', LIVE_CSS + '''
.ban{height:118px;margin-bottom:16px}.ban .bt2{position:absolute;inset:6px;display:flex;align-items:center;padding:0 28px}
.ban p{font-size:13px;color:var(--ink2);margin-top:4px}.ban .st{margin-left:auto;display:flex;gap:34px;text-align:center}.ban .st b{display:block;font-size:28px;color:var(--deep-orange)}.ban .st small{font-size:12px;color:var(--ink2);font-family:var(--zh)}
.fl{display:flex;align-items:center;gap:12px;margin-bottom:10px}
.cats{display:flex;gap:20px}.cats a{font-family:var(--zh);font-size:15px;color:var(--soft);position:relative;padding-bottom:4px}.cats a .num{font-size:13px}
.cats a.on{color:var(--navy)}.cats a.on:after{content:'';position:absolute;left:0;right:0;bottom:-2px;height:3px;border-radius:3px;background:var(--orange);filter:url(#wob)}
.sbox{display:flex;align-items:center;gap:8px;height:34px;padding:0 14px;border-radius:30px;position:relative;font-size:12px;color:var(--soft);width:230px;background:var(--paper)}
.tps{display:flex;gap:6px;margin-bottom:14px}
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
.ex{padding:14px 18px;display:flex;flex-direction:column;min-height:146px}
.ex .tp{display:flex;align-items:center;gap:8px}.ex .to{font-size:11.5px;color:var(--soft);font-family:var(--zh)}
.ex h3{font-size:19px;font-weight:400;margin:8px 0 2px;line-height:1.3}.ex p{font-size:13px;color:var(--ink2)}
.ex .bt{margin-top:auto;padding-top:8px;border-top:1px dashed var(--rule);display:flex;gap:12px;align-items:center;font-size:11px;color:var(--soft)}
.ex .bt b{margin-left:auto;width:26px;height:26px;border-radius:50%;display:grid;place-items:center;background:var(--peach);color:#8a4325}''')

# ------------------------------------------------------------ 3 · 练习工作台
paras = ['C’est un tabou. Les enseignants qui se lient à leurs élèves sont vus par leurs collègues comme des âmes trop sensibles. Pourtant, les études montrent que <span class="mk1">le lien affectif est le premier levier pour la réussite scolaire</span>. Dans son ouvrage qui vient de paraître, <i>Quand les profs aiment les élèves</i>, Maël Virat invite à un changement profond des mentalités.',
         'Évidemment, le titre de cet essai frappe. Et pas forcément au bon endroit. D’emblée, on imagine des amours coupables. C’est tout l’inverse, bien sûr, que défend Maël Virat, chercheur en psychologie qui montre à quel point l’<span class="wordnote">investissement affectif</span> de l’enseignant est vertueux. Ce lien qu’il appelle « <span class="mk2">amour compassionnel</span> » rend les deux parties plus heureuses et, surtout, favorise l’apprentissage.',
         '« On les voit en masse dans les séries, les films et les émissions. On les voit et on les aime ces enseignants qui nouent avec leurs élèves des liens si puissants que les jeunes se subliment pour réussir leur formation… »']
qn = ''.join(f'<span class="{c}">{i}</span>' for i, c in enumerate(['a', 'a', 'cur', '', '', '', '', '', '', '', ''], 1))
bank3 = fpage('题库练习 · 练习工作台', f'''
<header class="pbar"><img src="../assets/hutao-logo.png" alt=""><span class="zh" style="font-size:16px;font-weight:700;color:#7a4b2e">胡桃法语</span><span class="fr" style="color:var(--plum);font-size:15px;margin-left:6px">DALF C1</span>
<span class="bc">题库练习 › C1 › 阅读 › <b>Enseignants : le droit d’aimer</b></span><span class="tm">{ic('clock',14)} 倒计时 <b class="num" style="color:var(--navy)">48:12</b>{hb()}</span><span class="tm">{ic('bookmark',14)} 收藏{hb()}</span><span class="tm">{ic('maximize',14)} 专注{hb()}</span></header>
<div class="dh"><span style="font-size:12px;color:var(--soft)">{ic('chevl',12)} 返回题库 · 2021 年 10 月 · 法国场次 · 教育与成长</span><h1 class="it">Enseignants : le droit d’aimer</h1><span class="zh" style="color:var(--plum)">教师也有表达关爱的权利 · 阅读理解 · 11 题</span></div>
<div class="split"><section class="pane"><div class="phd">{ic('book',14)} 阅读材料<span class="seg" style="margin-left:auto">{''.join(f'<a class="{"on" if i==0 else ""}" style="font-family:var(--zh);font-size:11.5px">{x}</a>' for i,x in enumerate(["法语原文","中文参考","双语对照"]))}{hb()}</span></div>
<div class="hint">选中词句可高亮（黄 → 紫 → 红），也可以加单词备注、收进生词本。</div><div class="rc">{''.join(f'<p>{x}</p>' for x in paras)}</div></section>
<div class="hd"><span>‹›{hb()}</span></div>
<section class="pane"><div class="phd">{ic('pen',14)} 作答区<span class="num" style="margin-left:auto">2 / 11</span></div>
<div class="q"><div class="qm"><b class="num">1</b><small>简答</small></div><h3>À quel paradoxe font face les enseignants dans l’article ?</h3><div class="ta">Le lien affectif favorise la réussite scolaire, mais il reste un tabou dans la profession.{hb('#cfc6bb')}</div></div>
<div class="q"><div class="qm"><b class="num">2</b><small>单选</small></div><h3>Pour Maël Virat, les jeunes enseignants se montrent… à l’idée de développer un rapport affectif avec leurs élèves.</h3>
<div class="op on"><i></i><span>prudents<small>谨慎</small></span>{hb('var(--plum)')}</div><div class="op"><i></i><span>indifférents<small>无所谓</small></span></div><div class="op"><i></i><span>enthousiastes<small>热情期待</small></span></div></div></section></div>
<div class="ft"><div class="qn">{qn}</div><span style="font-size:12px;color:var(--soft)">已作答 <b class="num">2 / 11</b></span><a class="btn solid">提交并查看复盘</a></div>''', 'm-bank', '''
.pbar{height:60px;display:flex;align-items:center;gap:10px;padding:0 28px;background:var(--peach)}
.pbar img{width:34px}.pbar .bc{font-size:12px;color:var(--ink2);margin:0 auto 0 24px}.pbar .bc b{font-weight:400;color:var(--navy)}
.tm{display:flex;gap:6px;align-items:center;font-size:12px;height:32px;padding:0 12px;border-radius:20px;position:relative;background:var(--paper);font-family:var(--zh)}
.dh{padding:14px 28px 12px}.dh h1{font-size:26px;font-weight:400;margin:4px 0 2px}
.split{display:grid;grid-template-columns:1fr 14px 1fr;height:668px;border-top:1.5px dashed var(--rule)}
.pane{overflow:hidden;background:var(--paper)}
.phd{height:46px;display:flex;align-items:center;gap:8px;padding:0 22px;font-family:var(--zh);font-size:13px;border-bottom:1px dashed var(--rule)}
.hint{padding:10px 26px 0;font-size:11px;color:var(--soft)}
.rc{padding:12px 28px;font:18px/1.75 var(--serif);color:#222}.rc p{margin-bottom:1em}
.hd{display:flex;align-items:center;justify-content:center;position:relative}.hd span{position:relative;width:24px;height:28px;display:grid;place-items:center;font-size:12px;color:var(--soft);background:var(--cream);border-radius:6px}
.q{padding:18px 26px;border-bottom:1px dashed var(--rule)}
.qm{display:flex;gap:10px;align-items:center;margin-bottom:8px}.qm b{font-size:24px}.qm small{font-size:11px;color:var(--soft);font-family:var(--zh)}
.q h3{font:400 17px/1.6 var(--serif);margin-bottom:12px}
.ta{position:relative;border-radius:10px;padding:10px 14px;font:16px/1.7 var(--serif);color:#333;min-height:76px}
.op{display:flex;gap:11px;align-items:flex-start;padding:9px 12px;border-radius:10px;font:15px/1.6 var(--serif);position:relative}
.op i{width:16px;height:16px;border-radius:50%;border:1.5px solid var(--soft);margin-top:4px;flex-shrink:0}.op.on i{border:5px solid var(--plum)}
.op small{display:block;font-size:11px;color:var(--soft);font-family:var(--zh)}
.ft{position:absolute;left:0;right:0;bottom:0;height:62px;display:flex;align-items:center;gap:14px;padding:0 28px;border-top:1.5px dashed var(--rule);background:var(--cream)}
.qn{display:flex;gap:6px;flex:1}.qn span{width:30px;height:30px;border-radius:8px;display:grid;place-items:center;font-family:var(--fr);font-weight:700;font-size:14px;color:var(--faint)}
.qn .a{background:var(--lav);color:var(--plum)}.qn .cur{background:var(--orange);color:#fff}''')

# ------------------------------------------------------------ 4 · B2 复盘
bank4 = fpage('题库练习 · B2 复盘', nav('bank') + f'''
<div class="wrap" style="padding-top:22px"><div class="flat sum"><div class="sc"><b class="fr">8/11</b></div><div><span class="pill" style="background:var(--paper);color:var(--amber)">DELF B2 · 阅读 2 · 复盘</span><h1 class="it">Faut-il être beau pour faire de l’information ?</h1><p class="zh">做新闻需要好看吗 · 科技影响 · 国外考过，国内暂未考过 · 用时 34 分 20 秒</p></div>
<div class="ks"><div><b class="num" style="color:var(--green)">8</b><small>正确</small></div><div><b class="num" style="color:var(--red)">2</b><small>错误</small></div><div><b class="num" style="color:var(--plum)">1</b><small>待自评</small></div><a class="btn or">{ic('repeat',12)} 重做错题</a></div></div></div>
<div class="wrap g"><section class="txt"><div class="hd2">{ic('book',14)} 原文定位 · 实线为已核对引文，虚线为候选位置</div>
<p>La sur-importance du physique et du style à la télévision fait couler de l’encre. Le magazine du <i>Monde</i> titrait il y a peu « Le Journal télévisé : nouveau concours de beauté ». Ce constat est-il vraiment nouveau ?</p>
<p>La récente charte vestimentaire de France 3 semble confirmer cette tendance. « Évitez les jeans délavés ou troués », « la jupe se porte au niveau du genou ». <span class="ev">La charte vestimentaire de la chaîne envoyée à tous les présentateurs va bien au-delà des impératifs techniques et visuels<sup>2·3</sup></span>, ceux qui permettent d’éviter un mélange de couleurs susceptible de produire des vibrations à l’écran.</p>
<p>« Les vêtements sont un langage, au même titre que le logo de la chaîne ou les décors », justifie le directeur. <span class="ev cand">Et c’est parfois toute l’apparence physique qui est contrôlée.<sup>1 ?</sup></span></p></section>
<section class="qs">
<div class="box qc">{hb()}<div class="t"><b class="num" style="color:var(--green)">1</b>单选<span class="pill mint">{ic('check',11)} 正确</span></div><h4>Le texte évoque le sujet… des présentateurs de journaux télévisés.</h4><div class="an">你的答案 <b>A · de l’apparence physique</b></div></div>
<div class="box qc">{hb()}<div class="t"><b class="num" style="color:var(--plum)">2</b>简答 · 自评<span class="pill lav">待自评</span></div><h4>Quel est le document que France 3 a diffusé auprès de ses présentateurs ?</h4>
<div class="an">你的答案 <b>un règlement sur les vêtements</b> · 参考 <b>une charte (vestimentaire)</b></div><div class="self">同义表达可以算对：<span class="pill mint">我答对了</span><span class="pill ghost">部分正确{hb('#cfc6bb')}</span><span class="pill ghost">答错了{hb('#cfc6bb')}</span></div></div>
<div class="box qc">{hb('var(--red)')}<div class="t"><b class="num" style="color:var(--red)">3</b>判断<span class="pill blush">{ic('x',11)} 错误</span></div><h4>D’après le document, les présentateurs doivent uniquement éviter les tenues qui posent des problèmes techniques.</h4>
<div class="an">你的答案 <b>Vrai</b> · 正确 <b>Faux</b></div><div class="why"><span class="fr" style="color:var(--amber)">Preuve</span> « …va bien au-delà des impératifs techniques et visuels » —— 着装规定远远超出技术要求，所以「只需避免技术问题」是错的。</div></div></section></div>''', 'm-bank', '''
.sum{display:flex;align-items:center;gap:26px;padding:18px 28px;background:var(--butter)}
.sc{width:96px;height:96px;border-radius:50%;background:conic-gradient(var(--orange) 0 72%,#fff6dc 72%);display:grid;place-items:center}
.sc b{width:78px;height:78px;border-radius:50%;background:var(--butter);display:grid;place-items:center;font-size:22px;color:var(--deep-orange)}
.sum h1{font-size:24px;font-weight:400;margin:8px 0 4px}.sum p{font-size:13px;color:var(--ink2)}
.ks{margin-left:auto;display:flex;gap:26px;align-items:center;text-align:center}.ks b{display:block;font-size:28px}.ks small{font-size:12px;color:var(--ink2);font-family:var(--zh)}
.g{display:grid;grid-template-columns:1fr 540px;gap:34px;margin-top:20px}
.hd2{display:flex;gap:8px;align-items:center;font-size:12.5px;color:var(--soft);margin-bottom:12px;font-family:var(--zh)}
.txt p{font:17px/1.85 var(--serif);margin-bottom:14px}
.ev{background:#fdebc8;border-bottom:2.5px solid var(--orange);padding:1px 2px}.ev.cand{background:none;border-bottom:2.5px dashed var(--orange)}
.ev sup{font:700 11px var(--fr);color:#fff;background:var(--orange);border-radius:8px;padding:1px 6px;margin-left:3px}
.qs{display:flex;flex-direction:column;gap:12px}
.qc{padding:14px 20px}.qc .t{display:flex;align-items:center;gap:10px;font-size:12px;color:var(--soft);font-family:var(--zh)}.qc .t b{font-size:24px}.qc .t .pill{margin-left:auto}
.qc h4{font:400 15px/1.6 var(--serif);margin:6px 0}.an{font-size:12.5px;color:var(--soft)}.an b{font:400 14px var(--serif);color:var(--navy)}
.self{display:flex;gap:8px;align-items:center;margin-top:10px;font-size:12px;color:var(--soft)}
.why{margin-top:10px;padding:10px 14px;border-radius:12px;background:var(--butter);font-size:12.5px;line-height:1.85;color:var(--ink2)}''')

PAGES = {'f31-bank-levels': bank1, 'f32-bank-c1-library': bank2, 'f33-bank-practice': bank3, 'f34-bank-b2-review': bank4}
