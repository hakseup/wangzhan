import fs from 'node:fs';export function loadBankFixture(){return JSON.parse(fs.readFileSync(new URL('../public/content.json',import.meta.url)));}
