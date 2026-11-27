提供 Apple 芯片（arm64）和 Intel（x64）的 DMG 与 ZIP 安装包。DMG 打开后将应用拖入 Applications。

首次运行时，macOS 可能阻止未签名应用；请在“系统设置 → 隐私与安全性”中选择“仍要打开”。无需关闭系统安全保护。

应用连接真实 Supabase 账号与学习服务。网站地址：https://noix-delf-b2-mac.vercel.app/

首次对学生开放前，管理员仍需配置 Supabase 正式 SMTP 与验证邮件回跳地址、登录后台初始化私有题库文件，并验证真实注册／兑换／两设备同步。未完成这些步骤时不能当作已验收的正式服务分发。代码和部署说明见 noix-delf-b2-mac 分支 CLOUD-DEPLOYMENT.md。

页面和题库更新通过联网服务及应用内提示生效；未签名客户端本体更新需重新下载安装包。
