+++
date = '2026-11-09T10:05:00+08:00'
draft = true
title = '文件头与 magic bytes：为什么 file 说的才算'
description = "同一份文件，三种伪装手法，file 有三种不同反应。用可复跑的实测讲清「改扩展名 / 伪头 / 尾部追加」，并给出提取流程。"
slug = "file-magic"
chapter = "S-FILE"
stage = 1
minutes = 40
prereq = ["S-CLI"]
skills = ["magic-bytes", "file-command", "append-data"]
problems = ["F-01", "F-02", "F-03"]
+++

## 学完这页你能做到

1. 拿到未知文件，30 秒内判断真实类型，不依赖扩展名；
2. 解释为什么 `file` 有时只说 `data`；
3. 区分三种伪装：改扩展名、伪头、尾部追加；
4. 从尾部追加的数据里把隐藏文件切出来。

## 前置：这一页用到的三个概念

**字节**：8 位组成一个字节，取值 0–255。文件在磁盘上就是一串字节。

**十六进制**：两个十六进制字符表示一个字节，例如 `50 4B 03 04` 表示 4 个字节。

**函数 `file`**：Linux 自带的命令，读文件**内容**判断类型。它有两条判断依据：一是开头的固定字节（magic bytes），二是后续的数据结构是否符合该格式的规范。只满足第一条不够，这就是下一节实测 2 的原因。

## 核心事实：`file` 看内容，不看扩展名

### 实测 1 · 改扩展名骗不过它

```bash
python3 -c "import zipfile; z=zipfile.ZipFile('a.zip','w'); z.writestr('n.txt','hi'); z.close()"
cp a.zip looks-like.png
file looks-like.png
```

```text
looks-like.png: Zip archive data, at least v2.0 to extract, compression method=deflate
```

扩展名是 `.png`，`file` 依然报 `Zip archive`。

### 实测 2 · 但也不是只看前 4 字节

```bash
printf '\x89PNG\r\n\x1a\n' > short.png
file short.png
```

```text
short.png: data
```

签名是对的，但后面没有 IHDR 块，`file` 拒绝承认。

> magic bytes 是**必要条件**，不是充分条件。只给 4 字节头时判断要谨慎。

### 实测 3 · 伪头会被识破，并给你一句关键提示

```bash
{ printf '\x89PNG\r\n\x1a\n'; cat a.zip; } > fake.png
file fake.png
```

```text
fake.png: Zip archive, with extra data prepended
```

`with extra data prepended` 就是「**前面有多余数据**」。看到它，去真实格式的起点开始读。

### 实测 4 · 尾部追加：`file` 完全看不出

```bash
python3 -c "import zipfile; z=zipfile.ZipFile('a.zip','w'); z.writestr('flag.txt','flag{appended_after_eof}'); z.close()"
cp base.png combined.png && cat a.zip >> combined.png
file combined.png
```

```text
combined.png: PNG image data, 1 x 1, 8-bit grayscale, non-interlaced
```

看起来完全正常。这就是尾部追加成为隐写首选手法的原因。

## 头字节速查表

| 类型 | 十六进制头 | ASCII |
| --- | --- | --- |
| PNG | `89 50 4E 47 0D 0A 1A 0A` | `.PNG....` |
| JPEG | `FF D8 FF` | — |
| GIF | `47 49 46 38` | `GIF8` |
| ZIP | `50 4B 03 04` | `PK..` |
| GZIP | `1F 8B` | — |
| PDF | `25 50 44 46` | `%PDF` |
| ELF | `7F 45 4C 46` | `.ELF` |
| 7z | `37 7A BC AF 27 1C` | `7z....` |

> 只给 4 字节时很多类型会被判成 `data`（见实测 2），所以题目通常给 8 或 16 字节。

## 三种伪装与 `file` 的检测能力

| 手法 | `file` 能否识破 | 你该做什么 |
| --- | --- | --- |
| 改扩展名 | 能 | 直接看 `file` 输出 |
| 伪头 | 能，提示 `extra data` | 找真实格式的起点 |
| 尾部追加 | **不能** | 自己搜签名 / 比长度 |

## 提取尾部追加的文件

```bash
python3 - <<'PY'
data = open('combined.png', 'rb').read()
i = data.rfind(b'PK\x03\x04')
print(f'总长 {len(data)}，PK 偏移 {i}')
open('out.zip', 'wb').write(data[i:])
PY
```

实测输出 `总长 205，PK 偏移 67`，切出来的 `out.zip` 是合法压缩包。

## 练习

### Q1 · 看头识类型

```text
89 50 4E 47 0D 0A 1A 0A
```

<details>
<summary>答案</summary>

PNG。但只有这 8 个字节时 `file` 会输出 `data`（实测 2），需要配合 IHDR 块。
</details>

### Q2 · 为什么 jar 其实是 zip

```text
50 4B 03 04
```

<details>
<summary>答案</summary>

ZIP 本地文件头。`.jar`、`.docx`、`.apk`、`.epub` 都是 zip 容器，头都是 `PK\x03\x04`。
</details>

### Q3 · 动手提取

先造出这个「尾部追加了 zip」的图片，再把追加的部分取出来：

```bash
python3 -c "import zipfile; z=zipfile.ZipFile('a.zip','w'); z.writestr('flag.txt','flag{appended_after_eof}'); z.close()"
cp base.png combined.png && cat a.zip >> combined.png
```

<details>
<summary>提示</summary>

1. `file` 不会报异常，要自己比大小或搜签名。
2. 搜 `PK\x03\x04` 的**最后一次**出现位置，从那切到末尾。
</details>

<details>
<summary>答案</summary>

```bash
python3 - <<'PY'
data = open('combined.png','rb').read()
i = data.rfind(b'PK\x03\x04')
open('out.zip','wb').write(data[i:])
PY
python3 -c "import zipfile; print(zipfile.ZipFile('out.zip').read('flag.txt').decode())"
```

得到 `flag{appended_after_eof}`。
</details>

## 自测

1. 为什么 `.png` 后缀的文件会被报成 `Zip archive`？
2. 什么情况下 `file` 说 `data` 但文件其实有类型？
3. 看到 `with extra data prepended` 你的下一步是什么？

<details>
<summary>自测答案</summary>

1. 它读内容里的签名，不读扩展名。
2. 前有伪装签名，或数据不足（只有 magic bytes 没有结构）。
3. 去真实格式的起点读，前面那段通常不是垃圾，而是另一层线索。
</details>

## 术语

| 中文 | English | 一句话 |
| --- | --- | --- |
| 文件签名 | magic bytes | 文件开头的固定字节 |
| 附加数据 | appended data | 逻辑末尾之后多出来的内容 |
| 伪装头 | fake header | 把 A 的签名贴在 B 前面 |

## 延伸

- `man file`、`magic(5)`：判断规则的来源。
- `binwalk` / `foremost`：自动扫描嵌入文件（W5 再学）。
