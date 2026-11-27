"""Reviewed corrections for OCR layout, answer alignment and source-based supplements."""
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
bank=json.loads((ROOT/'data/raw-bank.json').read_text())
base={e['id']:e for e in bank}
out={}
def answer(v,ref=''):
 return {'value':v,'reference':ref or v}
def C(prompt,options,key,ref=''):
 return {'type':'choice','prompt':prompt,'options':[{'id':chr(65+i),'text':s} for i,s in enumerate(options.split('|'))],**({'answer':answer(key,ref)} if key else {})}
def T(prompt,ref='',accepted=None):
 return {'type':'text','prompt':prompt,**({'answer':{'reference':ref,**({'accepted':accepted} if accepted else {})}} if ref else {})}
def TF(prompt,key,ref):return {'type':'tf','prompt':'Vrai ou faux ? '+prompt,'answer':answer(key,ref)}
def put(id,qs=None,**patch):
 if qs is not None:
  for n,q in enumerate(qs,1):q.update(id='q'+str(n),number=n,sourceNumber=n)
  patch['questions']=qs
 out[id]={**out.get(id,{}),**patch}
def reuse(id,keys,refs={}):
 qs=base[id]['questions']
 for n,q in enumerate(qs,1):
  q.pop('answer',None)
  if n<=len(keys) and keys[n-1] in 'ABCVF' and keys[n-1]!='_':q['answer']=answer(keys[n-1],refs.get(n,''))
  elif n in refs:q['answer']={'reference':refs[n]}
 put(id,qs)

# Short listening: each recording has its own transcript and its own question sheet.
reuse('short-2021-6-cn-1','CBC')
reuse('short-2021-6-cn-2','BAC_', {4:'Ce sont les élèves qui notent les professeurs, et non l’inverse. 学生为老师打分，而非只有老师为学生打分。'})
old=base['short-2022-6-cn-1']['questions']
put('short-2022-6-cn-1',old[:4]);put('short-2022-6-cn-2',old[4:])
for id,keys in [('short-2022-6-cn-1','CBAB'),('short-2022-6-cn-2','CB_')]:
 for i,q in enumerate(out[id]['questions']):
  q.pop('answer',None)
  if keys[i]!='_':q['answer']=answer(keys[i])
  else:q['answer']={'reference':'Un budget annuel de cinq millions d’euros. 每年五百万欧元。','accepted':['5 millions d’euros','cinq millions d’euros','5 millions','5000000','500万欧元']}
reuse('short-2023-3-cn-1','BBC')
reuse('short-2023-3-cn-2','A_CC',{2:'La monnaie locale doit encourager la consommation et les échanges à l’échelle locale. 应促进本地消费与贸易。'})
put('short-2024-3-fr-1',[
 C('Le théâtre national de l’Opéra-Comique propose à des spectateurs…','d’offrir des billets à d’autres spectateurs.|de gagner un abonnement gratuit pour l’année.|d’acheter de bonnes places à des prix attractifs.','A','Le spectateur peut offrir une place à une personne qu’il ne connaît pas.'),
 C('Aujourd’hui, les personnes bénéficiaires de cette opération sont choisies en fonction de…','leur âge.|leur travail.|leurs revenus.','A','Le dispositif s’adresse aux jeunes de moins de 28 ans et aux étudiants.'),
 C('Selon Gérard Desportes, l’objectif de cette opération est…','de remplir davantage les salles.|de rendre l’opéra plus accessible.|de faire connaître de nouveaux artistes.','B'),
 T('Pourquoi Gérard Desportes considère-t-il que cette opération est symbolique ?','Il s’agit de partager la chance de connaître l’opéra avec un jeune qui ne le connaît pas forcément, sans connaître le bénéficiaire du don. 这是让他人共享文化体验的举动。')])
put('short-2024-3-fr-2',[
 C('L’enfant qui reçoit un vélo de l’association Solicycle promet…','de l’utiliser régulièrement.|de le maintenir en bon état.|de le partager avec ses camarades.','B'),
 C('Le moment le plus marquant pour Marianne Rallu est…','la validation de la charte par l’enfant.|l’échange entre l’ancien et le nouveau vélo.|la découverte du vélo par l’enfant et ses parents.','A','La signature de la charte responsabilise l’enfant.'),
 C('Les vélos de Solicycle sont obtenus grâce à…','la générosité des habitants.|des subventions de la mairie.|des financements d’entreprises.','A','Ce sont des vélos d’occasion reçus en don, réparés puis remis en circulation.')])
reuse('short-2024-6-cn-1','CBC')
reuse('short-2024-6-cn-2','ABC_', {4:'La capacité à être heureux ne suffit pas à neutraliser des conditions matérielles très difficiles, comme la précarité d’un chômeur en fin de droits. 幸福还受到现实生活条件的制约。'})
put('short-2024-11-cn-1',[
 C('Qu’est-ce que la « nomophobie » ? La peur de…','devenir dépendant de son téléphone portable.|tomber malade à cause du téléphone portable.|se retrouver sans téléphone portable disponible.','C'),
 C('Selon Mathieu Vidard, en plus de l’anxiété, quel autre symptôme peut accompagner la nomophobie ? Le fait…','d’être coupé de la réalité.|d’entendre des sons imaginaires.|d’avoir souvent des maux de tête.','B','Le journaliste évoque des hallucinations sonores et des signaux fantômes.'),
 C('Pour aider les nomophobes, Mathieu Vidard leur propose, entre autres…','d’utiliser un téléphone fictif.|d’acheter un forfait de téléphone restreint.|d’avoir un téléphone sans connexion Internet.','A','Le NoPhone est un faux téléphone qui ne sonne jamais.')])
put('short-2024-11-cn-2',[
 C('L’association dont parle l’émission met en relation l’art et…','l’humanitaire.|l’environnement.|la création d’emplois.','B'),
 T('Quel est le résultat visé par l’association ?','Donner une seconde vie aux déchets et matériaux en permettant aux professionnels de la culture de les réutiliser dans leurs créations. 让废弃材料在艺术创作中获得第二次生命。'),
 C('Pour pouvoir acheter les matériaux stockés, il faut obligatoirement être…','un artiste professionnel.|un membre de l’association.|un habitant de région parisienne.','B'),
 C('Les artistes apprécient de se fournir à la boutique de l’association parce qu’ils…','rencontrent souvent d’autres artistes.|trouvent des idées pour leurs créations.|encouragent l’association dans son action.','B')])
put('short-2025-3-cn-1',[
 C('D’après le journaliste, les intonations du mot « bonjour » reflètent…','l’éducation de la personne.|le caractère de la personne.|l’origine sociale de la personne.','B'),
 C('Pour les besoins de leur enquête, les chercheurs ont…','comparé les prononciations de « bonjour » entre hommes et femmes.|fait écouter à la suite plusieurs intonations de « bonjour » à des personnes.|enregistré des personnes qui disent « bonjour » avec différentes intonations.','B'),
 C('Les résultats de l’enquête montrent que les différences de perception sont…','minimes entre les personnes.|de plus en plus grandes avec l’âge.|expliquées par la disparité hommes / femmes.','A','Hommes et femmes perçoivent les intonations de façon similaire.')])
put('short-2025-3-cn-2',[
 C('D’après le journaliste, environ un quart des livres est…','récupéré par les éditeurs.|jeté aux ordures par les éditeurs.|envoyé au recyclage par les éditeurs.','C'),
 C('Il y a autant de livres invendus car…','l’édition française est en crise.|l’industrie du livre dysfonctionne.|la filière du livre produit en excès.','C'),
 C('Le journaliste rappelle que cette situation a des conséquences sur…','l’écologie.|la société.|l’économie.','A'),
 C('Qui semble avoir le plus conscience du problème actuellement ?','Les libraires.|Les éditeurs.|Les imprimeurs.','C')])
reuse('short-2025-6-cn-1','CAAB')
reuse('short-2025-6-cn-2','AB_', {3:'Les parents sont favorables à cette démarche écologique et souhaitent sa généralisation. 家长支持这一环保举措，希望推广。'})
reuse('short-2025-8-fr-1','CAC_', {4:'Des actions de sensibilisation et d’éducation à l’alimentation accompagnent le changement de cantine. 配合开展饮食与环保教育。'})
reuse('short-2025-8-fr-2','BCB')
reuse('short-2025-11-cn-1','ABC')
put('short-2025-11-cn-2',[
 T('En quoi consiste l’entreprise Peas and Love ?','Elle propose aux citadins de louer une parcelle de potager urbain, cultivée par un professionnel, dont ils peuvent récolter les produits. 向城市居民出租由专业园丁照料的菜园。'),
 C('Les jardins sont cultivés par…','des jardiniers confirmés.|l’ensemble des locataires.|le locataire de chaque parcelle.','A'),
 C('Les plantes cultivées sont choisies en fonction de…','leurs qualités nutritives.|la rapidité de leur croissance.|leur rareté dans les magasins.','C'),
 C('D’après le fondateur de Peas and Love, les plantes cultivées sont de très bonne qualité en raison…','du mode d’arrosage.|du lieu de plantation.|du type de semences.','C')])

# Long listening: clean digital questions and check the reference against the transcript.
reuse('long-2021-3-cn','B_C__A_C__C',{
 2:'Ils travaillent de manière collaborative et partagent leurs outils et leurs connaissances. 创客的特点是协作、共享工具与知识。',
 4:'Une production individualisée, communautaire et décentralisée, adaptée aux besoins locaux. 实现个性化、社区化、去中心化且满足本地需求的生产。',
 5:'Produire des objets moins coûteux et mieux adaptés ; réparer ou recycler des objets et des matériaux. 降低成本、按需定制，并便于维修和回收。',
 7:'L’informatique était au départ réservée à des passionnés avant de devenir accessible à tous. 早期计算机也局限于专业爱好者，随后逐渐普及。',
 9:'Le fonctionnement de Facebook repose sur une conception précise des relations sociales. 脸书的技术建立在对社会关系的特定理解之上。',
 10:'Des questions éthiques : une voiture autonome doit prendre des décisions morales dans certaines situations. 自动驾驶提出了伦理和道德选择的问题。'})
reuse('long-2022-11-cn','B__B_B_A_C_',{
 2:'L’utilisation de robots par l’armée est ancienne et documentée, contrairement aux robots domestiques. 军用机器人使用历史更长，有资料可查。',
 3:'Les soldats donnent un nom à leur robot et s’attachent à lui au point de vouloir le protéger. 士兵为机器人取名，甚至想要保护它。',
 5:'La parole, les gestes, les expressions du visage et les mouvements du corps. 语言、动作、面部表情和身体姿态。',
 7:'Les fabricants cherchent des robots agréables, toujours patients et adaptés aux attentes de l’acheteur pour mieux les vendre. 商业利益促使机器人迎合消费者。',
 9:'Le risque de préférer la compagnie prévisible et agréable des robots à celle des humains. 人可能依赖机器人，并疏远真实的人际关系。',
 11:'Le risque d’exploiter la solitude et la fragilité affective des personnes. 利用人的孤独和情感脆弱牟利。'})
reuse('long-2023-10-fr','AC__C___CC_',{
 3:'Pouvoir mieux articuler vie professionnelle et vie personnelle. 更好地协调工作与私人生活。',
 4:'Davantage de souplesse et d’autonomie dans l’organisation du travail. 在工作安排上获得更多灵活性与自主性。',
 6:'Elles associent la présence au bureau à la productivité et à la créativité collective. 企业将到岗与生产力、集体创新联系在一起。',
 7:'Un management fondé sur la confiance et les objectifs plutôt que sur le contrôle de la présence. 以信任和目标为基础的管理。',
 8:'Ils doivent acquérir l’expérience et les pratiques de l’entreprise au contact des collègues. 年轻员工需要在公司中学习经验和工作方式。',
 11:'Le préjugé selon lequel un salarié à domicile ne travaille pas réellement. 认为员工在家就没有认真工作的偏见。'})
reuse('long-2024-3-cn','C_CA AA_B____'.replace(' ',''),{
 2:'Consommer des loisirs pour se consoler ou oublier la réalité. 通过消费休闲活动来获得慰藉、暂时忘记现实。',
 7:'De nombreuses dépenses de transport et d’hébergement sont liées aux loisirs mais ne sont pas comptabilisées comme telles. 交通、住宿等休闲支出未被完整统计。',
 9:'Le temps libre joue désormais un rôle structurant dans la vie des individus. 休闲时间开始在生活中发挥结构性的作用。',
 10:'L’organisation urbaine reflète une culture du temps libre : rapport au corps, au soleil et à la nature. 城市空间反映了身体、阳光、自然等休闲需求。',
 11:'Les individus cumulent différentes fonctions et différents rôles sociaux. 多重社会角色与职能使人们更加流动。',
 12:'Les loisirs seront de plus en plus individualisés. 休闲将越来越个性化。'})
reuse('long-2024-6-cn','AB_A____A_',{
 3:'Elle est centrée sur les souvenirs et l’histoire personnelle de l’individu. 自传式记忆与个人经历及人生故事有关。',
 5:'Une mémoire construite dans les interactions et les échanges avec autrui. 在与他人的交往、交流中形成的记忆。',
 6:'Nos souvenirs se construisent toujours dans un cadre social et en relation avec les autres. 个人记忆始终存在于社会框架和人际关系之中。',
 7:'La mémoire collective acquiert sa propre existence et repose aussi sur des institutions, des monuments, les médias et l’éducation. 集体记忆也由纪念设施、媒体和教育塑造。',
 8:'Sur la définition des différents types de mémoire et les termes employés. 不同研究者难以统一记忆分类的定义与术语。',
 10:'Croiser les disciplines et faire dialoguer leurs approches de la mémoire. 加强学科间对话、结合不同研究方法。'})
reuse('long-2026-6-cn','B_C___A____B',{
 2:'Rédiger un rapport sur les sciences participatives. 撰写一份关于参与式科学的报告。',
 4:'Collecter des données, observer, contribuer à un projet commun ou participer à certaines étapes de la recherche. 收集数据、观察或参与集体研究。',
 5:'Le niveau de formation a augmenté et certains citoyens disposent de davantage de temps, notamment à la retraite. 受教育水平提高，部分人有更多可支配时间。',
 6:'L’envie de partager une passion et de contribuer à un domaine qui intéresse personnellement le participant. 分享个人兴趣并为感兴趣的领域作出贡献。',
 8:'Les outils numériques permettent de partager et de traiter les données à grande échelle. 数字工具支持大规模共享和处理数据。',
 9:'Le nombre de publications scientifiques issues de collaborations participatives. 通过参与式合作产生的科学论文数量。',
 10:'Ces projets se généralisent et certaines publications ne précisent plus leur origine collaborative. 合作研究日益普及，有些论文不再标明这一性质。',
 11:'Réduire les élèves à de simples exécutants sans leur faire comprendre la démarche scientifique. 避免学生只执行任务，而不理解科学方法。'})

# Correct the cold-science sheet: the original page has unnumbered questions.
put('long-2024-11-cn',[
 T('Selon la journaliste, pourquoi est-il paradoxal d’organiser une exposition scientifique sur le froid ?','Le froid n’a pas de véritable définition scientifique. 寒冷并不是一个严格的科学定义。'),
 C('Laurence Fournaison s’intéresse au froid…','mesuré dans la nature.|produit de façon artificielle.|ressenti par le corps humain.','B'),
 T('Pourquoi Laurence Fournaison trouve-t-elle difficile de définir le froid ?','Il s’agit d’une sensation subjective : dans les mêmes conditions, nous n’avons pas tous froid. 寒冷是主观感受，在相同条件下不同人的感觉不同。'),
 C('Jean-Louis Étienne s’intéresse…','à la manière dont le corps humain réagit au froid.|au froid maximal qu’on peut trouver dans la nature.|aux différentes techniques pour se protéger du froid.','A'),
 T('Que veut dire Jean-Louis Étienne lorsqu’il qualifie les êtres humains d’« homéothermes » ?','Notre température corporelle est régulée autour de 37 °C. 人体将体温维持在约 37 摄氏度。'),
 C('Jean-Louis Étienne a séjourné dans des régions polaires…','parce qu’il aime l’expérience du froid.|pour des nécessités professionnelles.|afin d’évaluer sa résistance physique.','B'),
 T('D’après Laurence Fournaison, quels sont les secteurs les plus consommateurs de froid ?','L’industrie agroalimentaire et l’industrie pharmaceutique. 食品工业和制药工业。'),
 C('D’après la journaliste, de nos jours, il est important de s’interroger sur…','l’utilisation du froid.|la répartition du froid.|la fabrication du froid.','C'),
 T('Quels sont les deux objectifs des recherches menées par Laurence Fournaison ?','Développer des systèmes moins consommateurs d’énergie et plus efficaces. 开发能耗更低、能源效率更高的系统。'),
 T('Selon Laurence Fournaison, pourquoi ses recherches ont-elles un caractère vital ?','Pour faire face au réchauffement climatique et à l’augmentation de la consommation énergétique. 应对全球变暖和不断增加的能源需求。')])

# Restored stems from visual inspection where OCR skipped entire lines.
put('long-2021-5-cn',[
 C('Quel est le thème de cet entretien ?','Les applications concrètes de la recherche scientifique.|Le problème du recrutement de chercheurs en sciences.|La difficulté à créer une entreprise en lien avec la recherche scientifique.','A'),
 T('De quel domaine professionnel est issue Mélanie Marcel ?','Elle vient de la recherche scientifique, dans le domaine des neurosciences. 她来自科学研究／神经科学领域。'),
 T('D’après Mélanie Marcel, quel est l’apport majeur de l’entreprise SoScience ? Donnez deux réponses.','Remettre la science au service de la société et établir des partenariats entre laboratoires publics et entrepreneurs sociaux. 让科学重新服务社会，建立公共实验室与社会企业之间的合作。'),
 C('Selon Mélanie Marcel, la principale difficulté des entreprises pour élaborer leurs projets est…','de recruter du personnel scientifique.|de financer leurs besoins scientifiques.|de se faire comprendre des scientifiques.','C'),
 T('Pour Mélanie Marcel, en quoi y a-t-il inégalité entre les grandes et les petites entreprises ?','Seules les grandes entreprises disposent des moyens nécessaires pour financer leurs recherches. 大企业有足够资金资助研究，小企业未必有。'),
 T('Quel type de projet l’entreprise SoScience soutient-elle majoritairement ? Donnez deux réponses.','Des entreprises qui ne peuvent financer la recherche et des projets éthiques ou innovants. 无力支付研究费用的企业，以及具有伦理意义或创新性的项目。'),
 T('D’après Mélanie Marcel, quel peut être l’intérêt pour un étudiant en master à collaborer avec SoScience ?','Associer sa passion scientifique à une recherche portant sur des enjeux de société. 把对科学的兴趣与社会议题研究结合起来。'),
 C('SoScience intervient dans des écoles d’ingénieurs pour…','recruter de futurs partenaires.|informer des débouchés en sciences.|financer son propre développement économique.','B'),
 T('Quel objectif recherche Mélanie Marcel en proposant des formations aux entreprises ?','Montrer qu’une grande entreprise peut mener une réflexion sur une recherche éthique. 促使大企业反思如何开展合乎伦理的研究。'),
 T('Comment peut se répartir la propriété intellectuelle dans les projets soutenus par SoScience ? Donnez deux réponses.','Soit l’innovation est ouverte, soit la propriété intellectuelle est partagée entre l’entreprise sociale et le laboratoire. 创新成果可开放共享，或由社会企业与实验室共享知识产权。'),
 T('Pourquoi Mélanie Marcel soutient-elle la recherche fondamentale ?','Elle peut avoir des applications sociales à plus ou moins long terme. 基础研究也可能在未来产生社会应用。'),
 C('Que dénoncent les scientifiques dont parle la journaliste ?','La délocalisation de la recherche fondamentale.|La baisse des crédits pour la recherche fondamentale.|La mainmise du privé sur la recherche fondamentale.','B')])
put('long-2022-6-cn',[
 T('Quel sujet Bruno Denaez a-t-il choisi de traiter pour inaugurer la semaine de la langue française ?','L’usage de la langue française par les journalistes de radio. 广播记者如何使用法语。'),
 T('Pourquoi Bernard Cerquiglini a-t-il été invité dans cette émission ?','Il est linguiste et a dirigé un organisme international consacré à la langue française. 他是语言学家，也曾负责国际语言机构。'),
 T('Bernard Cerquiglini évoque deux types d’oral. Lesquels ?','L’oral familier et l’oral soutenu. 通俗口语与雅语／正式口语。'),
 T('Pour Bernard Cerquiglini, quel doit être le rôle de la radio dans le domaine de la langue et à quoi peut-on le comparer ?','La radio doit fournir un modèle de langue, comme les instituteurs autrefois. 广播应像过去的小学教师一样，提供语言使用的范例。'),
 C('Pour Bernard Cerquiglini, la langue familière est acceptable à la radio…','quand c’est une personne interrogée qui l’utilise.|quand un journaliste couvre un événement sportif.|quand certains mots n’ont pas d’équivalent moins familier.','A'),
 C('Pourquoi Simon reproche-t-il aux journalistes de trop utiliser le mot « ubérisation » ?','Parce que ce n’est pas un mot d’origine française.|Parce qu’il est incompréhensible pour beaucoup de gens.|Parce qu’on l’emploie sans raison à propos de n’importe quel sujet.','C'),
 T('Comment Bernard Cerquiglini justifie-t-il l’emploi d’un néologisme tel qu’« ubérisation » ?','La création de mots permet au français de décrire le monde contemporain. 新词的创造使法语可以描述当代世界。'),
 C('Concernant les expressions à la mode, Bernard Cerquiglini pense que le rôle de la radio est…','de les adopter afin de rester proche des auditeurs.|d’éviter systématiquement les expressions toutes faites.|d’utiliser seulement les expressions devenues très populaires.','B'),
 T('Qu’est-ce qui montre que certaines expressions ne sont qu’un phénomène de mode ?','Elles disparaissent rapidement avant même qu’on s’en aperçoive. 某些表达很快就消失了。'),
 C('Selon Bernard Cerquiglini, les journalistes devraient…','éviter totalement de recourir à des anglicismes.|employer uniquement les anglicismes les plus courants.|s’efforcer de n’employer que les équivalents français des anglicismes.','C'),
 T('Dans quel domaine la francisation des mots anglais a-t-elle été un succès ?','Dans le domaine de l’informatique. 信息技术／计算机领域。',['l’informatique','informatique','计算机领域','信息技术领域']),
 C('Selon Bernard Cerquiglini, préférer les mots français, pour un journaliste, c’est…','respecter son public.|affirmer son individualité.|montrer une forme de snobisme.','B')])
put('long-2023-11-cn',[
 T('Quelles sont les personnes désignées par le terme de « génération Z » ?','Les personnes nées entre 1995 et 2010. 1995 至 2010 年出生的人。'),
 C('Pour Emmanuelle Duez, ce qui caractérise le mieux cette génération Z est l’idée…','d’anarchie.|de mutation.|de conformisme.','B'),
 C('Selon Monique Dagnaud, la génération Z…','reproduit le modèle de la génération Y.|s’oppose radicalement à la génération Y.|intensifie les caractéristiques de la génération Y.','C'),
 T('D’après Monique Dagnaud, quel phénomène sociétal coïncide avec l’émergence de la génération Y ?','L’entrée dans l’ère de la transformation numérique. 进入数字化转型时代。'),
 T('Selon la journaliste, comment Emmanuelle Duez perçoit-elle la génération Z ?','Comme une génération multiple et diverse, aux identités multiples. 这一代人是多样的，具有多重身份。'),
 T('Pourquoi Emmanuelle Duez est-elle gênée par le nom même de « génération Z » ?','Ce phénomène dépasse une génération et reflète une transformation globale de la société. 这不只是代际现象，更体现了整体社会变革。'),
 T('Quelles sont les trois caractéristiques du monde dans lequel évolue la génération Z ?','Un monde digitalisé, globalisé et accéléré. 数字化、全球化、加速变化的世界。'),
 C('Selon Monique Dagnaud, la notion de génération est instable en raison des différences dans…','la catégorie sociale des individus.|le niveau de formation des individus.|l’origine géographique des individus.','B'),
 T('Quelle idée reçue dénonce Monique Dagnaud sur le rapport entre monde digital et génération Z ?','L’idée que ces jeunes sont isolés devant leurs écrans ; ils ont au contraire une sociabilité intense. 年轻人并非都孤立在屏幕前，他们也有丰富的社交生活。'),
 C('Pour Monique Dagnaud, la génération Z se définit par…','la solidarité et l’échange.|l’ouverture aux autres générations.|l’engagement dans les grandes causes.','A'),
 T('D’après Monique Dagnaud, quelles valeurs la génération Z a-t-elle reçues de ses parents ?','La communication, l’expression et la possibilité pour l’enfant de faire entendre son point de vue. 沟通、表达，以及重视儿童发声。')])
put('long-2024-3-cn',[
 C('Ce document traite…','des loisirs préférés des Français.|de l’inégalité des Français devant les loisirs.|de la place des loisirs dans la vie des Français.','C'),
 T('Comment la journaliste résume-t-elle l’expression « société de consolation » ?','Consommer des loisirs pour oublier la réalité. 消费休闲活动以获得慰藉、忘记现实。'),
 C('Selon Gérard Mermet, la société française s’interroge de plus en plus sur…','le financement des loisirs.|la grande diversité des loisirs aujourd’hui.|l’impact des loisirs sur notre épanouissement.','C'),
 C('Selon Jean Viard, le temps travaillé va…','diminuer.|augmenter.|se stabiliser.','A'),
 C('Selon Jean Viard, le travail devient de plus en plus…','soutenu.|fatiguant.|compliqué.','A'),
 C('Jean Viard estime que le contenu du temps libre dépend surtout…','de la volonté de chacun.|du revenu de chacun.|de l’origine sociale de chacun.','A'),
 T('Pourquoi les statistiques de l’Insee ne sont-elles pas révélatrices des dépenses des Français concernant les loisirs ?','Elles ne comptabilisent pas comme loisirs toutes les dépenses de transport et d’hébergement qui y sont liées. 交通和住宿等关联支出未计入休闲支出。'),
 C('D’après Jean Viard, les Français profitent davantage du temps libre en raison de…','l’augmentation de leurs revenus.|l’allongement de l’espérance de vie.|la réduction des inégalités sociales.','B'),
 T('Selon Jean Viard, quel rôle joue le temps libre dans la vie des individus ?','Il est devenu structurant. 休闲时间发挥着结构性的作用。'),
 T('Comment la ville d’aujourd’hui montre-t-elle que nous sommes dans une société de loisirs ?','La culture du temps libre façonne le rapport au corps, au soleil et à la nature dans la ville. 城市体现了身体、阳光和自然等休闲需求。'),
 T('Comment les deux invités expliquent-ils que nous soyons de plus en plus mobiles ?','Nous exerçons plusieurs fonctions et rôles sociaux. 我们有多重职能与社会角色。'),
 T('Selon Gérard Mermet, quelle sera la caractéristique principale des loisirs dans le futur ?','Les loisirs seront liés au virtuel. 休闲将与虚拟世界相联系。')])
put('long-2024-3-fr',[
 T('Quelle est la contradiction relevée par le présentateur au début de l’émission ?','Les parents évaluent avec des notes alors que celles-ci demeurent un sujet d’inquiétude. 家长依赖分数，但分数也带来担忧。'),
 T('Comment Laetitia Ferrari propose-t-elle de voir l’évaluation pour la rendre bénéfique ?','Comme un moyen de progresser et non comme une punition. 把评价看作进步的手段，而非惩罚。'),
 T('Selon Pierre Merle, pourquoi la note apparaît-elle indispensable du point de vue de la société ?','Elle permet de classer les élèves. 分数可用来给学生排序。'),
 T('Selon Pierre Merle, pourquoi la note revêt-elle une importance plus grande qu’auparavant ?','Elle est liée aux diplômes, indispensables à l’insertion professionnelle et sociale. 分数与融入职场和社会所需的文凭相关。'),
 T('Pour Pierre Merle, quelles sont les conséquences des mauvaises notes sur les élèves ? Donnez deux réponses.','Le décrochage, le manque de motivation ou la perte de confiance en soi. 辍学、失去动力或缺乏自信。'),
 C('Pierre Merle estime que l’évaluation est nécessaire pour permettre…','aux professeurs de fixer des objectifs précis.|aux parents de suivre les progrès de leur enfant.|aux élèves d’obtenir un avis extérieur sur leur travail.','C'),
 C('Laetitia Ferrari propose de lutter contre la subjectivité de la note en…','supprimant l’évaluation faite de notes chiffrées.|permettant à la classe de co-construire l’évaluation.|faisant évaluer les élèves par plusieurs professeurs.','B'),
 C('À quel élément Loys Bonod accorde-t-il le plus d’importance dans son travail d’évaluateur ?','La note finale obtenue.|Le corrigé des exercices.|Les remarques sur la copie.','C'),
 C('De nombreux parents préfèrent l’utilisation des notes, car…','ils les trouvent stimulantes pour les enfants.|les autres systèmes leur conviennent moins.|ils sont familiarisés avec leur fonctionnement.','C'),
 T('Selon Pierre Merle, quels sont les parents les moins favorables au système des notes à l’école ?','Les parents dont les enfants rencontrent le plus de difficultés scolaires. 孩子在学校遇到较大困难的家长。'),
 T('Pour Pierre Merle, quelles sont les deux visions de l’école qui s’opposent aujourd’hui ?','Une école inclusive qui accueille tous les élèves et une école fondée sur la sélection. 包容所有学生的学校，与以筛选为基础的学校。')])
put('long-2025-11-cn',[
 C('Cette émission a pour but de…','critiquer un projet.|présenter une initiative.|comparer des pratiques.','B'),
 T('Que propose l’entreprise Magic Makers ?','Des ateliers de programmation informatique destinés aux jeunes. 为青少年提供编程课程。'),
 T('Selon Claude Térosier, en quoi les activités proposées par Magic Makers sont-elles adaptées aux enfants ?','Elles sont ouvertes aux enfants, avec des consignes simples et concrètes qui leur permettent de créer des choses porteuses de sens. 活动指令简单具体，帮助孩子创造有意义的事物。'),
 C('Les enfants peuvent participer aux stages de Magic Makers à condition…','de savoir lire et écrire.|d’avoir des notions d’informatique.|d’avoir des compétences en mathématiques.','A'),
 T('En quoi les activités de Magic Makers se distinguent-elles de l’utilisation habituelle des écrans ?','Les enfants créent et réfléchissent activement au lieu de consommer passivement. 孩子是主动创造和思考，而非被动消费。'),
 C('Selon Claude Térosier, participer aux stages Magic Makers permet aux enfants…','d’accroître leur attention.|d’affirmer leur personnalité.|de développer leur socialisation.','A'),
 T('Pourquoi Claude Térosier qualifie-t-elle la démarche de Magic Makers de « pédagogie active » ?','L’enfant apprend en concevant lui-même un projet et en le réalisant jusqu’au bout. 孩子通过自己设计并完成项目来学习。'),
 C('Pour Claude Térosier, rendre les enfants actifs en informatique leur fait prendre conscience…','de l’aspect humain lié à cette activité.|du besoin de mutualisation des compétences.|de la complémentarité de cette matière avec d’autres.','A'),
 T('Selon Claude Térosier, en quoi Magic Makers joue-t-elle un rôle civique ?','Elle donne aux jeunes les moyens de devenir des citoyens et des acteurs de la société numérique. 帮助年轻人成为数字社会的公民和参与者。'),
 T('Qu’auront appris les enfants à travers cette expérience malgré le développement continu de l’informatique ?','Ils auront compris la logique informatique. 他们将理解计算机的逻辑。'),
 C('La plus grande participation des garçons est due, selon Claude Térosier, à un…','conditionnement par l’école.|choix de la part des parents.|manque de motivation des filles.','B'),
 T('Pourquoi Claude Térosier a-t-elle choisi de cibler un public d’enfants et non d’adultes ? Donnez deux réponses.','Apprendre l’informatique est plus facile enfant, et ces enfants sont les adultes de demain. 儿童更容易学习计算机，他们也是未来的成年人。')])
put('long-2025-6-cn',[
 C('Les commentaires des auditeurs font ressortir que, pour eux, la littérature est…','un remède contre l’ennui.|un soutien psychologique.|un passe-temps reposant.','B'),
 T('Selon Christine Henniqueau, quelle est la fonction de la littérature dans la société ?','Elle nous relie aux autres, au monde et à nous-mêmes. 文学把我们与他人、世界及自身联系起来。'),
 C('D’après Christine Henniqueau, la lecture…','déçoit les jeunes d’aujourd’hui.|effraie les jeunes d’aujourd’hui.|ennuie les jeunes d’aujourd’hui.','B'),
 T('Pourquoi certains adolescents voient-ils les livres comme un autre monde ?','Ils ont l’impression que les auteurs ne s’adressent pas à eux ; le sens et les mots leur échappent. 他们觉得作者并非为自己而写，也难以理解词语和意义。'),
 T('Que pense Sarah Sauquet de l’évolution des pratiques de lecture des jeunes ? Donnez deux réponses.','Les pratiques de lecture changent et ne se limitent plus au livre traditionnel ; il faut partir des usages réels des jeunes pour les accompagner. 阅读方式正在变化，应从年轻人的实际阅读习惯出发。'),
 C('D’après Sarah Sauquet, quelle activité permet d’inciter les jeunes à lire ?','Des séances de lecture collective.|Des travaux préalables à la lecture.|Des exposés à l’issue de la lecture.','B'),
 T('Pourquoi Sarah Sauquet parle-t-elle de « difficulté culturelle » ?','Il manque parfois aux élèves les références et les codes nécessaires pour entrer dans une œuvre. 学生有时缺少理解文学作品所需的文化背景。'),
 T('Quel constat a motivé Sarah Sauquet à créer des applications pour smartphone ?','Le smartphone occupe une grande place dans la vie des jeunes : il peut devenir un moyen de rencontre avec les textes. 手机可以成为年轻人接触文学的新入口。'),
 C('Les textes proposés sur l’application Un texte, un jour sont des extraits…','de livres francophones récents.|d’œuvres d’auteurs français du passé.|de romans internationaux du XXe siècle.','B'),
 C('L’application Un texte, un jour permet…','de lire les extraits avec un lexique simplifié.|d’écouter une version audio des extraits choisis.|d’accéder à diverses ressources complémentaires.','C')])
put('long-2026-3-cn',[
 C('Dans cet entretien, Thierry Paquot propose de…','limiter l’extension et la croissance des villes.|varier les types d’habitats des ensembles urbains.|mettre en adéquation l’individu et son cadre de vie.','C'),
 T('Selon Thierry Paquot, en quoi l’agriculteur français appartient-il à la sphère de la ville ?','Il adopte les modes de vie urbains même s’il ne réside pas en ville. 即使不住在城市，农民也采取城市人的生活方式。'),
 C('Pour Thierry Paquot, la notion de ville est…','dépassée.|pertinente.|indispensable.','A'),
 T('Citez deux caractéristiques propres à l’idée que se fait Thierry Paquot de la ville.','L’urbanité, la diversité et l’altérité. 城市性、多样性、他者性，答出其中两项。'),
 C('Selon Thierry Paquot, l’augmentation de la population citadine va…','redéfinir la notion de ville.|améliorer la qualité des villes.|réduire l’espace de vie de chacun.','A'),
 C('Thierry Paquot dénombre cinq types d’architectures citadines qui ont en commun de…','séparer les individus les uns des autres.|favoriser les échanges entre les habitants.|donner trop d’importance à la sécurisation des espaces.','A'),
 T('D’après Thierry Paquot, quel est l’effet des ensembles urbains sur l’être humain ?','Ils l’enferment dans l’espace mais aussi dans le temps. 城市建筑群不仅限制人的空间，也限制人的时间。'),
 T('Pour Thierry Paquot, quel mot devrait remplacer le mot « proximité » ?','Le familier. 熟悉、亲近的。',['familier','le familier','熟悉的']),
 T('Pourquoi Thierry Paquot qualifie-t-il les gratte-ciel d’une « impasse en hauteur » ?','Leur hauteur n’améliore pas les conditions de vie de l’individu. 摩天大楼的高度并不改善个人的生活条件。'),
 T('En quoi l’idée de progrès ne s’accorde-t-elle pas avec la nature de l’être humain ?','Le progrès favorise la vitesse et l’excès, alors que l’humain a besoin d’équilibre, de stabilité et de modération. 进步偏向速度与过度，而人需要平衡、稳定与节制。'),
 T('Quel aspect William Morris avait-il associé à la recherche du beau dans ses créations ?','Le souci de créer des objets et un cadre à l’échelle humaine. 将美与适合人的尺度和需求相联系。'),
 C('Le fait que la journaliste qualifie Thierry Paquot d’utopiste…','le gêne.|le satisfait.|le contrarie.','B')])

# Source answer keys checked against the actual recording transcripts.
out['short-2022-6-cn-1']['questions'][3]['answer']=answer('C')
out['short-2022-6-cn-2']['questions'][2]['answer']={'reference':'Un budget annuel de trois millions d’euros. 每年三百万欧元。','accepted':['3 millions d’euros','trois millions d’euros','3 millions','3000000','300万欧元']}
out['short-2025-3-cn-2']['questions'][3]['answer']=answer('B','Les éditeurs sont présentés comme les plus engagés pour le moment.')
out['short-2025-11-cn-2']['questions'][2]['answer']=answer('B','Les plantes prennent peu de place et se récoltent sur une courte période.')
out['short-2025-11-cn-2']['questions'][3]['answer']=answer('B','Les cultures en toiture sont éloignées des particules fines et utilisent un substrat biologique.')
out['long-2026-6-cn']['questions'][2]['answer']=answer('B')

from curate_reading import curate_reading
curate_reading(base,put,C,T,TF,answer)
from curate_mocks import curate_mocks
curate_mocks(put,C,T,TF)

# Preserve reviewed labels in a normal JSON asset for reproducible imports.
(ROOT/'data').mkdir(exist_ok=True)
(ROOT/'data'/'overrides.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
print('Reviewed',len(out),'exercise sheets')
