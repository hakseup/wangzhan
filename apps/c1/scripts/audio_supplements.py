"""Review excerpts from the two audio-only attachments, without inventing exam questions."""
import json
from pathlib import Path
def exercise(n,title,zh,topic,paragraphs,rows):
 questions=[]
 for i,(prompt,options,key) in enumerate(rows,1):
  options=[{'id':chr(65+j),'text':t}for j,t in enumerate(options.split('|'))]
  questions.append({'id':'q'+str(i),'number':i,'type':'choice','prompt':prompt,'options':options,'answer':{'value':key,'reference':next(o['text']for o in options if o['id']==key)}})
 return {'id':f'short-2024-3-cn-{n}','category':'short','title':title,'titleZh':zh,'topic':topic,'source':'2024 年 3 月 · 中国场次 · 附件仅含音频','audioKey':'2024-3-cn','audioSegment':n,'practiceOrigin':'audio-supplement','transcriptionKind':'reviewed-excerpts','ocr':False,'sourceFiles':[f'2024年3月中国DALF C1短听力（{"一"if n==1 else"二"}）.m4a'],'paragraphs':[{'fr':p}for p in paragraphs],'questions':questions}
data=[exercise(1,'Les colocations à projets solidaires','用合租参与社区互助','社会与生活',[
 'De nouvelles formes de colocation émergent, comme la colocation intergénérationnelle. Il existe aussi le dispositif KAPS, pour « colocation à projets solidaires », géré par l’Afev.',
 'Les bénéficiaires s’engagent à participer à la vie de leur quartier en échange d’un loyer modéré.',
 'En pratique, les étudiants s’engagent à consacrer plusieurs heures par semaine à la vie du quartier où ils ont obtenu leur logement. Ils animent des temps de convivialité entre voisins et s’impliquent dans l’accompagnement des enfants.',
 'Un jardin potager permet de sensibiliser les habitants et les parents au jardinage, à la nature et à l’environnement, et de donner envie aux enfants de jardiner avec leurs parents.'
 ],[
 ('Dans cet extrait, que signifie le dispositif KAPS ?','Des colocations à projets solidaires.|Des logements réservés aux personnes âgées.|Des résidences sans engagement collectif.','A'),
 ('En échange d’un loyer modéré, les étudiants doivent…','devenir propriétaires du logement.|participer à la vie de leur quartier.|travailler pour une agence immobilière.','B'),
 ('Le jardin potager évoqué vise notamment à…','produire exclusivement pour les commerces.|remplacer l’accompagnement des enfants.|associer parents et enfants au jardinage et à l’environnement.','C')
 ]),exercise(2,'Le budget participatif à Paris','巴黎的参与式预算','城市与环境',[
 'Depuis trois ans, dans la capitale, la mairie propose aux Parisiens d’améliorer leur environnement grâce à un budget participatif. Plusieurs centaines de projets ont permis d’améliorer la vie de tous les jours.',
 'Les projets peuvent concerner des espaces végétalisés, des pistes cyclables ou la réhabilitation d’équipements. Ils doivent être d’intérêt général et relever de la compétence de la mairie.',
 'Une fois les projets examinés, les citoyens font leur choix. Les habitants peuvent voter sans distinction de nationalité ni d’âge : même les étrangers et les enfants peuvent participer. La seule condition est d’habiter la ville.',
 'Le vote peut se faire en ligne ou dans la rue, avec des urnes installées sur des triporteurs.'
 ],[
 ('À quoi sert le budget participatif présenté dans cet extrait ?','À financer des projets améliorant le cadre de vie.|À réserver les décisions aux entreprises privées.|À remplacer toutes les dépenses municipales.','A'),
 ('Pour être retenu, un projet doit notamment…','être proposé par un élu.|être d’intérêt général et relever de la compétence municipale.|bénéficier uniquement à son auteur.','B'),
 ('Qui peut participer au vote ?','Uniquement les Français majeurs.|Uniquement les propriétaires.|Les habitants, sans distinction d’âge ou de nationalité.','C')
 ])]
(Path(__file__).resolve().parents[1]/'data/audio-supplements.json').write_text(json.dumps(data,ensure_ascii=False,indent=2))
