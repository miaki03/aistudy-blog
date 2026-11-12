+++
date = '2026-11-09T09:05:00+08:00'
draft = true
title = '学习路径 05 · 工具、资源清单与术语表'
description = "已核验的资源清单、按周分批安装命令、中英日术语表与链接核验记录。"
categories = ["学习路径"]
slug = "learning-path-05-resources"
+++

## 05 · 工具、资源清单与术语表

> 三合一：① 按周分批的工具安装；② 已核验的资源清单（标了核验状态）；③ 中英日术语表。
> **原则：能用网页版就不装本地；每周最多 3 个新工具。**

---

## 1. 资源清单（按线分类）

**核验说明**：标 ✅ 的已用 `web_fetch` 实际探测可访问；标 ⚠️ 的有特殊情况（反爬/需登录/需同意规则）；标 ❓ 的未逐个核验，但仍属常见入口。

### 1.1 CTF 平台

| 资源 | 链接 | 状态 | 适合 | 备注 |
| --- | --- | --- | --- | --- |
| picoCTF / CyLab Security Academy | <https://cylabacademy.org> | ✅ | **主线** | 原 picoCTF 已并入此站，旧账号可继续用；免费、有难度梯度 |
| OverTheWire Wargames | <https://overthewire.org/wargames/> | ✅ | **W1 起点** | Bandit 免注册，`ssh bandit0@bandit.labs.overthewire.org -p 2220` |
| CTFtime | <https://ctftime.org> | ✅ | 比赛 | 赛事日历、writeup 聚合、战队排行 |
| HackTheBox | <https://www.hackthebox.com> | ✅ | 进阶 | 免费题有限，Academy/Labs 需注册；本路径只在 W6 之后选用 |
| TryHackMe | <https://tryhackme.com> | ✅ | Web/取证入门 | 免费房间足够入门 |
| PortSwigger Web Security Academy | <https://portswigger.net/web-security> | ✅ | **Web 入门首选** | 免费课程 + 在线 lab，适合 `[S]` |
| pwn.college | <https://pwn.college> | ⚠️ | 了解即可 | 首次进入需同意「不公开题解」规则；本路径不主攻 pwn |
| Root-Me | <https://www.root-me.org> | ⚠️ | 补充题库 | 有反爬验证页，**用浏览器访问**，脚本会看到验证页 |
| CTF Wiki（中文） | <https://ctf-wiki.org> | ✅ | 中文系统教程 | 术语与英文略有差异，注意对照 |

### 1.2 Puzzle Hunt

| 资源 | 链接 | 状态 | 适合 | 备注 |
| --- | --- | --- | --- | --- |
| MIT Mystery Hunt 档案 | <https://puzzles.mit.edu> | ✅ | **主线** | 历年题量大、质量高；`www.mit.edu/~puzzle/` 会跳到这里 |
| Puzzled Pint | <https://puzzledpint.org> | ✅ | **W7 首选** | 注意是 **.org**（.com 会跳转）；每月一组，难度友好、有答案 |
| Puzzle Hunt Calendar | <https://www.puzzlehuntcalendar.com> | ✅ | 找活动 | 看当年有哪些 hunt 可参加 |
| Galactic Puzzle Hunt | <https://galacticpuzzlehunt.com> | ✅ | W8–W9 | 会自动跳到当年赛事子域（如 `/2026`），属正常 |
| Puzzling Stack Exchange | <https://puzzling.stackexchange.com> | ✅ | 卡住时提问 | 只读浏览无需登录 |
| National Puzzlers' League | <https://www.puzzledom.org> | ❓ | 词谜专练 | **注意：`npl.org` 是纽瓦克公共图书馆，不是这里**；官网疑为 puzzledom.org，未核验 |
| OneLook（词典反查） | <https://www.onelook.com> | ❓ | wordplay | 按模式/含义反查单词 |
| Nutrimatic（正则搜词） | <https://nutrimatic.org> | ✅ | wordplay | 会跳到 `/2024/` 新版入口，属正常 |
| quipqiup（替换密码求解） | <https://quipqiup.com> | ✅ | 古典密码 | 单表替换自动求解，结果仍需常识校验 |
| dCode | <https://www.dcode.fr> | ✅ | 编解码全家桶 | 默认法语，左上角切 **EN**；英文入口 `/en` |

### 1.3 ARG / 案例

| 资源 | 链接 | 状态 | 用途 |
| --- | --- | --- | --- |
| ARGNet | <https://www.argn.com> | ✅ | ARG 新闻与归档，W10 精读入口 |
| Unfiction | <https://www.unfiction.com> | ✅ | 老 ARG 社区论坛归档 |
| Wayback Machine | <https://web.archive.org> | ❓ | 看网站旧版，ARG 溯源必备 |
| Puzzling / r/ARG | 见 §1.6 | ⚠️ | 讨论与提问 |

### 1.4 在线工具（免安装优先）

| 工具 | 链接 | 状态 | 用途 |
| --- | --- | --- | --- |
| CyberChef | <https://gchq.github.io/CyberChef/> | ✅ | **最重要的一个**：编码/变换/取数据；可下载离线版 |
| dCode | <https://www.dcode.fr> | ✅ | 古典密码、摩斯、A1Z26 等 |
| quipqiup | <https://quipqiup.com> | ✅ | 单表替换 |
| Nutrimatic | <https://nutrimatic.org> | ✅ | 正则搜词（英文） |
| OneLook | <https://www.onelook.com> | ❓ | 词典反查 |
| Wayback | <https://web.archive.org> | ❓ | 历史页面 |
| Google Lens / Yandex 图片反查 | 搜索即可 | ❓ | 图片定位 / OSINT |

### 1.5 本地工具官网

| 工具 | 链接 | 状态 |
| --- | --- | --- |
| ExifTool | <https://exiftool.org> | ❓ |
| Wireshark | <https://www.wireshark.org> | ❓ |
| binwalk | <https://github.com/ReFirmLabs/binwalk> | ❓ |
| Audacity | <https://www.audacityteam.org> | ❓ |
| Sonic Visualiser | <https://www.sonicvisualiser.org> | ❓ |

### 1.6 中文资源

| 资源 | 链接 | 状态 | 用途 |
| --- | --- | --- | --- |
| CTF Wiki | <https://ctf-wiki.org> | ✅ | 中文系统教程（最可靠的中文 CTF 入口） |
| 先知社区 | <https://xz.aliyun.com> | ❓ | 中文 WriteUp 与安全文章 |
| 看雪论坛 | <https://bbs.pediy.com> | ❓ | 逆向、安全讨论 |
| reddit r/securityCTF、r/puzzles | 站内搜索 | ❓ | 英文提问 |

> **中文 Puzzle Hunt 系统性教程目前稀缺**，已挂进 [总览的「资料补给机制」](/p/learning-path/)。遇到好的中文长文，请贴给我，我整理成导读卡。

### 1.7 日语加餐（可选，不占主线）

你零基础学日语，这条只作为「以后可能用得上」的备注，不是任务：

- 日本有成熟的**謎解き（なぞとき / nazotoki）**文化：线上/线下解谜活动、解谜书、主题咖啡厅。
- 术语表里已列常用日文对照；等你能读片假名与基础汉字后，可把「日式谜题题面」当作阅读材料。
- **现在不要碰**：主线已经够满，日语加餐会稀释进度。

---

## 2. 工具安装（按周分批）

### 2.1 W1：不装任何本地工具

用网页版 CyberChef + `ssh` 打 Bandit。先建立手感。

### 2.2 W2：Python 环境

```bash
sudo apt update
sudo apt install -y python3-venv
python3 -m venv ~/ctf/venv
source ~/ctf/venv/bin/activate
pip install requests pillow pycryptodome
```

> 每次开新终端都要 `source ~/ctf/venv/bin/activate`。嫌麻烦就在 `~/.bashrc` 末尾加一行。

### 2.3 W3：文件与隐写 I

```bash
sudo apt install -y file xxd binutils exiftool pngcheck binwalk
```

### 2.4 W4：隐写 II

```bash
sudo apt install -y ffmpeg sox
sudo apt install -y ruby && gem install zsteg
```

### 2.5 W5：取证

```bash
sudo apt install -y foremost tshark tcpdump p7zip-full
```

### 2.6 W10：跨媒介

```bash
sudo apt install -y imagemagick zbar-tools qrencode
```

### 2.7 装不上怎么办

| 症状 | 处理 |
| --- | --- |
| `apt` 下载极慢 | 换镜像源，再 `apt update` |
| 找不到包 | `apt-cache search 关键词`；或用 `pipx install` |
| `zsteg` 装不上 | 用网页版 stegsolve，或自己写 Python LSB 提取 |
| 命令找不到 | 先 `which 命令`；没装就回到上面的对应周 |

**镜像源示例**（Ubuntu，换之前先备份 `/etc/apt/sources.list`）：

```bash
sudo cp /etc/apt/sources.list /etc/apt/sources.list.bak
sudo sed -i 's@//.*archive.ubuntu.com@//mirrors.tuna.tsinghua.edu.cn@g' /etc/apt/sources.list
sudo apt update
```

---

## 3. 术语表（中 · 英 · 日）

> 用法：读英文资料遇到生词就来查；表里没有的**自己加一行**。日文列只作对照，不要求记。

### 3.1 通用与学习

| 中文 | English | 日本語 | 一句话 |
| --- | --- | --- | --- |
| 谜题 | puzzle | パズル | 需要动脑解决的问题 |
| 解谜 | puzzle solving | 謎解き（なぞとき） | 日式说法，特指解谜活动 |
| 题目 | challenge / problem | 問題（もんだい） | |
| 提示 | hint | ヒント | |
| 答案 | answer | 答え（こたえ） | PH 里通常是单词 |
| 提交 | submit | 提出（ていしゅつ） | |
| 复盘 | retrospective / writeup | 振り返り（ふりかえり） | 做完之后回头看 |
| 笔记 | notes | メモ / ノート | |
| 卡点 | blocker | つまずき | 卡住的地方 |
| 团队 | team | チーム | |
| 单人 | solo | ソロ / 一人（ひとり） | |
| 难度 | difficulty | 難易度（なんいど） | |
| 排行榜 | scoreboard / leaderboard | ランキング | |

### 3.2 技术底座

| 中文 | English | 日本語 | 一句话 |
| --- | --- | --- | --- |
| 编码 | encoding | 符号化 / エンコード | 可逆的表示转换 |
| 解码 | decode | デコード | |
| 加密 | encryption | 暗号化（あんごうか） | 需要密钥 |
| 解密 | decryption | 復号（ふくごう） | |
| 明文 | plaintext | 平文（へいぶん） | |
| 密文 | ciphertext | 暗号文（あんごうぶん） | |
| 密钥 | key | 鍵（かぎ） | |
| 哈希 | hash | ハッシュ | 单向摘要 |
| 二进制 | binary | バイナリ / 2進数 | |
| 十六进制 | hex / hexadecimal | 16進数（じゅうろくしんすう） | |
| 十进制 | decimal | 10進数 | |
| 模运算 | modular arithmetic | 剰余演算（じょうよえんざん） | `a % m` |
| 异或 | XOR | XOR / 排他的論理和 | 同则为 0 |
| 位运算 | bitwise operation | ビット演算 | |
| 字符串 | string | 文字列（もじれつ） | |
| 文件 | file | ファイル | |
| 压缩包 | archive | アーカイブ / 圧縮ファイル | |
| 命令行 | command line | コマンドライン | |
| 终端 | terminal | ターミナル | |
| 脚本 | script | スクリプト | |
| 虚拟机 | virtual machine | 仮想マシン | |
| 服务器 | server | サーバー | |
| 漏洞 | vulnerability | 脆弱性（ぜいじゃくせい） | |
| 靶机 | target machine / lab | 演習環境 / ターゲット | 练习用目标 |
| 注入 | injection | インジェクション | |

### 3.3 密码与隐写

| 中文 | English | 日本語 | 一句话 |
| --- | --- | --- | --- |
| 古典密码 | classical cipher | 古典暗号 | |
| 凯撒密码 | Caesar cipher | シーザー暗号 | 整体平移 |
| 维吉尼亚 | Vigenère cipher | ヴィジュネル暗号 | 多表替换 |
| 单表替换 | substitution cipher | 換字式暗号（かんじしき） | 一一映射 |
| 换位密码 | transposition cipher | 転置式暗号（てんちしき） | 重排字符 |
| 培根密码 | Bacon's cipher | ベーコン暗号 | A/B 五种一组 |
| 摩斯电码 | Morse code | モールス信号 | 点划 |
| 词频分析 | frequency analysis | 頻度分析（ひんどぶんせき） | 破替换的第一步 |
| 爆破 | brute force | ブルートフォース / 総当たり | 穷举 |
| 变位词 | anagram | アナグラム | 字母重排 |
| 隐写 | steganography | ステガノグラフィ | 藏数据而非加密 |
| 最低有效位 | least significant bit (LSB) | 最下位ビット | 图片藏数据常用 |
| 元数据 | metadata | メタデータ | |
| 频谱 | spectrum | スペクトル / 周波数スペクトル | 音频藏字常用 |

### 3.4 Puzzle Hunt / ARG

| 中文 | English | 日本語 | 一句话 |
| --- | --- | --- | --- |
| 提取 | extraction | 抽出（ちゅうしゅつ） | **PH 的核心动作** |
| 元谜题 | meta puzzle | メタパズル | 用前面答案作输入的题 |
| 线索 | clue | 手がかり | |
| 线索链 | trail | 手がかりの連鎖 | ARG 的主结构 |
| 兔子洞 | rabbit hole | ラビットホール | ARG 的伪装入口 |
| 门禁 | gate | ゲート | 必须按顺序解锁 |
| 题面 | flavor text | 問題文（もんだいぶん） | |
| 首字母 | acrostic | 頭文字（かしらもじ） | 藏头 |
| 枚举 | enumeration | 列挙（れっきょ） | 给答案长度 |
| 填字游戏 | crossword | クロスワード | |
| 二维码 | QR code | QRコード | |
| 跨媒介 | transmedia | トランスメディア | |
| 另类实境游戏 | ARG | ARG | |
| 网络流量 | network traffic | 通信トラフィック | |

### 3.5 取证与 Web

| 中文 | English | 日本語 | 一句话 |
| --- | --- | --- | --- |
| 取证 | forensics | フォレンジック | |
| 流量包 | packet capture (pcap) | パケットキャプチャ | |
| 数据包 | packet | パケット | |
| 请求头 | request header | リクエストヘッダ | |
| 会话 | session | セッション | |
| 令牌 | token | トークン | |
| 逆向工程 | reverse engineering | リバースエンジニアリング | |
| 反汇编 | disassembly | 逆アセンブル | |
| 栈溢出 | stack overflow | スタックオーバーフロー | 本路径不覆盖 |
| 信息收集 | OSINT | OSINT | |

---

## 4. 核验记录

| 日期 | 范围 | 结果 |
| --- | --- | --- |
| 建立教材时 | 22 个关键 URL | 全部可达。修正 3 处：`puzzledpint` → `.org`；`npl.org` 是图书馆，Puzzlers' League 在 `puzzledom.org`（未核验）；`galacticpuzzlehunt.com` 会跳当年子域 |

> 后续每季度可抽查一次。发现失效就在 [总览的「资料补给机制」](/p/learning-path/)里加一行，我来换链接。
