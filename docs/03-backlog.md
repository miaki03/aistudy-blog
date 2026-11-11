# 当前批次

> 只记「现在要做的一批」。完整计划在 `07-syllabus.md`，工作流在 `08-chapter-pipeline.md`。

## 当前：Part 0 · 基座（5 章 22 节）

| 章 | 节 | 状态 |
| --- | --- | --- |
| U00 数据在机器里的样子 | 4 | ✅ 已上线，8 题 |
| U01 终端 | 5 | ✅ 已上线，8 题 |
| U02 Python 最小可用 | 5 | ✅ 已上线，9 题 |
| U03 Python 与字节 | 4 | **下一个** |
| U04 位运算与掩码 | 4 | todo |
| P1 侦察报告 | — | todo（有草稿，待改引用贯穿样本） |

### U03 的节表（已定，可直接开工）

| 节 | 跑通物 | 题 |
| --- | --- | --- |
| 3.1 `str` 与 `bytes` 是两种东西 | `"abc".encode()` → `b'abc'`；`"你好".encode()` → `b'\xe4\xbd\xa0\xe5\xa5\xbd'` | U03.1-01 |
| 3.2 编解码失败与 `errors` | `b'\xff'.decode()` 抛 `UnicodeDecodeError`；`errors="replace"` 得 `\ufffd` | U03.2-01 |
| 3.3 字节与整数互转 | `int.from_bytes` / `to_bytes`；从 S-01 的 IHDR 取宽高 | U03.3-01 |
| 3.4 读二进制文件 | `open(p,"rb")`；在 S-04 里找 gzip 偏移 32 | U03.4-01 |

## 紧接着

- B-01 U03（4 节）
- B-02 U04（4 节）→ Part 0 收尾 → 入口自测 → 第一次 Part 级评审
- B-03 U12 补到 4 节后上线；U10 补节末速查
- B-04 P1 改成引用贯穿样本

## Part 0 收尾后

第一次 Part 级评审（用 `05-qa.md` 的 7 类清单），通过则推送并宣布 Part 0 完成。

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
- [x] **U01 全章**（5 节 + 自检 3 + 动手 1，8 题）+ 教学用访问日志
- [x] 上线 U00 / U01 / U10 三篇
- [x] `scripts/selftest.py` + 5 道入口自测（改作 U04 出口检查）

## 已知问题

| 问题 | 影响 | 处理 |
| --- | --- | --- |
| `baseURL` 仍是占位 | canonical 指向错误 | 等用户确认域名 |
| 旧 8 篇无 `chapter`/`stage` | 不进课程地图 | 校验已对 post 豁免 |
| 现有两页未按 v4 节结构改造 | 与后续章格式不一致 | B-04 |
| 技能页全 `draft = true` | 线上看不到 | 用户逐章确认后改 |
