# 课程状态表

> 计划在 `07-syllabus.md`。本文档只记**当前完成度**，不记计划。

## 已完成

| 章 | 页面 | 状态 | 节 | 题 | 时长 |
| --- | --- | --- | --- | --- | --- |
| U00 | `content/skill/u00-data-in-machine.md` | draft | 4 + 自检 + 动手 | 8 | 80 |
| U10 | `content/skill/base64-family.md` | draft | 4（待补节末速查） | 5 | 70 |
| U12（部分） | `content/skill/file-magic.md` | draft | 2（待补） | 3 | 40 |
| P1 | `content/project/p1-encoding-recon.md` | draft | — | 6 | 170 |

> U10 与 U12 写于 v3，尚未按 v4 补「节末速查 / 章末术语表」，排在 U04 之后统一改造。

## 进行中

| 章 | 进度 |
| --- | --- |
| U01 终端 | 未开始 |

## 未开始

Part 0 其余 4 章 → Part 1 → … → Part 6，共 24 章未开。见 `07-syllabus.md` §6。

## 贯穿样本集

| 样本 | 状态 |
| --- | --- |
| S-01 … S-07 | ✅ 已生成，`scripts/verify-corpus.py` 20 项断言全过 |

文件在 `static/samples/`，站点路径 `/samples/S-01.png`，由 `scripts/build-corpus.py` 确定性重建。

## 概念台账

`kb/concepts.json` 已登记 10 个概念。`scripts/check.py` 会拦住「声明了未登记的概念」「台账说 A 章定义但 A 章没声明」两类漂移。

## 旧版 8 篇

`content/post/learning-path-*.md`，模块导语性质，不动。计划降级为「旧版归档」，不参与课程依赖。
