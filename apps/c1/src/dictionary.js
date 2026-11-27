export const dictKey=s=>String(s||'').normalize('NFC').toLocaleLowerCase('fr').replace(/[’‘]/g,"'").replace(/^[\s«»"“”.,;:!?()\[\]]+|[\s«»"“”.,;:!?()\[\]]+$/g,'').replace(/\s+/g,' ').trim();
export const POS={n:'n.',v:'v.',adj:'adj.',adv:'adv.',pron:'pron.',prep:'prép.',conj:'conj.',det:'dét.',article:'art.',intj:'interj.',num:'num.',phrase:'loc.',prep_phrase:'loc. prép.',proverb:'prov.',name:'n. propre',abbrev:'abr.',prefix:'préf.',suffix:'suff.',unknown:'词性待核'};
export function lookupWord(lexicon,query){
 if(!lexicon?.entries)return null;
 const key=dictKey(query),map=lexicon.entries;
 const candidates=[key,key.replace(/^(?:l|d|s|j|qu|n|c|m|t)'/,''),key.replace(/^(?:les|des|une?|du|la|le) /,'')];
 for(const k of [...candidates]){if(k.endsWith('aux'))candidates.push(k.slice(0,-3)+'al');if(/[sx]$/.test(k))candidates.push(k.slice(0,-1));}
 const roots=[...new Set(candidates.flatMap(k=>[lexicon.aliases?.[k],...(lexicon.formLemmas?.[k]||[]),k]).filter(k=>k&&map[k]))];
 if(!roots.length)return null;
 const lemma=roots[0],entry=map[lemma];
 const senses=roots.flatMap(fr=>(map[fr].senses?.length?map[fr].senses:[{pos:'unknown',zh:map[fr].zh}]).map(s=>({...s,lemma:fr}))).filter(s=>s.zh);
 return {...entry,fr:lemma,query:key,inflected:lemma!==key,senses:[...new Map(senses.map(s=>[s.pos+'|'+s.zh,s])).values()],alternatives:roots};
}
export function dictionaryPhrases(lexicon,entry){
 if(!entry)return [];
 const manual=entry.collocations||[],forms=[entry.fr,...(entry.forms||[])].map(dictKey);
 const related=(lexicon.phrases||[]).filter(p=>forms.some(f=>(' '+dictKey(p.fr)+' ').includes(' '+f+' '))&&dictKey(p.fr)!==entry.fr);
 return [...new Map([...manual,...related].map(p=>[p.fr,p])).values()].filter(p=>p.zh).slice(0,8);
}
export function queryParts(lexicon,query){
 const tokens=[...new Set((query.match(/[\p{L}]+(?:[’'\-][\p{L}]+)*/gu)||[]).map(dictKey))];
 return tokens.map(word=>({word,entry:lookupWord(lexicon,word)}));
}
export function restoreQueryNames(query,text,pairs=[]){
 const source=dictKey(query);let result=text;
 for(const [fr,zh]of pairs)if(new RegExp('(^|[^\\p{L}])'+dictKey(fr).replace(/[.*+?^${}()|[\]\\]/g,'\\$&')+'(?=[^\\p{L}]|$)','u').test(source)&&zh&&zh!==fr)result=result.split(zh).join(fr);
 return result;
}
export function localTranslation(lexicon,query){
 const q=dictKey(query);return lexicon.translations?.[q]||lexicon.translations?.[q.replace(/œ/g,'oe')]||null;
}
const cacheKey='noix-dalf-lookup-v2';
export function readLookupCache(query){try{return JSON.parse(localStorage.getItem(cacheKey)||'{}')[dictKey(query)]||null;}catch{return null;}}
function cacheTranslation(query,text){try{const pairs=Object.entries(JSON.parse(localStorage.getItem(cacheKey)||'{}')).filter(([k])=>k!==dictKey(query)).slice(-149);localStorage.setItem(cacheKey,JSON.stringify(Object.fromEntries([...pairs,[dictKey(query),text]])));}catch{}}
let translator=null;
export async function enableLocalTranslation({onProgress}={}){
 if(!globalThis.Translator)throw Error('当前浏览器不支持本机翻译。站内词库、词形与已有参考译文仍可查询；可在支持 Translator 的新版 Chrome 中启用本地词句翻译。');
 const pair={sourceLanguage:'fr',targetLanguage:'zh'};
 const status=await globalThis.Translator.availability(pair);
 if(status==='unavailable')throw Error('当前设备暂不支持法语到中文的本地语言包；站内词库仍可使用。');
 if(!translator)translator=await globalThis.Translator.create({...pair,monitor(m){m.addEventListener('downloadprogress',e=>onProgress?.(e.loaded));}});
 return translator;
}
export async function translateSelection(query,{signal,lexicon,allowOnline=false}={}){
 const cached=localTranslation(lexicon||{},query)||readLookupCache(query);if(cached)return {text:cached,source:'站内参考译文 / 查询缓存'};
 if(query.length>5000)throw Error('请选择较短的词句，分段查询。');
 let localError='';
 try{
  if(!translator&&globalThis.Translator&&await globalThis.Translator.availability({sourceLanguage:'fr',targetLanguage:'zh'})==='available')await enableLocalTranslation();
  if(translator){const text=restoreQueryNames(query,await translator.translate(query,{signal}),lexicon?.namePairs);if(text?.trim()){cacheTranslation(query,text);return {text,source:'浏览器本地翻译 · 查询文字不上传'};}}
 }catch(e){if(signal?.aborted)throw e;localError=e.message;}
 if(!allowOnline)throw Error(localError||'此词句尚未收录。可启用浏览器本地翻译，或勾选联网补充，只发送当前查询文字。');
 const chunks=[];let buffer='';for(const word of query.split(/\s+/)){if((buffer+' '+word).length>300&&buffer){chunks.push(buffer);buffer='';}buffer+=(buffer?' ':'')+word;}if(buffer)chunks.push(buffer);
 const results=[];
 for(const chunk of chunks){
  const url=new URL('https://api.mymemory.translated.net/get');url.searchParams.set('q',chunk);url.searchParams.set('langpair','fr|zh-CN');
  const response=await fetch(url,{signal,credentials:'omit',referrerPolicy:'no-referrer'});if(!response.ok)throw Error('在线补充暂时不可用，请稍后重试。');
  const data=await response.json();if(Number(data.responseStatus)!==200||!data.responseData?.translatedText)throw Error(Number(data.responseStatus)===429||String(data.responseDetails||'').includes('LIMIT')?'在线服务额度暂时用完，站内词库仍可使用。':'尚未取得补充译文，请稍后重试。');
  const text=data.responseData.translatedText;if(/MYMEMORY WARNING|QUERY LENGTH LIMIT|INVALID LANGUAGE/i.test(text))throw Error('在线补充暂时受限，站内词库仍可使用。');results.push(text);
 }
 const text=restoreQueryNames(query,results.join(''),lexicon?.namePairs);cacheTranslation(query,text);return {text,source:'在线补充参考译文 · MyMemory'};
}
