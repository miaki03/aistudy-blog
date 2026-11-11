# 课程状态表

> 计划在 `07-syllabus.md`，通用方法在 `PLAYBOOK.md`。本文档只记**当前完成度**。

## 已上线（draft = false）

| 章 | 页面 | 网址 | 规模 | 题 | 时长 |
| --- | --- | --- | --- | --- | --- |
| U00 | `content/skill/u00-data-in-machine.md` | `/s/u00-data-in-machine/` | 526 行 / 11737 字 | 8 | 80 |
| U01 | `content/skill/u01-terminal.md` | `/s/u01-terminal/` | 599 行 / 12520 字 | 8 | 140 |
| U02 | `content/skill/u02-python-min.md` | `/s/u02-python-min/` | 576 行 / 12197 字 | 9 | 140 |
| U03 | `content/skill/u03-python-bytes.md` | `/s/u03-python-bytes/` | 527 行 / 11328 字 | 8 | 120 |
| U10 | `content/skill/base64-family.md` | `/s/base64-family/` | 467 行 / 9298 字 | 5 | 70 |

五篇共 2695 行、47,080 字、38 道题（其中 31 道机器可验，`check.py` 全部实跑通过）。

**Part 0 已完成 4/5 章**，只差 U04 位运算。

## 草稿中（draft = true）

| 章 | 页面 | 缺口 |
| --- | --- | --- |
| U12 | `content/skill/file-magic.md` | 只有 2 节（应为 4），缺节末速查 |
| P1 | `content/project/p1-encoding-recon.md` | 用的是自造 6 样本，未接贯穿样本集 |

## 进行中

| 章 | 进度 |
| --- | --- |
| U04 位运算与掩码 | 未开始，节表已定 |

## 未开始

Part 1 起共 23 章。见 `07-syllabus.md` §6。

## 贯穿样本集

| 样本 | 状态 |
| --- | --- |
| S-01 … S-07 | ✅ `scripts/verify-corpus.py` 20 项断言全过 |
| u01-access.log | ✅ U01 专用，30 行，条数写死；U02 复用 |
| selftest/ ×5 | ✅ 入口自测，U04 收尾时用作出口检查 |

文件在 `static/samples/`，站点路径 `/samples/S-01.png`，由 `scripts/build-corpus.py` 确定性重建。

**已动用**：S-01（U00 头字节、U03 IHDR 宽高）、S-04（U00 file 骗局、U03 偏移与解压）、S-06（U01 strings 提取）。

## 工程

| 项 | 状态 |
| --- | --- |
| 题库 `kb/problems.json` | 47 条（机器可验 39 / 人工证据 8） |
| 概念台账 `kb/concepts.json` | 23 条 |
| `scripts/check.py` | 题目库 + 概念台账 + 复用门槛，全绿 |
| `specs/` | U00、U01、U02、U03 有节表与实测记录 |
| 发布构建 | `hugo --gc --minify` 32 页，`/s/` 五页可达 |

## 旧版 8 篇

`content/post/learning-path-*.md`，模块导语性质，不动。
