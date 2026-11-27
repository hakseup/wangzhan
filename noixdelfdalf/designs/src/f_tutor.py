from common import ic
from fcommon import nav, head, tabs, fpage, hb

STAR = ic('star', 12, 'fill:#e1a23a;stroke:#e1a23a')

def av(init, bg, fg, size=64, fs=24, on=False):
    dot = '<i class="on"></i>' if on else ''
    return f'<span class="av" style="width:{size}px;height:{size}px;background:{bg};color:{fg};font-size:{fs}px">{init}{dot}</span>'

AV_CSS = '.av .on{position:absolute;right:2px;bottom:2px;width:13px;height:13px;border-radius:50%;background:#6fae7f;border:2px solid var(--cream)}'
PHOTO_CSS = '.ph3{position:relative;border-radius:12px}.ph3 .img{position:absolute;inset:6px;border-radius:8px;background:var(--img)}'

T = [('CD', 'Camille Durand', 'var(--blush)', 'var(--red)', '法国 · 里昂', '母语法语 · 会说英语、中文 B1', '4.98', '1 240', '326', '188', '曾任 DELF / DALF 口试考官 6 年。擅长 B2–C1 口语陈述与辩论，课上用真题模拟，课后给逐项评分表。', ['考官经历', '口语', '考试冲刺', 'B2–C1'], 'url(../assets/paris-haze.png) 20% 30%/300%'),
     ('王', '王思敏', 'var(--mint)', 'var(--green)', '中国 · 上海', '母语中文 · 法语 C2 · 索邦大学硕士', '4.95', '860', '214', '128', '用中文把语法讲透：时态、虚拟式、关系代词一张图理清。零基础到 B1 的学员最多，可以配合「系统学习」进度上课。', ['中文授课', '语法', '零基础', 'A1–B1'], 'url(../assets/arc-haze.png) 80% 70%/300%'),
     ('LM', 'Léa Martin', 'var(--sky)', 'var(--blue)', '法国 · 波尔多', '母语法语 · 会说英语', '4.92', '530', '148', '158', '每节课一篇法国新闻：先精读，再讨论，最后纠音。适合想把「阅读精听」里的内容说出口的同学。', ['新闻精读', '发音纠正', '会话', 'B1–C1'], 'url(../assets/arc-haze.png) 45% 40%/300%')]

# ------------------------------------------------------------ 1 · 浏览老师
rows = ''
for init, name, bg, fg, place, langs, rate, les, stu, price, intro, tags, img in T:
    tg = ''.join(f'<span class="pill {"blush" if i == 0 else "ghost"}">{t}{hb("#cfc6bb") if i else ""}</span>' for i, t in enumerate(tags))
    rows += f'''<div class="row"><div class="box l">{hb()}{av(init, bg, fg, 84, 30, True)}
<div class="info"><div class="nm"><b class="zh">{name}</b><span class="pill mint">{ic('shield',11)} 已认证</span></div><small>{place} · {langs}</small><div class="tg">{tg}</div><p>{intro}</p></div>
<div class="pr"><div>{STAR} <b class="num" style="color:var(--navy)">{rate}</b><small>{stu} 位学员 · {les} 节课</small></div><div class="price"><span class="fr num">¥{price}</span><small>50 分钟 · 试听 ¥39</small></div><a class="btn solid sm" style="background:var(--red)">预约试听</a><a class="btn line sm">{ic('msg',13)} 发消息{hb()}</a></div></div>
<div class="ph3 vd" style="--img:{img}"><div class="img"></div><span class="pl">{ic('play',16)}</span><div class="sl"><small>本周可约</small><div>{''.join(f'<i class="{c}"></i>' for c in ['a','a','','a','b','a','','','a','a','a','','b','a'])}</div></div>{hb('var(--orange)','thick')}</div></div>'''
flt = ''.join(f'<div class="f"><small>{a}</small><span>{b} {ic("chevd",11)}</span></div>' for a, b in [('我想学', 'DELF / DALF 备考'), ('授课语言', '法语 · 中文'), ('价格 / 50 分钟', '¥80 – 250'), ('可上课时间', '工作日晚上')])
tutor1 = fpage('找老师 · 浏览老师', nav('tutor') + head('Trouver un prof', '找老师', '先看 1 分钟视频，再约一节 25 分钟试听课。课后笔记和生词同步到你的学习记录。',
               f'<a class="btn line sm">{ic("calendar",13)} 我的课程{hb()}</a><a class="btn line sm">{ic("user",13)} 成为老师{hb()}</a>') + f'''
<div class="wrap"><div class="box fb">{hb()}{flt}<div class="chips"><span class="pill blush">母语老师</span><span class="pill ghost">考官经历{hb('#cfc6bb')}</span><span class="pill ghost">口语{hb('#cfc6bb')}</span></div><span class="cnt zh">找到 <b class="num">48</b> 位老师</span></div>
{rows}</div>''', 'm-tutor', AV_CSS + PHOTO_CSS + '''
.fb{display:flex;align-items:center;gap:6px;padding:10px 16px;margin-bottom:16px}
.fb .f{display:flex;flex-direction:column;padding:2px 16px;border-right:1px dashed var(--rule)}.fb .f small{font-size:10.5px;color:var(--soft)}.fb .f span{font-family:var(--zh);font-size:14px;display:flex;gap:6px;align-items:center}
.fb .chips{display:flex;gap:6px;margin-left:8px}.fb .cnt{margin-left:auto;font-size:13px;color:var(--ink2)}.fb .cnt b{font-size:17px}
.row{display:grid;grid-template-columns:1fr 330px;gap:16px;margin-bottom:14px}
.l{display:flex;gap:20px;padding:18px 22px}.info{flex:1}
.nm{display:flex;gap:10px;align-items:center}.nm b{font-size:20px}
.l small{font-size:11.5px;color:var(--soft)}.tg{display:flex;gap:6px;margin:8px 0}.l p{font-size:12.5px;line-height:1.85;color:var(--ink2)}
.pr{width:170px;display:flex;flex-direction:column;gap:7px;border-left:1px dashed var(--rule);padding-left:18px;font-size:12px}
.pr small{display:block}.price .num{font-size:28px}.pr .btn{justify-content:center}
.vd .pl{position:absolute;left:50%;top:40%;transform:translate(-50%,-50%);width:46px;height:46px;border-radius:50%;background:var(--cream);color:var(--red);display:grid;place-items:center}
.vd .sl{position:absolute;left:18px;right:18px;bottom:16px;background:#fffdf8e6;border-radius:10px;padding:6px 10px}.vd .sl small{font-size:10.5px;color:var(--ink2);font-family:var(--zh)}
.vd .sl div{display:grid;grid-template-columns:repeat(14,1fr);gap:3px;margin-top:4px}.vd .sl i{height:12px;border-radius:3px;background:#ece5da}.vd .sl i.a{background:var(--blush)}.vd .sl i.b{background:var(--orange)}''')

# ------------------------------------------------------------ 2 · 老师主页
init, name, bg, fg, place, langs, rate, les, stu, price, intro, tags, img = T[0]
days = ['周四 26', '周五 27', '周六 28', '周日 29', '周一 30', '周二 1', '周三 2']
sl = [['', 'a', 'a', '', 'a'], ['a', '', 'a', 'a', ''], ['a', 'a', '', '', ''], ['', '', 'a', 'a', 'a'], ['a', 'a', 'a', '', 'a'], ['', 'a', '', 'a', 'a'], ['a', '', 'a', 'a', '']]
times = ['09:00', '12:00', '18:30', '19:30', '20:30']
cal = '<div class="cal"><span></span>' + ''.join(f'<b>{d}</b>' for d in days) + ''.join(f'<small>{t}</small>' + ''.join(f'<i class="{sl[c][r]}"></i>' for c in range(7)) for r, t in enumerate(times)) + '</div>'
tutor2 = fpage('找老师 · 老师主页', nav('tutor') + f'''
<div class="wrap g"><section><div class="crumb">找老师 › {name}</div>
<div class="hero">{av(init, bg, fg, 92, 34, True)}<div><b class="zh" style="font-size:28px">{name}</b> <span class="pill blush" style="vertical-align:6px">{ic('shield',11)} DELF / DALF 考官经历</span><div style="font-size:12.5px;color:var(--soft);margin-top:2px">{place} · {langs} · 当地时间 13:40</div>
<div style="display:flex;gap:6px;margin-top:8px">{''.join(f'<span class="pill ghost">{t}{hb("#cfc6bb")}</span>' for t in ['口语陈述','辩论','写作批改','B2–C1'])}</div></div>
<div class="nums"><div><b class="num">{rate}</b><small>{STAR} 评分</small></div><div><b class="num">{les}</b><small>节课</small></div><div><b class="num">98%</b><small>出勤率</small></div></div></div>
<div class="ph3 vid" style="--img:url(../assets/paris-haze.png) 30% 40%/cover"><div class="img"></div><div class="tint"></div><div class="q"><span class="fr" style="font-size:30px;line-height:1.3">« Parler, c’est déjà gagner la moitié de l’épreuve. »</span><small class="zh">开口，就已经赢了口试的一半。—— 自我介绍视频 1:20</small></div><span class="pl">{ic('play',20)}</span>{hb('var(--orange)','thick')}</div>
<div class="tabs" style="padding:0;margin:18px 0 14px">{''.join(f'<a class="{"on" if i==0 else ""}">{t}</a>' for i,t in enumerate(['关于我','课程','学员评价 · 326','教学资料']))}</div>
<div class="two"><div><h3 class="zh">我会怎样上课</h3><p>{intro}每节课从你在「题库练习」里的口语题开始：10 分钟准备、陈述、辩论，再逐条讲解语法和表达。</p></div>
<div><div class="box rv">{hb('#cfc6bb')}<div class="h">{av('M','var(--lav)','var(--plum)',26,12)} 梅同学 · C1 口语冲刺 {STAR*5}<small>2 周前</small></div><p>模拟了 6 次口试，每次都有评分表。考试那天题目刚好是教育话题，一点都不慌。</p></div>
<div class="box rv">{hb('#cfc6bb')}<div class="h">{av('L','var(--butter)','var(--amber)',26,12)} Lucas · B2 会话 {STAR*5}<small>1 个月前</small></div><p>Très patiente, elle corrige sans jamais interrompre. 课后笔记很详细。</p></div></div></div></section>
<aside class="box bk">{hb()}<span class="label">Réserver un cours</span>
<div class="ls"><div>{ic('spark',15)}<span>试听课<small>25 分钟 · 了解水平和目标</small></span><b class="num">¥39</b></div>
<div class="on">{ic('mic',15)}<span>DALF C1 口语模拟<small>50 分钟 · 含评分表</small></span><b class="num">¥188</b>{hb('var(--orange)')}</div>
<div>{ic('msg',15)}<span>自由会话<small>50 分钟</small></span><b class="num">¥158</b></div><div>{ic('layers',15)}<span>考前冲刺 · 10 节<small>每节 ¥169，省 ¥190</small></span><b class="num">¥1690</b></div></div>
<div style="display:flex;justify-content:space-between;font-size:12px;color:var(--soft);margin-bottom:8px;font-family:var(--zh)"><span>可约时间 · 北京时间</span><span>11 月 26 日 – 12 月 2 日</span></div>{cal}
<a class="btn solid" style="width:100%;justify-content:center;margin-top:16px;background:var(--red)">选择时间并预约 {ic('arrow',13)}</a><div style="font-size:11px;color:var(--soft);text-align:center;margin-top:8px">开课前 24 小时可免费取消或改期</div></aside></div>''', 'm-tutor', AV_CSS + PHOTO_CSS + '''
.g{display:grid;grid-template-columns:1fr 370px;gap:34px;padding-top:22px}
.hero{display:flex;gap:20px;align-items:center}
.nums{margin-left:auto;display:flex;gap:26px;text-align:center}.nums b{display:block;font-size:28px}.nums small{font-size:11.5px;color:var(--soft);font-family:var(--zh)}
.vid{height:240px;margin-top:18px}.vid .tint{position:absolute;inset:6px;border-radius:8px;background:#f3d3cf70}
.vid .q{position:absolute;left:34px;bottom:26px;max-width:520px;color:var(--navy)}.vid .q small{display:block;margin-top:6px;font-size:13px}
.vid .pl{position:absolute;right:40px;bottom:34px;width:56px;height:56px;border-radius:50%;background:var(--cream);color:var(--red);display:grid;place-items:center}
.two{display:grid;grid-template-columns:1fr 1fr;gap:22px}.two h3{font-size:17px;margin-bottom:6px}.two p{font-size:12.5px;line-height:1.95;color:var(--ink2)}
.rv{padding:12px 16px;margin-bottom:10px}.rv .h{display:flex;align-items:center;gap:8px;font-size:12px;font-family:var(--zh)}.rv .h small{margin-left:auto;font-size:11px;color:var(--soft)}.rv p{font-size:12px;line-height:1.8;margin-top:4px}
.bk{padding:22px;align-self:start;margin-top:26px}
.ls{display:flex;flex-direction:column;gap:8px;margin:12px 0 16px}
.ls div{display:flex;align-items:center;gap:10px;padding:10px 14px;border-radius:12px;font-size:13px;font-family:var(--zh);position:relative;background:var(--cream)}
.ls div small{display:block;font-size:11px;color:var(--soft);font-family:var(--sans)}.ls div b{margin-left:auto;font-size:17px}.ls .on{background:var(--blush)}
.cal{display:grid;grid-template-columns:40px repeat(7,1fr);gap:4px;font-size:10px;color:var(--soft);text-align:center}.cal b{font-weight:400;font-family:var(--zh)}.cal small{text-align:left;align-self:center}
.cal i{height:20px;border-radius:5px;background:#efe8dd}.cal i.a{background:var(--blush)}''')

# ------------------------------------------------------------ 3 · 预约
times2 = ['09:00', '10:00', '12:00', '18:30', '19:30', '20:30', '21:30']
s2 = [['a','','a','','a','a',''], ['','a','a','a','','',''], ['a','a','','','','a','a'], ['','','a','a','a','',''], ['a','a','a','','sel','a',''], ['','a','','a','a','a','a'], ['a','','a','a','','','a']]
cal2 = '<div class="cal2"><span></span>' + ''.join(f'<b class="zh">{d}</b>' for d in days)
for r, t in enumerate(times2):
    cal2 += f'<small class="num" style="color:var(--soft)">{t}</small>' + ''.join(f'<i class="{s2[c][r]}">{("<span class=num style=color:#fff>19:30</span>" if s2[c][r]=="sel" else ("可约" if s2[c][r]=="a" else ""))}{hb("#e2b6ad") if s2[c][r]=="a" else ""}</i>' for c in range(7))
cal2 += '</div>'
tutor3 = fpage('找老师 · 预约课程', nav('tutor') + f'''
<div class="wrap g"><section><div class="steps"><span class="d"><i>{ic('check',12)}</i>选择课程</span><em></em><span class="on"><i class="fr">2</i>选择时间</span><em></em><span><i class="fr">3</i>确认并支付</span></div>
<span class="fr" style="color:var(--red);font-size:20px">Choisir un créneau</span><h1 class="zh" style="font-size:28px">选一个上课时间</h1><p style="font-size:13px;color:var(--ink2);margin:4px 0 16px">Camille 每周更新可约时段。选好后为你保留 10 分钟，等你完成支付。</p>
<div class="tz">{ic('globe',14)} 北京时间 (UTC+8) · 老师所在地 里昂 (UTC+1)<span style="margin-left:auto" class="pill ghost">‹ 11 月 26 日 – 12 月 2 日 ›{hb('#cfc6bb')}</span></div>{cal2}
<div class="lg"><span><i style="background:var(--paper);outline:1.5px solid #e2b6ad"></i>可预约</span><span><i style="background:var(--orange)"></i>已选择</span><span><i style="background:#efe8dd"></i>已约满 / 休息</span><span style="margin-left:auto">{ic('repeat',12)} 设为每周固定时间</span></div></section>
<aside class="box od">{hb(None,'thick')}<span class="label">Votre réservation</span>
<div class="t">{av('CD','var(--blush)','var(--red)',54,20)}<div><b class="zh" style="font-size:17px">Camille Durand</b><small>DALF C1 口语模拟 · 50 分钟</small></div></div>
<div class="kv"><div><span>时间</span><span>11 月 30 日 周一 19:30 – 20:20</span></div><div><span>上课方式</span><span>胡桃课堂（浏览器直接进入）</span></div><div><span>取消政策</span><span>开课前 24 小时免费</span></div></div>
<div class="flat note">想练 C1 口语「Faut-il tout noter ?」这道题，希望重点纠正连接词和论证结构。</div>
<div style="display:flex;gap:6px;margin-top:8px;flex-wrap:wrap"><span class="pill blush">{ic('library',11)} 附上题库：Faut-il tout noter ?</span><span class="pill ghost">{ic('note',11)} 分享我的生词本{hb('#cfc6bb')}</span></div>
<div class="tot"><span class="zh">合计</span><b class="fr num">¥188</b></div>
<div class="pay"><span class="on">微信支付{hb('var(--red)')}</span><span>支付宝{hb('#cfc6bb')}</span></div>
<a class="btn solid" style="width:100%;justify-content:center;margin-top:14px;height:46px;font-size:15px;background:var(--red)">确认预约并支付 {ic('arrow',14)}</a></aside></div>''', 'm-tutor', AV_CSS + '''
.g{display:grid;grid-template-columns:1fr 400px;gap:34px;padding-top:24px}
.steps{display:flex;gap:10px;align-items:center;margin-bottom:18px;font-size:13px;color:var(--soft);font-family:var(--zh)}
.steps span{display:flex;align-items:center;gap:8px}.steps i{width:26px;height:26px;border-radius:50%;display:grid;place-items:center;font-style:normal;font-size:14px;background:#efe8dd}
.steps .d i{background:var(--mint);color:var(--green)}.steps .on{color:var(--navy)}.steps .on i{background:var(--red);color:#fff}.steps em{flex:0 0 40px;height:1.5px;background:var(--rule)}
.tz{display:flex;align-items:center;gap:8px;font-size:12.5px;color:var(--ink2);margin-bottom:12px}
.cal2{display:grid;grid-template-columns:56px repeat(7,1fr);gap:6px;text-align:center}.cal2 b{font-weight:400;font-size:13px;padding-bottom:4px}.cal2 small{text-align:left;align-self:center;font-size:14px}
.cal2>i{height:42px;border-radius:10px;background:#efe8dd;font-style:normal;display:grid;place-items:center;font-size:12px;font-family:var(--zh);color:var(--red);position:relative}
.cal2>i.a{background:var(--paper)}.cal2>i.sel{background:var(--orange);font-size:16px}
.lg{display:flex;gap:18px;margin-top:14px;font-size:12px;color:var(--ink2);font-family:var(--zh)}.lg i{display:inline-block;width:12px;height:12px;border-radius:3px;vertical-align:-2px;margin-right:5px}
.od{padding:24px}
.od .t{display:flex;gap:14px;align-items:center;margin:12px 0;padding-bottom:14px;border-bottom:1px dashed var(--rule)}.od .t small{display:block;font-size:12px;color:var(--soft)}
.kv{display:flex;flex-direction:column;gap:10px;font-size:12.5px;padding-bottom:14px;border-bottom:1px dashed var(--rule)}.kv div{display:flex;justify-content:space-between}.kv span:first-child{color:var(--soft)}
.note{margin-top:14px;padding:12px 14px;background:var(--butter);font-size:12.5px;line-height:1.8;color:var(--ink2)}
.tot{display:flex;justify-content:space-between;align-items:baseline;margin-top:14px}.tot b{font-size:34px}
.pay{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:10px}.pay span{height:40px;border-radius:12px;display:grid;place-items:center;font-size:13px;font-family:var(--zh);position:relative}.pay .on{background:var(--blush);color:var(--red)}''')

# ------------------------------------------------------------ 4 · 我的课程
tutor4 = fpage('找老师 · 我的课程', nav('tutor') + head('Mes cours', '我的课程', '', f'<a class="btn line sm">{ic("plus",13)} 预约新课程{hb()}</a>') + f'''
<div class="wrap g"><section>
<div class="flat next">{av('CD','var(--blush)','var(--red)',62,22)}<div><span class="fr" style="color:#f3b48f;font-size:16px">Prochain cours</span><b class="zh">DALF C1 口语模拟 · Camille Durand</b><small>11 月 30 日 周一 19:30 · 题目：Faut-il tout noter ?</small></div>
<div class="cd"><b class="fr">3 j 6 h</b><small>距离上课</small></div><a class="btn" style="background:var(--cream);color:var(--red)">{ic('video',14)} 进入课堂</a></div>
<div class="tabs" style="padding:0;margin:18px 0 12px">{''.join(f'<a class="{"on" if i==0 else ""}">{t}</a>' for i,t in enumerate(['即将开始 · 2','已完成 · 14','课时包 · 剩 6 节']))}</div>
<div class="box lr">{hb()}<div class="d"><b class="fr num">30</b><small>11 月 · 周一</small></div>{av('CD','var(--blush)','var(--red)',42,15)}<div class="t"><b class="zh">DALF C1 口语模拟</b><small>19:30 – 20:20 · 已附题库与生词本</small></div><span class="pill blush">已确认</span><span class="pill ghost">改期{hb('#cfc6bb')}</span></div>
<div class="box lr">{hb()}<div class="d"><b class="fr num">3</b><small>12 月 · 周四</small></div>{av('王','var(--mint)','var(--green)',42,15)}<div class="t"><b class="zh">语法答疑 · 虚拟式和条件式</b><small>王思敏 · 20:00 – 20:50 · 对应系统学习 B2 第 2 单元</small></div><span class="pill mint">已确认</span><span class="pill ghost">改期{hb('#cfc6bb')}</span></div>
<div class="box lr" style="opacity:.75">{hb('#cfc6bb')}<div class="d"><b class="fr" style="color:var(--faint)">23</b><small>11 月 · 周日</small></div>{av('LM','var(--sky)','var(--blue)',42,15)}<div class="t"><b class="zh">新闻精读 · Les forêts françaises face à la sécheresse</b><small>Léa Martin · 已完成 · 待评价</small></div><span class="pill butter">{STAR} 去评价</span></div></section>
<aside><div class="flat nt"><span class="fr" style="color:#7a5a18;font-size:18px">Notes du professeur</span><h4 class="zh">11 月 23 日 · C1 口语模拟 · Camille 的课后笔记</h4>
<div class="sc">{''.join(f'<div>{a}<b class="num">{b}</b></div>' for a,b in [('论证结构','4/5'),('词汇丰富度','3.5/5'),('语法准确','3/5'),('流利度','4/5')])}</div>
<div class="fx">Bien que ce <s>est</s> → <b>soit</b> une bonne idée…</div><div class="fx">Il faut <s>prendre en compte de</s> → <b>tenir compte de</b> l’avis des élèves.</div>
<div style="display:flex;gap:6px;flex-wrap:wrap;margin-top:8px"><span class="pill" style="background:var(--paper)">nuancer</span><span class="pill" style="background:var(--paper)">en revanche</span><span class="pill" style="background:var(--paper)">il n’en demeure pas moins que</span></div>
<div style="font-size:12px;color:var(--green);margin-top:12px;display:flex;gap:6px;align-items:center">{ic('check',13)} 3 个表达已进生词本 · 1 个语法点已推送到系统学习</div></div>
<div class="box msg">{hb()}<span class="label">Messages</span><div class="b">{av('CD','var(--blush)','var(--red)',28,11)}<p>Pour lundi, prépare une introduction avec une problématique claire. À bientôt !</p></div><div class="b me"><p>Merci Camille, je vous envoie mon plan dimanche.</p></div></div></aside></div>''', 'm-tutor', AV_CSS + '''
.g{display:grid;grid-template-columns:1fr 400px;gap:32px}
.next{display:flex;gap:20px;align-items:center;padding:20px 26px;background:var(--navy);color:var(--cream)}
.next b{display:block;font-size:20px;margin:2px 0}.next small{font-size:12.5px;color:#cfd0dc}.next .cd{margin-left:auto;text-align:center}.next .cd b{font-size:28px;color:#f3b48f}
.lr{display:flex;align-items:center;gap:16px;padding:14px 20px;margin-bottom:12px}
.lr .d{width:74px;text-align:center;border-right:1px dashed var(--rule);padding-right:12px;white-space:nowrap}.lr .d b{display:block;font-size:28px;line-height:1}.lr .d small{font-size:11px;color:var(--soft)}
.lr .t{flex:1}.lr .t b{font-size:16px}.lr .t small{display:block;font-size:12px;color:var(--soft);margin-top:2px}
.nt{padding:20px 22px;background:var(--butter)}.nt h4{font-size:14px;margin:4px 0 10px}
.sc{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:10px}.sc div{padding:8px 12px;border-radius:10px;background:var(--paper);font-size:12px;display:flex;justify-content:space-between;font-family:var(--zh)}.sc b{font-size:16px}
.fx{font:14px/1.8 var(--serif);padding:6px 0;border-top:1px dashed #e0cf98}.fx s{color:var(--red)}.fx b{color:var(--green)}
.msg{margin-top:16px;padding:16px 18px}.msg .b{display:flex;gap:10px;margin-top:10px}.msg .b p{font-size:12.5px;line-height:1.7;background:var(--cream);padding:8px 12px;border-radius:4px 14px 14px 14px}
.msg .b.me{flex-direction:row-reverse}.msg .b.me p{background:var(--blush);border-radius:14px 4px 14px 14px}''')

PAGES = {'f41-tutor-discover': tutor1, 'f42-tutor-profile': tutor2, 'f43-tutor-booking': tutor3, 'f44-tutor-my-lessons': tutor4}
