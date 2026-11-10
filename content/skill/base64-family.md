+++
date = '2026-11-09T10:00:00+08:00'
draft = false
title = 'Base64 家族：原理、手算与排错'
description = "从位与字节讲起，逐步推导 Base64 的分组规则、字母表映射、padding 与长度公式；给出编码与解码两个方向的手算示例，以及一个能实际跑出结论的识别脚本。"
slug = "base64-family"
chapter = "U10"
stage = 1
minutes = 70
prereq = ["U00"]
concepts = ["base64"]
reuse = ["U12", "U23", "U41", "U42", "U51", "U61"]
skills = ["base16", "base32", "base64", "base64url"]
problems = ["B64-01", "B64-02", "B64-03", "B64-04", "B64-05"]
+++

## 读完能做什么

1. 手算任意 3 字节以内数据的 Base64 编码，以及任意一段 Base64 的解码。
2. 说出 Base64 与 Base32 / Base16 / base64url 的关系，并认出它们各自的特征字符。
3. 拿到一段乱码，用一条命令判断它是不是 Base64；解出来还是乱码时，说出下一步该查什么。

## 这一页解决什么问题

你会遇到一串形如 `ZmxhZ3tiNjRf...` 的字符，需要判断它是什么编码、解出原文；更重要的，你要能理解它为什么长这样，这样遇到变形（缺 padding、换字符集、二次编码）才不会被卡住。

## 前置：四个必须先说清的概念

不解释这些，后面的推导就读不下去。

**位（bit）**：最小的数据单位，只有 0 和 1 两种取值。

**字节（byte）**：8 位组成一个字节，取值范围 0–255。计算机里文件、网络传输的基本单位都是字节。

**十六进制（hex）**：用 16 个符号 `0-9A-F`（或小写 `0-9a-f`）表示二进制，一个十六进制字符表示 4 位，两个字符表示一个字节。所以 `0x66` 和 `01100110` 是同一个数，写法不同。

**ASCII**：把 0–127 的整数映射到字符的约定。常用的是：`48` = `'0'`，`65` = `'A'`，`97` = `'a'`。所以字符串 `"f"` 在文件里存的其实是字节 `0x66`。

> 后面所有推导都只用到这四个概念，不需要其他背景。

## 编码是什么，不是什么

**编码（encoding）**：把数据从一种表示形式转换成另一种表示形式，规则公开、可逆、不需要密钥。

**加密（encryption）**：转换需要密钥，目的是让别人无法还原。

两者容易混，区别在**有没有密钥**和**目的**：编码是为了让数据能安全地通过只支持特定字符集的通道（比如邮件正文只能放可打印 ASCII），不是为了保密。

Base64 的体积会比原文大 1/3 左右，这是编码的代价，不是 bug。

## Base64 的完整算法

设输入是 `n` 个字节。

**第一步**：把字节序列按每 3 个字节一组切开。3 字节 = 24 位。

**第二步**：每一组的 24 位，从高位开始切成 4 段，每段 6 位。每段是一个 0–63 的整数。

**第三步**：用下面这张字母表，把每个整数换成对应的字符。

**第四步**：如果最后一组不足 3 字节：

- 剩余 1 字节（8 位）：在末尾补 4 个 0 凑成 12 位，得到 2 段，输出 2 个字符，再补 2 个 `=`；
- 剩余 2 字节（16 位）：补 2 个 0 凑成 18 位，得到 3 段，输出 3 个字符，再补 1 个 `=`；
- 剩余 0 字节：3 段正好，输出 4 个字符，不补 `=`。

这就是全部规则。下面两节用具体字节走一遍。

## 字母表

6 位能表示 0–63，共 64 个数，需要 64 个符号：

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

结构：`0–25` 是大写字母表，`26–51` 是小写字母表，`52–61` 是数字，`62` 是 `+`，`63` 是 `/`。

## 手算示例一：`"f"`

`"f"` 的 ASCII 是 102，也就是 `0x66`，也就是 `01100110`（8 位）。

只有 1 个字节，按第四步规则补 4 个 0：

```text
原始：      01100110
补 0 后：   01100110 0000     （12 位 = 2 段 × 6 位）
分组：      011001 | 100000
转十进制：      25  |     32
查表：          Z  |      g
输出：      Zg==
```

验证：

```bash
python3 -c "import base64; print(base64.b64encode(b'f').decode())"
```

```text
Zg==
```

## 手算示例二：`"fl"`

`f` = `0x66` = `01100110`，`l` = `0x6C` = `01101100`。

```text
原始：      01100110 01101100      （16 位）
补 0 后：   01100110 01101100 00   （18 位 = 3 段 × 6 位）
分组：      011001 | 100110 | 1100 00
转十进制：      25  |     38  |    48
查表：          Z  |      m  |     w
输出：      Zmw=
```

验证：

```bash
python3 -c "import base64; print(base64.b64encode(b'fl').decode())"
```

```text
Zmw=
```

## 手算示例三：`"fla"`

正好 3 个字节，不需要补位，也不产生 `=`：

```text
f = 0x66 = 01100110
l = 0x6C = 01101100
a = 0x61 = 01100001

合并：  01100110 01101100 01100001
分组：  011001 | 100110 | 110001 | 100001
十进制：    25 |     38 |     49 |     33
查表：       Z |      m |      x |      h
输出：   Zmxh
```

## 手算示例四：反方向，从字符回到字节

给你 `Zg==`，求原文：

**第一步**：拆成 4 个字符：`Z`、`g`、`=`、`=`。

**第二步**：`=` 不是数据。查表：`Z` = 25 = `011001`，`g` = 32 = `100000`。

**第三步**：拼回 12 位：`011001100000`。

**第四步**：按原始字节取 8 位，丢掉补的 4 位：`01100110`。

**第五步**：`01100110` = `0x66` = 102 = `'f'`。

验证：

```bash
python3 -c "import base64; print(base64.b64decode('Zg==').decode())"
```

```text
f
```

## 长度公式

设输入 `n` 字节，输出字符数（含 `=`）与 `=` 的个数是确定的：

```text
输出长度 = 4 * ceil(n / 3)
等号个数 = (3 - n % 3) % 3
```

实测对照：

| n 字节 | 输出长度 | 等号数 |
| --- | --- | --- |
| 1 | 4 | 2 |
| 2 | 4 | 1 |
| 3 | 4 | 0 |
| 4 | 8 | 2 |
| 5 | 8 | 1 |
| 6 | 8 | 0 |

反推原始长度：`n = 输出长度 / 4 * 3 - 等号个数`。

例：长度 20、末尾 2 个 `=` → `20/4*3 - 2 = 13` 字节。

## 四个变体的关系

所有 Base 编码的差别只有一个参数：**每组取多少位**。

如果一组取 `k` 位，就需要 `2^k` 个符号。所以：

| 编码 | 每组位数 k | 符号数 2^k | 字符集 | 为什么用它 |
| --- | --- | --- | --- | --- |
| Base16 | 4 | 16 | `0-9A-Fa-f` | 和十六进制完全一致，人眼易读 |
| Base32 | 5 | 32 | `A-Z2-7` | 字符集不区分大小写，适合人工转录 |
| Base64 | 6 | 64 | `A-Za-z0-9+/` | 体积效率高，最通用 |
| Base64url | 6 | 64 | `A-Za-z0-9-_` | 把 `+`、`/` 换成 URL 里安全的 `-`、`_` |

Base64url 和 Base64 的算法完全相同，只是字母表最后两个符号不同。它在 URL、文件名、JWT 里使用，因为 `+` 在 URL 里表示空格、`/` 是路径分隔符，都可能被转义或截断。

## 长度关系（为什么 Base64 变大 1/3）

每 3 字节（24 位）变成 4 个字符，字符是 ASCII 存储，每个占 1 字节，所以 3 字节变 4 字节，体积乘以 4/3。

Base32 是每 5 字节（40 位）变 8 字符，体积乘以 8/5 = 1.6。
Base16 是每 1 字节变 2 字符，体积乘以 2。

这就是为什么 Base64 最常用：它是三者里体积代价最小的。

## 识别：不要靠眼睛，跑脚本

看字符集只能给出候选，真正判定要看**解码是否成功、结果是否为可读文本**。

把下面这段存成 `tryall.py`，把待判定的字符串作为参数传入：

```python
import base64
import sys

def pad4(s):
    return s + "=" * (-len(s) % 4)

def attempt(name, fn, s):
    try:
        out = fn(s)
        print(f"{name:10} 成功   {out.decode('utf-8')!r}")
    except Exception as e:
        print(f"{name:10} 失败   {type(e).__name__}: {str(e)[:60]}")

s = sys.argv[1]
attempt("hex",       lambda x: bytes.fromhex(x), s)
attempt("base32",    lambda x: base64.b32decode(pad4(x.upper())), s)
attempt("base64",    lambda x: base64.b64decode(pad4(x), validate=True), s)
attempt("base64url", lambda x: base64.urlsafe_b64decode(pad4(x)), s)
```

实测四种输入的输出：

```text
输入 ZmxhZ3tiNjRfaXNfZ3JvdXBpbmdfbm90X2NoYXJhY3RlcnN9
  base64   成功   'flag{b64_is_grouping_not_characters}'
  base64url 成功  'flag{b64_is_grouping_not_characters}'

输入 MZWGCZY=
  base32   成功   'flag'
  base64   成功   但也解出了字节，只是不是可读文本（UTF-8 解码失败）
```

**判读规则**：

1. 报错的不算；
2. 解出来不是合法 UTF-8 文本的不算（多数题目答案是 ASCII）；
3. 只剩一个成功 → 就是它；
4. 同时成功且结果相同 → 说明两种解码器都兼容，按上下文决定（出现 `-`/`_` 就是 Base64url，否则标准 Base64）。

> 注意 `base64url` 解码器也接受标准字母表，所以它经常和 `base64` 同时成功。**能区分两者的是输入里有没有 `-` 或 `_`**，不是解码器。

## 三类常见错误

### 错误 1：`Incorrect padding`

```text
binascii.Error: Incorrect padding
```

成因：长度不是 4 的倍数。修法看余数：

| `len % 4` | 含义 | 处理 |
| --- | --- | --- |
| 0 | 正常 | 不需要处理 |
| 2 | 缺 2 个字符 | 补 `==` |
| 3 | 缺 1 个字符 | 补 `=` |
| 1 | 输入本身有问题 | 补 3 个 `=` 无法修复，先检查是否丢字符 |

### 错误 2：`Invalid base64-encoded string`

```text
binascii.Error: Invalid base64-encoded string: number of data characters (5) cannot be 1 more than a multiple of 4
```

两种来源：

- 长度模 4 余 1；
- 把 Base64url 丢给标准解码器。但这里有一个陷阱：Python 的 `b64decode` 默认 `validate=False`，会**静默丢弃字母表之外的字符**，所以 `-_8=` 里的 `-`、`_` 被删掉，只剩 `8=`，于是报的是长度错误而不是字符错误。

修法：

```python
s.replace("-", "+").replace("_", "/")   # 先换成标准字母表
```

想看到真实原因，加 `validate=True`，此时会报 `Only base64 data is allowed`。

### 错误 3：解出来是乱码

先看解出来的字节，再决定下一步，不要直接再解一次：

| 解出来的字节特征 | 处理 |
| --- | --- |
| 仍然是 Base64 字符集 | 可能是二次编码，再解一次 |
| 以 `PK`、`\x1f\x8b`、`\x89PNG` 开头 | 是压缩包/图片，先判断文件类型 |
| 看起来随机 | 可能是加密数据，不是编码题 |
| 中文乱码 | 是字符集问题（GBK/UTF-8），与 Base 无关 |

## 跨平台说明

`base64 -d`、`base32 -d`、`xxd -r -p` 属于 GNU coreutils，Linux 上可用。macOS 自带的是 BSD 版：`base64` 解码参数是 `-D`，而且可能没有 `base32`。

不依赖平台的做法是用 Python：

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

长度 48，是 4 的倍数，结尾没有 `=`。长度是 3 的倍数时本来就不会有 `=`，这不影响它是 Base64。
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

长度 18，`18 % 4 = 2`，按上面的表要补 `==`。
</details>

<details>
<summary>答案</summary>

`flag{padding}`

```bash
python3 -c "import base64; print(base64.b64decode('ZmxhZ3twYWRkaW5nfQ' + '==').decode())"
```
</details>

### Q3 · Base64url

```text
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9
```

<details>
<summary>提示</summary>

`eyJ` 对应 `{"` 加一个可打印字节。这是 JSON 的开头。
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

字符只有大写字母和 `2-7`，长度 8 的倍数，还带 `=`——三个条件同时满足。
</details>

<details>
<summary>答案</summary>

`flag`

```bash
printf 'MZWGCZY=' | base32 -d
```
</details>

### Q5 · Base16

```text
666c61677b6865787d
```

<details>
<summary>提示</summary>

只含 `0-9` 和 `a-f`，长度 18（偶数）。每 2 个字符是一个字节。
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
2. 一串长度 20、末尾带 `==` 的 Base64，原始数据是几字节？
3. 长度 15、没有 `=` 的串，能直接解码吗，为什么？

<details>
<summary>自测答案</summary>

1. `0x41` = `01000001`，补 4 个 0 得 `01000001 0000`，分组 `010000(16)=Q`、`010000(16)=Q` → `QQ==`。
2. 13 字节。`20/4*3 - 2 = 13`。验算：`13 % 3 = 1`，等号数 `(3-1)%3 = 2`，输出长度 `4*ceil(13/3) = 20`。
3. 不能。`15 % 4 = 3`，缺 1 个字符，补 1 个 `=` 后才能解。这说明「没有 `=` 就不是 Base64」的判断是错的。
</details>

## 术语

| 中文 | English | 定义 |
| --- | --- | --- |
| 编码 | encoding | 可逆、无密钥的表示转换 |
| 字母表 | alphabet | 一组有序符号，Base64 有 64 个 |
| 补位 | padding | 最后一组不足时的补 0 位与 `=` 标记 |
| URL 安全 | URL-safe | 不使用在 URL 中有特殊含义的字符 |

## 延伸

- **RFC 4648**：Base16/32/64 的正式定义，包含完整字符表与 padding 规则，是这一页所有规则的出处。
- **JWT**：header 与 payload 都使用 Base64url，两段之间用 `.` 连接。看到 `eyJ...` 多半是它。
