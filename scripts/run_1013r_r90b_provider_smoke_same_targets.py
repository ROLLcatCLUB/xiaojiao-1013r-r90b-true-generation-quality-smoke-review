from __future__ import annotations

import json
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from backend.xiaobei_ai import providers
import build_1013r_r90b_d0_synthetic_candidate_strict_gate_dry_run as d0


BASE = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
OUT = BASE / "1013R_R90B_TRUE_GENERATION_QUALITY_SMOKE_V1"
R90A = BASE / "1013R_R90A_TRUE_GENERATION_CONTRACT_AND_PROFILE_PREFLIGHT"


TARGET_FIELDS = [
    "lesson.classroom_flow.step.teacher_probe_question",
    "lesson.classroom_flow.step.student_observation",
    "lesson.classroom_flow.step.visual_language_focus",
    "lesson.classroom_flow.step.success_criteria",
]


def write_json(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def build_prompt(strict_policy: dict[str, Any], r82_schema: dict[str, Any], candidate_keys: list[str]) -> dict[str, str]:
    slot_map = strict_policy["step_target_field_to_generation_slot"]
    template_candidate = {
        "field_patch_id": "r90b_provider_candidate_001",
        "schema_key": "classroom_flow",
        "canonical_field_key": "classroom_flow",
        "target_field_key": TARGET_FIELDS[0],
        "target_section": "teaching_process",
        "target_step_id": "observation_inquiry_01",
        "target_line_contract_id": slot_map[TARGET_FIELDS[0]],
        "target_destination": "existing_edit_card_before_after_suggestion_panel",
        "before_summary": "不超过30字",
        "after_candidate": "不超过60字",
        "xiaojiao_suggestion": "不超过40字",
        "impact_scope": ["classroom_flow", "observation"],
        "source_refs": ["active_profile:art_lesson_design_profile_v1@1.0.0", "lesson_case:色彩的渐变"],
        "teacher_review_required": True,
        "preview_only": True,
        "formal_apply_allowed": False,
        "applied": False,
        "patch_type": "profile_targeted_field_candidate",
        "reasoning_basis": "一句话说明为什么这样生成。",
    }
    request = {
        "stage_id": "1013R_R90B_TRUE_GENERATION_QUALITY_SMOKE_V1",
        "task": "只生成一个 observation_inquiry 课堂环节的 4 个字段候选，用于 strict provider raw validation。",
        "active_profile": {
            "profile_id": "art_lesson_design_profile_v1",
            "profile_version": "1.0.0",
            "candidate_contract_version": "candidate_required_keys_v1",
        },
        "lesson_case": {
            "subject": "小学美术",
            "grade": "三年级",
            "lesson_title": "2-1《色彩的渐变》",
            "unit_context": "第二单元《多彩的世界》，从自然和作品中的色彩变化进入渐变表达。",
            "known_student_start": "学生能看到颜色深浅、浓淡和鲜灰差异，但容易把渐变理解为几种颜色排上去。",
            "current_problem": "观察问题和评价证据偏泛，需要把观察、表达、评价都落到渐变层次。",
        },
        "required_top_level_keys": r82_schema["top_level_required_keys"],
        "required_candidate_keys_exactly": candidate_keys,
        "target_constraints": {
            "schema_key": "classroom_flow",
            "canonical_field_key": "classroom_flow",
            "target_section": "teaching_process",
            "target_step_id": "observation_inquiry_01",
            "target_fields_exactly_in_order": TARGET_FIELDS,
            "target_line_contract_id_map": {key: slot_map[key] for key in TARGET_FIELDS},
            "candidate_count": 4,
        },
        "content_quality_requirements": [
            "teacher_probe_question 必须是教师能在课堂中直接问的问题，聚焦渐变层次或过渡方向。",
            "student_observation 必须有学生可见动作，如圈出、排序、比较、说出变化方向。",
            "visual_language_focus 必须显性包含明度、色相、层次、过渡、渐变中的至少两个。",
            "success_criteria 必须能让学生检查作品，不写空泛表扬。",
        ],
        "length_limits": {
            "before_summary_max_zh_chars": 30,
            "after_candidate_max_zh_chars": 60,
            "xiaojiao_suggestion_max_zh_chars": 40,
            "impact_scope_max_items": 5,
            "source_refs_max_items": 4,
        },
        "hard_rules": [
            "只输出一个合法 JSON 对象，不要 Markdown，不要代码块，不要解释。",
            "field_patch_candidates 必须正好 4 个。",
            "每个 candidate 只能包含 required_candidate_keys_exactly 中的 19 个 key，不能多也不能少。",
            "target_field_key 不能写 classroom_flow，必须写 target_fields_exactly_in_order 中对应字段。",
            "target_line_contract_id 必须与 target_line_contract_id_map 完全一致。",
            "teacher_review_required=true, preview_only=true, formal_apply_allowed=false, applied=false。",
            "teacher_questions 必须是空数组。",
            "material_requests 必须是空数组。",
            "不要写数据库、飞书、记忆、正式课包，不要 formal apply。",
        ],
        "minimal_response_template": {
            "response_stage": "1013R_R90B_TRUE_GENERATION_QUALITY_SMOKE_V1",
            "request_id": "r90b_provider_smoke_001",
            "lesson_design_mode": "profile_targeted_smoke",
            "intent_summary": "string",
            "lesson_logic_brief": {
                "inherited_unit_context_summary": "string",
                "core_learning_problem": "string",
                "student_starting_point": "string",
                "target_shift": "string",
                "lesson_focus_question": "string",
                "visual_language_use": "string",
                "teaching_route": ["string"],
                "evidence_plan": ["string"],
                "risk_points": ["string"],
                "source_basis": ["active_profile", "lesson_case"],
                "material_gaps": [],
            },
            "target_resolution": [
                {
                    "schema_key": "classroom_flow",
                    "target_section": "teaching_process",
                    "target_step_id": "observation_inquiry_01",
                    "target_field": "observation_inquiry_active_step_fields",
                    "reason": "string",
                    "source_refs": ["active_profile:art_lesson_design_profile_v1@1.0.0"],
                }
            ],
            "step_reasoning_updates": [],
            "field_patch_candidates": [template_candidate],
            "quality_gate_update": {
                "level": "basic_usable",
                "passed_items": [],
                "missing_items": [],
                "risk_items": [],
                "next_best_action": "string",
            },
            "material_requests": [],
            "teacher_questions": [],
            "ui_binding_hint": {
                "should_enter_edit_mode": True,
                "edit_target": "teaching_process/observation_inquiry_01",
                "candidate_display_position": "existing_edit_card_before_after_suggestion_panel",
                "right_tray_updates": [],
                "view_mode_summary": "string",
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
        },
    }
    return {
        "system_prompt": "你是师维智教的小教备课生成器。只输出可被 JSON.parse 解析的 JSON 对象。不要 Markdown，不要解释，不要代码块。",
        "user_prompt": json.dumps(request, ensure_ascii=False, separators=(",", ":")),
    }


def quality_check(candidates: list[dict[str, Any]]) -> dict[str, Any]:
    by_key = {candidate.get("target_field_key"): candidate for candidate in candidates}
    checks = []

    teacher_text = str(by_key.get("lesson.classroom_flow.step.teacher_probe_question", {}).get("after_candidate") or "")
    checks.append(
        {
            "dimension": "teacher_probe_question",
            "passed": ("？" in teacher_text or "?" in teacher_text) and any(token in teacher_text for token in ["渐变", "层次", "过渡", "变化", "深", "浅"]),
            "text": teacher_text,
        }
    )

    observation_text = str(by_key.get("lesson.classroom_flow.step.student_observation", {}).get("after_candidate") or "")
    checks.append(
        {
            "dimension": "student_observation",
            "passed": any(token in observation_text for token in ["圈", "排序", "比较", "观察", "说出", "找出", "指出"]),
            "text": observation_text,
        }
    )

    visual_text = str(by_key.get("lesson.classroom_flow.step.visual_language_focus", {}).get("after_candidate") or "")
    visual_tokens = ["明度", "色相", "层次", "过渡", "渐变", "深浅"]
    checks.append(
        {
            "dimension": "visual_language_focus",
            "passed": sum(1 for token in visual_tokens if token in visual_text) >= 2,
            "text": visual_text,
        }
    )

    criteria_text = str(by_key.get("lesson.classroom_flow.step.success_criteria", {}).get("after_candidate") or "")
    checks.append(
        {
            "dimension": "success_criteria",
            "passed": any(token in criteria_text for token in ["作品", "至少", "层次", "清楚", "连续", "证据", "自查"]),
            "text": criteria_text,
        }
    )

    passed = sum(1 for item in checks if item["passed"])
    if passed == len(checks):
        result = "BASIC_USABLE"
    elif passed >= 2:
        result = "NEEDS_RETRY"
    else:
        result = "NOT_USABLE"
    return {"result": result, "passed_count": passed, "total": len(checks), "checks": checks}


def render_quality_md(strict_result: dict[str, Any], quality: dict[str, Any], provider_meta: dict[str, Any]) -> str:
    lines = [
        "# R90B Provider Quality Smoke Result",
        "",
        f"- strict_provider_raw_validation_result: `{strict_result['result']}`",
        f"- quality_smoke_result: `{quality['result']}`",
        f"- provider: `{provider_meta.get('provider')}`",
        f"- model: `{provider_meta.get('model')}`",
        f"- latency_ms: `{provider_meta.get('latency_ms')}`",
        "",
        "## Rubric",
        "",
    ]
    for item in quality["checks"]:
        lines.extend(
            [
                f"### {item['dimension']}",
                "",
                f"- passed: `{item['passed']}`",
                f"- text: {item['text']}",
                "",
            ]
        )
    lines.extend(
        [
            "## Boundary",
            "",
            "- R21 modified: `false`",
            "- formal apply: `false`",
            "- database/Feishu/memory write: `false`",
            "- candidate destination: `existing_edit_card_before_after_suggestion_panel`",
            "",
        ]
    )
    return "\n".join(lines)


def render_provider_preview(candidates: list[dict[str, Any]], validation: dict[str, Any], quality: dict[str, Any], provider_meta: dict[str, Any]) -> str:
    lines = [
        "# R90B Provider Teacher Review Card Preview",
        "",
        "This is the first real provider smoke for the frozen art profile. It used "
        f"{provider_meta.get('model')} through the existing openai-compatible provider channel. "
        "It did not modify R21, write a database, write memory, or perform formal apply.",
        "",
        "## Scope",
        "",
        "- profile: `art_lesson_design_profile_v1@1.0.0`",
        "- schema_key: `classroom_flow`",
        "- step_type: `observation_inquiry`",
        "- target_step_id: `observation_inquiry_01`",
        "- strict_provider_raw_validation_result: `" + validation["result"] + "`",
        "- quality_smoke_result: `" + quality["result"] + "`",
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
            "Each candidate is preview-only and should enter the existing edit-card before/after/suggestion panel in the next visible runtime/card binding stage.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    strict_policy = d0.load_json(d0.STRICT_POLICY_PATH)
    r82_schema = d0.load_json(d0.R82_SCHEMA_PATH)
    candidate_keys = d0.load_json(d0.CANDIDATE_KEYS_PATH)["candidate_required_keys_v1"]
    prompt = build_prompt(strict_policy, r82_schema, candidate_keys)

    request_record = {
        "stage": "1013R_R90B_TRUE_GENERATION_QUALITY_SMOKE_V1",
        "substage": "provider_smoke_same_targets",
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "provider_family": "minimax_or_openai_compatible",
        "model": None,
        "system_prompt": prompt["system_prompt"],
        "user_prompt": prompt["user_prompt"],
        "boundary": {
            "r21_modified": False,
            "formal_apply_allowed": False,
            "database_written": False,
            "feishu_written": False,
            "memory_written": False,
        },
    }
    write_json(OUT / "r90b_provider_request.json", request_record)

    started = time.perf_counter()
    try:
        provider_result = providers.generate_json_patch(
            {"mode": "1013R_R90B_TRUE_GENERATION_QUALITY_SMOKE_V1", "case_id": "color_gradient_observation_inquiry_01"},
            prompt,
            {
                "provider": "openai_compatible",
                "temperature": 0.1,
                "max_tokens": 2200,
                "timeout_ms": 120000,
                "use_response_format": True,
                "use_reasoning_split": False,
                "minimax_m3_thinking": "disabled",
            },
        )
        provider_meta = dict(provider_result.get("provider_meta") or {})
        raw_text = str(provider_result.get("raw_text") or "")
        provider_error = None
    except Exception as exc:  # noqa: BLE001 - smoke record needs exact provider failure.
        provider_meta = {}
        raw_text = ""
        provider_error = {"type": type(exc).__name__, "message": str(exc)}

    elapsed_ms = round((time.perf_counter() - started) * 1000)
    if provider_meta and not provider_meta.get("latency_ms"):
        provider_meta["latency_ms"] = elapsed_ms

    (OUT / "r90b_provider_raw_response.txt").write_text(raw_text, encoding="utf-8")
    write_json(
        OUT / "r90b_provider_call_record.json",
        {
            "provider_called": provider_error is None,
            "provider_error": provider_error,
            "provider_meta": provider_meta,
            "raw_text_length": len(raw_text),
            "elapsed_ms": elapsed_ms,
        },
    )

    if provider_error is not None:
        result = {
            "round": "1013R_R90B_TRUE_GENERATION_QUALITY_SMOKE_V1",
            "substage": "provider_smoke_same_targets",
            "result": "FAIL_PROVIDER_UNAVAILABLE",
            "provider_error": provider_error,
            "provider_meta": provider_meta,
            "scope": {
                "r21_modified": False,
                "formal_apply_allowed": False,
                "database_written": False,
                "feishu_written": False,
                "memory_written": False,
            },
        }
        write_json(OUT / "strict_provider_raw_validation_result.json", result)
        print(json.dumps({"result": result["result"], "provider_error": provider_error}, ensure_ascii=False, indent=2))
        return

    try:
        parsed = json.loads(raw_text)
        raw_parse_ok = True
        parse_error = None
    except Exception as exc:  # noqa: BLE001
        parsed = None
        raw_parse_ok = False
        parse_error = str(exc)

    if raw_parse_ok and isinstance(parsed, dict):
        write_json(OUT / "r90b_provider_raw_response.json", parsed)
        strict_result = d0.validate_response(parsed, r82_schema, candidate_keys, strict_policy)
    else:
        strict_result = d0.fail("raw_provider_json_parse_failed", {"parse_error": parse_error})

    candidates = parsed.get("field_patch_candidates") if isinstance(parsed, dict) else []
    candidates = candidates if isinstance(candidates, list) else []
    quality = quality_check(candidates) if strict_result["result"] == "PASS" else {"result": "NOT_EVALUATED_STRICT_FAILED", "checks": []}

    normalized = {
        "source": "provider_raw_response",
        "strict_validation_result": strict_result["result"],
        "field_patch_candidates": candidates if strict_result["result"] == "PASS" else [],
    }
    write_json(OUT / "normalized_candidates.json", normalized)

    final_result = {
        "round": "1013R_R90B_TRUE_GENERATION_QUALITY_SMOKE_V1",
        "substage": "provider_smoke_same_targets",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "result": "PASS" if strict_result["result"] == "PASS" else "FAIL_STRICT_PROVIDER_RAW_VALIDATION",
        "raw_provider_json_parse_ok": raw_parse_ok,
        "strict_provider_raw_validation": strict_result,
        "quality_smoke": quality,
        "provider_meta": provider_meta,
        "scope": {
            "provider_runtime_connected": True,
            "r21_modified": False,
            "formal_apply_allowed": False,
            "database_written": False,
            "feishu_written": False,
            "memory_written": False,
            "new_fields_added": False,
            "full_lesson_generation": False,
            "salvage_used": False,
        },
        "next_recommended_round": "1013R_R91_MULTI_STEP_CLASSROOM_FLOW_SMOKE" if strict_result["result"] == "PASS" else "1013R_R90B_PROVIDER_PROMPT_RETRY",
    }
    write_json(OUT / "strict_provider_raw_validation_result.json", final_result)

    if strict_result["result"] == "PASS":
        (OUT / "r90b_provider_teacher_review_card_preview.md").write_text(
            render_provider_preview(candidates, final_result, quality, provider_meta),
            encoding="utf-8",
        )
    else:
        (OUT / "r90b_provider_teacher_review_card_preview.md").write_text(
            "# R90B Provider Teacher Review Card Preview\n\nStrict provider raw validation failed, so no candidates may enter teacher review.\n",
            encoding="utf-8",
        )
    (OUT / "quality_smoke_result.md").write_text(render_quality_md(final_result, quality, provider_meta), encoding="utf-8")

    print(
        json.dumps(
            {
                "result": final_result["result"],
                "raw_provider_json_parse_ok": raw_parse_ok,
                "quality_smoke_result": quality["result"],
                "provider_meta": provider_meta,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
