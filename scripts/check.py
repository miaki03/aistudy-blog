#!/usr/bin/env python3
"""统一校验入口。检查项随课程进度生长，不预写没用的检查。

当前检查：
  1. 题目库（转调 check-kb.py）
  2. 概念台账：页面声明的概念必须已登记，且台账的 first 必须指向真的定义了它的章
  3. 复用门槛：课程页必须声明 ≥3 个后续复用章

用法：python3 scripts/check.py
"""

import json
import pathlib
import subprocess
import sys
import tomllib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
CONTENT = ROOT / "content"
KB = ROOT / "kb"


def run(cmd):
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    return r.returncode, (r.stdout + r.stderr).strip()


def front_matter(path):
    text = path.read_text(encoding="utf-8")
    if not text.startswith("+++"):
        return None
    end = text.find("\n+++", 3)
    if end == -1:
        return None
    return tomllib.loads(text[3:end])


def course_pages():
    out = []
    for sub in ("skill", "project"):
        for p in sorted((CONTENT / sub).glob("*.md")):
            fm = front_matter(p)
            if fm:
                out.append((p, fm))
    return out


def check_concepts(pages):
    """概念台账一致性。"""
    reg = json.loads((KB / "concepts.json").read_text(encoding="utf-8"))["concepts"]
    issues = []

    claimed = {}
    for path, fm in pages:
        chapter = fm.get("chapter", "?")
        for cid in fm.get("concepts", []):
            if cid not in reg:
                issues.append(f"{path.name}: 概念 {cid} 未在 concepts.json 登记")
                continue
            owner = reg[cid]["first"]
            if owner != chapter:
                issues.append(
                    f"{path.name}: 声明首次定义 {cid}，但台账记的是 {owner}"
                )
            if cid in claimed:
                issues.append(
                    f"{cid} 被 {claimed[cid]} 和 {chapter} 都声明为首次定义"
                )
            claimed[cid] = chapter

    # 台账里写了 first 的章，必须真的声明了它
    for cid, meta in reg.items():
        owner = meta.get("first")
        if owner and cid not in claimed:
            issues.append(f"台账记 {cid} 由 {owner} 首次定义，但那一章没声明它")

    return issues, len(reg), len(claimed)


def check_reuse(pages):
    """复用门槛：每个技能页必须写出 ≥3 个后续复用它的章。"""
    issues = []
    for path, fm in pages:
        if path.parent.name != "skill":
            continue
        reuse = fm.get("reuse", [])
        if len(reuse) < 3:
            issues.append(
                f"{path.name}: 复用点只有 {len(reuse)} 个（门槛 3）——考虑降为章末速查表"
            )
    return issues


def main():
    print("=" * 60)
    print("[1/3] 题目库")
    code, out = run([sys.executable, str(SCRIPTS / "check-kb.py")])
    for line in out.splitlines():
        print("     " + line)

    print("[2/3] 概念台账")
    pages = course_pages()
    c_issues, n_reg, n_claimed = check_concepts(pages)
    print(f"     登记 {n_reg} 个概念，{len(pages)} 个课程页声明了 {n_claimed} 个")
    for i in c_issues:
        print("     ! " + i)

    print("[3/3] 复用门槛")
    r_issues = check_reuse(pages)
    for i in r_issues:
        print("     ! " + i)
    if not r_issues:
        print("     全部课程页通过")

    print("=" * 60)
    bad = (code != 0) + len(c_issues) + len(r_issues)
    if bad:
        print(f"未通过：共 {len(c_issues) + len(r_issues)} 处问题，题目库退出码 {code}")
        return 1
    print("全部通过")
    return 0


if __name__ == "__main__":
    sys.exit(main())
