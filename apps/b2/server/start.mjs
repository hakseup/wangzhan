import {createApp} from './app.mjs';
const app=createApp();app.server.listen(Number(process.env.PORT||3000),'0.0.0.0',()=>console.log('胡桃法语服务已启动'));process.on('SIGTERM',()=>app.server.close(()=>{app.close();process.exit(0);}));
