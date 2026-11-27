const {app,BrowserWindow,shell,dialog}=require('electron');
const config=require('./app-config.json');
let win;
function approved(url){try{return new URL(url).origin===new URL(config.url).origin;}catch{return false;}}
async function createWindow(){
 if(!config.url||!config.url.startsWith('https://')){await dialog.showMessageBox({type:'error',message:'此安装包缺少已部署的服务地址，请联系发布者。'});app.quit();return;}
 win=new BrowserWindow({width:1440,height:960,minWidth:900,minHeight:650,title:'胡桃法语 · DELF B2',backgroundColor:'#fffaf1',webPreferences:{nodeIntegration:false,contextIsolation:true,sandbox:true,partition:'persist:noix-user'}});
 win.webContents.setWindowOpenHandler(({url})=>{if(url.startsWith('https://'))shell.openExternal(url);return {action:'deny'};});
 win.webContents.on('will-navigate',(event,url)=>{if(!approved(url)){event.preventDefault();if(url.startsWith('https://'))shell.openExternal(url);}});
 win.webContents.session.setPermissionRequestHandler((_wc,_permission,callback)=>callback(false));
 win.webContents.on('did-fail-load',(_event,code)=>{if(code!==-3)dialog.showMessageBox(win,{type:'info',message:'暂时无法连接学习服务',detail:'请检查网络后，在菜单中重新加载。账号和云端学习记录不会因此清除。'});});
 await win.loadURL(config.url);

}
app.whenReady().then(createWindow);app.on('window-all-closed',()=>{if(process.platform!=='darwin')app.quit();});app.on('activate',()=>{if(BrowserWindow.getAllWindows().length===0)createWindow();});
