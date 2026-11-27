export function mergeLexiconParts(bank,parts){
 const lexicon={...(bank.lexicon||{})};
 for(const part of parts)for(const [key,value]of Object.entries(part)){
  if(Array.isArray(value))lexicon[key]=[...(lexicon[key]||[]),...value];
  else lexicon[key]={...(lexicon[key]||{}),...value};
 }
 const result={...bank,lexicon};delete result.lexiconFiles;return result;
}
export async function loadBank(entitled=false,fetcher=fetch){
 const response=await fetcher(entitled?'/content.json':'/api/catalog');if(!response.ok)throw Error(response.status);const bank=await response.json();
 const parts=await Promise.all((bank.lexiconFiles||[]).map(async path=>{if(!/^\/dictionary\/part-\d+\.json$/.test(path))throw Error('Invalid dictionary asset');const r=await fetcher(path);if(!r.ok)throw Error(r.status);return r.json();}));
 const merged=mergeLexiconParts(bank,parts);
 if(!entitled)return merged;
 const revisions=await fetcher('/api/content-revisions');if(!revisions.ok)throw Error('Content revisions '+revisions.status);
 const manifest=await revisions.json();
 const updates=await Promise.all(manifest.categories.map(async category=>{if(!['long','short','reading1','reading2','writing','speaking'].includes(category))throw Error('Invalid revision category');const r=await fetcher('/api/content-revisions?category='+category);if(!r.ok)throw Error('Content revisions '+r.status);const part=await r.json();if(part.version!==manifest.version)throw Error('Content version changed; reload to continue');return part;}));
 const byId=new Map(updates.flatMap(p=>p.exercises).map(e=>[e.id,e])),translations=Object.assign({},...updates.map(p=>p.translations));
 const lexicon={...merged.lexicon,translations,entries:{...merged.lexicon.entries},bookEntries:{...merged.lexicon.bookEntries}};
 for(const fix of updates.flatMap(p=>p.dictionaryFixes||[]))if(['entries','bookEntries'].includes(fix.section))lexicon[fix.section][fix.key]=fix.entry;
 return {...merged,contentRevision:manifest.version,lexicon,exercises:merged.exercises.map(e=>({...e,...byId.get(e.id)}))};
}

