# Mac正式应用：Supabase + Vercel

目标为真实在线账号与同步，不使用本地预览邮箱或模拟云端数据。保留原刷题版，独立分支noix-delf-b2-mac。

## 当前准备内容

- Mac Electron桌面入口：隔离网页与系统能力，禁止任意导航和Node注入。
- Intel和Apple Silicon两类DMG/ZIP的macOS构建流程。
- 应用壳版本更新的下载与安装流程；网页功能及题库更新由Vercel部署和现有版本提示管理。

## 尚未完成的上线前提

1. 在当前对话连接Supabase与Vercel，不能只在其网站登录。
2. 选择或创建Supabase项目，将原SQLite账户系统迁移到Supabase Auth/Postgres，并设置兑换码和用户进度的权限策略。
3. 在Vercel部署支持Supabase的服务；原SQLite服务不能原封不动放入Vercel函数中持久运行。
4. 在Supabase配置真实发信服务，验证注册、重设密码和确认链接；所有密钥只保存到服务端环境配置。
5. 为Mac签名和Apple公证配置Developer ID Application证书与Apple开发者凭据。不要把证书私钥或口令发到聊天或提交GitHub。缺少这些配置时构建会停止，不把未签名包称作正式可用安装包。
6. 部署地址确认后设置仓库变量NOIX_APP_URL，并在macOS Actions中构建签名安装包。签名、公证完成和真实账号/兑换码/两设备同步验证通过后，才发布正式下载链接。

本文件记录准备状态，不代表已部署、已连接云账号、已完成数据库迁移或已生成Mac安装包。
