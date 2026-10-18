import json,re,math,collections,unicodedata
from pathlib import Path
import spacy
ROOT=Path(__file__).resolve().parents[1]
source=json.loads((ROOT/'public/content.json').read_text())
nlp=spacy.load('fr_core_news_sm',disable=['parser','ner']);nlp.max_length=2000000

def norm(s):return ''.join(c for c in unicodedata.normalize('NFD',s.lower()) if not unicodedata.combining(c))
stop={norm(s) for s in nlp.Defaults.stop_words}|{'document','texte','auteur','journaliste','article','selon','expliquer','exemple','reponse','principal','donner','deux','raison','propos','question','interlocuteur','interviewe','intervenant'}
synsets=['collaboratif collaboration commun partager collectif ensemble','personnaliser individualise individuel adapter local','rentabilite rentable economique cout cher prix','numerique informatique technologie ordinateur','empathie emotion sentiment affectif affectivite amour aimer','baisse diminuer reduire recul decline declin','augmenter hausse croissance progresser developper expansion','adolescent jeune jeunesse enfant','emploi metier travail professionnel profession','ecole eleve scolaire enseignant professeur classe','femme feminin fille mere maternel','homme masculin garcon pere paternel','apprendre apprentissage apprendre connaissance savoir','peur crainte inquieter inquietude anxiete angoisse','croyance croire conviction','discrimination inegalite disparite ecart','biodiversite espece animal nature environnement','faux errone erreur trompeur desinformation','bonheur heureux epanouissement plaisir satisfaction','deconnexion deconnecter connexion connecter connecte disponibilite','marche marcher deplacement pied','difficile difficulte complexe complexite','liberte libre autonome autonomie','imagination imaginer creativite creer','sante soin medical medecin maladie','revenu remuneration salaire argent financement financier','securite securiser danger risque dangereux','patrimoine heritage culture culturel','memoire souvenir memoriser','insuffisant insuffisance manque limiter limite','sommeil dormir reve rever','pesticide chimique phytosanitaire','surveiller surveillance videosurveillance camera','voyager voyage tourisme touriste voyageur','noter note notation evaluation evaluer','lecture lire livre lecteur','mobilite transport voiture automobile trajet deplacement','defavorable negatif nefaste nuisible nocif','positif favorable benefice avantage utile utilite','diversite divers varier difference different','temps horaire heure duree','accessible acces accessibilite','gratuit gratuite abonnement payant','vrai verite reel realite','confiance confiant mefiance','investissement investir financement financer']
syn={norm(w):i for i,g in enumerate(synsets) for w in g.split()}
def tokens(doc):
 words=[norm(t.lemma_) for t in doc if t.is_alpha or t.like_num]
 return [w for w in words if w not in stop and len(w)>2]
def enrich(words):return set(words)|{'S'+str(syn[w]) for w in words if w in syn}
review=[]
for e in source['exercises']:
 if not e['questions']:continue
 sentences=[]
 for p in e['paragraphs']:
  chunks=re.split(r'(?<=[.!?])\s+(?=[A-ZÀ-Ü«])',p['fr'])
  for chunk in chunks:
   if len(chunk)<25:continue
   sentences.append({'pid':p['id'],'quote':chunk})
 docs=list(nlp.pipe([x['quote'] for x in sentences]));features=[enrich(tokens(d)) for d in docs]
 df=collections.Counter(w for f in features for w in f);idf=lambda w:math.log((len(features)+1)/(df[w]+1))+.5
 for q in e['questions']:
  ref=q.get('answer',{}).get('reference','');answer=next((o['text'] for o in q.get('options',[]) if o['id']==q.get('answer',{}).get('value')) ,ref)
  answer=re.split(r'[\u4e00-\u9fff]',answer)[0]
  a=enrich(tokens(nlp(answer)));b=enrich(tokens(nlp(q['prompt'])))
  weights={w:idf(w)*(3 if w in a else .7) for w in a|b}
  ranks=[]
  for i,f in enumerate(features):
   overlap=sum(weights[w] for w in f if w in weights)
   score=overlap/(max(1,len(f))**.25)
   if norm(sentences[i]['quote']) in norm(ref):score+=8
   ranks.append((score,i))
  top=sorted(ranks,reverse=True)[:3]
  review.append({'id':e['id'],'qid':q['id'],'number':q['number'],'prompt':q['prompt'],'answer':answer,'reference':ref,'candidates':[{**sentences[i],'score':round(score,2)} for score,i in top]})
(ROOT/'data/evidence-candidates.json').write_text(json.dumps(review,ensure_ascii=False,indent=2))
with open('/tmp/evidence-review.txt','w') as f:
 for x in review:
  f.write('\n'+x['id']+' '+x['qid']+' '+x['prompt']+'\nA: '+x['answer']+'\n')
  for i,c in enumerate(x['candidates']):f.write(str(i)+' '+c['pid']+' '+c['quote']+'\n')
print(len(review))
