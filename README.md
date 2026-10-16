# 胡桃法语 · DALF C1

## 下载后双击使用

下载 [离线网站压缩包](https://github.com/hakseup/wangzhan/raw/refs/heads/noix-dalf-c1/downloads/noix-dalf-c1-offline.zip)（约 88 MB），完整解压后，用电脑 Chrome 或 Edge 打开里面的 **胡桃法语-DALF-C1-双击打开.html**。无需安装 Node.js 或启动服务器，完整题库与 36 段音频均已嵌入。

GitHub 的 **Code → Download ZIP** 下载的是开发源码。源码根目录的 `index.html` 不能通过双击直接运行；若已下载源码压缩包，请进入其中的 `downloads` 文件夹，再解压 `noix-dalf-c1-offline.zip` 并打开里面的 HTML。

一个可独立部署的法语刷题网站。题库由本次上传的 PDF 和音频整理而成，按长听力、短听力、阅读、写作和口语导航，文章使用法语标题、中文释义与主题标签。考试场次仅作为详情页来源。

已收录全部 117 个附件：81 份 PDF、486 页材料、36 段音频，整理成 176 组练习、547 道交互题，另含 28 组写作和 85 组口语练习。两段只有音频、没有对应 PDF 的资料使用转写摘录和明确标记的补充理解题。

## 启动

需要 Node.js 20.19+ 或 22.12+（当前环境使用 Node.js 24）。

```bash
cd /workspace/wangzhan
npm ci
npm run dev -- --port 5173 --strictPort
```

生产版本：

```bash
npm run build
npm run preview -- --port 4173 --strictPort
```

部署时上传 `dist/` 到支持静态文件的网站托管服务即可。网站采用哈希路由，不需要服务端路由重写。必须同时上传 `content.json` 和 `audio/`，并使用 HTTP/HTTPS 访问，不能直接双击 `index.html`。当前源码与本地运行验证不等于已经部署到公网。

## 已实现

- 按题型、文章主题、法语或中文关键词筛选；收藏、练习记录、错题回顾。
- 独立音频播放器：播放、暂停、拖动、前后跳转 15 秒、0.5–2 倍速。
- PDF 正文提取为网页文字，不嵌入 PDF；法语原文和中文参考译文切换。
- 选择词句后高亮；再次点击可依次切换黄色、紫色、红色，第四次取消高亮。
- 单词与词句备注：红色加粗、悬停提示、独立单词笔记页。
- 每道题独立选择或输入；保留未作答、正确、错误、待自评四种状态。
- 写作原题或明确标注的补充指令在上，下面是输入区；分别保存综合写作和议论文草稿，统计法语词数。
- 85 个口语题目按主题分类，提供法中题目、原文材料、表达提纲和自检清单。
- 计时器、字号调节、移动端导航，以及学习数据 JSON 导出和导入。

## 答案与翻译的边界

客观选择题依据整理后的答案自动核对。填空接受列明的标准表达和精确匹配；不同表述的开放回答留待对照参考要点自评，不采用简单关键词相似度强行判错。判断题可核对判断选项，引用依据需要自评。写作和口语提供草稿、自检与保存，不声称提供 AI 或官方评分。

题目与参考要点已按原资料和正文整理。扫描件可能有水印遮挡或识别误差。没有原题、仅有文章的资料，所补充的理解题明确标注为“补充理解练习”。中文正文由本地 Argos 模型通过法语→英语→中文生成，页面标明“机器参考译文”；术语、细节及标准表述以法语原文和原始材料为准。

## 数据和隐私

应用运行不需要 API 密钥、数据库、登录或外部翻译服务。练习、草稿、收藏和标注仅写入当前浏览器的 `localStorage`。换设备前请导出学习备份；清理浏览器数据会移除本地记录。题库正文和音频属于网站静态资源，不随学习备份重复导出。

## 检查

```bash
npm test
npm run build
python3 tests/browser_smoke.py
```

浏览器检查需要运行中的开发服务器、Python Playwright 和 Chromium。可通过 `NOIX_TEST_URL` 指向生产预览服务器。

## 内容维护

- `public/content.json`：网站实际使用的题库与参考译文。
- `public/audio/`：用户上传的原始音频；未转码改变音质。
- `data/overrides.json`：逐题整理的题干、选项与参考要点。
- `data/translations.json`：以原段落 SHA-256 为键的中文机器参考译文。
- `scripts/catalog.py`：双语标题与主题分类。
- `scripts/extract.py`、`questions_ocr.py`、`materials_ocr.py`：PDF 文字层修复与 OCR。
- `scripts/curate*.py`、`build_content.py`：题卡整理与静态题库构建。
- `scripts/translate.py`：可选的本地参考翻译脚本，应用启动和构建不依赖此步骤。

PDF 原件在当前工作区的 `/workspace/attachments`，不会被复制到网站或部署产物。重新导入原始 PDF 需 Python 的 PyMuPDF、Pillow、NumPy、Tesseract 与法语语言数据。日常开发、启动和部署直接使用已生成的题库，不需要重新运行 OCR 或下载语言模型。

完整源码已提交到 GitHub 仓库 `hakseup/wangzhan` 的 `noix-dalf-c1` 分支。网站尚未部署到公网。在 Netlify 导入该仓库并选择 `noix-dalf-c1` 分支；仓库中的 `netlify.toml` 已配置构建命令 `npm run build`、发布目录 `dist` 和 Node.js 22。

## 双击打开的离线版本

运行 `npm run build` 后执行 `python3 scripts/package_standalone.py`，会生成 `../wangzhan-release/胡桃法语-DALF-C1-双击打开.html`。它将样式、程序、完整题库和 36 段音频嵌入同一个文件，可用桌面 Chrome 或 Edge 直接打开，无需解压、联网或启动服务器。文件约 121 MB，首次打开需要稍等。浏览器学习记录与线上版本分别存储，换版本前请导出备份。
