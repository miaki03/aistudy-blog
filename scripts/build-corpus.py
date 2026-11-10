#!/usr/bin/env python3
"""生成贯穿样本集 samples/corpus/S-01 … S-07。

要求：确定性。同一份脚本重复运行必须产出同一批字节，
否则「新 Part 推翻旧 Part 结论」的检测就失效了。

用法：
    python3 scripts/build-corpus.py            # 生成全部
    python3 scripts/build-corpus.py --list     # 只看清单
"""

import base64
import gzip
import io
import os
import random
import struct
import subprocess
import sys
import wave
import zipfile
import zlib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "static", "samples")

SEED = 20261110


# --------------------------------------------------------------------------
# PNG
# --------------------------------------------------------------------------
def png_chunk(tag, data):
    return (
        struct.pack(">I", len(data))
        + tag
        + data
        + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
    )


def png_build(width, height, rows, claimed_height=None):
    """rows[y][x] = (r, g, b)。claimed_height 用来做「高度被改小」的样本。"""
    raw = b""
    for row in rows:
        raw += b"\x00" + b"".join(bytes(px) for px in row)
    h = height if claimed_height is None else claimed_height
    ihdr = struct.pack(">IIBBBBB", width, h, 8, 2, 0, 0, 0)
    return (
        b"\x89PNG\r\n\x1a\n"
        + png_chunk(b"IHDR", ihdr)
        + png_chunk(b"IDAT", zlib.compress(raw, 9))
        + png_chunk(b"IEND", b"")
    )


def set_lsb(px, bit):
    r, g, b = px
    return ((r & 0xFE) | bit, g, b)


def build_s01(rng):
    """64x64 普通 PNG，红通道最低位藏 'S01-LSB-OK'。"""
    msg = b"S01-LSB-OK"
    bits = "".join(f"{b:08b}" for b in msg)
    need = 64 * 64
    bits = bits + "0" * (need - len(bits))
    idx = 0
    rows = []
    for y in range(64):
        row = []
        for x in range(64):
            base = (20 + x, 20 + y, 90)
            row.append(set_lsb(base, int(bits[idx])))
            idx += 1
        rows.append(row)
    return png_build(64, 64, rows)


def build_s02(rng):
    """64x64，但 IHDR 高度被改成 32 且 CRC 未重算。下半 32 行是一整块红。"""
    rows = []
    for y in range(64):
        row = []
        for x in range(64):
            if y < 32:
                row.append((10 + x // 4, 60, 120 + y))
            else:
                row.append((200, 30, 30))
        rows.append(row)
    blob = bytearray(png_build(64, 64, rows))  # 先按真高度算好 CRC
    blob[20:24] = struct.pack(">I", 32)  # 只改高度字段，CRC 故意留着
    return bytes(blob)


# --------------------------------------------------------------------------
# ZIP（伪加密 + 尾部附加数据）
# --------------------------------------------------------------------------
def make_zip(name, data):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_STORED) as z:
        info = zipfile.ZipInfo(name, date_time=(2026, 11, 10, 0, 0, 0))
        info.external_attr = 0o644 << 16
        z.writestr(info, data)
    return buf.getvalue()


def set_pseudo_encrypt(blob):
    """把本地头与中央目录的 general purpose flag 第 0 位置 1。

    数据本身没有加密，所以解开后内容完整 —— 这就是「伪加密」。
    """
    out = bytearray(blob)
    i = 0
    while True:
        j = out.find(b"PK\x03\x04", i)
        if j < 0:
            break
        flags = struct.unpack("<H", out[j + 6 : j + 8])[0] | 1
        out[j + 6 : j + 8] = struct.pack("<H", flags)
        i = j + 4
    i = 0
    while True:
        j = out.find(b"PK\x01\x02", i)
        if j < 0:
            break
        flags = struct.unpack("<H", out[j + 8 : j + 10])[0] | 1
        out[j + 8 : j + 10] = struct.pack("<H", flags)
        i = j + 4
    return bytes(out)


def build_s03(rng):
    inner = make_zip("readme.txt", b"S03 zip payload: 0x5A\n")
    blob = set_pseudo_encrypt(inner)
    return blob + b"\nS03-TRAILER-appended-note\n"


# --------------------------------------------------------------------------
# gzip（前缀垃圾）
# --------------------------------------------------------------------------
def build_s04(rng):
    junk = bytes(rng.randrange(256) for _ in range(32))
    buf = io.BytesIO()
    with gzip.GzipFile(fileobj=buf, mode="wb", mtime=0) as gz:
        gz.write(b"S04 gzip payload: offset-found\n")
    return junk + buf.getvalue()


# --------------------------------------------------------------------------
# WAV（频谱画 CTF）
# --------------------------------------------------------------------------
FONT = {
    "C": ["01110", "10001", "10000", "10000", "10000", "10001", "01110"],
    "T": ["11111", "00100", "00100", "00100", "00100", "00100", "00100"],
    "F": ["11111", "10000", "10000", "11110", "10000", "10000", "10000"],
}


def build_s05(rng):
    fs = 44100
    block = 0.1  # 每个字符列 0.1 秒
    text = "CTF"
    cols = []
    for ch in text:
        for c in FONT[ch]:
            cols.append(c)
        cols.append("00000")  # 字间距
    nblock = len(cols)
    freqs = [2600 - i * 300 for i in range(7)]  # 上到下 2600→800 Hz
    n = int(fs * block * nblock)
    samples = [0.0] * n
    per = int(fs * block)
    for bi, col in enumerate(cols):
        start = bi * per
        for row, bit in enumerate(col):
            if bit != "1":
                continue
            f = freqs[row]
            for k in range(per):
                t = k / fs
                # 加淡入淡出，避免块边界爆音
                env = min(1.0, k / 200.0, (per - k) / 200.0)
                samples[start + k] += 0.18 * env * __import__("math").sin(
                    2 * 3.141592653589793 * f * t
                )
    buf = io.BytesIO()
    with wave.open(buf, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(fs)
        w.writeframes(
            b"".join(
                struct.pack("<h", max(-32767, min(32767, int(s * 32767))))
                for s in samples
            )
        )
    return buf.getvalue()


# --------------------------------------------------------------------------
# pcap（HTTP 里传 base64）
# --------------------------------------------------------------------------
def csum(data):
    if len(data) % 2:
        data += b"\x00"
    s = 0
    for i in range(0, len(data), 2):
        s += (data[i] << 8) + data[i + 1]
    while s >> 16:
        s = (s & 0xFFFF) + (s >> 16)
    return (~s) & 0xFFFF


CLIENT_IP = bytes([192, 168, 10, 50])
SERVER_IP = bytes([203, 0, 113, 10])
CPORT = 41000
SPORT = 80


def tcp_packet(seq, ack, flags, payload, t):
    src_mac = b"\x02\x00\x00\x00\x00\x01"
    dst_mac = b"\x02\x00\x00\x00\x00\x02"
    eth = dst_mac + src_mac + b"\x08\x00"

    tcp = struct.pack(">HHIIBBHHH", CPORT, SPORT, seq, ack, 5 << 4, flags, 8192, 0, 0)
    pseudo = CLIENT_IP + SERVER_IP + b"\x00\x06" + struct.pack(">H", len(tcp) + len(payload))
    tcp = tcp[:16] + struct.pack(">H", csum(pseudo + tcp + payload)) + tcp[18:]

    iplen = 20 + len(tcp) + len(payload)
    ip = (
        b"\x45\x00"
        + struct.pack(">H", iplen)
        + struct.pack(">H", 1000 + t)
        + b"\x40\x00"
        + b"\x40\x06"
        + b"\x00\x00"
        + CLIENT_IP
        + SERVER_IP
    )
    ip = ip[:10] + struct.pack(">H", csum(ip)) + ip[12:]
    frame = eth + ip + tcp + payload

    rec = struct.pack("<IIII", 1752300000 + t, 0, len(frame), len(frame))
    return rec + frame


def build_s06(rng):
    out = io.BytesIO()
    out.write(struct.pack("<IHHiIII", 0xA1B2C3D4, 2, 4, 0, 0, 65535, 1))
    cseq = 1000
    sseq = 5000
    t = 0
    out.write(tcp_packet(cseq, 0, 0x02, b"", t))  # SYN
    t += 1
    out.write(tcp_packet(sseq, cseq + 1, 0x12, b"", t))  # SYN-ACK
    t += 1
    out.write(tcp_packet(cseq + 1, sseq + 1, 0x10, b"", t))  # ACK
    t += 1

    hidden = base64.b64encode(b"S06-http-b64-ok").decode()
    req = (
        b"GET /files/%E4%BD%A0%E5%A5%BD.txt HTTP/1.1\r\n"
        b"Host: ctf.example\r\n"
        b"User-Agent: curl/8.5.0\r\n"
        b"Cookie: sid=" + hidden.encode() + b"\r\n"
        b"\r\n"
    )
    out.write(tcp_packet(cseq + 1, sseq + 1, 0x18, req, t))
    cseq2 = cseq + 1 + len(req)
    t += 1
    out.write(tcp_packet(sseq + 1, cseq2, 0x10, b"", t))
    t += 1

    body = b"nothing here, keep looking\n"
    resp = (
        b"HTTP/1.1 200 OK\r\n"
        b"Content-Type: text/plain\r\n"
        b"Content-Length: " + str(len(body)).encode() + b"\r\n"
        b"X-Note: " + base64.b64encode(b"S06-header-note") + b"\r\n"
        b"\r\n" + body
    )
    out.write(tcp_packet(sseq + 1, cseq2, 0x18, resp, t))
    sseq2 = sseq + 1 + len(resp)
    t += 1
    out.write(tcp_packet(cseq2, sseq2, 0x10, b"", t))
    return out.getvalue()


# --------------------------------------------------------------------------
# ELF crackme
# --------------------------------------------------------------------------
C_SRC = r"""
#include <stdio.h>
#include <string.h>
static const unsigned char enc[] = {%ENC%};
int main(int argc, char **argv) {
    if (argc < 2) { puts("usage: ./S-07 <key>"); return 1; }
    if (strlen(argv[1]) != sizeof(enc)) { puts("wrong length"); return 1; }
    for (unsigned i = 0; i < sizeof(enc); i++) {
        if ((unsigned char)(argv[1][i] ^ 0x5A) != enc[i]) { puts("nope"); return 1; }
    }
    puts("correct");
    return 0;
}
"""


def build_s07(rng, path):
    key = b"S07-crackme-ok"
    enc = ", ".join(f"0x{b ^ 0x5A:02x}" for b in key)
    src = C_SRC.replace("%ENC%", enc)
    srcpath = os.path.join(OUT, "_S-07.c")
    with open(srcpath, "w") as f:
        f.write(src)
    try:
        subprocess.run(
            ["gcc", "-O0", "-o", path, srcpath], check=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        )
    except (OSError, subprocess.CalledProcessError) as e:
        print(f"  ! 编译失败，跳过 S-07：{e}")
        return None
    finally:
        if os.path.exists(srcpath):
            os.remove(srcpath)
    return key


U01_IPS = [
    ("203.0.113.7", 10),
    ("198.51.100.23", 8),
    ("192.0.2.88", 6),
    ("203.0.113.91", 4),
    ("198.51.100.5", 2),
]


def build_u01_log():
    """U01 的教学用访问日志。30 行，各 IP / 路径 / 状态码的条数全部写死，
    这样正文与题目里的数字不会随随机种子漂移。"""
    rng = random.Random(SEED + 1)
    paths = (
        ["/"] * 8
        + ["/login"] * 6
        + ["/admin"] * 5
        + ["/api/v1/list?page=2"] * 6
        + ["/static/app.js"] * 5
    )
    statuses = [200] * 23 + [404] * 5 + [302] * 2
    ips = []
    for ip, n in U01_IPS:
        ips.extend([ip] * n)
    rng.shuffle(paths)
    rng.shuffle(statuses)
    rng.shuffle(ips)
    lines = []
    for i, (ip, path, st) in enumerate(zip(ips, paths, statuses)):
        method = "POST" if path == "/login" and i % 3 == 0 else "GET"
        lines.append(
            f"2026-11-10T08:{i // 60:02d}:{i % 60:02d}Z {ip} {method} {path} {st} {200 + (i * 137) % 4000}"
        )
    return ("\n".join(lines) + "\n").encode()


def main():
    os.makedirs(OUT, exist_ok=True)
    if "--list" in sys.argv:
        for n in ("S-01", "S-02", "S-03", "S-04", "S-05", "S-06", "S-07"):
            print(n)
        return

    rng = random.Random(SEED)
    items = [
        ("S-01.png", build_s01),
        ("S-02.png", build_s02),
        ("S-03.zip", build_s03),
        ("S-04.gz", build_s04),
        ("S-05.wav", build_s05),
        ("S-06.pcap", build_s06),
    ]
    for name, fn in items:
        blob = fn(rng)
        p = os.path.join(OUT, name)
        with open(p, "wb") as f:
            f.write(blob)
        print(f"  {name:12s} {len(blob):>7d} bytes")

    blob = build_u01_log()
    with open(os.path.join(OUT, "u01-access.log"), "wb") as f:
        f.write(blob)
    print(f"  {'u01-access.log':12s} {len(blob):>7d} bytes")

    key = build_s07(rng, os.path.join(OUT, "S-07"))
    if key:
        print(f"  {'S-07':12s} {os.path.getsize(os.path.join(OUT, 'S-07')):>7d} bytes  正确输入 = {key.decode()}")


if __name__ == "__main__":
    main()
