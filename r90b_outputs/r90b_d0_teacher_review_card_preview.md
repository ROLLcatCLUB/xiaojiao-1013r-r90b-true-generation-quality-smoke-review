# R90B-D0 Teacher Review Card Preview

This is a synthetic dry run. It does not use a provider, modify R21, write a database, write memory, or perform formal apply.

## Scope

- profile: `art_lesson_design_profile_v1@1.0.0`
- schema_key: `classroom_flow`
- step_type: `observation_inquiry`
- target_step_id: `observation_inquiry_01`
- strict_validation_result: `PASS`

## Candidate Cards

### 1. `lesson.classroom_flow.step.teacher_probe_question`

- line_contract_id: `R88-GEN/lesson.classroom_flow.step.teacher_probe_question`
- before: 观察问题较泛
- after: 你从浅到深能找到几个过渡台阶？哪个变化最明显？
- xiaojiao_suggestion: 把观察聚焦到渐变层次和变化方向。
- review_flags: teacher_review_required=True, preview_only=True, formal_apply_allowed=False, applied=False

### 2. `lesson.classroom_flow.step.student_observation`

- line_contract_id: `R88-GEN/lesson.classroom_flow.step.student_observation`
- before: 观察任务不够具体
- after: 学生圈出色块由浅到深的顺序，并说出变化方向。
- xiaojiao_suggestion: 把学生观察动作写成圈出、排序、说明。
- review_flags: teacher_review_required=True, preview_only=True, formal_apply_allowed=False, applied=False

### 3. `lesson.classroom_flow.step.visual_language_focus`

- line_contract_id: `R88-GEN/lesson.classroom_flow.step.visual_language_focus`
- before: 美术语言不显性
- after: 关注明度渐变：同一色相由浅到深逐步变化。
- xiaojiao_suggestion: 让美术语言落到明度、层次和过渡。
- review_flags: teacher_review_required=True, preview_only=True, formal_apply_allowed=False, applied=False

### 4. `lesson.classroom_flow.step.success_criteria`

- line_contract_id: `R88-GEN/lesson.classroom_flow.step.success_criteria`
- before: 评价标准偏空
- after: 作品至少出现3个连续渐变层次，过渡清楚。
- xiaojiao_suggestion: 把成功标准写成学生能自查的作品证据。
- review_flags: teacher_review_required=True, preview_only=True, formal_apply_allowed=False, applied=False

## Teacher Review Actions

Each candidate is preview-only and should enter the existing edit-card before/after/suggestion panel in R90B provider smoke.
