# 课程状态表

> 计划在 `07-syllabus.md`，通用方法在 `PLAYBOOK.md`。本文档只记**当前完成度**。

## 已上线（draft = false）

| 章 | 页面 | 网址 | 规模 | 题 | 时长 |
| --- | --- | --- | --- | --- | --- |
| U00 | `content/skill/u00-data-in-machine.md` | `/s/u00-data-in-machine/` | 526 行 / 11737 字 | 8 | 80 |
| U01 | `content/skill/u01-terminal.md` | `/s/u01-terminal/` | 599 行 / 12520 字 | 8 | 140 |
| U10 | `content/skill/base64-family.md` | `/s/base64-family/` | 467 行 / 9298 字 | 5 | 70 |

三篇都是草稿期被逐章核对过的，`check.py` 的 21 条 `verify` 全部实跑通过。

## 草稿中（draft = true）

| 章 | 页面 | 缺口 |
| --- | --- | --- |
| U12 | `content/skill/file-magic.md` | 只有 2 节（应为 4），缺节末速查 |
| P1 | `content/project/p1-encoding-recon.md` | 用的是自造 6 样本，未接贯穿样本集 |

## 进行中

| 章 | 进度 |
| --- | --- |
| U02 Python 最小可用 | 未开始 |

## 未开始

Part 0 剩余 2 章（U03、U04）→ Part 1 起共 23 章。见 `07-syllabus.md` §6。

## 贯穿样本集

| 样本 | 状态 |
| --- | --- |
| S-01 … S-07 | ✅ `scripts/verify-corpus.py` 20 项断言全过 |
| u01-access.log | ✅ U01 专用，30 行，条数写死 |
| selftest/ ×5 | ✅ 入口自测，改作 U04 出口检查 |

文件在 `static/samples/`，站点路径 `/samples/S-01.png`，由 `scripts/build-corpus.py` 确定性重建。

## 工程

| 项 | 状态 |
| --- | --- |
| 题库 `kb/problems.json` | 30 条（机器可验 24 / 人工证据 6） |
| 概念台账 `kb/concepts.json` | 14 条 |
| `scripts/check.py` | 题目库 + 概念台账 + 复用门槛，全绿 |
| `specs/` | U00、U01 有节表与实测记录 |
| 发布构建 | `hugo --gc --minify` 30 页，`/s/` 三页可达 |

## 旧版 8 篇

`content/post/learning-path-*.md`，模块导语性质，不动。
