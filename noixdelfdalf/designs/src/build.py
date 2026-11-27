"""Write every mockup page to designs/html/. Usage: python3 build.py"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import home, learn, read, bank, tutor, homes, bento_fr, poster, f_learn, f_read, f_bank, f_tutor
out = pathlib.Path(__file__).parent.parent / 'html'
for mod in (home, learn, read, bank, tutor, homes, bento_fr, poster, f_learn, f_read, f_bank, f_tutor):
    for name, html in mod.PAGES.items():
        (out / f'{name}.html').write_text(html, encoding='utf-8')
        print('wrote', name)
