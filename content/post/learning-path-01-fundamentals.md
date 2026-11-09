+++
date = '2026-11-09T08:45:00+08:00'
draft = false
title = '学习路径 01 · 基础底座：环境、Python、编码与数制'
description = "W1–W2：WSL2 工具链、Python 够用速成、编码与数制判断表、10 道自测题（含答案）、古典密码最小集与数学工具箱。"
categories = ["学习路径"]
slug = "learning-path-01-fundamentals"
+++

## 01 · 基础底座：环境、Python、编码与数制

> 覆盖 W1–W2。目标不是「学会编程」，而是**建立一套够用的最小工具箱**：能判断一串怪字符是什么、能量出文件里藏了什么、能写 20 行脚本把重复劳动包掉。
> 之后遇到 Python 不够用，再回来查，不要提前系统学。

---

## 1. 本模块目标

- [ ] 能在 WSL2 里自如地看文件、搜内容、跑脚本
- [ ] 能对任意一串字符串，在 3 分钟内判断它属于哪种编码并还原
- [ ] 能读懂并修改 6 段固定脚本
- [ ] 知道「不会就查」的边界在哪：能用工具代替的，绝不自己硬推

---

## 2. 环境与工具链

### 2.1 W1 只做三件事（别一开始就装一堆）

1. 确认 WSL2 可用：`wsl -l -v`
2. 建好工作区：`mkdir -p ~/ctf/{notes,writeups,work,tools}`
3. 跑通「网页版 CyberChef + ssh 打 Bandit」

> 本地工具安装推迟到 W3（见 [总览里的分批安装表](/p/learning-path/)）。**能用网页版就别装本地**，CyberChef 网页版能替代一半工具。

### 2.2 命令行最小集（20 个就够撑到 W6）

| 命令 | 用途 | 必记用法 |
| --- | --- | --- |
| `ls -la` | 看目录（含隐藏文件） | `-la` 两个参数一起用 |
| `cd cp mv rm mkdir` | 移动文件 | 沙箱里删错救不回，先 `mv` 备着 |
| `cat less head tail` | 看文件 | `less` 里按 `q` 退出 |
| `grep -a -n` | 搜内容，`-a` 把二进制当文本搜 | `grep -a -n "flag" .` |
| `file` | **看真实类型**（不信后缀） | 永远是第一步 |
| `xxd -l 64` | 看十六进制头部 | `-l 64` 只看前 64 字节 |
| `strings -n 6` | 抽可打印字符串 | 小于 6 字符的碎片太吵 |
| `od -c` | 按字符看二进制 | 备选，`xxd` 更常用 |
| `chmod +x` | 给脚本执行权限 | 下载的脚本跑不动时先想这个 |
| `curl -O` | 下文件 / 看网页 | `curl -I` 只看响应头 |
| `wget` | 下文件 | 备选 |
| `ssh user@host -p 端口` | 登录靶机 | Bandit 用 `-p 2220` |
| `scp` | 传文件 | 从靶机拉文件出来 |
| `find . -name "*.png"` | 找文件 | 配合 `-exec` 批量处理 |
| `\|` `>` `>>` `<` | 管道与重定向 | `cmd1 \| cmd2 > out.txt` |
| `xargs` | 把列表变成参数 | 批量对每个文件跑命令 |
| `cut -d -f` | 按列切 | 处理 CSV/日志 |
| `sort \| uniq -c` | 频次统计 | 找重复、做词频 |
| `python3 -c "..."` | 一行脚本 | 临时算个数最方便 |
| `man/cmd --help` | 查用法 | 记不住就查，不丢人 |

**练习**：在 `~/ctf/work` 里创建一个文件，把上面每条命令至少用一次，记进 `notes/w1.md`。

### 2.3 W3 起才装的本地工具（现在只做到"知道有它"）

```bash
# W3 隐写/文件分析
sudo apt install -y file xxd binutils exiftool pngcheck binwalk
# W5 取证
sudo apt install -y foremost tshark tcpdump p7zip-full
# W10 跨媒介
sudo apt install -y ffmpeg imagemagick zbar-tools qrencode
# Python 环境（W2 就装）
sudo apt install -y python3-venv
python3 -m venv ~/ctf/venv && source ~/ctf/venv/bin/activate
pip install requests pillow pycryptodome
```

> 若 `apt` 下载慢：先换镜像源（`sudo sed -i 's@//.*archive.ubuntu.com@//mirrors.tuna.tsinghua.edu.cn@g' /etc/apt/sources.list`，再 `apt update`）。若某个包不存在，用 `apt-cache search <关键词>` 找替代，不要死磕。

---

## 3. Python 够用版：只学 8 件事

### 3.1 八个概念（学会就能改脚本）

| # | 概念 | 在解谜里为什么需要 |
| --- | --- | --- |
| 1 | `str` 与 `bytes` 的区别 | 解码必须在 bytes 上做；`'abc'.encode()` / `b'abc'.decode()` |
| 2 | 列表与切片 | `s[::-1]` 反转、`s[::2]` 隔位取、`s[i:j]` 切段 |
| 3 | `for` / `if` | 爆破、筛选 |
| 4 | `def` 函数 | 把重复动作包起来 |
| 5 | 文件读写 `open(...,'rb')` | 题目给的多半是二进制文件 |
| 6 | 字符串方法 | `split/strip/replace/startswith` |
| 7 | `import` 标准库 | `base64`、`itertools`、`binascii`、`re` |
| 8 | f-string | `f"{x:08b}"` 格式化输出，调试神器 |

> 不学：类、装饰器、异步、类型标注、数据库。**等真的需要再说。**

### 3.2 六段直接能改的脚本

**① 看文件头与长度**

```python
data = open('challenge.bin', 'rb').read()
print(data[:16].hex())   # 前 16 字节的十六进制
print(len(data))         # 总长度
```

**② 单字节 XOR 爆破**

```python
data = open('cipher.bin', 'rb').read()
for k in range(256):
    out = bytes(b ^ k for b in data)
    if b'flag' in out:
        print(k, out)
```

**③ 常见编码互转**

```python
import base64
print(base64.b64decode('aGVsbG8='))      # b'hello'
print(bytes.fromhex('68656c6c6f'))       # b'hello'
print(base64.b32decode('NBSWY3DP'))      # b'hello'
print('flag'.encode().hex())             # 666c6167
```

**④ 全目录搜 flag**

```python
import os, re
for root, _, files in os.walk('.'):
    for f in files:
        p = os.path.join(root, f)
        try:
            t = open(p, 'rb').read().decode('utf-8', 'ignore')
        except Exception:
            continue
        if re.search(r'(flag|CTF)\{', t, re.I):
            print('HIT:', p)
```

**⑤ 抓网页**

```python
import requests
r = requests.get('https://example.com', timeout=10)
print(r.status_code, r.headers.get('content-type'))
print(r.text[:500])
```

**⑥ 图片像素 / LSB 读取（W3 用）**

```python
from PIL import Image
im = Image.open('x.png').convert('RGB')
px = list(im.getdata())
bits = ''.join(str(p[2] & 1) for p in px[:800])   # 取蓝通道最低位
print(bits[:64])
```

**练习**：把 ② 改成「自动猜 key：找可打印字符占比最高的结果」，输出候选明文。

---

## 4. 编码与数制（本模块的重头）

### 4.1 拿到怪字符串的五步开场

```
1. file / 看长度            → 先确定它是文本还是二进制
2. 看字符集                 → 全是 0-9a-f？全是 A-Z2-7？全是 0/1？
3. 套 §4.2 判断表           → 选出 1–2 个最可能的编码
4. CyberChef 的 Magic 一键猜 → 别自己手算，让它猜
5. 还不行 → 看结尾是否有多余数据（附加数据、第二层编码）
```

### 4.2 判断表（贴在这里，随时回查）

| 看到什么 | 先试什么 | 注意 |
| --- | --- | --- |
| 结尾 `=` 或 `==`，字符集含 `+/` | Base64 | 长度不是 4 的倍数 → 可能缺 padding |
| 只有 `A-Z2-7`，长度是 8 的倍数 | Base32 | 结尾通常有 `=` |
| 只有 `0-9a-f`，长度为偶数 | Hex（base16） | 两两一组转 ASCII |
| 只有 `0` `1`，长度是 8 的倍数 | 二进制 | 每 8 位转一个字符 |
| 只有 `A/B` 或 `a/b`，长度是 5 的倍数 | Bacon（培根密码） | 5 个一组，A=0/B=1 |
| 只有 `.` `-` `/` 和空格 | 摩斯电码 | 空格分词、`/` 分字母 |
| 出现 `%41` 这类 | URL 编码 | 连续 `%XX` 很常见 |
| 出现 `&#65;` `&amp;` | HTML 实体 | 查表还原 |
| 出现 `\101` `\x41` | 八进制/十六进制转义 | 常见于 C 风格字符串 |
| 字母看起来「长得对但怪」 | 同形字 Unicode 混淆 | 如西里尔字母 а 冒充 a |
| 整片乱码但可打印 | ROT47 / 单字节 XOR | 先试 ROT47（只影响可打印 ASCII） |
| 中文乱码 | GBK ↔ UTF-8 互转 | CyberChef 有对应操作 |

### 4.3 逐个编码，各记一句话

| 编码 | 一句话记住 | 工具 |
| --- | --- | --- |
| Hex | 两字符 = 一字节 | CyberChef `From Hex`、`xxd -r -p` |
| Base16/32/58/62/64/85/91 | 同一族，字符集不同；64 最常见 | CyberChef 一键；`base64 -d` |
| ASCII | 65–90 大写、97–122 小写、48–57 数字 | `chr()` / `ord()` |
| Unicode | `U+XXXX`；同形字是坑 | CyberChef 有专门操作 |
| URL | `%XX` | `urllib.parse.unquote` |
| HTML 实体 | `&#65;` 或 `&amp;` | `html.unescape` |
| 摩斯 | 点划 + 空格/斜杠分隔 | dCode、CyberChef |
| Bacon | 5 个 A/B 一组 | 手写 10 行脚本最快 |
| 八进制/转义 | `\101` = `A` | `int('101', 8)` |
| ROT13/ROT47 | ROT13 只转字母；ROT47 转可打印 ASCII | CyberChef |

**Base 家族差异（考过就懂）**

- Base64：`A-Za-z0-9+/`，`=` 补位。变体：URL-safe 把 `+/` 换成 `-_`，可能要补 `=`。
- Base32：`A-Z2-7`，长度总是 8 的倍数。
- Base58：去掉了 `0OIl` 等易混字符，比特币用。
- Base85：`Ascii85`，4 字节 → 5 字符，常用于 PDF。
- Base91：更紧凑，题目里出现频率低，但 CyberChef 有。

### 4.4 位运算（3 个性质撑起半个 misc）

| 运算 | 用途 | 关键性质 |
| --- | --- | --- |
| `^` 异或 | 加密、找重复密钥 | `a^a=0`、`a^0=a`、可交换 |
| `&` 与 | 取位、掩码 | `x & 1` 取最低位（LSB 隐写） |
| `<<` `>>` | 移位 | `x >> 2` 去掉低 2 位 |

**关键技巧**：把密文和它自身移位后异或比较，若在某个位移上出现大量 0，说明密钥长度 = 该位移 → 这是发现 Vigenère/重复密钥的第一步。

```python
c = open('cipher.bin','rb').read()
for shift in range(1, 41):
    same = sum(1 for i in range(len(c)-shift) if c[i] == c[i+shift])
    if same / (len(c)-shift) > 0.05:
        print('疑似密钥长度', shift, round(same/(len(c)-shift), 3))
```

### 4.5 自测 10 题（先自己试，再看答案）

> 建议全部用 CyberChef / 手写 Python 完成，不要搜在线工具。

1. `666c61677b6865787d`
2. `ZmxhZ3tiNjR9`
3. `synt{ebg13}`
4. `01100110 01101100 01100001 01100111`
5. `..-. .-.. .- --.`
6. `aabab ababb aaaaa aabba`
7. `%66%6c%61%67%7b%75%72%6c%7d`
8. `uozt{zgyzhs}`
9. 密文 `EOBD`，已知用单字节 XOR 加密，求明文
10. `01100111 01100001 01101100 01100110`，先转 ASCII 再反转字符串

<details>
<summary>答案（点开）</summary>

1. `flag{hex}`
2. `flag{b64}`
3. `flag{rot13}`
4. `flag`
5. `FLAG`
6. `FLAG`（A=0, B=1：aabab=F, ababb=L, aaaaa=A, aabba=G）
7. `flag{url}`
8. `flag{atbash}`
9. key=0x23，明文 `flag`
10. 解出 `galf`，反转得 `flag`

</details>

---

## 5. 古典密码最小集（W5 主学，这里先埋点）

| 密码 | 长什么样 | 怎么破 |
| --- | --- | --- |
| Caesar / ROT-N | 字母整体平移 | 试 25 个位移；ROT13 是 N=13 |
| Atbash | 字母镜像 a↔z | 直接映射，无需密钥 |
| Vigenère | 多表替换，字母表轮换 | 先猜密钥长度（见 4.4），再逐组当 Caesar 破 |
| 单表替换 | 字母随机映射 | 词频（英文最高 ETAOIN）+ quipqiup 自动求解 |
| 栅栏 / 列换位 | 字符位置重排 | 试栏数，看是否出现可读片段 |
| 键盘位移 | 按 QWERTY 左右/上下错位 | 试着把每个字符在键盘上挪一格 |

**工具优先级**：CyberChef（有现成操作） > dCode（参数齐全） > 自己写脚本。
**不要背词频表**，用 quipqiup 类自动求解器，再用常识校验结果。

---

## 6. 数学工具箱（够用版）

| 需要什么 | Python 一行 | 用在哪 |
| --- | --- | --- |
| 进制互转 | `int('ff',16)`、`hex(255)`、`bin(255)` | 所有编码 |
| 大整数 | Python 原生支持任意精度 | RSA 类题目 |
| 取模 | `a % m`、`pow(a, b, m)` | 公钥、古典密码 |
| 排列组合 | `itertools.permutations / combinations / product` | 枚举、换位 |
| 位运算 | 见 4.4 | 隐写、XOR |
| 概率直觉 | 生日悖论：23 人就有 ~50% 概率撞生日 | 判断爆破空间是否可行 |
| 约束满足 | 枚举 + 剪枝 | 网格题、数独式 |

**够用判据**：能在 3 分钟内估算「这个爆破空间有多大、值不值得写脚本」。
例：单字节 XOR 是 256 次 → 值得；3 字节密钥是 1600 万次 → 先想别的路。

---

## 7. 练习阶梯（W1–W2 全部题目）

| 序 | 题目 | 标记 | 难度 | 时长 | 验收 |
| --- | --- | --- | --- | --- | --- |
| 1 | OverTheWire Bandit 0–5 | `[S]` | ★1 | 2h | 每关命令写进 `notes/w1.md` |
| 2 | Bandit 6–10 | `[S]` | ★2 | 2h | 同上 |
| 3 | CyberChef 自练：用 Magic 还原 3 个样例 | `[S]` | ★1 | 30min | 能说出它猜对的编码名 |
| 4 | 本文件 §4.5 的 10 道自测 | `[S]` | ★1–2 | 1.5h | 全对，且每题写 1 行「怎么判断的」 |
| 5 | 写「编码识别器」：输入字符串，输出候选编码 | `[S]` | ★2 | 1.5h | `tools/whichcode.py` 能跑 |
| 6 | 写「XOR 爆破器」：输入文件，输出可打印结果 | `[S]` | ★2 | 1h | `tools/xorbrute.py` 能跑 |
| 7 | CTF 平台 General Skills 类 5–8 题 | `[S]` | ★1–2 | 2h | 每道一条速记 writeup |

> 平台题名会随改版变化。认准**分类**（General Skills / Misc / 入门），不要死记题名。

---

## 8. 验收标准（W2 结束时自测）

- [ ] 给一段陌生字符串，能在 3 分钟内判断出编码类型并还原（限时 5 题，对 4 题及格）
- [ ] 能不看笔记写出「单字节 XOR 爆破」的 6 行脚本
- [ ] Bandit 过到第 10 关
- [ ] `~/ctf/tools/` 下至少有 2 个自写脚本
- [ ] `notes/w1.md`、`notes/w2.md` 各有一页，含本周卡点
- [ ] 错题本里至少 3 条，每条都有「下次的检查动作」

---

## 9. 常见卡点（提前知道能省 2 小时）

| 卡点 | 真相 | 处理 |
| --- | --- | --- |
| `file` 说是 `data` | 头 16 字节被改过是常见手法 | `xxd -l 64` 看有没有可疑字符串或压缩包头（`PK`、`\x1f\x8b`） |
| Base64 解码报 `Incorrect padding` | 缺 `=` | 补到长度是 4 的倍数 |
| Python 打印出来是 `b'...'` | 你在 print bytes | 加 `.decode()`；解码失败用 `errors='ignore'` |
| 中文乱码 | 编码猜错 | 试 `gbk`、`utf-8`、`latin-1` 三种，看哪个出汉字 |
| `apt install` 找不到包 | 源没更新或包名不同 | `apt update` 后 `apt-cache search` |
| Bandit 连不上 | 端口错或网络 | 端口是 **2220**，不是 22 |
| 装了一堆工具却没用过 | 收集癖 | 本周只用 3 个，其余记下来以后装 |

---

## 10. 本模块结束时的能力自检（一句话版）

> 「给我一个文件或一串字符，我知道先跑哪三个命令，并且能写 10 行脚本把重复部分包掉。」

做不到 → 回去把 §4.5 和 §7 的第 5、6 项重做一遍，不要进入 W3。
