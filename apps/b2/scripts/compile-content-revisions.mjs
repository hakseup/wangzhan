import {readFileSync,readdirSync,writeFileSync,mkdirSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {dictKey} from '../src/dictionary.js';
const hash=text=>createHash('sha256').update(text).digest('hex');
const entities={quot:'"',apos:"'",amp:'&',lt:'<',gt:'>',nbsp:' '};
const radicals={'⻓':'长','⻉':'贝','⻄':'西','⻝':'食','⻋':'车','⺠':'民','⻢':'马','⻔':'门','⻛':'风','⻘':'青','⻚':'页','⻅':'见','⻬':'齐','⻜':'飞','⻆':'角','⻤':'鬼','⻙':'韦'};
export function cleanChinese(text){
 if(typeof text!=='string')return text;
 for(let i=0;i<3;i++)text=text.replace(/&(#x[\da-f]+|#\d+|quot|apos|amp|lt|gt|nbsp);/gi,(_,key)=>key[0]==='#'?String.fromCodePoint(parseInt(key.slice(key[1]?.toLowerCase()==='x'?2:1),key[1]?.toLowerCase()==='x'?16:10)):entities[key.toLowerCase()]);
 return text.normalize('NFC').replace(/[\u2e80-\u2fff\uf900-\ufaff]/g,c=>radicals[c]||c.normalize('NFKC')).replace(/[\u0000-\u0008\u000b\u000e-\u001f\u200b\ufeff]/g,'').replace(/([\u3400-\u9fff])[ \t]+(?=[\u3400-\u9fff])/g,'$1');
}
const tokens=text=>new Set((text||'').normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase().match(/[a-z]{4,}|\d+/g)?.filter(t=>!['dans','avec','pour','plus','cette','comme','leur','leurs','elle','elles','vous','nous','entre','mais','sont','etre','avoir','tout','tous','selon','apres','avant','pourquoi','quels','quelle','quelles'].includes(t))||[]);
const overlap=(a,b)=>[...a].filter(t=>b.has(t)).length/Math.max(1,Math.sqrt(a.size));
function tidyFields(value,key=''){
 if(Array.isArray(value))return value.map(v=>tidyFields(v,key));
 if(value&&typeof value==='object')return Object.fromEntries(Object.entries(value).map(([k,v])=>[k,tidyFields(v,k)]));
 return ['zh','titleZh','reason','answer','reference'].includes(key)&&typeof value==='string'?cleanChinese(value):value;
}
export function compileContentRevisions(){
 const bank=JSON.parse(readFileSync('public/content.json')),original=new Map(bank.exercises.map(e=>[e.id,e]));
 const revisions=readdirSync('data/translation-review/revisions').filter(f=>f.endsWith('.json')).map(f=>JSON.parse(readFileSync('data/translation-review/revisions/'+f)));
 const revised=new Map(bank.exercises.map(e=>[e.id,tidyFields(structuredClone(e))]));let reviewed=0,corrected=0;
 for(const revision of revisions){
  const source=original.get(revision.id),exercise=revised.get(revision.id);if(!source)throw Error('Unknown exercise '+revision.id);
  for(const patch of revision.paragraphs){
   const before=source.paragraphs.find(p=>p.id===patch.id),p=exercise.paragraphs.find(p=>p.id===patch.id);if(!p||hash(before.fr)!==patch.sourceHash)throw Error('Source changed '+revision.id+':'+patch.id);
   const sourceUnits=patch.sourceCorrection?.units||before.sentenceTranslations?.map(s=>s.fr)||[before.fr];
   if(sourceUnits.length!==patch.translations.length||patch.translations.some(t=>typeof t!=='string'||!t.trim()))throw Error('Missing translation '+revision.id+':'+patch.id);
   const translated=patch.translations.map(cleanChinese);p.zh=translated.join('');p.translationReviewed=true;
   if(patch.sourceCorrection){
    const units=sourceUnits.map(u=>u.trim());p.fr=units.join(' ');let offset=0;
    p.sentenceTranslations=units.map((fr,i)=>{const text=fr+(i<units.length-1?' ':'');const start=offset;offset+=text.length;return {start,end:offset,fr:text,zh:translated[i]};});
    p.sourceRepair=patch.sourceCorrection.reason;corrected++;
   }else if(before.sentenceTranslations?.length)p.sentenceTranslations=before.sentenceTranslations.map((s,i)=>({...s,zh:translated[i]}));
   if(patch.sourceIssue)p.sourceIssue=patch.sourceIssue;reviewed++;
  }
 }
 let translatedQuestions=0;const translatedIDs=new Set();
 for(const file of ['questions-1.json','questions-2.json','questions-3.json']){
  for(const patch of JSON.parse(readFileSync('data/translation-review/'+file))){
   const e=revised.get(patch.id);if(!e)throw Error('Unknown questions '+patch.id);
   for(const item of patch.questions){const q=e.questions.find(q=>q.id===item.id);if(!q||q.options.length!==item.options.length||translatedIDs.has(item.id)||new Set(item.options.map(o=>o.id)).size!==q.options.length)throw Error('Invalid question '+item.id);translatedIDs.add(item.id);if((item.prompt&&!item.sourceRepair)||item.options.some(o=>o.text&&!o.sourceRepair&&!item.sourceRepair))throw Error('Undocumented source repair '+item.id);q.zh=cleanChinese(item.zh);if(item.prompt)q.prompt=item.prompt;if(item.sourceRepair)q.sourceRepair=item.sourceRepair;if(item.sourceIssue)q.sourceIssue=item.sourceIssue;for(const option of item.options){const o=q.options.find(o=>o.id===option.id);if(!o)throw Error('Invalid option '+item.id);o.zh=cleanChinese(option.zh);if(option.text)o.text=option.text;if(option.sourceRepair)o.sourceRepair=option.sourceRepair;}translatedQuestions++;}
  }
 }
 let reanchored=0;
 for(const e of revised.values()){
  const allUnits=e.paragraphs.flatMap(p=>(p.sentenceTranslations||[{start:0,end:p.fr.length,fr:p.fr,zh:p.zh}]).map(s=>({...s,pid:p.id,words:tokens(s.fr)})));
  const pairs=[];
  for(const q of e.questions){
   const selected=q.options.find(o=>o.id===q.answer?.value),reference=tokens(q.answer?.reference),context=tokens(q.prompt+' '+(selected?.text||''));
   for(const [index,v]of (q.explanation?.evidence||[]).entries()){
    let p=e.paragraphs.find(p=>p.id===v.pid),start=p?.fr.indexOf(v.quote)??-1;
    if(start<0){
     const old=tokens(v.quote),ranked=allUnits.map(s=>({s,score:overlap(reference,s.words)*4+overlap(context,s.words)*2+overlap(old,s.words)})).sort((a,b)=>b.score-a.score);
     const s=ranked[0]?.s;if(!s)continue;v.pid=s.pid;v.quote=s.fr;v.zh=s.zh;v.confirmed=false;p=e.paragraphs.find(p=>p.id===v.pid);start=s.start;reanchored++;
    }else{
     const units=(p.sentenceTranslations||[]).filter(s=>s.start<start+v.quote.length&&s.end>start);v.zh=units.length?units.map(s=>s.zh).join(''):p.zh;
    }
    const id=v.pairIds?.[0]||`${q.id}-e${index}`;v.pairIds=[id];pairs.push({id,pid:v.pid,start,end:start+v.quote.length,fr:v.quote,zh:v.zh,confirmed:v.confirmed});
   }
  }
  if(pairs.length)e.reviewPassages=pairs;
 }
 const updates=[...revised.values()].map(e=>({id:e.id,paragraphs:e.paragraphs,questions:e.questions,reviewPassages:e.reviewPassages}));
 const translations={};
 for(const e of revised.values()){
  for(const p of e.paragraphs){if(p.zh)translations[dictKey(p.fr)]=p.zh;for(const s of p.sentenceTranslations||[])if(s.zh)translations[dictKey(s.fr)]=s.zh;}
  for(const q of e.questions){if(q.zh)translations[dictKey(q.prompt)]=q.zh;for(const o of q.options||[])if(o.zh)translations[dictKey(o.text)]=o.zh;}
 }
 const payload={version:hash(JSON.stringify(updates)).slice(0,16),exercises:updates,translations};
 const dictionaryFixes=JSON.parse(readFileSync('data/translation-review/dictionary-fixes.json')).map(fix=>{
  if(!['entries','bookEntries'].includes(fix.section)||!bank.lexicon[fix.section]?.[fix.key])throw Error('Unknown dictionary repair');
  const entry=tidyFields(fix.entry);if(/[⁇�]|&(?:quot|amp|nbsp);/.test(JSON.stringify(entry)))throw Error('Unrepaired dictionary entry '+fix.key);
  return {...fix,entry};
 });
 payload.version=hash(JSON.stringify({updates,dictionaryFixes})).slice(0,16);
 const lexicon={...bank.lexicon,translations,entries:{...bank.lexicon.entries},bookEntries:{...bank.lexicon.bookEntries}};
 for(const fix of dictionaryFixes)lexicon[fix.section][fix.key]=fix.entry;
 const allParagraphs=[...revised.values()].flatMap(e=>e.paragraphs);
 for(const p of allParagraphs)if(/[⁇�]|&(?:amp;)?(?:quot|apos|nbsp);/.test(p.zh||''))throw Error('Unrepaired Chinese corruption '+p.id);
 const baseline=bank.exercises.flatMap(e=>e.paragraphs).filter(p=>p.translationReviewed===false).length;
 if(allParagraphs.filter(p=>p.translationReviewed===false).length)throw Error('Unreviewed machine translation remains');
 if(translatedQuestions!==bank.exercises.reduce((n,e)=>n+e.questions.length,0))throw Error('Not all questions translated');
 const categories=[...new Set(bank.exercises.map(e=>e.category))];
 const parts=categories.map(category=>{
  const exercises=updates.filter(e=>original.get(e.id).category===category),keys=new Set();
  for(const e of exercises){for(const p of e.paragraphs){keys.add(dictKey(p.fr));for(const s of p.sentenceTranslations||[])keys.add(dictKey(s.fr));}for(const q of e.questions){keys.add(dictKey(q.prompt));for(const o of q.options)keys.add(dictKey(o.text));}}
  return {version:payload.version,category,exercises,translations:Object.fromEntries([...keys].filter(key=>translations[key]).map(key=>[key,translations[key]])),dictionaryFixes:category==='long'?dictionaryFixes:[]};
 });
 mkdirSync('cloud',{recursive:true});writeFileSync('cloud/content-revisions.json',JSON.stringify({version:payload.version,categories}));
 for(const part of parts){if(Buffer.byteLength(JSON.stringify(part))>4_400_000)throw Error('Revision part too large '+part.category);writeFileSync('cloud/revisions-'+part.category+'.json',JSON.stringify(part));}
 const checked=new Set([1,2,3].flatMap(i=>JSON.parse(readFileSync(`data/translation-review/reviewed-audit-${i}.json`)).checked));
 if(bank.exercises.some(e=>e.paragraphs.every(p=>p.translationReviewed!==false)&&!checked.has(e.id)))throw Error('An existing translation has not been reviewed');
 const audit={exercises:bank.exercises.length,paragraphs:allParagraphs.length,oldMachineParagraphs:baseline,retranslatedOrRevisedParagraphs:reviewed,sourceRepairedParagraphs:corrected,questionTranslations:translatedQuestions,reanchoredEvidence:reanchored,dictionaryEntriesRepaired:dictionaryFixes.length,otherArticlesReviewed:bank.exercises.filter(e=>e.paragraphs.every(p=>p.translationReviewed!==false)).length,additionalReviewChecks:checked.size,version:payload.version,sourceIssues:[...revised.values()].flatMap(e=>e.paragraphs.filter(p=>p.sourceIssue).map(p=>({id:e.id,pid:p.id,note:p.sourceIssue})))};
 writeFileSync('data/translation-review/audit.json',JSON.stringify(audit,null,2)+'\n');return {payload,parts,audit,bank:{...bank,lexicon,exercises:[...revised.values()]}};
}
