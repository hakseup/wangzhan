"""Create the GitHub-downloadable, double-clickable full offline release."""
from pathlib import Path
import runpy
from zipfile import ZipFile,ZIP_DEFLATED
ROOT=Path(__file__).resolve().parents[1]
runpy.run_path(str(ROOT/'scripts/package_standalone.py'))
html=ROOT.parent/'wangzhan-release'/'胡桃法语-DALF-C1-双击打开.html'
out=ROOT/'downloads/noix-dalf-c1-offline.zip';out.parent.mkdir(exist_ok=True)
readme='''胡桃法语 DALF C1 · 巴黎风格离线版（2026-10-17）

1. 完整解压此压缩包。
2. 用电脑 Chrome 或 Edge 打开“胡桃法语-DALF-C1-双击打开.html”。
3. 文件内含全部题库、36 段音频、背景和 Logo，无需联网或安装。首次打开请稍等。
4. 题目右上角可点击“全屏刷题”；Esc 或“退出全屏”可退出。
5. 材料和答题区可分别滚动；可拖动中间分隔线调整宽度。
6. 听力需答完全部题目并提交，下一页才显示原文与参考译文。
7. 正文已改为白底无衬线字体；高亮仍按黄→紫→红切换，词汇备注红色加粗。

新版保留浏览器学习备份功能。换文件或设备前，请在旧版设置中导出备份，再到新版导入。
写作与口语正文已重新整理，旧版标注会保留在单词本，但可能无法定位到修改后的正文；草稿、作答和收藏仍可导入。

资料说明：已重新处理 269 页写作/口语材料，并修复字体编码、扫描噪点和段落问题。
低清扫描仍可能有识别误差；中文为未逐段人工校对的机器参考译文。写作、口语和开放回答需要对照自评，不提供自动语义评分。

请勿打开源码包根目录的 index.html：那是开发入口，需要 Node.js 构建。
手机的文件预览器可能不运行网页程序，建议使用电脑浏览器。
'''
with ZipFile(out,'w',ZIP_DEFLATED,compresslevel=5)as z:
 z.write(html,html.name)
 z.writestr('先读我.txt',readme)
with ZipFile(out)as z:assert z.testzip()is None
assert out.stat().st_size<100*1024**2,'GitHub per-file size limit'
print('Verified offline ZIP:',out,round(out.stat().st_size/1024**2,1),'MiB')
