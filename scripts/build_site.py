#!/usr/bin/env python3
"""把仓库 Markdown 生成静态网页：GitHub 只作源码仓库，全部内容在网页内阅读。

生成：
  cases/*.md            -> cases/*.html（案例拆解页，顶部带「阅读原文」按钮）
  LEADERBOARD.md        -> leaderboard.html
  STANDARDS.md          -> standards.html
  guide/7-stage-map.md  -> guide.html
index.html（榜单首页）为手工维护页，本脚本不覆盖。
用法：python3 scripts/build_site.py
"""
import re
import sys
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent.parent

ORIGINALS = {
    "FDE-001-liangzhu-fde-framework": ("https://x.com/liangzhu_AI", "作者主页 ↗（原帖直链待补）"),
    "FDE-002-openai-deployment-gap": ("https://openai.com/index/forward-deployed-engineering-means/", "阅读原文 ↗"),
    "FDE-003-miles-mazy-geely-training": ("https://x.com/miles_mazy/status/2113624481759429118", "阅读原文 ↗"),
    "FDE-004-china-entrepreneur-fde-truth": ("https://finance.sina.cn/stock/jdts/2026-10-21/detail-inivysym6175878.d.html", "阅读原文 ↗"),
}

CSS = """
:root{--bg:#faf8f5;--card:#fff;--ink:#23202b;--sub:#6d6759;--line:#e8e2d6;--accent:#b4632a;--accent2:#2f6f5e}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font-family:"Noto Sans CJK SC","PingFang SC","Microsoft YaHei",sans-serif;line-height:1.75}
.wrap{max-width:820px;margin:0 auto;padding:28px 18px 64px}
.topnav{font-size:14px;margin-bottom:20px}
.topnav a{color:var(--accent);text-decoration:none;margin-right:16px}
.topnav a:hover{text-decoration:underline}
article{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:26px 28px;box-shadow:0 1px 3px rgba(60,50,30,.05)}
article h1{font-size:25px;line-height:1.4;margin:0 0 14px}
article h2{font-size:19px;margin:28px 0 8px;padding-top:14px;border-top:1px solid var(--line)}
article h3{font-size:16px;margin:20px 0 6px}
article a{color:var(--accent)}
article table{width:100%;border-collapse:collapse;font-size:13.5px;margin:12px 0;display:block;overflow-x:auto}
article th,article td{border:1px solid var(--line);padding:7px 10px;text-align:left;vertical-align:top}
article th{background:#f3eee3}
article blockquote{border-left:3px solid var(--accent);margin:12px 0;padding:6px 14px;background:#fbf7ee;color:var(--ink)}
article hr{border:none;border-top:1px solid var(--line);margin:22px 0}
article em{color:var(--sub)}
.origin{display:inline-block;background:var(--accent);color:#fff !important;text-decoration:none;font-weight:600;font-size:14.5px;padding:9px 20px;border-radius:8px;margin:4px 0 14px}
footer{margin-top:26px;color:var(--sub);font-size:13px}
footer a{color:var(--accent);text-decoration:none}
"""

TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — FDE Casebook</title>
<style>{css}</style>
</head>
<body>
<div class="wrap">
<nav class="topnav">
  <a href="{prefix}index.html">榜单首页</a>
  <a href="{prefix}leaderboard.html">完整榜单</a>
  <a href="{prefix}standards.html">入选标准</a>
  <a href="{prefix}guide.html">7 环节能力地图</a>
</nav>
<article>
{origin}
{body}
</article>
<footer><p>FDE Casebook · 本页由仓库 Markdown 自动生成，GitHub 仅作源码仓库。维护：Bruce Cao（<a href="https://x.com/sycbruce">@sycbruce</a>）</p></footer>
</div>
</body>
</html>
"""


def fix_links(html: str) -> str:
    """站内 .md 链接改 .html；裸 URL 转可点链接（不在标签属性内时）。"""
    html = re.sub(r'href="([^"]+)\.md(["#])', r'href="\1.html\2', html)
    html = html.replace('href="LEADERBOARD.html"', 'href="leaderboard.html"')
    html = html.replace('href="STANDARDS.html"', 'href="standards.html"')
    html = html.replace('href="../leaderboard.html"', 'href="../leaderboard.html"')
    return html


def convert(md_path: Path, out_path: Path, prefix: str, origin_html: str = "") -> str:
    text = md_path.read_text(encoding="utf-8")
    m = re.search(r"^# (.+)$", text, re.M)
    title = m.group(1).strip() if m else md_path.stem
    body = markdown.markdown(text, extensions=["tables", "sane_lists"])
    body = fix_links(body)
    page = TEMPLATE.format(title=title, css=CSS, prefix=prefix, origin=origin_html, body=body)
    out_path.write_text(page, encoding="utf-8")
    return title


def main() -> int:
    jobs = []
    for md in sorted((ROOT / "cases").glob("*.md")):
        stem = md.stem
        url, label = ORIGINALS.get(stem, ("", ""))
        origin = f'<a class="origin" href="{url}" target="_blank" rel="noopener">{label}</a>' if url else ""
        jobs.append((md, ROOT / "cases" / f"{stem}.html", "../", origin))
    jobs.append((ROOT / "LEADERBOARD.md", ROOT / "leaderboard.html", "", ""))
    jobs.append((ROOT / "STANDARDS.md", ROOT / "standards.html", "", ""))
    jobs.append((ROOT / "guide" / "7-stage-map.md", ROOT / "guide.html", "", ""))
    for md, out, prefix, origin in jobs:
        t = convert(md, out, prefix, origin)
        print(f"built {out.relative_to(ROOT)}  <-  {md.relative_to(ROOT)}  ({t[:40]})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
