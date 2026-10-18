export const dictKey=s=>String(s||'').normalize('NFC').toLocaleLowerCase('fr').replace(/[’‘]/g,"'").replace(/^[\s«»"“”.,;:!?()\[\]]+|[\s«»"“”.,;:!?()\[\]]+$/g,'').replace(/\s+/g,' ').trim();
export function lookupWord(lexicon,query){
 if(!lexicon?.entries)return null;
 const key=dictKey(query),map=lexicon.entries;
 const candidates=[key,key.replace(/^(?:l|d|s|j|qu|n|c|m|t)'/,''),key.replace(/^(?:les|des|une?|du|la|le) /,'')];
 for(const k of [...candidates]){if(k.endsWith('aux'))candidates.push(k.slice(0,-3)+'al');if(/[sx]$/.test(k))candidates.push(k.slice(0,-1));}
 for(const k of candidates){const lemma=lexicon.aliases?.[k]||k;if(map[lemma])return {...map[lemma],fr:lemma,query:key,inflected:lemma!==key};}
 return null;
}
export function dictionaryPhrases(lexicon,entry){
 if(!entry)return [];
 const manual=entry.collocations||[];
 const forms=[entry.fr,...(entry.forms||[])].map(dictKey);
 const related=(lexicon.phrases||[]).filter(p=>forms.some(f=>(' '+dictKey(p.fr)+' ').includes(' '+f+' '))&&dictKey(p.fr)!==entry.fr);
 return [...new Map([...manual,...related].map(p=>[p.fr,p])).values()].slice(0,6);
}
