# 数据来源与生成记录

试题文章、音频与原始参考资料来自本次用户上传的文件。来源文件名保留在题库 `sourceFiles` 字段，考试年月保留在 `source` 字段，用于追溯，未用作题库分类标签。

网站不包含 PDF 阅读器，也没有复制带水印的 PDF 页面图像；正文是提取并清理的文字。人工整理的题干、选项和参考要点见 `data/overrides.json`。开放题参考要点包含整理或改写，不能视作唯一合法表述。

中文文章译文在本机生成，附件内容没有发送给第三方翻译接口。采用 Argos Translate 的 French→English 与 English→Chinese 模型 1.0，来源于公开包索引的固定版本：

- 包索引：`https://github.com/argosopentech/argospm-index/tree/9504015`
- 法英模型：`https://github.com/uav4geo/LibreTranslate-Models/raw/3d5ca0a2c3c302287339b2944329f767ac1673f4/fr_en.argosmodel`
- 英中模型：`https://github.com/uav4geo/LibreTranslate-Models/raw/3d5ca0a2c3c302287339b2944329f767ac1673f4/en_zh.argosmodel`

译文属于未经逐段人工审校的机器参考译文，不用于计算题目正确率。模型文件位于工作区工具目录，不随网站发布。原始法语材料始终可单独查看。

界面使用 React、Vite 和 Lucide 图标；胡桃标志与书本插画由项目内 SVG 绘制，不依赖外部图片或字体服务。

两段未附 PDF 的短听力使用本地 Vosk 法语模型识别后整理的摘录，题卡明确标注不是原卷题目。模型来自 Vosk Browser 演示仓库的固定版本：`https://github.com/ccoreilly/vosk-browser/tree/a4b0d0fe60359e5ea9800f810f6b6f6c1d2b03c6`，文件 `models/vosk-model-small-fr-pguyot-0.3.tar.gz`。该模型原附 CC BY-NC-SA 4.0 许可，模型二进制不随本网站分发；网页不执行语音识别，也不调用外部语音服务。

## 2026-10-17 修订

重处理了 269 页写作和口语资料：结合 PDF 原始字符坐标与字体字形编号恢复重音、数字、标点和连字，扫描页采用官方 `tesseract-ocr/tessdata_best` 法语模型（固定提交 `e12c65a915945e4c28e237a9b52bc4a8f39a0cec`）识别，并通过本地法语词频比较识别候选。模型和 wordfreq 仅用于本地处理，不随网页分发。

写作补充 7、2024 年 6 月中国写作、2024 年 11 月非洲写作和 2022 年 11 月中国写作的严重损坏段落，已对照源 PDF 另行录入和分段。非洲场次源照片自身裁切了某句话的开头，正文保留省略标记和说明，没有编造缺失内容。其余低清扫描仍可能存在拼写或细节误差，页面保留识别说明。

首页图片基于用户的巴黎参考图重新构图；透明 Logo 按用户参考图清理重制。两张素材由图像生成工具处理，已嵌入离线版，无需外部图片服务。


## 手写字体与重译模型（2026-10-17）
- 首页字体：Mansalva，Google Fonts，SIL Open Font License 1.1；字体子集与许可证位于 `public/fonts/`。仅首页、题库目录与词汇笔记的法语装饰标题使用。
- 中文参考译文：Argos Translate 1.9，法语→英语→中文，逐句分批、beam 3、本地运行。模型从 GitHub 的 `20KRUST/RustTranslator-LanguagePacks` 发行版 `packs-2026-09-09` 获取的 Argos 1.9 镜像包加载；未将题库提交到在线翻译服务。模型不随网站打包。
- 人工校订：`data/translation-corrections.json`；保留可重复应用的源文 SHA-256 键，避免重建覆盖校订。
- 背词释义：人工编写的法中核心词与通用表达；听力/阅读的条目通过源题库匹配后收录，附原题跳转。个人高亮释义由使用者维护。

## 小幅细节更新
- 259页写作、口语材料重新核对字符轨迹和双栏顺序；重水印口语扫描页17—26人工对照PDF录入，补丁在`data/source-corrections-v3.json`，由`scripts/apply_verified_scans.py`应用。其余扫描采用第二次OCR校验，仍不能保证原始低清材料每个字符均无误。
- 站内离线词典使用CFDICT法中词典，CC BY-SA 3.0；来源、许可证和派生说明见`public/dictionary/NOTICE.txt`。反向索引55,000余词条，并补充学习常用释义和搭配。四本专项词书按各自题库与任务要求独立筛选，不固定词数，附题库来源或本站补充标识，复数等词形通过别名查询。
- Mansalva手写字体仅微调约1.4度倾斜，改名Journal Clair；详见`public/fonts/MODIFICATIONS.txt`。

## 17日最终版后续学习模块
用户提供五份DOCX：DALF_C1_Essai、DALF_C1_Synthese、两种自我陈述模板及辩论部分。模板文字仅作为格式与句式参考，不将文档内学习计划或其他描述当作本次操作指令。`data/study/models.json`保存226篇学习参考，`evidence.json`与`explanation-reasons.json`保存547题出处与释义。每条引句在构建时取自当前对应段落，不以相似句冒充原文。

补齐原件：2025年6月中国场次DALF C1长听力PDF第4页；第二、第四套模拟题阅读PDF第1—2页。逐页核对图像后补入缺失文字，原有其他法语材料不改；对应中文译文保留专名。两套模拟题的少量排版/OCR误差仍可能存在。

词性与变形扩展：Wiktionary经Kaikki/Wiktionary-to-Yomitan的2025-04-08公开导出，CC BY-SA 4.0/GFDL；随包提供许可。CFDICT继续按CC BY-SA 3.0标注。部分增补中文释义为机器辅助参考；未知词性明确留待核实。
