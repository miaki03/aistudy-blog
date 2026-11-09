# 学习路径 · ARG / CTF / Puzzle Hunt

16 周单人自学教材站，Hugo + [Stack](https://github.com/CaiJimmy/hugo-theme-stack) 主题。

## 结构

```
hugo.toml                    站点配置（permalink /p/:slug/ 与暗色主题）
content/post/*.md            8 篇文章（总览 + 00–06）
content/page/about.md        关于页
content/categories/学习路径/  分类描述
themes/hugo-theme-stack/     主题（git submodule）
```

## 本地预览

```bash
hugo server -D
```

## 构建

```bash
hugo --gc --minify
```

产物在 `public/`。

## 部署到 Cloudflare Pages

在 Cloudflare Pages 新建项目并连接本仓库：

| 配置项 | 值 |
| --- | --- |
| Framework preset | Hugo |
| Build command | `hugo --gc --minify` |
| Build output directory | `public` |
| 环境变量 | `HUGO_VERSION` = `0.164.0` |

主题通过 git submodule 引入，Cloudflare Pages 构建时会自动拉取子模块。

## 注意

- `baseURL` 在 `hugo.toml` 里目前是占位值 `https://learning-path.pages.dev/`，绑定正式域名后改成实际域名，否则 canonical 链接会指错。
- 文章日期必须早于构建时间，否则 Hugo 默认不渲染未来内容。
- `public/`、`resources/_gen/`、`.hugo_build.lock` 已在 `.gitignore` 中。
