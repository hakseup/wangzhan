// 胡桃法语合并站点构建：门户（/）+ DALF C1（/c1/）+ DELF B2 外壳（/b2/）。
// B2 的题库正文、音频与 PDF 不进入公开构建，继续由 api/handler.mjs 从 Supabase 私有存储签名下发。
import {readFileSync,writeFileSync,rmSync,mkdirSync,cpSync,readdirSync,existsSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {resolve} from 'node:path';
import {build} from 'vite';

const ROOT=process.cwd(),OUT=resolve(ROOT,'web-dist'),TMP=resolve(ROOT,'.build');
const files=dir=>readdirSync(dir,{withFileTypes:true}).flatMap(e=>e.isDirectory()?files(dir+'/'+e.name):[dir+'/'+e.name]).sort();
const json=path=>JSON.parse(readFileSync(path,'utf8'));
rmSync(OUT,{recursive:true,force:true});rmSync(TMP,{recursive:true,force:true});mkdirSync(TMP,{recursive:true});

// 1. B2 后端数据：目录（不含正文）与译文修订，写入根目录 cloud/ 供 Vercel 函数读取。
process.chdir(resolve(ROOT,'apps/b2'));
const {compileContentRevisions}=await import('../apps/b2/scripts/compile-content-revisions.mjs');
compileContentRevisions();
process.chdir(ROOT);
mkdirSync('cloud',{recursive:true});
for(const f of readdirSync('apps/b2/cloud'))cpSync('apps/b2/cloud/'+f,'cloud/'+f);
rmSync('apps/b2/cloud',{recursive:true,force:true});
const b2=json('apps/b2/public/content.json'),c1=json('apps/c1/public/content.json');
writeFileSync('cloud/catalog.json',JSON.stringify({level:b2.level,exercises:b2.exercises.map(e=>({id:e.id,category:e.category,title:e.title,titleZh:e.titleZh,topic:e.topic,subtopic:e.subtopic,examSessionLabel:e.examSessionLabel,source:e.source,paragraphs:[],questions:[],studyModels:[],audio:null})),lexicon:{bookCounts:Object.fromEntries(Object.entries(b2.lexicon.books||{}).map(([id,words])=>[id,words.length])),books:{}}}));

// 2. 门户首页使用的题库统计（只含数量，不含题目）。
const count=bank=>bank.exercises.reduce((m,e)=>(m[e.category]=(m[e.category]||0)+1,m),{});
writeFileSync('src/bank-stats.json',JSON.stringify({b2:{total:b2.exercises.length,categories:count(b2)},c1:{total:c1.exercises.length,categories:count(c1)}},null,1)+'\n');

// 3. 三个前端分别构建。
await build({root:ROOT,base:'/',publicDir:'public',build:{outDir:OUT,emptyOutDir:true}});
await build({root:resolve(ROOT,'apps/c1'),base:'/c1/',publicDir:resolve(ROOT,'apps/c1/public'),build:{outDir:resolve(OUT,'c1'),emptyOutDir:true}});
const b2Public=resolve(TMP,'b2-public');mkdirSync(b2Public);
for(const f of ['fonts','images','icon-192.png','icon-512.png','manifest.webmanifest'])cpSync('apps/b2/public/'+f,b2Public+'/'+f,{recursive:true});
await build({root:resolve(ROOT,'apps/b2'),base:'/b2/',publicDir:b2Public,build:{outDir:resolve(OUT,'b2'),emptyOutDir:true}});

// 4. 版本号与 B2 离线外壳缓存。
const hash=createHash('sha256');
for(const file of [...files('web-dist'),...files('api'),...files('cloud').filter(f=>!f.endsWith('/build.json')),...files('src'),...files('apps/b2/src'),...files('apps/c1/src')]){hash.update(file);hash.update(readFileSync(file));}
const id=hash.digest('hex').slice(0,16);
writeFileSync('cloud/build.json',JSON.stringify({id}));writeFileSync('web-dist/build.json',JSON.stringify({id}));
const b2Assets=['/b2/',...files('web-dist/b2').map(f=>f.slice('web-dist'.length))];
writeFileSync('web-dist/b2/sw.js',readFileSync('apps/b2/public/sw.js','utf8').replace('__BUILD__',id).replace('__ASSETS__',JSON.stringify(b2Assets)));

// 5. 防止 B2 受保护内容误入公开目录。
for(const dir of ['web-dist','web-dist/b2'])for(const forbidden of ['content.json','audio','pdfs','dictionary'])if(existsSync(dir+'/'+forbidden))throw Error('Private B2 asset leaked: '+dir+'/'+forbidden);
rmSync(TMP,{recursive:true,force:true});
console.log('胡桃法语站点构建完成：',id);
