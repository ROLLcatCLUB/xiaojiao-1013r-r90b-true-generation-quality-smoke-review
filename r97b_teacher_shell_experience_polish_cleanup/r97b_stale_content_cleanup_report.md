# R97B Stale Content Cleanup Report

本轮目标是清理 R97A3 复制页中的旧审核残留，使教师默认阅读流只呈现干净的单课备课闭环。

## 已处理

- `mock_candidate_fixture` 所在的 R39 候选预览块：从教师默认 HTML 中移除。
- `R90B / R90B-P1 / R91A` 回填面板：从教师默认 HTML 中移除。
- `old candidate preview`、`修改前 / 修改后候选` 等旧审核内容：不再作为教师默认阅读流显示。
- 右侧历史 8 屏大屏草稿：运行时降级到开发者折叠区，P6 课堂联动优先。

## 清理记录

- `r39_mock_candidate_preview_panel`：matched=1，action=removed_from_teacher_default_html
- `r91a_static_backfill_panel`：matched=1，action=removed_from_teacher_default_html

## 保留边界

- 未修改真实 R91A/R87 源壳层。
- 未改 R21/R36 core。
- 未 formal apply，未写库/飞书/记忆。
- 未生成 PPTX/PDF/DOCX，未进入 R95。
