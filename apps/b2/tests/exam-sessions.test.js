import test from 'node:test';import assert from 'node:assert/strict';
import {examSessions} from '../src/exam-sessions.js';import {loadBankFixture} from './bank-fixture.js';
test('cards show every recorded sitting, including repeats and overseas-only items',()=>{
 const bank=loadBankFixture();for(const e of bank.exercises){const label=examSessions(e);const dates=[...(e.source||'').matchAll(/(\d{4})年(\d{1,2})月/g)];for(const [,year,month]of dates)assert.ok(label.includes(`${year}年${Number(month)}月场`));if(!dates.length&&!e.examSessionLabel)assert.equal(label,'国外考过，国内暂未考过');}
 assert.equal(examSessions({source:'中国场次 2024年6月；中国场次 2026年6月',examSessionLabel:'2026年6月场'}),'2024年6月场、2026年6月场');
});
