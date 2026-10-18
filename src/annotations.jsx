import React,{createContext,useContext,useState,useRef,useEffect,useLayoutEffect} from 'react';
import {Highlighter,MessageSquarePlus,BookOpen,Trash2,X,Check} from 'lucide-react';
import {annotationParts} from './lib.js';
import {visibleMarks,rebaseMarks,removeHighlight} from './annotation-utils.js';
import {DictionaryPanel} from './dictionary.jsx';
const Context=createContext(null);
export function AnnotationProvider({annotations,onChange,lexicon,exercise,Modal,children}){
 const root=useRef(null),[selection,setSelection]=useState(null),[dialog,setDialog]=useState(''),[note,setNote]=useState('');
 const place=(rect,spans,input=null)=>setSelection({spans,input,x:Math.max(8,Math.min(innerWidth-355,rect.left)),y:Math.max(8,Math.min(innerHeight-65,rect.top-49))});
 const capture=()=>{
  const sel=getSelection();if(!sel||sel.isCollapsed||!sel.rangeCount)return;
  const range=sel.getRangeAt(0);if(!root.current?.contains(range.commonAncestorContainer))return;
  const spans=[];
  for(const el of root.current.querySelectorAll('[data-annotation]')){
   if(el.closest('.answer-highlight-layer')||!range.intersectsNode(el))continue;
   const text=el.dataset.annotationText||'';let start=0,end=text.length;
   if(el.contains(range.startContainer)){const r=document.createRange();r.selectNodeContents(el);r.setEnd(range.startContainer,range.startOffset);start=r.toString().length;}
   if(el.contains(range.endContainer)){const r=document.createRange();r.selectNodeContents(el);r.setEnd(range.endContainer,range.endOffset);end=r.toString().length;}
   if(end>start&&text.slice(start,end).trim())spans.push({pid:el.dataset.annotation,start,end,text:text.slice(start,end)});
  }
  if(spans.length)place(range.getBoundingClientRect(),spans);
 };
 useEffect(()=>{document.addEventListener('mouseup',capture);document.addEventListener('keyup',capture);return()=>{document.removeEventListener('mouseup',capture);document.removeEventListener('keyup',capture);};},[annotations]);
 useEffect(()=>{const outside=e=>{if(!e.target.closest('.annotation-toolbar,.modal,[data-annotation],[data-annotation-input]'))setSelection(null);};document.addEventListener('mousedown',outside);return()=>document.removeEventListener('mousedown',outside);},[]);
 const clear=()=>{getSelection()?.removeAllRanges();if(selection?.input){const el=selection.input;el.setSelectionRange(el.selectionEnd,el.selectionEnd);}setSelection(null);};
 const alter=(kind,value)=>{
  if(!selection)return;
  if(kind==='unhighlight'){onChange(old=>removeHighlight(old,selection.spans));clear();return;}
  onChange(old=>{let next=[...old];for(const span of selection.spans){const found=next.find(a=>!a.detached&&a.pid===span.pid&&a.start===span.start&&a.end===span.end);if(kind==='remove'){next=next.filter(a=>a.id!==found?.id);continue;}
   if(found){let a={...found};if(kind==='note')a.note=value;else a.level=(a.level+1)%4;next=next.filter(x=>x.id!==found.id);if(a.level||a.note)next.push(a);}else next.push({...span,id:crypto.randomUUID(),level:kind==='note'?0:1,note:kind==='note'?value:''});}
   return next;});clear();
 };
 const hasSelectedHighlight=selection&&annotations.some(a=>a.level&&!a.detached&&selection.spans.some(s=>s.pid===a.pid&&s.start<a.end&&s.end>a.start));
 const selectedMark=selection&&annotations.find(a=>a.pid===selection.spans[0]?.pid&&a.start===selection.spans[0]?.start&&a.end===selection.spans[0]?.end&&!a.detached);
 const clickMark=(event,a)=>{if(!getSelection()?.isCollapsed)return;event.preventDefault();event.stopPropagation();place(event.currentTarget.getBoundingClientRect(),[{pid:a.pid,start:a.start,end:a.end,text:a.text}]);};
 const selectInput=el=>{if(el.selectionEnd>el.selectionStart){const start=el.selectionStart,end=el.selectionEnd;place(el.getBoundingClientRect(),[{pid:el.dataset.annotationInput,start,end,text:el.value.slice(start,end)}],el);}};
 const openDictionary=(text,pid='model-query')=>{setSelection({spans:[{pid,start:0,end:text.length,text}],model:true,x:8,y:8});setDialog('dictionary');};
 const edit=(pid,before,after)=>onChange(old=>rebaseMarks(old,pid,before,after));
 return <Context.Provider value={{annotations,clickMark,selectInput,edit,openDictionary}}><div ref={root} className="annotation-scope" style={{display:'contents'}}>{children}</div>
 {selection&&!dialog&&!selection.model&&<div className="annotation-toolbar" style={{left:selection.x,top:selection.y}} onMouseDown={e=>e.preventDefault()}><button onClick={()=>alter('highlight')}><Highlighter size={15}/>{selectedMark?'切换颜色':'高亮'}<span className="highlight-dots"><i/><i/><i/></span></button><button onClick={()=>{setNote(selectedMark?.note||'');setDialog('note');}}><MessageSquarePlus size={15}/>备注</button><button aria-label="查询中文释义与搭配" onClick={()=>setDialog('dictionary')}><BookOpen size={15}/>查词</button>{hasSelectedHighlight&&<button onClick={()=>alter('unhighlight')}>删除高亮</button>}{selectedMark&&<button aria-label="删除这个标注" onClick={()=>alter('remove')}><Trash2 size={14}/></button>}<button aria-label="关闭标注工具" onClick={clear}><X size={14}/></button></div>}
 {dialog==='note'&&selection&&<Modal title="给这个词句留一条笔记" close={()=>setDialog('')}><blockquote lang="fr">{selection.spans.map(s=>s.text).join(' ')}</blockquote><label>释义、搭配或你想记住的内容<textarea autoFocus rows={4} value={note} onChange={e=>setNote(e.target.value)}/></label><div className="modal-actions"><button className="secondary-btn" onClick={()=>setDialog('')}>取消</button><button className="primary-btn" disabled={!note.trim()} onClick={()=>{alter('note',note.trim());setDialog('');}}>保存备注 <Check size={15}/></button></div></Modal>}
 {dialog==='dictionary'&&selection&&<Modal title="词义与搭配" close={()=>setDialog('')}><DictionaryPanel lexicon={lexicon} exercise={exercise} initial={selection.spans.map(s=>s.text).join(' ')} save={value=>{setNote(value);setDialog('note');}}/></Modal>}
 </Context.Provider>;
}
export function AnnotatedText({pid,text='',as:Tag='span',className='',...props}){
 const ctx=useContext(Context);if(!ctx)return <Tag className={className} {...props}>{text}</Tag>;
 const marks=visibleMarks(ctx.annotations,pid,text);
 return <Tag data-annotation={pid} data-annotation-text={text} className={className} {...props}>{annotationParts(text,marks).map(part=>part.annotation?<mark key={part.start} role="button" tabIndex={0} className={'text-mark level-'+part.level+(part.notes.length?' word-note':'')} title={part.notes.map(n=>n.note).join('\n')||'高亮、备注或查词'} aria-label={part.notes.length?'词汇备注：'+part.notes.map(n=>n.note).join('；'):'切换高亮颜色'} onClick={e=>ctx.clickMark(e,part.annotation)} onKeyDown={e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();ctx.clickMark(e,part.annotation);}}}>{part.text}</mark>:<React.Fragment key={part.start}>{part.text}</React.Fragment>)}</Tag>;
}
export function AnnotatedInput({pid,value='',onChange,className='',...props}){
 const ctx=useContext(Context),mirror=useRef(null),input=useRef(null);
 useLayoutEffect(()=>{const el=input.current,layer=mirror.current;if(!el||!layer)return;const sync=()=>{const c=getComputedStyle(el);for(const prop of ['fontFamily','fontSize','fontWeight','fontStyle','letterSpacing','lineHeight','paddingTop','paddingRight','paddingBottom','paddingLeft','borderTopWidth','borderRightWidth','borderBottomWidth','borderLeftWidth','textAlign','tabSize'])layer.style[prop]=c[prop];Object.assign(layer.style,{top:el.offsetTop+'px',left:el.offsetLeft+'px',width:el.offsetWidth+'px',height:el.offsetHeight+'px'});};sync();const observer=new ResizeObserver(sync);observer.observe(el);return()=>observer.disconnect();},[value,className]);
 return <div className={'annotated-input-wrap field-'+className}><div ref={mirror} className="answer-highlight-layer" aria-hidden="true"><AnnotatedText as="div" pid={pid} text={value+'\n'} className="answer-highlight-text"/></div><textarea {...props} ref={input} className={className} data-annotation-input={pid} value={value} onChange={e=>{ctx?.edit(pid,value,e.target.value);onChange?.(e);}} onSelect={e=>ctx?.selectInput(e.currentTarget)} onKeyUp={e=>ctx?.selectInput(e.currentTarget)} onMouseUp={e=>ctx?.selectInput(e.currentTarget)} onScroll={e=>{if(mirror.current){mirror.current.scrollTop=e.currentTarget.scrollTop;mirror.current.scrollLeft=e.currentTarget.scrollLeft;}}}/></div>;
}

export const useAnnotationTools=()=>useContext(Context);
