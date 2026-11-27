# 胡桃法语 · Noix le français

胡桃法语的完整网站：首页门户 + 系统学习 + 阅读精听 + 题库练习 + 找老师。
题库练习板块包含两套完整题库，原样迁入：

| 题库 | 来源分支 / 提交 | 组数 | 访问方式 |
| --- | --- | ---: | --- |
| DELF B2 | `noix-delf-b2-mac` @ `5c75025`（2026-11-06） | 313 | 兑换码开通，账号云端同步 |
| DALF C1 | `noix-dalf-c1` @ `3b33a81`（2026-11-24 星期二更新版） | 252 | 开放使用，登录后自动备份 |

题库正文、音频、PDF、词典、译文修订及所有数据整理记录都是逐字节复制，没有改动。

## 目录

```
index.html, src/          门户（首页、系统学习、阅读精听、题库练习、找老师、账号）
src/site.js               门户里可编辑的文字与占位内容（sample: true 为待替换的示例）
public/                   门户的字体、图片
apps/b2/                  DELF B2 完整应用（原分支文件树），站点路径 /b2/
apps/c1/                  DALF C1 完整应用（原分支文件树），站点路径 /c1/
api/handler.mjs           Vercel 后端（原 B2 后台：登录、兑换码、管理后台、消息、云端进度）
cloud/supabase.mjs        Supabase 网关（只用登录用户的 JWT，不含 service_role）
supabase/                 数据库结构与迁移；multi-bank-progress.sql 为本次新增
desktop/, .github/        原 B2 的 Mac 客户端与工作流
scripts/build.mjs         一次构建三个前端 → web-dist/
scripts/preview.mjs       本地预览（模拟账号，不连 Supabase）
```

## 后台与登录（沿用原 B2 后台）

- 账号仍是原 Supabase 项目 `dxjqnimxdcrzndpowbkl` 的邮箱 + 密码账号，需要邮箱验证；管理员仍是 `meilinheyhey@outlook.com`。
- 原有的用户、兑换码、开通记录、消息、版本说明、B2 学习进度（`noix_progress`）以及私有存储桶 `noix-private` 中的 B2 文件都不动，新网站直接接着用。
- 在门户右上角登录后，进入 B2 和 C1 都是同一个账号（同域 HttpOnly Cookie）。
- 管理后台：管理员登录后，从门户「我的学习账号 → 管理后台」打开（即 `/b2/?panel=admin`），功能与原来相同。
- C1 原先登录的是另一个托管服务（`/api/auth/*`），现在改为统一账号。C1 的学习记录单独存放在新表 `noix_bank_progress`，与 B2 进度互不覆盖。

## 部署（Vercel）

1. 在 Vercel 导入本仓库，Framework 选 Other；`vercel.json` 已配置构建命令 `npm run build` 与输出目录 `web-dist`。
2. 环境变量：`SUPABASE_URL`、`SUPABASE_PUBLISHABLE_KEY`（与原 `noix-delf-b2-mac` 项目相同，见 `.env.example`）。
3. **在 Supabase SQL Editor 执行一次 `supabase/multi-bank-progress.sql`**（只新增表和函数，可重复执行）。不执行时 B2 不受影响，C1 登录后云端备份会提示待同步，本机记录照常保存。
4. Supabase → Authentication → URL Configuration：把新域名加入 Site URL / Redirect URLs（验证邮件会回到门户首页 `/`，门户会自动完成验证）。
5. SMTP 发信仍需按原 `apps/b2/CLOUD-DEPLOYMENT.md` 配置后才能公开注册。

B2 的受保护文件仍走根路径 `/content.json`、`/audio/…`、`/pdfs/…`、`/dictionary/…`，由后端核对兑换权限后签名跳转到 Supabase 私有存储，所以已导入的文件不用重新上传。构建会检查这些文件没有混进公开目录。C1 题库和以前一样是公开静态文件，位于 `/c1/`。

## 本地开发

```bash
npm ci
npm run build
npm run preview        # http://localhost:4173 ，账号为本地模拟：任意邮箱 + 10 位以上密码
npm run dev            # 只调门户页面（vite）
npm test               # 后端接口 + B2 + C1 测试
```

`apps/b2/tests/platform-server.test.js` 测的是 B2 旧的自托管 SQLite 服务器（`apps/b2/server`），在原 `noix-delf-b2-mac` 分支上就已失败。线上（Vercel + Supabase）不使用该服务器。

## 之后填充内容

门户其他板块目前只做了版式。编辑 `src/site.js` 即可替换今日推送、新闻、课程、词汇单元、文章、听写和老师；把对应条目的 `sample: true` 去掉，「示例 / 版式占位」标记就会消失。题库练习板块里的数字来自真实题库，构建时自动统计（`src/bank-stats.json`）。

各题库自己的说明见 `apps/b2/README.md`、`apps/c1/README.md`。C1 原分支的离线压缩包与口语、听力 PDF 原样保存在 `apps/c1/downloads/`（不在网站上公开提供）。
