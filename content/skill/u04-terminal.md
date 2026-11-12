+++
date = '2026-11-10T10:00:00+08:00'
draft = false
title = '第 5 章 · 终端：把工具接成一条流水线'
description = '路径、管道、重定向、sort/uniq/wc、cut/tr/sed，最后把它们拼成一条命令。'
slug = 'u04-terminal'
chapter = 'U04'
stage = 0
minutes = 140
prereq = ['U00']
concepts = ['path', 'pipe', 'redirect', 'field']
reuse = ['U10', 'U12', 'U20', 'U40', 'U41', 'U60']
skills = ['shell', 'pipeline', 'text-processing']
problems = ['U04.1-01', 'U04.3-01', 'U04.4-01', 'U04.5-01', 'U04.6-01', 'U04.6-02', 'U04.6-03', 'U04.7-01']
+++

## 读完能做什么

1. 说出 `ls -l` 输出里每一列是什么意思，并能用 `head` / `wc -l` 只看一个文件的一部分。
2. 用 `|`、`>`、`>>`、`2>` 把三个以上命令接成一条，并说出每一步的输入和输出分别是什么类型。
3. 给定一份访问日志，不查资料写出一条命令，输出「出现次数最多的前三个来源 IP」。

这一章所有练习都在同一个文件上做：`samples/u01-access.log`，30 行访问日志。

## 前置

需要 第 1 章 里那个终端，以及 `samples/` 目录。若你还没下载样本：

```console
$ mkdir -p samples && cd samples
$ for f in S-01.png S-02.png S-03.zip S-04.gz S-05.wav S-06.pcap S-07 u01-access.log; do
>   curl -sLO "https://ai.xcfx.com/samples/$f"
> done
```

本章新用到三个命令，先确认在不在：

```console
$ cut --version | head -1
cut (GNU coreutils) 9.4
```

`sort`、`uniq`、`wc`、`head`、`grep`、`cut`、`tr`、`sed`、`strings` 在 Linux/macOS/WSL 都是自带的，不用装。只有 `cut --version` 这类 GNU 专有参数在 macOS（BSD 版）上会报错，本章给的用法两边都通用。

---

## 1.1 路径、查看一个文件

### 跑通

```console
$ pwd
/mnt/f/vibecoding/learning-path-site

$ ls -l samples/u01-access.log
-rw-r--r-- 1 miaki miaki 1681 Nov 10 18:20 samples/u01-access.log

$ head -3 samples/u01-access.log
2026-11-10T08:00:00Z 198.51.100.23 POST /login 302 200
2026-11-10T08:00:01Z 192.0.2.88 GET /static/app.js 200 337
2026-11-10T08:00:02Z 203.0.113.7 GET / 200 474

$ wc -l < samples/u01-access.log
30
```

### 机制

**路径**是「从哪里开始、怎么走到那个文件」。两种写法：

- **绝对路径**以 `/` 开头，从根目录开始：`/mnt/f/vibecoding/learning-path-site/samples/u01-access.log`
- **相对路径**不以 `/` 开头，从**当前目录**开始：`samples/u01-access.log`

当前目录由 `pwd` 显示。`cd` 改变它。`..` 是上一级，`.` 是当前级。所以 `../samples/x` 和 `samples/x` 可能指同一个文件，取决于你在哪。

`ls -l` 的每一列：

```text
-rw-r--r-- 1 miaki miaki 1681 Nov 10 18:20 samples/u01-access.log
└───┬────┘ │ └─┬─┘ └─┬─┘ └┬─┘ └────┬─────┘
  权限    链接数 属主   属组  字节数   修改时间
```

**第三列之后那个数字是字节数**，不是行数。1681 字节、30 行 —— 这两个数不一样，跟 第 1 章 讲的「字节数 ≠ 字符数」是同一件事的不同面。

> **易错**　不要把 `ls` 和 `ls -l` 搞混。`ls` 只给名字，`ls -l` 才给字节数和权限。要判断一个文件是不是空的，看第五列，不要靠眼睛。

`wc -l < 文件` 里的 `<` 是**输入重定向**：把文件内容接到 `wc` 的标准输入上。为什么不直接写 `wc -l 文件`？因为那样会多输出一列文件名：

```console
$ wc -l samples/u01-access.log
30 samples/u01-access.log
```

两个数都在时，脚本里就更难比较。加 `<` 之后只输出数字，这才是能直接拿去比对的形态。

### 速查

| 命令 | 作用 |
| --- | --- |
| `pwd` | 打印当前目录的绝对路径 |
| `ls` / `ls -l` | 列名字 / 列名字 + 权限 + 字节数 + 时间 |
| `head -3 文件` | 前 3 行 |
| `tail -3 文件` | 后 3 行 |
| `wc -l 文件` | 行数（会带文件名） |
| `wc -l < 文件` | 行数（纯数字） |
| `wc -c 文件` | 字节数 |

### 题 U04.1-01

`samples/u01-access.log` 有多少行？只输出数字。

<details><summary>提示</summary>

要「只输出数字」，就得用 `<` 把文件接到标准输入，而不是把文件名当参数传进去。

</details>

<details><summary>答案</summary>

```console
$ wc -l < samples/u01-access.log
30
```

如果写成 `wc -l samples/u01-access.log`，输出是 `30 samples/u01-access.log`，多了文件名，就不止是数字了。

</details>

---

## 1.2 管道与重定向

### 跑通

```console
$ head -3 samples/u01-access.log > /tmp/a.txt
$ wc -l < /tmp/a.txt
3

$ head -3 samples/u01-access.log >> /tmp/a.txt
$ wc -l < /tmp/a.txt
6

$ head -1 samples/u01-access.log > /tmp/a.txt
$ wc -l < /tmp/a.txt
1
```

三组命令，只差一个符号：`>` 覆盖（清空后写），`>>` 追加（接到末尾）。第三组又用了 `>`，所以文件被清回 1 行。

管道是另一个符号：

```console
$ cut -d' ' -f2 samples/u01-access.log | head -3
198.51.100.23
192.0.2.88
203.0.113.7
```

`cut` 把第 2 列（IP）切出来，`|` 把它的输出直接交给 `head`，`head` 只留前 3 行。

### 机制

每个在终端里跑起来的程序，都自动接了三根线：

| 编号 | 名字 | 默认接哪 |
| --- | --- | --- |
| 0 | 标准输入（stdin） | 键盘 |
| 1 | 标准输出（stdout） | 终端屏幕 |
| 2 | 标准错误（stderr） | 终端屏幕 |

**这两根输出线是分开的**，这是初学者最容易忽略的一点。`1>` 只管正常输出，`2>` 只管报错：

```console
$ python3 -c "import sys; sys.stderr.write('boom\n')" 2> /tmp/err.txt
$ cat /tmp/err.txt
boom
```

如果刚才写成 `> /tmp/err.txt`，`boom` 不会进文件，因为你把 stdout 接走了，而这条消息走的是 stderr。

| 符号 | 作用 |
| --- | --- |
| `命令 > 文件` | 把 stdout 写进文件（**覆盖**） |
| `命令 >> 文件` | 把 stdout 追加到文件末尾 |
| `命令 2> 文件` | 把 stderr 写进文件 |
| `命令 > 文件 2>&1` | stdout 和 stderr 都写进同一个文件 |
| `A \| B` | 把 A 的 stdout 接到 B 的 stdin |
| `命令 < 文件` | 把文件接到命令的 stdin |

**管道的本质**是把前一个程序的 stdout 直接接到后一个程序的 stdin，中间不落盘。所以 `A | B` 和 `A > tmp && B < tmp` 结果一样，但前者不产生临时文件、也不等 A 跑完才开始 B（两者并行，边产边消费）。

这一点在实际做题时有意义：处理几百 MB 的抓包时，用管道可以直接边解边过，避免写一个巨大的中间文件。

> **实践**　`>` 会**无声地清空**目标文件。养成习惯：先用 `>>` 或者先 `mkdir` 到一个专门目录，别对着 `>` 敲一个已存在的重要文件名。

### 速查

见上表。另记一条常用组合：`命令 > out.txt 2>&1` —— 把正常输出和报错一起收进同一个文件。

---

## 1.3 sort / uniq / wc：数数

### 跑通

先看一个陷阱。把 IP 列出来，直接 `uniq -c`：

```console
$ awk '{print $2}' samples/u01-access.log | uniq -c | wc -l
25
```

30 行数据，得到 25 组。可是文件里只有 5 个不同的 IP。**为什么？**

因为 `uniq` 只合并**相邻**的重复行。这份日志按时间排，同一个 IP 散落在各处，不相邻，所以合并不掉。

先排序再数：

```console
$ awk '{print $2}' samples/u01-access.log | sort | uniq -c | wc -l
5
```

5 组，对了。再看内容：

```console
$ awk '{print $2}' samples/u01-access.log | sort | uniq -c | sort -rn | head -3
     10 203.0.113.7
      8 198.51.100.23
      6 192.0.2.88
```

状态码的分布同理，只是取的列不同：

```console
$ cut -d' ' -f5 samples/u01-access.log | sort | uniq -c | sort -rn
     23 200
      5 404
      2 302
```

### 机制

四个命令各自的职责，很少混用：

| 命令 | 职责 | 注意 |
| --- | --- | --- |
| `sort` | 按行排序（默认字典序） | `-n` 按数值，`-r` 倒序，`-u` 排序并去重 |
| `uniq` | **合并相邻的**重复行 | 不排序直接用，等于没去重 |
| `uniq -c` | 合并时输出出现次数 | 输出格式是「次数 内容」两列 |
| `wc -l` | 数行数 | 用 `<` 才是纯数字 |

**为什么 `uniq` 只处理相邻行**：它是一次往后看一眼的流式算法，只保留「上一个读到的东西」做比较。这样内存占用是常数，处理一个 10 GB 的文件也不需要把它全读进内存。代价就是你得先 `sort`，否则相同的值不挨着。

所以那个经典套路是三段，缺一不可：

```text
取出一列  →  sort  →  uniq -c  →  sort -rn
```

最后那个 `sort -rn` 是按**次数**从大到小排，因为 `uniq -c` 的输出第一列就是次数。`-rn` 里的 `n` 表示按数值比较——不加 `n` 的话，`10` 会被排在 `8` 前面（字典序里 `1` < `8`）。

> **易错**　`sort -r` 是字符串倒序，`sort -rn` 才是数值倒序。数 10 和 8 的顺序会暴露你有没有加 `n`。

### 速查

| 写法 | 结果 |
| --- | --- |
| `sort` | 字典序升序 |
| `sort -n` | 数值升序 |
| `sort -rn` | 数值降序 |
| `sort -u` | 排序 + 去重（等价于 `sort \| uniq`） |
| `uniq` | 去重（仅相邻） |
| `uniq -c` | 去重并计数 |
| `uniq -d` | 只留出现 ≥2 次的 |
| `uniq -u` | 只留出现 1 次的 |

### 题 U04.3-01

写出出现次数**最多**的那个 IP 及其次数，格式为「次数 空格 IP」，例如 `7 10.0.0.1`。

<details><summary>提示</summary>

在 `sort | uniq -c | sort -rn` 之后，第一行就是最多的。但 `head -1` 会带上前导空格，用 `awk '{print $1, $2}'` 重新排版最稳。

</details>

<details><summary>答案</summary>

```console
$ awk '{print $2}' samples/u01-access.log | sort | uniq -c | sort -rn | head -1 | awk '{print $1, $2}'
10 203.0.113.7
```

`uniq -c` 的输出每行前面有空格对齐，直接 `head -1` 会带着空格。`awk '{print $1, $2}'` 会按空白切分再拼回去，得到干净的「10 203.0.113.7」。

</details>

---

## 1.4 cut / tr / sed：取出你要的那一块

### 跑通

```console
$ cut -d' ' -f2 samples/u01-access.log | head -3
198.51.100.23
192.0.2.88
203.0.113.7

$ cut -d' ' -f4 samples/u01-access.log | head -1
/login

$ sed -n '1,2p' samples/u01-access.log
2026-11-10T08:00:00Z 198.51.100.23 POST /login 302 200
2026-11-10T08:00:01Z 192.0.2.88 GET /static/app.js 200 337

$ head -1 samples/u01-access.log | sed 's/T/ /'
2026-11-10 08:00:00Z 198.51.100.23 POST /login 302 200

$ echo 'a b c' | tr ' ' '\n'
a
b
c
```

### 机制

三件事，各管一类操作：

**`cut` 按位置切片。** `-d' '` 指定分隔符是一个空格，`-f2` 取第 2 段。这份日志用空格分隔，所以字段编号是：

```text
1=时间戳  2=IP  3=方法  4=路径  5=状态码  6=字节数
```

> **易错**　`cut` 不合并连续分隔符。如果两列之间有两个空格，`-d' '` 会把中间那个空字段也算一段，字段编号整体错位。日志里字段对齐时尤其容易踩。稳妥做法是先 `tr -s ' '` 把连续空格压成一个，或用 `awk '{print $N}'`（`awk` 会自动合并空白）。

**`tr` 逐字符替换。** `tr ' ' '\n'` 把每个空格换成换行。它只能做「字符 → 字符」的映射，不能按字段切，所以常用来把一行拆成多行，好让 `sort`/`uniq` 处理。

**`sed` 按行处理。** `-n '1,2p'` 只打印第 1–2 行（`-n` 抑制默认输出，`p` 手动打印）。`s/T/ /` 把每行第一个 `T` 换成空格——注意它默认只替换**每行第一个**，要替换全部得加 `g`：`s/a/b/g`。

### 速查

| 写法 | 作用 |
| --- | --- |
| `cut -d' ' -f2` | 按空格切，取第 2 段 |
| `cut -d',' -f1,3` | 取第 1 和第 3 段 |
| `cut -c1-10` | 按字符位置取前 10 个 |
| `tr ' ' '\n'` | 空格换行 |
| `tr -s ' '` | 压缩连续空格为一个 |
| `tr -d '\r'` | 删掉所有回车（Windows 文本转 Unix 常用） |
| `sed -n '3p'` | 只打印第 3 行 |
| `sed -n '1,5p'` | 打印 1–5 行 |
| `sed 's/旧/新/'` | 替换每行第一个 |
| `sed 's/旧/新/g'` | 替换全部 |
| `sed '/关键词/d'` | 删掉含关键词的行 |

### 题 U04.4-01

用 `cut` 取出这份日志的**第 4 段**（路径），只要第一行。

<details><summary>提示</summary>

`-d' '` 定分隔符，`-f4` 取第 4 段，再用 `head -1` 只留一行。

</details>

<details><summary>答案</summary>

```console
$ cut -d' ' -f4 samples/u01-access.log | head -1
/login
```

第 4 段是路径。注意路径里如果有空格（比如带查询参数的 URL 被 URL 编码后仍可能含 `%20`，但不会含真空格），`cut` 就会切错——这也正是上面「易错」那条说的。

</details>

---

## 1.5 把以上拼成一条命令

### 跑通

目标：按状态码统计，次数从多到少。

```console
$ cut -d' ' -f5 samples/u01-access.log | sort | uniq -c | sort -rn
     23 200
      5 404
      2 302
```

从左往右读，每一步的数据形态都在变：

| 步骤 | 输入 | 输出 |
| --- | --- | --- |
| `cut -d' ' -f5` | 30 行日志 | 30 行状态码 |
| `sort` | 30 行状态码 | 30 行，已排序 |
| `uniq -c` | 30 行已排序 | 3 行「次数 状态码」 |
| `sort -rn` | 3 行 | 3 行，按次数降序 |

### 机制

一条组合命令不神秘，它是**数据形态的逐步变换**。判断组合对不对，只看两件事：

1. 上一步的输出，下一步接不接得住（是不是纯文本行、字段位置对不对）；
2. 最终形态是不是你要的（行数、列数、顺序）。

排错也按这两条反推：命令不出结果时，从左边开始，每加一个 `|` 就跑一次，看输出变成什么样。**不要一次写完再猜哪里错。**

```console
$ cut -d' ' -f5 samples/u01-access.log | head -3
302
200
200
$ cut -d' ' -f5 samples/u01-access.log | sort | head -3
200
200
200
$ cut -d' ' -f5 samples/u01-access.log | sort | uniq -c
      2 302
     23 200
      5 404
```

分三步跑，每一步都能肉眼核对。这是后面每一章都会用的调试方式。

### 速查

常用组合配方：

| 目标 | 命令 |
| --- | --- |
| 某列的取值分布 | `cut -d' ' -fN 文件 \| sort \| uniq -c \| sort -rn` |
| 某列的前 3 | `... \| head -3` |
| 按某列排序整行 | `sort -t' ' -k5 -n 文件` |
| 只保留含关键词的行 | `grep '关键词' 文件` |
| 排除含关键词的行 | `grep -v '关键词' 文件` |
| 统计匹配条数 | `grep -c '关键词' 文件` |
| 从二进制文件里抠可打印字符串 | `strings -a 文件` |

最后一行是本章给后续埋的钩子：`strings` 能把二进制文件里的可打印片段全列出来，抓包文件里没加密的 HTTP 内容就是靠它快速看到的。

### 题 U04.5-01

状态码 `404` 的请求有多少条？只输出数字。

<details><summary>提示</summary>

两种做法都行：用 `cut` 取第 5 段再 `grep -c`，或者直接用 `awk '$5==404'` 过滤。

</details>

<details><summary>答案</summary>

```console
$ awk '$5==404' samples/u01-access.log | wc -l
5
```

`awk` 的 `$5` 是第 5 个字段，`$5==404` 是条件，条件成立才输出整行。再用 `wc -l` 数行数。

用 `grep -c '404'` 也能得到 5，但它匹配的是「整行里出现过 404 这个串」，如果字节数那一列恰好是 404，就会被误算进去。**按字段判定比按子串匹配可靠。**

</details>

---

## 6 自检

### U04.6-01

路径 `/login` 在这份日志里出现多少次？

<details><summary>提示</summary>

注意 `/login` 后面跟一个空格——不加空格会把 `/login/xxx` 也匹配进来（本例没有，但这个习惯要从开始就养成）。

</details>

<details><summary>答案</summary>

```console
$ grep -c '/login ' samples/u01-access.log
6
```

`grep -c` 输出匹配的**行数**，不是匹配次数。一行里有两次也只算 1。

</details>

### U04.6-02

不加 `sort`、直接对 IP 列跑 `uniq -c`，输出多少行？

<details><summary>提示</summary>

先想想为什么不是 5。

</details>

<details><summary>答案</summary>

```console
$ awk '{print $2}' samples/u01-access.log | uniq -c | wc -l
25
```

30 行里相邻重复的只有 5 处被合并掉，剩 25 组。这说明**`uniq` 只合并相邻行**——日志按时间排序，同一 IP 不挨着，所以合并不掉。

</details>

### U04.6-03

用 `strings` 从 `samples/S-06.pcap` 里找出被请求的 URL（不含 `GET` 和尾部空格）。

<details><summary>提示</summary>

`strings -a` 列出所有可打印片段，再用 `grep` 挑出以 `GET ` 开头的行，最后切掉前面的 `GET `。

</details>

<details><summary>答案</summary>

```console
$ strings -a samples/S-06.pcap | grep -o 'GET [^ ]*' | cut -d' ' -f2
/files/%E4%BD%A0%E5%A5%BD.txt
```

`grep -o` 只输出匹配到的那一段（不是整行）。`[^ ]*` 表示「一串非空格字符」，所以正好截到 URL 结尾。`%E4%BD%A0%E5%A5%BD` 是 URL 编码，第 10 章 会讲怎么还原。

</details>

---

## 7 动手

### U04.7-01 一份日志的三问

1. 每个状态码各多少条，按次数降序（三行，形如「次数 状态码」）。
2. 说明为什么 `uniq` 必须先 `sort`；用本章的 25 / 5 两个数字支持你的说法。
3. 用 `strings -a samples/S-06.pcap` 的完整输出，找出**域名**和 **Cookie 的值**，并说明这个 Cookie 值看起来像什么编码。

<details><summary>提示</summary>

第 1 问用 1.5 节那条命令，只换一下取哪一列。
第 3 问的 `strings` 输出共 9 行，直接看就行，不需要过滤。

</details>

<details><summary>答案</summary>

第 1 问：

```console
$ cut -d' ' -f5 samples/u01-access.log | sort | uniq -c | sort -rn
     23 200
      5 404
      2 302
```

第 2 问：`uniq` 只比较相邻两行。日志按时间排序，同一 IP 分散，所以不排序时有 25 组；排序后相同值相邻，只剩 5 组。**排序是把「相同的东西放到一起」，`uniq` 才能看见它们。**

第 3 问：`strings -a samples/S-06.pcap` 的第 2 行是 `Host: ctf.example`，所以域名是 `ctf.example`。Cookie 行是 `Cookie: sid=UzA2LWh0dHAtYjY0LW9r`，去掉 `sid=` 后是 `UzA2LWh0dHAtYjY0LW9r`——只含字母数字，没有 `+/`，长度 20 是 4 的倍数，**这是 Base64**。第 9 章 会讲怎么解。

</details>

---

## 小结

- 路径分绝对（`/` 开头）与相对（从当前目录）。`pwd` 告诉你现在在哪。
- `ls -l` 的第五列是**字节数**，不是行数。
- 三个标准流：stdin 0 / stdout 1 / stderr 2。`>` 覆盖、`>>` 追加、`2>` 收报错、`|` 接下一环。
- `uniq` 只合并相邻行，所以套路永远是 `sort | uniq -c | sort -rn`。
- `cut` 按字段、`tr` 按字符、`sed` 按行。`cut` 不合并连续分隔符，`awk` 会。
- 组合命令是数据形态的逐步变换。排错时从左边开始，每加一个 `|` 就跑一次。

## 术语

| 中文 | English | 定义 |
| --- | --- | --- |
| 绝对路径 | absolute path | 以 `/` 开头，从根目录开始的路径 |
| 相对路径 | relative path | 不以 `/` 开头，从当前目录开始的路径 |
| 标准输入 | stdin | 程序默认读的那根线，编号 0，默认接键盘 |
| 标准输出 | stdout | 程序正常输出，编号 1，默认接屏幕 |
| 标准错误 | stderr | 程序报错输出，编号 2，默认接屏幕 |
| 管道 | pipe | `\|`，把前一程序的 stdout 接到后一程序的 stdin |
| 重定向 | redirection | `>` / `>>` / `<` / `2>`，把流改接到文件 |
| 字段 | field | 一行按分隔符切开后的每一段，`cut`/`awk` 的单位 |

## 延伸

- `man 1 sort`、`man 1 uniq`：完整参数。看 `man` 里「BUGS」一节往往比正文有用。
- `awk` 是这份流水线里的第 5 个工具，本章只用了 `$N` 和条件。等到需要按多条件筛选（第 22 章 过滤抓包）时再单独讲。
