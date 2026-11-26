"""Round 4: bento homepage in the spirit of the Salon du livre jeunesse poster:
hand-lettered capitals, flat mint / peach / butter colour, thin wobbly hand-drawn outlines,
orange for dates and numbers, everyday calm."""
from common import ic, page

WOB = '''<svg width="0" height="0" style="position:absolute"><filter id="wob"><feTurbulence type="fractalNoise" baseFrequency="0.022" numOctaves="1" seed="7"/><feDisplacementMap in="SourceGraphic" scale="1.8"/></filter>
<filter id="wob2"><feTurbulence type="fractalNoise" baseFrequency="0.018" numOctaves="1" seed="2"/><feDisplacementMap in="SourceGraphic" scale="2.6"/></filter></svg>'''

CSS = '''
@font-face{font-family:'Patrick Hand SC';src:url(../assets/fonts/patrick-hand-sc-latin-400-normal.woff2) format('woff2'),url(../assets/fonts/patrick-hand-sc-latin-ext-400-normal.woff2) format('woff2')}
:root{--mint:#dbeadf;--mint-line:#c3dacb;--peach:#f2c6aa;--green:#2f7d52;--orange:#e1653a;--navy:#282c44;--cream:#fbf7ef;
 --butter:#f6e5ad;--sky:#d3e3ef;--blush:#f3d3cf;--ink2:#4d5068;--soft:#7d7f90;--plum:#6f566f;
 --cap:'Patrick Hand SC','Comic Sans MS',cursive;--zh:'LXGW WenKai','Kaiti SC','STKaiti',serif;--sans:'PingFang SC','Noto Sans SC',sans-serif}
html{background:var(--cream)}
body{font-family:var(--sans);color:var(--navy)}
.cap{font-family:var(--cap);letter-spacing:1.4px;font-weight:400}
.hb{position:absolute;inset:0;border:2px solid var(--bc,var(--navy));border-radius:inherit;filter:url(#wob);pointer-events:none}
.hb.thick{border-width:2.6px;filter:url(#wob2)}
/* nav */
.nav{height:72px;display:flex;align-items:center;gap:30px;padding:0 64px;position:relative;z-index:2}
.nav .brand{display:flex;align-items:center;gap:10px}
.nav .brand img{width:40px}
.nav .brand b{font-family:var(--zh);font-size:21px;color:#7a4b2e;display:block;line-height:1.1;font-weight:700}
.nav .brand small{font-family:var(--cap);font-size:12px;color:var(--orange);letter-spacing:1px}
.nav .links{display:flex;gap:26px;flex:1;margin-left:20px}
.nav .links a{font-family:var(--zh);font-size:15px;color:var(--ink2);display:flex;gap:6px;align-items:baseline;position:relative;padding:4px 0}
.nav .links a i{font-style:normal;font-family:var(--cap);font-size:12px;color:var(--soft);letter-spacing:1px}
.nav .links a.on{color:var(--navy)}
.nav .links a.on:after{content:'';position:absolute;left:0;right:0;bottom:-3px;height:3px;border-radius:3px;background:var(--orange);filter:url(#wob)}
.nav .search{display:flex;align-items:center;gap:8px;height:36px;padding:0 16px;border-radius:30px;position:relative;font-size:12px;color:var(--soft);background:#fffdf8}
.nav .me{width:36px;height:36px;border-radius:50%;display:grid;place-items:center;font-family:var(--cap);font-size:16px;background:var(--butter);position:relative}
/* bento grid */
.grid{display:grid;grid-template-columns:1.2fr 1fr 1fr 1fr;grid-template-rows:1.25fr .85fr auto;gap:18px}
.t{position:relative;border-radius:20px;padding:22px 24px;display:flex;flex-direction:column}
.t .lab{font-family:var(--cap);font-size:15px;letter-spacing:1.5px;color:var(--lc,var(--green))}
.t h3{font-family:var(--zh);font-size:23px;font-weight:700;margin:2px 0 6px}
.t p{font-size:12.5px;line-height:1.8;color:var(--ink2)}
.bank{grid-row:1/3}
.daily{grid-column:2/5}
.quick{grid-column:1/-1}
.ph{flex:1;display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:16px}
.ph>div{display:flex;flex-direction:column}
.ph .fr{flex:1;border-radius:6px;position:relative;padding:6px;min-height:150px}
.ph .fr .img{height:100%;border-radius:3px;background:var(--img)}
.ph b{font-family:var(--cap);font-size:23px;letter-spacing:1px;margin-top:10px;font-weight:400}
.ph small{font-size:12px;color:var(--ink2)}
.ph small em{font-style:normal;font-family:var(--cap);font-size:16px;color:var(--orange)}
.soon{display:flex;gap:8px;margin-top:14px}
.soon span{font-family:var(--cap);font-size:13px;letter-spacing:1px;color:var(--soft);padding:3px 12px;border-radius:20px;position:relative}
.dw{display:grid;grid-template-columns:1fr 250px;gap:28px;height:100%}
.dtab{display:inline-flex;gap:14px;font-family:var(--zh);font-size:13px;color:var(--soft)}
.dtab .on{color:var(--navy);position:relative}
.dtab .on:after{content:'';position:absolute;left:-2px;right:-2px;bottom:-2px;height:2px;background:var(--orange);filter:url(#wob)}
.word{font-family:var(--cap);font-size:46px;letter-spacing:1px;line-height:1.1;margin:10px 0 0}
.pron{font-size:12px;color:var(--soft)}
.zhm{font-family:var(--zh);font-size:15px;margin-top:6px}
.ex{font-family:var(--zh);font-size:14px;color:var(--ink2);margin-top:6px}
.acts{display:flex;gap:16px;margin-top:auto;padding-top:14px;font-size:12px;color:var(--ink2)}.acts span{display:flex;gap:5px;align-items:center}
.dw>div:first-child{display:flex;flex-direction:column}
.news{display:flex;flex-direction:column;gap:12px;padding-left:24px;position:relative}
.news:before{content:'';position:absolute;left:0;top:4px;bottom:4px;width:1.6px;background:var(--navy);opacity:.35;filter:url(#wob)}
.news small{font-family:var(--cap);font-size:13px;letter-spacing:1px;color:var(--orange)}
.news b{display:block;font:400 15px/1.35 Georgia,serif}
.news span{font-size:11px;color:var(--soft)}
.m .ico{width:40px;height:40px;display:grid;place-items:center;margin-bottom:10px;position:relative;border-radius:50%}
.m .meta{margin-top:auto;font-size:12px;color:var(--ink2);display:flex;gap:6px;align-items:center}
.m .meta em{font-style:normal;font-family:var(--cap);font-size:15px;color:var(--orange);letter-spacing:.5px}
.quick{display:flex;align-items:center;gap:10px;border-radius:18px;padding:14px 22px;background:var(--qb);color:#f2ece3}
.quick .cap{color:var(--qa);font-size:17px;margin-right:10px}
.quick a{display:flex;align-items:center;gap:7px;padding:7px 14px;border-radius:30px;font-size:12.5px;background:#ffffff14;border:1px solid #ffffff22;white-space:nowrap}
.quick a em{font-style:normal;font-family:var(--cap);font-size:15px;color:var(--qa)}
'''

def nav(search_bg='#fffdf8'):
    links = ''.join(f'<a class="{"on" if i == 0 else ""}">{z}<i>{f}</i></a>' for i, (z, f) in enumerate(
        [('首页', 'Accueil'), ('系统学习', 'Apprendre'), ('阅读精听', 'Lire & écouter'), ('题库练习', 'S’exercer'), ('找老师', 'Professeurs')]))
    return f'''<header class="nav"><a class="brand"><img src="../assets/hutao-logo.png" alt=""><span><b>胡桃法语</b><small>NOIX · LE FRANÇAIS</small></span></a>
<nav class="links">{links}</nav><span class="search" style="background:{search_bg}">{ic('search',14)}搜索语法、词汇、文章<i class="hb" style="--bc:var(--navy)"></i></span><span class="me">H<i class="hb"></i></span></header>'''

def quick():
    items = [('DELF B2 题库', '313'), ('DALF C1 题库', '252'), ('错题回顾', '23'), ('生词本', '20'), ('我的收藏', '14'), ('我的课程', '')]
    a = ''.join(f'<a>{t}{f" <em>{n}</em>" if n else ""}</a>' for t, n in items)
    return f'<div class="quick"><span class="cap">ACCÈS RAPIDE</span>{a}</div>'

def tiles(frame='var(--orange)', card_bg=('#fffdf8', '#fffdf8', '#fffdf8', '#fffdf8', '#fffdf8'), border=True, bc='var(--navy)',
          icon_bg=('var(--mint)', 'var(--sky)', 'var(--blush)')):
    hb = (lambda c=bc: f'<i class="hb" style="--bc:{c}"></i>') if border else (lambda c=bc: '')
    bank = f'''<div class="t bank" style="background:{card_bg[0]}">{hb()}<span class="lab" style="--lc:var(--orange)">BANQUE D’EXERCICES</span><h3>题库练习</h3>
<p>DELF / DALF 真题，听力、阅读、写作、口语四项都有。做完看复盘解析和原文定位。</p>
<div class="ph">
<div><div class="fr"><div class="img" style="--img:url(../assets/arc-haze.png) 30% 60%/cover"></div><i class="hb thick" style="--bc:{frame}"></i></div><b>DELF B2</b><small><em>313</em> 组 · 已练 46</small></div>
<div><div class="fr"><div class="img" style="--img:url(../assets/paris-haze.png) 68% 40%/cover"></div><i class="hb thick" style="--bc:{frame}"></i></div><b>DALF C1</b><small><em>252</em> 组 · 已练 88</small></div>
</div><div class="soon"><span>A2 · BIENTÔT<i class="hb" style="--bc:#b9bccb"></i></span><span>B1 · BIENTÔT<i class="hb" style="--bc:#b9bccb"></i></span></div></div>'''
    daily = f'''<div class="t daily" style="background:{card_bg[1]}">{hb()}<div class="dw"><div>
<div style="display:flex;justify-content:space-between;align-items:center"><span class="lab">AUJOURD’HUI · 今日推送</span><span class="dtab"><span class="on">一词</span><span>一句</span><span>新闻</span></span></div>
<div class="word">LA FLÂNERIE</div><div class="pron">[flɑnʁi] n.f. · 城市生活</div><div class="zhm">闲逛、漫步；带着好奇心在城里随意走走。</div><div class="ex">« Paris se découvre par la flânerie. »</div>
<div class="acts"><span>{ic('volume',13)} 听发音</span><span>{ic('plus',13)} 加入生词本</span><span>{ic('cards',13)} 「城市生活」词汇单元</span></div></div>
<div class="news"><small>3 ARTICLES · 今日新闻</small><div><b>Les cafés gardent leurs terrasses l’hiver</b><span>B1 · 3 分钟 · 附音频</span></div><div><b>Le télétravail redessine les villes moyennes</b><span>B2 · 6 分钟</span></div><div><b>Sommeil : ce que la recherche a vraiment prouvé</b><span>C1 · 8 分钟 · 附音频</span></div></div></div></div>'''
    mods = ''
    for k, (lab, lc, zh, desc, icon, meta) in enumerate([
        ('APPRENDRE', 'var(--green)', '系统学习', '分级语法课和主题词汇，学完马上练。', 'grammar', '继续 <em>LEÇON 5</em> · bien que'),
        ('LIRE & ÉCOUTER', '#3c6a95', '阅读精听', '新闻精读、逐句听写，点词就能查。', 'headphones', '今日 <em>3</em> 篇 · <em>4</em> 段音频'),
        ('PROFESSEURS', '#c0533a', '找老师', '看视频挑老师，约一节一对一。', 'users', '下节课 <em>LUN. 19:30</em>')]):
        mods += f'''<div class="t m" style="background:{card_bg[2 + k]}">{hb()}<span class="ico" style="background:{icon_bg[k]};color:{lc}">{ic(icon,18)}</span><span class="lab" style="--lc:{lc}">{lab}</span><h3>{zh}</h3><p>{desc}</p><div class="meta">{meta}</div></div>'''
    return bank + daily + mods + quick()

# ====================================================================== P1 · Affiche 海报
p1 = page('首页 P1 · 海报', WOB + f'''
<style>{CSS}
body{{background:var(--cream)}}
.band{{background:var(--peach);padding:0 0 30px;position:relative}}
.band .nav{{background:transparent}}
.band .head{{display:flex;align-items:flex-end;padding:22px 64px 0}}
.band h1{{font-family:var(--cap);font-weight:400;font-size:54px;line-height:1.02;color:var(--green);letter-spacing:2px}}
.band .zh{{font-family:var(--zh);font-size:19px;color:var(--navy);margin-top:10px}}
.band .r{{margin-left:auto;text-align:right}}
.band .date{{font-family:var(--cap);font-size:30px;color:var(--orange);letter-spacing:1.5px}}
.band .r small{{display:block;font-family:var(--zh);font-size:14px;color:var(--navy)}}
.wall{{background:linear-gradient(var(--mint-line) 1.5px,transparent 1.5px) 0 0/68px 52px,linear-gradient(90deg,var(--mint-line) 1.5px,transparent 1.5px) 0 0/68px 52px,var(--mint);padding:24px 64px 30px;height:636px}}
.wall .grid{{height:100%}}
.quick{{--qb:var(--navy);--qa:#f3b48f}}
</style>
<div class="band">{nav()}
<div class="head"><div><h1>UN PETIT PAS,<br>CHAQUE JOUR.</h1><div class="zh">你好 Hutao，今天想从哪里开始？</div></div>
<div class="r"><div class="date">MER. 26 NOV.</div><small>连续学习 12 天 · 本周已练 9 组题</small></div></div></div>
<div class="wall"><div class="grid">{tiles()}</div></div>''')

# ====================================================================== P2 · Aplats 平涂色块
p2 = page('首页 P2 · 平涂色块', WOB + f'''
<style>{CSS}
body{{background:var(--cream)}}
.head{{display:flex;align-items:flex-end;padding:20px 64px 22px}}
.head h1{{font-family:var(--zh);font-size:32px;font-weight:700}}
.head h1 .cap{{font-size:30px;color:var(--green);margin-right:14px}}
.head .r{{margin-left:auto;font-size:13px;color:var(--ink2);display:flex;gap:18px;align-items:baseline}}
.head .r em{{font-style:normal;font-family:var(--cap);font-size:20px;color:var(--orange);letter-spacing:1px}}
.main{{padding:0 64px;height:738px;padding-bottom:30px}}
.main .grid{{height:100%}}
.t{{border-radius:24px}}
.quick{{--qb:#3a2c37;--qa:#f3cf86}}
</style>
{nav()}
<div class="head"><h1><span class="cap">BONJOUR, HUTAO</span>今天想从哪里开始？</h1><div class="r"><span><em>MER. 26 NOV.</em></span><span>连续 <em>12</em> 天</span><span>本周 <em>9</em> 组题</span></div></div>
<div class="main"><div class="grid">{tiles(frame='#fffdf8', card_bg=('var(--mint)', 'var(--peach)', 'var(--butter)', 'var(--sky)', 'var(--blush)'), border=False, icon_bg=('#fffdf8a0', '#fffdf8a0', '#fffdf8a0'))}</div></div>''')

# ====================================================================== P3 · Croquis 线描
p3 = page('首页 P3 · 线描', WOB + f'''
<style>{CSS}
html,body{{background:#fffdf9}}
.head{{padding:26px 64px 24px;display:flex;align-items:flex-end;gap:24px}}
.head .cap{{font-size:22px;color:var(--orange)}}
.head h1{{font-family:var(--zh);font-size:34px;font-weight:700;position:relative;display:inline-block}}
.head h1:after{{content:'';position:absolute;left:0;right:30%;bottom:-6px;height:3px;background:var(--green);border-radius:3px;filter:url(#wob2)}}
.head .r{{margin-left:auto;font-size:13px;color:var(--ink2)}}
.head .r em{{font-style:normal;font-family:var(--cap);font-size:20px;color:var(--orange)}}
.main{{padding:0 64px;height:722px;padding-bottom:30px}}
.main .grid{{height:100%;gap:22px}}
.t{{border-radius:18px}}
.quick{{--qb:#3a2c37;--qa:#f3cf86}}
</style>
{nav('#fffdf9')}
<div class="head"><div><span class="cap">BONJOUR, HUTAO —</span><br><h1>今天想从哪里开始？</h1></div><div class="r"><em>MER. 26 NOV.</em> · 连续 <em>12</em> 天 · 本周 <em>9</em> 组题</div></div>
<div class="main"><div class="grid">{tiles(frame='var(--orange)', card_bg=('transparent',) * 5, border=True, bc='var(--navy)', icon_bg=('var(--mint)', 'var(--sky)', 'var(--blush)'))}</div></div>''')

PAGES = {
    'r4-P1-affiche': p1,
    'r4-P2-aplats': p2,
    'r4-P3-croquis': p3,
}
