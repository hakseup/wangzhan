# 数据来源与生成记录

试题文章、音频与原始参考资料来自本次用户上传的文件。来源文件名保留在题库 `sourceFiles` 字段，考试年月保留在 `source` 字段，用于追溯，未用作题库分类标签。

网站不包含 PDF 阅读器，也没有复制带水印的 PDF 页面图像；正文是提取并清理的文字。人工整理的题干、选项和参考要点见 `data/overrides.json`。开放题参考要点包含整理或改写，不能视作唯一合法表述。

中文文章译文在本机生成，附件内容没有发送给第三方翻译接口。当前译文使用本地French→English模型1.0与English→Chinese模型1.9，并结合拼写修复、专名词表和人工润色。原版使用的1.0模型来源保留如下：

- 包索引：`https://github.com/argosopentech/argospm-index/tree/9504015`
- 法英模型：`https://github.com/uav4geo/LibreTranslate-Models/raw/3d5ca0a2c3c302287339b2944329f767ac1673f4/fr_en.argosmodel`
- 英中模型：`https://github.com/uav4geo/LibreTranslate-Models/raw/3d5ca0a2c3c302287339b2944329f767ac1673f4/en_zh.argosmodel`

译文属于未经逐段人工审校的机器参考译文，不用于计算题目正确率。模型文件位于工作区工具目录，不随网站发布。原始法语材料始终可单独查看。

界面使用 React、Vite 和 Lucide 图标；胡桃标志与书本插画由项目内 SVG 绘制，不依赖外部图片或字体服务。

两段未附 PDF 的短听力使用本地 Vosk 法语模型识别后整理的摘录，题卡明确标注不是原卷题目。模型来自 Vosk Browser 演示仓库的固定版本：`https://github.com/ccoreilly/vosk-browser/tree/a4b0d0fe60359e5ea9800f810f6b6f6c1d2b03c6`，文件 `models/vosk-model-small-fr-pguyot-0.3.tar.gz`。该模型原附 CC BY-NC-SA 4.0 许可，模型二进制不随本网站分发；网页不执行语音识别，也不调用外部语音服务。


新增的英中1.9模型来自未修改的公开Argos语言包镜像：
`https://github.com/NicoriciN89/RimWorldModTranslator/releases/download/language-packs/translate-en_zh-1_9.zip`。

逐题释义为基于原材料编写的中文解释，证据句必须逐字存在于指定的法语段落中。`data/evidence-locations.json`记录核对的段落，`data/explanation-reasons.json`保存547条释义。补回了旧提取流程漏掉的阅读模拟题2、4正文、2025年6月长听力末页及一篇阅读的结尾。个别明确与正文不符的选项、参考答案同时修正；修订题目打开旧记录时会重新核对，原始作答保留。

范文依据用户上传的五份模板编写，属于练习示范，不是官方答案或官方评分。范文中的自拟情境用作论证例子，不伪装为材料中的统计研究。Synthèse仅综合相应材料，缺少独立Essai原题的素材组，题目和范文明确标记为补充练习。

547道题干与705个选择题选项已逐条重写中文译文，分别保存在`data/question-translations.tsv`和`data/option-translations.tsv`。文章译文已重新处理并重点润色，但不宣称所有机器译文均已逐段人工审校；扫描识别及机器翻译仍可能遗漏细节。人名、地名、书名、网站名称保留原文形式，专名变体另存于`data/name-variants.tsv`。文章的人工修订保存在`data/translation-edits.json`和`data/paragraph-translations.tsv`，便于继续校订。

## 站内词句查询数据

离线词库由Wiktionary中英文版经Kaikki与Wiktionary-to-Yomitan整理的数据生成，原始公开版本日期为2025-04-08。词条按词性保存，另索引变位、复数、阴阳性等词形及明确的派生关系。缺失的英文版释义和课文句子使用本机模型补译。人工整理的C1短语、词族和句子参考分别位于`data/dictionary/phrases.tsv`、`families.tsv`、`sentences-reviewed.tsv`。

数据以CC BY-SA 4.0提供；来源、变更及许可全文随发行版和单文件保留。详见`data/dictionary/NOTICE.md`与`CC-BY-SA-4.0.txt`。词性与词形资料不意味着机器补译达到专业辞书审校质量；未收录内容可按使用者开关在本页联网补充。
