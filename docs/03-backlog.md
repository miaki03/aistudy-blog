# 任务清单

每项任务应能在**一次会话内**完成。完成即移到「已完成」并更新 `06-progress.md`。

## 正在做

- [ ] **B-01** 把 `content/skill/file-magic.md` 按新风格校准：去掉比喻、补前置概念、补原理说明

## 紧接着

- [ ] **B-02** 新增 `S-BIN`（位、字节、十六进制、ASCII、位运算）——它是 B64 的前置，目前缺失
- [ ] **B-03** 新增 `S-CLI`（命令行：ls/cat/grep/管道/重定向），P1 项目需要
- [ ] **B-04** 新增 `S-PY`（Python 够用版），后续隐写页都依赖它
- [ ] **B-05** 实现 `claims` 机制：`kb/claims.json` + `scripts/check-claims.py`，把知识性断言也纳入机器校验

## 之后

- [ ] **B-06** 新增 `S-LSB`、`S-META`、`S-AUDIO`、`S-ZIP`
- [ ] **B-07** 新增 `S-CLASSIC`、`S-TRANSPOSE`
- [ ] **B-08** 新增 `S-PH-TYPE`、`S-PH-EXTRACT`、`S-PH-META`
- [ ] **B-09** 新增 `S-OSINT`、`S-WEB`
- [ ] **B-10** 新增 `S-ARG-TRAIL`、`S-ARG-MEDIA`
- [ ] **B-11** 项目页 P2–P5
- [ ] **B-12** 课程索引页（按依赖自动生成学习顺序）
- [ ] **B-13** 免责声明页（版权署名与「仅供个人学习」）

## 已完成

- [x] 站点从 `miaki-blog` 拆出为独立仓库 `aistudy-blog`
- [x] 8 篇旧文迁移
- [x] 题目库 `kb/problems.json` + `scripts/check-kb.py`
- [x] S-B64 两轮修订（补手算、改启发式、按保姆级重写）
- [x] S-FILE 初版
- [x] P1 项目页
- [x] 项目文档（AGENTS.md、docs/00–06）

## 已知问题

| 问题 | 影响 | 处理 |
| --- | --- | --- |
| `baseURL` 仍是 `learning-path.pages.dev` 占位 | canonical 指向错误域名 | 等用户确认域名后改 |
| 旧版 8 篇无 `chapter`/`stage` 字段 | 无法纳入课程地图 | 校验脚本已对 post 豁免 |
| 技能页全部 `draft = true` | 线上看不到 | 需用户确认后逐页发布 |
