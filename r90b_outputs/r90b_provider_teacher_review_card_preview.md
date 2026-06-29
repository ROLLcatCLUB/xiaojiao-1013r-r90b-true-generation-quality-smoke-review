# R90B Provider Teacher Review Card Preview

This is the first real provider smoke for the frozen art profile. It used MiniMax-M3 through the existing openai-compatible provider channel. It did not modify R21, write a database, write memory, or perform formal apply.

## Scope

- profile: `art_lesson_design_profile_v1@1.0.0`
- schema_key: `classroom_flow`
- step_type: `observation_inquiry`
- target_step_id: `observation_inquiry_01`
- strict_provider_raw_validation_result: `PASS`
- quality_smoke_result: `BASIC_USABLE`

## Candidate Cards

### 1. `lesson.classroom_flow.step.teacher_probe_question`

- line_contract_id: `R88-GEN/lesson.classroom_flow.step.teacher_probe_question`
- before: 教师泛问颜色有什么变化。
- after: 请指出这片色块里，色彩是从哪里浅、往哪里深，又是怎样从这一色过渡到另一色的？
- xiaojiao_suggestion: 主问过渡方向与明度变化。
- review_flags: teacher_review_required=True, preview_only=True, formal_apply_allowed=False, applied=False

### 2. `lesson.classroom_flow.step.student_observation`

- line_contract_id: `R88-GEN/lesson.classroom_flow.step.student_observation`
- before: 学生大致说出颜色好看。
- after: 用笔圈出端色与中间过渡带，并口述色相与明度由浅到深的变化方向。
- xiaojiao_suggestion: 要求圈出过渡带并说方向。
- review_flags: teacher_review_required=True, preview_only=True, formal_apply_allowed=False, applied=False

### 3. `lesson.classroom_flow.step.visual_language_focus`

- line_contract_id: `R88-GEN/lesson.classroom_flow.step.visual_language_focus`
- before: 只说颜色丰富。
- after: 聚焦明度阶梯与色相过渡的层次关系，识别端色、中间色与过渡方向。
- xiaojiao_suggestion: 锁定明度与色相两轴的层次。
- review_flags: teacher_review_required=True, preview_only=True, formal_apply_allowed=False, applied=False

### 4. `lesson.classroom_flow.step.success_criteria`

- line_contract_id: `R88-GEN/lesson.classroom_flow.step.success_criteria`
- before: 作品颜色多即可。
- after: 能圈出至少三处层次清晰的过渡带，并说明明度或色相的渐变方向。
- xiaojiao_suggestion: 以过渡带数量与方向为自检点。
- review_flags: teacher_review_required=True, preview_only=True, formal_apply_allowed=False, applied=False

## Teacher Review Actions

Each candidate is preview-only and should enter the existing edit-card before/after/suggestion panel in the next visible runtime/card binding stage.
