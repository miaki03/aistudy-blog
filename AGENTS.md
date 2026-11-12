# AGENTS.md — 在本仓库工作的约定

## 项目是什么

一套面向单人自学的 **ARG / CTF / Puzzle Hunt** 课程，以 Hugo 静态站发布在 `ai.xcfx.com`。
仓库：`github.com/miaki03/aistudy-blog`（**不是** `miaki-blog`，那个是博主自己的博客，不要动）。

**方法论与流水线的学科无关版本在 [`docs/PLAYBOOK.md`](docs/PLAYBOOK.md)**：换成高数、语言、乐理等主题时照它做，本文件的仓库约定则按新仓库改。**它只给 agent 用，不进 Hugo 构建、不上线、不加导航。**
**课程总览与阅读顺序在 [`content/page/course.md`](content/page/course.md)（线上 `/course/`）**：加新章后要同步更新它，否则读者找不到。

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

# 提交前必跑：题目库 + 概念台账 + 复用门槛
python3 scripts/check.py

# 重建 / 核对着贯穿样本集
python3 scripts/build-corpus.py
python3 scripts/verify-corpus.py
```

## 每轮工作协议（不要跳步）

1. 读 `docs/06-progress.md` 的「下一步」，再读 `docs/03-backlog.md` 顶部；
2. 只领取**一项**任务，不要顺手改别的；
3. **章**为单位：3–5 个**节**，每节 15–25 分钟，四件套 = 跑通物 / 机制 / 速查 / 题；
4. 开写前先在 `specs/<章ID>.md` 出节表（每节的跑通物想不出来就说明这节不该存在）；**并读 `docs/10-reader-pitfalls.md` 的 12 条卡点规则**；
5. 改完跑 `python3 scripts/check.py`，失败修到通过；
6. **独立复验最多 3 轮**：第 3 轮仍有卡点即算通过，剩余卡点记进 `specs/<章ID>.md` 的「已知卡点」；
7. 更新 `docs/06-progress.md`（做了什么、下一步）；
8. 一项任务一次提交，提交信息用 `feat:` / `docs:` / `fix:` 前缀并写明章节 ID。

## 推送策略（部署有构建配额，必须遵守）

**commit 密，push 稀。**

- 本地按节/章提交；**攒够数篇可读文章即可推送**，不必等一个 Part 收尾；
- **绝不**把 `git commit` 和 `git push` 写进同一条命令；
- **push 前必须单独取得用户当次确认**。「用户批准了某项内容变更」≠「批准推送」，这是两个决定；
- 任何**改变线上可见内容**的动作（下线页面、改导航、改标题）都要单独确认；
- Cloudflare Pages 每次推送都触发一次构建，免费额度按次计，省下来留给真正要上线的更新；
- 推送前先在本地跑 `hugo -D --gc --minify`，**不要拿云端构建当调试手段**；
- 推送命令：`GIT_SSH=/home/miaki/.git-ssh-443.sh git push origin main`
  （**不要写 `$HOME`**：在 `wsl.exe -e bash -lc` 里它会被 Windows 的 `HOME` 污染成 `C:UsersMiaki`）

## 目录约定

```
content/skill/     技能章（URL /s/<slug>/）
content/project/   项目页（URL /proj/<slug>/）
content/post/      旧版 8 篇模块导语（legacy，暂不改）
content/page/      关于、免责声明
kb/problems.json   题目库
kb/concepts.json   概念台账（每个概念只能有一个首次定义章）
specs/             章的节表与实测记录（不进 Hugo）
static/samples/    贯穿样本集 S-01…S-07，站点路径 /samples/
scripts/           校验与生成脚本
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
