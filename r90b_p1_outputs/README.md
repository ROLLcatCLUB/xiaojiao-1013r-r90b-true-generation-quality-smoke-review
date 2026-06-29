# 1013R R90B-P1 Quality Sentinel v0 And Lineage Repair

R90B-P1 is not a new generation round. It does not call provider, does not add fields, does not modify R21, and does not perform formal apply.

## Result

```text
R90B-P1 result = PASS_WITH_NOTES
quality_sentinel_v0.result = BASIC_USABLE
blocking = false
candidate_count = 4
lineage_hash_coverage = 6/6
```

## What This Round Does

- Reuses existing R90B provider outputs.
- Converts the thin R90B quality smoke into a lightweight Quality Sentinel v0.
- Records generation lineage from profile to provider request, raw response, strict validation, normalized candidates, teacher review preview, and quality sentinel.
- Records SHA256 hashes for the six R90B input files.

## What This Round Does Not Do

- No provider call in this round.
- No new fields.
- No `art_lesson_design_profile_v1` change.
- No R21 modification.
- No formal apply.
- No database / Feishu / memory write.
- No shell/UI binding.
- No full lesson generation.
- No R90C or R91 execution.

## Override Of Old R90B Next Field

R90B `strict_provider_raw_validation_result.json` may contain:

```text
next_recommended_round=1013R_R91_MULTI_STEP_CLASSROOM_FLOW_SMOKE
```

This round intentionally overrides that old recommendation. The latest handoff requires R90B-P1 first because R90B quality smoke is only a thin 4-field check and generation lineage was not yet summarized.

## Claim Limit

`BASIC_USABLE` means only the `observation_inquiry` slice has basic usable evidence. It does not mean full lesson quality passed, multi-step classroom quality passed, or public-lesson quality passed.

## Main Files

- `quality_sentinel_v0_result.json`
- `quality_sentinel_v0_notes.md`
- `generation_lineage_1013R_R90B.json`
- `validate_1013R_R90B_P1_quality_sentinel_v0_and_lineage_result.json`
- `REVIEW_PACKAGE_MANIFEST.json`
- `REVIEW_PACKAGE_MANIFEST.md`
- `GPT_REVIEW_PROMPT_1013R_R90B_P1.md`

## Next

Stop after R90B-P1 and wait for GPT review. Do not automatically enter R90C or R91.
