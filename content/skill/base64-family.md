+++
date = '2026-11-09T10:00:00+08:00'
draft = true
title = 'Base64 家族：从 6 位分组到四个变体'
description = "给出手算步骤与字母表，讲清 padding 的两种含义、长度公式、启发式识别表，以及三类典型报错的真实成因。"
slug = "base64-family"
chapter = "S-B64"
stage = 1
minutes = 60
prereq = ["S-BIN"]
skills = ["base16", "base32", "base64", "base64url"]
problems = ["B64-01", "B64-02", "B64-03", "B64-04", "B64-05"]
+++

## 学完这页你能做到

1. 看到一串陌生字符，判断它是不是 Base 家族、是哪一种，并说明**依据**；
2. **手算**任意 1–3 字节的 Base64，不看工具也能写出结果；
3. 用长度公式预判输出长度和等号个数；
4. 遇到 `Incorrect padding` / `Invalid base64-encoded string` 知道真实成因与修法。

## 一个模型统一四个变体

Base 家族都做同一件事：**把二进制按固定位数切开，每段映射成一个字符**。

| 编码 | 每组位数 | 字符集 | 3 字节变成 | 常见场景 |
| --- | --- | --- | --- | --- |
| Base16（hex） | 4 | `0-9A-Fa-f` | 6 字符 | 十六进制摘要、文件头 |
| Base32 | 5 | `A-Z2-7` | 8 字符（含 `=`） | 不区分大小写的场合 |
| Base64 | 6 | `A-Za-z0-9+/` | 4 字符 | 邮件附件、图片内嵌 |
| Base64url | 6 | `A-Za-z0-9-_` | 4 字符 | URL、文件名、JWT |

一句话：**Base64 是「6 位一组」的产物**，另外三个只是换位宽或换字符集。

## 为什么偏偏是 6 位

3 字节 = 24 位，`24 / 6 = 4`，正好整除，所以 3 字节 → 4 字符。

选 6 位是因为 `2^6 = 64`：64 个可打印字符够用，且不会在传输中被转义。

## 字母表（手算必须背下来）

| 索引 | 字符 | 索引 | 字符 |
| --- | --- | --- | --- |
| 0–25 | `A`–`Z` | 26–51 | `a`–`z` |
| 52–61 | `0`–`9` | 62 | `+` |
| 63 | `/` | | |

展开看：

```text
 0=A   1=B   2=C   3=D   4=E   5=F   6=G   7=H
 8=I   9=J  10=K  11=L  12=M  13=N  14=O  15=P
16=Q  17=R  18=S  19=T  20=U  21=V  22=W  23=X
24=Y  25=Z  26=a  27=b  28=c  29=d  30=e  31=f
32=g  33=h  34=i  35=j  36=k  37=l  38=m  39=n
40=o  41=p  42=q  43=r  44=s  45=t  46=u  47=v
48=w  49=x  50=y  51=z  52=0  53=1  54=2  55=3
56=4  57=5  58=6  59=7  60=8  61=9  62=+  63=/
```

规律：大写 0–25，小写 26–51，数字 52–61，`+` 62，`/` 63。

## 手算一个字节

以 `f` 为例：

```text
f            = 0x66      = 01100110          （8 位）
补 4 个 0     = 01100110 0000                （凑满 12 位 = 2 组 × 6）
分组         = 011001 100000
转十进制      = 25      32
查表         = Z       g
结果         = Zg==                          （少一组，补一个 =）
```

验证：

```bash
python3 -c "import base64; print(base64.b64encode(b'f').decode())"
# Zg==
```

再算两个：

```text
fl  = 0x66 0x6C = 01100110 01101100
    -> 011001(25)=Z  100110(38)=m  110000(48)=w  缺一组补 =
    -> Zmw=

fla = 0x66 0x6C 0x61  （正好 3 字节，无 =）
    -> 011001(25)=Z  100110(38)=m  110001(49)=x  100001(33)=h
    -> Zmxh
```

对照实测：

```bash
for s in f fl fla flag; do printf '%-6s -> %s\n' "$s" "$(printf '%s' "$s" | base64)"; done
```

```text
f      -> Zg==
fl     -> Zmw=
fla    -> Zmxh
flag   -> ZmxhZw==
```

## 长度公式（预判，不用试）

设输入 `n` 字节：

```text
输出长度 = 4 * ceil(n / 3)
等号个数 = (3 - n % 3) % 3
```

实测对照：

| n | 输出长度 | 等号数 |
| --- | --- | --- |
| 1 | 4 | 2 |
| 2 | 4 | 1 |
| 3 | 4 | 0 |
| 4 | 8 | 2 |
| 5 | 8 | 1 |
| 6 | 8 | 0 |

看到 `=` 的个数，就能反推原数据长度：`n = 输出长度/4*3 - 等号个数`。

## padding 到底是什么

这里有两件不同的事，混起来就会讲错：

1. **位补零**：最后一组不足 6 位时，编码器在末尾补 0 位凑满；
2. **`=` 标记**：每缺一个完整的 6 位组，就输出一个 `=`。

所以 `=` 不是往数据里塞字节，但**它确实计入长度**——`Zg==` 的 4 个字符里有 2 个是标记。解码器正是靠在末尾的 `=` 个数知道原始数据是 1、2 还是 3 的倍数。

严格说，`=` 是「缺组标记」，属于 padding 机制的一部分，不是「填充的实际数据」。

## 启发式识别表

> **重要**：下表是排查顺序，不是判定规则。最终要靠**字符集 + 长度模数 + 上下文**三者一起看。

| 你看到 | 更可能是 | 关键依据 |
| --- | --- | --- |
| 只有 `0-9A-Fa-f`、长度为偶数 | Base16 | 字符集限定在 16 个符号内 |
| 只有 `A-Z2-7`、带 `=`、长度是 8 的倍数 | Base32 | **带 padding 时**长度才是 8 的倍数，去 padding 后不一定 |
| 含 `A-Za-z0-9+/`，可能带 `=` | Base64 | `=` 只是**常见**，不是必需：长度是 3 的倍数或已去掉 padding 时就没有 |
| **出现 `-` 或 `_`** | Base64url | 这才是强信号；只有「没有 `=`」不能区分（标准 Base64 去掉 padding 也没 `=`） |
| `eyJ` 开头 | `{"` + 可打印字节的 base64url | 强提示，不是证明 |

关于 `eyJ`，实测一下就更清楚：

```bash
python3 - <<'PY'
import base64
for s in ['{"a":1}', '{"A":1}', '{"', '[{"a":1}]']:
    enc = base64.urlsafe_b64encode(s.encode()).decode().rstrip('=')
    print(f'{s!r:12} -> {enc}')
PY
```

```text
'{"a":1}'      -> eyJhIjoxfQ
'{"A":1}'      -> eyJBIjoxfQ
'{"'           -> eyI
'[{"a":1}]'    -> W3siYSI6MX1d
```

结论：`eyJ` 对应「`{"` + 一个 0x40–0x7F 的字节」；单独的 `{"` 得到的是 `eyI`；数组开头是 `W3si`。所以它很有用，但不是万能钥匙。

## base64url 与标准 Base64 的差别

```bash
python3 -c "import base64; print(base64.urlsafe_b64encode(b'\xfb\xff').decode())"
python3 -c "import base64; print(base64.urlsafe_b64decode('-_8='))"
```

```text
-_8=
b'\xfb\xff'
```

同样两字节，标准 Base64 编成 `+/8=`。`-`/`_` 只是 `+`/`/` 的替身，编码算法完全一样——所以在 URL、文件名、JWT 里更安全。

## 三类报错与修法

### 坑 1：`Incorrect padding`

```text
binascii.Error: Incorrect padding
```

成因：长度不是 4 的倍数。**修法看模数，不是无脑补 `=`**：

| `len % 4` | 含义 | 处理 |
| --- | --- | --- |
| 0 | 正常 | 不用补 |
| 2 | 缺两个字符 | 补 `==` |
| 3 | 缺一个字符 | 补 `=` |
| 1 | **输入本身有问题** | 补 3 个 `=` 也救不回来，先检查是否少了/多了字符 |

### 坑 2：`Invalid base64-encoded string`

```text
binascii.Error: Invalid base64-encoded string: number of data characters (5) cannot be 1 more than a multiple of 4
```

这条常见于「长度模 4 余 1」。另一个来源是 base64url 丢给标准解码器——但报错信息可能**误导**，因为 Python 的 `b64decode` 默认 `validate=False`，会**静默丢弃**字母表之外的字符：

```text
-_8=  -> 丢弃 - 和 _ -> 只剩 8=  -> 报长度错误
```

修法：
- 先替换字符集：`s.replace('-', '+').replace('_', '/')`；
- 想看真正原因就加 `validate=True`，非法字符会直接报 `Only base64 data is allowed`；
- 别被报错文字带跑，先确认字符集对不对。

### 坑 3：解出来还是乱码

**不要条件反射地"再解一次"。** 先看解出来的字节：

| 解出来的样子 | 下一步 |
| --- | --- |
| 仍然是 Base64 字符集 | 可能是二次编码，再解一次 |
| 像压缩数据（`PK`、`\x1f\x8b`） | 换思路：先判断文件类型 |
| 像加密数据或随机字节 | 不是编码题，别硬解 |
| 中文乱码 | 字符集问题（GBK/UTF-8），不是 Base 问题 |

## 跨平台提醒

上面的 `base64 -d`、`base32 -d`、`xxd -r -p` 属于 GNU coreutils。macOS 上 `base64` 是 BSD 版（参数是 `-D`），`base32` 可能不存在。

可移植写法用 Python：

```bash
python3 -c "import base64; print(base64.b64decode('ZmxhZw==').decode())"
python3 -c "import base64; print(base64.b32decode('MZWGCZY=').decode())"
python3 -c "print(bytes.fromhex('666c6167').decode())"
```

## 练习

### Q1 · 基础解码

```text
ZmxhZ3tiNjRfaXNfZ3JvdXBpbmdfbm90X2NoYXJhY3RlcnN9
```

<details>
<summary>提示</summary>

长度 48，是 4 的倍数，结尾没有 `=`——这很常见，不代表不是 Base64。
</details>

<details>
<summary>答案</summary>

`flag{b64_is_grouping_not_characters}`

```bash
echo ZmxhZ3tiNjRfaXNfZ3JvdXBpbmdfbm90X2NoYXJhY3RlcnN9 | base64 -d
```
</details>

### Q2 · 缺 padding

```text
ZmxhZ3twYWRkaW5nfQ
```

<details>
<summary>提示</summary>

长度 18，`18 % 4 = 2` → 缺两个字符 → 补 `==`。
</details>

<details>
<summary>答案</summary>

`flag{padding}`

```bash
python3 -c "import base64; print(base64.b64decode('ZmxhZ3twYWRkaW5nfQ' + '==').decode())"
```
</details>

### Q3 · 换个字符集

```text
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9
```

<details>
<summary>提示</summary>

`eyJ` 对应 `{"` + 可打印字节，这是 JSON 开头。
</details>

<details>
<summary>答案</summary>

`{"alg":"HS256","typ":"JWT"}`

```bash
python3 -c "import base64; print(base64.urlsafe_b64decode('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9').decode())"
```
</details>

### Q4 · Base32

```text
MZWGCZY=
```

<details>
<summary>提示</summary>

全大写 + 数字 2–7，长度 8 的倍数，还带 `=`。
</details>

<details>
<summary>答案</summary>

`flag`

```bash
printf 'MZWGCZY=' | base32 -d
```
</details>

### Q5 · Base16（这题最容易看错）

```text
666c61677b6865787d
```

<details>
<summary>提示</summary>

只有 `0-9` 和 `a-f`，长度 18（偶数）——这是十六进制，不是 Base64。
</details>

<details>
<summary>答案</summary>

`flag{hex}`

```bash
printf '666c61677b6865787d' | xxd -r -p
```
</details>

## 自测

1. 手算：字节 `0x41` 的 Base64 是什么？
2. 一串长度 20、结尾带 `==` 的 Base64，原始数据是多少字节？
3. 长度 15、没有 `=` 的 Base64 串，能直接解码吗？为什么？

<details>
<summary>自测答案</summary>

1. `0x41 = 01000001`，补 4 个 0 → `010000(16)=Q`、`010000(16)=Q` → `QQ==`。
2. **13 字节**。`20/4×3 − 2 = 13`；验算：`13 % 3 = 1`，等号数 `(3−1)%3 = 2`，输出长度 `4×ceil(13/3) = 20`。
3. 不能。`15 % 4 = 3`，缺一个字符，要补一个 `=` 才能解。这也说明「没有 `=` 就说明不是 Base64」是错的判断。
</details>

## 术语

| 中文 | English | 一句话 |
| --- | --- | --- |
| 编码 | encoding | 可逆的表示转换，不是加密 |
| 字母表 | alphabet | 64 个符号的有序集合 |
| 补位 | padding | 位补零 + `=` 缺组标记 |
| URL 安全 | URL-safe | 换成不触发 URL 转义的字符 |

## 延伸

- **RFC 4648**：Base16/32/64 的正式定义（含全部字符表与 padding 规则）。
- **JWT**：header 与 payload 都是 base64url，中间用 `.` 连接。
