"""Merge attributed Wiktionary POS and inflections into the existing journal bank.
Set WIKTIONARY_INDEX to the normalized export; raw downloads stay outside source.
"""
import json,re,os
from pathlib import Path
from bank_assets import load_bank
ROOT=Path(__file__).resolve().parents[1]
b=load_bank(ROOT/'public');lex=b['lexicon']
x=json.loads(Path(os.environ.get('WIKTIONARY_INDEX','/workspace/work/reference-drafts/lexicon.json')).read_text())
for word,senses in x['entries'].items():
 e=lex['entries'].setdefault(word,{'zh':'','forms':[],'sources':[]})
 known=[s for s in senses if s['pos']!='unknown'];senses=known or senses
 e['senses']=[{'pos':s['pos'],'zh':'；'.join(s['senses']).replace('▁','').strip()}for s in senses if s.get('senses')]
 if not e.get('zh') and e['senses']:e['zh']='；'.join(s['zh']for s in e['senses'])
 if x['related'].get(word):e['related']=x['related'][word]
 coll=[{'fr':v,'zh':lex['entries'].get(v,{}).get('zh')or '；'.join(ss for s in x['entries'].get(v,[])for ss in s['senses'])}for v in x['collocations'].get(word,[])]
 if coll:e['collocations']=list({v['fr']:v for v in e.get('collocations',[])+coll}.values())[:8]
lex['formLemmas']={k:[v for v in vs if v in lex['entries']]for k,vs in x['forms'].items()if any(v in lex['entries']for v in vs)}
# Keep only clean corpus references; never treat a paragraph as a selected-sentence translation.
lex['translations']={k:v.replace('▁','')for k,v in x['translations'].items()if '�'not in v and '⁇'not in v and len(v)>1}
lex['namePairs']=[[a,z]for a,z in x['names']if 1<len(z)<45 and len(a)<80 and not re.search(r'(.)\1{4}',a+z)]
lex['attribution']=x['attribution']
(ROOT/'public/content.json').write_text(json.dumps(b,ensure_ascii=False,separators=(',',':')))
print('Dictionary entries',len(lex['entries']),'inflected forms',len(lex['formLemmas']))
