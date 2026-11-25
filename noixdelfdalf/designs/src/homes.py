"""Six homepage layout options (round 2)."""
from common import ic, topnav, page

STAR = ic('star', 12, 'fill:#e5b04a;stroke:#e5b04a')

QUICK_ITEMS = [('library', 'DELF B2 题库', '313'), ('library', 'DALF C1 题库', '252'), ('rotate', '错题回顾', '23'),
               ('note', '生词本', '20'), ('bookmark', '我的收藏', '14'), ('calendar', '我的课程', '')]

def quick(style='qbar', k=6):
    items = ''.join(f'<a>{ic(i,14)}{t}{f"<b>{n}</b>" if n else ""}</a>' for i, t, n in QUICK_ITEMS[:k])
    return f'<div class="quick {style}"><span class="hand">Accès rapide</span>{items}</div>'

DAILY_TABS = '<div class="dtabs"><span class="on">一词</span><span>一句</span><span>新闻</span></div>'

BASE = '''
.quick{display:flex;align-items:center;gap:10px;background:#3a2c37;color:#e6d8e0;border-radius:18px;padding:14px 20px}
.quick .hand{color:#f3cf86;font-size:16px;margin-right:8px;white-space:nowrap}
.quick a{display:flex;align-items:center;gap:7px;padding:8px 13px;border-radius:30px;background:#ffffff12;border:1px solid #ffffff1c;font-size:12px;white-space:nowrap}
.quick a b{font-family:var(--hand);color:#f3cf86;font-weight:400;font-size:13px}
.dtabs{display:inline-flex;gap:2px;padding:3px;border-radius:20px;background:#6b4f2f14}
.dtabs span{white-space:nowrap;font-size:10.5px;padding:2px 10px;border-radius:20px;color:#8a6d4a}
.dtabs span.on{background:#fffdfa;color:#5a4128}
.kraft{background:#f1e5d1;color:#5f4529;border-radius:18px}
.kraft .hand{color:#8a5f2d}
.lvl{display:inline-flex;align-items:center;gap:6px;padding:4px 11px;border-radius:20px;font-size:11px;white-space:nowrap}
.lvl.b2{background:var(--amber-soft);color:var(--amber)}.lvl.c1{background:var(--plum-soft);color:var(--plum)}.lvl.soon{border:1px dashed var(--line-2);color:var(--faint)}
'''

# ============================================================ A · Bento 便当格
bento = page('首页方案 A · Bento', topnav('home') + f'''
<style>{BASE}
.wrap{{padding:26px 72px 0;display:grid;grid-template-columns:1.25fr 1fr 1fr;grid-template-rows:auto 1fr 1fr auto;gap:16px;height:828px;padding-bottom:30px}}
.hi{{grid-column:1/-1;display:flex;align-items:baseline;gap:16px}}
.hi .hand{{font-size:22px;color:#a0687f}}
.hi h1{{font-family:var(--serif-zh);font-size:28px;font-weight:600}}
.hi span.s{{margin-left:auto;font-size:12px;color:var(--muted)}}
.t{{border-radius:22px;padding:22px 24px;position:relative;overflow:hidden;border:1px solid var(--line);background:#fffdfb}}
.t .hand{{font-size:17px}}
.t h3{{font-family:var(--serif-zh);font-size:21px;font-weight:600;margin:4px 0 6px;color:#33262f}}
.t p{{font-size:12px;color:var(--muted);line-height:1.8}}
.t .go{{position:absolute;right:20px;top:20px;width:34px;height:34px;border-radius:50%;display:grid;place-items:center;background:#fff;border:1px solid var(--line);color:var(--ink-2)}}
.bank{{grid-row:2/4;background:linear-gradient(170deg,#efe6f2,#f7f1f3 60%,#fbf4ea);border:0;display:flex;flex-direction:column}}
.bank .hand{{color:var(--plum)}}
.ex{{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:16px;flex:1}}
.ex>div{{border-radius:18px;padding:18px;color:#fff;position:relative;overflow:hidden;min-height:170px;display:flex;flex-direction:column}}
.ex>div:before{{content:'';position:absolute;inset:0;background:var(--img);z-index:0}}
.ex>div:after{{content:'';position:absolute;inset:0;background:var(--v);z-index:0}}
.ex>div>*{{position:relative;z-index:1}}
.ex b{{font-family:var(--hand);font-size:25px;white-space:nowrap;font-weight:400;line-height:1}}
.ex small{{font-size:11px;opacity:.9;margin-top:4px}}
.ex ul{{list-style:none;margin-top:auto;font-size:11px;display:grid;grid-template-columns:1fr 1fr;gap:3px 8px}}
.ex .bar{{background:#ffffff40;margin-top:10px}}
.soon{{display:flex;gap:8px;margin-top:12px}}
.daily{{grid-column:2/4;display:grid;grid-template-columns:1fr 230px;gap:20px;padding:22px 26px}}
.daily .w{{font-family:var(--hand);font-size:38px;color:#5f3f58;margin:12px 0 2px}}
.daily .ph{{font-size:11px;color:#9a7b5a}}
.daily p{{font-size:12.5px;line-height:1.8;color:#6b5236;margin-top:6px}}
.daily .ex2{{font:italic 13px/1.7 var(--serif-fr);color:#7b5a34;margin-top:6px}}
.daily .nw{{border-left:1px dashed #c9ad86;padding-left:20px;font-size:12px;color:#6b5236;display:flex;flex-direction:column;gap:10px}}
.daily .nw div b{{display:block;font:400 14px/1.4 var(--serif-fr);color:#4d3720}}
.daily .nw small{{font-size:10.5px;color:#9a7b5a}}
.m{{display:flex;flex-direction:column}}
.m .ico{{width:40px;height:40px;border-radius:12px;display:grid;place-items:center;background:var(--s);color:var(--c);margin-bottom:12px}}
.m .hand{{color:var(--c)}}
.m .meta{{margin-top:auto;display:flex;gap:6px;flex-wrap:wrap}}
.learn{{--c:var(--sage);--s:var(--sage-soft)}}.read{{--c:var(--blue);--s:var(--blue-soft)}}.tutor{{--c:var(--rose);--s:var(--rose-soft)}}
.quick{{grid-column:1/-1}}
</style>
<div class="wrap">
<div class="hi"><span class="hand">Bonjour, Hutao</span><h1>今天想从哪里开始？</h1><span class="s">连续学习 12 天 · 本周已练 9 组题</span></div>
<div class="t bank"><span class="go">{ic('arrowup',15)}</span><span class="hand">Banque d’exercices</span><h3>题库练习</h3><p>DELF / DALF 真题，听力、阅读、写作、口语四项。提交后看复盘解析与原文定位。</p>
<div class="ex">
<div style="--img:url(../assets/arc-haze.png) 30% 60%/cover;--v:linear-gradient(170deg,#c08636d0,#6d4a1fe6)"><b>DELF B2</b><small>Le café au pied de l’Arc</small><ul><li>听力 34</li><li>阅读 34</li><li>写作 17</li><li>口语 228</li></ul><div class="bar"><span style="width:15%;background:#fff"></span></div></div>
<div style="--img:url(../assets/paris-haze.png) 70% 40%/cover;--v:linear-gradient(170deg,#97789dd0,#4a344ce6)"><b>DALF C1</b><small>Brume sur la Seine</small><ul><li>听力 56</li><li>阅读 28</li><li>写作 28</li><li>口语 140</li></ul><div class="bar"><span style="width:35%;background:#fff"></span></div></div>
</div><div class="soon"><span class="lvl soon">DELF A2 · 即将上线</span><span class="lvl soon">DELF B1 · 即将上线</span></div></div>
<div class="t kraft daily"><div><div style="display:flex;justify-content:space-between;align-items:center"><span class="hand">Aujourd’hui · 今日推送</span>{DAILY_TABS}</div>
<div class="w">la flânerie</div><div class="ph">[flɑnʁi] n.f. · 城市生活</div><p>闲逛、漫步；带着好奇心在城里随意散步。</p><div class="ex2">« Paris se découvre par la flânerie. »</div></div>
<div class="nw"><span style="font-size:10.5px;color:#9a7b5a">今日新闻 · 3 篇</span><div><b>Les cafés gardent leurs terrasses l’hiver</b><small>B1 · 3 分钟 · 附音频</small></div><div><b>Le télétravail redessine les villes moyennes</b><small>B2 · 6 分钟</small></div></div></div>
<div class="t m learn"><span class="go">{ic('arrowup',15)}</span><span class="ico">{ic('grammar',19)}</span><span class="hand">Apprendre</span><h3>系统学习</h3><p>分级语法课与主题词汇，学完即练。</p><div class="meta"><span class="lvl" style="background:var(--sage-soft);color:var(--sage)">继续：bien que + 虚拟式</span></div></div>
<div class="t m read"><span class="go">{ic('arrowup',15)}</span><span class="ico">{ic('headphones',19)}</span><span class="hand">Lire &amp; écouter</span><h3>阅读精听</h3><p>新闻精读、逐句听写，点词即查。</p><div class="meta"><span class="lvl" style="background:var(--blue-soft);color:var(--blue)">今日 3 篇 · 4 段音频</span></div></div>
<div class="t m tutor" style="display:none"></div>
{quick()}
</div>''', mod='')
# Put 找老师 into the bento: replace the hidden tile with a slim row tile inside the quick bar area is awkward; add it as 4th small tile instead
bento = bento.replace('<div class="t m tutor" style="display:none"></div>', '')
bento = bento.replace('grid-template-columns:1.25fr 1fr 1fr;', 'grid-template-columns:1.25fr 1fr 1fr 1fr;').replace('.daily{{', '.daily{{').replace('.quick{grid-column:1/-1}', '.quick{grid-column:1/-1}')
bento = bento.replace('.daily{grid-column:2/4;', '.daily{grid-column:2/5;')
bento = bento.replace('<div class="t m read">', '<div class="t m read">', 1)
bento = bento.replace('{quick()}', '')
bento = bento.replace('</div>\n<div class="quick qbar">', '</div>\n<div class="quick qbar">')
bento = bento.replace('<div class="quick qbar">', f'''<div class="t m tutor"><span class="go">{ic('arrowup',15)}</span><span class="ico">{ic('users',19)}</span><span class="hand">Professeurs</span><h3>找老师</h3><p>看视频挑老师，预约一对一。</p><div class="meta"><span class="lvl" style="background:var(--rose-soft);color:var(--rose)">下节课 周一 19:30</span></div></div>
<div class="quick qbar">''', 1)

# ============================================================ B · 侧边栏应用 (App shell)
side = page('首页方案 B · 侧边栏', f'''
<style>{BASE}
.app{{display:grid;grid-template-columns:240px 1fr 340px;height:900px}}
.sb{{background:#fffdfb;border-right:1px solid var(--line);padding:24px 18px;display:flex;flex-direction:column;gap:3px}}
.sb .brand{{display:flex;align-items:center;gap:10px;margin:0 6px 22px}}
.sb .brand img{{width:40px}}
.sb .brand b{{font-family:var(--serif-zh);font-size:18px;color:var(--walnut);display:block}}
.sb .brand small{{font-family:var(--hand);font-size:11px;color:#b07d4a}}
.sb .search{{display:flex;align-items:center;gap:8px;height:36px;padding:0 12px;border-radius:10px;background:var(--paper-2);color:var(--faint);font-size:12px;margin-bottom:14px}}
.sb .search kbd{{margin-left:auto;font:10px var(--sans);border:1px solid var(--line-2);border-radius:4px;padding:0 4px}}
.sb .h{{font-family:var(--hand);font-size:15px;color:var(--plum);margin:14px 8px 6px}}
.sb a{{display:flex;align-items:center;gap:10px;padding:9px 10px;border-radius:9px;font-size:13px;color:#6f6371}}
.sb a b{{margin-left:auto;font-family:var(--hand);font-weight:400;font-size:12px;color:var(--faint)}}
.sb a.on{{background:var(--plum-soft);color:var(--ink)}}
.sb a .d{{width:8px;height:8px;border-radius:50%;background:var(--c)}}
.sb .user{{margin-top:auto;display:flex;align-items:center;gap:10px;padding:12px;border-radius:12px;border:1px solid var(--line);font-size:12px}}
.sb .user small{{display:block;color:var(--faint);font-size:10.5px}}
.mid{{padding:28px 40px 30px;display:flex;flex-direction:column;gap:16px}}
.mid .hand.g{{font-size:22px;color:#a0687f}}
.mid h1{{font-family:var(--serif-zh);font-size:30px;font-weight:600;margin-top:2px}}
.cont{{display:flex;align-items:center;gap:20px;padding:20px 24px;border-radius:20px;background:linear-gradient(110deg,#efe6f2,#f8f3f4);}}
.cont .hand{{font-size:14px;color:var(--plum)}}
.cont b{{display:block;font:400 22px var(--serif-fr);color:#33262f;margin:2px 0}}
.cont small{{font-size:11.5px;color:var(--muted)}}
.cont .btn{{margin-left:auto}}
.grid{{display:grid;grid-template-columns:1fr 1fr;gap:14px}}
.mc{{padding:18px 20px;border-radius:18px;background:#fffdfb;border:1px solid var(--line);display:flex;gap:14px}}
.mc .ico{{width:42px;height:42px;border-radius:12px;display:grid;place-items:center;background:var(--s);color:var(--c);flex-shrink:0}}
.mc .hand{{font-size:14px;color:var(--c)}}
.mc h3{{font-family:var(--serif-zh);font-size:18px;font-weight:600;color:#33262f}}
.mc p{{font-size:12px;color:var(--muted);margin-top:4px;line-height:1.7}}
.mc .tags{{display:flex;gap:6px;margin-top:10px;flex-wrap:wrap}}
.learn{{--c:var(--sage);--s:var(--sage-soft)}}.read{{--c:var(--blue);--s:var(--blue-soft)}}.bank{{--c:var(--plum);--s:var(--plum-soft)}}.tutor{{--c:var(--rose);--s:var(--rose-soft)}}
.quick{{margin-top:auto;flex-wrap:wrap}}.rec{{display:flex;flex-direction:column;gap:12px}}.rh{{display:flex;align-items:baseline;gap:12px}}.rh .hand{{font-size:16px;color:var(--plum)}}.rh b{{font-family:var(--serif-zh);font-size:17px;color:#33262f}}.rh small{{margin-left:auto;font-size:11.5px;color:var(--faint)}}.rl{{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}}.rl div{{padding:16px 18px;border-radius:16px;border:1px solid var(--line);background:#fffdfb;display:flex;flex-direction:column;gap:6px;align-items:flex-start}}.rl b{{font:400 16px/1.35 var(--serif-fr);color:#2f2630}}.rl small{{font-size:11px;color:var(--muted)}}
.rp{{border-left:1px solid var(--line);background:#fcf9f5;padding:34px 24px;display:flex;flex-direction:column;gap:16px}}
.rp .kraft{{padding:20px 22px}}
.rp .w{{font-family:var(--hand);font-size:34px;color:#5f3f58;margin:12px 0 2px}}
.rp p{{font-size:12px;line-height:1.8;color:#6b5236}}
.rp .fx{{font:italic 12.5px/1.7 var(--serif-fr);color:#7b5a34;margin-top:6px;padding-top:10px;border-top:1px dashed #c9ad86}}
.rp .card{{padding:18px 20px}}
.rp .card .hand{{font-size:15px;color:var(--plum)}}
.wk{{display:grid;grid-template-columns:repeat(7,1fr);gap:6px;margin-top:12px;text-align:center;font-size:10px;color:var(--faint)}}
.wk i{{display:block;height:30px;border-radius:8px;background:#efe8ee;margin-top:4px}}.wk i.on{{background:var(--plum)}}
</style>
<div class="app">
<aside class="sb"><div class="brand"><img src="../assets/hutao-logo.png"><span><b>胡桃法语</b><small>Noix · le français</small></span></div>
<div class="search">{ic('search',13)}搜索<kbd>⌘K</kbd></div>
<a class="on">{ic('home',16)}首页</a>
<div class="h">Parcours</div>
<a style="--c:var(--sage)">{ic('grammar',16)}系统学习<b>86</b></a><a style="--c:var(--blue)">{ic('headphones',16)}阅读精听<b>3</b></a><a style="--c:var(--plum)">{ic('library',16)}题库练习<b>565</b></a><a style="--c:var(--rose)">{ic('users',16)}找老师</a>
<div class="h">Mon espace</div>
<a>{ic('rotate',16)}错题回顾<b>23</b></a><a>{ic('note',16)}生词本<b>312</b></a><a>{ic('bookmark',16)}我的收藏<b>14</b></a><a>{ic('clock',16)}学习记录</a>
<div class="user"><span class="avatar">H</span><div>Hutao<small>目标：DALF C1 · 2027 年 3 月</small></div></div></aside>
<main class="mid"><div><span class="hand g">Bonjour, Hutao</span><h1>今天也走一小步</h1></div>
<div class="cont"><div><span class="hand">Reprendre</span><b>Enseignants : le droit d’aimer</b><small>C1 阅读 · 教师也有表达关爱的权利 · 第 3 / 11 题</small></div><a class="btn dark">继续作答 {ic('arrow',13)}</a></div>
<div class="grid">
<div class="mc bank"><span class="ico">{ic('library',19)}</span><div><span class="hand">S’exercer</span><h3>题库练习</h3><p>DELF / DALF 真题，复盘解析与原文定位。</p><div class="tags"><span class="lvl b2">B2 · 313 组</span><span class="lvl c1">C1 · 252 组</span><span class="lvl soon">A2 · B1</span></div></div></div>
<div class="mc learn"><span class="ico">{ic('grammar',19)}</span><div><span class="hand">Apprendre</span><h3>系统学习</h3><p>分级语法课与主题词汇，学完即练。</p><div class="tags"><span class="lvl" style="background:var(--sage-soft);color:var(--sage)">B2 · 第 2 单元</span></div></div></div>
<div class="mc read"><span class="ico">{ic('headphones',19)}</span><div><span class="hand">Lire &amp; écouter</span><h3>阅读精听</h3><p>每日新闻与原声音频，逐句听写。</p><div class="tags"><span class="lvl" style="background:var(--blue-soft);color:var(--blue)">今日 3 篇</span></div></div></div>
<div class="mc tutor"><span class="ico">{ic('users',19)}</span><div><span class="hand">Professeurs</span><h3>找老师</h3><p>母语或中文老师一对一。</p><div class="tags"><span class="lvl" style="background:var(--rose-soft);color:var(--rose)">下节 周一 19:30</span></div></div></div>
</div>
<div class="rec"><div class="rh"><span class="hand">Pour toi</span><b>今天推荐练这 3 组</b><small>根据错题和目标 DALF C1 推荐</small></div>
<div class="rl"><div><span class="lvl c1">C1 长听力</span><b>La nomophobie</b><small>科技与社会 · 11 题 · 有音频</small></div><div><span class="lvl b2">B2 阅读 2</span><b>Faut-il être beau pour faire de l’information ?</b><small>科技影响 · 11 题</small></div><div><span class="lvl c1">C1 口语</span><b>Faut-il tout noter ?</b><small>社会与生活 · 陈述 + 辩论</small></div></div></div>
{quick(k=4)}
</main>
<aside class="rp"><div class="kraft"><div style="display:flex;justify-content:space-between;align-items:center"><span class="hand">Aujourd’hui</span>{DAILY_TABS}</div><div class="w">la flânerie</div><p>闲逛、漫步；带着好奇心在城里随意散步。</p><div class="fx">« Paris se découvre par la flânerie. »</div></div>
<div class="card"><span class="hand">Cette semaine</span><div class="wk"><span>一<i class="on"></i></span><span>二<i class="on"></i></span><span>三<i class="on"></i></span><span>四<i></i></span><span>五<i></i></span><span>六<i></i></span><span>日<i></i></span></div><p style="font-size:11.5px;color:var(--muted);margin-top:10px">连续 12 天 · 本周 2 小时 40 分</p></div>
<div class="card"><span class="hand" style="color:var(--rose)">Prochain cours</span><div style="display:flex;gap:12px;align-items:center;margin-top:10px"><span class="avatar" style="background:var(--rose-soft);color:var(--rose)">CD</span><div style="font-size:12px"><b style="font-weight:500">Camille Durand</b><div style="color:var(--muted);font-size:11px">C1 口语模拟 · 周一 19:30</div></div></div></div>
<div class="card"><span class="hand">Objectif</span><div style="font-family:var(--serif-zh);font-size:16px;margin-top:6px">DALF C1 · 还有 108 天</div><div class="bar" style="margin-top:10px"><span style="width:62%;background:var(--plum)"></span></div><div style="font-size:11px;color:var(--muted);margin-top:6px">C1 题库已练 35% · 口语 12 / 140</div></div>
</aside></div>''')

# ============================================================ C · 搜索优先 (Search-first)
search = page('首页方案 C · 搜索优先', topnav('home') + f'''
<style>{BASE}
.wrap{{padding:0 120px;display:flex;flex-direction:column;align-items:center}}
.top{{text-align:center;padding-top:110px}}
.top .hand{{font-size:28px;color:#a0687f}}
.top h1{{font-family:var(--serif-zh);font-size:38px;font-weight:600;margin:8px 0 26px;color:#33262f}}
.sbox{{width:760px;border-radius:22px;background:#fffdfb;border:1px solid var(--line-2);box-shadow:0 18px 50px #5a3b4c14;padding:8px 8px 8px 22px;display:flex;align-items:center;gap:12px}}
.sbox span{{flex:1;font-size:15px;color:var(--faint)}}
.sbox .seg{{background:var(--paper-2)}}
.sbox .btn{{height:44px}}
.sug{{display:flex;gap:8px;margin-top:14px;font-size:12px;color:var(--muted);align-items:center}}
.sug .chip{{background:#fff;border:1px solid var(--line)}}
.mods{{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;width:100%;margin-top:52px}}
.mo{{padding:18px 20px;border-radius:18px;background:#fffdfb;border:1px solid var(--line);display:flex;flex-direction:column;gap:4px}}
.mo .r{{display:flex;justify-content:space-between;align-items:center;color:var(--c)}}
.mo .hand{{font-size:15px;color:var(--c)}}
.mo h3{{font-family:var(--serif-zh);font-size:19px;font-weight:600;color:#33262f}}
.mo small{{font-size:11.5px;color:var(--muted)}}
.learn{{--c:var(--sage)}}.read{{--c:var(--blue)}}.bank{{--c:var(--plum)}}.tutor{{--c:var(--rose)}}
.low{{display:grid;grid-template-columns:1fr 1fr;gap:14px;width:100%;margin-top:14px}}
.low .kraft{{padding:16px 22px;display:flex;align-items:center;gap:22px}}
.low .kraft .w{{font-family:var(--hand);font-size:26px;color:#5f3f58;white-space:nowrap}}
.low .kraft p{{font-size:12px;color:#6b5236}}
.low .card{{padding:16px 22px;display:flex;align-items:center;gap:16px}}
.quick{{width:100%;margin-top:14px}}
</style>
<div class="wrap">
<div class="top"><span class="hand">Que veux-tu apprendre aujourd’hui ?</span><h1>今天想学点什么？</h1></div>
<div class="sbox">{ic('search',18)}<span>输入单词、语法点、文章标题或题目关键词，例如 « subjonctif »</span><div class="seg"><a class="on">全部</a><a>词</a><a>语法</a><a>真题</a></div><a class="btn dark">搜索</a></div>
<div class="sug">常搜：<span class="chip">bien que + 虚拟式</span><span class="chip">C1 口语 · 教育</span><span class="chip">B2 长听力</span><span class="chip">dont 的用法</span><span class="chip">议论文连接词</span></div>
<div class="mods">
<div class="mo learn"><div class="r"><span class="hand">Apprendre</span>{ic('arrowup',15)}</div><h3>系统学习</h3><small>语法 86 课 · 词汇 12 单元</small></div>
<div class="mo read"><div class="r"><span class="hand">Lire &amp; écouter</span>{ic('arrowup',15)}</div><h3>阅读精听</h3><small>今日 3 篇新闻 · 4 段音频</small></div>
<div class="mo bank"><div class="r"><span class="hand">S’exercer</span>{ic('arrowup',15)}</div><h3>题库练习</h3><small><span class="lvl b2" style="padding:1px 8px">B2 313</span> <span class="lvl c1" style="padding:1px 8px">C1 252</span></small></div>
<div class="mo tutor"><div class="r"><span class="hand">Professeurs</span>{ic('arrowup',15)}</div><h3>找老师</h3><small>48 位老师 · 试听 ¥39 起</small></div>
</div>
<div class="low"><div class="kraft"><span class="hand" style="font-size:15px">Aujourd’hui</span><span class="w">la flânerie</span><p>闲逛、漫步 · « Paris se découvre par la flânerie. »</p><span style="margin-left:auto">{DAILY_TABS}</span></div>
<div class="card"><span class="hand" style="font-size:15px;color:var(--plum)">Reprendre</span><div><b style="font:400 15px var(--serif-fr)">Enseignants : le droit d’aimer</b><div style="font-size:11px;color:var(--muted)">C1 阅读 · 第 3 / 11 题</div></div><a class="btn dark sm" style="margin-left:auto">继续</a></div></div>
{quick()}
</div>''')

# ============================================================ D · 分栏主视觉 (Split hero landing)
split = page('首页方案 D · 分栏主视觉', topnav('home') + f'''
<style>{BASE}
.hero{{display:grid;grid-template-columns:1fr 600px;gap:56px;padding:56px 72px 0 96px;align-items:center}}
.hero .hand{{font-size:26px;color:#a0687f;display:inline-block;transform:rotate(-2deg)}}
.hero h1{{font-family:var(--serif-zh);font-size:48px;line-height:1.35;font-weight:600;color:#33262f;margin:14px 0 12px}}
.hero h1 em{{font-style:normal;color:var(--plum)}}
.hero .fr{{font-size:20px;color:#80627f}}
.hero p{{font-size:13px;line-height:2;color:var(--muted);margin:14px 0 24px;max-width:470px}}
.hero .ctas{{display:flex;gap:10px}}
.prev{{position:relative;height:430px}}
.prev .main{{position:absolute;inset:0 60px 40px 0;border-radius:22px;overflow:hidden;background:url(../assets/paris-haze.png) 65% 40%/cover;box-shadow:0 30px 70px #5a3b4c26}}
.prev .main:after{{content:'';position:absolute;inset:0;background:linear-gradient(0deg,transparent 50%,#3a2c37b0)}}
.prev .main .c{{position:absolute;left:24px;top:22px;z-index:1;color:#fff}}
.prev .main .c b{{font-family:var(--hand);font-size:34px;font-weight:400;display:block}}
.prev .main .c small{{font-size:12px;opacity:.9}}
.prev .q{{position:absolute;right:0;top:40px;width:270px;padding:18px 20px;border-radius:18px;background:#fffdfb;border:1px solid var(--line);box-shadow:0 20px 50px #5a3b4c1f}}
.prev .q small{{font-size:10.5px;color:var(--faint)}}
.prev .q p{{font:14px/1.6 var(--serif-fr);color:#2f2630;margin:8px 0 10px}}
.prev .q .o{{display:flex;flex-direction:column;gap:6px}}
.prev .q .o span{{padding:7px 10px;border-radius:9px;border:1px solid var(--line);font:13px var(--serif-fr)}}
.prev .q .o span.ok{{border-color:#c8d6c0;background:#f4f8f1;color:var(--sage)}}
.prev .k{{position:absolute;left:30px;bottom:0;width:250px;padding:14px 18px}}
.prev .k .w{{font-family:var(--hand);font-size:24px;color:#5f3f58;margin-top:4px}}
.row{{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;padding:34px 72px 0 96px}}
.row div{{padding:14px 18px;border-top:2px solid var(--c)}}
.row .hand{{font-size:14px;color:var(--c)}}
.row b{{display:block;font-family:var(--serif-zh);font-size:17px;color:#33262f;margin:2px 0}}
.row small{{font-size:11.5px;color:var(--muted)}}
.quick{{margin:22px 72px 0 96px}}
</style>
<section class="hero"><div><span class="hand">Un petit pas chaque jour</span>
<h1>从语法到真题，<br>一个地方学完<em>法语</em></h1><div class="fr fr">De A1 jusqu’au DALF C1.</div>
<p>系统学习打基础，阅读精听练语感，DELF / DALF 真题题库检验水平，再找一位老师开口说。</p>
<div class="ctas"><a class="btn dark">免费开始 {ic('arrow',13)}</a><a class="btn ghost">{ic('library',13)} 直接刷题</a></div></div>
<div class="prev"><div class="main"><div class="c"><b>DALF C1</b><small>252 组真题 · 36 段原声 · 复盘解析</small></div></div>
<div class="q"><small>C1 阅读 · 第 2 题</small><p>Les jeunes enseignants se montrent… à l’idée d’un rapport affectif.</p><div class="o"><span class="ok">A. prudents ✓</span><span>B. indifférents</span><span>C. enthousiastes</span></div></div>
<div class="kraft k"><div style="display:flex;justify-content:space-between"><span class="hand" style="font-size:14px">Aujourd’hui</span><span style="font-size:10.5px">一词</span></div><div class="w">la flânerie</div><small style="font-size:11px">闲逛、漫步</small></div></div>
</section>
<div class="row">
<div style="--c:var(--sage)"><span class="hand">Apprendre</span><b>系统学习</b><small>86 节语法课 · 12 个词汇单元</small></div>
<div style="--c:var(--blue)"><span class="hand">Lire &amp; écouter</span><b>阅读精听</b><small>每日新闻 · 逐句听写</small></div>
<div style="--c:var(--plum)"><span class="hand">S’exercer</span><b>题库练习</b><small>B2 313 组 · C1 252 组</small></div>
<div style="--c:var(--rose)"><span class="hand">Professeurs</span><b>找老师</b><small>一对一 · 试听 ¥39 起</small></div>
</div>
{quick()}''')

# ============================================================ E · 杂志编辑风 (Editorial)
edit = page('首页方案 E · 杂志版式', topnav('home') + f'''
<style>{BASE}
.wrap{{padding:28px 72px 0}}
.mast{{display:flex;align-items:flex-end;border-bottom:2px solid #33262f;padding-bottom:12px}}
.mast .hand{{font-size:44px;color:#33262f;line-height:1}}
.mast .r{{margin-left:auto;text-align:right;font-size:11.5px;color:var(--muted);line-height:1.8}}
.mast .r b{{font-family:var(--serif-fr);font-style:italic;font-weight:400;color:#33262f;font-size:14px}}
.secs{{display:flex;gap:26px;padding:10px 0;border-bottom:1px solid var(--line);font-size:12.5px;color:var(--ink-2)}}
.secs span i{{font-style:normal;font-family:var(--hand);font-size:11px;color:var(--faint);margin-left:5px}}
.cols{{display:grid;grid-template-columns:1.5fr 1fr 1fr;gap:30px;padding-top:22px}}
.lead .pic{{height:250px;border-radius:4px;background:url(../assets/arc-haze.png) 45% 60%/cover}}
.lead .k{{font-size:10.5px;letter-spacing:2px;color:var(--rose);margin-top:14px}}
.lead h2{{font:400 30px/1.25 var(--serif-fr);color:#2f2630;margin:6px 0}}
.lead .zh{{font-family:var(--serif-zh);font-size:15px;color:var(--muted)}}
.lead p{{font:14px/1.85 var(--serif-fr);color:#4c4049;margin-top:10px}}
.lead .m{{display:flex;gap:14px;font-size:11.5px;color:var(--muted);margin-top:10px}}
.col h4{{font-family:var(--hand);font-size:18px;color:var(--c);border-bottom:1px solid var(--line);padding-bottom:6px;margin-bottom:10px}}
.col .it{{padding:10px 0;border-bottom:1px solid #f1ebe9}}
.col .it b{{display:block;font:400 16px/1.35 var(--serif-fr);color:#2f2630}}
.col .it small{{font-size:11.5px;color:var(--muted)}}
.word{{margin-top:14px;padding:16px 18px}}
.word .w{{font-family:var(--hand);font-size:28px;color:#5f3f58}}
.word p{{font-size:12px;color:#6b5236}}
.lv{{display:flex;gap:6px;margin-top:8px}}
.quick{{margin-top:20px}}
</style>
<div class="wrap">
<div class="mast"><span class="hand">Le Petit Noix</span><span style="font-family:var(--serif-zh);font-size:15px;color:var(--muted);margin-left:16px">胡桃法语 · 今日学习刊</span><div class="r"><b>Mercredi 25 novembre 2026</b><br>No 328 · 今日 3 篇新闻 · 1 个语法点 · 1 个单词</div></div>
<div class="secs"><span>系统学习<i>Apprendre</i></span><span>阅读精听<i>Lire &amp; écouter</i></span><span>题库练习<i>S’exercer</i></span><span>找老师<i>Professeurs</i></span></div>
<div class="cols">
<article class="lead"><div class="pic"></div><div class="k">À LA UNE · 今日推送 · B1</div><h2>À Paris, les cafés gardent leurs terrasses l’hiver</h2><div class="zh">巴黎咖啡馆的露天座，冬天也不收了</div>
<p>Les terrasses éphémères, nées pendant la crise sanitaire, sont désormais pérennisées. Les riverains, eux, s’inquiètent du bruit…</p><div class="m"><span>{ic('headphones',12)} 音频 3:40</span><span>{ic('note',12)} 生词 9</span><span>{ic('clock',12)} 3 分钟</span></div></article>
<div class="col" style="--c:var(--plum)"><h4>S’exercer · 题库</h4>
<div class="it"><b>Enseignants : le droit d’aimer</b><small>C1 阅读 · 继续第 3 / 11 题</small></div>
<div class="it"><b>Le retour du troc ?</b><small>B2 短听力 · 上次 8 / 10</small></div>
<div class="it"><b>Faut-il tout noter ?</b><small>C1 口语 · 教育话题</small></div>
<div class="lv"><span class="lvl b2">DELF B2 · 313</span><span class="lvl c1">DALF C1 · 252</span></div></div>
<div class="col" style="--c:var(--sage)"><h4>Apprendre · 学习</h4>
<div class="it"><b>bien que + subjonctif</b><small>B2 语法 · 第 5 课 · 配套 10 题</small></div>
<div class="it"><b>Écologie · 108 mots</b><small>主题词汇 · 已掌握 55%</small></div>
<div class="kraft word"><span class="hand" style="font-size:14px">Le mot du jour</span><div class="w">la flânerie</div><p>闲逛、漫步</p></div>
<h4 style="--c:var(--rose);color:var(--rose);margin-top:14px">Professeurs</h4><div class="it" style="border:0;padding-top:0"><b>Camille Durand</b><small>{STAR} 4.98 · 口语冲刺 · 周一 19:30 可约</small></div></div>
</div>
{quick()}
</div>''')

# ============================================================ F · 标签切换 (Tabbed hero)
tabs = page('首页方案 F · 板块切换', topnav('home') + f'''
<style>{BASE}
.wrap{{padding:34px 72px 0}}
.hi{{display:flex;align-items:flex-end;gap:20px;margin-bottom:20px}}
.hi .hand{{font-size:24px;color:#a0687f}}
.hi h1{{font-family:var(--serif-zh);font-size:32px;font-weight:600;color:#33262f}}
.hi .kraft{{margin-left:auto;padding:12px 18px;display:flex;align-items:center;gap:14px}}
.hi .kraft .w{{font-family:var(--hand);font-size:22px;color:#5f3f58}}
.hi .kraft small{{font-size:11.5px}}
.tb{{display:grid;grid-template-columns:repeat(4,1fr);gap:0;border-bottom:1px solid var(--line)}}
.tb a{{padding:14px 18px 14px;display:flex;flex-direction:column;gap:2px;position:relative;color:var(--muted)}}
.tb a .hand{{font-size:15px;color:var(--faint)}}
.tb a b{{font-family:var(--serif-zh);font-size:18px;font-weight:600}}
.tb a small{{font-size:11px}}
.tb a.on{{color:#33262f}}.tb a.on .hand{{color:var(--plum)}}
.tb a.on:after{{content:'';position:absolute;left:18px;right:18px;bottom:-1px;height:3px;border-radius:3px;background:var(--plum)}}
.pane{{display:grid;grid-template-columns:1fr 1fr 360px;gap:18px;padding-top:22px}}
.lv{{border-radius:20px;padding:24px;color:#fff;position:relative;overflow:hidden;min-height:330px;display:flex;flex-direction:column}}
.lv:before{{content:'';position:absolute;inset:0;background:var(--img);z-index:0}}.lv:after{{content:'';position:absolute;inset:0;background:var(--v);z-index:0}}
.lv>*{{position:relative;z-index:1}}
.lv b{{font-family:var(--hand);font-size:42px;font-weight:400;line-height:1}}
.lv .fr{{font-size:15px;margin-top:4px}}
.lv .cats{{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-top:auto}}
.lv .cats span{{padding:9px 10px;border-radius:12px;background:#ffffff26;border:1px solid #ffffff38;font-size:11px}}
.lv .cats span i{{display:block;font-style:normal;font-family:var(--hand);font-size:19px}}
.lv .ft{{display:flex;align-items:center;gap:12px;margin-top:14px;font-size:11.5px}}
.lv .ft .bar{{flex:1;background:#ffffff40}}
.lv .ft .btn{{background:#fff;color:var(--c)}}
.side{{display:flex;flex-direction:column;gap:12px}}
.side .card{{padding:16px 18px}}
.side .hand{{font-size:15px;color:var(--plum)}}
.side .it{{display:flex;justify-content:space-between;font-size:12px;color:var(--muted);padding:8px 0;border-bottom:1px solid #f1ebe9}}
.side .it b{{font:400 13.5px var(--serif-fr);color:#2f2630}}
.side .soon{{display:flex;gap:6px}}
.quick{{margin-top:18px}}
</style>
<div class="wrap">
<div class="hi"><div><span class="hand">Bonjour, Hutao</span><h1>选一个板块开始</h1></div>
<div class="kraft"><span class="hand" style="font-size:14px">Aujourd’hui</span><span class="w">la flânerie</span><small>闲逛、漫步</small>{DAILY_TABS}</div></div>
<div class="tb"><a><span class="hand">Apprendre</span><b>系统学习</b><small>语法 · 主题词汇</small></a><a><span class="hand">Lire &amp; écouter</span><b>阅读精听</b><small>新闻 · 音频 · 生词</small></a><a class="on"><span class="hand">S’exercer</span><b>题库练习</b><small>DELF / DALF 真题</small></a><a><span class="hand">Professeurs</span><b>找老师</b><small>一对一在线课</small></a></div>
<div class="pane">
<div class="lv" style="--img:url(../assets/arc-haze.png) 30% 60%/cover;--v:linear-gradient(165deg,#c48a3cd9,#5c3d17f0);--c:var(--amber)"><b>DELF B2</b><div class="fr fr">Le café au pied de l’Arc</div>
<div class="cats"><span><i>17 · 17</i>长 · 短听力</span><span><i>34</i>阅读</span><span><i>17 · 228</i>写作 · 口语</span></div><div class="ft">已练 46 / 313<div class="bar"><span style="width:15%;background:#fff"></span></div><a class="btn sm">进入</a></div></div>
<div class="lv" style="--img:url(../assets/paris-haze.png) 70% 50%/cover;--v:linear-gradient(165deg,#9a7aa0d9,#3f2c42f0);--c:var(--plum)"><b>DALF C1</b><div class="fr fr">Brume sur la Seine</div>
<div class="cats"><span><i>20 · 36</i>长 · 短听力</span><span><i>28</i>阅读</span><span><i>28 · 140</i>写作 · 口语</span></div><div class="ft">已练 88 / 252<div class="bar"><span style="width:35%;background:#fff"></span></div><a class="btn sm">进入</a></div></div>
<div class="side"><div class="card"><span class="hand">Récemment</span><div class="it"><b>Enseignants : le droit d’aimer</b><span>3 / 11</span></div><div class="it"><b>Le retour du troc ?</b><span>8 / 10</span></div><div class="it" style="border:0"><b>La nomophobie</b><span>9 / 11</span></div></div>
<div class="card"><span class="hand">Bientôt</span><div class="soon" style="margin-top:8px"><span class="lvl soon">DELF A2</span><span class="lvl soon">DELF B1</span></div></div></div>
</div>
{quick()}
</div>''')

PAGES = {
    'r2-A-bento': bento,
    'r2-B-sidebar-app': side,
    'r2-C-search-first': search,
    'r2-D-split-hero': split,
    'r2-E-editorial': edit,
    'r2-F-tabbed': tabs,
}
