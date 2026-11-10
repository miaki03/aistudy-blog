#!/usr/bin/env python3
"""校验题目库：每条题要么能被 verify 命令复现答案，要么显式标记为人工验证。

同时扫描 content/ 下所有页面的 TOML front matter，确认引用到的题号都存在。
"""
import json
import pathlib
import subprocess
import sys
import tomllib

ROOT = pathlib.Path(__file__).resolve().parent.parent
KB = ROOT / "kb" / "problems.json"
CONTENT = ROOT / "content"


def load_kb():
    data = json.loads(KB.read_text(encoding="utf-8"))
    return data["problems"]


def check_verifiable(problems):
    failures = []
    for p in problems:
        pid = p["id"]
        if p.get("verify"):
            try:
                out = subprocess.run(
                    p["verify"], shell=True, capture_output=True, text=True, timeout=20
                )
            except subprocess.TimeoutExpired:
                failures.append(f"{pid}: verify 超时")
                continue
            got = out.stdout.strip()
            want = p["answer"].strip()
            if out.returncode != 0:
                failures.append(f"{pid}: verify 退出码 {out.returncode} / {out.stderr.strip()[:80]}")
            elif got != want:
                failures.append(f"{pid}: 期望 {want!r}，实得 {got!r}")
        elif not p.get("manual"):
            failures.append(f"{pid}: 既没有 verify 也没标 manual")
        else:
            if not p.get("evidence", "").strip():
                failures.append(f"{pid}: manual 题缺少 evidence")
    return failures


def front_matter(path):
    text = path.read_text(encoding="utf-8")
    if not text.startswith("+++"):
        return None
    end = text.find("\n+++", 3)
    if end == -1:
        return None
    try:
        return tomllib.loads(text[3:end])
    except tomllib.TOMLDecodeError as exc:
        return {"__error__": str(exc)}


def check_pages(problems):
    ids = {p["id"] for p in problems}
    failures = []
    for path in sorted(CONTENT.rglob("*.md")):
        fm = front_matter(path)
        if not fm:
            continue
        if "__error__" in fm:
            failures.append(f"{path.name}: front matter 解析失败：{fm['__error__']}")
            continue
        for pid in fm.get("problems", []):
            if pid not in ids:
                failures.append(f"{path.name}: 引用了不存在的题号 {pid}")
        # 只有课程页（skill / project）强制要求课程元数据
        if path.parent.name in ("skill", "project"):
            for key in ("chapter", "stage", "minutes"):
                if key not in fm:
                    failures.append(f"{path.name}: 缺少字段 {key}")
    return failures


def main():
    problems = load_kb()
    print(f"题目库共 {len(problems)} 条")
    failures = check_verifiable(problems) + check_pages(problems)
    if failures:
        print("\n发现 %d 个问题：" % len(failures))
        for f in failures:
            print("  -", f)
        return 1
    print("全部通过：题目答案可复现，页面引用的题号都存在")
    return 0


if __name__ == "__main__":
    sys.exit(main())
