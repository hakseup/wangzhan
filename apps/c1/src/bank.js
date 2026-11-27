export function mergeLexiconParts(bank,parts){
 const lexicon={...(bank.lexicon||{})};
 for(const part of parts)for(const [key,value]of Object.entries(part)){
  if(Array.isArray(value))lexicon[key]=[...(lexicon[key]||[]),...value];
  else lexicon[key]={...(lexicon[key]||{}),...value};
 }
 const result={...bank,lexicon};delete result.lexiconFiles;return result;
}
// 合并站点中 C1 题库位于 /c1/ 下；content.json 内的绝对路径保持原样，在此统一加前缀。
const BASE=(typeof import.meta!=='undefined'&&import.meta.env?.BASE_URL)||'/';
export const withBase=path=>typeof path==='string'&&path.startsWith('/')&&!path.startsWith(BASE)?BASE+path.slice(1):path;
export async function loadBank(fetcher=fetch){
 const response=await fetcher(withBase('/content.json'),{cache:'no-cache'});if(!response.ok)throw Error(response.status);const bank=await response.json();
 const parts=await Promise.all((bank.lexiconFiles||[]).map(async path=>{if(!/^\/dictionary\/part-\d+\.json$/.test(path))throw Error('Invalid dictionary asset');const r=await fetcher(withBase(path));if(!r.ok)throw Error(r.status);return r.json();}));
 const merged=mergeLexiconParts(bank,parts);
 merged.exercises=(merged.exercises||[]).map(e=>e.audio?{...e,audio:withBase(e.audio)}:e);
 return merged;
}
