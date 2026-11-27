import test from 'node:test';
import assert from 'node:assert/strict';
import {initializeResources} from '../src/resources.js';
import {exerciseFromHash} from '../src/navigation.js';
test('email verification fragments are never mistaken for exercise links',()=>{
 assert.equal(exerciseFromHash('#access_token=private&refresh_token=private&type=signup'),'');
 assert.equal(exerciseFromHash('#error=expired_token'),'');
 assert.equal(exerciseFromHash('#long-123/review'),'long-123');
 assert.equal(exerciseFromHash('#%zz'),'');
});
test('administrator initialization imports the bank first and makes it usable before remaining assets finish',async()=>{
 const calls=[],states=[];
 const api=async(_path,body)=>{if(body.index===undefined)return {total:4,pending:[3,0,2],bankReady:false};calls.push(body.index);};
 await initializeResources(api,s=>states.push(s));
 assert.deepEqual(calls,[0,2,3]);assert.equal(states[0].bankReady,false);assert.equal(states[1].bankReady,true);assert.equal(states[1].phase,'importing');assert.equal(states.at(-1).phase,'ready');assert.equal(states.at(-1).done,4);
});
test('reopening after an interrupted import only requests missing files; failure is not reported as success',async()=>{
 const calls=[];let state;
 await assert.rejects(initializeResources(async(_path,b)=>{if(b.index===undefined)return {total:3,pending:[2],bankReady:true};calls.push(b.index);throw Error('temporary outage');},s=>state=s),/outage/);
 assert.deepEqual(calls,[2]);assert.equal(state.bankReady,true);assert.equal(state.phase,'importing');assert.equal(state.done,2);
 await initializeResources(async()=>({total:3,pending:[],bankReady:true}),s=>state=s);assert.equal(state.phase,'ready');
});
