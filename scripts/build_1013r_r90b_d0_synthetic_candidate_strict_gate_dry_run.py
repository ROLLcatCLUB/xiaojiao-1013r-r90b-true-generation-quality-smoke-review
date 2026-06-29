from __future__ import annotations

import json
from copy import deepcopy
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
R90A = BASE / "1013R_R90A_TRUE_GENERATION_CONTRACT_AND_PROFILE_PREFLIGHT"
OUT = BASE / "1013R_R90B_TRUE_GENERATION_QUALITY_SMOKE_V1"

STRICT_POLICY_PATH = R90A / "r90a_true_generation_strict_validator_policy_1013R_R90A.json"
R82_SCHEMA_PATH = R90A / "upstream_refs" / "lesson_generation_response_schema_1013R_R82.json"
CANDIDATE_KEYS_PATH = R90A / "upstream_refs" / "r89_candidate_required_keys_single_source_1013R_R89.json"
PROFILE_MANIFEST_PATH = R90A / "r90a_art_lesson_design_profile_manifest_1013R_R90A.json"

TARGETS = [
    {
        "field_patch_id": "r90b_d0_candidate_001",
        "target_field_key": "lesson.classroom_flow.step.teacher_probe_question",
        "before_summary": "观察问题较泛",
        "after_candidate": "你从浅到深能找到几个过渡台阶？哪个变化最明显？",
        "xiaojiao_suggestion": "把观察聚焦到渐变层次和变化方向。",
        "impact_scope": ["classroom_flow", "observation", "visual_language"],
        "reasoning_basis": "观察探究先用追问把学生注意力拉到渐变证据。",
    },
    {
        "field_patch_id": "r90b_d0_candidate_002",
        "target_field_key": "lesson.classroom_flow.step.student_observation",
        "before_summary": "观察任务不够具体",
        "after_candidate": "学生圈出色块由浅到深的顺序，并说出变化方向。",
        "xiaojiao_suggestion": "把学生观察动作写成圈出、排序、说明。",
        "impact_scope": ["classroom_flow", "student_action", "evidence_note"],
        "reasoning_basis": "学生需要有可见动作，才能留下观察证据。",
    },
    {
        "field_patch_id": "r90b_d0_candidate_003",
        "target_field_key": "lesson.classroom_flow.step.visual_language_focus",
        "before_summary": "美术语言不显性",
        "after_candidate": "关注明度渐变：同一色相由浅到深逐步变化。",
        "xiaojiao_suggestion": "让美术语言落到明度、层次和过渡。",
        "impact_scope": ["classroom_flow", "visual_language", "teacher_prompt"],
        "reasoning_basis": "美术课的生成候选必须把观察转成可说清的视觉语言。",
    },
    {
        "field_patch_id": "r90b_d0_candidate_004",
        "target_field_key": "lesson.classroom_flow.step.success_criteria",
        "before_summary": "评价标准偏空",
        "after_candidate": "作品至少出现3个连续渐变层次，过渡清楚。",
        "xiaojiao_suggestion": "把成功标准写成学生能自查的作品证据。",
        "impact_scope": ["classroom_flow", "assessment", "work_evidence"],
        "reasoning_basis": "成功标准要能回指学生作品中的渐变层次。",
    },
]


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def fail(reason: str, details: dict[str, Any] | None = None) -> dict[str, Any]:
    return {"result": "FAIL", "reason": reason, "details": details or {}}


def pass_result(details: dict[str, Any] | None = None) -> dict[str, Any]:
    return {"result": "PASS", "details": details or {}}


def candidate_for(target: dict[str, Any], slot_map: dict[str, str]) -> dict[str, Any]:
    target_field_key = target["target_field_key"]
    return {
        "field_patch_id": target["field_patch_id"],
        "schema_key": "classroom_flow",
        "canonical_field_key": "classroom_flow",
        "target_field_key": target_field_key,
        "target_section": "teaching_process",
        "target_step_id": "observation_inquiry_01",
        "target_line_contract_id": slot_map[target_field_key],
        "target_destination": "existing_edit_card_before_after_suggestion_panel",
        "before_summary": target["before_summary"],
        "after_candidate": target["after_candidate"],
        "xiaojiao_suggestion": target["xiaojiao_suggestion"],
        "impact_scope": target["impact_scope"],
        "source_refs": [
            "active_profile:art_lesson_design_profile_v1@1.0.0",
            "lesson_case:三年级美术《色彩的渐变》",
            "step_type:observation_inquiry",
        ],
        "teacher_review_required": True,
        "preview_only": True,
        "formal_apply_allowed": False,
        "applied": False,
        "patch_type": "profile_targeted_field_candidate",
        "reasoning_basis": target["reasoning_basis"],
    }


def build_response(candidates: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "response_stage": "1013R_R90B_D0_SYNTHETIC_CANDIDATE_STRICT_GATE_DRY_RUN",
        "request_id": "r90b_d0_synthetic_001",
        "lesson_design_mode": "profile_targeted_smoke",
        "intent_summary": "用虚拟 provider 响应验证 R90B strict gate 能放行正确候选并拒绝越界候选。",
        "lesson_logic_brief": {
            "inherited_unit_context_summary": "三年级色彩单元从观察自然与作品中的色彩变化进入渐变表达。",
            "core_learning_problem": "学生能感觉颜色有变化，但未必能说清渐变层次和过渡方向。",
            "student_starting_point": "学生能辨认颜色深浅差异，但需要把直观感受转成观察证据。",
            "target_shift": "从看见颜色变化，转向用明度、层次、过渡描述并表达渐变。",
            "lesson_focus_question": "颜色怎样一步步从浅到深变化？",
            "visual_language_use": "明度渐变、层次、过渡、同一色相深浅变化。",
            "teaching_route": [
                "观察色块变化",
                "圈出渐变层次",
                "说出过渡方向",
                "用作品证据自查",
            ],
            "evidence_plan": [
                "学生圈出的渐变顺序",
                "学生口头描述的变化方向",
                "作品中的连续渐变层次",
            ],
            "risk_points": [
                "学生只说好看不好看",
                "作品颜色跳变明显但缺少过渡",
            ],
            "source_basis": ["active_profile", "R90B_revised_plan", "synthetic_fixture"],
            "material_gaps": [],
        },
        "target_resolution": [
            {
                "schema_key": "classroom_flow",
                "target_section": "teaching_process",
                "target_step_id": "observation_inquiry_01",
                "target_field": "observation_inquiry_active_step_fields",
                "reason": "R90B-D0 只验证 observation_inquiry 环节的四个 active profile step fields。",
                "source_refs": ["active_profile:art_lesson_design_profile_v1@1.0.0"],
            }
        ],
        "step_reasoning_updates": [],
        "field_patch_candidates": candidates,
        "quality_gate_update": {
            "level": "basic_usable",
            "passed_items": [
                "四个候选分别覆盖教师追问、学生观察、美术语言焦点、成功标准",
                "候选均定位到 active profile 的 R88 step field",
            ],
            "missing_items": ["真实 provider 内容质量尚未验证"],
            "risk_items": ["D0 是 synthetic dry run，不能替代 R90B provider smoke"],
            "next_best_action": "D0 通过后再进行真实 provider 窄切生成。",
        },
        "material_requests": [],
        "teacher_questions": [],
        "ui_binding_hint": {
            "should_enter_edit_mode": True,
            "edit_target": "teaching_process/observation_inquiry_01",
            "candidate_display_position": "existing_edit_card_before_after_suggestion_panel",
            "right_tray_updates": [],
            "view_mode_summary": "D0 只生成教师审核卡预览，不写 R21，不 formal apply。",
        },
        "boundary_flags": {
            "teacher_review_required": True,
            "formal_apply_performed": False,
            "database_written": False,
            "memory_written": False,
            "feishu_written": False,
            "formal_export_created": False,
            "official_archive_created": False,
        },
    }


def validate_candidate(candidate: dict[str, Any], required: list[str], policy: dict[str, Any]) -> dict[str, Any]:
    missing = [key for key in required if key not in candidate]
    extra = [key for key in candidate if key not in required]
    if missing:
        return fail("candidate_missing_required_keys", {"missing": missing})
    if extra:
        return fail("candidate_has_extra_keys", {"extra": extra})
    if candidate["schema_key"] != "classroom_flow":
        return fail("schema_key_not_classroom_flow", {"schema_key": candidate["schema_key"]})
    if candidate["canonical_field_key"] != "classroom_flow":
        return fail("canonical_field_key_not_classroom_flow", {"canonical_field_key": candidate["canonical_field_key"]})

    classroom_policy = policy["target_field_key_policy"]["classroom_flow"]
    allowed = set(classroom_policy["target_field_key_allowed_values"])
    target_field_key = candidate["target_field_key"]
    if target_field_key not in allowed:
        return fail("target_field_key_not_active_profile_step_field", {"target_field_key": target_field_key})

    expected_slot = policy["step_target_field_to_generation_slot"].get(target_field_key)
    if candidate["target_line_contract_id"] != expected_slot:
        return fail(
            "target_line_contract_id_mismatch",
            {"target_field_key": target_field_key, "expected": expected_slot, "actual": candidate["target_line_contract_id"]},
        )

    if not candidate["target_step_id"]:
        return fail("target_step_id_required_for_classroom_flow")

    boundaries = policy["boundary_flags_required"]
    for key, expected in boundaries.items():
        if candidate.get(key) is not expected:
            return fail("candidate_boundary_flag_mismatch", {"key": key, "expected": expected, "actual": candidate.get(key)})

    if len(candidate["after_candidate"]) > 60:
        return fail("after_candidate_too_long", {"length": len(candidate["after_candidate"])})
    if len(candidate["xiaojiao_suggestion"]) > 40:
        return fail("xiaojiao_suggestion_too_long", {"length": len(candidate["xiaojiao_suggestion"])})
    if len(candidate["before_summary"]) > 30:
        return fail("before_summary_too_long", {"length": len(candidate["before_summary"])})
    if len(candidate["impact_scope"]) > 5:
        return fail("impact_scope_too_long", {"length": len(candidate["impact_scope"])})
    if len(candidate["source_refs"]) > 4:
        return fail("source_refs_too_long", {"length": len(candidate["source_refs"])})

    return pass_result({"target_field_key": target_field_key, "target_line_contract_id": expected_slot})


def validate_response(payload: dict[str, Any], schema: dict[str, Any], required: list[str], policy: dict[str, Any]) -> dict[str, Any]:
    top_missing = [key for key in schema["top_level_required_keys"] if key not in payload]
    if top_missing:
        return fail("top_level_required_keys_missing", {"missing": top_missing})

    if payload["teacher_questions"] != []:
        return fail("teacher_questions_must_be_empty")
    if payload["material_requests"] not in ([], None):
        if not isinstance(payload["material_requests"], list) or len(payload["material_requests"]) > 1:
            return fail("material_requests_out_of_d0_scope")

    boundary_required = schema["boundary_flags_required"]
    for key, expected in boundary_required.items():
        if payload["boundary_flags"].get(key) is not expected:
            return fail("top_level_boundary_flag_mismatch", {"key": key, "expected": expected, "actual": payload["boundary_flags"].get(key)})

    candidates = payload.get("field_patch_candidates")
    if not isinstance(candidates, list) or len(candidates) != 4:
        return fail("candidate_count_must_equal_4", {"actual": len(candidates) if isinstance(candidates, list) else None})

    candidate_results = [validate_candidate(candidate, required, policy) for candidate in candidates]
    failed = [result for result in candidate_results if result["result"] != "PASS"]
    if failed:
        return fail("candidate_strict_validation_failed", {"candidate_results": candidate_results})

    return pass_result({"candidate_count": len(candidates), "candidate_results": candidate_results})


def build_negative_fixtures(valid: list[dict[str, Any]]) -> list[dict[str, Any]]:
    wrong_target = deepcopy(valid[0])
    wrong_target["field_patch_id"] = "r90b_d0_negative_target_field_key_equals_schema_key"
    wrong_target["target_field_key"] = "classroom_flow"

    wrong_line_contract = deepcopy(valid[1])
    wrong_line_contract["field_patch_id"] = "r90b_d0_negative_line_contract_id_mismatch"
    wrong_line_contract["target_line_contract_id"] = "R88-GEN/lesson.classroom_flow.step.wrong"

    wrong_boundary = deepcopy(valid[2])
    wrong_boundary["field_patch_id"] = "r90b_d0_negative_formal_apply_allowed_true"
    wrong_boundary["formal_apply_allowed"] = True

    return [wrong_target, wrong_line_contract, wrong_boundary]


def render_preview(candidates: list[dict[str, Any]], validation: dict[str, Any]) -> str:
    lines = [
        "# R90B-D0 Teacher Review Card Preview",
        "",
        "This is a synthetic dry run. It does not use a provider, modify R21, write a database, write memory, or perform formal apply.",
        "",
        "## Scope",
        "",
        "- profile: `art_lesson_design_profile_v1@1.0.0`",
        "- schema_key: `classroom_flow`",
        "- step_type: `observation_inquiry`",
        "- target_step_id: `observation_inquiry_01`",
        "- strict_validation_result: `" + validation["result"] + "`",
        "",
        "## Candidate Cards",
        "",
    ]
    for idx, candidate in enumerate(candidates, 1):
        lines.extend(
            [
                f"### {idx}. `{candidate['target_field_key']}`",
                "",
                f"- line_contract_id: `{candidate['target_line_contract_id']}`",
                f"- before: {candidate['before_summary']}",
                f"- after: {candidate['after_candidate']}",
                f"- xiaojiao_suggestion: {candidate['xiaojiao_suggestion']}",
                f"- review_flags: teacher_review_required={candidate['teacher_review_required']}, preview_only={candidate['preview_only']}, formal_apply_allowed={candidate['formal_apply_allowed']}, applied={candidate['applied']}",
                "",
            ]
        )
    lines.extend(
        [
            "## Teacher Review Actions",
            "",
            "Each candidate is preview-only and should enter the existing edit-card before/after/suggestion panel in R90B provider smoke.",
            "",
        ]
    )
    return "\n".join(lines)


def render_notes(profile_manifest: dict[str, Any], result: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# R90B-D0 Synthetic Candidate Strict Gate Notes",
            "",
            "R90B-D0 is a dry run inside `1013R_R90B_TRUE_GENERATION_QUALITY_SMOKE_V1`.",
            "",
            "It proves the strict gate can accept profile-correct candidate envelopes and reject known bad envelopes before a real provider is connected.",
            "",
            "## Active Profile",
            "",
            f"- profile_id: `{profile_manifest['profile_id']}`",
            f"- profile_version: `{profile_manifest['profile_version']}`",
            f"- candidate_contract_version: `{profile_manifest['candidate_contract_version']}`",
            "",
            "## Boundaries",
            "",
            "- no R21 modification",
            "- no provider/runtime connection",
            "- no database/Feishu/memory write",
            "- no formal apply",
            "- no new fields",
            "- no full lesson generation",
            "",
            "## Result",
            "",
            f"- strict_valid_candidates: `{result['summary']['strict_valid_candidates']}`",
            f"- expected_rejected_negative_candidates: `{result['summary']['expected_rejected_negative_candidates']}`",
            f"- result: `{result['result']}`",
            "",
            "## Next",
            "",
            "If GPT accepts D0, run R90B provider smoke with the same four target fields and the same strict validator.",
            "",
        ]
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)

    strict_policy = load_json(STRICT_POLICY_PATH)
    r82_schema = load_json(R82_SCHEMA_PATH)
    candidate_keys = load_json(CANDIDATE_KEYS_PATH)["candidate_required_keys_v1"]
    profile_manifest = load_json(PROFILE_MANIFEST_PATH)
    slot_map = strict_policy["step_target_field_to_generation_slot"]

    candidates = [candidate_for(target, slot_map) for target in TARGETS]
    synthetic_response = build_response(candidates)
    response_raw = json.dumps(synthetic_response, ensure_ascii=False, indent=2)
    parsed_response = json.loads(response_raw)
    strict_result = validate_response(parsed_response, r82_schema, candidate_keys, strict_policy)

    negative_fixtures = build_negative_fixtures(candidates)
    negative_results = [
        {
            "field_patch_id": candidate["field_patch_id"],
            "validation": validate_candidate(candidate, candidate_keys, strict_policy),
            "expected": "FAIL",
        }
        for candidate in negative_fixtures
    ]

    all_negative_rejected = all(item["validation"]["result"] == "FAIL" for item in negative_results)
    result = {
        "round": "1013R_R90B_D0_SYNTHETIC_CANDIDATE_STRICT_GATE_DRY_RUN",
        "parent_round": "1013R_R90B_TRUE_GENERATION_QUALITY_SMOKE_V1",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "result": "PASS" if strict_result["result"] == "PASS" and all_negative_rejected else "FAIL",
        "active_profile": {
            "profile_id": profile_manifest["profile_id"],
            "profile_version": profile_manifest["profile_version"],
            "candidate_contract_version": profile_manifest["candidate_contract_version"],
        },
        "scope": {
            "synthetic_only": True,
            "provider_runtime_connected": False,
            "r21_modified": False,
            "formal_apply_allowed": False,
            "database_written": False,
            "feishu_written": False,
            "memory_written": False,
            "new_fields_added": False,
            "full_lesson_generation": False,
        },
        "strict_positive_validation": strict_result,
        "negative_candidate_validation": negative_results,
        "summary": {
            "strict_valid_candidates": len(candidates) if strict_result["result"] == "PASS" else 0,
            "expected_rejected_negative_candidates": sum(1 for item in negative_results if item["validation"]["result"] == "FAIL"),
            "candidate_required_key_count": len(candidate_keys),
            "target_fields": [candidate["target_field_key"] for candidate in candidates],
        },
        "next_recommended_round": "1013R_R90B_PROVIDER_SMOKE_SAME_TARGETS",
    }

    write_json(OUT / "r90b_d0_synthetic_provider_response.json", synthetic_response)
    write_json(OUT / "r90b_d0_negative_candidate_fixtures.json", negative_fixtures)
    write_json(OUT / "r90b_d0_strict_validation_result.json", result)
    (OUT / "r90b_d0_teacher_review_card_preview.md").write_text(render_preview(candidates, result), encoding="utf-8")
    (OUT / "R90B_D0_SYNTHETIC_STRICT_GATE_NOTES.md").write_text(render_notes(profile_manifest, result), encoding="utf-8")
    (OUT / "README.md").write_text(
        "\n".join(
            [
                "# 1013R R90B True Generation Quality Smoke V1",
                "",
                "Current completed substage:",
                "",
                "```text",
                "R90B-D0_SYNTHETIC_CANDIDATE_STRICT_GATE_DRY_RUN",
                "```",
                "",
                "This folder currently contains only synthetic dry-run evidence. It does not contain real provider output yet.",
                "",
                "## Files",
                "",
                "- `r90b_d0_synthetic_provider_response.json`",
                "- `r90b_d0_negative_candidate_fixtures.json`",
                "- `r90b_d0_strict_validation_result.json`",
                "- `r90b_d0_teacher_review_card_preview.md`",
                "- `R90B_D0_SYNTHETIC_STRICT_GATE_NOTES.md`",
                "",
                "## Boundary",
                "",
                "- no R21 modification",
                "- no provider/runtime connection",
                "- no formal apply",
                "- no database/Feishu/memory write",
                "- no new fields",
                "",
            ]
        ),
        encoding="utf-8",
    )

    print(json.dumps({"result": result["result"], "out": str(OUT), "summary": result["summary"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
