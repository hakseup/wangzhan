# 胡桃法语 B2：真实账号服务与 Mac 客户端

此分支 `noix-delf-b2-mac` 使用 Supabase 真实账号和私有存储；不包含付款功能。原 C1 项目不变。

## 已创建的服务

- Vercel 项目 `noix-delf-b2-mac`：Node 24，构建 `npm run build:cloud`，输出 `web-dist`。
- Supabase 项目 `dxjqnimxdcrzndpowbkl`，新加坡区域。
- 数据库已通过远程迁移应用 `schema.sql`（20261106100618）及 `admin-dashboard.sql`。不要把源 SQL 重复应用到已有项目。
- `import-assets` Edge Function 使用固定 Git 提交及 SHA256 清单导入资源。每个请求先验证用户与管理员权限；服务密钥只存在 Supabase 内部，不进入客户端或 Vercel。

## 首次正式使用前必须完成

1. Supabase → Authentication → URL Configuration：Site URL 设置为 `https://noix-delf-b2-mac.vercel.app`；Redirect URLs 增加 `https://noix-delf-b2-mac.vercel.app/`。
2. Authentication → Email → SMTP Settings 配置正式发信服务。默认发信仅可供组织成员测试，不能用于公开注册。保持邮箱确认开启。
3. 管理员使用 `meilinheyhey@outlook.com` 注册，验证真实邮件，并自行设置密码。没有预设管理员密码。
4. 登录后进入“管理后台”，点击“初始化／更新题库资源”，保持页面打开，等待全部私有文件导入。
5. 生成兑换码，使用另一真实邮箱验证注册、兑换和两设备同步，然后再分发安装包。

## 运行与保护

- BFF 在 HttpOnly、Secure、SameSite=Lax Cookie 中保存会话，调用 Supabase 用户身份接口验证。所有写操作检查相同 HTTPS Origin。
- 数据库 RLS、管理员白名单、单次兑换事务和进度版本比较共同限制访问。并发进度冲突要求用户选择版本。
- 题库文件仅以两分钟有效的私有存储链接下载；前端公共构建只包含页面、字体、图片和不含正文的目录。
- 消息与版本说明后台发布后每30秒及重新打开／恢复联网时检查。用户可以稍后更新。云端进度不依赖本机预览数据库。
- GitHub 原始附件历史已有公开副本；本分支的新服务保护不能撤回之前公开的下载。

## Mac 包

GitHub Actions `Build unsigned Mac app` 在 macOS runner 上构建两种架构的 DMG 和 ZIP。首次打开需在 macOS“系统设置 → 隐私与安全性”允许打开。未签名应用不执行自动替换安装；页面和题库功能由 HTTPS 服务更新，安装包本身更新时需重新下载。

Mac 客户端需要联网登录、兑换和同步。无服务地址或服务未配置完成时，安装包不能替代后端。`desktop/service.json` 只包含公开服务地址，无密钥。

开发验证：先 `npm run build:pwa`，再 `npm test`；正式 Vercel 构建使用 `npm run build:cloud`，不要将本地 `dist` 发布到公共托管。
