"""Create the GitHub-downloadable, double-clickable full offline release."""
from pathlib import Path
import runpy
from zipfile import ZipFile,ZIP_DEFLATED
ROOT=Path(__file__).resolve().parents[1]
runpy.run_path(str(ROOT/'scripts/package_standalone.py'))
html=ROOT.parent/'wangzhan-release'/'胡桃法语-DALF-C1-双击打开.html'
out=ROOT/'downloads/noix-dalf-c1-offline.zip';out.parent.mkdir(exist_ok=True)
readme='''胡桃法语 DALF C1 · 巴黎手帐版（2026-10-17）

1. 完整解压此压缩包，用电脑 Chrome 或 Edge 打开“胡桃法语-DALF-C1-双击打开.html”。
2. 文件内含176组题库、36段音频、巴黎背景、Logo及手写字体，无需安装或启动服务。首次打开请稍等。
3. 首页是一屏背景与六个入口；点击左侧题型或首页入口后，只显示所选题型全部题目。
4. 首页词句每两分钟随机轮换，来自题库与个人高亮。
5. 单词与笔记中可选择五本词书，进行“法语选中文”或“听音拼写”。到期复习优先，每天最多20个新词。
6. 法语朗读使用电脑/浏览器的法语语音。请先安装可用的法语系统语音；部分设备的语音需要联网。程序会在无法播放时提示原因。
7. 记住后按1、2、4、7、15、30、60天安排复习；答错后10分钟重试。每日待复习数在站内显示，网站关闭时不提供系统推送。
8. 具体题型内保留白底无衬线正文、独立滚动、拖动分栏及全屏刷题。听力答完提交后进入原文复盘。
9. 旧版作答、草稿、收藏和高亮可通过“学习设置与备份”导出，再在新版导入。词汇复习进度和个人释义也纳入备份。

中文正文和写作指令已全量重新生成参考译文，标题、导语、写作指令及部分正文另经人工校订。其余仍为机器参考译文，尚未全部逐句人工审校；原始材料错行或缺失的已识别片段会注明，不猜测补写。
阅读段落ID和法语文本保留，已增加标题、访谈问题及段落层级，尽量维护旧版标注位置。

不要双击源码根目录的index.html，那是开发入口。手机文件预览器可能不执行网页程序，建议用电脑浏览器打开本文件。
'''
with ZipFile(out,'w',ZIP_DEFLATED,compresslevel=5)as z:
 z.write(html,html.name)
 z.writestr('先读我.txt',readme)
 z.write(ROOT/'public/fonts/OFL.txt','手写字体许可证.txt')
with ZipFile(out)as z:assert z.testzip()is None
assert out.stat().st_size<100*1024**2,'GitHub per-file size limit'
print('Verified offline ZIP:',out,round(out.stat().st_size/1024**2,1),'MiB')
