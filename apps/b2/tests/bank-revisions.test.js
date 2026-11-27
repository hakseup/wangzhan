import test from 'node:test';import assert from 'node:assert/strict';import {loadBank} from '../src/bank.js';
test('licensed bank loads a matching private revision and replaces stale sentence translations',async()=>{
 const calls=[],fetcher=async path=>{calls.push(path);if(path==='/content.json')return Response.json({exercises:[{id:'a',paragraphs:[{fr:'Bonjour.',zh:'old'}]}],lexicon:{translations:{bonjour:'bad'}}});if(path==='/api/content-revisions')return Response.json({version:'new',categories:['long']});return Response.json({version:'new',exercises:[{id:'a',paragraphs:[{fr:'Bonjour.',zh:'你好。'}]}],translations:{bonjour:'你好。'}});};
 const bank=await loadBank(true,fetcher);assert.equal(bank.contentRevision,'new');assert.equal(bank.exercises[0].paragraphs[0].zh,'你好。');assert.deepEqual(bank.lexicon.translations,{bonjour:'你好。'});assert.ok(calls.includes('/api/content-revisions?category=long'));
});
test('guest catalog never requests private translation revisions; mixed versions fail rather than serving partial content',async()=>{
 const calls=[];await loadBank(false,async path=>{calls.push(path);return Response.json({exercises:[],lexicon:{}});});assert.deepEqual(calls,['/api/catalog']);
 await assert.rejects(loadBank(true,async path=>Response.json(path==='/content.json'?{exercises:[],lexicon:{}}:path==='/api/content-revisions'?{version:'new',categories:['long']}:{version:'old',exercises:[],translations:{}})),/version changed/);
});
