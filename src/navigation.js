export function exerciseFromHash(hash){
 const fragment=hash.replace(/^#/,'');
 const auth=new URLSearchParams(fragment);
 if(auth.has('access_token')||auth.has('refresh_token')||auth.has('error'))return '';
 try{return decodeURIComponent(fragment.split('/')[0]);}catch{return '';}
}
