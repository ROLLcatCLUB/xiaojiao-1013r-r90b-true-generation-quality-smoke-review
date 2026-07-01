# GPT Review Prompt: 1013R_R97A3_SHELL_CONTEXT_AND_ARTIFACT_RAIL_ALIGNMENT

Please review this GitHub package:

Repo: https://github.com/ROLLcatCLUB/xiaojiao-1013r-r90b-true-generation-quality-smoke-review
Directory: `r97a3_shell_context_artifact_rail_alignment/`

Core question:

R97A2 proved that R93-P6 is bound only into the original R91A prep-notebook `六、教学过程` slot. R97A3 should now prove static context alignment between that P6 teaching process and the shell-side artifacts: right courseware rail, worksheet/rubric entries, bottom Xiaojiao context, and teacher action buttons.

Review focus:

1. Does P6 remain only in `六、教学过程`, without replacing the full shell or `#renderLayer`?
2. Does the right rail show `P6 课堂联动` and map five episodes to S01-S10?
3. Do worksheet tasks, teacher observation dimensions, and student self-check items map back to the same five episodes?
4. Does bottom Xiaojiao context have episode title, teacher talk, misconception/scaffold/evidence, and next-action hint?
5. Are teacher action buttons preview-only/no-op, with no formal apply or runtime calls?
6. Is this still a static copy-page context preview, not production UI runtime integration?

Allowed result labels:

- `PASS_AS_CONTEXT_ALIGNMENT_PREVIEW`
- `PASS_WITH_NOTES`
- `NEEDS_PATCH`
- `FAIL_CONTEXT_ALIGNMENT`

Boundaries: no R95, no formal PPT/PDF/DOCX export, no database/Feishu/memory write, no R21/R36 core modification, no real UI runtime binding.
