"""Shared fragments for the 胡桃法语 platform design mockups."""

ICONS = {
    'search': '<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/>',
    'bell': '<path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"/><path d="M10.3 21a1.9 1.9 0 0 0 3.4 0"/>',
    'arrow': '<path d="M5 12h14"/><path d="m13 6 6 6-6 6"/>',
    'arrowup': '<path d="M7 17 17 7"/><path d="M8 7h9v9"/>',
    'chev': '<path d="m9 6 6 6-6 6"/>',
    'chevl': '<path d="m15 6-6 6 6 6"/>',
    'chevd': '<path d="m6 9 6 6 6-6"/>',
    'book': '<path d="M2 4h6a4 4 0 0 1 4 4v13a3 3 0 0 0-3-3H2z"/><path d="M22 4h-6a4 4 0 0 0-4 4v13a3 3 0 0 1 3-3h7z"/>',
    'grammar': '<path d="M4 19.5V4.5A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1 0-5H20"/><path d="M9 7h7M9 11h5"/>',
    'cards': '<rect x="3" y="6" width="14" height="14" rx="2"/><path d="M7 3h12a2 2 0 0 1 2 2v12"/>',
    'headphones': '<path d="M3 14h3a2 2 0 0 1 2 2v3a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-7a9 9 0 0 1 18 0v7a2 2 0 0 1-2 2h-1a2 2 0 0 1-2-2v-3a2 2 0 0 1 2-2h3"/>',
    'wave': '<path d="M2 10v3M6 6v11M10 3v18M14 8v7M18 5v13M22 10v3"/>',
    'news': '<path d="M4 22h16a2 2 0 0 0 2-2V4a2 2 0 0 0-2-2H8a2 2 0 0 0-2 2v16a2 2 0 0 1-2 2Zm0 0a2 2 0 0 1-2-2v-9c0-1.1.9-2 2-2h2"/><path d="M18 14h-8M15 18h-5M10 6h8v4h-8z"/>',
    'pen': '<path d="M12 20h9"/><path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4Z"/>',
    'mic': '<rect x="9" y="2" width="6" height="12" rx="3"/><path d="M19 10v2a7 7 0 0 1-14 0v-2M12 19v3"/>',
    'library': '<path d="m16 6 4 14M12 6v14M8 8v12M4 4v16"/>',
    'bookmark': '<path d="m19 21-7-4-7 4V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"/>',
    'rotate': '<path d="M3 12a9 9 0 1 0 9-9 9.8 9.8 0 0 0-6.7 2.7L3 8"/><path d="M3 3v5h5"/>',
    'note': '<path d="M13.4 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-7.4"/><path d="M2 6h4M2 10h4M2 14h4M2 18h4"/><path d="M21.4 5.6a2.1 2.1 0 1 0-3-3l-5 5-1 4 4-1z"/>',
    'clock': '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
    'user': '<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>',
    'users': '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.9M16 3.1a4 4 0 0 1 0 7.8"/>',
    'star': '<path d="m12 2 3.1 6.3 6.9 1-5 4.9 1.2 6.8L12 17.8 5.8 21l1.2-6.8-5-4.9 6.9-1z"/>',
    'video': '<path d="m16 13 5.2 3.5a.5.5 0 0 0 .8-.4V7.9a.5.5 0 0 0-.8-.4L16 11"/><rect x="2" y="6" width="14" height="12" rx="2"/>',
    'calendar': '<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/>',
    'msg': '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>',
    'play': '<path d="M7 4v16l13-8z" fill="currentColor"/>',
    'pause': '<path d="M8 5v14M16 5v14" stroke-width="3"/>',
    'back15': '<path d="M3 12a9 9 0 1 0 3-6.7L3 8"/><path d="M3 3v5h5"/>',
    'fwd15': '<path d="M21 12a9 9 0 1 1-3-6.7L21 8"/><path d="M21 3v5h-5"/>',
    'check': '<path d="M20 6 9 17l-5-5"/>',
    'x': '<path d="M18 6 6 18M6 6l12 12"/>',
    'plus': '<path d="M12 5v14M5 12h14"/>',
    'filter': '<path d="M22 3H2l8 9.5V19l4 2v-8.5z"/>',
    'globe': '<circle cx="12" cy="12" r="10"/><path d="M2 12h20M12 2a15 15 0 0 1 0 20 15 15 0 0 1 0-20"/>',
    'heart': '<path d="M19 14c1.5-1.5 3-3.2 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.8 0-3 .5-4.5 2-1.5-1.5-2.7-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4 3 5.5l7 7z"/>',
    'spark': '<path d="M12 3v4M12 17v4M3 12h4M17 12h4M5.6 5.6l2.8 2.8M15.6 15.6l2.8 2.8M5.6 18.4l2.8-2.8M15.6 8.4l2.8-2.8"/>',
    'flame': '<path d="M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.4-.5-2-1-3-1.1-2.1-.2-4.1 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.2.4-2.3 1-3.3.4 1.4 1.3 2.5 2.5 2.8"/>',
    'target': '<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/>',
    'layers': '<path d="m12 2 10 5-10 5L2 7z"/><path d="m2 17 10 5 10-5M2 12l10 5 10-5"/>',
    'lock': '<rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>',
    'volume': '<path d="M11 5 6 9H2v6h4l5 4z"/><path d="M15.5 8.5a5 5 0 0 1 0 7M19 5a10 10 0 0 1 0 14"/>',
    'eye': '<path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12"/><circle cx="12" cy="12" r="3"/>',
    'highlighter': '<path d="m9 11-6 6v3h9l3-3"/><path d="m22 12-4.6 4.6a2 2 0 0 1-2.8 0l-5.2-5.2a2 2 0 0 1 0-2.8L14 4"/>',
    'type': '<path d="M4 7V4h16v3M9 20h6M12 4v16"/>',
    'shield': '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10"/>',
    'card': '<rect x="2" y="5" width="20" height="14" rx="2"/><path d="M2 10h20"/>',
    'home': '<path d="m3 10 9-7 9 7v10a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><path d="M9 22V12h6v10"/>',
    'grid': '<rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/>',
    'chart': '<path d="M3 3v18h18"/><path d="m7 15 4-4 3 3 5-6"/>',
    'repeat': '<path d="m17 2 4 4-4 4"/><path d="M3 11v-1a4 4 0 0 1 4-4h14M7 22l-4-4 4-4"/><path d="M21 13v1a4 4 0 0 1-4 4H3"/>',
    'download': '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M7 10l5 5 5-5M12 15V3"/>',
    'maximize': '<path d="M8 3H5a2 2 0 0 0-2 2v3M21 8V5a2 2 0 0 0-2-2h-3M3 16v3a2 2 0 0 0 2 2h3M16 21h3a2 2 0 0 0 2-2v-3"/>',
    'sun': '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>',
}


def ic(name, size=16, extra=''):
    return f'<svg class="i" style="width:{size}px;height:{size}px;{extra}" viewBox="0 0 24 24">{ICONS[name]}</svg>'


NAV = [
    ('home', '首页', 'Accueil', 'index'),
    ('learn', '系统学习', 'Apprendre', 'learn'),
    ('read', '阅读精听', 'Lire &amp; écouter', 'read'),
    ('bank', '题库练习', 'S’exercer', 'bank'),
    ('tutor', '找老师', 'Professeurs', 'tutor'),
]


def topnav(active, clear=False):
    links = ''.join(
        f'<a class="{"on" if key == active else ""}">{zh}<i>{fr}</i></a>' for key, zh, fr, _ in NAV)
    return f'''<header class="topnav{' clear' if clear else ''}">
  <a class="brand"><img src="../assets/hutao-logo.png" alt=""><span><b>胡桃法语</b><small>Noix · le français</small></span></a>
  <nav class="nav-links">{links}</nav>
  <div class="nav-tools">
    <div class="searchpill">{ic('search', 14)}搜索语法、词汇、文章<kbd>⌘K</kbd></div>
    <span class="iconbtn">{ic('bell', 15)}</span>
    <span class="avatar">H</span>
  </div>
</header>'''


def page(title, body, mod='', cls='', head=''):
    return f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=1440">
<title>{title}</title><link rel="stylesheet" href="noix.css">{head}</head>
<body class="{mod} {cls}">
{body}
</body></html>'''


def rail(items, note=''):
    """items: list of ('h', hand, small) | ('a', icon, label, count, on) | ('sep',)"""
    out = []
    for it in items:
        if it[0] == 'h':
            out.append(f'<div class="rail-h"><span class="hand">{it[1]}</span><small>{it[2]}</small></div>')
        elif it[0] == 'sep':
            out.append('<div class="sep"></div>')
        else:
            _, icon, label, count, on = it
            b = f'<b>{count}</b>' if count != '' else ''
            out.append(f'<a class="{"on" if on else ""}">{ic(icon, 16)}{label}{b}</a>')
    if note:
        out.append(f'<div class="note">{note}</div>')
    return '<aside class="rail">' + ''.join(out) + '</aside>'
