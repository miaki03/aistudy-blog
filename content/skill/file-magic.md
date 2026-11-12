+++
date = '2026-11-09T10:05:00+08:00'
draft = false
title = '第 11 章 · 文件与容器：`file` 为什么会骗你'
description = '改扩展名、贴伪头、尾部追加、伪加密、CRC 不符——五种「文件看起来正常其实被动过」的情况，逐个用贯穿样本实测，并给出提取流程。'
slug = 'file-magic'
chapter = 'U12'
stage = 1
minutes = 110
prereq = ['U00', 'U06']
concepts = ['magic-number', 'pseudo-encryption', 'appended-data']
reuse = ['U20', 'U21', 'U22', 'U32', 'U33', 'U41']
skills = ['magic-bytes', 'file-command', 'append-data', 'zip']
problems = ['U12.1-01', 'U12.2-01', 'U12.3-01', 'U12.3-02', 'U12.4-01', 'U12.5-01', 'U12.5-02', 'U12.5-03', 'U12.6-01']
+++

## 读完能做什么

1. 拿到一个未知文件，30 秒内判断它的**真实类型**，不依赖扩展名，也不只依赖 `file`。
2. 认出五种「被动过」的情况：改扩展名、前缀垃圾、贴伪头、伪加密、CRC 不符，并说出各自的检测方法。
3. 把一个文件按「逻辑末尾」切开，从尾部附加的数据里取出隐藏的另一个文件。

这一章之后，`file` 的输出在你眼里只是一个**线索**，不再是结论。

## 前置

第 1 章（字节、十六进制）、第 7 章（`open(...,"rb")`、`find`、`int.from_bytes`）。样本：`samples/S-01.png`、`S-02.png`、`S-03.zip`、`S-04.gz`。

本章所有实测都跑在这四个文件上——它们是贯穿样本，后面 Part 2 还会再挖一次。

---

## 12.1 `file` 读内容，不读扩展名

### 跑通

先改个扩展名，看 `file` 在不在乎：

```console
$ cp samples/S-03.zip /tmp/looks-like.png
$ file /tmp/looks-like.png
/tmp/looks-like.png: Zip archive data, at least v2.0 to extract, compression method=store
```

扩展名是 `.png`，它照样报 `Zip archive`。

再给它一个「正确的签名」，但后面什么都不给：

```console
$ printf '\x89PNG\r\n\x1a\n' > /tmp/short.png
$ file /tmp/short.png
/tmp/short.png: data
```

签名完全正确，`file` 却说 `data`。

### 机制

`file` 的判断分两步，**两步都要过**：

1. **看开头的固定字节**（magic bytes）。`50 4B 03 04` → 可能是个 ZIP。
2. **验证后续结构符合该格式的规范**。ZIP 要求后面跟着本地文件头字段；PNG 要求紧跟一个 `IHDR` 块。

只满足第一步时，`file` 会谨慎地报 `data`。所以 **magic bytes 是必要条件，不是充分条件**。

这个设计直接决定了做题时的一个常识：**题目里只给 4 个字节让你认类型，是不严谨的**；正常会给 8 或 16 字节。

`file` 不看扩展名，是因为它拿到的只有一个路径。扩展名存在文件名里，而文件名和内容没有任何绑定关系——第 1 章 已经讲过。

> **易错**　`file` 说 `data` **不等于**「这不是个正常文件」。它只意味着「我没认出」。`S-04.gz` 就是个例子，下一节会看到它被认成了一个完全不相干的东西。

### 速查

常见格式的头字节（只列本课会用到的）：

| 类型 | 十六进制头 | ASCII |
| --- | --- | --- |
| PNG | `89 50 4E 47 0D 0A 1A 0A` | `.PNG....` |
| JPEG | `FF D8 FF` | — |
| GIF | `47 49 46 38` | `GIF8` |
| ZIP | `50 4B 03 04` | `PK..` |
| GZIP | `1F 8B 08` | — |
| PDF | `25 50 44 46` | `%PDF` |
| ELF | `7F 45 4C 46` | `.ELF` |
| 7z | `37 7A BC AF 27 1C` | `7z....` |
| RAR | `52 61 72 21 1A 07` | `Rar!..` |
| WAV | `52 49 46 46` | `RIFF` |

`PK` 这一族值得单记：`.zip`、`.jar`、`.docx`、`.apk`、`.epub` **都是 ZIP 容器**，头全是 `50 4B 03 04`。所以看到一个 `.docx`，正确的心态是「这是个 ZIP，解开看里面」。

### 题 U12.1-01

一个文件只有 `89 50 4E 47 0D 0A 1A 0A` 这 8 个字节，`file` 会输出什么？

<details><summary>提示</summary>

只有签名、没有后续结构时，`file` 不敢下结论。

</details>

<details><summary>答案</summary>

```console
$ printf '\x89PNG\r\n\x1a\n' > /tmp/short.png
$ file /tmp/short.png
/tmp/short.png: data
```

`data`。这正是「magic bytes 是必要条件而非充分条件」的直接证据。

做题时如果 `file` 报 `data`，别急着换工具——先 `xxd` 看头 16 字节，再对照上面那张表。

</details>

---

## 12.2 前缀垃圾与伪头

### 跑通

```console
$ file samples/S-04.gz
static/samples/S-04.gz: OpenPGP Public Key

$ xxd -l 8 samples/S-04.gz
00000000: 9959 f1bf a35c a775                      .Y...\.u
```

`file` 说它是 **PGP 公钥**。而它的真实身份是 **gzip 压缩包**，只是前面塞了 32 字节垃圾。

第 1 章 和 第 7 章 已经用过这个文件，这里把它作为「前缀垃圾」的标准案例收进本章。

另一种手法是**贴伪头**——把 A 的签名贴在 B 前面：

```console
$ { printf '\x89PNG\r\n\x1a\n'; cat samples/S-03.zip; } > /tmp/fake.png
$ file /tmp/fake.png
/tmp/fake.png: Zip archive, with extra data prepended
```

### 机制

「被动过开头」有两种，`file` 的反应完全不同：

| 手法 | 做法 | `file` 的反应 |
| --- | --- | --- |
| 前缀垃圾 | 随机字节 + 真数据 | **可能误判成别的格式**（S-04 → PGP 公钥） |
| 贴伪头 | 别的格式的正确签名 + 真数据 | 通常报 `with extra data prepended` |

为什么前者会误判：`file` 的规则库是按「开头几个字节匹配什么特征」写的。`99 59 f1 bf` 恰好落在 PGP 公钥的判定范围内，于是它给出了一个自信的错误答案。**规则库是经验性的，不是格式规范。**

`with extra data prepended` 这句提示极有价值：它明确告诉你「**前面有多余数据**」。看到它，下一步就是找真实格式的起点。

找法就是 第 7 章 学过的：读全 → `find` 魔数 → 判 `-1` → 切片。

```console
$ python3 -c "
d = open('samples/S-04.gz','rb').read()
print(d.find(b'\x1f\x8b\x08'))
"
32
```

> **实践**　`file` 的输出里出现 `with extra data`、`data`、或者一个你完全没预期的类型时，一律回到 `xxd`。**三种情况都意味着「它在猜」。**

### 速查

| 手法 | 你该做什么 |
| --- | --- |
| 改扩展名 | 直接信 `file`（它不看扩展名） |
| 前缀垃圾 | 用 `find` 搜魔数，从命中处切 |
| 贴伪头 | 同上；`file` 已经提示了 |
| 尾部追加 | 见 12.4，`file` **完全看不出** |

### 题 U12.2-01

`file samples/S-04.gz` 输出什么？（照抄冒号后面那一部分）

<details><summary>提示</summary>

它被前 32 字节垃圾骗了，报了一个完全不相干的格式。

</details>

<details><summary>答案</summary>

```console
$ file samples/S-04.gz
static/samples/S-04.gz: OpenPGP Public Key
```

`OpenPGP Public Key`。这是「`file` 会自信地说错」的最好例子。

注意它在 第 1 章 里出现过一次、第 7 章 里用 `find` 推翻了结论——本章是第三次见同一个文件，但角度是「伪头/前缀」这一类手法，而不是「怎么解压」。**贯穿样本就是这么用的：同一个文件，每次换一个角度看。**

</details>

---

## 12.3 伪加密与 CRC 不符

### 跑通

```console
$ python3 -c "
import zipfile
zi = zipfile.ZipFile('samples/S-03.zip').infolist()[0]
print(hex(zi.flag_bits), zi.filename)
"
0x1 readme.txt

$ python3 -c "
import zipfile
print(zipfile.ZipFile('samples/S-03.zip').read('readme.txt'))
"
RuntimeError: File 'readme.txt' is encrypted, password required for extraction
```

标志位说「已加密」，所以工具拒绝解压。但**数据本身没有加密**——把标志位清掉就能读：

```console
$ python3 -c "
import io, struct, zipfile
d = bytearray(open('samples/S-03.zip','rb').read())
for sig, off in ((b'PK\x03\x04', 6), (b'PK\x01\x02', 8)):
    i = 0
    while True:
        j = d.find(sig, i)
        if j < 0: break
        f = struct.unpack('<H', d[j+off:j+off+2])[0] & ~1
        d[j+off:j+off+2] = struct.pack('<H', f)
        i = j + 4
print(zipfile.ZipFile(io.BytesIO(bytes(d))).read('readme.txt').decode().strip())
"
S03 zip payload: 0x5A
```

第二个样本换一种「被改过」——PNG 的宽高被改小，CRC 没跟着重算：

```console
$ python3 -c "
import struct, zlib
d = open('samples/S-02.png','rb').read()
w, h = struct.unpack('>II', d[16:24])
crc = struct.unpack('>I', d[29:33])[0]
real = zlib.crc32(b'IHDR' + d[16:29]) & 0xFFFFFFFF
print('宽', w, '声称高', h, '文件CRC', hex(crc), '实算CRC', hex(real))
"
宽 64 声称高 32 文件CRC 0x250be689 实算CRC 0x2dffe9d3
```

两个 CRC 不一致，说明 IHDR 的内容被改过。

### 机制

**伪加密**利用的是「标志位」和「实际加密」是两件事：

- ZIP 的每个条目有一个 2 字节的「通用标志」字段，第 0 位（值 1）表示「本条目已加密」；
- 真正的加密（ZipCrypto 或 AES）会在数据前加 12 字节左右的加密头，并在中央目录里记录压缩方法；
- **只把第 0 位置 1、不加加密头**，就是伪加密：所有工具都会以为要密码，但数据是明文。

要改两处，因为工具会交叉检查：

| 位置 | 偏移（从 `PK\x03\x04` 起） | 偏移（从 `PK\x01\x02` 起） |
| --- | --- | --- |
| 通用标志字段 | +6 | +8 |
| 要清的位 | 第 0 位（`& ~1`） | 第 0 位（`& ~1`） |

只改本地头不改中央目录，某些工具仍会报错；只改中央目录不改本地头，另一些会报错。**两处都改**才是稳的。

**CRC 是校验，不是加密。** PNG 每个块末尾有 4 字节 CRC，是块名与块数据的 CRC-32。改块内容不重算 CRC，就会出现「文件 CRC ≠ 实算 CRC」。

这给了一个可用的推理方向：**CRC 不符的地方，就是被改过的地方**。S-02 的 IHDR 被改了高度，于是暴露出来。反过来，如果知道正确 CRC，还能暴力反推出被改的 4 字节里应该是什么——那是 Part 2 的处理手法（宽度被改的题常这么做）。

> **易错**　不是所有工具都检查 CRC。多数图片查看器会忽略 CRC 不符，照样把图渲染出来（S-02 就是只显示上半部分）。所以「图能打开」不能证明「文件没被动过」。

### 速查

「被动过」的常见信号与检测方法：

| 信号 | 怎么查 | 说明 |
| --- | --- | --- |
| 标志位声明加密但解压时不需要密码 | `infolist()[0].flag_bits` | 伪加密 |
| 块 CRC 与实算不符 | `zlib.crc32(块名+数据)` | 内容被改 |
| 文件长度不是格式规范里的值 | `len(data)` 与结构字段对比 | 有附加数据 |
| 宽高与像素数据量对不上 | 像素数 × 通道数 vs IDAT 解压长度 | 尺寸被改 |
| 时间戳早于文件内容引用的版本 | `exiftool` | 伪造痕迹 |

### 题 U12.3-01

`samples/S-03.zip` 里那个条目的加密标志位（`flag_bits`）是多少？输出十进制。

<details><summary>提示</summary>

它是「已加密」这个声明的值，也就是第 0 位置 1 的结果。

</details>

<details><summary>答案</summary>

```console
$ python3 -c "
import zipfile
print(zipfile.ZipFile('samples/S-03.zip').infolist()[0].flag_bits)
"
1
```

十进制 1，也就是只有第 0 位被置了。

如果它是真加密，`flag_bits` 同样是 1——**光看标志位分不出真假**。区分要靠「清掉标志位后能不能解开」：能解开就是伪加密。

</details>

### 题 U12.3-02

`samples/S-02.png` 的 IHDR 声称高度是多少像素？输出十进制。

<details><summary>提示</summary>

IHDR 数据从偏移 16 开始，宽占 `16:20`，高占 `20:24`，大端。

</details>

<details><summary>答案</summary>

```console
$ python3 -c "
import struct
d = open('samples/S-02.png','rb').read()
print(struct.unpack('>II', d[16:24])[1])
"
32
```

声称 32，实际 64（第 7 章 自检里算过）。

差出来的那一半就是被藏起来的内容——这是「改高度」类隐写的标准形态。恢复方法：重算 CRC 后暴力试高度，直到 CRC 匹配。Part 2 会遇到。

</details>

---

## 12.4 附加数据与逻辑末尾

### 跑通

```console
$ python3 -c "
d = open('samples/S-03.zip','rb').read()
i = d.rfind(b'PK\x05\x06')
print('总长', len(d), 'EOCD 偏移', i)
print('尾部长度', len(d) - (i + 22))
print(repr(d[i+22:]))
"
总长 167 EOCD 偏移 118
尾部长度 27
b'\nS03-TRAILER-appended-note\n'
```

ZIP 的结尾是一个叫 **EOCD**（End of Central Directory）的 22 字节结构，签名 `PK\x05\x06`。按格式规范，文件到这里就该结束了。但它后面还有 **27 字节**，内容是 `S03-TRAILER-appended-note`。

### 机制

**「文件的长度」和「格式的逻辑末尾」是两件事。** 解析器按规范读到 EOCD 就停，剩下的字节它不看——这正是尾部追加能藏东西的原因。

不同格式的「逻辑末尾」各不相同：

| 格式 | 逻辑末尾 | 找法 |
| --- | --- | --- |
| ZIP | EOCD（`PK\x05\x06`）之后 22 字节 | `rfind(b'PK\x05\x06')` |
| PNG | `IEND` 块之后 12 字节 | `find(b'IEND')` |
| GZIP | 解压流结束处 | 长度写在流尾 4 字节（ISIZE） |
| JPEG | `FF D9` 之后 | `rfind(b'\xff\xd9')` |
| PDF | `%%EOF` 之后 | `rfind(b'%%EOF')` |

**为什么用 `rfind` 而不是 `find`**：尾部追加时，真数据在文件**末尾**，而文件开头可能也有同名的签名（比如一个 ZIP 里嵌套 ZIP）。取最后一次出现的位置，才切得到最后附加的那一段。

但也别盲信 `rfind`：如果附加的数据本身也是个 ZIP（常见于「图片里塞压缩包」），`rfind(b'PK\x03\x04')` 会命中**内层 ZIP 的某个条目头**而不是它的开头。稳妥做法是同时打印所有命中位置，人工看一眼哪个偏移之后的内容能独立解开：

```console
$ python3 -c "
d = open('samples/S-03.zip','rb').read()
pos = [i for i in range(len(d)) if d.startswith(b'PK\x03\x04', i)]
print(pos)
"
```

> **实践**　`file` 对尾部追加**完全无感**——它会正常报 `PNG image data` / `Zip archive data`，因为前面确实是一个合法文件。所以「类型对、能打开」不等于「没藏东西」。

### 速查

| 目标 | 写法 |
| --- | --- |
| 找某签名最后一次出现 | `d.rfind(b'签名')` |
| 找所有出现位置 | `[i for i in range(len(d)) if d.startswith(sig, i)]` |
| 切出尾部 | `d[i:]` |
| 算尾部长度 | `len(d) - (i + 22)`（ZIP 的 22 是 EOCD 长度） |
| 判断 PNG 是否有多余数据 | `i = d.find(b'IEND'); len(d) - (i + 8)` |

### 题 U12.4-01

`samples/S-03.zip` 的 EOCD 之后还有多少字节？输出十进制。

<details><summary>提示</summary>

先 `rfind(b'PK\x05\x06')` 找到 EOCD 起点，EOCD 本身占 22 字节。

</details>

<details><summary>答案</summary>

```console
$ python3 -c "
d = open('samples/S-03.zip','rb').read()
print(len(d) - (d.rfind(b'PK\x05\x06') + 22))
"
27
```

内容就是那句 `S03-TRAILER-appended-note`（外面还包了两个换行）。

这 27 字节在真实题目里可能是一整段 flag、一个内嵌 ZIP、或者一张图片。判断方式一样：**先算长度差，再把尾部切出来单独 `file` 一下。**

</details>

---

## 12.5 自检

### U12.5-01

`b'PK\x03\x04'` 的十六进制表示是什么？

<details><summary>提示</summary>

四个字节，每个字节两位十六进制。`P` 是 `0x50`，`K` 是 `0x4B`。

</details>

<details><summary>答案</summary>

```console
$ python3 -c "print(b'PK\x03\x04'.hex())"
504b0304
```

`50` = `P`、`4B` = `K`、`03 04` 是 ZIP 本地文件头的版本字段。

记住这个串后面很有用：做题时看到 `504b0304` 就知道「这是一个 ZIP 的开始」，不必再看 ASCII 那一列。

</details>

### U12.5-02

不修改任何字节，直接用 `zipfile` 读 `samples/S-03.zip` 里的 `readme.txt`，会抛出哪种异常？给出异常类名。

<details><summary>提示</summary>

标志位说加密了，`zipfile` 会拒绝而不是返回错误数据。

</details>

<details><summary>答案</summary>

```console
$ python3 -c "
import zipfile
try:
    zipfile.ZipFile('samples/S-03.zip').read('readme.txt')
except Exception as e:
    print(type(e).__name__)
"
RuntimeError
```

`RuntimeError`，消息是 `File 'readme.txt' is encrypted, password required for extraction`。

注意它**没有**抛 `BadZipFile`——文件结构是好的，只是被标志位拦住了。这个区别很重要：`BadZipFile` 意味着文件真的坏了，`RuntimeError` 意味着「需要密码」。看到后者，先怀疑伪加密。

</details>

### U12.5-03

`samples/S-03.zip` 里那个条目的文件名是什么？

<details><summary>提示</summary>

列 `infolist()` 拿第一个的名字。伪加密不影响列目录。

</details>

<details><summary>答案</summary>

```console
$ python3 -c "
import zipfile
print(zipfile.ZipFile('samples/S-03.zip').infolist()[0].filename)
"
readme.txt
```

伪加密只拦「读内容」，不拦「读目录」。这是因为文件名和大小存在中央目录里，没被加密。

做题时这一点有用：**即使解不开，也能知道里面有哪些文件、各多大**，据此判断值不值得去破。

</details>

---

## 12.6 动手

### U12.6-01 给四个样本写一份「被动过」清单

对 `samples/` 下的 `S-01.png`、`S-02.png`、`S-03.zip`、`S-04.gz` **各写一段**，每段包含：

1. `file` 的原样输出；
2. 你的判断：它是正常文件，还是被动过？被动的是哪一处？
3. 你用什么命令确认的（贴出来）；
4. 如果藏着东西，藏的是什么、在哪个偏移。

要求：**S-01 要判为正常**（它是本章的反例——不是每个样本都被动过）。S-02、S-03、S-04 各对应一节讲的手法，要能对上号。

<details><summary>提示</summary>

- S-02：算 IHDR 的 CRC，和文件里存的比。
- S-03：看 `flag_bits`，再算 EOCD 之后剩多少字节。
- S-04：头 8 字节是不是 gzip？不是的话用 `find` 搜 `1f 8b 08`。
- S-01：`file` 说 PNG，CRC 对不对？有没有多余字节？

</details>

<details><summary>答案（四段的关键结论）</summary>

| 样本 | `file` 说 | 判断 | 依据 |
| --- | --- | --- | --- |
| S-01.png | `PNG image data, 64 x 64, ...` | **正常** | IHDR CRC 相符；IEND 之后无剩余字节；LSB 里的东西是**内容层**隐写，不是文件结构被改 |
| S-02.png | `PNG image data, 64 x 32, ...` | 被改过 | IHDR CRC 不符（文件 `0x250be689`，实算 `0x2dffe9d3`）；实际像素数据是 64×64 |
| S-03.zip | `Zip archive data, ...` | 被改过两处 | ① `flag_bits=0x1` 但清位后可读 → 伪加密；② EOCD 之后多 27 字节 → 尾部附加 |
| S-04.gz | `OpenPGP Public Key` | 被改过 | 真实数据从偏移 32 开始（`1f 8b 08`），前面是垃圾前缀 |

**S-01 是本章最重要的一行。** 它的 `file` 输出、CRC、长度全都正常，但它确实藏了东西（`S01-LSB-OK`，第 8 章 动手题解过）。这说明：

- 「结构正常」和「没有藏东西」是两件事；
- 结构检查只能发现**结构层**的改动，内容层的隐写（LSB、频谱、元数据）要靠 Part 2 的手段。

**这也是 Part 2 的起点。** 本章教的是「先证明文件结构被动过」，Part 2 教的是「结构没问题时，怎么证明内容里藏了东西」。

</details>

---

## 小结

- `file` 读内容、不看扩展名；它的判断是**必要条件 + 结构验证**，两步都过才给结论。
- `data` 意味着「没认出」，不是「不正常」。`with extra data prepended` 意味着「前面有多余数据」。
- 前缀垃圾能让 `file` 自信地报错类型（S-04 → PGP 公钥）。看到意外类型一律回 `xxd`。
- 伪加密 = 标志位置 1 但没有真加密。要同时改本地头和中央目录两处。
- CRC 是校验不是加密；块 CRC 不符 = 那块被改过。
- 文件长度 ≠ 格式逻辑末尾。尾部附加用 `rfind` 找，别用 `find`。
- **结构正常 ≠ 没藏东西。** S-01 全部结构指标正常，但 LSB 里有一整句话。

## 术语

| 中文 | English | 定义 |
| --- | --- | --- |
| 文件签名 | magic bytes | 文件开头的固定字节，用于标识格式 |
| 前缀垃圾 | junk prefix | 贴在真实数据前面的无关字节 |
| 伪装头 | fake header | 把 A 的签名贴在 B 前面 |
| 伪加密 | pseudo-encryption | 只置「已加密」标志位而不真正加密数据 |
| 附加数据 | appended data | 格式逻辑末尾之后多出来的字节 |
| EOCD | End of Central Directory | ZIP 的结尾结构，签名 `PK\x05\x06`，22 字节 |
| 校验和 | checksum / CRC | 用于检测内容被改的短值，不提供保密性 |

## 延伸

- `man file`、`man 5 magic`：`file` 的判断规则来源。看懂 `magic` 文件能自己加规则。
- `binwalk`、`foremost`：自动扫描嵌入文件与文件雕刻。本课不依赖它们，因为 WSL 里没有预装，而手工 `find` 已经够用。
- ZIP 格式规范：PKWARE APPNOTE。查「General purpose bit flag」和「End of central directory record」两节即可。
