# 课程状态表

> 计划在 `07-syllabus.md`，通用方法在 `PLAYBOOK.md`。本文档只记**当前完成度**。

## 已上线（draft = false）

| 章 | 页面 | 网址 | 规模 | 题 | 时长 |
| --- | --- | --- | --- | --- | --- |
| U00 | `content/skill/u00-data-in-machine.md` | `/s/u00-data-in-machine/` | 526 行 / 11737 字 | 8 | 80 |
| U01 | `content/skill/u01-terminal.md` | `/s/u01-terminal/` | 599 行 / 12520 字 | 8 | 140 |
| U02 | `content/skill/u02-python-min.md` | `/s/u02-python-min/` | 576 行 / 12197 字 | 9 | 140 |
| U03 | `content/skill/u03-python-bytes.md` | `/s/u03-python-bytes/` | 527 行 / 11328 字 | 8 | 120 |
| U04 | `content/skill/u04-bits.md` | `/s/u04-bits/` | 526 行 / 10300 字 | 8 | 90 |
| U10 | `content/skill/base64-family.md` | `/s/base64-family/` | 467 行 / 9298 字 | 5 | 70 |
| U12 | `content/skill/file-magic.md` | `/s/file-magic/` | 579 行 / 13078 字 | 9 | 110 |

七篇共 3800 行、70,458 字、55 道题（其中 47 道机器可验，`check.py` 全部实跑通过）。

**Part 0 已完成（5/5 章）**，评审记录见 `docs/reviews/P0.md`。
**Part 1 完成 2/3 章**：U10、U12 已上线，差 U11 与项目页 P1。

## 草稿中（draft = true）

| 章 | 页面 | 缺口 |
| --- | --- | --- |
| P1 | `content/project/p1-encoding-recon.md` | 用的是自造 6 样本，未接贯穿样本集 |

## 进行中

| 章 | 进度 |
| --- | --- |
| U11 表层编码 | 未开始，Part 1 最后一章 |

## 未开始

Part 2 起共 21 章。见 `07-syllabus.md` §6。

## 贯穿样本集

| 样本 | 状态 |
| --- | --- |
| S-01 … S-07 | ✅ `scripts/verify-corpus.py` 20 项断言全过 |
| u01-access.log | ✅ U01 专用，30 行，条数写死；U02 复用 |
| selftest/ ×5 | ✅ 入口自测，U04 收尾时用作出口检查 |

文件在 `static/samples/`，站点路径 `/samples/S-01.png`，由 `scripts/build-corpus.py` 确定性重建。

**已动用**：S-01（U00 头字节、U03 宽高、U04 LSB、U12 反例）、S-02（U12 CRC）、S-03（U12 伪加密 + 尾部）、S-04（U00、U03、U12）、S-06（U01 strings）。S-05、S-07 待 Part 2/3。

## 工程

| 项 | 状态 |
| --- | --- |
| 题库 `kb/problems.json` | 61 条（机器可验 52 / 人工证据 9） |
| 概念台账 `kb/concepts.json` | 28 条 |
| `scripts/check.py` | 题目库 + 概念台账 + 复用门槛，全绿 |
| `specs/` | U00–U04、U12 六章有节表与实测记录 |
| `docs/reviews/` | P0 评审记录 |
| 发布构建 | `hugo --gc --minify` 35 页，`/s/` 七页可达 |

## 旧版 8 篇

`content/post/learning-path-*.md`，模块导语性质，不动。
