import {readFileSync,writeFileSync} from 'node:fs';import {createHash} from 'node:crypto';
const build=createHash('sha256').update(readFileSync('dist/index.html')).digest('hex').slice(0,12);writeFileSync('dist/sw.js',readFileSync('public/sw.js','utf8').replace('__BUILD__',build));console.log('PWA build:',build);
