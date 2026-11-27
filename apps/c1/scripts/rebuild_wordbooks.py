"""Select four independent, source-traceable books; no target size or shared padding.
Uses only the local question bank, local dictionary and public wordfreq frequencies.
Run with simplemma and wordfreq installed. Only content.json book metadata changes.
"""
import json,re,sys,os,math,collections,unicodedata
from pathlib import Path
if os.environ.get('NOIX_LEXICON_PYTHON'):sys.path.insert(0,os.environ['NOIX_LEXICON_PYTHON'])
import simplemma
from wordfreq import zipf_frequency
from bank_assets import load_bank
ROOT=Path(__file__).resolve().parents[1]
manifest=json.loads((ROOT/'public/content.json').read_text());bank=load_bank(ROOT/'public');lex=bank['lexicon'];entries=lex['entries']
key=lambda s:unicodedata.normalize('NFC',s).lower().replace('’',"'").replace('‘',"'").strip()
token=re.compile(r'[A-Za-zÀ-ÖØ-öø-ÿœŒ]+(?:[-’\'][A-Za-zÀ-ÖØ-öø-ÿœŒ]+)*')
stop=set("pers perce software stanford bon mauvais vrai faux puis petit grand année jour temps personne gens lieu part côté appel mois janvier février mars avril mai juin juillet août septembre octobre novembre décembre ".split())|set("être avoir faire dire aller venir pouvoir vouloir devoir falloir savoir prendre mettre voir donner trouver passer rester rendre porter tenir sembler utiliser permettre proposer présenter montrer expliquer penser parler considérer demander répondre choisir écrire lire écouter comprendre bonjour merci monsieur madame oui non aujourd'hui demain hier maintenant ici là alors ainsi aussi assez après avant avec chez comme comment contre dans depuis dessous dessus deux dont donc encore entre faut fois jusqu jamais leur leurs lui même mêmes mais moins mon notre nous nos parce par pas plus pour pourquoi quand que quelque quelques qui quoi sans ses son sont sous sur tant tel telle tels telles très trop une vers vos vous votre cela celle celles celui ceux ces cet cette chacun chaque rien soit selon seulement aucun aucune pendant parfois où aux des les mes tes et ou est on ne ni si ce ça car de du au la le en un il ils elle elles es ai as a y se sa ta ma te tu me tous tout toute toutes quel quelle quels quelles autre autres peut exemple document texte article auteur question réponse première deuxième troisième premier dernier partie idée introduction conclusion problématique plan mots mot numéro sujet thème dit bien peu beaucoup plusieurs certain certaine certains certaines déjà toujours souvent notamment cependant néanmoins pourtant vraiment quelquefois plupart mieux manière chose point afin grâce fin début suite nom prénom français française france paris anglais english www http pdf c'est c'était qu'il qu'elle d'abord c1 dalf delphine".split())
# Task-specific complements: learning units, not an assertion of official exam frequency.
SUPPLEMENTS={
'listening':{
'prendre des notes':'记笔记','repérer les mots-clés':'捕捉关键词','reformuler une idée':'换一种方式表述观点','un témoignage':'一段亲历者的陈述','un reportage':'一则现场报道','une enquête de terrain':'一项实地调查','un enjeu de société':'一个社会议题','un point de vue nuancé':'一个有分寸的观点','la prise de parole':'发言','un entretien radiophonique':'一次广播访谈','un constat partagé':'一种共同的判断','remettre en question':'提出质疑','mettre en œuvre':'付诸实施','faire le point sur':'梳理……的现状','aller à l’encontre de':'违背；与……相反','un biais de perception':'感知偏差','la sensibilisation du public':'提升公众意识','le bouche-à-oreille':'口口相传','la reconversion professionnelle':'职业转型','un savoir-faire artisanal':'一门手工技艺','une initiative citoyenne':'一项公民倡议','la fracture numérique':'数字鸿沟','la consommation responsable':'负责任的消费','le lien social':'社会联系','les pouvoirs publics':'公共管理部门','les conditions de travail':'工作条件','le pouvoir d’achat':'购买力','la mise en commun':'共同使用；汇集共享','un retour d’expérience':'经验反馈','la fiabilité des sources':'信息来源的可靠性'},
'reading':{
'la thèse défendue':'作者所持的核心主张','un argument implicite':'一个隐含论据','un raisonnement déductif':'一种演绎推理','une relation de cause à effet':'因果关系','une concession argumentative':'论证中的让步','une prise de position':'表明立场','une donnée chiffrée':'一项统计数据','une corrélation':'一种相关关系','une idée reçue':'一种成见','un parti pris':'一种预设立场；偏见','une portée limitée':'有限的适用范围','mettre en perspective':'结合背景加以分析','étayer une affirmation':'为论断提供依据','nuancer un propos':'为说法作出限定','relativiser un constat':'结合条件审视某种判断','tirer une conclusion':'得出结论','dégager les enjeux':'提炼问题的关键','à l’instar de':'如同；与……一样','en dépit de':'尽管','dans la mesure où':'鉴于；在……范围内','à cet égard':'在这一点上','au détriment de':'以损害……为代价','la cohésion sociale':'社会凝聚力','la transition écologique':'生态转型','le développement durable':'可持续发展','la liberté d’expression':'言论自由','les inégalités sociales':'社会不平等','le patrimoine culturel':'文化遗产','la recherche scientifique':'科学研究','la transmission des savoirs':'知识传承'},
'writing':{
'une synthèse objective':'客观的综合概述','croiser les informations':'对照、整合信息','hiérarchiser les idées':'按重要程度组织观点','structurer un raisonnement':'有条理地组织论证','formuler une proposition':'提出建议','une mesure concrète':'一项具体措施','une mise en balance':'对利弊的权衡','une solution viable':'一种切实可行的解决方案','un compromis acceptable':'一种可接受的折中方案','à première vue':'乍看之下','force est de constater que':'必须承认……','il convient de souligner que':'应当指出……','il n’en demeure pas moins que':'尽管如此，仍须承认……','encore faut-il que':'但前提还在于……','cela ne saurait suffire':'仅此尚不足够','loin de se limiter à':'远不止于……','à condition de':'以……为条件','sous réserve de':'在……的前提下','en tenant compte de':'在考虑……的情况下','en ce qui concerne':'关于；就……而言','d’une part':'一方面','d’autre part':'另一方面','en revanche':'相反；另一方面','par conséquent':'因此','en définitive':'归根结底','la mise en place':'建立；推行','la faisabilité':'可行性','le financement public':'公共资金支持','l’égalité des chances':'机会平等','la responsabilité collective':'集体责任'},
'speaking':{
'prendre position sur':'就……表明立场','défendre son point de vue':'为自己的观点辩护','rebondir sur une remarque':'承接对方的话进一步展开','répondre à une objection':'回应异议','reconnaître une limite':'承认局限','apporter une précision':'补充说明','revenir sur un point':'回到某一点再加以说明','illustrer un argument':'举例说明论据','ouvrir le débat':'引出进一步讨论','si je vous comprends bien':'如果我理解得没错','vous soulevez un point important':'您提出了一个重要的问题','je partage votre préoccupation':'我理解并认同您的担忧','je nuancerais cette affirmation':'我想对这一说法作些限定','tout dépend du contexte':'这完全取决于具体背景','prenons un exemple concret':'我们来看一个具体例子','cela mérite réflexion':'这一点值得思考','pour revenir à votre question':'回到您的问题','je tiens à préciser que':'我想特别说明……','dans une certaine mesure':'在一定程度上','sur le terrain':'在实际工作中；在一线','à court terme':'短期而言','à long terme':'长期而言','les parties prenantes':'利益相关方','la concertation':'协商','la participation citoyenne':'公民参与','la confiance mutuelle':'相互信任','un désaccord constructif':'一种有建设性的分歧','une décision éclairée':'基于充分信息的决定','un intérêt commun':'共同利益','la prévention des risques':'风险预防'}
}
cache={}
def lemma_of(form):
 form=key(form);word=re.sub(r"^(?:l|d|s|n|qu|c|j|m|t)'",'',form)
 if word in cache:return cache[word]
 lemma=key(simplemma.lemmatize(word,lang='fr'))
 # Corpus aliases were verified when building the dictionary, but never cross categories here.
 candidates=[lemma,lex.get('aliases',{}).get(word),word,*lex.get('formLemmas',{}).get(word,[])]
 result=next((w for w in candidates if w in entries and ' 'not in w and re.search('[\u4e00-\u9fff]',entries[w].get('zh',''))),None)
 cache[word]=result;return result
books={};sources={};forms={};audit={}
for book in ['listening','reading','writing','speaking']:
 freq=collections.Counter();docs=collections.defaultdict(set);locations=collections.defaultdict(set);wordforms=collections.defaultdict(set);title_words=set();lowercase=collections.Counter()
 exercises=[e for e in bank['exercises']if ('listening'if e['category']in ['long','short']else e['category'])==book]
 for e in exercises:
  texts=[('title',e['title'])]
  if book in ['listening','reading']:
   texts += [('material',p['fr'])for p in e['paragraphs']if p.get('role')not in ['source','label']]
   for q in e['questions']:
    texts.append(('question',q['prompt']));texts += [('option',o['text'])for o in q.get('options',[])]
    texts.append(('answer',q.get('answer',{}).get('reference','')))
  else:
   texts += [('task',t.get('fr',''))for t in e.get('tasks',[])]
   # Oral source articles are deliberately excluded: themes + actual monologue/debate models only.
   texts += [('model:'+m['id'],p)for m in e.get('studyModels',[])for p in m['paragraphs']]
  for location,text in texts:
   for form in token.findall(text):
    lemma=lemma_of(form)
    if not lemma or lemma in stop or len(lemma)<4:continue
    lowercase[lemma]+=int(form[0].islower());freq[lemma]+=1;docs[lemma].add(e['id']);locations[lemma].add(location);wordforms[lemma].add(key(form))
    if location=='title':title_words.add(lemma)
 chosen=[]
 for word in freq:
  # Repeated task vocabulary, and accessible topic-specific terms appearing once.
  f=zipf_frequency(word,'fr');df=len(docs[word]);senses=entries[word].get('senses',[])
  if not lowercase[word]:continue
  if senses and not any(s.get('pos')in ['n','v','adj','adv','loc','locution','n.m','n.f']for s in senses):continue
  if f<2.5 or (f<3.4 and df<2 and word not in title_words):continue
  if not re.fullmatch('[a-zà-öø-ÿœæ-]+',word):continue
  chosen.append(word)
 chosen.sort(key=lambda w:(-len(docs[w]),-min(freq[w],30),-zipf_frequency(w,'fr'),w))
 sources[book]={w:sorted(docs[w])for w in chosen};forms[book]={w:sorted(wordforms[w])for w in chosen}
 for fr,zh in SUPPLEMENTS[book].items():
  fr=key(fr)
  if fr not in chosen:chosen.append(fr)
  if fr not in entries:manifest['lexicon'].setdefault('bookEntries',{})[fr]={'zh':zh,'curated':True,'usage':'本站补充 · C1任务表达'}
  sources[book].setdefault(fr,[])
 books[book]=chosen
 audit[book]={'exerciseCount':len(exercises),'selected':len(chosen),'corpusEntries':sum(bool(v)for v in sources[book].values()),'supplements':len(SUPPLEMENTS[book]),'locations':dict(collections.Counter(loc for w in chosen for loc in locations[w]))}
for category,words in books.items():
 corpus=[w for w in words if sources[category][w]];supplements=[w for w in words if not sources[category][w]]
 def importance(w):
  own=len(sources[category][w])/audit[category]['exerciseCount']
  other=sum(len(sources[c].get(w,[]))/audit[c]['exerciseCount']for c in books if c!=category)/3
  specificity=(own+.02)/(other+.02)
  familiarity=zipf_frequency(w,'fr')
  return math.log1p(len(sources[category][w]))*(.6+min(specificity,4))*(.3 if familiarity>5.3 else 1)
 corpus.sort(key=lambda w:(-importance(w),w))
 books[category]=corpus[:30]+supplements+corpus[30:]
manifest['lexicon']['books']=books;manifest['lexicon']['bookSources']=sources;manifest['lexicon']['bookForms']=forms
manifest['lexicon']['bookDescriptions']={
'listening':'从全部长、短听力的文本、题干、选项和参考答案提取，补充听辨、访谈与社会议题表达。',
'reading':'从全部阅读材料、题干、选项和参考答案提取，补充论证、逻辑关系与常见社会主题表达。',
'writing':'从全部写作题目、写作指令及综合、议论范文提取，补充组织论证和提出建议的常用表达。',
'speaking':'从全部口语主题及 monologue、débat 范文提取，补充回应异议、举例和互动讨论表达。'}
(ROOT/'public/content.json').write_text(json.dumps(manifest,ensure_ascii=False,separators=(',',':')))
report={'method':'Independent corpora; lemma frequency and document recurrence; common function words excluded; task-specific supplements; no quotas. Not an official exam-frequency list.','books':audit,'overlap':{a+'-'+b:len(set(books[a])&set(books[b]))for i,a in enumerate(books)for b in list(books)[i+1:]}}
(ROOT/'data/wordbooks-audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps(report,ensure_ascii=False,indent=2))
