# TASK-FOR-CODEX｜FDE Casebook 页面高端化改版

## 任务
按仓库 `DESIGN.md` 把站点改版到"高端大气"的专业榜单气质，并发布上线。需求细节、设计系统、逐页要求、验收标准全在 DESIGN.md，本文件只定执行方式。

## 先读
1. `DESIGN.md`（需求本体，先完整读一遍再动手）
2. `scripts/build_site.py`（生成管线：案例页/leaderboard/standards/guide 都由它从 md 生成）
3. `index.html`（手工维护的榜单首页，可直接改）
4. `cases/*.md`、`LEADERBOARD.md`、`STANDARDS.md`（内容源，只读不改）

## 执行边界
- **只改呈现，不改内容**：分数、五维分、评价、摘录、verdict、人物评级一个字不动；文案微调必须在报告里逐条列明。
- 改样式优先改 `scripts/build_site.py` 的模板/CSS 与 `index.html`；**不要直接手改生成的 cases/*.html、leaderboard.html、standards.html、guide.html 当交付**——改完必须重跑 `python3 scripts/build_site.py` 并提交生成结果。
- 不引入构建框架与外部 CDN 依赖；CSS/JS 内联或单文件；GitHub Pages 静态托管不变。
- 站内阅读闭环不许破：不新增跳出站外的阅读入口；`#original-excerpts` 锚点保留可用。
- 每完成一页先本地截图自查（桌面 1280 / 手机 390 两档），再继续下一页。

## 交付物
1. 改版后的全部页面源码 + 重建后的生成页，一次 commit 推送到 main（commit 信息注明 redesign）。
2. GitHub Pages 发布后逐页复验（200 + 线上截图）。
3. 交付报告 `docs/reports/redesign-v1.md`：改动文件清单、最终 design token 表、桌面/手机截图路径、内容零改动声明（或文案微调清单）、遗留问题与建议。

## 验收（对照 DESIGN.md 第六节逐项打勾，写进报告）
- [ ] 全站视觉体系一致
- [ ] 重跑 build_site.py 不回退
- [ ] 站内链接/锚点全可用
- [ ] 数据与文案与改版前一致
- [ ] 双档截图齐全
- [ ] 线上逐页 200 已复验

## 卡住时
设计取舍拿不准，先按 DESIGN.md 的"参照气质"自行判断并在报告里说明理由，不要停工等回复；只有涉及改内容/改数据/破硬约束时才停下来问。
