+++
date = '2026-11-09T10:00:00+08:00'
draft = true
title = 'Base64 家族：一个模型搞懂 Base16 / 32 / 64 / 64url'
description = "从「6 位一组」这一条规则出发，一次讲清四个变体、padding 的来源、3 秒辨识法，附 4 道可自验的题。"
slug = "base64-family"
chapter = "S-B64"
stage = 1
minutes = 45
prereq = ["S-BIN"]
skills = ["base16", "base32", "base64", "base64url"]
problems = ["B64-01", "B64-02", "B64-03", "B64-04"]
+++

## 学完这页你能做到

1. 看到任意一串陌生字符，3 秒内判断它是不是 Base 家族、是哪一种；
2. 手算任意 1–3 字节的 Base64 结果，包括结尾有几个 `=`；
3. 认出 base64url，并说出它最常出现在哪里；
4. 遇到 `Incorrect padding` 知道原因、当场能修。

## 先建一个模型

Base 家族所有编码干的是同一件事：**把二进制按固定位数切开，每一段映射成一个字符**。

| 编码 | 每组位数 | 字符集 | 3 字节变成 | 典型信号 |
| --- | --- | --- | --- | --- |
| Base16（hex） | 4 | `0-9a-f` | 6 字符 | 偶数长度、纯十六进制 |
| Base32 | 5 | `A-Z2-7` | 8 字符（含 `=`） | 全大写、长度是 8 的倍数 |
| Base64 | 6 | `A-Za-z0-9+/` | 4 字符 | 大小写混合、结尾常有 `=` |
| Base64url | 6 | `A-Za-z0-9-_` | 4 字符 | 出现 `-` 或 `_`、常常没有 `=` |

一句话：**Base64 只是「6 位一组」这条规则的产物**，另外三个要么换位宽，要么换字符集。

## 为什么偏偏是 6 位

3 字节 = 24 位，`24 / 6 = 4`，正好整除，所以 3 个字节变成 4 个字符。

选 6 位是因为 `2^6 = 64`，64 个可打印字符足够表达，又好认、好复制、不会在传输里被转义。

## padding 根本不是"填充符"，是补位

当输入不是 3 的倍数时，最后一组凑不满 24 位：

- 剩 **1 字节**（8 位）→ 补 4 个 0 凑成 2 组 → 输出 2 字符 + `==`
- 剩 **2 字节**（16 位）→ 补 2 个 0 凑成 3 组 → 输出 3 字符 + `=`
- 剩 **0 字节** → 4 字符，没有等号

### 实测（这条命令就是全部证据）

```bash
for s in f fl fla flag; do printf '%-6s -> %s\n' "$s" "$(printf '%s' "$s" | base64)"; done
```

输出：

```text
f      -> Zg==
fl     -> Zmw=
fla    -> Zmxh
flag   -> ZmxhZw==
```

自己数一遍：1 字节 → 2 字符 + 2 个等号；2 字节 → 3 字符 + 1 个等号；3 字节 → 4 字符、无等号。

## 3 秒判断表

| 你看到 | 结论 | 下一步 |
| --- | --- | --- |
| 全是 `0-9a-f`、长度为偶数 | Base16 / hex | `xxd -r -p` 或 `bytes.fromhex()` |
| `A-Z2-7`、长度是 8 的倍数、结尾可能有 `=` | Base32 | `base32 -d` |
| `A-Za-z0-9+/`、结尾有 `=` | Base64 | `base64 -d` |
| `A-Za-z0-9-_`、没有 `=` | Base64url | 把 `-`/`_` 换成 `+`/`/` 再解 |
| `eyJ` 开头 | base64url 的 JSON（JWT 头） | 解出来是 `{"alg":...}` |
| 以上都不像 | 先别猜，看长度和字符集再排除 | 回到本表逐行试 |

## 实测：base64url 与标准 Base64 的差别

```bash
python3 -c "import base64; print(base64.urlsafe_b64encode(b'\xfb\xff').decode())"
python3 -c "import base64; print(base64.urlsafe_b64decode('-_8='))"
```

输出分别是 `-_8=` 和 `b'\xfb\xff'`。

同样两个字节，标准 Base64 会编成 `+/8=`。`-` 和 `_` 就是 `+` 和 `/` 的 URL 安全替身——因为在 URL、文件名、JWT 里 `+` 和 `/` 容易被转义或截断。

## 三个坑（附报错原文）

**坑 1：`Incorrect padding`**

```text
binascii.Error: Incorrect padding
```

原因：长度不是 4 的倍数。修法：补到 4 的倍数，通常补 `=`。

**坑 2：base64url 丢给标准解码器**

```text
binascii.Error: Invalid base64-encoded string
```

修法：`s.replace('-', '+').replace('_', '/')`，再补 padding。

**坑 3：解一次出来还是乱码**

说明是二次编码。别急着换工具，**再解一次**。

## 练习

> 全部可以本地复现。先自己做，再看折叠的提示与答案。

### Q1 · 基础解码

题面：

```text
ZmxhZ3tiNjRfaXNfZ3JvdXBpbmdfbm90X2NoYXJhY3RlcnN9
```

<details>
<summary>提示</summary>

1. 长度 48，是 4 的倍数，结尾没有 `=`。
2. 含大小写字母与数字，先试 Base64。
</details>

<details>
<summary>答案</summary>

`flag{b64_is_grouping_not_characters}`

```bash
echo ZmxhZ3tiNjRfaXNfZ3JvdXBpbmdfbm90X2NoYXJhY3RlcnN9 | base64 -d
```
</details>

### Q2 · 缺 padding

题面：

```text
ZmxhZ3twYWRkaW5nfQ
```

<details>
<summary>提示</summary>

1. 数长度：18。
2. `18 % 4 = 2` → 需要补 **两个** `=`。
</details>

<details>
<summary>答案</summary>

`flag{padding}`

```bash
python3 -c "import base64; print(base64.b64decode('ZmxhZ3twYWRkaW5nfQ' + '==').decode())"
```
</details>

### Q3 · 换个字符集

题面：

```text
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9
```

<details>
<summary>提示</summary>

1. 没有 `-`/`_`，但也没有 `=`，长度是 4 的倍数。
2. `eyJ` 是 `{"` 的 base64url 编码——这是 JSON 的开头。
</details>

<details>
<summary>答案</summary>

`{"alg":"HS256","typ":"JWT"}`

```bash
python3 -c "import base64; print(base64.urlsafe_b64decode('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9').decode())"
```
</details>

### Q4 · 不是 Base64

题面：

```text
MZWGCZY=
```

<details>
<summary>提示</summary>

1. 全大写 + 数字 2–7，长度 8 的倍数——这是 Base32 的地盘。
2. 用 `base32 -d`，别用 `base64 -d`。
</details>

<details>
<summary>答案</summary>

`flag`

```bash
printf 'MZWGCZY=' | base32 -d
```
</details>

## 自测（30 秒内回答，不许查）

1. Base64 为什么按 6 位分组？
2. 输入 4 个字节，输出结尾会有几个 `=`？
3. `-_8=` 是哪种编码？为什么会出现 `-`？

<details>
<summary>自测答案</summary>

1. 因为 `2^6 = 64`，正好用满 64 个可打印字符；且 24 位能被 6 整除。
2. **两个**。4 字节 = 3 + 1，最后一组只剩 1 字节 → 输出 6 字符 + `==`。
3. base64url；`-` 是 `+` 的替身，`_` 是 `/` 的替身，避免在 URL 中被转义。
</details>

## 术语

| 中文 | English | 一句话 |
| --- | --- | --- |
| 编码 | encoding | 可逆的表示转换，不是加密 |
| 补位 | padding | 凑满分组的填充，用 `=` 表示 |
| 字符集 | alphabet | 64 个符号的集合 |
| URL 安全 | URL-safe | 换成不触发 URL 转义的字符 |

## 延伸

- **RFC 4648**：Base16/32/64 的正式定义，含全部字符表。
- **JWT**：header 与 payload 都是 base64url，中间用 `.` 连接。
