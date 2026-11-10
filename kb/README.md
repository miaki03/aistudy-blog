# 题目库（机器可校验）

`problems.json` 里每条题都必须满足一条：**要么有 `verify` 命令且输出等于 `answer`，要么显式标 `manual` 并给出 `evidence`**。

`scripts/check-kb.py` 会真的执行 `verify` 并比对输出——这就是防止「AI 编题」的机制。

```json
{
  "id": "B64-01",
  "page": "base64-family",
  "skills": ["base64"],
  "difficulty": 1,
  "minutes": 3,
  "answer": "flag{...}",
  "verify": "echo ... | base64 -d"
}
```

人工验证的题型（如文件头判断）这样写：

```json
{
  "id": "F-01",
  "manual": true,
  "evidence": "为什么这个答案成立，尽量给可核对的事实"
}
```

页面通过 TOML front matter 引用题号：

```toml
problems = ["B64-01", "B64-02"]
```

`check-kb.py` 同时会检查：页面引用的题号是否存在、页面是否写了 `chapter` / `stage` / `minutes`。
