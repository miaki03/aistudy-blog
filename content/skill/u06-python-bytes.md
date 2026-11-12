+++
date = '2026-11-10T12:00:00+08:00'
draft = false
title = 'U06 · Python 与字节：str 和 bytes 是两种东西'
description = 'encode/decode、编解码失败、字节切片与整数互转、读二进制文件。这一章之后你就能用 Python 直接动样本文件了。'
slug = 'u06-python-bytes'
chapter = 'U06'
stage = 0
minutes = 120
prereq = ['U00', 'U05']
concepts = ['bytes-type', 'encode-decode', 'endianness']
reuse = ['U12', 'U21', 'U22', 'U31', 'U41', 'U61']
skills = ['python', 'bytes']
problems = ['U06.1-01', 'U06.2-01', 'U06.3-01', 'U06.4-01', 'U06.5-01', 'U06.5-02', 'U06.5-03', 'U06.6-01']
+++

## 读完能做什么

1. 说出 `str` 和 `bytes` 的区别，并在两者之间正确转换，不再踩 `TypeError`。
2. 用 `int.from_bytes` / `to_bytes` 在字节与整数之间互转，并指定字节序。
3. 用 `open(路径, "rb")` 读一个二进制文件，按偏移切出任意一段，并对它做后续处理。

U05 里所有例子处理的都是**文本**。这一章开始处理**字节**——图片、压缩包、抓包，后面 20 多章的主战场。

## 前置

U00（字节、十六进制）、U05（`with open`、切片、函数）。样本 `samples/S-01.png` 和 `samples/S-04.gz`。

---

## 3.1 str 与 bytes 是两种东西

### 跑通

```console
$ python3 -c 'print("abc".encode())'
b'abc'

$ python3 -c 'print("你好".encode())'
b'\xe4\xbd\xa0\xe5\xa5\xbd'

$ python3 -c 'print(len("你好".encode()))'
6
```

`"你好"` 是两个字符、六个字节。`encode()` 把 `str` 变成 `bytes`，`decode()` 反过来。

### 机制

Python 里这是**两个完全不同的类型**，不能混用：

| 类型 | 是什么 | 字面量 | 下标取出什么 |
| --- | --- | --- | --- |
| `str` | Unicode 字符序列 | `"abc"` | 一个字符 `"a"` |
| `bytes` | 字节序列 | `b"abc"` | 一个整数 `97` |

混用会直接报错，不给你含糊空间：

```console
$ python3 -c "print('abc' + b'def')"
TypeError: can only concatenate str (not "bytes") to str
```

这条报错值得记住。它的意思是「`str` 只能和 `str` 相加」。修法只有两种：把 `'abc'` 编码成 `b'abc'`，或者把 `b'def'` 解码成 `'def'`。选哪个取决于你最终要的是文本还是字节。

**为什么必须有这个区分**：`str` 的「长度」是字符数，`bytes` 的「长度」是字节数。U00 已经证过这两者可以差 3 倍。如果 Python 允许混用，`len(x)` 到底指哪个就说不清了。C 语言里 `char*` 混着用，就是这个问题的来源。

**为什么 `b'abc'` 看起来和 `'abc'` 一样**：因为 ASCII 范围内两者字节相同。一旦超出 0x7F 就露出真相：

```console
$ python3 -c "print(b'\xe4\xbd\xa0\xe5\xa5\xbd')"
b'\xe4\xbd\xa0\xe5\xa5\xbd'
```

`bytes` 打印时会把不可打印的字节显示成 `\xNN`，这是为你好——直接往终端怼 6 个原始字节，屏幕上只会是乱码。

> **易错**　`open(p)` 读出来是 `str`，`open(p, "rb")` 读出来是 `bytes`。**对同一个二进制文件用前者，会在读的那一步抛 `UnicodeDecodeError`**，而不是等到你用的时候。看到这个错，先检查 `open` 有没有加 `"rb"`。

### 速查

| 操作 | 写法 |
| --- | --- |
| str → bytes | `s.encode()`（默认 UTF-8） |
| bytes → str | `b.decode()`（默认 UTF-8） |
| 指定编码 | `s.encode("gbk")` / `b.decode("latin-1")` |
| 字节字面量 | `b"\x89PNG"` |
| 从整数造字节 | `bytes([0x89, 0x50])` |
| 字节长度 | `len(b)`（字节数） |
| 字符长度 | `len(s)`（字符数） |

### 题 U06.1-01

`"你好".encode()` 的结果有多少字节？只输出数字。

<details><summary>提示</summary>

U00 讲过 UTF-8 里一个汉字占 3 字节。`len()` 作用于 `bytes` 时数的是字节。

</details>

<details><summary>答案</summary>

```console
$ python3 -c 'print(len("你好".encode()))'
6
```

两个汉字 × 3 字节 = 6。对比 `len("你好")` 得 2。

**同一段内容，两个不同的长度，取决于你问的是谁。** 后面算 Base64 长度、算 padding、算文件偏移，用的都是字节数。

</details>

---

## 3.2 编解码失败，与 `errors` 参数

### 跑通

```console
$ python3 -c "print(b'\xff'.decode())"
Traceback (most recent call last):
  File "<string>", line 1, in <module>
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xff in position 0: invalid start byte
```

`0xff` 在 UTF-8 里不是合法的起始字节（U00 讲过：合法起始字节只有 `0xxxxxxx`、`110xxxxx`、`1110xxxx`、`11110xxx` 四种模式，`FF` = `1111 1111` 不匹配任何一个）。

换一种处理方式就不报错：

```console
$ python3 -c "print(repr(b'\xff'.decode('utf-8', errors='replace')))"
'�'
```

### 机制

`decode()` 遇到不合法字节时，`errors` 参数决定怎么办：

| 取值 | 行为 | 结果长度 |
| --- | --- | --- |
| `'strict'`（默认） | 抛 `UnicodeDecodeError` | — |
| `'replace'` | 每个不可解码的**片段**换成一个 `U+FFFD`（显示为 `�`） | 会变短 |
| `'ignore'` | 直接丢掉 | 会变短 |

注意 `'replace'` 的粒度是「片段」不是「字节」：

```console
$ python3 -c "print(len(b'\xe4\xbd'.decode('utf-8', errors='replace')))"
1
```

`e4 bd` 是「声称 3 字节但只有 2 字节」的残缺序列，算**一个**片段，所以只替换成 1 个 `�`。

**这三种取值的用途完全不同**：

- `'strict'` 用来**判断**。想知道「这到底是不是合法 UTF-8」，就让它抛异常——这是 U00 里文本/二进制判据的基础。
- `'replace'` 用来**看**。分析一个二进制文件时，用它把可读部分捞出来，`�` 的位置就告诉你哪里是数据、哪里是文本。
- `'ignore'` 用来**丢**。只在明确不关心无效部分时用，因为它会静默改变长度，很危险。

> **易错**　`errors='ignore'` 处理完的字符串长度可能和原始字节数差很远，而且**没有任何提示**。用它之后再算偏移，一定错位。调试阶段一律用 `'replace'`，能看见 `�` 才知道丢了东西。

### 题 U06.2-01

`b'\xe4\xbd'.decode('utf-8', errors='replace')` 的结果有几个字符？

<details><summary>提示</summary>

`e4 bd` 不构成一个完整字符。`'replace'` 是按「不可解码的片段」替换，不是按字节。

</details>

<details><summary>答案</summary>

```console
$ python3 -c "print(len(b'\xe4\xbd'.decode('utf-8', errors='replace')))"
1
```

整个残缺序列只替换成 1 个 `U+FFFD`。如果按字节替换，这里会是 2。

换成 `errors='ignore'` 则得到空字符串，长度 0——**两个字节凭空消失**。这就是上面说的危险：用 `ignore` 之后你对「有多少内容」的判断就全错了。

</details>

---

## 3.3 字节的切片、索引与整数互转

### 跑通

```console
$ python3 -c "d = b'ABCD'; print(d[0], d[0:2], type(d[0:2]).__name__)"
65 b'AB' bytes

$ python3 -c "print(b'A'[0], b'A' == 65, b'abc' == 'abc')"
65 False False
```

三件事一起看：

- `d[0]` 取出的是**整数 65**，不是 `b'A'`；
- `d[0:2]` 取出的是**bytes** `b'AB'`，切片永远返回同类型；
- `b'A' == 65` 是 `False`——`bytes` 和整数不是同一个东西，即使「值看起来一样」。

```console
$ python3 -c "print(b'\x89PNG'.hex())"
89504e47
```

```console
$ python3 -c "print(int.from_bytes(b'\x00\x00\x00\x40', 'big'))"
64
$ python3 -c "print((64).to_bytes(4, 'big').hex())"
00000040
```

### 机制

**索引给整数，切片给 bytes。** 这条规则没有例外，记住它就不会在写循环时把 `d[i]` 当字节串用。

**`.hex()` / `bytes.fromhex()`** 是字节与十六进制串之间的桥。分析文件时几乎每个脚本都会用到 `.hex()`——它把字节变成 U00 里那种可读的十六进制写法。

**字节序（endianness）** 是这一节最容易混的东西。4 个字节 `00 00 00 40` 表示多大的数，取决于从哪头读：

| 顺序 | 读法 | 结果 |
| --- | --- | --- |
| big（大端） | 最高位字节在前 | 64 |
| little（小端） | 最低位字节在前 | 1073741824 |

`int.from_bytes(data, 'big')` 和 `int.from_bytes(data, 'little')` 就差这一个字，结果可能差 1680 万倍。

> **约定**　网络协议、PNG、JPEG、ZIP 用**大端**（网络字节序）。x86 的 CPU、ELF、Windows 的 PE 用**小端**。所以抓包和图片文件用 `'big'`，逆向可执行文件时看到的多是 `'little'`。**判断依据不是猜，是看格式文档或者先试一次哪个数看起来合理。**

**为什么 `(64).to_bytes(4, 'big')` 要写 4**：因为 `to_bytes` 必须知道占几个字节。它不会自动选最短的，你要明确说。这也是为什么读字节比写字节简单——读的时候长度由切片决定。

### 速查

| 操作 | 写法 |
| --- | --- |
| 索引（得整数） | `d[i]` |
| 切片（得 bytes） | `d[a:b]` |
| 字节 → hex 串 | `d.hex()` |
| hex 串 → 字节 | `bytes.fromhex(s)` |
| 字节 → 整数 | `int.from_bytes(d, 'big')` |
| 整数 → 字节 | `n.to_bytes(长度, 'big')` |
| 整数列表 → 字节 | `bytes([0x89, 0x50])` |
| 字节拼接 | `a + b`（两边都必须是 bytes） |
| 字节分割 | `d.split(b'\x00')`（分隔符必须是 bytes） |
| 查找子串位置 | `d.find(b'\x1f\x8b')`（找不到返回 -1） |

### 题 U06.3-01

`(64).to_bytes(4, 'big')` 的十六进制表示是什么？

<details><summary>提示</summary>

大端意味着高位字节在前。64 的十六进制是 `40`，要占 4 个字节就得在前面补三个 `00`。

</details>

<details><summary>答案</summary>

```console
$ python3 -c "print((64).to_bytes(4, 'big').hex())"
00000040
```

换成 `'little'` 是 `40000000`。**同一句话的两种编码，只差字节序声明**——这正是后面读文件头时最容易搞错的地方。

</details>

---

## 3.4 读二进制文件

### 跑通

```console
$ python3 -c "
with open('samples/S-04.gz','rb') as f:
    print(f.read(8).hex())
"
9959f1bfa35ca775
```

`S-04.gz` 的前 8 字节根本不是 gzip。U00 里已经踩过一次：`file` 说它是 PGP 公钥，因为它只看了开头。

真正的 gzip 数据从这里开始：

```console
$ python3 -c "
d = open('samples/S-04.gz','rb').read()
print(len(d))
print(d.find(b'\x1f\x8b\x08'))
print(d[32:40].hex())
"
83
32
1f8b080000000000
```

文件 83 字节，前 32 字节是垃圾，从偏移 32 开始才是 `1f 8b 08`。

### 机制

`open(p, "rb")` 的三种读法，按用途选：

| 写法 | 得到 | 用途 |
| --- | --- | --- |
| `f.read()` | 全部内容，一个 `bytes` | 小文件、需要反复切片 |
| `f.read(n)` | 前 n 字节 | 只看文件头 |
| `for chunk in f:` | 逐行 bytes（**按 `\n` 切**） | 大文本类文件，不推荐用于二进制 |

二进制文件用 `f.read()` 一次性读进内存最省事——样本都在 MB 级以下。真的遇到大文件（几百 MB 的抓包、磁盘镜像）再改用 `f.read(chunk_size)` 分块，本章不涉及。

**`find` 是这一节的核心动作。** `d.find(b'\x1f\x8b\x08')` 返回第一个匹配的起始偏移，找不到返回 `-1`。所以「在一个脏文件里定位真实数据」这件事，标准写法就是：

```python
d = open(path, "rb").read()
off = d.find(b"\x1f\x8b\x08")   # 魔数（U12 会系统讲）
if off < 0:
    print("没有 gzip 数据")
else:
    real = d[off:]              # 从这里切到末尾
```

最后一步 `d[off:]` 拿到干净的 gzip 字节流，交给 `gzip.decompress` 就能解：

```console
$ python3 -c "
import gzip
d = open('samples/S-04.gz','rb').read()
print(gzip.decompress(d[32:]).decode().strip())
"
S04 gzip payload: offset-found
```

**这里出现了两次「切」**：先切掉垃圾前缀（`d[32:]`），解压后又用 `.decode()` 变成 `str` 才能 `strip()`。每一步都在换类型：`bytes` → `bytes` → `str`。写脚本时脑子里要一直有这根线。

> **实践**　`find` 找不到时返回 `-1`，而 `d[-1:]` 是**最后一个字节**，不是空。所以必须显式判断 `if off < 0`，否则你会拿着文件末尾的一个字节继续往下跑，报出的错离真正原因很远。

### 题 U06.4-01

`S-04.gz` 里 gzip 数据的起始偏移是多少（十进制）？只输出数字。

<details><summary>提示</summary>

gzip 的固定开头是 `1f 8b 08`。用 `.find()` 找它，或者直接看 U00 里 `xxd -s 32` 的输出。

</details>

<details><summary>答案</summary>

```console
$ python3 -c "print(open('samples/S-04.gz','rb').read().find(b'\x1f\x8b\x08'))"
32
```

注意这里用的是 `static/samples/` 下的真实路径；你本地按实际位置写。

`1f 8b 08` 三个字节里，`1f 8b` 是 gzip 的魔数，`08` 是压缩方法（8 = deflate）。三者一起匹配能大幅降低误命中。

</details>

---

## 5 自检

### U06.5-01

`b'abc' == 'abc'` 的结果是什么？输出 `True` 或 `False`。

<details><summary>提示</summary>

`bytes` 和 `str` 是两种类型。Python 里不同类的对象比较相等，只有在该类自己定义了比较规则时才可能为真。

</details>

<details><summary>答案</summary>

```console
$ python3 -c "print(b'abc' == 'abc')"
False
```

同理 `b'A' == 65` 也是 `False`，尽管 `b'A'[0]` 就是 65。

这两个 `False` 是同一类 bug 的源头：**看起来一样，类型不同，比较永远为假且不报错**。U05 里 `int` 与 `str` 比较也是这个问题。养成习惯：比较之前先确认两边的类型。

</details>

### U06.5-02

`samples/S-01.png` 的 PNG 宽度是多少像素？只输出数字。

<details><summary>提示</summary>

PNG 的 IHDR 块从偏移 16 开始，前 4 字节是宽，后 4 字节是高，**大端**。用 `int.from_bytes(d[16:20], 'big')`。

</details>

<details><summary>答案</summary>

```console
$ python3 -c "
d = open('samples/S-01.png','rb').read()
print(int.from_bytes(d[16:20], 'big'))
"
64
```

高在 `d[20:24]`，也是 64（这个样本是正方形）。

偏移 16 是怎么来的：PNG 签名 8 字节 + 块长度 4 字节 + 块名 4 字节 = 16，之后才是 IHDR 的数据。U21 会把这个结构完整讲一遍。

</details>

### U06.5-03

`b'A'[0]` 输出什么？

<details><summary>提示</summary>

`bytes` 的索引用整数，不是 `str` 那样的单字符。

</details>

<details><summary>答案</summary>

```console
$ python3 -c "print(b'A'[0])"
65
```

65 就是 `0x41`，U00 里查过的那张 ASCII 表。

对比 `'A'[0]` 得 `'A'`。**同一个下标操作，`bytes` 给数字，`str` 给字符**——这一条区别决定了写循环时的写法：处理字节时 `for b in data:` 里的 `b` 是整数，要转字符得 `chr(b)`。

</details>

---

## 6 动手

### U06.6-01 从脏文件里挖出内容

写一个脚本 `dig.py`，对 `samples/S-04.gz` 完成三件事，并把结果打印出来：

1. 文件总字节数；
2. gzip 数据起始偏移（若找不到，打印「没有 gzip 数据」并退出）；
3. 切出 gzip 部分、解压、去掉首尾空白后打印那行文本。

要求：**不使用 `gzip.decompress(d[32:])` 这种写死偏移的写法**，必须用 `find` 动态定位。

参考输出：

```console
83
32
S04 gzip payload: offset-found
```

<details><summary>提示</summary>

1. `len(d)` 得总字节数；
2. `d.find(b"\x1f\x8b\x08")` 得偏移，记得判 `-1`；
3. `import gzip`，`gzip.decompress(d[off:])` 得 bytes，再 `.decode().strip()`。

</details>

<details><summary>答案</summary>

```python
import gzip

d = open("samples/S-04.gz", "rb").read()
print(len(d))

off = d.find(b"\x1f\x8b\x08")
if off < 0:
    print("没有 gzip 数据")
    raise SystemExit(1)

print(off)
print(gzip.decompress(d[off:]).decode().strip())
```

```console
$ python3 dig.py
83
32
S04 gzip payload: offset-found
```

`raise SystemExit(1)` 是「带失败状态退出」。用 `exit()` 也行，但 `SystemExit` 在脚本里更明确，而且退出码非 0 能被 shell 的 `&&` 和 CI 感知。

这个脚本的形状（读全 → 找魔数 → 判断 → 切片 → 解 → 打印）就是后面所有「从脏文件里挖东西」的模板。U12 只是把 `find` 的魔数换成一张表。

</details>

---

## 小结

- `str` 是字符序列，`bytes` 是字节序列，两者不能混用，混用必报错。
- `encode()` / `decode()` 互转；默认 UTF-8。`len(str)` 数字符，`len(bytes)` 数字节。
- `errors='strict'` 判断、`'replace'` 查看、`'ignore'` 丢弃（危险）。
- 索引 `d[i]` 给整数，切片 `d[a:b]` 给 bytes；`.hex()` 是分析文件的主力工具。
- 字节序必须显式指定：网络协议与图片用 `'big'`，ELF/PE 用 `'little'`。
- 读二进制一律 `open(p, "rb")`。挖东西的模板是「读全 → `find` 魔数 → 判 `-1` → 切片 → 处理」。

## 术语

| 中文 | English | 定义 |
| --- | --- | --- |
| 字节串 | `bytes` | 不可变的字节序列，下标取出整数 |
| 编码 | encode | `str` → `bytes` |
| 解码 | decode | `bytes` → `str` |
| 字节序 | endianness | 多字节整数在内存里的排列顺序：大端高位在前，小端低位在前 |
| 替换字符 | U+FFFD | 解码失败时用来占位的字符，显示为 `�` |
| 魔数 | magic number | 文件开头用于标识格式的固定字节（U12 展开） |

## 延伸

- `python3 -c "help(bytes)"` 列出全部方法，`split` / `replace` / `startswith` 在字节上都有对应版本（参数必须是 bytes）。
- 完整的编码错误处理策略还有 `'backslashreplace'`、`'surrogateescape'`，本课用不到。
