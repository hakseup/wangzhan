import test from 'node:test';
import assert from 'node:assert/strict';
import {createProgressSync} from '../src/cloud-progress.js';
import {EMPTY_STATE} from '../src/lib.js';
const copy=x=>structuredClone(x);
function service(){let row={revision:0,state:null},offline=false;return {
 get row(){return copy(row);},set offline(value){offline=value;},
 async call(_path,body,method){if(offline)throw Error('offline');if(method==='PUT'){if(body.revision!==row.revision)throw Object.assign(Error('conflict'),{status:409});row={revision:row.revision+1,state:copy(body.state)};return {revision:row.revision};}return copy(row);}
};}
function client(server,initial=EMPTY_STATE,options={}){const result={state:copy(initial),status:'',conflict:null,pending:options.pending||null};result.engine=createProgressSync({call:server.call,initial,readPending:()=>result.pending,writePending:state=>result.pending=copy(state),removePending:()=>result.pending=null,onState:state=>result.state=copy(state),onStatus:value=>result.status=value,onConflict:value=>result.conflict=value,...options});return result;}
test('first login persists a cloud snapshot, a second client reads all learning fields',async()=>{
 const server=service(),website=client(server);await website.engine.sync();assert.equal(server.row.revision,1);
 const state={...copy(EMPTY_STATE),drafts:{essay:{text:'Mon brouillon'}},answers:{listen:{q1:{value:'A'}}},attempts:{read:{results:{q1:{status:'correct'}}}},bookmarks:['read'],annotations:{read:[{id:'mark',text:'bonjour',note:'你好'}]},vocabProgress:{bonjour:{due:123,step:1}},vocabDefinitions:{bonjour:'你好'},modelEdits:{essay:'<p>Mon texte</p>'},rubrics:{essay:[1]},activity:['2026-11-06']};
 website.engine.setLocal(state);await website.engine.flush();assert.equal(website.status,'云端已同步');
 const mac=client(server);assert.equal(mac.engine.setLocal(copy(EMPTY_STATE)),false);await mac.engine.sync();assert.deepEqual(mac.state,state);assert.equal(mac.conflict,null);
 mac.engine.setLocal({...mac.state,drafts:{...mac.state.drafts,speech:{text:'Mon plan'}}});await mac.engine.flush();await website.engine.sync();assert.deepEqual(website.state,server.row.state);assert.equal(website.state.drafts.speech.text,'Mon plan');
});
test('concurrent clients keep both snapshots until a deliberate conflict choice',async()=>{
 const server=service(),a=client(server),b=client(server);await a.engine.sync();await b.engine.sync();
 a.engine.setLocal({...a.state,drafts:{a:'first device'}});await a.engine.flush();b.engine.setLocal({...b.state,drafts:{b:'second device'}});
 await assert.rejects(b.engine.flush(),e=>e.status===409);assert.ok(b.conflict);assert.equal(b.pending.drafts.b,'second device');assert.equal(server.row.state.drafts.a,'first device');
 await b.engine.resolve(false);assert.equal(server.row.state.drafts.b,'second device');assert.equal(b.pending,null);
});
test('offline changes survive reopening and upload after reconnection',async()=>{
 const server=service(),a=client(server);server.offline=true;await assert.rejects(a.engine.sync());a.engine.setLocal({...a.state,drafts:{essay:'offline draft'}});assert.ok(a.pending);assert.notEqual(a.status,'云端已同步');
 server.offline=false;const reopened=client(server,EMPTY_STATE,{pending:copy(a.pending)});await reopened.engine.flush();assert.equal(server.row.state.drafts.essay,'offline draft');assert.equal(reopened.status,'云端已同步');
});
test('edits arriving while a write is in flight are uploaded in order',async()=>{
 const server=service(),base=client(server);await base.engine.sync();let release;const wait=new Promise(r=>release=r);let writes=0;
 const a=client(server,EMPTY_STATE,{call:async(...args)=>{if(args[2]==='PUT'&&++writes===1)await wait;return server.call(...args);}});await a.engine.sync();a.engine.setLocal({...a.state,drafts:{text:'first'}});const saving=a.engine.flush();await Promise.resolve();a.engine.setLocal({...a.state,drafts:{text:'latest'}});release();await saving;assert.equal(server.row.state.drafts.text,'latest');assert.equal(a.pending,null);
});
test('full browser storage does not stop the cloud write',async()=>{
 const server=service(),a=client(server,EMPTY_STATE,{writePending:()=>{throw Error('quota');}});a.engine.setLocal({...a.state,drafts:{text:'keep'}});await a.engine.flush();assert.equal(server.row.state.drafts.text,'keep');
});
test('JSONB key order does not cause false conflicts when a pending write already reached the server',async()=>{
 const server=service(),a=client(server);await a.engine.sync();a.engine.setLocal({...a.state,answers:{read:{q:{value:'A',justification:'preuve'}}}});await a.engine.flush();
 const pending={...server.row.state,answers:{read:{q:{justification:'preuve',value:'A'}}}};
 const reopened=client(server,EMPTY_STATE,{pending});await reopened.engine.flush();assert.equal(reopened.conflict,null);assert.equal(reopened.status,'云端已同步');
});
