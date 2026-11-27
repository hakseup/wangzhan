import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {createHash} from 'node:crypto';

const readJson=path=>JSON.parse(fs.readFileSync(new URL(path,import.meta.url)));
test('download catalogue includes all 77 original PDFs in the requested groups',()=>{
 const catalogue=readJson('../src/pdf-downloads.json');
 assert.deepEqual(catalogue.sections.map(s=>[s.id,s.files.length]),[
  ['long',17],['short',17],['reading1',17],['reading2',17],['writing',1],['speaking',7],
 ]);
 const files=[...catalogue.sections.flatMap(s=>s.files),...catalogue.resources];
 assert.equal(files.length,77);
 assert.equal(new Set(files.map(f=>f.asset)).size,77);
 const audit=readJson('../data/pdf-downloads-audit.json');
 assert.equal(audit.files.length,77);
 assert.equal(new Set(audit.files.map(f=>f.uploadId)).size,77);
 assert.ok(audit.files.every(f=>/^file_[a-f0-9]+$/.test(f.uploadId)));
 for(const file of files){
  const bytes=fs.readFileSync(new URL('../public/pdfs/'+file.asset,import.meta.url));
  assert.equal(bytes.subarray(0,5).toString(),'%PDF-');
  assert.equal(bytes.length,file.bytes);
  assert.equal(createHash('sha256').update(bytes).digest('hex'),file.sha256);
  assert.ok(file.filename.endsWith('.pdf'));
  assert.ok(audit.files.some(f=>f.asset===file.asset&&f.sha256===file.sha256));
 }
 const bank=readJson('../public/content.json');
 const norm=s=>s.normalize('NFC').replace(/\s/g,'');
 for(const section of catalogue.sections.slice(0,4)){
  const names=section.files.map(f=>norm(f.filename));
  for(const e of bank.exercises.filter(e=>e.category===section.id))assert.ok(names.includes(norm(e.sourceFile)),e.id);
 }
});
