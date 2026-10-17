import React,{useState,useMemo} from 'react';
import {Search,NotebookPen} from 'lucide-react';
import {lookupWord,dictionaryPhrases,dictKey} from './dictionary.js';
export function DictionaryPanel({lexicon,exercise,initial,save}){
 const [query,setQuery]=useState(initial),[term,setTerm]=useState(initial);
 const entry=useMemo(()=>lookupWord(lexicon,term),[lexicon,term]),phrases=useMemo(()=>dictionaryPhrases(lexicon,entry),[lexicon,entry]);
 const examples=useMemo(()=>{if(!entry)return [];const forms=[entry.fr,...(entry.forms||[])].map(dictKey);return exercise.paragraphs.filter(p=>forms.some(f=>(' '+dictKey(p.fr)+' ').includes(' '+f+' '))).slice(0,2);},[entry,exercise]);
 return <div className="dictionary-panel"><form className="dictionary-search" onSubmit={e=>{e.preventDefault();setTerm(query);}}><input autoFocus aria-label="查询法语词汇" value={query} onChange={e=>setQuery(e.target.value)} placeholder="输入法语单词或短语"/><button className="secondary-btn" type="submit"><Search size={15}/> 查询</button></form>
 {entry?<><h3 lang="fr">{entry.fr}</h3>{entry.inflected&&<p className="dictionary-inflection">所选词形：<span lang="fr">{term}</span> · 已对应到词条原形</p>}<h4>中文释义</h4><p className="dictionary-meaning">{entry.zh}</p>{phrases.length>0&&<><h4>常用搭配与短语</h4><ul className="dictionary-phrases">{phrases.map(p=><li key={p.fr}><strong lang="fr">{p.fr}</strong><span>{p.zh}</span></li>)}</ul></>}{examples.length>0&&<><h4>本题用法</h4>{examples.map(p=><div className="dictionary-example" key={p.id}><p lang="fr">{p.fr.length>450?p.fr.slice(0,450)+'…':p.fr}</p><p>{p.zh?.length>250?p.zh.slice(0,250)+'…':p.zh}</p></div>)}</>}{!phrases.length&&<p className="dictionary-empty">此词暂无已收录的固定搭配，可参考本题语境。</p>}<button className="primary-btn" onClick={()=>save(entry.zh+(phrases.length?'\n'+phrases.slice(0,3).map(p=>p.fr+' — '+p.zh).join('\n'):''))}><NotebookPen size={16}/> 将释义与搭配记入备注</button></>:<p className="dictionary-empty">暂未找到这个词条。可尝试单词原形或较短的短语；未收录的内容不会生成猜测释义。</p>}
 <p className="dictionary-credit">站内离线词库 · CFDICT（CC BY-SA 3.0）与本站整理</p></div>;
}
