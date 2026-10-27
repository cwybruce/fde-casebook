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
import html
import re
import sys
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent.parent

CASE_STEMS = [
    "FDE-001-liangzhu-fde-framework",
    "FDE-002-openai-deployment-gap",
    "FDE-003-miles-mazy-geely-training",
    "FDE-004-china-entrepreneur-fde-truth",
    "FDE-005-bylixing-agent-into-enterprise",
    "FDE-006-john-deere-ai-customer-success",
    "FDE-007-bbva-chatgpt-enterprise-rollout",
    "FDE-008-morgan-stanley-eval-first",
    "FDE-009-cnzhihao-funds-report",
    "FDE-010-miles-mazy-data-cleaning",
]

CSS = """
:root{
  --paper:#f7f4ee;--surface:#fffdfa;--surface-muted:#f0ebe2;--ink:#202522;--sub:#66675f;
  --line:#ded8cc;--line-strong:#c7bfb1;--accent:#954b25;--accent-bright:#dda77d;--green:#2f6656;
  --grade-s:#98711c;--grade-a:#954b25;--grade-b:#526b7b;--night:#19211f;--night-sub:#b9c1ba;
  --font-sans:"Noto Sans CJK SC","PingFang SC","Microsoft YaHei",system-ui,sans-serif;
  --font-serif:Georgia,"Songti SC","Noto Serif CJK SC","SimSun",serif;
  --text-xs:12px;--text-sm:14px;--text-base:16.5px;--text-h3:19px;--text-h2:26px;--text-h1:42px;
  --space-1:4px;--space-2:8px;--space-3:12px;--space-4:16px;--space-5:24px;--space-6:32px;--space-7:48px;--space-8:64px;
  --radius-sm:5px;--radius:9px;--shadow:0 8px 24px rgba(34,39,32,.045);--measure:880px;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth;scroll-padding-top:24px}
body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--font-sans);font-size:var(--text-base);line-height:1.85;-webkit-font-smoothing:antialiased}
a{color:var(--accent);text-underline-offset:3px}
a:focus-visible,[tabindex]:focus-visible{outline:2px solid var(--accent);outline-offset:4px}
.wrap{width:min(var(--measure),calc(100% - 48px));margin-inline:auto}
.topnav{display:flex;align-items:center;justify-content:space-between;gap:24px;min-height:72px;border-bottom:1px solid var(--line);font-size:var(--text-sm)}
.brand{color:var(--ink);font-family:var(--font-serif);font-size:18px;font-weight:700;letter-spacing:-.02em;text-decoration:none;white-space:nowrap}
.navlinks{display:flex;align-items:center;gap:4px;flex-wrap:wrap}
.navlinks a{display:inline-flex;align-items:center;min-height:40px;padding:4px 10px;color:var(--sub);text-decoration:none;border-radius:var(--radius-sm)}
.navlinks a:hover{color:var(--accent);background:var(--surface-muted)}
.page-hero{background:var(--night);color:#f6f2e9;border-bottom:3px solid var(--accent)}
.page-hero .wrap{padding-block:52px 46px}
.eyebrow{margin:0 0 18px;color:var(--accent-bright);font-size:var(--text-xs);font-weight:700;letter-spacing:.16em;text-transform:uppercase}
.page-hero h1{max-width:780px;margin:0;font-family:var(--font-serif);font-size:clamp(32px,5vw,var(--text-h1));font-weight:700;line-height:1.28;letter-spacing:-.035em}
.case-meta{display:flex;gap:8px;flex-wrap:wrap;margin:0 0 22px;padding:0;list-style:none}
.case-meta li{padding:3px 10px;border:1px solid #46504a;border-radius:var(--radius-sm);color:#d5dbd4;font-size:var(--text-xs);line-height:1.7}
.score-band{display:flex;align-items:center;gap:22px;flex-wrap:wrap;margin-top:30px;padding-top:24px;border-top:1px solid #3a433e}
.total-score{display:flex;align-items:baseline;gap:7px;font-variant-numeric:tabular-nums;line-height:1}
.total-score strong{font-family:var(--font-serif);font-size:52px;font-weight:400;letter-spacing:-.04em}
.total-score span{color:var(--night-sub);font-size:var(--text-sm)}
.grade{display:inline-flex;align-items:center;justify-content:center;min-height:28px;padding:2px 10px;border:1px solid currentColor;border-radius:var(--radius-sm);font-size:var(--text-sm);font-weight:700;line-height:1.2;white-space:nowrap}
.grade-s{color:#e0bc69}.grade-a{color:var(--accent-bright)}.grade-b{color:#a8bfce}
.rank{color:var(--night-sub);font-size:var(--text-sm)}
.origin{display:inline-flex;align-items:center;justify-content:center;min-height:44px;margin-left:auto;padding:8px 18px;background:var(--accent-bright);border:1px solid var(--accent-bright);border-radius:var(--radius-sm);color:var(--night)!important;font-size:var(--text-sm);font-weight:700;text-decoration:none;transition:background .18s ease,transform .18s ease}
.origin:hover{background:#edbd97;transform:translateY(-1px)}
.article-body{padding-block:36px 64px}
.content-section{margin:0 0 24px;padding:30px 34px;background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);box-shadow:var(--shadow);overflow-wrap:anywhere}
.content-section.intro{padding-top:26px}
.content-section h2{margin:0 0 20px;padding-bottom:14px;border-bottom:1px solid var(--line);font-family:var(--font-serif);font-size:var(--text-h2);line-height:1.4;letter-spacing:-.025em}
.content-section h3{margin:28px 0 10px;font-size:var(--text-h3);line-height:1.55;letter-spacing:-.015em}
.content-section p{margin:0 0 17px}
.content-section p:last-child{margin-bottom:0}
.content-section ul,.content-section ol{margin:0 0 18px;padding-left:1.5em}
.content-section li{margin:7px 0}
.content-section a{overflow-wrap:anywhere}
.source-meta{margin:0!important;padding:0!important;list-style:none;color:var(--sub);font-size:var(--text-sm)}
.source-meta li{padding:9px 0;margin:0;border-bottom:1px solid var(--line)}
.source-meta li:last-child{border-bottom:0}
.summary-section{border-top:3px solid var(--green)}
.summary-section p:last-child{font-family:var(--font-serif);font-size:20px;line-height:1.75}
.stage-section{background:#f2f3ed;border-color:#d5ddd2}
.verdict-section{border-left:3px solid var(--accent)}
.verdict-section p:last-child{font-size:18px}
.excerpt-section{scroll-margin-top:24px}
blockquote{margin:22px 0;padding:20px 24px;background:var(--surface-muted);border-left:3px solid var(--accent);color:var(--ink)}
blockquote p{font-family:var(--font-serif);line-height:1.85}
.content-section em{color:var(--sub);font-size:var(--text-sm)}
.table-scroll{width:100%;margin:20px 0;overflow-x:auto;border:1px solid var(--line);border-radius:var(--radius-sm)}
table{width:100%;min-width:560px;border-collapse:collapse;font-size:var(--text-sm);line-height:1.7;font-variant-numeric:tabular-nums}
.score-table{min-width:660px}
th,td{min-width:96px;padding:13px 15px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}
th{background:var(--surface-muted);color:#484d47;font-size:var(--text-xs);font-weight:700;letter-spacing:.04em;white-space:nowrap}
tr:last-child td{border-bottom:0}
td:nth-child(2){white-space:nowrap}
.score-section{padding:0;overflow:hidden;border-top:3px solid var(--green)}
.score-section>h2{margin:0;padding:26px 34px 20px;background:#eef1e9;border-bottom:1px solid #d5ddd2}
.score-section>.table-scroll{margin:0;border:0;border-radius:0}
.score-section td:first-child{font-weight:700;white-space:nowrap}
.score-section td:nth-child(2){color:var(--green);font-weight:700}
.coverage-note{margin:0!important;padding:24px 34px;background:#f8f8f2;border-top:1px solid #d5ddd2}
.coverage-note strong{color:var(--green);font-size:var(--text-sm);letter-spacing:.05em}
hr{border:0;border-top:1px solid var(--line);margin:30px 0}
footer{border-top:1px solid var(--line);color:var(--sub);font-size:var(--text-xs)}
footer .wrap{padding-block:24px 40px}
footer p{margin:0}
footer a{min-height:40px;display:inline-flex;align-items:center}
@media(max-width:680px){
  :root{--text-base:16px;--text-h2:23px}
  .wrap{width:min(var(--measure),calc(100% - 32px))}
  .topnav{align-items:flex-start;flex-direction:column;gap:4px;padding-block:14px 10px}
  .navlinks{width:100%;gap:0 2px}
  .navlinks a{padding-inline:8px;font-size:13px}
  .page-hero .wrap{padding-block:34px 30px}
  .page-hero h1{font-size:32px;line-height:1.35}
  .case-meta{margin-bottom:18px}
  .score-band{gap:14px;margin-top:24px;padding-top:20px}
  .total-score strong{font-size:46px}
  .origin{width:100%;margin:6px 0 0}
  .article-body{padding-block:24px 44px}
  .content-section{margin-bottom:16px;padding:24px 20px}
  .content-section h2{margin-bottom:16px;padding-bottom:12px}
  .summary-section p:last-child{font-size:18px}
  blockquote{margin:18px 0;padding:16px 18px}
  th,td{padding:11px 12px}
  .score-section>h2{padding:22px 20px 17px}
  .coverage-note{padding:20px}
}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}*,*::before,*::after{animation:none!important;transition:none!important}}
"""

TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="color-scheme" content="light">
<title>{title} — FDE Casebook</title>
<style>{css}</style>
</head>
<body>
<nav class="topnav wrap" aria-label="站内导航">
  <a class="brand" href="{prefix}index.html">FDE Casebook</a>
  <div class="navlinks">
    <a href="{prefix}index.html">榜单首页</a>
    <a href="{prefix}leaderboard.html">完整榜单</a>
    <a href="{prefix}standards.html">入选标准</a>
    <a href="{prefix}guide.html">7 环节能力地图</a>
    <a href="{prefix}certifications.html">证书栏目</a>
    <a href="{prefix}job-market.html">招聘与市场</a>
    <a href="{prefix}changelog.html">更新日志</a>
  </div>
</nav>
<header class="page-hero">
  <div class="wrap">
    <p class="eyebrow">FDE Casebook · Field research</p>
    {case_meta}
    <h1>{title}</h1>
    {score_band}
  </div>
</header>
<main class="article-body wrap">
  <article>{body}</article>
</main>
<footer><div class="wrap"><p>FDE Casebook · 本页由仓库 Markdown 自动生成，GitHub 仅作源码仓库。维护：Bruce Cao（<a href="https://x.com/sycbruce">@sycbruce</a>）</p></div></footer>
</body>
</html>
"""


def fix_links(source: str) -> str:
    source = re.sub(r'href="([^"]+)\.md(["#])', r'href="\1.html\2', source)
    source = source.replace('LEADERBOARD.html', 'leaderboard.html')
    return source.replace('STANDARDS.html', 'standards.html')


def decorate_body(body: str) -> str:
    body = re.sub(r"^\s*<h1>.*?</h1>", "", body, count=1, flags=re.S)
    body = body.replace("<ul>", '<ul class="source-meta">', 1)
    parts = re.split(r"(<h2>.*?</h2>)", body)
    result = [f'<section class="content-section intro">{parts[0]}</section>']
    for heading, content in zip(parts[1::2], parts[2::2]):
        section_class = "content-section"
        if "一句话摘要" in heading:
            section_class += " summary-section"
        if "全流程 7 环节" in heading:
            section_class += " stage-section"
        if ">verdict</h2>" in heading:
            section_class += " verdict-section"
        if "原文摘录" in heading:
            section_class += " excerpt-section"
        if "评分与维度分析" in heading:
            section_class += " score-section"
        table_class = ' class="score-table"' if "score-section" in section_class else ""
        content = content.replace("<table>", f'<div class="table-scroll" tabindex="0"><table{table_class}>')
        content = content.replace("</table>", "</table></div>")
        content = content.replace(
            "<p><strong>7 环节覆盖分析</strong>",
            '<p class="coverage-note"><strong>7 环节覆盖分析</strong>',
        )
        result.append(f'<section class="{section_class}">{heading}{content}</section>')
    return "".join(result)


def case_header(text: str, origin_html: str) -> tuple[str, str]:
    meta_match = re.search(r"^- \*\*分类\*\*：(.+)$", text, re.M)
    categories = []
    if meta_match:
        categories = [part.strip() for part in meta_match.group(1).split("｜") if "榜单评分" not in part]
    case_meta = ""
    if categories:
        case_meta = '<ul class="case-meta">' + "".join(f"<li>{html.escape(item)}</li>" for item in categories) + "</ul>"
    score_match = re.search(r"榜单评分：(\d+) · ([SABC])", text)
    rank_match = re.search(r"(精选主榜第 \d+|海外榜第 \d+|国内榜第 \d+)", text)
    if not score_match:
        return case_meta, origin_html
    score, grade = score_match.groups()
    rank = rank_match.group(1) if rank_match else ""
    score_band = f'''<div class="score-band">
      <div class="total-score"><strong>{score}</strong><span>/ 100</span></div>
      <span class="grade grade-{grade.lower()}">{grade} 级</span>
      <span class="rank">{rank}</span>
      {origin_html}
    </div>'''
    return case_meta, score_band


def convert(md_path: Path, out_path: Path, prefix: str, origin_html: str = "") -> str:
    text = md_path.read_text(encoding="utf-8")
    match = re.search(r"^# (.+)$", text, re.M)
    title = match.group(1).strip() if match else md_path.stem
    body = decorate_body(fix_links(markdown.markdown(text, extensions=["tables", "sane_lists"])))
    case_meta, score_band = case_header(text, origin_html)
    page = TEMPLATE.format(
        title=html.escape(title),
        css=CSS,
        prefix=prefix,
        case_meta=case_meta,
        score_band=score_band,
        body=body,
    )
    page = "\n".join(line.rstrip() for line in page.splitlines()) + "\n"
    out_path.write_text(page, encoding="utf-8")
    return title


def main() -> int:
    jobs = []
    for md in sorted((ROOT / "cases").glob("*.md")):
        stem = md.stem
        origin = '<a class="origin" href="#original-excerpts">站内读原文摘录 ↓</a>' if stem in CASE_STEMS else ""
        jobs.append((md, ROOT / "cases" / f"{stem}.html", "../", origin))
    jobs.append((ROOT / "LEADERBOARD.md", ROOT / "leaderboard.html", "", ""))
    jobs.append((ROOT / "STANDARDS.md", ROOT / "standards.html", "", ""))
    jobs.append((ROOT / "guide" / "7-stage-map.md", ROOT / "guide.html", "", ""))
    jobs.append((ROOT / "CERTIFICATIONS.md", ROOT / "certifications.html", "", ""))
    jobs.append((ROOT / "JOBMARKET.md", ROOT / "job-market.html", "", ""))
    jobs.append((ROOT / "CHANGELOG.md", ROOT / "changelog.html", "", ""))
    for md, out, prefix, origin in jobs:
        title = convert(md, out, prefix, origin)
        print(f"built {out.relative_to(ROOT)}  <-  {md.relative_to(ROOT)}  ({title[:40]})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
