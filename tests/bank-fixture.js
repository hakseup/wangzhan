import fs from 'node:fs';
import {mergeLexiconParts} from '../src/bank.js';
export function loadBankFixture(){const bank=JSON.parse(fs.readFileSync(new URL('../public/content.json',import.meta.url)));return mergeLexiconParts(bank,(bank.lexiconFiles||[]).map(path=>JSON.parse(fs.readFileSync(new URL('../public'+path,import.meta.url)))));}
