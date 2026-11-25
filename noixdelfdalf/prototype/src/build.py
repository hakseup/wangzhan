import json,sys
a=json.load(open(sys.argv[1]))
t=open(sys.argv[2],encoding='utf-8').read()
for k,v in {'__FONT__':a['font'],'__LOGO__':a['logo'],'__IMG_LEARN__':a['tutor'],'__IMG_READ__':a['read'],'__IMG_BANK__':a['bank'],'__IMG_TUTOR__':a['learn']}.items(): t=t.replace(k,v)
open(sys.argv[3],'w',encoding='utf-8').write(t)
