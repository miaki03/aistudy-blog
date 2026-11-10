+++
date = '2026-11-09T10:10:00+08:00'
draft = true
title = '项目 P1 · 编码与文件侦察报告'
description = "把「Base64 家族」和「文件头」两页学到的东西用一次：6 个可疑样本，产出一份可复现的侦察报告。"
slug = "p1-encoding-recon"
chapter = "P1"
stage = 1
minutes = 170
prereq = ["U00", "U10", "U12"]
skills = ["base64", "base32", "hex", "base64url", "magic-bytes", "file-command"]
problems = ["P1-01", "P1-02", "P1-03", "P1-04", "P1-05", "P1-06"]
+++

## 这个项目要你做什么

交付一份 Markdown 报告 `report.md`，对下面 6 个「可疑样本」逐个给出：

1. **判断**：它是什么类型（哪种编码 / 哪种文件）；
2. **证据**：你依据哪几个字符或哪几个字节下的判断；
3. **命令**：一条能复现结论的命令；
4. **结论**：解出来的内容，或「里面还藏着一层」。

格式照抄这个模板即可：

```markdown
## 样本 01
- 判断：
- 证据：
- 命令：
- 结论：
```

## 样本清单

### 样本 01 · 一串字符

```text
ZmxhZ3tiNjRfaXNfZ3JvdXBpbmdfbm90X2NoYXJhY3RlcnN9
```

### 样本 02 · 一串字符

```text
MZWGCZ33OBQWIZDJNZTX2===
```

### 样本 03 · 一串字符

```text
666c61677b6865787d
```

### 样本 04 · 一串字符

```text
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9
```

### 样本 05 · 一个文件

用这条命令自己造出来：

```bash
python3 -c "import zipfile; z=zipfile.ZipFile('a.zip','w'); z.writestr('n.txt','hi'); z.close()"
cp a.zip sample05.png
```

### 样本 06 · 一个文件

```bash
python3 -c "import zipfile; z=zipfile.ZipFile('a.zip','w'); z.writestr('flag.txt','flag{appended_after_eof}'); z.close()"
cp base.png sample06.png && cat a.zip >> sample06.png
```

> `base.png` 需要先按「文件头」那页的实测 4 造一个 1x1 PNG。造不出来就直接用一个真实 PNG 代替，效果一样。

## 评分标准

| 项 | 分值 | 说明 |
| --- | --- | --- |
| 判断正确 | 6 分 | 每个样本 1 分 |
| 证据具体 | 6 分 | 能指出「第几个字符 / 哪些字节」，不是「看起来像」 |
| 命令可复现 | 6 分 | 我把命令贴进终端能跑出同样结果 |
| 结论准确 | 6 分 | 解出的内容一字不差 |
| 报告可读 | 2 分 | 一眼能看出每个样本的结论 |

26 分里拿到 20 分算通过。

## 卡住时怎么办

| 症状 | 先检查 |
| --- | --- |
| 解码报 `Incorrect padding` | 长度是不是 4 的倍数（Base64）/ 8 的倍数（Base32） |
| 解出来还是乱码 | 是不是还有一层编码 |
| `file` 说 `data` | 字节是不是太少了？换 8 或 16 字节再判断 |
| 文件看起来正常但总觉得不对 | 比大小、搜 `PK` / `\x89PNG` |

## 完成后你应该能

- 不查资料说出 Base16/32/64/64url 的区别；
- 拿到文件先跑 `file` + `xxd`，而不是先双击；
- 知道「看起来正常」不等于「没问题」。

## 扩展（可选）

把样本 06 里的隐藏文件换成一个真正的 flag 文件，再让同学做一遍——出题是检验自己是否真懂最快的方式。
