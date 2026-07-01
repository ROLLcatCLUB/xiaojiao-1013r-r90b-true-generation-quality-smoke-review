# 1013R_R97A2_PREP_NOTEBOOK_TEACHING_PROCESS_SLOT_BINDING_REPAIR

本轮修复上一版壳层接入粒度错误：P6 教师导航内容只接入原备课本 `六、教学过程` 槽位。

## 输出

- `R91A_prep_notebook_teaching_process_slot_binding_from_R93_P6.html`
- `r97a2_slot_binding_viewmodel.json`
- `r97a2_original_shell_slot_audit.md`
- `r97a2_previous_r97a_demote_decision.md`
- `validate_1013R_R97A2_prep_notebook_teaching_process_slot_binding_repair_result.json`
- `r97a2_visual_slot_smoke.md`
- `R91A_slot_binding_dom_dump.html`
- `R91A_slot_binding_from_R93_P6_screenshot.png`
- `R91A_slot_binding_teaching_process_section_screenshot.png`

## 边界

- 不改原 R91A/R87 壳层源文件。
- 不替换整页 `#renderLayer`。
- 不覆盖单课正文其他章节。
- 复制页内适配 R21 最终覆盖层；不修改原 R21/R36 合同或源文件。
- 不 formal apply，不写数据库/飞书/记忆，不改 R21/R36。

HTML SHA256: `627887bc63c7cf78de42a8918b91cc6258383a8309cc510db31843b1f0f769bc`
