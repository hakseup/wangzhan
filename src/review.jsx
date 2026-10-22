import React from 'react';
import {AnnotatedText} from './annotations.jsx';
import {CheckCircle2,XCircle,Clock3,LocateFixed,Minus,Plus} from 'lucide-react';
export function EvidenceReader({exercise,active,activate,fontSize,resizeFont}){
 const paragraphs=new Map(exercise.paragraphs.map(p=>[p.id,p]));
 return <div className="evidence-reader reader-content" style={{fontSize}}><div className="review-caption"><strong>答案句 · 对应译文</strong><span>悬停或聚焦句子，绿色下划线对应双语</span><div className="reader-size"><button aria-label="缩小正文" disabled={fontSize<=14} onClick={()=>resizeFont(Math.max(14,fontSize-1))}><Minus size={14}/></button><span>Aa</span><button aria-label="放大正文" disabled={fontSize>=26} onClick={()=>resizeFont(Math.min(26,fontSize+1))}><Plus size={14}/></button></div></div>{(exercise.reviewPassages||[]).map(pair=><article key={pair.id} className={'evidence-pair '+(active===pair.id?'is-linked':'')} data-evidence-id={pair.id} data-paragraph={pair.pid}>
 <div className="evidence-labels">{pair.questionIds.map(id=><span key={id}>Q{exercise.questions.find(q=>q.id===id)?.number}</span>)}<small>原文第 {pair.paragraphNumber} 段</small></div>
 <p className="evidence-fr" lang="fr" tabIndex={0} onMouseEnter={()=>activate(pair.id)} onMouseLeave={()=>activate(null)} onFocus={()=>activate(pair.id)} onBlur={()=>activate(null)}><AnnotatedText pid={pair.pid} offset={pair.start} sourceText={paragraphs.get(pair.pid)?.fr} text={pair.fr}/></p>
 <p className="evidence-zh" lang="zh-CN" tabIndex={0} onMouseEnter={()=>activate(pair.id)} onMouseLeave={()=>activate(null)} onFocus={()=>activate(pair.id)} onBlur={()=>activate(null)}><AnnotatedText pid={'reference:translation:'+pair.id} text={pair.zh}/></p>
 </article>)}{!exercise.reviewPassages?.length&&<p>本题缺少可核实的原文依据，请以原始资料为准。</p>}</div>;
}
function AnswerText({q,answer,expected=false}){
 const value=expected?(q.answer?.value||''):answer.value;
 const option=q.options?.find(o=>o.id===value);
 if(option)return <><span className="review-option-id">{value}. </span><AnnotatedText pid={'option:'+q.id+':'+value} text={option.text} lang="fr"/>{option.zh&&<small className="review-option-zh">{option.zh}</small>}</>;
 return <AnnotatedText pid={expected?'reference:'+q.id:'answer:'+q.id+':value'} text={expected?(q.explanation?.answer||q.answer?.reference||'原资料未提供可核实的标准答案。'):(value||'未作答')}/>;
}
export function ReviewQuestion({exercise,question:q,answer,result,locate,selfEvaluate}){
 const status=result?.status||'unanswered',x=q.explanation;
 return <article className={'question review-question '+status} id={'question-'+q.id}>
 <div className="question-meta"><span>{String(q.number).padStart(2,'0')}</span><small>答案核对</small><span className={'question-status '+status}>{status==='correct'?<CheckCircle2 size={15}/>:status==='incorrect'?<XCircle size={15}/>:<Clock3 size={14}/>}{{correct:'正确',incorrect:'错误',review:'待自评',unanswered:'未作答'}[status]}{result?.selfEvaluated?' · 自评':''}</span></div>
 <AnnotatedText as="h3" lang="fr" pid={'question:'+q.id} text={q.prompt}/>{q.zh&&<p className="review-question-zh">{q.zh}</p>}
 <div className="review-answer-comparison"><div><strong>你的答案</strong><p><AnswerText q={q} answer={answer}/></p>{answer.justification&&<p className="review-justification"><AnnotatedText pid={'answer:'+q.id+':justification'} text={answer.justification} lang="fr"/></p>}</div><div><strong>参考答案</strong><p><AnswerText q={q} answer={answer} expected/></p>{q.type==='tf'&&q.answer?.reference&&<p>{q.answer.reference}</p>}</div></div>
 <section className="review-reason"><h4>解析与原文依据</h4>{x?.reason&&<AnnotatedText as="p" pid={'reference:reason:'+q.id} text={x.reason}/>}<div className="review-evidence-list">{x?.evidence?.map((v,i)=>{const paragraph=exercise.paragraphs.find(p=>p.id===v.pid),offset=paragraph?.fr.indexOf(v.quote)||0;return <blockquote key={i}><div className="review-evidence-tools"><small>原文第 {exercise.paragraphs.findIndex(p=>p.id===v.pid)+1} 段</small>{v.pairIds?.[0]&&<button className="text-btn" onClick={()=>locate(v.pairIds[0])}><LocateFixed size={13}/>定位</button>}</div><AnnotatedText as="p" pid={v.pid} offset={Math.max(0,offset)} sourceText={paragraph?.fr} text={v.quote} lang="fr"/></blockquote>;})}</div>{x?.limitation&&<p className="evidence-limit">{x.limitation}</p>}
 {(status==='review'||result?.selfEvaluated)&&<div className="self-eval"><span>对照原文自评：</span><button onClick={()=>selfEvaluate('correct')}>掌握了</button><button onClick={()=>selfEvaluate('incorrect')}>需要再练</button></div>}</section>
 </article>;
}
