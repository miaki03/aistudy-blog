+++
date = '2026-11-10T15:00:00+08:00'
draft = true
title = 'U00 · 在终端里看见字节'
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

## 前置：需要先知道的 0 个概念

本章是全课第一课，没有前置。三个新词（字节、偏移、可打印字符）在 0.2 节第一次用到时当场定义。

> **约定** 命令都在终端里输入，一行一条。

## 0.1 在终端里跑第一条命令

### 跑通物

终端系统自带，按你的系统挑一个：

- **Windows**：开始菜单搜 `Ubuntu`（WSL，你的 F 盘在里面是 `/mnt/f`），或搜 `Git Bash`；PowerShell 里没有本章要用的 `xxd`、`file`。
- **macOS**：`Command + 空格`，输入 `Terminal`，回车。
- **Linux**：`Ctrl + Alt + T`。

末尾带 `$` 的那行是提示符，意思是"我在等你打字"。逐行输入，每条按回车：

```console
$ pwd
/mnt/f/vibecoding/learning-path-site

$ ls
README.md  content  docs  hugo.toml  kb  scripts  static
```

你的目录不同，`ls` 的输出就不会和这里一样。

### 机制

终端是一个只做四件事的窗口：你打字、按回车、它执行、它回话。操作全写成一行字，一行字是**命令名**加**参数**，中间用空格隔开。

- `pwd` 无参数，回答"我在哪个目录"，输出是当前目录的完整路径。
- `ls` 无参数，回答"这个目录里有哪些条目"；`ls static` 列出的是 `static` 里的东西。

两处容易错。

第一，大小写敏感：`XXD` 不是 `xxd`，`s-01.png` 也不是 `S-01.png`。

第二，报错只说命令没跑成，不是你把东西弄坏了：

```console
$ ls static/samples/S-1.png
ls: cannot access 'static/samples/S-1.png': No such file or directory
```

`No such file or directory` 是"路径上找不到东西"，九成是打错了：少一层目录、拼错字母、大小写不对。是路径问题，不是权限问题。

### 速查

| 命令 | 它回答什么 |
| --- | --- |
| `pwd` | 我在哪个目录 |
| `ls` | 这个目录里有什么 |
| `ls -l` | 同上，另加大小、时间、权限 |
| `cd 目录` | 切到那里再执行后面的命令 |

### 题 U00.1-01

`static/samples/u01-access.log` 有几个字节？用一条命令，让输出只有数字。

<details><summary>提示</summary>

1. `wc` 数数，`-c` 数字节数；`wc -c 文件` 会连文件名一起印出来。
2. 要输出只剩数字，用 `命令 < 文件`：`<` 把文件内容送进命令的输入。完整重定向在 U04。

</details>

<details><summary>答案</summary>

```console
$ wc -c < static/samples/u01-access.log
1681
```

对照不加 `<` 的样子，多出来的是文件名：

```console
$ wc -c static/samples/u01-access.log
1681 static/samples/u01-access.log
```

`1681` 就是字节数。

</details>

### 练习站：Bandit 第 0–5 关

<https://overthewire.org/wargames/bandit/>：OverTheWire 的命令行闯关练习站，从第 0 关打到第 5 关，免费、免注册、SSH 直连。

为什么是这 5 关：它们只需要 `ls`、`cat`、`cd`、`file`，正好覆盖本章；第 6 关起要把命令接起来，那是 U04 之后的事。个别关卡可能还要多试几条命令，卡住就跳过：本章的要求是把 `pwd`、`ls`、`cd`、`cat`、`file` 用熟。

登录要用一条 `ssh` 命令，网站首页写着完整的那一行，照抄即可；`ssh` 本身不在本章范围。

它缺的东西补在这里：`cat 文件` 把内容打到屏幕上，用来读关卡说明；`cd 目录` 换目录，`cd ..` 回上一层；`ls -a` 连 `.` 开头的隐藏条目一起列；`file 文件` 看这是什么东西。

报错怎么读：`No such file or directory` 是路径写错，`Permission denied` 才是权限不够。

> **实践** 动手部分就是这 5 关。它只给线索不给解释：提示写在说明文件里，你自己 `cat` 出来读，再用命令找下一关的密码。

## 0.2 用 xxd 看见字节

### 跑通物

```console
$ xxd -l 16 static/samples/S-01.png
00000000: 8950 4e47 0d0a 1a0a 0000 000d 4948 4452  .PNG........IHDR
```

`xxd` 把文件按**字节**列出来，`-l 16` 是参数，"只要前 16 个字节"。字节是文件在硬盘上的计数单位：文件不存"字"，一个位置存一个字节，文件大小按字节数算，`S-01.png` 是 2483 个字节。

### 机制

一行三列，空格隔开：

1. **偏移列**：这行第一个字节距离文件开头多远。第一个字节是 0，一行 16 个，下一行就从 16 开始：

```console
$ xxd -l 32 static/samples/S-01.png
00000000: 8950 4e47 0d0a 1a0a 0000 000d 4948 4452  .PNG........IHDR
00000010: 0000 0040 0000 0040 0802 0000 0025 0be6  ...@...@.....%..
```

第二行左边的 `00000010` 就是 16。偏移用十六进制写，为什么是十六进制属于 U01，此刻读作"从第 16 个字节开始"。

2. **字节列**：每两个字符是**一个**字节，8 个一组，一行 16 个字节、32 个字符，第一个字节是 `89`。

3. **可打印列**：同样这 16 个字节的第二种写法，能显示的字符原样显示，不能显示的写 `.`。左边 `89` 在右边是 `.`，`50` 是 `P`，`4e` 是 `N`，`47` 是 `G`；`0d`、`0a`、`00` 显示不出来。右边 16 个字符与左边 16 个字节一个对一个。

PNG 规定文件以 `89 50 4e 47 0d 0a 1a 0a` 这 8 个字节开头，`file` 认的就是这 8 个。

> **易错** 右边的点不代表字节内容相同：`.PNG` 前后那 9 个点是 9 个不同的字节，只是都显示不出来。

### 速查

| 命令 | 作用 |
| --- | --- |
| `xxd -l N 文件` | 只看前 N 个字节 |
| `xxd -s 偏移 文件` | 从该偏移开始，如 `-s 4` |
| `xxd -p 文件` | 去掉偏移列与可打印列，字节连成一串 |

### 题 U00.2-01

`static/samples/S-01.png` 的前 4 个字节是什么？只取字节列。

<details><summary>提示</summary>

1. 只取字节列用 `-p`，只要前 4 个用 `-l 4`，两个选项可以写在同一行。
2. `-p` 的输出连写：4 个字节是 8 个字符，中间没有空格。

</details>

<details><summary>答案</summary>

```console
$ xxd -l 4 -p static/samples/S-01.png
89504e47
```

这 8 个字符是 4 个字节 `89 50 4e 47`，与 0.2 节第一行开头一致。

</details>

## 0.3 文件就是一串字节

### 跑通物

```console
$ file static/samples/S-01.png
static/samples/S-01.png: PNG image data, 64 x 64, 8-bit/color RGB, non-interlaced
```

冒号后是类型判断：PNG 图片，64 乘 64 像素，每像素 8 位 RGB 三色，非隔行。

### 机制

`file` 不读扩展名：它读开头的一小段字节，对照一份已知文件头的清单，对上哪条就报哪条。

证明：复制成一个 `.txt` 结尾的名字，再问一次。

```console
$ cp static/samples/S-01.png /tmp/a.txt
$ file -b /tmp/a.txt
PNG image data, 64 x 64, 8-bit/color RGB, non-interlaced
```

`-b` 是参数，"不打印文件名，只打印类型"。结论和改名前一字不差：名字里写着 `txt`，内容仍然是 PNG。扩展名由你随手起，清单里对上的字节不由改名决定；两者不一致时，报的是字节那一侧。

这是猜，依据只有开头几个字节；改动它们就能让它报出错误的类型，那是 U12 的内容。

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
2. 复制到 `/tmp/a.txt`，用 `file -b` 问它，看冒号后那句有没有变。

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

- 一行字是命令名加参数；`pwd` 报位置，`ls` 报内容。
- 文件在硬盘上就是一串字节，字节是计数单位。
- `xxd` 排三列：偏移、每字节两个字符、可打印字符（显示不出的写 `.`）。
- `file` 按开头字节猜类型，不看扩展名。
- 要背的只有一条：`xxd -l 16 文件`。

## 术语

| 中文 | English | 定义 |
| --- | --- | --- |
| 字节 | byte | 文件内容的最小计数单位 |
| 偏移 | offset | 字节距离文件开头多远，首字节为 0，`xxd` 写在行首 |
| 可打印字符 | printable character | 能显示成一个字的字符；显示不出的字节在 `xxd` 第三列写 `.` |
| xxd | xxd | 按字节列出文件的命令；`-l` 限长度，`-s` 定起点，`-p` 只输出字节列 |
| file | file | 读开头字节判断类型的命令；`-b` 省掉文件名 |

## 延伸

- OverTheWire Bandit：<https://overthewire.org/wargames/bandit/>，第 0–5 关对应本章。
- `man xxd`：在你自己的终端里执行，看完整参数表。
- U01 十六进制：讲偏移列为什么用十六进制写。
