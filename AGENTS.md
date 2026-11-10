# AGENTS.md — 在本仓库工作的约定

## 项目是什么

一套面向单人自学的 **ARG / CTF / Puzzle Hunt** 课程，以 Hugo 静态站发布在 `ai.xcfx.com`。
仓库：`github.com/miaki03/aistudy-blog`（**不是** `miaki-blog`，那个是博主自己的博客，不要动）。

## 环境事实（省去重复勘探）

| 项 | 事实 |
| --- | --- |
| 宿主 | Windows 11，DSH 以 full-access 运行 |
| WSL | `Ubuntu-24.04`，用户 `miaki`，可通过 `wsl.exe -d Ubuntu-24.04 -e bash <脚本>` 调用 |
| Hugo | WSL 内 `v0.164.0 extended`（Windows 侧**没有** hugo） |
| Node | Windows 侧 v24；WSL 内没有 node |
| GitHub | 只有 SSH 密钥，**没有 gh、没有 API token，无法新建仓库** |
| SSH | 22 端口不通，必须走 `ssh.github.com:443`；包装脚本在 `~/.git-ssh-443.sh`，用 `GIT_SSH` 指向它 |
| 代理 | `HTTPS_PROXY=http://127.0.0.1:7890`；`api.github.com` 直连可能被限流 |
| 仓库工作副本 | `F:\vibecoding\learning-path-site` |

## 命令

```bash
# 构建（发布用，忽略草稿）
hugo --gc --minify

# 本地预览（包含草稿）
hugo -D --gc --minify

# 题目库校验（必须通过才能提交）
python3 scripts/check-kb.py
```

## 每轮工作协议（不要跳步）

1. 读 `docs/06-progress.md` 的「下一步」，再读 `docs/03-backlog.md` 顶部；
2. 只领取**一项**任务，不要顺手改别的；
3. 改完跑 `python3 scripts/check-kb.py`，失败就修到通过；
4. 更新 `docs/06-progress.md`（做了什么、下一步）；
5. 一项任务一次提交，提交信息用 `feat:` / `docs:` / `fix:` 前缀并写明章节 ID。

## 目录约定

```
content/skill/     技能页（补给站），URL /s/<slug>/
content/project/   项目页，URL /proj/<slug>/
content/post/      旧版 8 篇模块导语（legacy，暂不改）
content/page/      关于、免责声明
kb/                题目库 problems.json + 说明
scripts/           校验脚本
docs/              项目文档（不被 Hugo 构建）
```

## 禁区

- 不改 `hugo.toml` 里的 `baseURL`，除非用户明确指定域名；
- 不改 `themes/hugo-theme-stack` 子模块指向（当前锁定 `2f8b1be`，与用户博客一致）；
- 不转载各 Puzzle Hunt / CTF 的题面原文，只链接 + 自写解法；
- 不新增 JS 依赖或前端框架；
- 不把 `public/`、`resources/_gen/` 提交进仓库（已在 `.gitignore`）；
- 不碰 `F:\vibecoding\miaki-blog`（那是另一个仓库）。

## 已定风格（详见 docs/02-style-guide.md）

**保姆级、原理优先、禁用比喻。** 不假设读者会去搜索；每个术语首次出现时当场定义。
