# 课程地图

## 两层结构

- **技能页**（`content/skill/`，URL `/s/<slug>/`）：一个能力点一页，自带练习。
- **项目页**（`content/project/`，URL `/proj/<slug>/`）：串起若干技能页，交付一份成品。

学习顺序 = 按 `prereq` 依赖走技能页，完成一组后进入项目页检验。

## 已完成

| ID | 页面 | 标题 | 状态 | 题数 | 时长 |
| --- | --- | --- | --- | --- | --- |
| S-B64 | `content/skill/base64-family.md` | Base64 家族：原理、手算与排错 | draft | 5 | 70min |
| S-FILE | `content/skill/file-magic.md` | 文件头与 magic bytes | draft | 3 | 40min |
| P1 | `content/project/p1-encoding-recon.md` | 项目 P1 · 编码与文件侦察报告 | draft | 6 | 120min |

## 旧版 8 篇（legacy）

`content/post/learning-path-*.md`：模块导语性质，暂不改动。后续可拆解为技能页，或降级为「模块首页」。

## 计划中的技能页（按依赖分层）

### 第 1 层 · 底座（无前置）

| ID | 主题 | 依赖 | 状态 |
| --- | --- | --- | --- |
| S-CLI | 命令行：文件、管道、重定向 | 无 | todo |
| S-PY | Python 够用版：bytes / 文件 / 循环 / 库 | 无 | todo |
| S-BIN | 位、字节、十六进制、ASCII、位运算 | 无 | todo |

### 第 2 层 · 编码与文件

| ID | 主题 | 依赖 | 状态 |
| --- | --- | --- | --- |
| S-B64 | Base64 家族 | S-BIN | done |
| S-FILE | 文件头与 magic bytes | S-CLI | done |
| S-URL | URL / HTML 实体 / 转义 | S-B64 | todo |
| S-MORSE | 摩斯 / 培根 / 二进制编码 | S-BIN | todo |
| S-UNICODE | Unicode 与同形字 | S-B64 | todo |

### 第 3 层 · 隐写与取证

| ID | 主题 | 依赖 | 状态 |
| --- | --- | --- | --- |
| S-LSB | 图片最低有效位 | S-PY, S-FILE | todo |
| S-META | 元数据与通道 | S-FILE | todo |
| S-AUDIO | 音频频谱与波形 | S-PY | todo |
| S-ZIP | 压缩包异常（伪加密、CRC、附加） | S-FILE | todo |
| S-PCAP | 流量包基础与 Wireshark 过滤 | S-CLI | todo |

### 第 4 层 · 密码

| ID | 主题 | 依赖 | 状态 |
| --- | --- | --- | --- |
| S-CLASSIC | 单表替换、词频、凯撒、维吉尼亚 | S-BIN | todo |
| S-TRANSPOSE | 换位类（栅栏、列换位） | S-BIN | todo |
| S-RSA | RSA 识别与入门攻击 | S-BIN, S-PY | todo |

### 第 5 层 · 结构（Puzzle Hunt）

| ID | 主题 | 依赖 | 状态 |
| --- | --- | --- | --- |
| S-PH-TYPE | 题型识别与题面结构 | S-B64 | todo |
| S-PH-EXTRACT | 提取法 12 种与触发信号 | S-PH-TYPE | todo |
| S-PH-META | meta 结构与答案格式 | S-PH-EXTRACT | todo |

### 第 6 层 · 检索与 ARG

| ID | 主题 | 依赖 | 状态 |
| --- | --- | --- | --- |
| S-OSINT | 搜索操作符、图片反查、地理定位 | 无 | todo |
| S-WEB | HTTP 头、Cookie、编码绕过 | S-CLI | todo |
| S-ARG-TRAIL | 线索链与兔子洞结构 | S-PH-META | todo |
| S-ARG-MEDIA | 跨媒介提取（频谱/条码/网页） | S-AUDIO, S-LSB | todo |

## 项目线

| ID | 项目 | 依赖技能 | 状态 |
| --- | --- | --- | --- |
| P1 | 编码与文件侦察报告 | S-B64, S-FILE | draft |
| P2 | 隐写与取证样本分析 | S-LSB, S-META, S-AUDIO, S-ZIP | todo |
| P3 | 单人 Puzzle Hunt 档案 | S-PH-EXTRACT, S-PH-META | todo |
| P4 | 迷你 ARG 自建 | S-ARG-TRAIL, S-ARG-MEDIA | todo |
| P5 | solo 一场 CTF + 复盘 | 全部 | todo |

## 覆盖规则

每个技能页必须被至少一个项目页引用；没有项目用到的技能页，要么补项目，要么删掉。
`scripts/check-kb.py` 目前只校验题号与字段，覆盖关系靠人工在本文档维护。
