import React,{useRef,useState,useEffect} from 'react';
import DOMPurify from 'dompurify';
import {AnnotatedText,useAnnotationTools} from './annotations.jsx';
import {wordCount,downloadText} from './lib.js';
export function cleanModelHTML(html){
 const safe=DOMPurify.sanitize(html,{ALLOWED_TAGS:['p','div','br','strong','b','em','i','u','mark','span','ul','ol','li'],ALLOWED_ATTR:['style']});
 const d=new DOMParser().parseFromString(safe,'text/html');
 for(const el of d.body.querySelectorAll('[style]')){const bg=el.style.backgroundColor,weight=el.style.fontWeight,dec=el.style.textDecoration;el.removeAttribute('style');if(bg&&/^(?:rgb\([\d, ]+\)|#[a-f\d]{3,8}|yellow|transparent)$/i.test(bg))el.style.backgroundColor=bg;if(weight==='bold'||weight==='700')el.style.fontWeight='bold';if(dec.includes('underline'))el.style.textDecoration='underline';}
 return d.body.innerHTML;
}
const escape=s=>s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
const originalHTML=model=>model.paragraphs.map(p=>'<p>'+(/^(?:Introduction|Problématique et plan|[IVX]+\.|Conclusion|[1-6]\.)/.test(p)?'<strong>'+escape(p)+'</strong>':escape(p))+'</p>').join('');
function ModelEditor({model,exercise,state,update}){
 const tools=useAnnotationTools(),key=exercise.id+':'+model.id,ref=useRef(null),[editing,setEditing]=useState(false),[reset,setReset]=useState(false),[count,setCount]=useState(0);
 const saved=state.modelEdits?.[key],source=originalHTML(model);
 useEffect(()=>{if(ref.current){ref.current.innerHTML=cleanModelHTML(saved??source);setCount(wordCount(ref.current.innerText));}},[key,editing]);
 const persist=()=>{if(!ref.current)return;const html=cleanModelHTML(ref.current.innerHTML);setCount(wordCount(ref.current.innerText));update(s=>({...s,modelEdits:{...s.modelEdits,[key]:html}}));};
 const format=(cmd,value)=>{ref.current?.focus();document.execCommand(cmd,false,value);persist();};
 return <article className="model-article"><div className="model-article-heading"><h3>{model.title}</h3><span>{count} mots</span></div>{model.structure&&<p className="model-structure">{model.structure}</p>}{model.context&&<p className="model-context">{model.context}</p>}
 <div className="model-actions"><button className="secondary-btn" onClick={()=>{if(editing)persist();setEditing(!editing);}}>{editing?'完成编辑':'编辑范文'}</button><button className="text-btn" onMouseDown={e=>e.preventDefault()} onClick={()=>{const s=getSelection();if(s&&!s.isCollapsed&&ref.current?.contains(s.anchorNode)&&ref.current?.contains(s.focusNode))tools?.openDictionary(s.toString(),'model:'+model.id);}}>查询所选词句</button><button className="text-btn" onClick={()=>downloadText(ref.current?.innerText||model.paragraphs.join('\n\n'),exercise.id+'-'+model.id+'.txt')}>导出文字</button>{saved!==undefined&&<button className="text-btn" onClick={()=>setReset(true)}>恢复原范文</button>}</div>
 {reset&&<div className="confirm-box"><p>恢复会清除这篇范文的个人修改。</p><button className="secondary-btn" onClick={()=>setReset(false)}>取消</button><button className="danger-btn" onClick={()=>{update(s=>{const next={...s.modelEdits};delete next[key];return {...s,modelEdits:next};});if(ref.current)ref.current.innerHTML=source;setCount(wordCount(model.paragraphs.join(' ')));setReset(false);}}>确认恢复</button></div>}
 {editing&&<div className="model-format-toolbar" role="toolbar" aria-label="范文格式"><button aria-label="加粗" onMouseDown={e=>e.preventDefault()} onClick={()=>format('bold')}><b>B</b></button><button aria-label="下划线" onMouseDown={e=>e.preventDefault()} onClick={()=>format('underline')}><u>U</u></button><button aria-label="范文高亮" onMouseDown={e=>e.preventDefault()} onClick={()=>format('hiliteColor','#fff0a8')}>高亮</button><button aria-label="删除范文高亮" onMouseDown={e=>e.preventDefault()} onClick={()=>format('hiliteColor','transparent')}>删除高亮</button><button onMouseDown={e=>e.preventDefault()} onClick={()=>format('removeFormat')}>清除格式</button><button aria-label="撤销编辑" onMouseDown={e=>e.preventDefault()} onClick={()=>format('undo')}>撤销</button><button onMouseDown={e=>e.preventDefault()} onClick={()=>format('redo')}>重做</button></div>}
 <div ref={ref} className={'model-text '+(editing?'is-editing':'')} contentEditable={editing} suppressContentEditableWarning role={editing?'textbox':undefined} aria-label={model.title+'内容'} aria-multiline={editing?true:undefined} lang="fr" onPaste={event=>{if(!editing)return;event.preventDefault();const rich=event.clipboardData.getData('text/html'),plain=event.clipboardData.getData('text/plain');ref.current?.focus();document.execCommand(rich?'insertHTML':'insertText',false,rich?cleanModelHTML(rich):plain);persist();}} onInput={persist} onBlur={persist}/><p className="model-save-status">{editing?'增删和格式修改自动保存到当前浏览器，可随学习备份导出。':'点击“编辑范文”可增删文字、加粗、加下划线或高亮。'}</p></article>;
}
export function StudyReference({exercise,state,update}){
 const models=exercise.studyModels||[];
 return <div className="study-reference"><p className="reference-intro">{exercise.category==='writing'?'按附件的综合与议论模板编排；写作训练目标约20/25。':'按附件的陈述与辩论模板编排；口语训练目标约14/25。'} 分数取决于现场完成情况。固定句式可复用，具体论据须随题目调整。</p>{models.map(model=><ModelEditor key={model.id} model={model} exercise={exercise} state={state} update={update}/>)}{!models.length&&<p>本题范文尚未收录。</p>}</div>;
}
export function AnswerExplanations({exercise,jump}){
 return <div className="answer-explanations"><h3>参考答案释义</h3>{exercise.questions.map(q=>{const x=q.explanation;return <article className="answer-explanation" key={q.id}><h4>第 {q.number} 题</h4><AnnotatedText as="p" pid={'explanation:prompt:'+q.id} text={q.prompt} lang="fr"/><p><strong>参考答案：</strong>{x?.answer||q.answer?.reference||'原资料未提供可核实答案。'}</p>{x?.reason&&<p>{x.reason}</p>}{x?.evidence?.map((v,i)=><blockquote key={i}><AnnotatedText as="p" pid={'evidence:'+q.id+':'+i} text={v.quote} lang="fr"/>{v.zh&&<p>{v.zh}</p>}<button className="text-btn" onClick={()=>jump(v.pid)}>定位到原文</button></blockquote>)}{x?.limitation&&<p className="evidence-limit">{x.limitation}</p>}</article>;})}</div>;
}
