# GPT Review Prompt: 1013R_R97A2_PREP_NOTEBOOK_TEACHING_PROCESS_SLOT_BINDING_REPAIR

Please review this GitHub package:

Repo: https://github.com/ROLLcatCLUB/xiaojiao-1013r-r90b-true-generation-quality-smoke-review
Directory: `r97a2_prep_notebook_teaching_process_slot_binding_repair/`

Core review question:

R93-P6 teacher navigation must be bound only into the original R91A prep-notebook `六、教学过程` slot. It must not replace the whole prep-room shell, the whole render layer, or the whole single-lesson notebook.

Review focus:

1. Does the copied R91A shell preserve topbar, left notebook tree, right courseware rail, and bottom Xiaojiao composer?
2. Is R93-P6 inserted only into `六、教学过程` rather than replacing `#renderLayer`?
3. Are `一、本课依据`, `二、学情分析`, `三、教学目标`, `四、教学重难点`, `五、教学准备`, `七、学习单与评价`, and `课堂后记` preserved?
4. Does `r97a2_visual_slot_smoke.md` plus screenshot/DOM dump prove the slot binding?
5. Is the previous R97A whole-shell attempt correctly demoted?
6. Is the copied-shell R21 package/normalizer patch justified by the final overwrite layer?

Do not call this formal apply. Recommended result labels:

- `PASS_AS_SLOT_BINDING_PREVIEW`
- `PASS_WITH_NOTES`
- `NEEDS_PATCH`
- `FAIL_AS_SLOT_BINDING`

Boundaries: no R95, no formal PPT/PDF/DOCX export, no database write, no real UI runtime binding.
