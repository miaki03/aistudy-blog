# 进度日志

> 新会话从这里开始读。只写「当前状态」，历史在 git log 与 `04-decisions.md`。

## 当前状态（2026-11-10）

**仓库**：`github.com/miaki03/aistudy-blog`，分支 `main`。
**线上**：`https://ai.xcfx.com`（Cloudflare Pages，push 自动构建）。
**线上内容**：只有旧版 8 篇；新课全部 `draft = true`，线上看不到。

## 大纲状态：v4 定稿

- 结构：7 个 Part / 26 章 / 103 节 / 8 项目
- 对标 C++ Primer：节为学习原子、章末术语表、表就地给、贯穿样本、两级练习、最小/完整两条路径
- 学时：最小路径 ≈45 h，完整路径 ≈67 h
- 详见 `07-syllabus.md`

## 已完成

1. 站点独立成仓库，主题子模块锁 `2f8b1be`。
2. 旧文 8 篇迁移到 `/p/<slug>/`。
3. **大纲 v4**（7 Part / 26 章 / 103 节 / 8 项目，对标 C++ Primer）+ **工作流 v3**（节为交付原子）。
4. **`docs/PLAYBOOK.md`**：学科无关的教材生产手册，可复刻到高数等主题。
5. **贯穿样本集 S-01…S-07** + `u01-access.log` + `selftest/`，`build-corpus.py` 确定性重建，`verify-corpus.py` 20 项断言全过。
6. **`kb/concepts.json`** 20 条 + **`scripts/check.py`**（题目库 / 概念台账 / 复用门槛）。
7. **Part 0 完成并上线**：U00（8 题）、U01（8 题）、U02（9 题）、U03（8 题）、U04（8 题）+ U10（5 题），共 46 题。评审见 `docs/reviews/P0.md`。
8. `scripts/selftest.py` + 5 道入口自测（待登记进题库，成为 Part 0 正式出口检查）。

## 下一步

1. **U12 补到 4 节并上线**（解锁 P1）
2. 5 道入口自测登记进题库
3. P1 改接贯穿样本
4. U11 表层编码；U10 补节末速查与题号重编

> **推送策略**：commit 密、push 稀。只在 Part 收尾 / 用户要求 / 修故障时推，避免耗掉 Cloudflare 构建额度。
> 上次推送 `59df372`（上线 U00/U01/U10）。此后 U02 起未推，等 Part 0 收尾一起推。

## 可复用的方法论文档

[`docs/PLAYBOOK.md`](PLAYBOOK.md) —— 学科无关的教材生产手册。换主题（高数、语言、乐理）时照它做，含 12 步复刻清单与学科适配表。

## 命令速查

```bash
python3 scripts/check.py            # 提交必跑
python3 scripts/build-corpus.py     # 重建贯穿样本
python3 scripts/verify-corpus.py    # 核对样本里藏的答案
hugo -D --gc --minify               # 含草稿构建
```

## 等用户确认

1. 域名：`baseURL` 仍是占位，需改成 `https://ai.xcfx.com/`。
2. 发布：样章何时 `draft = false`。
3. 最小路径（45 h）是否为第一目标。

## 环境备忘

- `hugo` 只能在 WSL：`wsl.exe -d Ubuntu-24.04 -e bash <脚本>`
- 推代码走 443：`GIT_SSH=$HOME/.git-ssh-443.sh`
- 不能新建 GitHub 仓库（无 gh、无 token）
- WSL 有 `gcc`、`xxd`、`file`、`python3`；没有 `zip`、`binwalk`、`node`
- Windows 侧有 node 24 / pnpm 11 / git 2.55，没有 hugo
