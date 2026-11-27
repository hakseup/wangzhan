import {readFileSync,writeFileSync,rmSync,mkdirSync,cpSync,readdirSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {build} from 'vite';
import {compileContentRevisions} from './compile-content-revisions.mjs';
compileContentRevisions();
const bank=JSON.parse(readFileSync('public/content.json'));
mkdirSync('cloud',{recursive:true});
writeFileSync('cloud/catalog.json',JSON.stringify({level:bank.level,exercises:bank.exercises.map(e=>({id:e.id,category:e.category,title:e.title,titleZh:e.titleZh,topic:e.topic,subtopic:e.subtopic,examSessionLabel:e.examSessionLabel,source:e.source,paragraphs:[],questions:[],studyModels:[],audio:null})),lexicon:{bookCounts:Object.fromEntries(Object.entries(bank.lexicon.books||{}).map(([id,words])=>[id,words.length]))}}));
rmSync('cloud-public',{recursive:true,force:true});mkdirSync('cloud-public');
for(const file of ['fonts','images','icon-192.png','icon-512.png','manifest.webmanifest'])cpSync('public/'+file,'cloud-public/'+file,{recursive:true});
await build({publicDir:'cloud-public',build:{outDir:'web-dist'}});
const files=dir=>readdirSync(dir,{withFileTypes:true}).flatMap(e=>e.isDirectory()?files(dir+'/'+e.name):[dir+'/'+e.name]).sort();
const hash=createHash('sha256');for(const file of [...files('web-dist'),...files('api'),...files('cloud').filter(f=>!f.endsWith('/build.json')), ...files('src')]){hash.update(file);hash.update(readFileSync(file));}
const id=hash.digest('hex').slice(0,16),assets=['/',...files('web-dist').map(f=>f.slice('web-dist'.length))];
writeFileSync('cloud/build.json',JSON.stringify({id}));writeFileSync('web-dist/build.json',JSON.stringify({id}));
writeFileSync('web-dist/sw.js',readFileSync('public/sw.js','utf8').replace('__BUILD__',id).replace('__ASSETS__',JSON.stringify(assets)));
// Protect licensed material even if future build changes accidentally copy files.
for(const forbidden of ['content.json','audio','pdfs','dictionary'])if(readdirSync('web-dist').includes(forbidden))throw Error('Private asset leaked: '+forbidden);
console.log('Cloud shell build:',id);
