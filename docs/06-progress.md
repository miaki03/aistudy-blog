# 进度日志

> 新会话从这里开始读。只写「当前状态」，历史细节在 git log 与 `04-decisions.md`。

## 当前状态（2026-11-10）

**仓库**：`github.com/miaki03/aistudy-blog`，分支 `main`，最新提交见 `git log -1`。
**线上**：`https://ai.xcfx.com`（Cloudflare Pages，Git 集成，push 自动构建）与 `https://miaki.pages.dev`。
**线上内容**：只有旧版 8 篇模块导语；所有新技能页/项目页都是 `draft = true`，**线上看不到**。

## 已完成

1. 站点从个人博客拆出为独立仓库，主题子模块锁在 `2f8b1be`。
2. 8 篇旧文迁移，路径 `/p/<slug>/`。
3. 题目库与校验：`kb/problems.json`（14 条）+ `scripts/check-kb.py`。
4. 样章三页（草稿）：
   - `S-B64` Base64 家族（按保姆级重写：前置四概念、字母表、四个手算示例含反方向、长度公式、一键试四种的脚本）
   - `S-FILE` 文件头与 magic bytes（已按新风格校准：补前置概念、去比喻）
   - `P1` 编码与文件侦察报告
5. 项目文档：`AGENTS.md`、`docs/00`–`06`。

## 下一步（按优先级）

1. **B-02** 写 `S-BIN`（位/字节/十六进制/ASCII/位运算）——它是 S-B64 的前置，缺了会让 B64 页的「前置」指向空
2. **B-03** 写 `S-CLI`
3. **B-05** 实现 `claims` 机器校验
4. **B-06** 隐写四页

## 等用户确认的三件事

1. 域名：`baseURL` 仍是 `https://learning-path.pages.dev/`，需要改成 `https://ai.xcfx.com/` 才能让 canonical 正确。
2. 发布：三页样章何时把 `draft` 改 `false`。
3. 是否实现 `claims` 机制（把知识性断言也纳入脚本校验）。

## 环境备忘

- `hugo` 只能在 WSL 里跑：`wsl.exe -d Ubuntu-24.04 -e bash <脚本>`
- 推代码必须走 443：`GIT_SSH=$HOME/.git-ssh-443.sh`
- 不能新建 GitHub 仓库（无 gh、无 token）
- 没有 `zip`、`binwalk`；Python 3.12 有 `tomllib`
