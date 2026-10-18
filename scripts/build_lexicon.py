"""Build local French→Chinese lookup and 900-word corpus-based books.
CFDICT source is CC BY-SA 3.0; attribution is retained in public/dictionary/NOTICE.txt.
Working inputs are explicit, local files; no runtime translation service is used.
"""
import subprocess,sys,os,json,re,collections,unicodedata
from pathlib import Path
sys.path.insert(0,'/workspace/work/python-refinements')
import simplemma
from wordfreq import zipf_frequency
ROOT=Path(__file__).resolve().parents[1]
def key(s):return unicodedata.normalize('NFC',s).lower().replace('’',"'").replace('‘',"'").strip()
source=Path(os.environ.get('CFDICT_SOURCE','/workspace/work/cfdict/cfdict-fr-main/cfdict.u8'))
raw=collections.defaultdict(list)
for line in source.read_text().splitlines():
 m=re.match(r'\S+ (\S+) \[[^]]*\] /(.*)/$',line)
 if not m:continue
 zh,frs=m.groups()
 for fr in frs.split('/'):
  fr=key(re.sub(r'\([^)]*\)','',fr))
  if not re.fullmatch(r'[a-zà-öø-ÿœæ][a-zà-öø-ÿœæ’\' -]{2,60}',fr):continue
  if zh not in raw[fr]:raw[fr].append(zh)
entries={fr:{'zh':'；'.join(sorted(zhs,key=lambda z:(zipf_frequency(z,'zh'),-len(z)),reverse=True)[:7])} for fr,zhs in raw.items()}
manual=json.loads(subprocess.check_output(['node','--input-type=module','-e',"import {CORE_WORDS,WRITING_WORDS,SPEAKING_WORDS,parseWords} from './src/word-seeds.js';console.log(JSON.stringify([...parseWords(CORE_WORDS),...parseWords(WRITING_WORDS),...parseWords(SPEAKING_WORDS)]));"],cwd=ROOT))
for w in manual:entries[key(w['fr'])]={'zh':w['zh'],'curated':True}
entries['fabricant']={'zh':'制造商；生产厂家；制造者','curated':True,'collocations':[{'fr':'un fabricant de voitures','zh':'一家汽车制造商'},{'fr':'un fabricant de meubles','zh':'一家家具制造商'},{'fr':'un fabricant de jouets','zh':'一家玩具制造商'},{'fr':'un fabricant local','zh':'一家本地制造商'}]}
manual_collocations=json.loads((ROOT/'data/collocations.json').read_text()) if (ROOT/'data/collocations.json').exists() else {}
for fr,collocations in manual_collocations.items():
 if fr in entries:entries[fr]['collocations']=collocations
stop=set('être avoir faire dire aller tout tous toute toutes quel quelle quels quelles ainsi autre autres avant avec après alors aussi assez chez comme comment contre dans depuis dessous dessus deux dont donc encore entre faut fois ici jusqu jamais leur leurs lui même mêmes mais moins mon non notre nous nos parce par pas peut plus pour pourquoi quand que quelque quelques qui quoi sans ses son sont sous sur tant tel telle tels telles très trop une vers vos vous votre cela celle celles celui ceux ces cet cette chacun chaque rien soit selon seulement aucun aucune pendant parfois parce où aux des les mes tes et ou est on ne ni si ce ça car de du au la le en un il ils elle elles es ai as a y se sa ta ma te tu me'.split())
bank=json.loads((ROOT/'public/content.json').read_text());aliases={};occ=collections.defaultdict(collections.Counter);forms=collections.defaultdict(set);bookcounts=collections.defaultdict(collections.Counter)
lemma_cache={}
for e in bank['exercises']:
 texts=[e['title'],*[p['fr']for p in e['paragraphs']],*[q['prompt']+' '+' '.join(o['text']for o in q.get('options',[]))for q in e['questions']],*[t['fr']for t in e.get('tasks',[])if t.get('fr')]]
 for text in texts:
  for form in re.findall(r'[A-Za-zÀ-ÖØ-öø-ÿœŒ]+(?:[-’\'][A-Za-zÀ-ÖØ-öø-ÿœŒ]+)*',text):
   form=key(form);word=re.sub(r"^(?:l|d|s|n|qu|c|j|m|t)'",'',form)
   if len(word)<3 or word in stop:continue
   if word not in lemma_cache:lemma_cache[word]=key(simplemma.lemmatize(word,lang='fr'))
   lemma=lemma_cache[word]
   if lemma not in entries:lemma=word
   if lemma not in entries or lemma in stop:continue
   aliases[form]=lemma;aliases[word]=lemma;forms[lemma].add(form);occ[lemma][e['id']]+=1;bookcounts['listening' if e['category'] in ['long','short'] else e['category']][lemma]+=1
for lemma,counts in occ.items():entries[lemma]['forms']=sorted(forms[lemma]);entries[lemma]['sources']=list(counts)
base=json.loads(subprocess.check_output(['node','--input-type=module','-e',"import fs from 'fs';import {makeBooks}from './src/vocabulary.js';console.log(JSON.stringify(makeBooks(JSON.parse(fs.readFileSync('public/content.json')).exercises,{annotations:{}})));"],cwd=ROOT));books={}
for category in ['listening','reading','writing','speaking']:
 chosen=[]
 for w in base[category]:
  fr=key(w['fr']);entries.setdefault(fr,{'zh':w['zh'],'curated':True})
  if fr not in chosen:chosen.append(fr)
 if category=='listening' and 'fabricant' not in chosen:chosen.insert(0,'fabricant')
 ranked=sorted(bookcounts[category],key=lambda w:(bookcounts[category][w],min(5.4,zipf_frequency(w,'fr'))),reverse=True)
 for w in ranked:
  if len(chosen)>=900:break
  if w not in chosen and zipf_frequency(w,'fr')>=2.3 and not any(x in w for x in ['http','www']):chosen.append(w)
 assert len(chosen)==900,(category,len(chosen))
 books[category]=chosen
phrases=[{'fr':fr,'zh':e['zh']}for fr,e in entries.items()if ' 'in fr and 2<=len(fr.split())<=5 and len(fr)<=45]
bank['lexicon']={'entries':entries,'aliases':aliases,'phrases':phrases,'books':books,'source':'CFDICT / 本站整理','license':'CC BY-SA 3.0'}
(ROOT/'public/content.json').write_text(json.dumps(bank,ensure_ascii=False,separators=(',',':')))
report={'entries':len(entries),'formAliases':len(aliases),'phrases':len(phrases),'books':{k:len(v)for k,v in books.items()},'fabricants':aliases.get('fabricants'),'method':'One lemma per book entry; corpus occurrence matching plus retained useful writing/speaking expressions.'}
(ROOT/'data/lexicon-audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(report)
