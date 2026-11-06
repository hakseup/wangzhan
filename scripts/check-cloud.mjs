import assert from 'node:assert/strict';
const origin='https://noix-delf-b2-mac.vercel.app';
const get=path=>fetch(origin+path,{redirect:'manual',signal:AbortSignal.timeout(30000)});
const home=await get('/');assert.equal(home.status,200,'Public homepage must be reachable without Vercel login');
const session=await get('/api/session');assert.equal(session.status,200);assert.deepEqual(await session.json(),{user:null,entitled:false});
const catalog=await get('/api/catalog');assert.equal(catalog.status,200);const bank=await catalog.json();assert.equal(bank.exercises.length,313);assert.ok(bank.exercises.every(e=>e.paragraphs.length===0&&e.questions.length===0&&e.studyModels.length===0&&!e.audio));
assert.ok(bank.exercises.every(e=>typeof e.source==='string'));assert.equal(bank.lexicon.bookCounts.listening,3693);
const news=await get('/api/news');assert.equal(news.status,200);assert.ok(Array.isArray((await news.json()).notices));
// HEAD only: do not download licensed material or follow signed redirects.
for(const path of ['/content.json','/api/content-revisions','/pdfs/long-1225a5a27013.pdf','/audio/long-2024-3.m4a']){
 const response=await fetch(origin+path,{method:'HEAD',redirect:'manual',signal:AbortSignal.timeout(30000)});assert.equal(response.status,401,'Unauthenticated asset must be blocked: '+path);
}
const admin=await get('/api/admin/dashboard');assert.equal(admin.status,401);
const csrf=await fetch(origin+'/api/login',{method:'POST',headers:{'Content-Type':'application/json',Origin:'https://example.invalid'},body:'{}'});assert.equal(csrf.status,403);
console.log('Public homepage, guest catalog, real Supabase news, private asset HEAD restrictions and CSRF checks passed.');
