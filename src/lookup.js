export const lookupKey=text=>String(text||'').normalize('NFC').replace(/[’ʼ]/g,"'").replace(/\s+/g,' ').trim().toLocaleLowerCase('fr');
export const tokens=text=>String(text).match(/[\p{L}]+(?:[-'][\p{L}]+)*/gu)||[];
export const POS={n:'n. 名词',v:'v. 动词',adj:'adj. 形容词',adv:'adv. 副词',prep:'prép. 介词',pron:'pron. 代词',conj:'conj. 连词',det:'dét. 限定词',article:'art. 冠词',num:'num. 数词',intj:'interj. 感叹词',name:'n.pr. 专有名词',phrase:'loc. 短语',prep_phrase:'loc.prép. 介词短语',proverb:'loc. 谚语',prefix:'préf. 前缀',suffix:'suff. 后缀',abbrev:'abrév. 缩写',contraction:'contr. 缩合形式',unknown:'词条'};
let loading;
export function loadLexicon(){
 if(!loading)loading=(async()=>{
  const embedded=document.getElementById('noix-lexicon');
  if(embedded)return JSON.parse(embedded.textContent);
  const r=await fetch('./lexicon.json');if(!r.ok)throw Error('本地词库未能加载，请重新打开文件或检查网站资源。');return r.json();
 })().catch(e=>{loading=null;throw e;});
 return loading;
}
function stripElision(word){return word.replace(/^(?:[ldjtmcsn]|qu|jusqu|lorsqu|puisqu)'/,'');}
const grammatical=new Set(['de','à','en','le','la','les','un','une','du','des','au','aux','que','qui','si','ne','se','ce','je','tu','il','elle','on','nous','vous','ils','elles','me','te','et','ou','où','mais','donc','pour','avec','sans','sur','sous','dans','chez','entre','vers','parmi','depuis','pendant','selon']);
export function wordEntries(bank,text){
 const word=lookupKey(text).replace(/^[^\p{L}]+|[^\p{L}']+$/gu,'');
 const roots=[],seen=new Set();
 const visit=(s,depth=0)=>{
  if(seen.has(s)||depth>3)return;seen.add(s);
  if(Array.isArray(bank.entries[s])&&bank.entries[s].length)roots.push(s);
  if(grammatical.has(s)&&roots.includes(s))return;
  if(s===word&&/^\p{Lu}/u.test(text)&&bank.entries[s]?.every?.(e=>e.pos==='name'))return;
  for(const base of Array.isArray(bank.forms[s])?bank.forms[s]:[])visit(base,depth+1);
 };
 visit(word);if(!roots.length&&stripElision(word)!==word)visit(stripElision(word));
 // Accentless typing is accepted only when it has one unambiguous dictionary match.
 if(!roots.length){
  const fold=s=>s.normalize('NFD').replace(/[\u0300-\u036f]/g,'');
  bank._folded??=Object.keys(bank.entries).reduce((a,k)=>{const f=fold(k);if(f!==k)(a[f]??=[]).push(k);return a;},Object.create(null));
  const matches=bank._folded[fold(word)]||[];if(matches.length===1)visit(matches[0]);
 }
 return roots.map(lemma=>({lemma,entries:bank.entries[lemma],form:lemma!==word}));
}
function componentWords(text){
 return tokens(text.replace(/[’ʼ]/g,"'")).flatMap(t=>t.includes("'")?t.split("'").map((v,i)=>i===0&&v.length<=2?v+"'":v):[t]);
}
export function lookup(bank,text){
 const query=lookupKey(text),parts=componentWords(text),single=tokens(text).length===1&&!/\s/.test(query);
 const exact=wordEntries(bank,query);
 const components=parts.map(word=>({word,results:wordEntries(bank,word)}));
 const normalized=components.map(c=>c.results.find(r=>r.entries.some(e=>e.pos==='v'))?.lemma||c.results[0]?.lemma||lookupKey(c.word)).join(' ');
 let phrase=exact;
 if(!single&&!phrase.length){
  if(!bank._phrases){
   bank._phrases={next:new Map()};
   for(const head of Object.keys(bank.entries)){
    const ws=componentWords(head);if(ws.length<2||ws.length>12)continue;
    let node=bank._phrases;for(const word of ws){const k=lookupKey(word);if(!node.next.has(k))node.next.set(k,{next:new Map()});node=node.next.get(k);}node.head=head;
   }
  }
  const candidates=components.map(c=>[...new Set([lookupKey(c.word),...c.results.map(r=>r.lemma)])].slice(0,10));
  const found=new Set();
  for(let start=0;start<Math.min(4,parts.length-1);start++){
   if(start&&!candidates[start-1].some(w=>['je','tu','il','elle','on','nous','vous','ils','elles','avoir','être','ne'].includes(w)))break;
   let nodes=[bank._phrases];
   for(const words of candidates.slice(start))nodes=nodes.flatMap(n=>words.map(w=>n.next.get(w)).filter(Boolean));
   for(const node of nodes)if(node.head)found.add(node.head);
  }
  phrase=[...found].flatMap(w=>wordEntries(bank,w));
 }
 const entryResults=single?exact:phrase;
 const lemmas=[...new Set(entryResults.map(r=>r.lemma))];
 const related=[...new Set(lemmas.flatMap(w=>bank.related[w]||[]))].filter(w=>!lemmas.includes(w)).map(w=>({word:w,results:wordEntries(bank,w)})).filter(r=>r.results.length).slice(0,12);
 const collocations=[...new Set(lemmas.flatMap(w=>bank.collocations[w]||[]))].slice(0,8);
 const cached=bank.translations[query]||bank.translations[query.replace(/[.!?…»”"]+$/,'').replace(/^[«“"]+/,'').trim()];
 return {kind:single?'word':parts.length>8||/[.!?]/.test(text)?'sentence':'phrase',entryResults,components,related,collocations,translation:typeof cached==='string'?cached:'',normalized};
}
export function definitionText(result){
 return result.entryResults.map(r=>r.lemma+' — '+r.entries.map(e=>(POS[e.pos]||e.pos+'.')+' '+e.senses.slice(0,3).join('；')).join(' / ')).join('\n')||result.translation||'';
}
export function restoreLookupNames(bank,source,translated){
 const folded=source.toLocaleLowerCase('fr');
 for(const [name,variant]of bank.names||[]){if(folded.includes(name.toLocaleLowerCase('fr'))&&new RegExp('(?<![\\p{L}\\p{N}_])'+name.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')+'(?![\\p{L}\\p{N}_])','iu').test(source))translated=translated.replaceAll(variant,name);}
 return translated;
}
export async function nativeTranslation(text){
 const T=globalThis.Translator;if(!T)return '';
 const availability=await T.availability({sourceLanguage:'fr',targetLanguage:'zh'});
 if(availability!=='available')return '';
 const translator=await T.create({sourceLanguage:'fr',targetLanguage:'zh'});
 try{return await translator.translate(text);}finally{translator.destroy();}
}
// Explicitly invoked from the in-page button; no new tabs, redirects or credentials.
export async function onlineTranslation(text,{signal,onDefinitions}={}){
 const url=new URL('https://translate.googleapis.com/translate_a/single');
 for(const [k,v]of Object.entries({client:'gtx',sl:'fr',tl:'zh-CN',hl:'en',dt:'t',q:text}))url.searchParams.set(k,v);
 url.searchParams.append('dt','bd');
 const response=await fetch(url,{signal,credentials:'omit',referrerPolicy:'no-referrer'});
 if(!response.ok)throw Error('联网翻译暂时不可用。你仍可查看本地释义与组成词，稍后重试。');
 const data=await response.json();const translated=(data[0]||[]).map(row=>row[0]||'').join('');
 const pos={noun:'n',verb:'v',adjective:'adj',adverb:'adv',preposition:'prep',pronoun:'pron',conjunction:'conj',interjection:'intj',article:'article',abbreviation:'abbrev'};
 const entries=(Array.isArray(data[1])?data[1]:[]).filter(row=>pos[row[0]]&&Array.isArray(row[1])).map(row=>({pos:pos[row[0]],senses:row[1].filter(s=>typeof s==='string'),source:'online'})).filter(e=>e.senses.length);
 if(entries.length)onDefinitions?.(entries);
 if(!translated.trim())throw Error('翻译服务暂未返回结果，请稍后重试。');return translated;
}
export function requestLookup(text,origin=null){document.dispatchEvent(new CustomEvent('noix-lookup',{detail:{text,origin}}));}
