import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {createHash} from 'node:crypto';
import {wordCount} from '../src/lib.js';
const json=path=>JSON.parse(fs.readFileSync(new URL(path,import.meta.url)));
const bank=json('../public/content.json');
const audit=json('../data/pasted-speaking-import-audit.json');
const raw=fs.readFileSync(new URL('../data/source-text/补充口语题目-用户提供.txt',import.meta.url),'utf8');
const compact=s=>s.replace(/\s+/g,'');
test('all twelve supplied oral topics are classified, with ten additions and no duplicated existing exercises',()=>{
 assert.equal(createHash('sha256').update(raw).digest('hex'),audit.sha256);
 assert.equal(audit.items.length,12);assert.equal(audit.added,10);assert.equal(audit.matchedExisting,2);
 assert.equal(new Set(audit.items.map(e=>e.id)).size,12);
 const headings=[...raw.matchAll(/^(\d+)\. (.+)$/gm)];
 for(let i=0;i<headings.length;i++){
  const h=headings[i],m=audit.items.find(m=>m.item===Number(h[1])),e=bank.exercises.find(e=>e.id===m.id);
  assert.ok(e);assert.equal(e.category,'speaking');assert.equal(e.topic,m.topic);assert.equal(e.subtopic,m.subtopic);assert.equal(e.subjectReference,m.reference);
  assert.equal(bank.exercises.filter(other=>other.category==='speaking'&&other.title===e.title).length,1);
  const block=raw.slice(h.index+h[0].length,headings[i+1]?.index).split(/^(?:小主题：|[一二三四五六七八九十]+、)/m)[0];
  const fr=block.split('法语原文')[1].split('中文翻译')[0].trim().split(/\n\s*\n/).slice(1).join('\n\n');
  assert.equal(compact(e.paragraphs.map(p=>p.fr).join('')),compact(fr));
  if(m.action==='added'){
   const zh=block.split('中文翻译')[1].trim().split(/\n\s*\n/).slice(1).join('\n\n');
   assert.equal(compact(e.paragraphs.map(p=>p.zh).join('')+(e.contentNotes||[]).join('')),compact(zh));
   assert.ok(e.paragraphs.every(p=>p.zh&&p.translationReviewed));
   assert.equal(e.source,'国外考过，国内暂未考过');assert.ok(!e.examSessionLabel);
   assert.ok(wordCount(e.studyModels[0].paragraphs.join(' '))>=300);
   assert.equal(e.studyModels[1].paragraphs.filter(p=>p.startsWith('Question :')).length,3);
  }else assert.equal(e.examSessionLabel,m.sessionPreserved);
 }
 assert.deepEqual(Object.fromEntries(['职业职场','男女问题','社会生活','科技影响'].map(topic=>[topic,audit.items.filter(m=>m.action==='added'&&m.topic===topic).length])),{'职业职场':2,'男女问题':2,'社会生活':3,'科技影响':3});
 const money=bank.exercises.find(e=>e.title==='Espèces en voie de disparition');assert.equal(money.topic,'科技影响');assert.match(money.titleZh,/现金/);assert.ok(money.contentNotes.some(n=>n.includes('现金')));
});
