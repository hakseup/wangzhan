import React,{useEffect,useRef,useState} from 'react';
import {Search,BookOpen,LoaderCircle} from 'lucide-react';
import {definitionText,loadLexicon,lookup,lookupKey,nativeTranslation,onlineTranslation,POS,requestLookup,restoreLookupNames} from './lookup.js';

function Senses({results,onWord}){
 return results.map(r=><div className="lookup-entry" key={r.lemma}><h4><button onClick={()=>onWord(r.lemma)} lang="fr">{r.lemma}</button>{r.form&&<small>原形 / 对应词条</small>}</h4>{r.entries.map((e,i)=><p key={i}><b>{POS[e.pos]||e.pos+'.'}</b> {e.senses.join('；')}</p>)}</div>);
}
export function LookupLayer({Modal,state,update,exercise}){
 const [request,setRequest]=useState(null),[query,setQuery]=useState(''),[bank,setBank]=useState(null),[loadError,setLoadError]=useState(''),[floating,setFloating]=useState(null),[translation,setTranslation]=useState(''),[busy,setBusy]=useState(false),[error,setError]=useState(''),[note,setNote]=useState(''),[saved,setSaved]=useState(false);
 const controller=useRef(null),serial=useRef(0),cache=useRef({});
 const [onlineEntries,setOnlineEntries]=useState([]);
 useEffect(()=>{try{cache.current=JSON.parse(localStorage.getItem('noix-lookup-cache-v1')||'{}');}catch{}},[]);
 useEffect(()=>{
  const open=ev=>{const next=ev.detail;if(!next?.text?.trim())return;setRequest(next);setQuery(next.text);setFloating(null);setSaved(false);};
  const capture=ev=>{
   if(ev.target.closest?.('.reader-content,.annotation-toolbar,.modal,.lookup-floating,input,textarea'))return;
   const selection=window.getSelection();if(!selection?.rangeCount||selection.isCollapsed){setFloating(null);return;}
   const range=selection.getRangeAt(0),parent=range.commonAncestorContainer.nodeType===1?range.commonAncestorContainer:range.commonAncestorContainer.parentElement;
   if(!parent?.closest('main')||parent.closest('.modal'))return;
   const text=selection.toString().trim();if(!/[A-Za-zÀ-ÿ]/.test(text)||/[\u4e00-\u9fff]/.test(text)||text.length>5000)return;
   const r=range.getBoundingClientRect();setFloating({text,x:Math.max(12,Math.min(innerWidth-155,r.left)),y:Math.max(8,Math.min(innerHeight-55,r.top-45))});
  };
  document.addEventListener('noix-lookup',open);document.addEventListener('mouseup',capture);document.addEventListener('keyup',capture);
  return()=>{document.removeEventListener('noix-lookup',open);document.removeEventListener('mouseup',capture);document.removeEventListener('keyup',capture);};
 },[]);
 useEffect(()=>{setRequest(null);setFloating(null);},[exercise?.id]);
 useEffect(()=>{
  if(!request)return;let active=true;setLoadError('');loadLexicon().then(x=>active&&setBank(x)).catch(e=>active&&setLoadError(e.message));return()=>{active=false;};
 },[request]);
 const result=bank&&request?lookup(bank,request.text):null;
 useEffect(()=>{
  const id=++serial.current;controller.current?.abort();setBusy(false);setError('');setSaved(false);setOnlineEntries([]);
  const text=request?.text||'';const found=bank&&text?lookup(bank,text):null;
  const stored=cache.current[lookupKey(text)];const cached=found?.translation||(typeof stored==='string'?stored:stored?.translation)||'';setTranslation(cached);if(stored?.entries)setOnlineEntries(stored.entries);setNote(found?definitionText(found):'');
  if(!text||cached||!found)return;
  nativeTranslation(text).catch(()=>'').then(t=>{if(serial.current!==id)return;if(t)setTranslation(restoreLookupNames(bank,text,t));else if(!found.entryResults.length&&state.lookupOnline!==false)translate();});
  return()=>{controller.current?.abort();};
 },[request,bank,state.lookupOnline]);
 const search=text=>{setRequest({text,origin:lookupKey(text)===lookupKey(request?.text)?request?.origin:null});setQuery(text);};
 const translate=async()=>{
  if(!request)return;const id=serial.current;controller.current?.abort();const abort=new AbortController();controller.current=abort;setBusy(true);setError('');const timeout=setTimeout(()=>abort.abort(),15000);
  try{let supplement=[];const raw=await onlineTranslation(request.text,{signal:abort.signal,onDefinitions:entries=>{supplement=entries.map(e=>({...e,senses:e.senses.map(s=>restoreLookupNames(bank,request.text,s))}));if(serial.current===id)setOnlineEntries(supplement);}});if(serial.current!==id)return;const text=restoreLookupNames(bank,request.text,raw);setTranslation(text);cache.current={...cache.current,[lookupKey(request.text)]:{translation:text,entries:supplement}};try{localStorage.setItem('noix-lookup-cache-v1',JSON.stringify(Object.fromEntries(Object.entries(cache.current).slice(-100))));}catch{}}
  catch(e){if(serial.current===id)setError(e.name==='AbortError'?'查询超时，请检查网络后重试。':e.name==='TypeError'?'联网查询失败，请检查网络后重试；本地词库仍可使用。':e.message);}
  finally{clearTimeout(timeout);if(serial.current===id)setBusy(false);}
 };
 const saveNote=()=>{
  const origin=request?.origin;if(!origin?.spans?.length||!note.trim())return;
  update(s=>{let marks=[...(s.annotations[origin.exerciseId]||[])];for(const span of origin.spans){const found=marks.find(a=>a.pid===span.pid&&a.start===span.start&&a.end===span.end);if(found)marks=marks.map(a=>a.id===found.id?{...a,note:note.trim()}:a);else marks.push({...span,id:crypto.randomUUID(),level:0,note:note.trim()});}return {...s,annotations:{...s.annotations,[origin.exerciseId]:marks}};});setSaved(true);
 };
 return <>{floating&&<button className="lookup-floating" style={{left:floating.x,top:floating.y}} onMouseDown={e=>e.preventDefault()} onClick={()=>requestLookup(floating.text)}><Search size={15}/> 查词 / 译句</button>}{request&&<Modal title="法语词句查询" close={()=>{controller.current?.abort();setRequest(null);}}><div className="lookup-panel"><form className="lookup-search" onSubmit={ev=>{ev.preventDefault();if(query.trim())search(query.trim());}}><input aria-label="查询法语单词、短语或句子" value={query} onChange={ev=>setQuery(ev.target.value)} maxLength={5000} autoFocus/><button className="secondary-btn" type="submit"><Search size={16}/> 查询</button></form>{loadError?<p role="alert">{loadError}<button className="text-btn" onClick={()=>setRequest({...request})}>重试加载词库</button></p>:!result?<p role="status"><LoaderCircle className="spin" size={15}/> 正在打开本地词库…</p>:<>
 <div className="lookup-kind">{result.kind==='word'?'单词释义':result.kind==='phrase'?'短语释义':'句子翻译'} · 法语 → 中文</div>
 {!!result.entryResults.length&&<Senses results={result.entryResults} onWord={search}/>}
 {!!onlineEntries.length&&<section><h4>联网补充的词性释义</h4><Senses results={[{lemma:request.text,entries:onlineEntries}]} onWord={search}/></section>}
 {translation&&<div className="lookup-translation"><h4>{result.kind==='word'?'补充译义':'所选文字的中文翻译'}</h4><p>{translation}</p></div>}
 {!result.entryResults.length&&!translation&&<p className="lookup-missing">本地暂未收录这一完整表达。可先查看组成词与原文语境，或在此页联网翻译。</p>}
 {result.kind!=='word'&&<section><h4>组成短语 / 句子的词汇</h4><div className="lookup-components">{result.components.map((c,i)=><div key={i}><button lang="fr" onClick={()=>search(c.word)}>{c.word}</button><span>{c.results.length?c.results.flatMap(r=>r.entries.slice(0,2).map(e=>(POS[e.pos]||e.pos)+ ' '+e.senses[0])).join(' / '):'未收录，可单独查询'}</span></div>)}</div></section>}
 {!!result.collocations.length&&<section><h4>搭配与原文用法</h4>{result.collocations.map(c=><button className="lookup-chip" key={c} lang="fr" onClick={()=>search(c)}>{c}</button>)}</section>}
 {!!result.related.length&&<section><h4>相关名词、动词与其他词形</h4>{result.related.map(r=><div className="lookup-related" key={r.word}><button lang="fr" onClick={()=>search(r.word)}>{r.word}</button><span>{r.results[0].entries.map(e=>(POS[e.pos]||e.pos)+' '+e.senses[0]).join(' / ')}</span></div>)}</section>}
 {request.origin?.paragraphs?.length>0&&<details className="lookup-context"><summary>所在段落参考译文</summary>{request.origin.paragraphs.map(p=><p key={p.id}>{p.zh}</p>)}</details>}
 <div className="lookup-network"><label className="lookup-network-switch"><input type="checkbox" checked={state.lookupOnline!==false} onChange={ev=>update({lookupOnline:ev.target.checked})}/> 本地未收录时，自动联网补充</label><button className="secondary-btn" disabled={busy} onClick={translate}>{busy?<LoaderCircle className="spin" size={15}/>:<BookOpen size={15}/>} {busy?'正在翻译…':'联网翻译所选文字'}</button><p>联网补充仅向Google翻译发送当前查询文字，结果显示在本页，不跳转网页。关闭上方开关后，只在点击按钮时联网。</p>{error&&<p className="inline-error" role="alert">{error}</p>}</div>
 {request.origin?.spans?.length>0&&<section className="lookup-save"><h4>添加备注到个人单词本</h4><textarea aria-label="查词备注" rows={3} value={note} onChange={ev=>{setNote(ev.target.value);setSaved(false);}} placeholder="可修改释义、补充搭配；只有保存了备注才会收录。"/>{translation&&!note&&<button className="text-btn" onClick={()=>setNote(translation)}>将译文填入备注</button>}<button className="primary-btn" disabled={!note.trim()} onClick={saveNote}>{saved?'备注已保存':'保存备注'}</button></section>}
 <details className="lookup-credit"><summary>词库来源与使用许可</summary><p>{bank.credit}</p>{bank.attribution&&<><p>{bank.attribution.author}</p><p>{bank.attribution.changes}</p>{bank.attribution.urls.map(url=><p key={url}>{url}</p>)}<details><summary>CC BY-SA 4.0许可全文</summary><pre style={{whiteSpace:'pre-wrap',fontSize:10}}>{bank.attribution.licenseText}</pre></details></>}</details>
 </>}</div></Modal>}</>;
}
