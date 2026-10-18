"""Merge reviewed idioms, word families and sentence references into the browser lexicon."""
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];DATA=ROOT/'data/dictionary'
source=DATA/'translated.json'
if not source.exists():source=DATA/'base.json'
bank=json.loads(source.read_text());key=lambda s:re.sub(r'\s+',' ',s.replace('’',"'").replace('ʼ',"'")).strip().lower()
native=json.loads((DATA/'base.json').read_text())
for word,entries in native['entries'].items():
 if entries:
  pos={e['pos'] for e in entries}
  bank['entries'][word]=entries+[e for e in bank['entries'].get(word,[]) if e['source']=='wiktionary-en-mt' and e['pos'] not in pos]
reviewed_phrases=[];replaced_phrases=set()
for line in (DATA/'phrases.tsv').read_text().splitlines():
 if not line or line.startswith('#'):continue
 word,pos,meaning=line.split('|');word=key(word)
 if ' ' in word and word not in replaced_phrases:bank['entries'][word]=[];replaced_phrases.add(word)
 entries=bank['entries'].setdefault(word,[])
 if ' ' in word:reviewed_phrases.append(word)
 same=next((e for e in entries if e['pos']==pos),None)
 if same:same['senses']=[meaning]+[t for t in same['senses'] if t!=meaning]
 else:entries.insert(0,{'pos':pos,'senses':[meaning],'source':'reviewed'})
# Add regular derivations only when the target is an attested dictionary entry
# with the expected POS. Irregular families are explicitly reviewed below.
for word,entries in bank['entries'].items():
 pos={e['pos'] for e in entries};candidates=[]
 if 'n' in pos:
  if word.endswith('ation'):candidates.append((word[:-5]+'er','v'))
  if word.endswith('ement'):candidates.append((word[:-5]+'er','v'))
  if word.endswith('ivité'):candidates.append((word[:-5]+'if','adj'))
  if word.endswith('bilité'):candidates.append((word[:-6]+'ble','adj'))
 if 'adj' in pos and word.endswith('able'):candidates.append((word[:-4]+'er','v'))
 if 'adv' in pos and word.endswith('ment'):candidates.append((word[:-4],'adj'))
 for other,target_pos in candidates:
  if len(other)>4 and any(e['pos']==target_pos for e in bank['entries'].get(other,[])):
   for a,b in [(word,other),(other,word)]:
    related=bank['related'].setdefault(a,[])
    if b not in related:related.append(b)
for line in (DATA/'families.tsv').read_text().splitlines():
 if not line or line.startswith('#'):continue
 family=line.split('|')
 for word in family:bank['related'][word]=list(dict.fromkeys([w for w in family if w!=word]+bank['related'].get(word,[])))[:12]
for phrase in bank['entries']:
 if not 2<=len(phrase.split())<=7:continue
 for word in re.findall(r'[a-zà-ÿœ]+',phrase):
  for lemma in [word]+bank['forms'].get(word,[])[:2]:
   if not any(e['pos'] in ['n','v','adj'] for e in bank['entries'].get(lemma,[])):continue
   coll=bank['collocations'].setdefault(lemma,[])
   if phrase not in coll and len(coll)<8:coll.append(phrase)
reviewed_collocations={}
for phrase in reviewed_phrases:
 for word in re.findall(r'[a-zà-ÿœ]+',phrase):
  for lemma in [word]+bank['forms'].get(word,[])[:2]:
   if any(e['pos'] in ['n','v','adj'] for e in bank['entries'].get(lemma,[])):reviewed_collocations.setdefault(lemma,[]).append(phrase)
reviewed_collocations.update({'de':['avoir besoin de','en raison de','à cause de'], 'à':['faire face à','avoir accès à','parvenir à'], 'en':['prendre en compte','mettre en place','en raison de'], 'pour':['pour autant','pour peu que','pour autant que'], 'que':['bien que','alors que','tandis que'], 'si':['même si','si bien que']})
for word,phrases in reviewed_collocations.items():bank['collocations'][word]=list(dict.fromkeys(phrases+bank['collocations'].get(word,[])))[:8]
variants=json.loads((ROOT/'data/name-glossary.json').read_text())
pairs=[]
for line in (ROOT/'data/name-variants.tsv').read_text().splitlines():
 if line and not line.startswith('#'):
  name,*forms=line.split('|');pairs.extend((name,form) for form in forms)
for name,form in variants.items():
 if form not in ['世界','自然','现在','工作','科学','文化','人类','今天','先生','女士','故事','儿童'] and len(form)>1:pairs.append((name,form))
pairs.extend((a,b) for a,b in {'France':'法国','Chine':'中国','Paris':'巴黎','Europe':'欧洲','Facebook':'脸书','YouTube':'优兔','Twitter':'推特'}.items())
patterns=[(a,a.casefold(),re.compile(r'(?<!\w)'+re.escape(a)+r'(?!\w)',re.I),b) for a,b in sorted(set(pairs),key=lambda x:len(x[1]),reverse=True)]
bank['names']=sorted(set(pairs),key=lambda x:len(x[1]),reverse=True)
bank['attribution']={'author':'Wiktionary contributors / Kaikki / Wiktionary-to-Yomitan contributors','urls':['https://zh.wiktionary.org/','https://en.wiktionary.org/','https://kaikki.org/','https://github.com/yomidevs/wiktionary-to-yomitan'],'changes':'提取纯文本；简繁转换；合并词性；建立词形与派生关系；补充原文搭配、人工短语及本地机器译文。','licenseText':(DATA/'CC-BY-SA-4.0.txt').read_text()}
translations={}
for text,translated in bank['translations'].items():
 folded=text.casefold()
 for name,fold,pattern,variant in patterns:
  if fold in folded and pattern.search(text):translated=translated.replace(variant,name)
 translations[key(text)]=translated
 translations[key(text).strip(' .!?…»”"«“')]=translated
bank['translations']=translations
for line in (DATA/'sentences-reviewed.tsv').read_text().splitlines():
 if line and not line.startswith('#'):
  fr,zh=line.split('|',1);bank['translations'][key(fr).strip(' .!?…»”"«“')]=zh
bank['entries']={w:es for w,es in bank['entries'].items() if es}
for word,entries in bank['entries'].items():
 canonical=next((s.split('：',1)[1] for e in entries if e['pos']=='name' for s in e['senses'] if s.startswith('专有名称，保留原文：')),word)
 for entry in entries:
  if entry['pos']=='unknown':
   raw=' '.join(entry['senses'])
   for label,pos in [('专有名词','name'),('形容词','adj'),('副词','adv'),('动词','v'),('名词','n'),('介词','prep'),('连词','conj'),('代词','pron')]:
    if label in raw:entry['pos']=pos;break
  entry['senses']=[re.sub(r'^\s*(?:通常\s*)?#+\s*','',re.sub(r'={2,}[^=]*={2,}','',s)).strip() for s in entry['senses']]
  if entry['pos']=='name':entry['senses']=['专有名称，保留原文：'+canonical]
 merged={}
 for entry in entries:
  if entry['pos'] not in merged:merged[entry['pos']]={**entry,'senses':[]}
  merged[entry['pos']]['senses']=list(dict.fromkeys(merged[entry['pos']]['senses']+entry['senses']))
 bank['entries'][word]=list(merged.values())
(ROOT/'public/lexicon.json').write_text(json.dumps(bank,ensure_ascii=False,separators=(',',':')))
print('Lexicon:',len(bank['entries']),'headwords;',len(bank['forms']),'inflected spellings;',len(bank['translations']),'sentence keys; source:',source.name)
