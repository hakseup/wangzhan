# 胡桃法语 B2：真实账号服务与 Mac 客户端

此分支 `noix-delf-b2-mac` 使用 Supabase 真实账号和私有存储；不包含付款功能。原 C1 项目不变。

## 已创建的服务

- Vercel 项目 `noix-delf-b2-mac`：Node 24，构建 `npm run build:cloud`，输出 `web-dist`。
- Supabase 项目 `dxjqnimxdcrzndpowbkl`，新加坡区域。
- 数据库已通过远程迁移应用 `schema.sql`（20261106100618）及 `admin-dashboard.sql`。不要把源 SQL 重复应用到已有项目。
- `import-assets` Edge Function 使用固定 Git 提交及 SHA256 清单导入资源。每个请求先验证用户与管理员权限；服务密钥只存在 Supabase 内部，不进入客户端或 Vercel。

## 本次部署验证（2026-11-06）

- 正式地址：https://noix-delf-b2-mac.vercel.app/
- 部署 `dpl_H6bvzgJ6QXsEMnmBQw8eTfGuG11n`，代码 `07402292b142633c12ae0041b96677372543ca48`，状态 READY。
- 30项本地自动测试通过，另通过真实线上匿名检查：首页、目录、Supabase消息、未登录私有文件HEAD阻断和CSRF检查。线上检查：https://github.com/hakseup/wangzhan/actions/runs/42202098147
- Supabase安全顾问无告警；5个业务表启用RLS，anon无权限执行题库RPC，存储桶为私有。
- Mac两架构DMG/ZIP构建成功：https://github.com/hakseup/wangzhan/actions/runs/42201676260
- 长期下载：https://github.com/hakseup/wangzhan/releases/tag/b2-mac-1.0.0-unsigned
- 待验证：真实邮件注册、管理员登录与资源导入、学生兑换、两台真实设备同步。尚未配置SMTP，不能声称公开注册已经可用。
- 此次使用连接器手动发布。后续要随Git推送自动部署，请在Vercel项目Settings → Git连接 `hakseup/wangzhan` 并将Production Branch明确设置为 `noix-delf-b2-mac`；不可使用C1分支。

## 首次正式使用前必须完成

1. Supabase → Authentication → URL Configuration：Site URL 设置为 `https://noix-delf-b2-mac.vercel.app`；Redirect URLs 增加 `https://noix-delf-b2-mac.vercel.app/`。
2. Authentication → Email → SMTP Settings 配置正式发信服务。默认发信仅可供组织成员测试，不能用于公开注册。保持邮箱确认开启。
3. 管理员使用 `meilinheyhey@outlook.com` 注册，验证真实邮件，并自行设置密码。没有预设管理员密码。
4. 管理员首次登录后会自动检查并导入缺失的私有文件。正文先就绪，其余音频与PDF继续导入；保持页面打开，失败时点击“继续初始化”。后台仍保留手动更新入口。
5. 生成兑换码，使用另一真实邮箱验证注册、兑换和两设备同步，然后再分发安装包。

## 运行与保护

2026-11-06 更新：PDF页仅锁定题目列表，考频表只禁用下载；词书保留标题、模式和搜索，仅锁定单词列表。公开目录只增加场次和词书数量，私有正文仍由后端保护。题卡底部显示考频资料中的全部已知月份。

云端同步改为首次登录即建立账号快照，之后自动保存完整学习状态；包括作答、草稿、练习结果、收藏、标注、背词计划、个人释义、范文编辑、自检及字体设置。读取与保存只要求已验证账号，兑换权限继续限制题库文件。离线内容放入该账号独立的待同步缓存，重新联网／恢复窗口焦点后重试；并发冲突保留两份快照，要求选择。清空／导入的确认文案明确说明会同步到账号。

验证覆盖40项自动测试及两个隔离浏览器环境下的草稿和收藏往返恢复。浏览器集成测试使用测试后端；不等同于用户真实账号已完成写入。真实账号应在新版登录后出现“云端已同步”，再核对Supabase记录版本和更新时间；不读取或输出用户草稿正文来做验收。

- BFF 在 HttpOnly、Secure、SameSite=Lax Cookie 中保存会话，调用 Supabase 用户身份接口验证。所有写操作检查相同 HTTPS Origin。
- 数据库 RLS、管理员白名单、单次兑换事务和进度版本比较共同限制访问。并发进度冲突要求用户选择版本。
- 题库文件仅以两分钟有效的私有存储链接下载；前端公共构建只包含页面、字体、图片和不含正文的目录。
- 消息与版本说明后台发布后每30秒及重新打开／恢复联网时检查。用户可以稍后更新。云端进度不依赖本机预览数据库。
- GitHub 原始附件历史已有公开副本；本分支的新服务保护不能撤回之前公开的下载。

## Mac 包

GitHub Actions `Build unsigned Mac app` 在 macOS runner 上构建两种架构的 DMG 和 ZIP。首次打开需在 macOS“系统设置 → 隐私与安全性”允许打开。未签名应用不执行自动替换安装；页面和题库功能由 HTTPS 服务更新，安装包本身更新时需重新下载。

Mac 客户端需要联网登录、兑换和同步。无服务地址或服务未配置完成时，安装包不能替代后端。`desktop/service.json` 只包含公开服务地址，无密钥。

开发验证：先 `npm run build:pwa`，再 `npm test`；正式 Vercel 构建使用 `npm run build:cloud`，不要将本地 `dist` 发布到公共托管。
