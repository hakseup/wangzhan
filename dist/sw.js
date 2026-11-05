const BUILD='09404aa8dded4c72',CACHE='noix-shell-'+BUILD,ASSETS=["/","/manifest.webmanifest","/icon-192.png","/icon-512.png","/assets/index-CcBKVPxI.js","/assets/index-YzuCJdpi.css","/fonts/Journal.ttf","/fonts/MODIFICATIONS.txt","/fonts/OFL.txt","/images/arc-haze.png","/images/hutao-logo.png"];
self.addEventListener('install',event=>event.waitUntil(caches.open(CACHE).then(cache=>cache.addAll(ASSETS))));
self.addEventListener('message',event=>{if(event.data?.type==='ACTIVATE')self.skipWaiting();});
self.addEventListener('activate',event=>event.waitUntil(caches.keys().then(keys=>Promise.all(keys.filter(k=>k.startsWith('noix-shell-')&&k!==CACHE).map(k=>caches.delete(k)))).then(()=>self.clients.claim())));
self.addEventListener('fetch',event=>{const u=new URL(event.request.url);if(event.request.method!=='GET'||u.origin!==location.origin||u.pathname.startsWith('/api/')||['/content.json','/audio/','/pdfs/','/dictionary/'].some(p=>u.pathname===p||u.pathname.startsWith(p)))return;
 if(event.request.mode==='navigate'){event.respondWith(fetch(event.request).catch(()=>caches.match('/')));return;}
 if(['/assets/','/images/','/fonts/','/icon-'].some(p=>u.pathname.startsWith(p)))event.respondWith(caches.match(event.request).then(saved=>saved||fetch(event.request).then(r=>{if(r.ok)caches.open(CACHE).then(c=>c.put(event.request,r.clone()));return r;})));
});
