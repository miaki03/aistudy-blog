+++
date = '2026-11-10T11:00:00+08:00'
draft = false
title = 'U02 · Python 最小可用：五件事够用'
description = '脚本、变量与字符串、列表与 for、if 与函数、读文件。只学这门课真正会用到的那部分，每节都跑得起来。'
slug = 'u02-python-min'
chapter = 'U02'
stage = 0
minutes = 140
prereq = ['U01']
concepts = ['script', 'variable', 'string', 'list', 'function', 'dict']
reuse = ['U21', 'U22', 'U30', 'U31', 'U41']
skills = ['python', 'scripting']
problems = ['U02.1-01', 'U02.2-01', 'U02.3-01', 'U02.4-01', 'U02.5-01', 'U02.6-01', 'U02.6-02', 'U02.6-03', 'U02.7-01']
+++

## 读完能做什么

1. 写出并运行一个 20 行以内的脚本，读一个文本文件、按字段筛选、输出统计结果。
2. 看懂别人给的 30 行脚本在做什么，并能改一行让它输出另一个字段。
3. 说出「终端一条命令」和「Python 脚本」各自适合什么场合。

这一章不教 Python 语言。它只教这门课后面 24 章**真的会用到**的五件事。面向对象、异常、装饰器、类型注解、异步，一律不碰。

## 前置

U01 的终端，以及 `samples/u01-access.log`。确认 Python 在：

```console
$ python3 --version
Python 3.12.3
```

如果 `python3` 不存在但 `python` 存在，把本章所有 `python3` 换成 `python` 即可，其余不变。

---

## 2.1 跑第一个脚本

### 跑通

新建一个文件 `hello.py`，内容就四行（`#` 开头是注释，不执行）：

```python
# 第一个脚本
print("hello")
print(2 ** 10)
```

运行它：

```console
$ python3 hello.py
hello
1024
```

### 机制

**脚本就是一个文本文件。** `python3` 是解释器，它读这个文件、按行执行、把 `print` 的内容送到标准输出。所以 U01 讲的三根标准流在这里同样成立——`python3 hello.py > out.txt` 一样能把输出收进文件。

三件在 Python 里必须一开始就知道的事：

**1. 缩进是语法，不是排版。** Python 用行首的空格数划分代码块，没有 `{}`。

**2. `print()` 是函数，括号不能省。** `print "hi"` 在 Python 3 里是语法错误。

**3. 字符串、数字、列表这些都有类型，但变量名没有。** 同一个名字可以先指向字符串，后面再指向列表——这是「名字绑定到对象」，不是「声明一个变量」。

> **易错**　从别处复制代码时，制表符（Tab）和空格混用会报 `TabError: inconsistent use of tabs and spaces in indentation`。统一用 4 个空格。

### 速查

| 操作 | 写法 |
| --- | --- |
| 运行脚本 | `python3 文件名.py` |
| 运行一行代码 | `python3 -c 'print(1+1)'` |
| 交互式试代码 | 直接敲 `python3`，出现 `>>>` 后逐行输入，`exit()` 退出 |
| 注释 | `#` 之后到行尾 |

### 题 U02.1-01

`print(len("你好"))` 会输出什么？

<details><summary>提示</summary>

U00 讲过：一个汉字在 UTF-8 里占 3 字节，但它是**一个字符**。`len()` 数的是字符还是字节？

</details>

<details><summary>答案</summary>

```console
$ python3 -c 'print(len("你好"))'
2
```

`len()` 数的是**字符**（更准确地说，是 Unicode 码位的个数）。要数字节得先编码：`len("你好".encode())` 得 6。

这是 U00 那条「字节数 ≠ 字符数」在 Python 里的直接体现。**凡是算长度、算偏移、算 padding，先问自己：这里要的是字节还是字符。**

</details>

---

## 2.2 变量与字符串

### 跑通

```python
name = "S-01.png"
print(len(name))
print(name[:4])
print(name.split(".")[1])
print(f"名字 {name} 后缀 {name.split('.')[1]}")
```

```console
$ python3 strs.py
8
S-01
png
名字 S-01.png 后缀 png
```

### 机制

**变量**是名字绑到对象上。`name = "S-01.png"` 之后，`name` 指向那个字符串对象。再写 `name = 5` 也合法，它就改为指向整数了。

**字符串是不可变的有序字符序列。** 不可变意味着 `name[0] = "X"` 会报错，要改只能造一个新字符串。

**切片 `[a:b]` 左闭右开**：`name[:4]` 取下标 0、1、2、3 共 4 个字符，不含下标 4。`name[2:5]` 取 2、3、4。省略左边表示从头，省略右边表示到末尾，负数从末尾数（`name[-4:]` 是最后 4 个字符）。

> **易错**　`name[:4]` 的长度是 4，不是 5。切片里的两个数字都是**边界下标**，不是「取几个」。`"S-01.png"[:4]` 得 `S-01`，四个字符。

**`split(sep)`** 按分隔符切成列表。`"S-01.png".split(".")` 得 `['S-01', 'png']`，再 `[1]` 取第二段。`.` 在 `split` 里是普通字符，不需要转义——但它在**正则表达式**里不是（到 U11 再讲）。

**`join`** 是 `split` 的反向：`"-".join(["a","b"])` 得 `a-b`。注意写法：分隔符在前，列表在后。

**f-string**（前缀 `f`）在字符串里用 `{}` 插值。要在结果里输出真的花括号，就写两层：`f"flag{{{name}}}"` → `flag{ok}`。外层 `{{` 表示一个字面 `{`。

### 速查

| 操作 | 写法 | 例子 |
| --- | --- | --- |
| 长度 | `len(s)` | `len("abc")` → 3 |
| 取字符 | `s[i]` | `"abc"[1]` → `b` |
| 切片 | `s[a:b]` | `"abcdef"[1:4]` → `bcd` |
| 末尾切片 | `s[-n:]` | `"abcdef"[-2:]` → `ef` |
| 切分 | `s.split(sep)` | `"a,b".split(",")` → `['a','b']` |
| 拼接 | `sep.join(列表)` | `"-".join(['a','b'])` → `a-b` |
| 去空白 | `s.strip()` | `"  hi ".strip()` → `hi` |
| 替换 | `s.replace(旧, 新)` | 全部替换 |
| 转小写 | `s.lower()` | |
| 找子串 | `s.find(x)` | 找不到返回 `-1` |
| 编码为字节 | `s.encode()` | 默认 UTF-8 |
| 字节解码 | `b.decode()` | |

### 题 U02.2-01

设 `name = "ok"`，`print(f"flag{{{name}}}")` 输出什么？

<details><summary>提示</summary>

`{{` 是转义后的一个字面 `{`。数一数原文里有几个花括号。

</details>

<details><summary>答案</summary>

```console
$ python3 -c 'name="ok"; print(f"flag{{{name}}}")'
flag{ok}
```

原文 `f"flag{{{name}}}"` 拆开看：`flag` + `{{` + `{name}` + `}}`。所以输出是 `flag` + `{` + `ok` + `}`。

这条后面用得很多：CTF 的 flag 格式就是 `flag{...}`，用 f-string 拼的时候少写一层括号就会变成 `flagok` 或者报错。

</details>

---

## 2.3 列表与 for

### 跑通

```python
lines = ["a 200", "b 404", "c 200"]
for i, line in enumerate(lines, 1):
    print(i, line.split()[1])
print([l.split()[1] for l in lines])
```

```console
$ python3 lists.py
1 200
2 404
3 200
['200', '404', '200']
```

### 机制

**列表是有序、可变的容器**，用 `[]` 写。和字符串最大的区别是能改：`lines.append("d 500")` 直接在末尾加一个。

**`for x in 序列`** 逐个取出元素。要同时拿到下标，用 `enumerate(序列, 起始值)`，它每轮给 `(下标, 元素)` 两样东西。起始值默认 0，写 `1` 就从 1 开始编号。

**`line.split()` 不传参数**时按「任意空白」切，并且会把连续空白合成一个分隔符。这正是 U01 说 `cut` 做不到、而 `awk` 能做到的那件事。所以处理字段数不定的文本时，`split()` 比 `cut` 稳。

**列表推导式 `[表达式 for 元素 in 序列 if 条件]`** 是「生成列表」的紧凑写法。上面 `[l.split()[1] for l in lines]` 等价于：

```python
result = []
for l in lines:
    result.append(l.split()[1])
```

推导式不是炫技，它的价值在于**不能有副作用**——只能算一个值出来，不能顺手改别的变量。这让它读起来比循环短且清楚。本章后面统计时一律用它做「筛 + 取」。

### 速查

| 操作 | 写法 | 结果 |
| --- | --- | --- |
| 建列表 | `[1, 2, 3]` | |
| 取元素 | `lst[0]` / `lst[-1]` | 第一个 / 最后一个 |
| 切片 | `lst[1:3]` | 第 1、2 个 |
| 追加 | `lst.append(x)` | 末尾加一个 |
| 长度 | `len(lst)` | |
| 排序 | `sorted(lst)` | 返回**新**列表 |
| 原地排序 | `lst.sort()` | 改自己，返回 `None` |
| 倒序 | `sorted(lst, reverse=True)` | |
| 按 key 排 | `sorted(lst, key=len)` | |
| 带下标遍历 | `for i, x in enumerate(lst, 1)` | |
| 推导式 | `[x * 2 for x in lst]` | |
| 带条件 | `[x for x in lst if x > 3]` | |

> **易错**　`sorted()` 返回新列表，`lst.sort()` 就地改且返回 `None`。写 `lst = lst.sort()` 会把列表变成 `None`。这个错误极其常见。

### 题 U02.3-01

`print([x * 2 for x in range(4)])` 输出什么？

<details><summary>提示</summary>

`range(4)` 产生 `0, 1, 2, 3`（含头不含尾）。

</details>

<details><summary>答案</summary>

```console
$ python3 -c 'print([x*2 for x in range(4)])'
[0, 2, 4, 6]
```

`range(4)` 是 0–3 共 4 个数，不是 0–4。这跟切片左闭右开是同一套约定：**Python 里凡是区间，含头不含尾。** 记住这一条，`range(len(x))` 就不会越界。

</details>

---

## 2.4 if 与函数

### 跑通

```python
def count_status(lines, code):
    n = 0
    for line in lines:
        if line.split()[4] == str(code):
            n += 1
    return n

with open("samples/u01-access.log") as f:
    lines = [l.strip() for l in f]
print(count_status(lines, 404))
print(count_status(lines, 200))
```

```console
$ python3 func.py
5
23
```

这两个数正好对上 U01 里 `cut -d' ' -f5 | sort | uniq -c` 得到的 `5 404` 和 `23 200`。

### 机制

**`def` 定义一个函数**：`def 名字(参数):` 后缩进写函数体，`return` 交回结果。

函数的价值在这里很具体：**`count_status` 写成一次，可以对任意状态码调用。** 如果写成 `count_404` 和 `count_200` 两个函数，就不如现在这样。判据是：函数体里出现的具体值越少，越好用。

**`if / elif / else`** 按顺序试，第一个成立的分支执行，其余跳过。条件可以是任意表达式，Python 会判断它的「真值」：

| 值 | 真值 |
| --- | --- |
| `0`、`0.0` | 假 |
| `""`（空字符串） | 假 |
| `[]`、`{}`、`()`（空容器） | 假 |
| `None` | 假 |
| 其他一切 | 真 |

所以 `if not lines:` 就是「列表为空」的惯用写法，不必写 `if len(lines) == 0`。

> **易错**　函数没有 `return` 语句时，返回值是 `None`，不是「什么都没有」。所以 `x = f()` 之后 `x` 是 `None`，再去 `x[0]` 就会报 `TypeError: 'NoneType' object is not subscriptable`。看到这个报错，第一反应是查上一个函数有没有忘记 `return`。

**`str(code)` 那句**：`code` 传进来是整数 `404`，而 `line.split()[4]` 是字符串 `"404"`，两者直接比较永远不等。Python 不会自动转换。**类型对不上时比较不报错、只是永远为假**，这类 bug 最难发现。

### 速查

| 操作 | 写法 |
| --- | --- |
| 定义函数 | `def f(a, b):` |
| 返回 | `return 值`（可返回多个：`return a, b`） |
| 条件 | `if x > 3:` / `elif` / `else` |
| 成员判断 | `if x in lst:` |
| 同时判断 | `if a and b:` / `or` / `not` |
| 空容器判断 | `if not lst:` |
| 类型转换 | `int(s)` / `str(n)` / `float(s)` |

### 题 U02.4-01

```python
def f(x):
    return x * 2 if x > 3 else x
print(f(5), f(1))
```

输出什么？

<details><summary>提示</summary>

`A if 条件 else B` 是表达式：条件成立取 A，否则取 B。先分别算 `f(5)` 和 `f(1)`。

</details>

<details><summary>答案</summary>

```console
$ python3 -c 'def f(x): return x*2 if x > 3 else x
print(f(5), f(1))'
10 1
```

`f(5)`：5 > 3 成立，取 `5*2` = 10。`f(1)`：不成立，取 `1`。

`print(a, b)` 输出时用空格分隔两个值，这是默认行为（`sep` 参数可以改）。

</details>

---

## 2.5 读文件

### 跑通

```python
with open("samples/u01-access.log") as f:
    lines = f.readlines()
print(len(lines))
print(lines[0].strip())
```

```console
$ python3 read.py
30
2026-11-10T08:00:00Z 198.51.100.23 POST /login 302 200
```

### 机制

**`open(路径)` 默认以文本模式打开**，读出来的是 `str`。`readlines()` 一次读完，返回「每行一个元素」的列表，**每行末尾的换行符 `\n` 还在**。

这就是为什么后面要 `.strip()`。不 strip 的话，`line.split()[5]` 会是 `"200\n"` 而不是 `"200"`——比较时又不相等，而且看不出来。

**`with` 保证文件被关掉**。哪怕中途抛异常，退出 `with` 块时也会关闭。不写 `with` 就得自己 `f.close()`，忘了就会占着文件句柄。**一律用 `with`。**

**如果文件是二进制的**（图片、抓包、压缩包），必须写 `open(路径, "rb")`。这时读出来是 `bytes` 不是 `str`，`.split()` 要传字节分隔符：`b" "`。这条在 U21 处理 PNG 时第一次真正用到。

对照一下两种做法：

| 做法 | 命令 |
| --- | --- |
| 终端 | `wc -l < samples/u01-access.log` |
| Python | `sum(1 for _ in open("samples/u01-access.log"))` |

后者丑得多。那为什么还要学 Python？因为当你要做的是「按第 5 个字段分组、每组算平均值、再按平均值排序」时，终端那条管道会变成六七个工具拼起来的东西，而 Python 是五行。**判据：一次性的、形态固定的处理用管道；需要条件分支、要多步中间状态、要复用的，用脚本。**

> **易错**　`open()` 不给完整路径时，从**当前目录**找文件。在别处运行脚本会报 `FileNotFoundError`。要么 `cd` 到项目根目录，要么在脚本里用 `os.path.dirname(__file__)` 拼绝对路径。

### 速查

| 操作 | 写法 |
| --- | --- |
| 读全部行 | `lines = f.readlines()` |
| 逐行遍历 | `for line in f:` |
| 读全部内容 | `f.read()` |
| 读二进制 | `open(p, "rb")` |
| 写文件 | `open(p, "w")` / `"a"` 追加 |
| 去首尾空白 | `line.strip()` |
| 去掉行尾换行 | `line.rstrip("\n")`（保留行首空格） |

### 题 U02.5-01

用一行 Python 数出 `samples/u01-access.log` 有多少行，只输出数字。

<details><summary>提示</summary>

`sum(1 for _ in open(路径))` —— `_` 是「这个变量我不用」的惯用名。

</details>

<details><summary>答案</summary>

```console
$ python3 -c "print(sum(1 for _ in open('static/samples/u01-access.log')))"
30
```

注意这里用的是 `static/samples/`（仓库内的路径）。你自己操作时路径要按实际位置写。

`sum(1 for _ in ...)` 的意思是「每读一行加 1」。它比 `len(f.readlines())` 省内存：后者要把所有行都装进列表，前者读完就扔。

</details>

---

## 6 自检

### U02.6-01

`print("a,b,c".split(","))` 输出什么？

<details><summary>提示</summary>

`split` 返回的是列表，打印列表时带方括号和引号。

</details>

<details><summary>答案</summary>

```console
$ python3 -c 'print("a,b,c".split(","))'
['a', 'b', 'c']
```

如果想输出 `a b c`，得配合 join：`print(" ".join("a,b,c".split(",")))`。

</details>

### U02.6-02

`print("-".join(["a", "b"]))` 输出什么？

<details><summary>提示</summary>

分隔符写在前面，被拼的列表写在括号里。

</details>

<details><summary>答案</summary>

```console
$ python3 -c 'print("-".join(["a","b"]))'
a-b
```

容易写反成 `["a","b"].join("-")`，那会报 `AttributeError: 'list' object has no attribute 'join'`。`join` 是**字符串**的方法，不是列表的方法。

</details>

### U02.6-03

设 `s = "  hi  "`，`print(repr(s.strip()))` 输出什么？

<details><summary>提示</summary>

`repr()` 会把字符串原样显示出来，包括引号——所以能看见还有没有空格。

</details>

<details><summary>答案</summary>

```console
$ python3 -c 's="  hi  "; print(repr(s.strip()))'
'hi'
```

用 `repr` 而不是直接 `print`，就是因为它会把引号也打出来，这样「有没有残留空格」一眼可见。调试字符串问题时，`print(repr(x))` 永远比 `print(x)` 可靠。

</details>

---

## 7 动手

### U02.7-01 用字典统计日志

写一个脚本，输出 `samples/u01-access.log` 里出现次数最多的前 3 个 IP，格式「次数 空格 IP」，每行一条。

提示：用一个 `dict` 记录每个 IP 的次数，`counts[ip] = counts.get(ip, 0) + 1`。`counts.get(key, 默认值)` 在 key 不存在时返回默认值，不会报 `KeyError`。

参考输出：

```console
10 203.0.113.7
8 198.51.100.23
6 192.0.2.88
```

<details><summary>提示</summary>

1. 先建空字典，逐行 `split()[1]` 取出 IP 累加；
2. `counts.items()` 给出 `(键, 值)` 序列；
3. `sorted(counts.items(), key=lambda kv: -kv[1])` 按次数降序——`lambda kv: -kv[1]` 是「取第二个元素再取负」，因为 `sorted` 默认升序，取负就变降序；
4. 取前 3 再打印。

</details>

<details><summary>答案</summary>

```python
counts = {}
with open("samples/u01-access.log") as f:
    for line in f:
        ip = line.split()[1]
        counts[ip] = counts.get(ip, 0) + 1

top = sorted(counts.items(), key=lambda kv: -kv[1])[:3]
for ip, n in top:
    print(n, ip)
```

```console
$ python3 top.py
10 203.0.113.7
8 198.51.100.23
6 192.0.2.88
```

和 U01 里那条 `awk '{print $2}' … | sort | uniq -c | sort -rn | head -3` 的结果一致——**同一件事的两种做法**。管道更短，脚本更能改。

</details>

---

## 小结

- 脚本是文本文件，`python3 文件.py` 执行。缩进是语法。
- 变量是名字绑定；字符串不可变；切片左闭右开；`split` / `join` 是反向操作。
- **Python 里凡是区间，含头不含尾**（`range`、切片都一样）。
- `sorted()` 返回新列表，`lst.sort()` 就地改并返回 `None`。
- 函数没 `return` 就返回 `None`；`int` 与 `str` 比较不报错、永远为假。
- 读文本用 `with open(p)`，读二进制用 `open(p, "rb")`；行尾有 `\n`，要 `strip`。
- 一次性固定处理用管道，需要分支和多步中间状态用脚本。

## 术语

| 中文 | English | 定义 |
| --- | --- | --- |
| 脚本 | script | 由解释器逐行执行的文本文件 |
| 变量 | variable | 绑定到对象的名字，本身没有类型 |
| 字符串 | string | 不可变的有序字符序列 |
| 列表 | list | 有序、可变的容器 |
| 字典 | dict | 键值对容器，按键查找 |
| 函数 | function | 有名字、带参数、可返回值的代码块 |
| 真值 | truthiness | 在条件里被判为真或假的性质 |
| 推导式 | comprehension | `[表达式 for 元素 in 序列 if 条件]` 形式的紧凑生成写法 |

## 延伸

- `python3 -i 脚本.py`：跑完脚本后进入交互模式，变量还在，方便检查。
- `python3 -m pdb 脚本.py`：内置调试器，`n` 下一行、`p 变量` 打印、`c` 继续。
- 官方教程第 3–7 章覆盖本章内容，但本课只需要上面这些。
