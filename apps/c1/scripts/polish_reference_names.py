"""Keep proper names in French without promoting ordinary capitalized words to names."""
import json,re
from pathlib import Path
from bank_assets import load_bank
ROOT=Path(__file__).resolve().parents[1];p=ROOT/'public/content.json';b=load_bank(ROOT/'public');lex=b['lexicon']
known=set('France Chine Paris Lyon Marseille Bordeaux Toulouse Lille Nantes Rennes Europe États-Unis Royaume-Uni Canada Québec Japon Allemagne Espagne Italie Afrique Inde Australie Brésil Belgique Suisse Russie Facebook YouTube Twitter Internet Google Tesla Nutella Science Nature Libération'.split())
known.update(['La Réunion','Le Monde','Le Figaro','Le Parisien','Le Point','La Croix','Sciences et Avenir','Quand les profs aiment les élèves','Ma mémoire et les autres','Les Cadres sociaux de la mémoire','Le jour où mon robot m’aimera','Le Triomphe d’une utopie','Manuel de l’anti-tourisme','Splendeurs et misères du travail','La Révolte des premiers de la classe','Nouvelles de nulle part','Un texte un jour'])
common={'Animaux':'动物','Villes':'城市','Réseaux':'网络','Médecins':'医生','Études':'研究','Minutes':'分钟','Tablettes':'平板电脑','Utilise':'使用','Bonjour':'你好','Recherche':'研究','Difficile':'困难','École':'学校','Télétravail':'远程办公','Smartphone':'智能手机','Conseil':'建议','Commission':'委员会','Tourisme':'旅游','Science':'科学','Robotique':'机器人技术','Progrès':'进步','Numérique':'数字技术','Orthographe':'拼写','Avenir':'未来','Quotidien':'日常','Cerveau':'大脑','Éducation':'教育','Enfant':'孩子','Demain':'未来','Professionnel':'职业','Travail':'工作','Publicité':'广告','Cohérence':'连贯性','Source':'来源','Grand':'大型','Univers':'世界'}
pairs=[];bad={}
for fr,zh in lex['namePairs']:
 roots=[fr.lower()]+lex.get('formLemmas',{}).get(fr.lower(),[]);pos={x['pos']for root in roots for x in lex['entries'].get(root,{}).get('senses',[])}
 ordinary=len(fr.split())==1 and pos and 'name'not in pos and pos-{'unknown','abbrev'} and fr not in known and not fr.isupper()
 if ordinary:
  meaning=common.get(fr)or next((lex['entries'][root].get('zh','').split('；')[0]for root in roots if root in lex['entries']),zh)
  if meaning and re.search('[\u4e00-\u9fff]',meaning)and len(meaning)<35:bad[fr]=meaning
 else:pairs.append([fr,zh])
for fr,zh in common.items():
 if fr not in known:bad[fr]=zh
lex['namePairs']=pairs
pair_sort=sorted(pairs,key=lambda p:len(p[1]),reverse=True)
def polish(fr,zh):
 for word,meaning in sorted(bad.items(),key=lambda v:len(v[0]),reverse=True):zh=re.sub(r'(?<![A-Za-zÀ-ÿ])'+re.escape(word)+r'(?![A-Za-zÀ-ÿ])',lambda _:meaning,zh)
 for name,variant in pair_sort:
  if variant in zh and re.search(r'(?<!\w)'+re.escape(name)+r'(?!\w)',fr):zh=zh.replace(variant,name)
 return zh
for e in b['exercises']:
 e['titleZh']=polish(e['title'],e['titleZh'])
 for v in e['paragraphs']+e.get('tasks',[]):v['zh']=polish(v['fr'],v.get('zh',''))
 for q in e['questions']:
  q['zh']=polish(q['prompt'],q.get('zh',''))
  for o in q.get('options',[]):o['zh']=polish(o['text'],o.get('zh',''))
  a=q.get('answer',{})
  if a.get('reference'):a['reference']=polish(q['prompt']+' '+a['reference'],a['reference'])
# Explicitly protect recurring place/media names; only where original text contains them.
for fr,zh in [('France','法国'),('Chine','中国'),('Paris','巴黎'),('Le Monde','世界报'),('Le Figaro','费加罗报'),('Facebook','脸书')]:
 for e in b['exercises']:
  for v in e['paragraphs']+e.get('tasks',[]):
   if re.search(r'(?<!\w)'+re.escape(fr)+r'(?!\w)',v['fr']):v['zh']=v['zh'].replace(zh,fr)
p.write_text(json.dumps(b,ensure_ascii=False,separators=(',',':')))
(ROOT/'data/study/name-pairs.json').write_text(json.dumps(pairs,ensure_ascii=False,indent=2))
print('Protected name variants',len(pairs),'ordinary word repairs',len(bad))
