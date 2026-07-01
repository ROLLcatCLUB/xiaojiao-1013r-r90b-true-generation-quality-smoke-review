# 1013R_R97B_TEACHER_SHELL_EXPERIENCE_POLISH_AND_STALE_CONTENT_CLEANUP

R97A3 已证明 P6 与右侧大屏、学习单/评价、小教上下文之间的静态关系。本轮只做教师壳层体验清理：把旧 mock/R90B/R91A 审核残留移出教师默认阅读流，并把右栏优先级调整为 P6 课堂联动。

## 输出

- `r97b_clean_shell_context_preview.html`
- `r97b_clean_shell_viewmodel.json`
- `r97b_stale_content_cleanup_report.md`
- `r97b_right_rail_priority_policy.md`
- `r97b_xiaojiao_episode_context_smoke.md`
- `r97b_teacher_action_preview_state_smoke.md`
- `validate_1013R_R97B_teacher_shell_experience_polish_result.json`

## 边界

- 静态复制页 preview，不接真实 runtime。
- 未修改真实 R91A/R87 壳层源文件。
- 不改 R21/R36 core。
- 不 formal apply，不写数据库/飞书/记忆。
- 不生成 PPTX/PDF/DOCX，不进入 R95。

HTML SHA256: `e4b90344e3c292f204574dd5e694a3c097e924904cd467a4532507f519b7db8e`
