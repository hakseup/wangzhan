import React from 'react';
import {ArrowLeft,ArrowDownToLine,Download,FileText,Headphones,AudioLines,BookOpen,PenLine,Mic} from 'lucide-react';
import catalogue from './pdf-downloads.json';
import './pdf-downloads.css';
import {usePlatform,Paywall} from './platform.jsx';
const icons={long:Headphones,short:AudioLines,reading1:BookOpen,reading2:BookOpen,writing:PenLine,speaking:Mic};
export function pdfHref(file){return (window.__NOIX_EMBEDDED_BANK__?'./pdfs/':'/pdfs/')+file.asset;}
function PdfLink({file,locked=false}){const Tag=locked?'div':'a';return <Tag className={'pdf-download-link'+(locked?' is-locked':'')} {...(locked?{}:{href:pdfHref(file),download:file.filename})}><span className="pdf-file-icon"><FileText size={20}/></span><span className="pdf-file-copy"><strong>{file.title}</strong><small>{file.subtitle?file.subtitle+' · ':''}PDF · {file.sizeLabel}</small></span><span className="pdf-download-action" aria-disabled={locked||undefined}><span>下载</span><ArrowDownToLine size={17}/></span></Tag>;}
export function PdfDownloads({onBack}){
 const {entitled}=usePlatform();
 return <div className="pdf-download-page"><button className="pdf-back" onClick={onBack}><ArrowLeft size={16}/> 返回首页</button><header className="pdf-page-heading"><div className="pdf-heading-icon"><Download size={25}/></div><p lang="fr">Les sujets à emporter</p><h1>下载题目PDF版本</h1><span>把题目带在身边，按自己的节奏练习。</span></header>{catalogue.resources.length>0&&<div className="pdf-resources">{catalogue.resources.map(file=><PdfLink key={file.asset} file={file} locked={!entitled}/>)}</div>}<div className="pdf-sections">{catalogue.sections.map(section=>{const Icon=icons[section.id];return <section className="pdf-section" key={section.id} aria-labelledby={'pdf-'+section.id}><div className="pdf-section-heading"><span className={'pdf-category-icon '+section.id}><Icon size={23}/></span><div><h2 id={'pdf-'+section.id}>{section.title}</h2><p lang="fr">{section.fr}</p></div><span className="pdf-section-count">{section.files.length} 份PDF</span></div><PdfFiles files={section.files} entitled={entitled}/></section>;})}</div></div>;
}

function PdfFiles({files,entitled}){const list=<div className="pdf-file-list">{files.map(file=><PdfLink file={file} key={file.asset} locked={!entitled}/>)}</div>;return entitled?list:<Paywall compact>{list}</Paywall>;}
