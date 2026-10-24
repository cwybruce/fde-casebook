# FDE Casebook 页面高端化改版交付报告

日期：2026-10-24

范围：首页、4 个案例页、完整榜单、入选标准、7 环节能力地图，共 8 个页面。

## 1. 设计取舍

采用“暖纸正文 + 墨黑封面”的浅色体系。暖纸面降低长文阅读疲劳，墨黑只用于首页封面与生成页标题区，形成研究报告的封面秩序；铜色用于行动与排名，深绿只用于评分数据。S/A/B 固定为金/铜/灰蓝，同时保留字母、分数与等级文字，不依赖颜色单独传达信息。

标题使用系统衬线栈，正文使用系统无衬线栈；不使用外部字体、CDN、框架或图表库。内容卡片以细边框和留白分层，圆角不超过 9px，阴影仅作轻微层级提示。桌面内容宽度首页 960px、阅读页 880px；手机以信息顺序和可横向滚动的表格保证可读性。

动效只保留卡片轻微抬升、平滑锚点滚动与首页分数条一次性生长，并完整支持 `prefers-reduced-motion`。

## 2. 改动文件清单

### 手工源文件

- `scripts/build_site.py`：统一 design tokens、全站导航、封面模板、案例分类/分数/等级/榜位提取、内容区块、表格滚动容器、移动端样式与降级动效。
- `index.html`：重排首屏封面、三项真实统计、双榜入口、案例榜卡片、人物行、页脚与双端样式。

### 由构建脚本重新生成

- `cases/FDE-001-liangzhu-fde-framework.html`
- `cases/FDE-002-openai-deployment-gap.html`
- `cases/FDE-003-miles-mazy-geely-training.html`
- `cases/FDE-004-china-entrepreneur-fde-truth.html`
- `leaderboard.html`
- `standards.html`
- `guide.html`

### 交付材料

- `docs/reports/redesign-v1.md`
- `docs/reports/screenshots/`：本地双端逐页截图、国内榜定位截图、案例摘录/评分区截图；线上复验截图使用 `online-` 前缀。

未修改：`cases/*.md`、`LEADERBOARD.md`、`STANDARDS.md`、`guide/7-stage-map.md`。

## 3. 最终 Design Tokens

### 色彩

| Token | 值 | 用途 |
|---|---|---|
| `--paper` | `#f7f4ee` | 全站暖纸背景 |
| `--surface` | `#fffdfa` | 正文与卡片表面 |
| `--surface-muted` | `#f0ebe2` | 表头、引用、标签底色 |
| `--ink` | `#202522` | 主文字 |
| `--sub` | `#66675f` | 次要文字 |
| `--line` | `#ded8cc` | 常规边框 |
| `--line-strong` | `#c7bfb1` | 强调分隔线 |
| `--accent` | `#954b25` | 铜色行动、链接、排名 |
| `--accent-bright` | `#dda77d` | 墨底上的铜色行动与标记 |
| `--green` | `#2f6656` | 五维评分条与分数 |
| `--night` | `#19211f` | 首页/案例页封面 |
| `--night-sub` | `#b9c1ba` | 墨底次要文字 |
| `--grade-s` | `#98711c` | S 级（金） |
| `--grade-a` | `#954b25` | A 级（铜） |
| `--grade-b` | `#526b7b` | B 级（灰蓝） |

### 字体与字阶

| Token / 层级 | 桌面值 | 手机值 | 字体/特征 |
|---|---:|---:|---|
| `--font-serif` | — | — | `Georgia, Songti SC, Noto Serif CJK SC, SimSun, serif` |
| `--font-sans` | — | — | `Noto Sans CJK SC, PingFang SC, Microsoft YaHei, system-ui, sans-serif` |
| 首页展示标题 `--text-display` | 64px | 46px | 衬线、紧字距 |
| 生成页 H1 `--text-h1` | 42px（流式上限） | 32px | 衬线、紧字距 |
| H2 `--text-h2` | 26px；榜单区标题 32px | 23–27px | 衬线、细分隔线 |
| H3 / 案例标题 `--text-h3` | 19px；首页案例 22px | 19px | 清晰层级 |
| 正文 `--text-base` | 16.5px / 1.85 | 16px / 1.8 | 长文阅读 |
| 小字 `--text-sm` | 14px | 14px | 辅助信息 |
| 微标签 `--text-xs` | 12px | 11–12px | 分类与英文标记 |
| 总分 | 46–52px | 36–46px | 衬线、`tabular-nums` |

### 网格、间距与形状

| Token | 值 | 用途 |
|---|---|---|
| `--measure` | 首页 960px；阅读页 880px | 内容最大宽度 |
| `--space-1` … `--space-8` | 4 / 8 / 12 / 16 / 24 / 32 / 48 / 64px | 统一间距阶梯 |
| `--radius-sm` | 5px | 按钮、标签、徽章 |
| `--radius` | 9px | 卡片与内容区块 |
| `--shadow` | `0 8px 24px rgba(34,39,32,.045)` | 轻层级阴影 |
| 页面边距 | 桌面 24px；手机 16px | 双端安全留白 |
| 点击区 | 导航最小 40px；主按钮 44px | 移动可访问性 |

## 4. 内容零改动声明

所有案例分数、五维分、评价、原文摘录、verdict、人物评级和 Markdown 内容源均未修改。没有文案微调。

自查方式：

1. `git diff` 确认 `cases/*.md`、`LEADERBOARD.md`、`STANDARDS.md`、`guide/7-stage-map.md` 无改动。
2. 对改版前 HEAD 与生成后 7 个页面进行可见文本逐项比对，原有文本全部保留。
3. 连续两次执行 `python3 scripts/build_site.py`，7 个生成页 SHA-256 完全一致，确认重建不回退。

为满足首屏统计与导航要求，仅新增界面辅助文字：“已收录案例 / S 级案例 / 一手人物”（按现有数据为 04 / 01 / 05）、“浏览国内榜 / 浏览海外榜”及英文栏目标记；案例分类、分数、等级和榜位均由原 Markdown 派生展示，不改结论。

## 5. 截图

截图宽度分别为 1280px 与 390px，PNG、1× 像素比；本地浏览器高度分别为 1000px 与 844px。

### 要求的首页、国内榜与案例页

| 场景 | 桌面 1280 | 手机 390 |
|---|---|---|
| 首页首屏 | `docs/reports/screenshots/index-1280.png` | `docs/reports/screenshots/index-390.png` |
| 国内榜 | `docs/reports/screenshots/china-1280.png` | `docs/reports/screenshots/china-390.png` |
| FDE-002 案例页 | `docs/reports/screenshots/case-FDE-002-1280.png` | `docs/reports/screenshots/case-FDE-002-390.png` |

### 其他本地逐页自查

- `leaderboard-1280.png` / `leaderboard-390.png`
- `standards-1280.png` / `standards-390.png`
- `guide-1280.png` / `guide-390.png`
- `case-FDE-001-1280.png` / `case-FDE-001-390.png`
- `case-FDE-003-1280.png` / `case-FDE-003-390.png`
- `case-FDE-004-1280.png` / `case-FDE-004-390.png`
- `case-FDE-002-excerpts-1280.png` / `case-FDE-002-excerpts-390.png`
- `case-FDE-002-score-1280.png` / `case-FDE-002-score-390.png`

以上文件均位于 `docs/reports/screenshots/`。

### 线上发布后复验截图

| 场景 | 桌面 1280 | 手机 390 |
|---|---|---|
| 首页首屏 | `docs/reports/screenshots/online-index-1280.png` | `docs/reports/screenshots/online-index-390.png` |
| 国内榜 | `docs/reports/screenshots/online-china-1280.png` | `docs/reports/screenshots/online-china-390.png` |
| FDE-002 案例页 | `docs/reports/screenshots/online-case-FDE-002-1280.png` | `docs/reports/screenshots/online-case-FDE-002-390.png` |

## 6. 验证结果

### 本地

- 8 个页面在桌面 1280 与手机 390 两档均完成浏览器截图检查。
- 8 个页面本地响应均为 200，无 JavaScript 页面错误、无页面级横向溢出。
- 15 个唯一站内链接目标及锚点全部可用；4 个案例的 `#original-excerpts` 保留。
- FDE-002 顶部主按钮已实际点击验证：URL 哈希更新且目标进入视口。
- 表格只在自身容器内横向滚动，不撑破移动页面。
- 无外部 CDN、构建框架、图表库或新增站外阅读入口。

### 线上 GitHub Pages

发布基址：`https://cwybruce.github.io/fde-casebook/`

| 页面 | HTTP |
|---|---:|
| `/` | 200 |
| `/leaderboard.html` | 200 |
| `/standards.html` | 200 |
| `/guide.html` | 200 |
| `/cases/FDE-001-liangzhu-fde-framework.html` | 200 |
| `/cases/FDE-002-openai-deployment-gap.html` | 200 |
| `/cases/FDE-003-miles-mazy-geely-training.html` | 200 |
| `/cases/FDE-004-china-entrepreneur-fde-truth.html` | 200 |

线上版本另以 1280/390 浏览器截图复核，并对 8 页执行新版封面标记检查，避免 CDN/浏览器缓存造成“200 但仍是旧版”的误判。

## 7. DESIGN.md 第六节验收清单

- [x] 全站（index + 4 案例页 + leaderboard/standards/guide）视觉体系一致，token 落地。
- [x] `python3 scripts/build_site.py` 重跑后页面不回退；连续构建字节一致。
- [x] 全部站内链接与锚点（`#original-excerpts`）可用；无跳仓库的阅读入口新增。
- [x] 所有分数、评价、摘录文字与改版前逐项一致，已完成 diff 与可见文本自查。
- [x] 桌面 1280 与手机 390 两档截图齐全：首页首屏、国内榜、FDE-002 案例页，并附其他页面截图。
- [x] 线上 Pages 发布后逐页 200，附线上截图复验。
- [x] 交付报告包含改动文件、token 表、截图路径、内容声明、设计理由与遗留问题。

## 8. 遗留问题与建议

- FDE-001 原帖直链仍为内容源已有的“待补”状态；本次严格保留，未补写或改动。
- 手机端宽表需要局部横向滚动，这是为避免压缩评价文字而保留的阅读方式；容器可键盘聚焦，页面本身不横向溢出。
- 本次未实现可选加分项（深色模式、按环节筛选、OG 分享图），以优先保证核心页面、内容零改动和双端阅读质量。
