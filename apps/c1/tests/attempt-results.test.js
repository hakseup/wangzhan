import test from 'node:test';
import assert from 'node:assert/strict';
import {currentAttemptResults} from '../src/attempt-results.js';

test('a source-complete revision keeps old records but never attributes old question scores to new questions',()=>{
 const exercise={contentRevision:'source-2026-11',questions:[{id:'source-q1',type:'choice',answer:{value:'C',reference:'C'}}]};
 const attempt={results:{q1:{status:'correct'}}},answers={q1:{value:'B'}};
 const before=JSON.stringify({attempt,answers});
 assert.equal(currentAttemptResults(exercise,attempt,answers)['source-q1'].status,'unanswered');
 assert.equal(JSON.stringify({attempt,answers}),before);
});
test('current revisions and unchanged exercises retain saved manual self-evaluation',()=>{
 const results={q1:{status:'correct',selfEvaluated:true}};
 assert.equal(currentAttemptResults({contentRevision:'v2'},{contentRevision:'v2',results}),results);
 assert.equal(currentAttemptResults({},{results}),results);
 assert.equal(currentAttemptResults({},null),null);
});
