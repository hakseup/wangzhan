// 合并站点后端：C1 学习记录接口（/api/study?bank=c1）。需先 npm run build 生成 cloud/*.json。
import test from 'node:test';
import assert from 'node:assert/strict';
process.env.SUPABASE_URL='https://sb.test';process.env.SUPABASE_PUBLISHABLE_KEY='pk';
const {default:handler}=await import('../api/handler.mjs');

function call({method='GET',route,query='',body,cookie='noix-access=tok'}){
 return new Promise(resolve=>{
  const headers={host:'site.test',cookie,origin:'https://site.test','content-type':'application/json'};
  const res={statusCode:200,headers:{},setHeader(k,v){this.headers[k]=v;},end(data){resolve({status:this.statusCode,data:data?JSON.parse(data):null});}};
  handler({method,url:'/api/handler?route='+route+query,headers,body:body?JSON.stringify(body):undefined},res);
 });
}
let row=null;const calls=[];
globalThis.fetch=async(url,opts={})=>{
 const u=new URL(url);calls.push(u.pathname);
 const json=(d,s=200)=>new Response(JSON.stringify(d),{status:s,headers:{'content-type':'application/json'}});
 if(u.pathname==='/auth/v1/user')return opts.headers.Authorization==='Bearer tok'?json({id:'u1',email:'a@b.c',email_confirmed_at:'2026-01-01'}):json({},401);
 if(u.pathname==='/rest/v1/noix_bank_progress'){assert.match(u.search,/bank=eq\.c1/);return json(row?[row]:[]);}
 if(u.pathname==='/rest/v1/rpc/noix_save_bank_progress'){const b=JSON.parse(opts.body);if(b.expected_revision!==(row?.revision||0))return json({code:'40001',message:'Progress conflict'},400);row={revision:(row?.revision||0)+1,state:b.new_state,updated_at:'2026-11-27T00:00:00Z'};return json({revision:row.revision,updated_at:row.updated_at});}
 return json({message:'unexpected '+u.pathname},500);
};

test('C1 study records: empty read, save, conflict returns current copy',async()=>{
 let r=await call({route:'study',query:'&bank=c1'});
 assert.deepEqual(r.data,{state:null,version:0,updatedAt:null});
 r=await call({method:'PUT',route:'study',query:'&bank=c1',body:{state:{version:1,answers:{}},expectedVersion:0}});
 assert.equal(r.status,200);assert.equal(r.data.version,1);
 r=await call({method:'PUT',route:'study',query:'&bank=c1',body:{state:{version:1,answers:{x:1}},expectedVersion:0}});
 assert.equal(r.status,409);assert.equal(r.data.current.version,1);
});
test('study requires a login and rejects unknown banks; B2 progress table is untouched',async()=>{
 assert.equal((await call({route:'study',query:'&bank=c1',cookie:''})).status,401);
 assert.equal((await call({route:'study',query:'&bank=zz'})).status,404);
 assert.ok(!calls.some(p=>p.includes('noix_progress')||p.includes('noix_save_progress')));
});
