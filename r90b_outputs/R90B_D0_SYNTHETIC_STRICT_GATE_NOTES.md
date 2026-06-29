# R90B-D0 Synthetic Candidate Strict Gate Notes

R90B-D0 is a dry run inside `1013R_R90B_TRUE_GENERATION_QUALITY_SMOKE_V1`.

It proves the strict gate can accept profile-correct candidate envelopes and reject known bad envelopes before a real provider is connected.

## Active Profile

- profile_id: `art_lesson_design_profile_v1`
- profile_version: `1.0.0`
- candidate_contract_version: `candidate_required_keys_v1`

## Boundaries

- no R21 modification
- no provider/runtime connection
- no database/Feishu/memory write
- no formal apply
- no new fields
- no full lesson generation

## Result

- strict_valid_candidates: `4`
- expected_rejected_negative_candidates: `3`
- result: `PASS`

## Next

If GPT accepts D0, run R90B provider smoke with the same four target fields and the same strict validator.
