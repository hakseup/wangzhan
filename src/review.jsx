import React,{useMemo} from 'react';
import {buildReviewParagraphs,activeSentenceLinks} from './review-paragraphs.js';
import {AnnotatedText} from './annotations.jsx';
import {CheckCircle2,XCircle,Clock3,LocateFixed,Minus,Plus} from 'lucide-react';
export function EvidenceReader({exercise,active,activate,fontSize,resizeFont,lexicon}){
 const paragraphs=useMemo(()=>buildReviewParagraphs(exercise,lexicon),[exercise,lexicon]);
 return <div className="evidence-reader reader-content full-review-reader" style={{fontSize}}><div className="review-caption"><strong>完整原文 · 逐段译文</strong><span>浅黄色标出答案句 · 悬停或聚焦可对应双语</span><div className="reader-size"><button aria-label="缩小正文" disabled={fontSize<=14} onClick={()=>resizeFont(Math.max(14,fontSize-1))}><Minus size={14}/></button><span>Aa</span><button aria-label="放大正文" disabled={fontSize>=26} onClick={()=>resizeFont(Math.min(26,fontSize+1))}><Plus size={14}/></button></div></div>{paragraphs.map(p=>{
 const link=activeSentenceLinks(p,active),linked=!!link.sourceId;
 return <article key={p.id} className={'evidence-pair review-paragraph '+(linked?'is-linked':'')} data-paragraph={p.id}>
 <p className={'evidence-fr paragraph-'+(p.role||'body')+(p.continuation?' paragraph-continuation':'')} lang="fr">{p.units.map(unit=><span key={unit.id} className={'review-source-unit '+(link.sourceId===unit.id?'is-linked':'')} data-evidence-id={unit.pairId} tabIndex={0} onMouseEnter={()=>activate(unit.id)} onMouseLeave={()=>activate(null)} onFocus={()=>activate(unit.id)} onBlur={()=>activate(null)}>{unit.evidenceIds.slice(1).map(id=><span key={id} data-evidence-id={id} className={'review-evidence-anchor '+(link.sourceId===unit.id?'is-linked':'')} aria-hidden="true"/>)}{unit.runs.map(run=><React.Fragment key={run.start}>{run.labels.length>0&&<span className="review-answer-label" aria-label={'第'+run.labels.join('、')+'题答案句'}>{run.labels.map(n=>'Q'+n).join(' · ')}</span>}<span className={run.answer?'answer-source':''}><AnnotatedText pid={p.id} offset={run.start} sourceText={p.fr} text={run.text}/></span></React.Fragment>)}</span>)}</p>
 <p className="evidence-zh" lang="zh-CN">{p.translation.map(t=><span key={t.start} className={'review-translation-unit '+(link.translationId===t.id?'is-linked':'')} tabIndex={0} onMouseEnter={()=>activate(t.id)} onMouseLeave={()=>activate(null)} onFocus={()=>activate(t.id)} onBlur={()=>activate(null)}><AnnotatedText pid={'reference:paragraph-translation:'+p.id} offset={t.start} sourceText={p.zh||''} text={t.text}/></span>)}</p>
 </article>;
 })}</div>;
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
 {['choice','tf'].includes(q.type)&&<div className="review-options" role="list" aria-label={'第'+q.number+'题全部选项'}>{(q.type==='choice'?q.options:[{id:'Vrai',text:'Vrai',zh:'符合原文'},{id:'Faux',text:'Faux',zh:'不符合原文'}]).map(o=>{const chosen=answer.value===o.id,correct=q.answer?.value===o.id;return <div key={o.id} role="listitem" className={'review-option '+(chosen?'chosen ':'')+(correct?'is-correct ':'')+(chosen&&q.answer?.value&&!correct?'is-incorrect':'')}><span className="review-radio" aria-hidden="true">{chosen?'●':'○'}</span><div><div className="review-option-fr">{q.type==='choice'&&<b>{o.id}. </b>}<AnnotatedText pid={'option:'+q.id+':'+o.id} text={o.text} lang="fr"/></div><span className="review-option-zh">{o.zh}</span></div><span className="review-option-tags">{chosen&&<small>你的选择</small>}{correct&&<small>正确答案</small>}</span></div>;})}</div>}
 <div className="review-answer-comparison"><div><strong>你的答案</strong><p><AnswerText q={q} answer={answer}/></p>{answer.justification&&<p className="review-justification"><AnnotatedText pid={'answer:'+q.id+':justification'} text={answer.justification} lang="fr"/></p>}</div><div><strong>参考答案</strong><p><AnswerText q={q} answer={answer} expected/></p>{q.type==='tf'&&q.answer?.reference&&<p>{q.answer.reference}</p>}</div></div>
 <section className="review-reason"><h4>解析与原文依据</h4>{x?.reason&&<AnnotatedText as="p" pid={'reference:reason:'+q.id} text={x.reason}/>}<div className="review-evidence-list">{x?.evidence?.map((v,i)=>{const paragraph=exercise.paragraphs.find(p=>p.id===v.pid),offset=paragraph?.fr.indexOf(v.quote)||0;return <blockquote key={i}><div className="review-evidence-tools"><small>原文第 {exercise.paragraphs.findIndex(p=>p.id===v.pid)+1} 段</small>{v.pairIds?.[0]&&<button className="text-btn" onClick={()=>locate(v.pairIds[0])}><LocateFixed size={13}/>定位</button>}</div><AnnotatedText as="p" pid={v.pid} offset={Math.max(0,offset)} sourceText={paragraph?.fr} text={v.quote} lang="fr"/></blockquote>;})}</div>{x?.limitation&&<p className="evidence-limit">{x.limitation}</p>}
 {(status==='review'||result?.selfEvaluated)&&<div className="self-eval"><span>对照原文自评：</span><button onClick={()=>selfEvaluate('correct')}>掌握了</button><button onClick={()=>selfEvaluate('incorrect')}>需要再练</button></div>}</section>
 </article>;
}
