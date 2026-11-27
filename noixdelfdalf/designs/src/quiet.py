"""Quiet versions of the section pages: same layouts, restrained colour (q-*.html)."""
import f_learn, f_read, f_bank, f_tutor

LINK = '<link rel="stylesheet" href="final.css">'
QLINK = LINK + '<link rel="stylesheet" href="quiet.css">'

# page-specific touches so that solid colour blocks turn into quiet white cards
FIX = {
    'f11-learn-overview': [
        ('.cont{display:flex;align-items:center;gap:20px;padding:18px 26px;background:var(--mint);', '.cont{display:flex;align-items:center;gap:20px;padding:18px 26px;background:#fff;border:1px solid #e8e1d7;'),
        ('.th{padding:18px 20px;position:relative;min-height:132px}', '.th{padding:18px 20px;position:relative;min-height:132px;background:#fff!important;border:1px solid #e8e1d7}.th .fr{color:var(--green)}'),
    ],
    'f12-learn-grammar-lesson': [
        ('<div class="flat c1" style="background:var(--green);color:var(--cream)"><span class="fr" style="color:#cfe6d6">Exercices</span>',
         '<div class="flat c1" style="background:#fff;border:1px solid #e8e1d7"><span class="fr" style="color:var(--green)">Exercices</span>'),
        ('<small style="color:#d8ebde">填空 · 选择 · 句型转换 · 约 8 分钟</small><a class="btn" style="background:var(--cream);color:var(--green);',
         '<small style="color:var(--soft)">填空 · 选择 · 句型转换 · 约 8 分钟</small><a class="btn" style="background:var(--navy);color:#fff;'),
        ('.lead{font-size:14px;line-height:2;color:var(--ink2);padding:14px 18px;background:var(--mint);border-radius:14px}',
         '.lead{font-size:14px;line-height:2;color:var(--ink2);padding:4px 0 4px 18px;border-left:2px solid var(--green)}'),
        ('.c1{padding:18px 20px}', '.c1{padding:18px 20px;border:1px solid #e8e1d7}.c1 .fr{color:var(--green)!important}'),
    ],
    'f21-read-kiosk': [
        ('.au{display:flex;gap:12px;align-items:center;padding:22px 18px;background:var(--sky);', '.au{display:flex;gap:12px;align-items:center;padding:22px 18px;background:#fff;border:1px solid #e8e1d7;'),
        ('.it2 .dot{width:12px;height:12px;', '.it2 .dot{width:8px;height:8px;background:var(--blue)!important;'),
    ],
    'f22-read-article': [
        ('.mini{display:flex;align-items:center;gap:12px;margin:16px 0 20px;padding:10px 14px;background:var(--sky)}',
         '.mini{display:flex;align-items:center;gap:12px;margin:16px 0 20px;padding:10px 14px;background:#fff;border:1px solid #e8e1d7}'),
        ('.q{margin-top:22px;padding:16px 18px}', '.q{margin-top:22px;padding:16px 18px;background:#fff!important;border:1px solid #e8e1d7}.q .o span{border:1px solid #ece6dd}'),
    ],
    'f32-bank-c1-library': [
        ('.ex .bt b{margin-left:auto;width:26px;height:26px;border-radius:50%;display:grid;place-items:center;background:var(--peach);color:#8a4325}',
         '.ex .bt b{margin-left:auto;width:26px;height:26px;border-radius:50%;display:grid;place-items:center;border:1px solid #e8e1d7;color:var(--orange)}'),
        ('--tint:#efe1f2a8', '--tint:#fbf9f7d0'),
    ],
    'f33-bank-practice': [('.qn .a{background:var(--lav);color:var(--plum)}', '.qn .a{background:#f1ede7;color:var(--navy)}')],
    'f41-tutor-discover': [('.price .num{font-size:28px}', '.price .num{font-size:28px}.av{background:#f4efe9!important;color:var(--red)!important}')],
    'f42-tutor-profile': [
        ('.vid .tint{position:absolute;inset:6px;border-radius:8px;background:#f3d3cf70}', '.vid .tint{position:absolute;inset:6px;border-radius:8px;background:#fbf9f7b0}'),
        ('.ls .on{background:var(--blush)}', '.ls .on{background:#fff;outline:1.5px solid var(--red)}.ls div{background:#faf8f5}.av{background:#f4efe9!important;color:var(--red)!important}'),
    ],
}

PAGES = {}
for mod in (f_learn, f_read, f_bank, f_tutor):
    for k, html in mod.PAGES.items():
        if k not in FIX:
            continue
        h = html.replace(LINK, QLINK)
        for a, b in FIX[k]:
            assert a in h, (k, a[:60])
            h = h.replace(a, b)
        PAGES['q' + k[1:]] = h
