import test from 'node:test';import assert from 'node:assert/strict';import {compareExercises} from '../src/exercise-sort.js';
test('unpracticed first reverses practiced priority and preserves the original order within each group',()=>{
 const items=[{id:'a',title:'Z'},{id:'b',title:'C'},{id:'c',title:'A'},{id:'d',title:'B'}],attempts={a:{},c:{}};
 assert.deepEqual([...items].sort((a,b)=>compareExercises('unpracticed',attempts,a,b)).map(e=>e.id),['b','d','a','c']);
 assert.deepEqual([...items].sort((a,b)=>compareExercises('progress',attempts,a,b)).map(e=>e.id),['a','c','b','d']);
 assert.deepEqual([...items].sort((a,b)=>compareExercises('default',attempts,a,b)),items);
});
