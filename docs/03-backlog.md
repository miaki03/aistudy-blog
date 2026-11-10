# 当前批次

> 只记「现在要做的一批」。完整计划在 `07-syllabus.md`，工作流在 `08-chapter-pipeline.md`。

## 当前：Part 0 · 基座（5 章 22 节）

| 章 | 节 | 状态 |
| --- | --- | --- |
| U00 数据在机器里的样子 | 4 | ✅ 完成，8 题，`check.py` 绿 |
| U01 终端 | 5 | **下一个** |
| U02 Python 最小可用 | 5 | todo |
| U03 Python 与字节 | 4 | todo |
| U04 位运算与掩码 | 4 | todo |
| P1 侦察报告 | — | todo（有草稿，待改引用贯穿样本） |

### U01 的节表（已定，可直接开工）

| 节 | 跑通物 | 题 |
| --- | --- | --- |
| 1.1 路径与查看 | `ls -l`、`head -3`、`wc -l` | U01.1-01 |
| 1.2 管道与重定向 | `grep x f \| wc -l`、`cmd > out.txt` | U01.2-01 |
| 1.3 sort / uniq / wc | 统计一组重复行的出现次数 | U01.3-01 |
| 1.4 cut / tr / sed | 从一行日志里取出 IP 字段 | U01.4-01 |
| 1.5 组合成一行 | 「日志里出现最多的 IP」一整条命令 | U01.5-01 |

## 紧接着

- B-01 U01（5 节）
- B-02 U02 / U03 / U04
- B-03 按 v4 改造 `base64-family.md` 与 `file-magic.md`（节末速查、章末术语表、`<章>.<节>-<序号>` 题号）
- B-04 P1 改成引用贯穿样本（现在用的是自造 6 样本）

## Part 1 之后

见 `07-syllabus.md` §6，不在此展开。

## 已完成

- [x] 站点独立成 `aistudy-blog`
- [x] 8 篇旧文迁移
- [x] `kb/problems.json` + `check-kb.py`
- [x] 样章三页（U10 / U12 部分 / P1）
- [x] 大纲 v4（对标 C++ Primer，三层结构）
- [x] 工作流 v3（节为交付原子）
- [x] 贯穿样本集 S-01…S-07 + `build-corpus.py` + `verify-corpus.py`（20 项断言全过）
- [x] `kb/concepts.json` + `scripts/check.py`（概念台账、复用门槛）
- [x] **U00 全章**（4 节 + 自检 3 + 动手 1，8 题）
- [x] `scripts/selftest.py` + 5 道入口自测（改作 U04 出口检查）

## 已知问题

| 问题 | 影响 | 处理 |
| --- | --- | --- |
| `baseURL` 仍是占位 | canonical 指向错误 | 等用户确认域名 |
| 旧 8 篇无 `chapter`/`stage` | 不进课程地图 | 校验已对 post 豁免 |
| 现有两页未按 v4 节结构改造 | 与后续章格式不一致 | B-04 |
| 技能页全 `draft = true` | 线上看不到 | 用户逐章确认后改 |
