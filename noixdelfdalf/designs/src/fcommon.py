"""Shared fragments for the final-style section pages (f-*.html)."""
from common import ic

WOB = '''<svg width="0" height="0" style="position:absolute"><filter id="wob"><feTurbulence type="fractalNoise" baseFrequency="0.022" numOctaves="1" seed="7"/><feDisplacementMap in="SourceGraphic" scale="1.8"/></filter>
<filter id="wob2"><feTurbulence type="fractalNoise" baseFrequency="0.018" numOctaves="1" seed="2"/><feDisplacementMap in="SourceGraphic" scale="2.6"/></filter></svg>'''

NAVS = [('home', '首页', 'Accueil'), ('learn', '系统学习', 'Apprendre'), ('read', '阅读精听', 'Lire & écouter'),
        ('bank', '题库练习', 'S’exercer'), ('tutor', '找老师', 'Professeurs')]


def hb(c=None, cls=''):
    st = f' style="--bc:{c}"' if c else ''
    return f'<i class="hb {cls}"{st}></i>'


def nav(active):
    links = ''.join(f'<a class="{"on" if k == active else ""}">{z}<i>{f}</i></a>' for k, z, f in NAVS)
    return f'''<header class="nav"><a class="brand"><img src="../assets/hutao-logo.png" alt=""><span><b>胡桃法语</b><small>Noix · le français</small></span></a>
<nav class="links">{links}</nav><span class="search">{ic('search',14)}搜索语法、词汇、文章{hb()}</span><span class="me">H{hb()}</span></header>'''


def head(fr, zh, desc='', right='', crumb=''):
    c = f'<div class="crumb">{crumb}</div>' if crumb else ''
    d = f'<p>{desc}</p>' if desc else ''
    return f'<div class="ph"><div>{c}<span class="k">{fr}</span><h1>{zh}</h1>{d}</div><div class="r">{right}</div></div>'


def tabs(items, on=0):
    return '<div class="tabs">' + ''.join(f'<a class="{"on" if i == on else ""}">{t}</a>' for i, t in enumerate(items)) + '</div>'


def fpage(title, body, mod='', style=''):
    return f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=1440">
<title>{title}</title><link rel="stylesheet" href="final.css"><style>{style}</style></head>
<body class="{mod}">{WOB}
{body}
</body></html>'''
