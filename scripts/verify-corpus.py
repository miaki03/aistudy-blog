#!/usr/bin/env python3
"""核对贯穿样本集是否真的藏着各自该藏的东西。

这份脚本同时是 samples/corpus 的答案键：正文里写的「藏了什么」
必须能在这里复算出来，否则说明样本或正文有一边错了。

用法：python3 scripts/verify-corpus.py
"""

import base64
import gzip
import io
import os
import struct
import subprocess
import sys
import zlib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
C = os.path.join(ROOT, "static", "samples")

ok = True


def check(name, cond, detail=""):
    global ok
    print(f"  [{'ok' if cond else 'FAIL'}] {name}{('  ' + detail) if detail else ''}")
    if not cond:
        ok = False


def png_chunks(blob):
    i = 8
    out = []
    while i < len(blob):
        ln = struct.unpack(">I", blob[i : i + 4])[0]
        tag = blob[i + 4 : i + 8]
        data = blob[i + 8 : i + 8 + ln]
        crc = struct.unpack(">I", blob[i + 8 + ln : i + 12 + ln])[0]
        out.append((tag, data, crc))
        i += 12 + ln
    return out


def png_raw(blob):
    for tag, data, _ in png_chunks(blob):
        if tag == b"IDAT":
            return zlib.decompress(data)
    return b""


# ---- S-01 ----------------------------------------------------------------
b = open(os.path.join(C, "S-01.png"), "rb").read()
ihdr = png_chunks(b)[0][1]
w, h = struct.unpack(">II", ihdr[:8])
raw = png_raw(b)
px = [raw[y * (1 + w * 3) + 1 + x * 3] for y in range(h) for x in range(w)]
bits = "".join(str(v & 1) for v in px)
msg = bytes(int(bits[i : i + 8], 2) for i in range(0, 80, 8))
check("S-01 尺寸 64x64", (w, h) == (64, 64), f"{w}x{h}")
check("S-01 LSB 前 10 字节", msg == b"S01-LSB-OK", msg.decode("latin1"))

# ---- S-02 ----------------------------------------------------------------
b = open(os.path.join(C, "S-02.png"), "rb").read()
chunks = png_chunks(b)
ihdr_data, ihdr_crc = chunks[0][1], chunks[0][2]
w, claimed_h = struct.unpack(">II", ihdr_data[:8])
real_crc = zlib.crc32(b"IHDR" + ihdr_data) & 0xFFFFFFFF
raw = png_raw(b)
real_h = len(raw) // (1 + w * 3)
check("S-02 IHDR CRC 不符", real_crc != ihdr_crc, f"文件={ihdr_crc:#010x} 实算={real_crc:#010x}")
check("S-02 声称高度 32", claimed_h == 32, str(claimed_h))
check("S-02 实际高度 64", real_h == 64, str(real_h))

# ---- S-03 ----------------------------------------------------------------
import zipfile

b = open(os.path.join(C, "S-03.zip"), "rb").read()
zf = zipfile.ZipFile(os.path.join(C, "S-03.zip"))
info = zf.infolist()[0]
eocd = b.rfind(b"PK\x05\x06")
trailer = b[eocd + 22 :] if eocd >= 0 else b""
check("S-03 标志位声明加密", bool(info.flag_bits & 1), f"flag_bits={info.flag_bits:#06x}")
check("S-03 尾部附加数据", trailer == b"\nS03-TRAILER-appended-note\n", repr(trailer))

# 伪加密的修法：把本地头与中央目录里的第 0 位清零，数据本来就没加密
fixed = bytearray(b)
for sig, off in ((b"PK\x03\x04", 6), (b"PK\x01\x02", 8)):
    i = 0
    while True:
        j = fixed.find(sig, i)
        if j < 0:
            break
        flags = struct.unpack("<H", fixed[j + off : j + off + 2])[0] & ~1
        fixed[j + off : j + off + 2] = struct.pack("<H", flags)
        i = j + 4
inner = zipfile.ZipFile(io.BytesIO(bytes(fixed))).read(info.filename)
check("S-03 清标志位后可读", inner.endswith(b": 0x5A\n"), inner.decode("latin1").strip())

# ---- S-04 ----------------------------------------------------------------
b = open(os.path.join(C, "S-04.gz"), "rb").read()
off = b.find(b"\x1f\x8b\x08")
check("S-04 gzip 魔数偏移 32", off == 32, str(off))
try:
    text = gzip.decompress(b).decode()
    from0 = "解压成功（不该）"
except Exception:
    from0 = "报错（预期）"
check("S-04 从 0 解压失败", "报错" in from0, from0)
check(
    "S-04 从偏移 32 解压",
    gzip.decompress(b[off:]) == b"S04 gzip payload: offset-found\n",
    gzip.decompress(b[off:]).decode().strip(),
)

# ---- S-05 ----------------------------------------------------------------
import wave

with wave.open(os.path.join(C, "S-05.wav"), "rb") as wv:
    fs = wv.getframerate()
    nch = wv.getnchannels()
    n = wv.getnframes()
    frames = wv.readframes(n)
samples = struct.unpack("<" + str(n) + "h", frames)
check("S-05 44100Hz 单声道", (fs, nch) == (44100, 1), f"{fs}Hz {nch}ch {n/fs:.2f}s")


def mag_at(seg, freq):
    """用 Goertzel 算某个频率的能量，避免引入 numpy。"""
    k = 2 * 3.141592653589793 * freq / fs
    c = 2 * 3.141592653589793 * freq / fs
    s_prev = s_prev2 = 0.0
    coeff = 2 * 3.141592653589793
    import math

    coeff = 2 * math.cos(c)
    for x in seg:
        s = x + coeff * s_prev - s_prev2
        s_prev2, s_prev = s_prev, s
    return s_prev2 * s_prev2 + s_prev * s_prev - coeff * s_prev * s_prev2


per = int(fs * 0.1)
col0 = samples[0:per]
e2300 = mag_at(col0, 2300)
e800 = mag_at(col0, 800)
check("S-05 第 1 列在 2300Hz 有能量（C 的上横）", e2300 > e800 * 5, f"{e2300:.3g} vs {e800:.3g}")

# ---- S-06 ----------------------------------------------------------------
b = open(os.path.join(C, "S-06.pcap"), "rb").read()
assert b[:4] == b"\xd4\xc3\xb2\xa1"
pos = 24
payloads = []
while pos + 16 <= len(b):
    _, _, incl, _ = struct.unpack("<IIII", b[pos : pos + 16])
    frame = b[pos + 16 : pos + 16 + incl]
    pos += 16 + incl
    if len(frame) < 54:
        continue
    ihl = (frame[14] & 0x0F) * 4
    tcp_off = 14 + ihl
    doff = (frame[tcp_off + 12] >> 4) * 4
    payloads.append(frame[tcp_off + doff :])
stream = b"".join(payloads)
check("S-06 抓到 HTTP 请求行", b"GET /files/" in stream)
import re

m = re.search(rb"Cookie: sid=([A-Za-z0-9+/=]+)", stream)
cookie = m.group(1) if m else b""
check(
    "S-06 Cookie 里是 base64",
    base64.b64decode(cookie) == b"S06-http-b64-ok",
    base64.b64decode(cookie).decode() if cookie else "",
)
from urllib.parse import unquote

check("S-06 URL 里的 %xx", unquote("/files/%E4%BD%A0%E5%A5%BD.txt").endswith("你好.txt"))
check("S-06 响应头里有 base64", b"X-Note: " + base64.b64encode(b"S06-header-note") in stream)

# ---- S-07 ----------------------------------------------------------------
p = os.path.join(C, "S-07")
if os.path.exists(p):
    r_bad = subprocess.run([p, "wrong-key"], capture_output=True)
    r_ok = subprocess.run([p, "S07-crackme-ok"], capture_output=True)
    check("S-07 错误输入被拒", r_bad.returncode != 0, r_bad.stdout.decode().strip())
    check("S-07 正确输入", r_ok.stdout.decode().strip() == "correct", r_ok.stdout.decode().strip())
else:
    check("S-07 存在", False)

print("\n全部通过" if ok else "\n有失败项")
sys.exit(0 if ok else 1)
