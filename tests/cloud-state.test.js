import test from 'node:test';import assert from 'node:assert/strict';
import {StudyStore,mergeStudy}from'../src/cloud-state.js';import{EMPTY_STATE,STORAGE_KEY}from'../src/lib.js';
const copy=x=>structuredClone(x);
class MemoryStorage{data=new Map();getItem=k=>this.data.get(k)||null;setItem=(k,v)=>this.data.set(k,v);removeItem=k=>this.data.delete(k);}
function backend(){const accounts=new Map();let current='A',writes=0,failRead=false;return {accounts,get writes(){return writes;},setUser:v=>current=v,setFail:v=>failRead=v,fetcher:async(path,options={})=>{
 const user={id:current,email:current.toLowerCase()+'@example.test'};
 if(path==='/api/auth/get-session')return Response.json({user});if(path==='/api/auth/sign-out')return Response.json({success:true});
 if(path==='/api/study'){
  assert.equal(options.headers['x-study-account'],current);
  const remote=accounts.get(current)||{state:null,version:0,updatedAt:null};if(options.method==='GET'){if(failRead)throw Error('offline');return Response.json(remote);}
  writes++;const data=JSON.parse(options.body);if(data.expectedVersion!==remote.version)return Response.json({current:remote},{status:409});const saved={state:data.state,version:remote.version+1,updatedAt:new Date().toISOString()};accounts.set(current,saved);return Response.json(saved);
 }throw Error(path);
 }};}
test('first login backs up guest progress and switching accounts never carries it into a second account',async()=>{
 const storage=new MemoryStorage(),api=backend(),guest=copy(EMPTY_STATE);guest.answers.old={q1:{value:'Ancienne réponse'}};storage.setItem(STORAGE_KEY,JSON.stringify(guest));const store=new StudyStore({storage,fetcher:api.fetcher,enabled:true,delay:999999});
 try{await store.init();await store.flush();assert.deepEqual(api.accounts.get('A').state.answers,guest.answers);assert.equal(storage.getItem(STORAGE_KEY),null);await store.signOut();api.setUser('B');await store.activate({id:'B',email:'b@example.test'});assert.deepEqual(store.snapshot.study.answers,{});await store.flush();assert.deepEqual(api.accounts.get('B').state.answers,{});api.setUser('A');await store.activate({id:'A',email:'a@example.test'});assert.deepEqual(store.snapshot.study.answers,guest.answers);}finally{store.dispose();}
});
test('a concurrent update merges independent edits, while conflicting answers remain blocked across reload',async()=>{
 const storage=new MemoryStorage(),api=backend();api.accounts.set('A',{state:copy(EMPTY_STATE),version:1,updatedAt:null});let store=new StudyStore({storage,fetcher:api.fetcher,enabled:true,delay:999999});
 try{
  await store.init();store.updateStudy(s=>({...s,answers:{e:{q:{value:'Local'}}}}));const other=copy(EMPTY_STATE);other.drafts.e={outline:'Remote outline'};api.accounts.set('A',{state:other,version:2,updatedAt:null});await store.flush();assert.equal(store.snapshot.conflict,null);await store.flush();assert.equal(api.accounts.get('A').state.answers.e.q.value,'Local');assert.equal(api.accounts.get('A').state.drafts.e.outline,'Remote outline');
  const baseline=copy(api.accounts.get('A').state);store.updateStudy(s=>({...s,answers:{e:{q:{value:'Changed locally'}}}}));baseline.answers.e.q.value='Changed remotely';api.accounts.set('A',{state:baseline,version:4,updatedAt:null});await store.flush();assert.ok(store.snapshot.conflict);const before=api.writes;store.dispose();store=new StudyStore({storage,fetcher:api.fetcher,enabled:true,delay:999999});await store.init();assert.ok(store.snapshot.conflict);await store.flush();assert.equal(api.writes,before);store.resolveConflict('remote');assert.equal(store.snapshot.study.answers.e.q.value,'Changed remotely');
 }finally{store.dispose();}
});
test('failed cloud hydration keeps the local records and never uploads them over an unknown cloud snapshot',async()=>{
 const storage=new MemoryStorage(),api=backend(),guest=copy(EMPTY_STATE);guest.drafts.e={essai:'Texte'};storage.setItem(STORAGE_KEY,JSON.stringify(guest));api.setFail(true);const store=new StudyStore({storage,fetcher:api.fetcher,enabled:true,delay:999999});try{await store.init();assert.equal(store.snapshot.status,'error');assert.equal(store.snapshot.study.drafts.e.essai,'Texte');await store.flush();assert.equal(api.writes,0);}finally{store.dispose();}
});
test('three-way merging preserves separate annotations and respects an intentional bookmark removal',()=>{
 const b=copy(EMPTY_STATE),l=copy(b),r=copy(b);b.bookmarks=['a'];l.bookmarks=[];r.bookmarks=['a','b'];l.annotations.e=[{id:'1',text:'a'}];r.annotations.e=[{id:'2',text:'b'}];b.annotations.e=[];const merged=mergeStudy(b,l,r);assert.equal(merged.conflicts,0);assert.deepEqual(merged.state.bookmarks,['b']);assert.equal(merged.state.annotations.e.length,2);
});
