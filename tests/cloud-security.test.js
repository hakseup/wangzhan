import test from 'node:test';
import assert from 'node:assert/strict';
import {privatePath,sameOrigin,gateway,identity,setSession} from '../cloud/supabase.mjs';
test('private asset paths reject traversal, URL injection and unlisted paths',()=>{
 for(const path of ['/content.json','/pdfs/long-123.pdf','/audio/short-2024-6.m4a'])assert.ok(privatePath(path));
 for(const path of ['/pdfs/../content.json','//evil.test/a.pdf','/pdfs/a?x.pdf','/admin/private.json'])assert.equal(privatePath(path),null);
});
test('mutations require exact HTTPS origin',()=>{
 sameOrigin({headers:{origin:'https://noix.test',host:'noix.test','sec-fetch-site':'same-origin'}});
 for(const origin of ['https://evil.test','http://noix.test',undefined])assert.throws(()=>sameOrigin({headers:{origin,host:'noix.test'}}));
});
test('session cookies are HttpOnly and never client-readable',()=>{
 let cookies;setSession({setHeader:(_k,v)=>cookies=v},{access_token:'token',refresh_token:'refresh'});
 assert.equal(cookies.length,2);for(const c of cookies)assert.match(c,/HttpOnly; Secure; SameSite=Lax/);
});
test('expired token uses verified refresh response, forged valid-looking tokens do not authenticate',async()=>{
 const sb=async path=>{if(path==='/auth/v1/user')throw Object.assign(Error('expired'),{status:401});throw Object.assign(Error('invalid'),{status:400});};
 let cleared=false;const auth=await identity({headers:{cookie:'noix-access=forged; noix-refresh=invalid'}},{setHeader:()=>cleared=true},sb);
 assert.equal(auth,null);assert.ok(cleared);
});
test('Supabase gateway preserves optimistic concurrency conflict and hides upstream details',async()=>{
 const sb=gateway({SUPABASE_URL:'https://db.test',SUPABASE_PUBLISHABLE_KEY:'public'},async()=>new Response(JSON.stringify({code:'40001',message:'private database detail'}),{status:500}));
 await assert.rejects(sb('/rest/v1/rpc/noix_save_progress'),e=>e.status===409&&!e.message.includes('private'));
});
