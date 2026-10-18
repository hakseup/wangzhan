import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
const bank=JSON.parse(fs.readFileSync(new URL('../public/content.json',import.meta.url)));
const all=bank.exercises.flatMap(e=>e.paragraphs);
test('all reference paragraphs have Chinese text and no replacement glyphs or subtitle formatting',()=>{assert.equal(all.length,3361);assert.ok(all.length>2900);for(const p of all){assert.ok(/[\u4e00-\u9fff]/.test(p.zh),p.fr);assert.ok(!/[⁇�]/.test(p.zh),p.zh);assert.ok(!/\{\\(?:fn|bord|pos)/.test(p.zh),p.zh);}});
test('key corrections retain the intended educational, medical and writing meanings',()=>{const teachers=bank.exercises.find(e=>e.id==='reading-2021-10-fr');assert.match(teachers.paragraphs[1].zh,/学业成功/);assert.ok(teachers.paragraphs.every(p=>p.translationReviewed));const medical=all.find(p=>p.fr.startsWith('L’homéopathie*'));assert.match(medical.zh,/顺势疗法/);const task=bank.exercises.find(e=>e.id==='writing-2024-6-cn').tasks.find(t=>t.id==='essai');assert.match(task.zh,/家庭作业/);assert.match(task.zh,/不平等/);});
test('all source writing instructions are translated instead of the former generic placeholder',()=>{for(const e of bank.exercises)for(const t of e.tasks||[]){assert.ok(t.zh?.trim());assert.ok(!t.zh.includes('按法语原题指定的身份、对象和要求'));}});
