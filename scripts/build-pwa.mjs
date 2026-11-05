import {readFileSync,writeFileSync,readdirSync} from 'node:fs';import {createHash} from 'node:crypto';
const files=dir=>readdirSync(dir,{withFileTypes:true}).flatMap(e=>e.isDirectory()?files(dir+'/'+e.name):[dir+'/'+e.name]).sort();
const hash=createHash('sha256');for(const file of [...files('dist').filter(f=>!['dist/sw.js','dist/build.json'].includes(f)),...files('server')]){hash.update(file+'\0');hash.update(readFileSync(file));}const build=hash.digest('hex').slice(0,16);
const assets=['/','/manifest.webmanifest','/icon-192.png','/icon-512.png',...['assets','fonts','images'].flatMap(dir=>files('dist/'+dir).map(file=>file.slice(4)))];
writeFileSync('dist/build.json',JSON.stringify({id:build,builtAt:new Date().toISOString()}));writeFileSync('dist/sw.js',readFileSync('public/sw.js','utf8').replace('__BUILD__',build).replace('__ASSETS__',JSON.stringify(assets)));console.log('PWA build:',build);
