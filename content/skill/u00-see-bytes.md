+++
date = '2026-11-10T15:00:00+08:00'
draft = false
title = '第 1 章 · 在终端里看见字节'
description = '用 xxd 列出任意文件的前 16 个字节，并说出输出三列各是什么'
slug = 'u00-see-bytes'
chapter = 'U00'
stage = 0
minutes = 60
prereq = []
concepts = ['byte', 'offset', 'printable']
reuse = ['U01', 'U02', 'U06', 'U07', 'U12', 'U21']
skills = ['terminal', 'xxd', 'bytes']
problems = ['U00.1-01', 'U00.2-01', 'U00.3-01']
+++

## 读完能做什么

给定任意一个文件，你能用 `xxd` 列出它的前 16 个字节，并说出输出三列各是什么。

本章是全课第一课，没有前置。三个新词（字节、偏移、可打印字符）在 0.2 节第一次用到时当场定义。

## 0.1 在终端里跑第一条命令

### 跑通物

> **约定** 命令都在终端里输入，一行一条。

**第一步，找到终端。** 本章要用的 `xxd`、`file`，PowerShell 里没有，所以要在 Linux 环境里做。按你的系统确认：

**Windows**

1. 开始菜单搜 `Ubuntu`，搜到就打开（WSL，Windows 里的 Linux）；看到 `用户名@主机:~$` 这样的提示符就是进去了。
2. 搜不到说明没装：开始菜单搜 `PowerShell` 打开，输入 `wsl --install` 回车，按提示重启；重启后打开 `Ubuntu`，设个用户名和密码（本章用不到）。
3. 不确定自己有没有管理员权限：照上面做，失败了看屏幕上的报错；实在装不上就先只读不跑，下面的题需要终端。

**macOS**：`Command + 空格`，输入 `Terminal`，回车。系统自带 `xxd`。

**Linux**：`Ctrl + Alt + T`。如果 `xxd` 报 `command not found`，装上 `vim-common` 这个包就有。

**第二步，准备文件。** 本章只需要一个 `S-01.png`，两条路选一条。

自己下载过本仓库（"仓库"就是这些文件所在的那个文件夹）：先走进去，再确认站对了：

```console
$ cd /mnt/f/vibecoding/learning-path-site
$ pwd
/mnt/f/vibecoding/learning-path-site
```

`cd` 后面跟路径，意思是"换到那个文件夹"。`/mnt/f` 是 WSL 里表示 F 盘：Windows 的 `F:\` 等于 WSL 的 `/mnt/f/`。Git Bash 里要写 `cd /f/vibecoding/learning-path-site`（那里 F 盘是 `/f`）。

没有仓库：在 Ubuntu 里直接下载，`curl -sO` 把它存到当前文件夹，`-s` 不显示进度条：

```console
$ curl -sO https://ai.xcfx.com/samples/S-01.png
$ ls
S-01.png
```

存到哪个文件夹都行；命令里出现 `static/samples/S-01.png` 的地方换成你的路径，就在当前文件夹的话直接写 `S-01.png`。

**第三步，跑两条命令。** 下面灰框里 `$` 开头的那行是提示符，`$` 在行首，**不要输入它**：从 `$` 后面的空格之后开始打。你屏幕上不会出现 `$` 本身，直接出结果。

```console
$ pwd
/mnt/f/vibecoding/learning-path-site

$ ls
README.md  content  docs  hugo.toml  kb  scripts  static
```

你的目录不同，输出就会不同。

### 机制

终端只做四件事：你打字、按回车、它执行、它回话。操作全写成一行字，一行字是**命令名**加**参数**，中间用空格隔开。

- `pwd` 无参数，回答"我在哪个目录"，输出是当前目录的完整路径。
- `ls` 无参数，回答"这个目录里有哪些条目"；`ls static` 列出的是 `static` 里的东西。

报错只说命令没跑成，不是你把东西弄坏了。三种最常见的：

| 屏幕上的原文 | 它在说什么 |
| --- | --- |
| `ls: cannot access 'static/samples/S-1.png': No such file or directory` | 路径写错：拼错、少一层、大小写不对 |
| `bash: xxd2: command not found` | 没有这条命令：没装，或命令名拼错 |
| `xxd: Is a directory` | 你给的是文件夹，不是文件 |

另外，命令名和文件名都区分大小写：`XXD` 不是 `xxd`，`s-01.png` 不是 `S-01.png`。

### 速查

| 命令 | 它回答什么 |
| --- | --- |
| `pwd` | 我在哪个目录 |
| `ls` | 这个目录里有什么 |
| `ls -l` | 同上，另加大小和时间 |
| `cd 目录` | 切到那个目录；`cd ..` 回上一层 |

### 题 U00.1-01

先 `cd static`，用 `ls samples` 找到样本文件 `S-01.png`；再 `cd ..` 回到根文件夹，用 `pwd` 确认。

<details><summary>提示</summary>

1. `cd static` 之后你站在 `static` 里，`ls samples` 列出的是 `samples` 文件夹的内容，不是当前文件夹的。
2. `cd ..` 里的 `..` 表示上一层；最后 `pwd` 应该和 0.1 开头那次一样。

</details>

<details><summary>答案</summary>

```console
$ cd static
$ pwd
/mnt/f/vibecoding/learning-path-site/static
$ ls samples
S-01.png
S-02.png
S-03.zip
S-04.gz
S-05.wav
S-06.pcap
S-07
selftest
u01-access.log
$ cd ..
$ pwd
/mnt/f/vibecoding/learning-path-site
```

`S-01.png` 就在这份列表里。终端窗口够宽的话，列表会排成几列而不是一列，内容不变。没有仓库的人：把 `static` 换成你放 `S-01.png` 的那个文件夹。

</details>

### 练习站（可以跳过）：Bandit 第 0–5 关

> **实践** 这是本章的动手部分，可以跳过：跳过不影响任何题目。

想多练 `ls`、`cat`、`cd`、`file`，去 OverTheWire 的 Bandit：<https://overthewire.org/wargames/bandit/>，整站英文，照下面这行走：

```console
$ ssh bandit0@bandit.labs.overthewire.org -p 2220
```

`ssh` 是远程登录：让你在自己的终端里操作另一台机器；`-p 2220` 是端口号，照抄就好。问 `Are you sure you want to continue connecting (yes/no)?` 时输 `yes`；看到 `password:` 时输 `bandit0`（屏幕不动、没有星号，正常）；进去后每关用 `ls` 找文件、`cat` 读文件，提示就写在文件里。这几关只需要 `ls`、`cat`、`cd`、`file`，第 6 关起要把命令接起来，那是 第 5 章 之后的事。卡住、或者连不上（2220 端口被网络挡）就跳过。补两个它没解释的：`cat 文件` 把内容打到屏幕上；`ls -a` 连隐藏条目一起列。

## 0.2 用 xxd 看见字节

### 跑通物

```console
$ xxd -l 16 static/samples/S-01.png
00000000: 8950 4e47 0d0a 1a0a 0000 000d 4948 4452  .PNG........IHDR
```

`xxd` 把文件按**字节**列出来，`-l 16` 是参数，"只看前 16 个字节"。文件里存的不是字符，是字节：一个位置存一个字节，一个字节能表示 0 到 255 中的一个数，文件大小按字节数算。字符是你拿一张对照表把字节读出来的结果。

### 机制

一行三列，空格隔开：

1. **偏移列**：这行第一个字节在文件里排第几个，从 0 数起；一行 16 个，所以第二行从 16 开始：

```console
$ xxd -l 32 static/samples/S-01.png
00000000: 8950 4e47 0d0a 1a0a 0000 000d 4948 4452  .PNG........IHDR
00000010: 0000 0040 0000 0040 0802 0000 0025 0be6  ...@...@.....%..
```

本章不要求你会把 `00000010` 换算成 16，只用它对齐：从第 16 个字节开始列，行首就是同一个写法。

```console
$ xxd -s 16 -l 16 static/samples/S-01.png
00000010: 0000 0040 0000 0040 0802 0000 0025 0be6  ...@...@.....%..
```

`-s 16` 是"从第 16 个字节开始"，输出与上面第二行一字不差。

2. **字节列**：每两个字符是**一个**字节；排版上每 4 个字符（也就是 2 个字节）空一格，一行 8 格、共 16 个字节。第一行前 4 个字节是 `89 50 4e 47`。

3. **可打印列**：同样这 16 个字节的第二种写法，能显示的字符原样显示，不能显示的写 `.`。判据只有一条：右边出现一个点，就是那个字节没有可见字符，不需要查全表。左边 `89` 是 `.`；`50` 对 `P`、`4e` 对 `N`、`47` 对 `G`，依据一张固定的"字节对字符"表，叫 ASCII，全表在 第 3 章，本章用不到全表。`0d`、`0a`、`1a`、`00` 都显示不出来。右边 16 个字符与左边 16 个字节一个对一个。

PNG 规定文件以 `89 50 4e 47 0d 0a 1a 0a` 这 8 个字节开头，`file` 认的就是这 8 个字节。

> **易错** 右边的点不代表字节内容相同。`89` 是点、`50` 是 `P`，两者都只占右边一个位置；点只是"这个字节没有可见字符"。

### 速查

| 命令 | 作用 |
| --- | --- |
| `xxd -l N 文件` | 只看前 N 个字节 |
| `xxd -s 偏移 文件` | 从该偏移开始，如 `-s 16` |
| `xxd -p 文件` | 去掉偏移列与可打印列，字节连成一串 |

短横线后的字母不能跨命令类推：`xxd -p` 是"只输出字节列"，`ssh -p 2220` 是端口号，两个 `-p` 没关系；参数只看命令自己的说明。

### 题 U00.2-01

`static/samples/S-01.png` 的前 4 个字节是什么？只取字节列。

<details><summary>提示</summary>

1. 只取字节列用 `-p`，只要前 4 个字节用 `-l 4`，两个选项可以写在同一条命令里，先后随意。
2. `-p` 输出连写：4 个字节写成 8 个字符，没有空格。

</details>

<details><summary>答案</summary>

```console
$ xxd -l 4 -p static/samples/S-01.png
89504e47
$ xxd -p -l 4 static/samples/S-01.png
89504e47
```

换先后输出一样。这 8 个字符是 4 个字节 `89 50 4e 47`，与 0.2 节第一行开头一致。

</details>

## 0.3 文件就是一串字节

### 跑通物

```console
$ file static/samples/S-01.png
static/samples/S-01.png: PNG image data, 64 x 64, 8-bit/color RGB, non-interlaced
```

冒号前是文件名，后面是类型判断。`64 x 64` 是宽和高各 64 像素；后面 `8-bit/color RGB`、`non-interlaced` 是这张图的参数，本章用不到，忽略。

### 机制

`file` 不读扩展名：它读文件开头的那一小段字节，拿这段去对照一张它自带的格式清单（几千种），对上哪条就报哪条。这张清单是 `file` 内置的，不属于本章范围；只需知道它查的是开头那一小段。PNG 的那一小段就是 0.2 节看到的 8 个字节。

验证：复制成一个 `.txt` 结尾的名字，再问一次。

```console
$ cp static/samples/S-01.png /tmp/a.txt
$ file -b /tmp/a.txt
PNG image data, 64 x 64, 8-bit/color RGB, non-interlaced
```

`cp 源 目标` 是复制，原文件不动；`/tmp` 是 Linux 的临时目录，随便写，重启会清空。`-b` 是"不打印文件名，只打印类型"。结论和改名前一字不差：名字写着 `txt`，内容仍是 PNG。扩展名由你随手起，字节不由改名决定；不一致时报的是字节那一侧。

所以它也能被伪造：改动开头那一小段字节，就会报出错误的类型——怎么伪造是 第 11 章 的事。

### 速查

| 命令 | 作用 |
| --- | --- |
| `file 文件` | 报文件名和类型判断 |
| `file -b 文件` | 只报类型判断 |
| `cp 源 目标` | 复制一份，做改名实验用 |

### 题 U00.3-01

把一个 PNG 改名成 `a.txt`，`file` 还会说它是 PNG 吗？做实验，把结论写下来。

<details><summary>提示</summary>

1. 不要在样本上直接改名，复制一份：`cp 源 目标`。
2. 复制到 `/tmp/a.txt`，用 `file -b` 问它，看冒号后那句变没变。

</details>

<details><summary>答案</summary>

```console
$ cp static/samples/S-01.png /tmp/a.txt
$ file -b /tmp/a.txt
PNG image data, 64 x 64, 8-bit/color RGB, non-interlaced
```

还是会。`file` 读的是开头那几个字节，改名不改字节。

</details>

## 小结

- 一行字是命令名加参数；`pwd` 报位置，`ls` 报内容，`cd` 换位置。文件里存的是字节，字符是照对照表读出来的。
- `xxd` 排三列：偏移、每两个字符一个字节、可打印字符（显示不出的写 `.`）；`file` 按开头字节猜类型，不看扩展名。
- 要背的只有一条：`xxd -l 16 文件`。

## 术语

| 中文 | English | 定义 |
| --- | --- | --- |
| 字节 | byte | 文件内容的最小计数单位 |
| 偏移 | offset | 字节距离文件开头多远，首字节为 0 |
| 可打印字符 | printable character | 能显示成一个字的字符；显示不出的在 `xxd` 第三列写 `.` |
| xxd | xxd | 按字节列出文件的命令；`-l` 限长度，`-s` 定起点，`-p` 只输出字节列 |
| file | file | 读开头字节判断类型的命令；`-b` 省掉文件名 |

## 延伸

- 第 2 章 十六进制：讲偏移列为什么用十六进制写。
