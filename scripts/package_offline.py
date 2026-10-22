"""Create the GitHub-downloadable, double-clickable full offline release."""
from pathlib import Path
import runpy
from zipfile import ZipFile,ZIP_DEFLATED
ROOT=Path(__file__).resolve().parents[1]
runpy.run_path(str(ROOT/'scripts/package_standalone.py'))
html=ROOT.parent/'wangzhan-release'/'胡桃法语-DALF-C1-双击打开.html'
out=ROOT/'downloads/noix-dalf-c1-offline.zip';out.parent.mkdir(exist_ok=True)
readme='''胡桃法语 DALF C1 · 巴黎手帐版 · 17日版细节续改

1. 完整解压此压缩包，用电脑 Chrome 或 Edge 打开“胡桃法语-DALF-C1-双击打开.html”。
2. 文件内含176组题库、36段音频、巴黎背景、Logo及手写字体，无需安装或启动服务。首次打开请稍等。
3. 首页是一屏背景与六个入口；点击左侧题型或首页入口后，只显示所选题型全部题目。
4. 首页词句每两分钟随机轮换，来自题库与个人高亮。
5. 听、读、写、口四本词书按各自题库独立筛选，不固定数量，另补充对应的C1任务表达；查词新增词性、词形、词族、短语组成词和句子翻译。未收录词句可在站内联网补充，只将当前查询文字发送给MyMemory，可在查词面板关闭；词库、缓存及可用的浏览器本地翻译仍可离线使用。题目、选项、自己的答案均可高亮，删除高亮可保留备注。单词与笔记中可选择五本词书，进行“法语选中文”或“听音拼写”。到期复习优先，不限制每天学习的新词数量。仅添加了备注的单词进入个人词书，纯高亮和句子不进入背词队列。
6. 法语朗读使用电脑/浏览器的法语语音。请先安装可用的法语系统语音；部分设备的语音需要联网。程序会在无法播放时提示原因。
7. 记住后按1、2、4、7、15、30、60天安排复习；答错后10分钟重试。每日待复习数在站内显示，网站关闭时不提供系统推送。
8. 听力与阅读作答时不展示中文译文；提交后进入双栏复盘，左侧只列答案句及对应译文，右侧逐题显示你的答案、参考答案、解析和原文依据。“定位”可找到左侧答案句，悬停或聚焦原文/译文会用绿色下划线对应双语。写作和口语第三个标签查看范文；支持编辑增删、加粗、下划线和高亮，个人修改自动保存并进入备份。范文是训练参考，不保证固定考试分数。长听力7分钟、短听力3分钟、阅读50分钟、写作150分钟、口语30分钟。具体题型内保留白底无衬线正文、独立滚动、拖动分栏及全屏刷题；题目页顶部已压缩，计时器移至全屏和收藏按钮左侧。
9. 点击右上角头像打开学习设置与备份。旧版作答、草稿、收藏和高亮可通过“学习设置与备份”导出，再在新版导入。词汇复习进度和个人释义也纳入备份。

中文正文和写作指令已全量重新生成参考译文，标题、导语、写作指令及部分正文另经人工校订。其余仍为机器参考译文，尚未全部逐句人工审校；原始材料错行或缺失的已识别片段会注明，不猜测补写。
阅读段落ID和法语文本保留，已增加标题、访谈问题及段落层级，尽量维护旧版标注位置。

不要双击源码根目录的index.html，那是开发入口。手机文件预览器可能不执行网页程序，建议用电脑浏览器打开本文件。
'''
with ZipFile(out,'w',ZIP_DEFLATED,compresslevel=9)as z:
 z.write(html,html.name)
 z.writestr('先读我.txt',readme)
 z.write(ROOT/'public/fonts/OFL.txt','手写字体许可证.txt')
 z.write(ROOT/'public/fonts/MODIFICATIONS.txt','字体微调说明.txt')
 z.write(ROOT/'public/dictionary/NOTICE.txt','离线词典来源与许可.txt')
 z.write(ROOT/'public/dictionary/CC-BY-SA-4.0.txt','补充词典许可证.txt')
with ZipFile(out)as z:assert z.testzip()is None
assert out.stat().st_size<100*1024**2,'GitHub per-file size limit'
print('Verified offline ZIP:',out,round(out.stat().st_size/1024**2,1),'MiB')
