#!/usr/bin/env python3
"""入门自测：生成 5 道题的样本，并给出答案键。

用法：
    python3 scripts/selftest.py          # 生成样本 + 打印答案键
    python3 scripts/selftest.py --quiet  # 只生成样本

样本落在 samples/selftest/。答案键只用于我判卷，不给读者。
"""

import base64
import gzip
import io
import json
import os
import random
import struct
import zlib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "static", "samples", "selftest")


def png_8x8(pixels):
    """无滤镜 8x8 RGB PNG，只依赖标准库。pixels[y][x] = (r,g,b)"""
    raw = b""
    for row in pixels:
        raw += b"\x00" + b"".join(bytes(px) for px in row)

    def chunk(tag, data):
        return (
            struct.pack(">I", len(data))
            + tag
            + data
            + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
        )

    ihdr = struct.pack(">IIBBBBB", 8, 8, 8, 2, 0, 0, 0)
    return (
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", ihdr)
        + chunk(b"IDAT", zlib.compress(raw, 9))
        + chunk(b"IEND", b"")
    )


def main():
    os.makedirs(OUT, exist_ok=True)
    random.seed(20261110)
    key = {}

    # ---- T1 · 字节与端序 ----------------------------------------------
    tail = bytes([0xDE, 0xAD, 0xBE, 0xEF])
    t1 = bytes(random.randrange(256) for _ in range(28)) + tail
    with open(os.path.join(OUT, "t1.bin"), "wb") as f:
        f.write(t1)
    key["T1"] = {
        "size": len(t1),
        "last4_hex": " ".join(f"{b:02x}" for b in tail),
        "last4_be_int": struct.unpack(">I", tail)[0],
        "last4_le_int": struct.unpack("<I", tail)[0],
    }

    # ---- T2 · 多层 Base64 --------------------------------------------
    plain = b"nested-done"
    layer = plain
    layers = 0
    while layers < 3:
        layer = base64.b64encode(layer)
        layers += 1
    t2 = layer.decode()
    with open(os.path.join(OUT, "t2.txt"), "w", encoding="utf-8") as f:
        f.write(t2 + "\n")
    key["T2"] = {"layers": layers, "plaintext": plain.decode(), "given": t2}

    # ---- T3 · 带前缀的 gzip ------------------------------------------
    secret_line = "offset-handled flag=selftest_3f9a"
    junk = bytes(random.randrange(256) for _ in range(16))
    buf = io.BytesIO()
    with gzip.GzipFile(fileobj=buf, mode="wb", mtime=0) as gz:
        gz.write((secret_line + "\n").encode())
    payload = buf.getvalue()
    with open(os.path.join(OUT, "t3.bin"), "wb") as f:
        f.write(junk + payload)
    key["T3"] = {
        "total_size": len(junk) + len(payload),
        "prefix_size": len(junk),
        "gzip_starts_at": len(junk),
        "first_line": secret_line,
    }

    # ---- T4 · 日志统计 ------------------------------------------------
    ips = {
        "203.0.113.7": 41,
        "198.51.100.23": 33,
        "192.0.2.88": 27,
        "203.0.113.91": 12,
        "198.51.100.5": 9,
        "192.0.2.140": 7,
        "203.0.113.204": 5,
        "198.51.100.77": 3,
    }
    pool = []
    for ip, n in ips.items():
        pool.extend([ip] * n)
    random.shuffle(pool)
    paths = ["/", "/login", "/api/v1/list", "/static/app.js", "/admin"]
    lines = []
    for i, ip in enumerate(pool):
        ts = f"2026-11-10T{8 + i // 3600:02d}:{(i // 60) % 60:02d}:{i % 60:02d}Z"
        lines.append(
            f"{ts} {ip} GET {random.choice(paths)} 200 {random.randrange(200, 9000)}"
        )
    with open(os.path.join(OUT, "t4.log"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    top3 = sorted(ips.items(), key=lambda kv: (-kv[1], kv[0]))[:3]
    key["T4"] = {"lines": len(lines), "top3": [[ip, n] for ip, n in top3]}

    # ---- T5 · 位平面 --------------------------------------------------
    msg = b"HI"
    bits = "".join(f"{b:08b}" for b in msg)  # 16 位
    pixels = []
    bit_iter = iter(bits + "0" * 48)
    for y in range(8):
        row = []
        for x in range(8):
            bit = int(next(bit_iter))
            r = (random.randrange(256) & 0xFE) | bit  # 最低位承载消息
            row.append((r, random.randrange(256), random.randrange(256)))
        pixels.append(row)
    with open(os.path.join(OUT, "t5.png"), "wb") as f:
        f.write(png_8x8(pixels))
    lsb_string = "".join(str(px[0] & 1) for row in pixels for px in row)
    chars = "".join(
        chr(int(lsb_string[i : i + 8], 2)) for i in range(0, 16, 8)
    )
    key["T5"] = {
        "first16_bits": lsb_string[:16],
        "first2_chars": chars,
    }

    print(json.dumps(key, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
