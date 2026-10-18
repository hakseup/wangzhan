"""Translate complete sentences without numeric placeholders, restore proper names by glossary.
Name translations are scoped to their original paragraph to avoid global substitutions.
"""
import json,re,hashlib,sqlite3,html,time
from pathlib import Path
import ctranslate2,sentencepiece as spm
ROOT=Path(__file__).resolve().parents[1];MODELS=ROOT.parent/'tooling/models'
key=lambda s:hashlib.sha256(s.encode()).hexdigest()
frsp=spm.SentencePieceProcessor(model_file=str(MODELS/'fr_en/sentencepiece.model'))
zhsp=spm.SentencePieceProcessor(model_file=str(MODELS/'translate-en_zh-1_9/sentencepiece.model'))
fr=ctranslate2.Translator(str(MODELS/'fr_en/model'),compute_type='int8',intra_threads=4)
zh=ctranslate2.Translator(str(MODELS/'translate-en_zh-1_9/model'),compute_type='int8',intra_threads=4)
db=sqlite3.connect(ROOT/'data/revised-translations-v3.sqlite');db.execute('CREATE TABLE IF NOT EXISTS translations(hash TEXT PRIMARY KEY,fr TEXT,zh TEXT)')
bank=json.loads((ROOT/'public/content.json').read_text());texts=[]
for e in bank['exercises']:
 texts.extend(p['fr'] for p in e['paragraphs']);texts.extend(q['prompt'] for q in e['questions']);texts.extend(o['text'] for q in e['questions'] for o in q.get('options',[]))
texts=list(dict.fromkeys(texts))
manual=json.loads((ROOT/'data/translation-edits.json').read_text())
for e in bank['exercises']:
 edits=manual.get(e['id'],{})
 for i,t in enumerate(edits.get('paragraphs',[])):
  s=e['paragraphs'][i]['fr'];db.execute('insert or replace into translations values (?,?,?)',(key(s),s,t))
 for i,t in enumerate(edits.get('questions',[])):
  s=e['questions'][i]['prompt'];db.execute('insert or replace into translations values (?,?,?)',(key(s),s,t))
db.commit()
# Full titles that are not consistently recognized by the statistical NER model.
books=['Quand les profs aiment les élèves','Ma mémoire et les autres','Les Cadres sociaux de la mémoire','Le jour où mon robot m’aimera','Le Triomphe d’une utopie','Le Triomphe d\'une utopie','Manuel de l’anti-tourisme','Manuel de l\'anti-tourisme','Splendeurs et misères du travail','La Révolte des premiers de la classe','Nouvelles de nulle part','Un texte un jour','Nous ne prendrons plus l’avion','Nous ne prendrons plus l\'avion']
names=json.loads((ROOT/'data/protected-names.json').read_text())+books
# Drop accidental fragments and ordinary vocabulary from NER.
names=sorted({n for n in names if (sum(w[0].isupper() for w in n.split() if w)>1 or n[0].isupper() and ' ' not in n or n in books) and len(n)<80 and not re.search(r'[^\wÀ-ÿ\s’\-\'.:/]',n)},key=len,reverse=True)
namecache=ROOT/'data/name-glossary.json'
def run(items):
 english=fr.translate_batch([frsp.encode(s,out_type=str) for s in items],beam_size=3,max_batch_size=32,max_decoding_length=400)
 en=[frsp.decode(r.hypotheses[0]) for r in english]
 chinese=zh.translate_batch([zhsp.encode(s,out_type=str) for s in en],beam_size=3,max_batch_size=32,max_decoding_length=450)
 return [zhsp.decode(r.hypotheses[0]).replace('▁','').strip() for r in chinese]
if namecache.exists():glossary=json.loads(namecache.read_text())
else:
 glossary={}
 for i in range(0,len(names),32):
  for n,t in zip(names[i:i+32],run(names[i:i+32])):
   t=t.strip(' 。.,:：;；“”"')
   if re.search(r'[\u4e00-\u9fff]',t) and len(t)>1 and t not in ['先生','女士','父亲','母亲','今天','互联网','因特网','儿童','青年','语言','年轻人','结论','法国人','中国人','英国人','美国人']:glossary[n]=t
 namecache.write_text(json.dumps(glossary,ensure_ascii=False,indent=2))
# Actual places and website names receive their original spelling.
glossary.update({'France':'法国','Chine':'中国','Paris':'巴黎','Lyon':'里昂','Marseille':'马赛','Bordeaux':'波尔多','Toulouse':'图卢兹','Lille':'里尔','Nantes':'南特','Rennes':'雷恩','Europe':'欧洲','États-Unis':'美国','Royaume-Uni':'英国','Canada':'加拿大','Québec':'魁北克','Japon':'日本','Allemagne':'德国','Espagne':'西班牙','Italie':'意大利','Afrique':'非洲','Inde':'印度','Australie':'澳大利亚','Brésil':'巴西','Belgique':'比利时','Suisse':'瑞士','Russie':'俄罗斯','La Réunion':'留尼汪','Facebook':'脸书','Internet':'因特网','Petit Palais':'小皇宫','YouTube':'优兔','Twitter':'推特'})
pattern=re.compile(r'(?<!\w)('+'|'.join(re.escape(n) for n in names)+r')(?!\w)')
from functools import lru_cache
try:
 from symspellpy import SymSpell,Verbosity
 from wordfreq import zipf_frequency
 spelling=SymSpell(max_dictionary_edit_distance=2,prefix_length=7)
 spelling.load_pickle(str(ROOT.parent/'tooling/french-spelling.pickle'))
except (ImportError,FileNotFoundError):spelling=None
@lru_cache(maxsize=50000)
def repair_word(w):
 if not spelling or not w.islower() or len(w)<5 or zipf_frequency(w,'fr')>=2.5:return w
 results=spelling.lookup(w,Verbosity.TOP,max_edit_distance=1 if len(w)<7 else 2)
 if results and results[0].distance>0 and zipf_frequency(results[0].term,'fr')>=3.2:return results[0].term
 return w

def prepare(s):
 s=html.unescape(s).replace('\u00a0',' ')
 for a,b in {'connavt':'connaît','jusqu’j':'jusqu’à','$lors':'Alors','%ien s':'Bien s',',l ':'Il ','h\\pothèse':'hypothèse','c{té':'côté','Bonjour':'Hello','Présentateur':'Presenter','mêrne':'même','sdentifiques':'scientifiques','écentfique':'scientifique','fesponsable':'responsable','camière':'carrière','plutdt':'plutôt','connavt':'connaît','fai c’est':'fait c’est','de plus en de prothèses':'de plus en plus de prothèses'}.items():s=s.replace(a,b)
 # Recognizable, systematic font substitution affects some entire scanned paragraphs.
 if s.count('ë')>=5 and any(w in s for w in ['éouê','éê','cêance','ëommeë']):
  s=s.translate(str.maketrans({'ë':'s','ê':'r','î':'v','é':'p','è':'q','I':',','K':'.'}))
 s=re.sub(r"[A-Za-zÀ-ÖØ-öø-ÿ]+",lambda m:repair_word(m.group()),s)
 return s

def polish(t,source):
 t=html.unescape(t).replace('▁','').replace(' ⁇ ','').replace('⁇','')
 for name in sorted(glossary,key=lambda n:len(glossary[n]),reverse=True):
  if name in source:t=t.replace(glossary[name],name)
 for a,b in {'介绍者':'主持人','计算机档案':'计算机文件','计算档案':'计算机文件','民主化':'普及','数字化时代':'数字时代'}.items():t=t.replace(a,b)
 if 'marche' in source.lower() and not 'marché' in source.lower():
  for a,b in {'游行':'步行','市场':'步行','行军':'步行','步进':'步行','走私':'步行'}.items():t=t.replace(a,b)
 t=t.replace(',', '，').replace(';','；').replace('?', '？').replace('!', '！')
 t=re.sub(r'(?<=[\u4e00-\u9fff])\s+(?=[\u4e00-\u9fff])','',t)
 t=re.sub(r'(?<=[\u4e00-\u9fff])\.(?!\d)','。',t)
 return t.strip()
pending=[s for s in texts if not db.execute('select 1 from translations where hash=?',(key(s),)).fetchone()];start=time.time();print('Pending',len(pending),flush=True)
for i in range(0,len(pending),12):
 batch=pending[i:i+12];segments=[];owners=[]
 for owner,s in enumerate(batch):
  for sentence in re.split(r'(?<=[.!?…])\s+',prepare(s)):
   # Shorter complete clauses avoid arbitrary subword cuts in long spoken sentences.
   if len(frsp.encode(sentence))>220:
    clauses=re.split(r'(?<=[;:])\s+|(?<=,)\s+(?=(?:mais|parce que|alors|et puis|donc)\b)',sentence)
   else:clauses=[sentence]
   for clause in clauses:
    tok=frsp.encode(clause,out_type=str)
    for j in range(0,len(tok),250):segments.append(frsp.decode(tok[j:j+250]));owners.append(owner)
 translated=['']*len(batch)
 for owner,t in zip(owners,run(segments)):translated[owner]+=polish(t,batch[owner])
 for s,t in zip(batch,translated):db.execute('insert or replace into translations values (?,?,?)',(key(s),s,t))
 db.commit()
 if i%120==0:print(min(i+12,len(pending)),'/',len(pending),round(time.time()-start),'sec',flush=True)
(ROOT/'data/revised-translations.json').write_text(json.dumps({r[0]:r[1] for r in db.execute('select hash,zh from translations')},ensure_ascii=False,separators=(',',':')))
print('Complete',flush=True)
