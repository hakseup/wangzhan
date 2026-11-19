from common import ic, topnav, page

STAR = ic('star', 12, 'fill:#e5b04a;stroke:#e5b04a')

def av(init, bg, fg, size=64, fs=24):
    return f'<span class="av" style="width:{size}px;height:{size}px;background:{bg};color:{fg};font-size:{fs}px">{init}</span>'

AV_CSS = '.av{border-radius:50%;display:grid;place-items:center;font-family:var(--hand);flex-shrink:0;position:relative}.av.on:after{content:"";position:absolute;right:2px;bottom:2px;width:12px;height:12px;border-radius:50%;background:#8fb27c;border:2px solid #fff}'

T = [
    ('CD', 'Camille Durand', '#ecd8d1', '#a65f58', '法国 · 里昂', '母语：法语 · 也会说：英语、中文 B1', '4.98', '1 240', '326', '¥ 188', '曾任 DELF/DALF 口试考官 6 年。擅长 B2–C1 口语陈述与辩论，课上用真题模拟，课后给出逐项评分表。', ['DELF 认证考官', '口语', '考试冲刺', 'B2–C1'], '20% 30%', 'paris-haze.png'),
    ('王', '王思敏', '#dfe7da', '#5f7759', '中国 · 上海', '母语：中文 · 法语 C2 · 巴黎索邦大学硕士', '4.95', '860', '214', '¥ 128', '用中文把语法讲透：时态、虚拟式、关系代词一张图理清。零基础到 B1 的学员最多，配合「系统学习」进度上课。', ['中文授课', '语法', '零基础', 'A1–B1'], '80% 70%', 'arc-haze.png'),
    ('LM', 'Léa Martin', '#e2e7f1', '#566d8e', '法国 · 波尔多', '母语：法语 · 也会说：英语', '4.92', '530', '148', '¥ 158', '每节课一篇法国新闻：先精读，再讨论，最后纠音。适合想把「阅读精听」里的内容说出来的同学。', ['新闻精读', '发音纠正', '会话', 'B1–C1'], '50% 40%', 'arc-haze.png'),
]

# ------------------------------------------------------------ 1 · 找老师列表
rows = ''
for init, name, bg, fg, place, langs, rate, lessons, stu, price, intro, tags, pos, img in T:
    tg = ''.join(f'<span class="chip {"rose" if i == 0 else "line"}">{t}</span>' for i, t in enumerate(tags))
    rows += f'''<div class="row"><div class="l">{av(init, bg, fg, 84, 30).replace('class="av"', 'class="av on"')}
<div class="info"><div class="nm"><b>{name}</b><span class="chip line">{ic('shield',11)} 已认证</span></div><small>{place} · {langs}</small><div class="tg">{tg}</div><p>{intro}</p></div>
<div class="pr"><div class="rt">{STAR}<b>{rate}</b><small>{stu} 位学员 · {lessons} 节课</small></div><div class="price"><b>{price}</b><small>50 分钟 · 试听 ¥ 39</small></div><a class="btn dark sm" style="background:var(--rose)">预约试听</a><a class="btn ghost sm">{ic('msg',13)} 发消息</a></div></div>
<div class="vd" style="background-image:url(../assets/{img});background-position:{pos}"><span class="pl">{ic('play',16)}</span><div class="slots"><small>本周可约</small><div>{''.join(f'<i class="{c}"></i>' for c in ['a','a','','a','b','a','','','a','a','a','','b','a'])}</div></div></div></div>'''
tutor1 = page('找老师 · 浏览老师', topnav('tutor') + f'''
<style>{AV_CSS}
.wrap{{padding:28px 72px 0}}
.head{{display:flex;align-items:flex-end;margin-bottom:18px}}
.head .hand{{font-size:26px;color:var(--rose)}}
.head h1{{font-family:var(--serif-zh);font-size:30px;font-weight:600;color:#33262f;margin-top:2px}}
.head p{{font-size:12.5px;color:var(--muted);margin-top:6px}}
.head .r{{margin-left:auto;display:flex;gap:10px}}
.fb{{display:flex;gap:10px;align-items:center;padding:12px 14px;border-radius:16px;background:#fffdfb;border:1px solid var(--line);margin-bottom:16px}}
.fb .f{{display:flex;flex-direction:column;gap:2px;padding:4px 14px;border-right:1px solid var(--line)}}
.fb .f small{{font-size:10px;color:var(--faint)}}
.fb .f span{{font-size:12.5px;color:var(--ink);display:flex;gap:6px;align-items:center}}
.fb .chips{{display:flex;gap:6px;margin-left:6px}}
.fb .searchpill{{margin-left:auto;background:#fff}}
.cnt{{display:flex;font-size:12px;color:var(--muted);margin-bottom:10px}}
.cnt span:last-child{{margin-left:auto}}
.row{{display:grid;grid-template-columns:1fr 330px;gap:16px;margin-bottom:14px}}
.row .l{{display:flex;gap:20px;padding:20px 22px;border-radius:18px;background:#fffdfb;border:1px solid var(--line)}}
.row .info{{flex:1}}
.row .nm{{display:flex;gap:10px;align-items:center}}
.row .nm b{{font-size:17px;font-weight:600;color:#33262f}}
.row small{{font-size:11.5px;color:var(--faint)}}
.row .tg{{display:flex;gap:6px;margin:10px 0}}
.row p{{font-size:12.5px;line-height:1.85;color:#5c4e57}}
.row .pr{{width:170px;display:flex;flex-direction:column;gap:8px;border-left:1px dashed var(--line-2);padding-left:20px}}
.row .rt{{display:flex;align-items:center;gap:5px;flex-wrap:wrap}}
.row .rt b{{font-size:15px;color:#33262f}}
.row .rt small{{width:100%}}
.row .price b{{font:400 22px var(--serif-fr);color:#33262f}}
.row .price small{{display:block}}
.row .btn{{justify-content:center}}
.vd{{border-radius:18px;background-size:300%;position:relative;overflow:hidden}}
.vd:after{{content:'';position:absolute;inset:0;background:linear-gradient(0deg,#2d2228cc,transparent 60%)}}
.vd .pl{{position:absolute;left:50%;top:38%;transform:translate(-50%,-50%);width:48px;height:48px;border-radius:50%;background:#ffffffe0;color:var(--rose);display:grid;place-items:center;z-index:1}}
.vd .slots{{position:absolute;left:16px;right:16px;bottom:14px;z-index:1;color:#fff}}
.vd .slots small{{font-size:10.5px;color:#f1e4e6}}
.vd .slots div{{display:grid;grid-template-columns:repeat(14,1fr);gap:3px;margin-top:6px}}
.vd .slots i{{height:14px;border-radius:3px;background:#ffffff33}}.vd .slots i.a{{background:#f0c9c2}}.vd .slots i.b{{background:#fff}}
</style>
<div class="wrap m-tutor">
<div class="head"><div><span class="hand">Trouver un prof</span><h1>找老师</h1><p>先看 1 分钟视频，再约一节 25 分钟试听课。课后笔记和生词会同步到你的学习记录。</p></div>
<div class="r"><a class="btn ghost sm">{ic('calendar',13)} 我的课程</a><a class="btn ghost sm">{ic('user',13)} 成为老师</a></div></div>
<div class="fb"><div class="f"><small>我想学</small><span>DELF / DALF 备考 {ic('chevd',11)}</span></div><div class="f"><small>授课语言</small><span>法语 · 中文 {ic('chevd',11)}</span></div><div class="f"><small>价格 / 50 分钟</small><span>¥ 80 – 250 {ic('chevd',11)}</span></div><div class="f"><small>可上课时间</small><span>工作日晚上 {ic('chevd',11)}</span></div>
<div class="chips"><span class="chip rose">母语老师</span><span class="chip line">考官经历</span><span class="chip line">口语</span></div><div class="searchpill" style="width:200px">{ic('search',13)}老师姓名或关键词</div></div>
<div class="cnt"><span>找到 48 位老师</span><span>排序：综合推荐 {ic('chevd',11)}</span></div>
{rows}
</div>''', mod='m-tutor')

# ------------------------------------------------------------ 2 · 老师主页
init, name, bg, fg, place, langs, rate, lessons, stu, price, intro, tags, pos, img = T[0]
days = ['周四 19', '周五 20', '周六 21', '周日 22', '周一 23', '周二 24', '周三 25']
slots = [['', 'a', 'a', '', 'a'], ['a', '', 'a', 'a', ''], ['a', 'a', '', '', ''], ['', '', 'a', 'a', 'a'], ['a', 'a', 'a', '', 'a'], ['', 'a', '', 'a', 'a'], ['a', '', 'a', 'a', '']]
times = ['09:00', '12:00', '18:30', '19:30', '20:30']
cal = '<div class="cal"><span></span>' + ''.join(f'<b>{d}</b>' for d in days)
for r, t in enumerate(times):
    cal += f'<small>{t}</small>' + ''.join(f'<i class="{slots[c][r]}"></i>' for c in range(7))
cal += '</div>'
tutor2 = page('找老师 · 老师主页', topnav('tutor') + f'''
<style>{AV_CSS}
.wrap{{padding:22px 72px 0;display:grid;grid-template-columns:1fr 360px;gap:30px}}
.hero{{display:flex;gap:22px;align-items:center}}
.hero b{{font-size:26px;font-weight:600;color:#33262f}}
.hero .s{{font-size:12px;color:var(--muted);margin-top:4px}}
.hero .tg{{display:flex;gap:6px;margin-top:10px}}
.hero .num{{margin-left:auto;display:flex;gap:26px;text-align:center}}
.hero .num b{{display:block;font-family:var(--hand);font-size:24px;color:var(--rose)}}
.hero .num small{{font-size:11px;color:var(--muted)}}
.vid{{height:250px;border-radius:20px;margin-top:20px;background:url(../assets/paris-haze.png) 30% 40%/cover;position:relative;overflow:hidden}}
.vid:after{{content:'';position:absolute;inset:0;background:linear-gradient(90deg,#3a2730b0,transparent 70%)}}
.vid .q{{position:absolute;left:30px;bottom:28px;z-index:1;color:#fff;max-width:420px}}
.vid .q .hand{{font-size:28px;line-height:1.3}}
.vid .q small{{display:block;margin-top:8px;font-size:12px;color:#f0dfe3}}
.vid .pl{{position:absolute;right:40px;bottom:30px;width:58px;height:58px;border-radius:50%;background:#fff;color:var(--rose);display:grid;place-items:center;z-index:1}}
.tabs{{margin-top:18px}}
.two{{display:grid;grid-template-columns:1fr 1fr;gap:22px}}
.two p{{font-size:12.5px;line-height:1.95;color:#5c4e57}}
.two h3{{font-family:var(--serif-zh);font-size:16px;margin-bottom:8px;color:#33262f}}
.rv{{padding:14px 16px;border-radius:14px;background:#fffdfb;border:1px solid var(--line);margin-bottom:10px}}
.rv .h{{display:flex;align-items:center;gap:8px;font-size:12px;color:#33262f}}
.rv .h small{{margin-left:auto;font-size:11px;color:var(--faint)}}
.rv p{{font-size:12px;line-height:1.8;color:#6c5e67;margin-top:6px}}
.bk{{border-radius:20px;background:#fffdfb;border:1px solid var(--line);padding:22px 22px;box-shadow:0 18px 50px #a65f5812}}
.bk .hand{{font-size:17px;color:var(--rose)}}
.ls{{display:flex;flex-direction:column;gap:8px;margin:12px 0 16px}}
.ls div{{display:flex;align-items:center;gap:10px;padding:11px 14px;border-radius:12px;border:1px solid var(--line);font-size:12.5px;color:#4c4049}}
.ls div small{{display:block;font-size:11px;color:var(--faint)}}
.ls div b{{margin-left:auto;font:400 16px var(--serif-fr);color:#33262f}}
.ls div.on{{border-color:#e2bcb5;background:#fcf3f1}}
.cal{{display:grid;grid-template-columns:40px repeat(7,1fr);gap:4px;font-size:10px;color:var(--faint);text-align:center}}
.cal b{{font-weight:400;font-size:9.5px;color:var(--muted)}}
.cal small{{font-size:9.5px;text-align:left;align-self:center}}
.cal i{{height:20px;border-radius:5px;background:#f3eeec}}.cal i.a{{background:#f0d3cd}}
.bk .btn{{width:100%;justify-content:center;margin-top:16px;background:var(--rose);color:#fff}}
.bk .note{{font-size:11px;color:var(--faint);text-align:center;margin-top:10px}}
</style>
<div class="wrap m-tutor"><section>
<div class="crumb">找老师 {ic('chev',11)} <span>{name}</span></div>
<div class="hero">{av(init, bg, fg, 92, 34).replace('class="av"', 'class="av on"')}<div><b>{name}</b> <span class="chip rose" style="vertical-align:5px">{ic('shield',11)} DELF/DALF 认证考官</span><div class="s">{place} · {langs} · 当地时间 13:40</div><div class="tg"><span class="chip line">口语陈述</span><span class="chip line">辩论</span><span class="chip line">写作批改</span><span class="chip line">B2–C1</span></div></div>
<div class="num"><div><b>{rate}</b><small>{STAR} 评分</small></div><div><b>{lessons}</b><small>节课</small></div><div><b>98%</b><small>出勤率</small></div></div></div>
<div class="vid"><div class="q"><span class="hand">« Parler, c’est déjà gagner la moitié de l’épreuve. »</span><small>开口，就已经赢了口试的一半。—— 自我介绍视频 1:20</small></div><span class="pl">{ic('play',20)}</span></div>
<div class="tabs"><a class="on">关于我</a><a>课程</a><a>学员评价 · 326</a><a>教学资料</a></div>
<div class="two"><div><h3>我会怎样上课</h3><p>{intro}<br>每节课从你在「题库练习」里的口语题开始：10 分钟准备、陈述、辩论，再逐条讲解语法与表达。</p></div>
<div><div class="rv"><div class="h">{av('M','#efe8f3','#735a78',26,12)} 梅同学 · C1 口语冲刺 {STAR}{STAR}{STAR}{STAR}{STAR}<small>2 周前</small></div><p>模拟了 6 次口试，每次都有评分表。考试那天题目刚好是教育话题，一点都不慌。</p></div>
<div class="rv"><div class="h">{av('L','#f7ecd6','#a6752f',26,12)} Lucas · B2 会话 {STAR}{STAR}{STAR}{STAR}{STAR}<small>1 个月前</small></div><p>Très patiente, elle corrige sans jamais interrompre. 课后笔记很详细。</p></div></div></div>
</section>
<aside style="padding-top:30px"><div class="bk"><span class="hand">Réserver un cours</span>
<div class="ls"><div>{ic('spark',15)}<span>试听课<small>25 分钟 · 了解水平与目标</small></span><b>¥ 39</b></div>
<div class="on">{ic('mic',15)}<span>DALF C1 口语模拟<small>50 分钟 · 含评分表</small></span><b>¥ 188</b></div>
<div>{ic('msg',15)}<span>自由会话<small>50 分钟</small></span><b>¥ 158</b></div>
<div>{ic('layers',15)}<span>考前冲刺 · 10 节<small>每节 ¥ 169，省 ¥ 190</small></span><b>¥ 1 690</b></div></div>
<div style="display:flex;justify-content:space-between;font-size:11.5px;color:var(--muted);margin-bottom:8px"><span>可约时间 · 北京时间</span><span>{ic('chevl',11)} 11 月 19 – 25 日 {ic('chev',11)}</span></div>
{cal}<a class="btn">选择时间并预约 {ic('arrow',13)}</a><div class="note">开课前 24 小时可免费取消或改期</div></div></aside>
</div>''', mod='m-tutor')

# ------------------------------------------------------------ 3 · 预约与确认
cal2 = '<div class="cal2"><span></span>' + ''.join(f'<b>{d}</b>' for d in days)
times2 = ['09:00', '10:00', '12:00', '18:30', '19:30', '20:30', '21:30']
sl2 = [['a','','a','','a','a',''], ['','a','a','a','','',''], ['a','a','','','','a','a'], ['','','a','a','a','',''], ['a','a','a','','sel','a',''], ['','a','','a','a','a','a'], ['a','','a','a','','','a']]
for r, t in enumerate(times2):
    cal2 += f'<small>{t}</small>' + ''.join(f'<i class="{sl2[c][r]}">{("19:30" if sl2[c][r]=="sel" else "")}</i>' for c in range(7))
cal2 += '</div>'
tutor3 = page('找老师 · 预约课程', topnav('tutor') + f'''
<style>{AV_CSS}
.wrap{{padding:26px 72px 0;display:grid;grid-template-columns:1fr 400px;gap:32px}}
.steps{{display:flex;gap:10px;align-items:center;margin-bottom:22px;font-size:12.5px;color:var(--faint)}}
.steps span{{display:flex;align-items:center;gap:8px}}
.steps i{{width:24px;height:24px;border-radius:50%;display:grid;place-items:center;font-style:normal;font-size:11px;border:1px solid var(--line-2)}}
.steps .done i{{background:var(--rose-soft);color:var(--rose);border-color:transparent}}
.steps .on{{color:var(--ink)}}.steps .on i{{background:var(--rose);color:#fff;border-color:var(--rose)}}
.steps em{{flex:0 0 40px;height:1px;background:var(--line-2)}}
h1{{font-family:var(--serif-zh);font-size:26px;font-weight:600;color:#33262f}}
.sub{{font-size:12.5px;color:var(--muted);margin:6px 0 18px}}
.tz{{display:flex;align-items:center;gap:10px;margin-bottom:12px;font-size:12px;color:var(--muted)}}
.tz .r{{margin-left:auto;display:flex;gap:8px}}
.cal2{{display:grid;grid-template-columns:56px repeat(7,1fr);gap:6px;text-align:center}}
.cal2 b{{font-weight:500;font-size:12px;color:#5c4e57;padding-bottom:6px}}
.cal2 small{{font-size:11px;color:var(--faint);text-align:left;align-self:center}}
.cal2 i{{height:42px;border-radius:10px;background:#f6f2f0;font-style:normal;display:grid;place-items:center;font-size:12px}}
.cal2 i.a{{background:#fff;border:1px solid #ecc9c2;color:var(--rose)}}
.cal2 i.a:before{{content:'可约';font-size:11px}}
.cal2 i.sel{{background:var(--rose);color:#fff;box-shadow:0 8px 20px #a65f5844;font-weight:600}}
.leg{{display:flex;gap:16px;margin-top:14px;font-size:11px;color:var(--muted)}}
.leg i{{display:inline-block;width:12px;height:12px;border-radius:3px;vertical-align:-2px;margin-right:5px}}
.od{{border-radius:22px;background:#fffdfb;border:1px solid var(--line);padding:24px;box-shadow:0 18px 50px #a65f5812}}
.od .hand{{font-size:17px;color:var(--rose)}}
.od .t{{display:flex;gap:14px;align-items:center;margin:14px 0;padding-bottom:16px;border-bottom:1px dashed var(--line-2)}}
.od .t b{{font-size:15px;color:#33262f}}
.od .t small{{display:block;font-size:11.5px;color:var(--muted)}}
.od .kv{{display:flex;flex-direction:column;gap:11px;font-size:12.5px;color:#5c4e57;padding-bottom:16px;border-bottom:1px dashed var(--line-2)}}
.od .kv div{{display:flex;justify-content:space-between}}
.od .kv span:first-child{{color:var(--muted)}}
.od textarea{{width:100%;height:76px;margin-top:14px;border:1px solid var(--line);border-radius:12px;padding:10px 12px;font:12px/1.7 var(--sans);color:#5c4e57;resize:none;background:#fff}}
.od .lk{{display:flex;gap:6px;margin-top:8px;flex-wrap:wrap}}
.od .tot{{display:flex;align-items:baseline;justify-content:space-between;margin-top:16px}}
.od .tot b{{font:400 30px var(--serif-fr);color:#33262f}}
.od .pay{{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:14px}}
.od .pay span{{height:40px;border-radius:12px;border:1px solid var(--line);display:flex;align-items:center;justify-content:center;gap:6px;font-size:12px;color:#5c4e57}}
.od .pay .on{{border-color:#e2bcb5;background:#fcf3f1;color:var(--rose)}}
.od .btn{{width:100%;justify-content:center;margin-top:14px;background:var(--rose);color:#fff;height:46px;font-size:13.5px}}
</style>
<div class="wrap m-tutor"><section>
<div class="steps"><span class="done"><i>{ic('check',12)}</i>选择课程</span><em></em><span class="on"><i>2</i>选择时间</span><em></em><span><i>3</i>确认并支付</span></div>
<h1>选一个上课时间</h1><div class="sub">Camille 每周更新可约时段。选择后会锁定 10 分钟，等你完成支付。</div>
<div class="tz">{ic('globe',14)} 北京时间 (UTC+8) · 老师所在地 里昂 (UTC+1)<div class="r"><span class="chip line">{ic('chevl',11)}</span><span class="chip line">11 月 19 – 25 日</span><span class="chip line">{ic('chev',11)}</span></div></div>
{cal2}
<div class="leg"><span><i style="background:#fff;border:1px solid #ecc9c2"></i>可预约</span><span><i style="background:var(--rose)"></i>已选择</span><span><i style="background:#f6f2f0"></i>已约满 / 休息</span><span style="margin-left:auto">{ic('repeat',12)} 设为每周固定时间</span></div>
</section>
<aside><div class="od"><span class="hand">Votre réservation</span>
<div class="t">{av('CD','#ecd8d1','#a65f58',54,20)}<div><b>Camille Durand</b><small>DALF C1 口语模拟 · 50 分钟</small></div></div>
<div class="kv"><div><span>时间</span><span>11 月 23 日 周一 19:30 – 20:20</span></div><div><span>上课方式</span><span>胡桃课堂（浏览器直接进入）</span></div><div><span>取消政策</span><span>开课前 24 小时免费</span></div></div>
<textarea>想练习 C1 口语「Faut-il tout noter ?」这道题，希望重点纠正连接词和论证结构。</textarea>
<div class="lk"><span class="chip rose">{ic('library',11)} 附上题库：Faut-il tout noter ?</span><span class="chip line">{ic('note',11)} 分享我的生词本</span></div>
<div class="tot"><span style="font-size:12px;color:var(--muted)">合计</span><b>¥ 188</b></div>
<div class="pay"><span class="on">{ic('card',14)} 微信支付</span><span>{ic('card',14)} 支付宝</span></div>
<a class="btn">确认预约并支付 {ic('arrow',14)}</a></div></aside>
</div>''', mod='m-tutor')

# ------------------------------------------------------------ 4 · 我的课程
tutor4 = page('找老师 · 我的课程', topnav('tutor') + f'''
<style>{AV_CSS}
.wrap{{padding:26px 72px 0;display:grid;grid-template-columns:1fr 380px;gap:30px}}
.head .hand{{font-size:24px;color:var(--rose)}}
.head h1{{font-family:var(--serif-zh);font-size:28px;font-weight:600;color:#33262f;margin:2px 0 16px}}
.next{{display:flex;gap:22px;align-items:center;padding:22px 26px;border-radius:22px;background:linear-gradient(120deg,#3c2b34,#6b4650);color:#fff;margin-bottom:18px}}
.next .hand{{font-size:16px;color:#f3c9c0}}
.next b{{display:block;font-size:20px;font-weight:500;margin:4px 0}}
.next small{{font-size:12px;color:#e8d4d8}}
.next .cd{{margin-left:auto;text-align:center}}
.next .cd b{{font-family:var(--hand);font-size:24px}}
.next .btn{{background:#fff;color:var(--rose)}}
.ls{{display:flex;flex-direction:column;gap:10px}}
.ls .it{{display:flex;align-items:center;gap:16px;padding:14px 18px;border-radius:16px;background:#fffdfb;border:1px solid var(--line)}}
.ls .d{{width:76px;white-space:nowrap;text-align:center;border-right:1px solid var(--line);padding-right:14px}}
.ls .d b{{display:block;font-family:var(--hand);font-size:24px;color:var(--rose);line-height:1}}
.ls .d small{{font-size:10.5px;color:var(--faint)}}
.ls .it .t{{flex:1}}
.ls .it .t b{{font-size:13.5px;color:#33262f;font-weight:500}}
.ls .it .t small{{display:block;font-size:11.5px;color:var(--muted);margin-top:3px}}
.nt{{border-radius:20px;background:#fffdfb;border:1px solid var(--line);padding:20px 22px}}
.nt .hand{{font-size:17px;color:var(--rose)}}
.nt h4{{font-size:13px;color:#33262f;margin:8px 0 10px;font-weight:500}}
.nt .sc{{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:12px}}
.nt .sc div{{padding:9px 12px;border-radius:10px;background:#fbf6f4;font-size:11.5px;color:#6c5e67;display:flex;justify-content:space-between}}
.nt .sc b{{font-family:var(--hand);color:var(--rose);font-size:14px}}
.nt .fix{{font:13px/1.8 var(--serif-fr);color:#4c4049;padding:10px 0;border-top:1px dashed var(--line-2)}}
.nt .fix s{{color:#c0817c}}.nt .fix b{{color:var(--sage)}}
.nt .ws{{display:flex;flex-wrap:wrap;gap:6px;margin-top:6px}}
.nt .sync{{margin-top:14px;font-size:11.5px;color:var(--sage);display:flex;gap:6px;align-items:center}}
.msg{{margin-top:14px;border-radius:20px;background:#fffdfb;border:1px solid var(--line);padding:16px 18px}}
.msg .b{{display:flex;gap:10px;margin-top:10px}}
.msg .b p{{font-size:12px;line-height:1.7;color:#4c4049;background:#f8f3f1;padding:9px 12px;border-radius:4px 14px 14px 14px}}
.msg .b.me{{flex-direction:row-reverse}}.msg .b.me p{{background:var(--rose-soft);border-radius:14px 4px 14px 14px}}
</style>
<div class="wrap m-tutor"><section>
<div class="head"><span class="hand">Mes cours</span><h1>我的课程</h1></div>
<div class="next">{av('CD','#ecd8d1','#a65f58',60,22)}<div><span class="hand">Prochain cours</span><b>DALF C1 口语模拟 · Camille Durand</b><small>11 月 23 日 周一 19:30 · 题目：Faut-il tout noter ?</small></div><div class="cd"><b>3 天 6 小时</b><small style="display:block">距离上课</small></div><a class="btn">{ic('video',14)} 进入课堂</a></div>
<div class="tabs"><a class="on">即将开始 · 2</a><a>已完成 · 14</a><a>课时包 · 剩余 6 节</a></div>
<div class="ls">
<div class="it"><div class="d"><b>23</b><small>11 月 · 周一</small></div>{av('CD','#ecd8d1','#a65f58',40,15)}<div class="t"><b>DALF C1 口语模拟</b><small>19:30 – 20:20 · 已附题库与生词本</small></div><span class="chip rose">已确认</span><span class="chip line">改期</span></div>
<div class="it"><div class="d"><b>26</b><small>11 月 · 周四</small></div>{av('王','#dfe7da','#5f7759',40,15)}<div class="t"><b>语法答疑 · 虚拟式与条件式</b><small>王思敏 · 20:00 – 20:50 · 对应系统学习 B2 第 2 单元</small></div><span class="chip sage">已确认</span><span class="chip line">改期</span></div>
<div class="it" style="opacity:.75"><div class="d"><b style="color:var(--faint)">16</b><small>11 月 · 周日</small></div>{av('LM','#e2e7f1','#566d8e',40,15)}<div class="t"><b>新闻精读 · Les forêts françaises face à la sécheresse</b><small>Léa Martin · 已完成 · 待评价</small></div><span class="chip line">{STAR} 去评价</span></div>
</div></section>
<aside style="padding-top:12px"><div class="nt"><span class="hand">Notes du professeur</span><h4>11 月 16 日 · C1 口语模拟 · Camille 的课后笔记</h4>
<div class="sc"><div>论证结构<b>4 / 5</b></div><div>词汇丰富度<b>3.5 / 5</b></div><div>语法准确<b>3 / 5</b></div><div>流利度<b>4 / 5</b></div></div>
<div class="fix">Bien que ce <s>est</s> → <b>soit</b> une bonne idée…</div>
<div class="fix">Il faut <s>prendre en compte de</s> → <b>tenir compte de</b> l’avis des élèves.</div>
<div class="ws"><span class="chip rose">nuancer</span><span class="chip rose">en revanche</span><span class="chip rose">il n’en demeure pas moins que</span></div>
<div class="sync">{ic('check',13)} 3 个表达已加入生词本 · 1 个语法点已推送到系统学习</div></div>
<div class="msg"><span class="hand" style="font-size:15px;color:var(--rose)">Messages</span>
<div class="b">{av('CD','#ecd8d1','#a65f58',28,11)}<p>Pour lundi, prépare une introduction avec une problématique claire. À bientôt !</p></div>
<div class="b me"><p>Merci Camille, je vous envoie mon plan dimanche.</p></div></div></aside>
</div>''', mod='m-tutor')

PAGES = {
    '41-tutor-discover': tutor1,
    '42-tutor-profile': tutor2,
    '43-tutor-booking': tutor3,
    '44-tutor-my-lessons': tutor4,
}
