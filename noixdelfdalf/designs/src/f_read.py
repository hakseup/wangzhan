from common import ic
from fcommon import nav, head, tabs, fpage, hb

H = [10,18,26,14,30,22,36,20,12,28,34,16,24,10,30,38,22,14,32,20,10,26,34,14,22,30,12,20,28,16,32,14,10,22,30,20,12,26,36,18,10,24,32,14,20,28,12,22,30,16,26,34,12,18,28,22,10,30,20,14]
def wave(on, k=1.0, gap=4, w=3):
    return ''.join(f'<i style="height:{int(v*k)}px;width:{w}px;margin-right:{gap}px;background:{"var(--blue)" if j < on else "#a9bdd3"}"></i>' for j, v in enumerate(H))

SEG = f'<span class="seg"><a>A2</a><a>B1</a><a class="on">B2</a><a>C1</a>{hb()}</span>'

# ------------------------------------------------------------ 1 · 今日报亭
more = [('Société', 'B2', 'Le télétravail redessine les villes moyennes', '远程办公正在重塑中等城市', '6 分钟', 'sky'),
        ('Culture', 'B1', 'Pourquoi les Français aiment tant les librairies', '法国人为什么这么爱逛书店', '4 分钟', 'butter'),
        ('Sciences', 'C1', 'Sommeil : ce que la recherche a vraiment prouvé', '关于睡眠，研究到底证明了什么', '8 分钟 · 音频', 'lav'),
        ('Environnement', 'B2', 'Les forêts françaises face à la sécheresse', '干旱中的法国森林', '5 分钟 · 音频', 'mint')]
ml = ''.join(f'<div class="it2"><span class="dot" style="background:var(--{c})"></span><div><div class="mt"><span class="fr">{cat}</span><b class="num">{lv}</b></div><h4>{fr}</h4><small>{zh} · {t}</small></div></div>' for cat, lv, fr, zh, t, c in more)
aud = [('Journal de 8 h', '晨间新闻 · 慢速', '05:12', 'B1'), ('Une rencontre, un métier', '职业访谈', '09:40', 'B2'), ('Le mot de la semaine', '每周一词', '03:05', 'A2'), ('Débat : faut-il tout noter ?', '辩论 · 口语素材', '12:30', 'C1')]
au = ''.join(f'<div class="flat au"><span class="pb">{ic("play",12)}</span><div><b>{a}</b><small>{b} · {d}</small></div><span class="num lv">{l}</span></div>' for a, b, d, l in aud)
read1 = fpage('阅读精听 · 今日报亭', nav('read') + head('Le kiosque du jour', '今日报亭', '11 月 27 日 · 3 篇新闻、4 段音频，按你的水平 B2 推荐', SEG + f'<a class="btn line sm">{ic("filter",13)} 主题{hb()}</a>') + f'''
<div class="wrap lay"><article class="box feat">{hb()}
<div class="ph2"><div class="img"></div>{hb('var(--orange)','thick')}</div>
<div class="b"><span class="pill sky">头条 · 社会 · B2</span><h2 class="it">À Paris, les cafés gardent leurs terrasses l’hiver</h2><div class="zh" style="font-size:16px;color:var(--blue)">巴黎咖啡馆的露天座，冬天也不收了</div>
<p>Les terrasses éphémères, nées pendant la crise sanitaire, sont désormais pérennisées. Les riverains, eux, s’inquiètent du bruit…</p>
<div class="meta"><span>{ic('clock',12)} 6 分钟</span><span>{ic('headphones',12)} 音频 3:40</span><span>{ic('note',12)} 预计生词 <b class="num">9</b></span><a class="btn solid sm" style="margin-left:auto;background:var(--blue)">开始精读 {ic('arrow',12)}</a></div></div></article>
<section><div class="secth"><span class="label">À lire aussi</span><h2 class="t">更多推荐</h2><span class="more">全部 ›</span></div>{ml}</section></div>
<div class="wrap"><div class="secth" style="margin-top:20px"><span class="label">À écouter</span><h2 class="t">今日音频</h2><span class="more">音频库 ›</span></div><div class="aus">{au}</div></div>''', 'm-read', '''
.lay{display:grid;grid-template-columns:1fr 430px;gap:30px}
.feat{padding:16px;display:grid;grid-template-columns:300px 1fr;gap:22px}
.ph2{position:relative;border-radius:12px;padding:6px;min-height:400px}.feat .b .pill{align-self:flex-start}.ph2 .img{position:absolute;inset:6px;border-radius:8px;background:url(../assets/arc-haze.png) 40% 60%/cover}
.feat .b{padding:8px 8px 4px 0;display:flex;flex-direction:column}
.feat h2{font-size:27px;font-weight:400;line-height:1.3;margin:12px 0 6px}
.feat p{font:14.5px/1.85 var(--serif);color:var(--ink2);margin-top:10px}
.meta{display:flex;align-items:center;gap:16px;font-size:12px;color:var(--soft);margin-top:auto}.meta span{display:flex;gap:5px;align-items:center}
.it2{display:flex;gap:14px;padding:12px 0;border-bottom:1px dashed var(--rule)}
.it2 .dot{width:12px;height:12px;border-radius:50%;margin-top:6px;flex-shrink:0}
.it2 .mt{display:flex;justify-content:space-between;font-size:14px;color:var(--blue)}.it2 .mt b{font-size:15px}
.it2 h4{font:400 16px/1.35 var(--serif);margin:2px 0}.it2 small{font-size:11.5px;color:var(--soft)}
.aus{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}
.au{display:flex;gap:12px;align-items:center;padding:22px 18px;background:var(--sky);position:relative}
.au .pb{width:36px;height:36px;border-radius:50%;background:var(--blue);color:#fff;display:grid;place-items:center;flex-shrink:0}
.au b{display:block;font:400 14px var(--serif)}.au small{font-size:11px;color:var(--ink2)}.au .lv{position:absolute;right:14px;top:8px;font-size:15px}''')

# ------------------------------------------------------------ 2 · 文章精读
read2 = fpage('阅读精听 · 文章精读', nav('read') + f'''
<div class="g"><section class="art">
<div class="tool"><span>{ic('chevl',13)} 今日报亭</span><span>{ic('highlighter',14)} 划线标注</span><span>{ic('type',14)} 字号</span><span class="seg" style="margin-left:auto"><a class="on" style="font-family:var(--zh);font-size:12px">法文</a><a style="font-family:var(--zh);font-size:12px">双语对照</a><a style="font-family:var(--zh);font-size:12px">中文参考</a>{hb()}</span></div>
<div style="display:flex;gap:8px"><span class="pill sky">社会 · B2</span><span class="pill ghost">示例新闻{hb('#cfc6bb')}</span></div>
<h1 class="it">À Paris, les cafés gardent leurs terrasses l’hiver</h1><div class="zh" style="font-size:17px;color:var(--blue)">巴黎咖啡馆的露天座，冬天也不收了</div>
<div class="flat mini"><span class="pb">{ic('pause',13)}</span><div class="w">{wave(22,.55,3,2)}</div><small class="num" style="color:var(--blue)">01:12 / 03:40</small></div>
<p><span class="cur">Les terrasses éphémères, nées pendant la crise sanitaire, sont désormais <span class="w1">pérennisées</span>.</span> Chaque hiver, elles accueillent des clients emmitouflés sous des <span class="mk1">couvertures en laine</span>, autour de radiateurs d’appoint.</p>
<p>Les <span class="wordnote">riverains</span>, eux, s’inquiètent du bruit et de l’<span class="mk2">encombrement des trottoirs</span>. « On ne peut plus passer avec une poussette », regrette une habitante du onzième arrondissement.</p>
<p>La mairie promet un <span class="mk3">cahier des charges plus strict</span> : chauffage électrique interdit, fermeture à vingt-deux heures…</p>
<div class="box pop">{hb(None,'thick')}<div class="h"><b class="fr">pérenniser</b><small>[peʁenize] v.t.</small><span>{ic('volume',16)}</span></div><ol><li>使长久存在，使永久化</li><li>（临时措施）转为常态</li></ol>
<div class="it" style="font-size:13px;color:var(--blue);margin-top:6px">« pérenniser un dispositif » 把一项措施固定下来</div>
<div class="mk"><i style="background:#fff29b"></i><i style="background:#dfc3f3"></i><i style="background:#f4a8ae"></i><small>高亮</small><a class="btn sm" style="margin-left:auto;background:var(--blue);color:#fff">{ic('plus',12)} 加入生词本</a></div></div></section>
<aside class="sd"><span class="label">Mots de l’article</span><small class="zh" style="color:var(--soft);margin-left:6px">本文生词 · 已加入 <span class="num">3</span></small>
<div class="wl">{''.join(f'<div><b>{a}</b><span>{b}</span></div>' for a, b in [('pérenniser','使常态化'),('éphémère','短暂的'),('le riverain','沿街居民'),('emmitouflé','裹得严实的'),('un cahier des charges','规范细则'),('d’appoint','辅助的')])}</div>
<div class="flat q" style="background:var(--sky)"><span class="fr" style="color:var(--blue)">Compréhension</span><p>读后小测 1 / 3：Que reprochent les riverains aux terrasses ?</p>
<div class="o"><span>A. Leurs prix trop élevés</span><span class="on">B. Le bruit et l’encombrement</span><span>C. Le manque de chauffage</span></div></div></aside></div>''', 'm-read', '''
.g{display:grid;grid-template-columns:1fr 340px;height:828px}
.art{padding:24px 110px 0;position:relative}
.tool{display:flex;align-items:center;gap:20px;font-size:12.5px;color:var(--soft);margin-bottom:16px;font-family:var(--zh)}.tool span{display:flex;gap:5px;align-items:center}
.art h1{font-size:34px;font-weight:400;line-height:1.3;margin:12px 0 4px}
.mini{display:flex;align-items:center;gap:12px;margin:16px 0 20px;padding:10px 14px;background:var(--sky)}
.mini .pb{width:32px;height:32px;border-radius:50%;background:var(--blue);color:#fff;display:grid;place-items:center}.mini .w{display:flex;align-items:center;flex:1}.mini i{border-radius:2px}
.art p{font:19px/1.95 var(--serif);margin-bottom:16px}
.cur{background:#e5eef7;box-shadow:0 0 0 4px #e5eef7;border-radius:3px}
.w1{border-bottom:2.5px solid var(--orange)}
.pop{position:absolute;left:600px;top:388px;width:330px;padding:18px 20px;z-index:3}
.pop .h{display:flex;align-items:baseline;gap:10px}.pop .h b{font-size:27px;color:var(--blue)}.pop .h small{font-size:11px;color:var(--soft)}.pop .h span{margin-left:auto;color:var(--blue)}
.pop ol{margin:8px 0 0 18px;font-size:13px;line-height:1.8;color:var(--ink2);font-family:var(--zh)}
.mk{display:flex;align-items:center;gap:6px;margin-top:12px;padding-top:12px;border-top:1px dashed var(--rule)}.mk i{width:20px;height:20px;border-radius:50%}.mk small{font-size:11px;color:var(--soft);font-family:var(--zh)}
.sd{padding:28px 26px;border-left:1.5px dashed var(--rule)}
.wl{margin-top:10px}.wl div{display:flex;justify-content:space-between;padding:10px 0;border-bottom:1px dashed var(--rule);font-size:12.5px;color:var(--soft);font-family:var(--zh)}.wl b{font:400 15px var(--serif);color:var(--navy)}
.q{margin-top:22px;padding:16px 18px}.q p{font-size:13px;line-height:1.8;color:var(--ink2);margin:6px 0 10px}
.q .o{display:flex;flex-direction:column;gap:6px}.q .o span{padding:8px 12px;border-radius:10px;background:var(--paper);font:13px var(--serif)}.q .o .on{outline:2px solid var(--blue)}''')

# ------------------------------------------------------------ 3 · 逐句精听
sents = [('00:00', 'Bonjour à toutes et à tous, il est huit heures, voici le journal.', 'd'),
         ('00:05', 'À la une ce matin : le gouvernement annonce de nouveaux trains de nuit vers l’Italie.', 'd'),
         ('00:12', '<span class="blur">Les premières liaisons seront ouvertes dès le printemps prochain.</span>', 'cur'),
         ('00:18', 'Une bonne nouvelle pour les voyageurs soucieux de leur empreinte carbone.', ''),
         ('00:25', 'Mais le prix des billets reste une question sensible…', '')]
tr = ''
for t, s, c in sents:
    tr += f'<div class="s {c}">{hb() if c=="cur" else ""}<small class="num">{t}</small><p>{s}</p></div>'
    if c == 'cur':
        tr += f'''<div class="flat dict"><div class="lb"><span>你的听写 · 第 3 句</span><span>Entrée 核对</span></div>
<div class="in"><span class="ok">Les premières</span> <span class="bad">liaison</span> <span class="fix">liaisons</span> <span class="ok">seront ouvertes</span> <span class="miss">dès</span> <span class="ok">le printemps prochain.</span></div>
<div class="res"><span style="color:var(--green)">{ic('check',12)} 7 词正确</span><span style="color:var(--red)">1 处拼写 · 复数 -s</span><span style="color:#9a6a10">1 处漏听 · dès</span></div></div>'''
read3 = fpage('阅读精听 · 逐句精听', nav('read') + f'''
<div class="g"><section>
<div class="crumb">阅读精听 › 原声音频 › Journal de 8 h</div>
<div class="top"><div><h1 class="it">Journal de 8 h · Trains de nuit</h1><div class="zh" style="font-size:15px;color:var(--blue)">晨间新闻：开往意大利的夜车 · 慢速 · B1 · 05:12</div></div><span class="seg" style="margin-left:auto">{''.join(f'<a class="{"on" if i==1 else ""}" style="font-family:var(--zh);font-size:12.5px">{x}</a>' for i,x in enumerate(["盲听","逐句听写","跟读","原文"]))}{hb()}</span></div>
<div class="flat pl"><div class="w">{wave(18,1.4,9,5)}</div><div class="ctr"><span>{ic('back15',18)}</span><span class="big">{ic('play',18)}</span><span>{ic('fwd15',18)}</span><span class="num" style="color:var(--navy)">00:12 / 05:12</span><span class="pill butter">{ic('repeat',11)} 单句循环 · 第 3 句</span><span class="pill" style="background:var(--paper);margin-left:auto">0.75×</span><span class="pill" style="background:var(--paper)">自动暂停</span></div></div>
<div class="tr">{tr}</div></section>
<aside class="sd"><div class="box c">{hb()}<span class="label">Mode d’écoute</span><div class="modes">
<div>{ic('headphones',16)}<span>盲听整段<small>先抓大意，不看原文</small></span></div><div class="on">{ic('pen',16)}<span>逐句听写<small>每句自动暂停，写完再核对</small></span></div><div>{ic('mic',16)}<span>影子跟读<small>录音对比原声语调</small></span></div></div></div>
<div class="flat c" style="background:var(--sky)"><span class="label">Ce matin</span><div class="st"><div><b class="num">2/9</b><small>已听写</small></div><div><b class="num">86%</b><small>准确率</small></div><div><b class="num">4</b><small>新生词</small></div></div></div>
<p class="note">{ic('note',14)} 听写错的单词会自动进生词本，并记下出处音频和时间点，复习时可以回放原句。</p></aside></div>''', 'm-read', '''
.g{display:grid;grid-template-columns:1fr 360px;gap:40px;padding:22px 64px 0}
.top{display:flex;align-items:flex-end;margin-bottom:16px}.top h1{font-size:30px;font-weight:400}
.pl{background:var(--sky);padding:20px 24px}.pl .w{display:flex;align-items:center;height:64px}.pl .w i{border-radius:3px}
.ctr{display:flex;align-items:center;gap:16px;margin-top:10px;color:var(--blue)}.big{width:48px;height:48px;border-radius:50%;background:var(--blue);color:#fff;display:grid;place-items:center}
.tr{margin-top:14px}
.s{display:flex;gap:18px;padding:10px 16px;border-radius:14px;position:relative}.s small{width:42px;padding-top:4px;font-size:15px}
.s p{font:18px/1.7 var(--serif);color:#9a9caa}.s.d p{color:var(--ink2)}.s.cur{background:var(--paper)}.s.cur p{color:var(--navy)}
.blur{filter:blur(6px)}
.dict{margin:8px 0 6px 76px;padding:14px 18px;background:var(--butter)}
.dict .lb{display:flex;justify-content:space-between;font-size:11.5px;color:#7a5a18;font-family:var(--zh)}
.dict .in{font:18px/1.8 var(--serif);margin-top:6px;padding:6px 12px;border-radius:10px;background:var(--paper)}
.ok{color:var(--green)}.bad{color:var(--red);text-decoration:line-through}.fix{color:var(--green);font-weight:700}.miss{color:#9a6a10;border-bottom:2px dashed #d8a640}
.res{display:flex;gap:16px;margin-top:8px;font-size:12px;font-family:var(--zh)}.res span{display:flex;gap:4px;align-items:center}
.sd{display:flex;flex-direction:column;gap:16px;padding-top:30px}
.c{padding:18px 20px}
.modes{display:flex;flex-direction:column;gap:8px;margin-top:10px}.modes div{display:flex;gap:12px;align-items:center;padding:10px 12px;border-radius:12px;font-size:13px;font-family:var(--zh);color:var(--ink2)}
.modes div small{display:block;font-size:11px;color:var(--soft);font-family:var(--sans)}.modes svg{color:var(--blue)}.modes .on{background:var(--sky);color:var(--navy)}
.st{display:grid;grid-template-columns:repeat(3,1fr);text-align:center;margin-top:8px}.st b{display:block;font-size:26px}.st small{font-size:11.5px;color:var(--ink2);font-family:var(--zh)}
.note{font-size:12.5px;line-height:1.8;color:var(--ink2)}''')

# ------------------------------------------------------------ 4 · 生词本
wb = [('pérenniser', 'v.t.', '使常态化', '« …sont désormais pérennisées. »', 'Les cafés gardent leurs terrasses', '阅读', 'mk1', '今天'),
      ('le riverain', 'n.m.', '沿街居民', '« Les riverains s’inquiètent du bruit. »', 'Les cafés gardent leurs terrasses', '阅读', 'mk2', '今天'),
      ('la liaison', 'n.f.', '线路；连接', '« Les premières liaisons seront ouvertes… »', 'Journal de 8 h', '听力 00:12', 'mk3', '明天'),
      ('le levier', 'n.m.', '杠杆；手段', '« …le premier levier pour la réussite scolaire. »', 'C1 阅读 · Enseignants', '题库', 'mk1', '3 天后'),
      ('la nomophobie', 'n.f.', '无手机恐惧症', '« La nomophobie touche surtout les jeunes. »', 'C1 长听力', '题库', 'mk2', '5 天后'),
      ('le troc', 'n.m.', '以物易物', '« Le retour du troc ? »', 'B2 短听力', '题库', 'mk1', '1 周后')]
wr = ''.join(f'<tr><td><b class="w">{w}</b><small>{p}</small></td><td class="zh" style="font-size:14px;color:var(--navy)">{m}</td><td class="ex"><span class="{mk}">{ex}</span></td><td><span class="it" style="color:var(--blue)">{src}</span><small>{k}</small></td><td>{n}</td></tr>' for w, p, m, ex, src, k, mk, n in wb)
read4 = fpage('阅读精听 · 生词本', nav('read') + head('Mon carnet de mots', '生词本', '四个板块里点过、划过、听错的词，都会带着原句和出处收进这里。', f'<a class="btn line sm">{ic("download",13)} 导出 Anki / CSV{hb()}</a>') + f'''
<div class="wrap"><div class="top3"><div class="flat rev"><div><span class="fr" style="color:#cfdcf0">À réviser aujourd’hui</span><b class="fr">20</b><small>个单词待复习 · 约 6 分钟</small></div><a class="btn" style="background:var(--cream);color:var(--blue);margin-left:auto">开始复习 {ic('arrow',13)}</a></div>
<div class="box sm">{hb()}<span class="label">Cette semaine</span><small class="zh" style="color:var(--soft);margin-left:6px">新增 <span class="num">38</span> 词</small><div class="bars">{''.join(f'<span style="height:{h}%;background:{c}"></span>' for h,c in [(40,'var(--blue)'),(70,'var(--blue)'),(55,'var(--blue)'),(100,'var(--orange)'),(10,'#e4ddd2'),(10,'#e4ddd2'),(10,'#e4ddd2')])}</div></div>
<div class="box sm">{hb()}<span class="label">Maîtrise</span><div class="mix"><span style="width:41%;background:var(--mint)"></span><span style="width:33%;background:var(--butter)"></span><span style="width:26%;background:var(--blush)"></span></div>
<div class="lg"><span>已掌握 <b class="num">128</b></span><span>学习中 <b class="num">102</b></span><span>新词 <b class="num">82</b></span></div></div></div>
<table><tr><th>单词</th><th>释义</th><th>原句（保留你的高亮颜色）</th><th>出处</th><th>下次复习</th></tr>{wr}</table></div>''', 'm-read', '''
.top3{display:grid;grid-template-columns:1.1fr 1fr 1fr;gap:16px;margin-bottom:18px}
.rev{display:flex;align-items:center;padding:18px 24px;background:var(--blue);color:#fff}.rev b{display:block;font-size:46px;line-height:1.1}.rev small{font-size:12px;color:#d5e0ee;font-family:var(--zh)}
.sm{padding:16px 20px}.bars{display:flex;gap:8px;align-items:flex-end;height:52px;margin-top:10px}.bars span{flex:1;border-radius:6px 6px 2px 2px}
.mix{display:flex;height:14px;border-radius:8px;overflow:hidden;margin:14px 0 10px}.lg{display:flex;gap:16px;font-size:12px;color:var(--ink2);font-family:var(--zh)}.lg b{font-size:15px}
td .w{font:400 16px var(--serif);color:var(--navy)}td small{display:block;font-size:11px;color:var(--soft)}td.ex{font:13px var(--serif);color:var(--navy)}''')

PAGES = {'f21-read-kiosk': read1, 'f22-read-article': read2, 'f23-read-listening': read3, 'f24-read-wordbook': read4}
