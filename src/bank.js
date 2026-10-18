export function mergeLexiconParts(bank,parts){
 const lexicon={...(bank.lexicon||{})};
 for(const part of parts)for(const [key,value]of Object.entries(part)){
  if(Array.isArray(value))lexicon[key]=[...(lexicon[key]||[]),...value];
  else lexicon[key]={...(lexicon[key]||{}),...value};
 }
 const result={...bank,lexicon};delete result.lexiconFiles;return result;
}
export async function loadBank(fetcher=fetch){
 const response=await fetcher('/content.json');if(!response.ok)throw Error(response.status);const bank=await response.json();
 const parts=await Promise.all((bank.lexiconFiles||[]).map(async path=>{if(!/^\/dictionary\/part-\d+\.json$/.test(path))throw Error('Invalid dictionary asset');const r=await fetcher(path);if(!r.ok)throw Error(r.status);return r.json();}));
 return mergeLexiconParts(bank,parts);
}
