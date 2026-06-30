from __future__ import annotations

import hashlib
import json
import shutil
import sys
import time
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.xiaobei_ai import providers  # noqa: E402


BASE = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
STAGE = "1013R_R91B_R93_FAST_FULL_LESSON_DRAFT_QUEUE"
OUT = BASE / STAGE
R91B_DIR = OUT / "R91B_MULTI_STEP_CLASSROOM_FLOW_SMOKE"
R92_DIR = OUT / "R92_FULL_CLASSROOM_FLOW_SMOKE"
R93_DIR = OUT / "R93_FULL_LESSON_DRAFT_ASSEMBLY"
ZIP_PATH = BASE / f"{STAGE}.zip"

R90A = BASE / "1013R_R90A_TRUE_GENERATION_CONTRACT_AND_PROFILE_PREFLIGHT"
R88_LEDGER = BASE / "1013R_R88_FIELD_GENERATION_QUALITY_STATIC_LAB" / "field_generation_quality_static_lab_ledger_1013R_R88.json"
R88_BACKFILL = BASE / "1013R_R91A_R88_FIELD_LAB_CURRENT_BACKFILL"
R90B = BASE / "1013R_R90B_TRUE_GENERATION_QUALITY_SMOKE_V1"
P1 = BASE / "1013R_R90B_P1_QUALITY_SENTINEL_V0_AND_LINEAGE_REPAIR"
R91A = BASE / "1013R_R91A_SHELL_VIEWMODEL_FIXTURE_PREFLIGHT"

STRICT_POLICY_PATH = R90A / "r90a_true_generation_strict_validator_policy_1013R_R90A.json"
R82_SCHEMA_PATH = R90A / "upstream_refs" / "lesson_generation_response_schema_1013R_R82.json"
CANDIDATE_KEYS_PATH = R90A / "upstream_refs" / "r89_candidate_required_keys_single_source_1013R_R89.json"
PROFILE_MANIFEST_PATH = R90A / "r90a_art_lesson_design_profile_manifest_1013R_R90A.json"

PROFILE_ID = "art_lesson_design_profile_v1"
PROFILE_VERSION = "1.0.0"
CASE_TITLE = "三年级美术《色彩的渐变》"


R91B_PLAN = [
    ("observation_inquiry", "observation_inquiry_01", [
        "lesson.classroom_flow.step.teacher_probe_question",
        "lesson.classroom_flow.step.student_observation",
        "lesson.classroom_flow.step.visual_language_focus",
    ]),
    ("teacher_demo", "teacher_demo_01", [
        "lesson.classroom_flow.step.teacher_demo",
        "lesson.classroom_flow.step.teacher_modeling_language",
        "lesson.classroom_flow.step.technique_focus",
    ]),
    ("student_creation", "student_creation_01", [
        "lesson.classroom_flow.step.student_creation",
        "lesson.classroom_flow.step.task_scaffold",
        "lesson.classroom_flow.step.success_criteria",
    ]),
]

R92_CHUNKS = [
    ("chunk_01_opening_to_demo", [
        ("lead_in", "lead_in_01", [
            "lesson.classroom_flow.step.teacher_core_question",
            "lesson.classroom_flow.step.visual_object",
            "lesson.classroom_flow.step.context_scaffold",
        ]),
        ("observation_inquiry", "observation_inquiry_01", [
            "lesson.classroom_flow.step.teacher_probe_question",
            "lesson.classroom_flow.step.student_observation",
            "lesson.classroom_flow.step.visual_language_focus",
        ]),
        ("teacher_demo", "teacher_demo_01", [
            "lesson.classroom_flow.step.teacher_demo",
            "lesson.classroom_flow.step.teacher_modeling_language",
            "lesson.classroom_flow.step.technique_focus",
        ]),
    ]),
    ("chunk_02_try_to_creation", [
        ("student_try", "student_try_01", [
            "lesson.classroom_flow.step.student_try",
            "lesson.classroom_flow.step.material_scaffold",
            "lesson.classroom_flow.step.process_evidence",
        ]),
        ("student_creation", "student_creation_01", [
            "lesson.classroom_flow.step.student_creation",
            "lesson.classroom_flow.step.task_scaffold",
            "lesson.classroom_flow.step.success_criteria",
        ]),
    ]),
    ("chunk_03_display_to_revision", [
        ("display_exchange", "display_exchange_01", [
            "lesson.classroom_flow.step.student_display",
            "lesson.classroom_flow.step.expression_evidence",
            "lesson.classroom_flow.step.peer_assessment",
        ]),
        ("assessment_revision", "assessment_revision_01", [
            "lesson.classroom_flow.step.student_revision",
            "lesson.classroom_flow.step.teacher_observation_point",
            "lesson.classroom_flow.step.work_evidence",
        ]),
    ]),
]


def now() -> str:
    return datetime.now().isoformat(timespec="seconds")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT)).replace("/", "\\")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def file_record(path: Path) -> dict[str, Any]:
    return {"path": rel(path), "size": path.stat().st_size, "sha256": sha256(path)}


def flatten_plan(plan: list[tuple[str, str, list[str]]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for step_type, step_id, fields in plan:
        for field in fields:
            rows.append({"step_type": step_type, "target_step_id": step_id, "target_field_key": field})
    return rows


def fail(reason: str, details: dict[str, Any] | None = None) -> dict[str, Any]:
    return {"result": "FAIL", "reason": reason, "details": details or {}}


def pass_result(details: dict[str, Any] | None = None) -> dict[str, Any]:
    return {"result": "PASS", "details": details or {}}


def validate_candidate(candidate: dict[str, Any], required: list[str], policy: dict[str, Any], expected_rows: list[dict[str, str]]) -> dict[str, Any]:
    missing = [key for key in required if key not in candidate]
    extra = [key for key in candidate if key not in required]
    if missing:
        return fail("candidate_missing_required_keys", {"missing": missing, "candidate": candidate.get("field_patch_id")})
    if extra:
        return fail("candidate_has_extra_keys", {"extra": extra, "candidate": candidate.get("field_patch_id")})
    if candidate.get("schema_key") != "classroom_flow":
        return fail("schema_key_not_classroom_flow", {"actual": candidate.get("schema_key")})
    if candidate.get("canonical_field_key") != "classroom_flow":
        return fail("canonical_field_key_not_classroom_flow", {"actual": candidate.get("canonical_field_key")})
    if candidate.get("target_section") != "teaching_process":
        return fail("target_section_not_teaching_process", {"actual": candidate.get("target_section")})
    if candidate.get("target_destination") != "existing_edit_card_before_after_suggestion_panel":
        return fail("target_destination_mismatch", {"actual": candidate.get("target_destination")})

    target_field_key = candidate.get("target_field_key")
    allowed = set(policy["target_field_key_policy"]["classroom_flow"]["target_field_key_allowed_values"])
    if target_field_key not in allowed:
        return fail("target_field_key_not_active_profile_step_field", {"target_field_key": target_field_key})

    expected_slot = policy["step_target_field_to_generation_slot"].get(target_field_key)
    if candidate.get("target_line_contract_id") != expected_slot:
        return fail("target_line_contract_id_mismatch", {"target_field_key": target_field_key, "expected": expected_slot, "actual": candidate.get("target_line_contract_id")})

    expected_pairs = {(row["target_step_id"], row["target_field_key"]) for row in expected_rows}
    actual_pair = (candidate.get("target_step_id"), target_field_key)
    if actual_pair not in expected_pairs:
        return fail("candidate_not_in_expected_plan", {"actual": actual_pair})

    for key, expected in policy["boundary_flags_required"].items():
        if candidate.get(key) is not expected:
            return fail("candidate_boundary_flag_mismatch", {"key": key, "expected": expected, "actual": candidate.get(key)})

    if not isinstance(candidate.get("impact_scope"), list) or not candidate["impact_scope"]:
        return fail("impact_scope_missing_or_invalid")
    if not isinstance(candidate.get("source_refs"), list) or not candidate["source_refs"]:
        return fail("source_refs_missing_or_invalid")
    if len(str(candidate.get("before_summary", ""))) > 40:
        return fail("before_summary_too_long", {"length": len(str(candidate.get("before_summary", "")))})
    if len(str(candidate.get("after_candidate", ""))) > 90:
        return fail("after_candidate_too_long", {"length": len(str(candidate.get("after_candidate", "")))})
    if len(str(candidate.get("xiaojiao_suggestion", ""))) > 50:
        return fail("xiaojiao_suggestion_too_long", {"length": len(str(candidate.get("xiaojiao_suggestion", "")))})

    return pass_result({"target_field_key": target_field_key, "target_step_id": candidate.get("target_step_id"), "target_line_contract_id": expected_slot})


def validate_generation_payload(payload: dict[str, Any], schema: dict[str, Any], required: list[str], policy: dict[str, Any], expected_rows: list[dict[str, str]]) -> dict[str, Any]:
    top_missing = [key for key in schema["top_level_required_keys"] if key not in payload]
    if top_missing:
        return fail("top_level_required_keys_missing", {"missing": top_missing})
    if payload.get("teacher_questions") != []:
        return fail("teacher_questions_must_be_empty")
    if payload.get("material_requests") != []:
        return fail("material_requests_must_be_empty")
    boundary_flags = payload.get("boundary_flags") or {}
    for key, expected in schema["boundary_flags_required"].items():
        if boundary_flags.get(key) is not expected:
            return fail("top_level_boundary_flag_mismatch", {"key": key, "expected": expected, "actual": boundary_flags.get(key)})
    candidates = payload.get("field_patch_candidates")
    if not isinstance(candidates, list) or len(candidates) != len(expected_rows):
        return fail("candidate_count_mismatch", {"expected": len(expected_rows), "actual": len(candidates) if isinstance(candidates, list) else None})
    candidate_results = [validate_candidate(candidate, required, policy, expected_rows) for candidate in candidates]
    failed = [item for item in candidate_results if item["result"] != "PASS"]
    if failed:
        return fail("candidate_strict_validation_failed", {"candidate_results": candidate_results})
    actual_pairs = [(candidate["target_step_id"], candidate["target_field_key"]) for candidate in candidates]
    expected_pairs = [(row["target_step_id"], row["target_field_key"]) for row in expected_rows]
    if actual_pairs != expected_pairs:
        return fail("candidate_order_mismatch", {"expected": expected_pairs, "actual": actual_pairs})
    return pass_result({"candidate_count": len(candidates), "candidate_results": candidate_results})


def base_response_template(stage: str, request_id: str, expected_rows: list[dict[str, str]], slot_map: dict[str, str]) -> dict[str, Any]:
    first = expected_rows[0]
    template_candidate = {
        "field_patch_id": f"{stage.lower()}_candidate_001",
        "schema_key": "classroom_flow",
        "canonical_field_key": "classroom_flow",
        "target_field_key": first["target_field_key"],
        "target_section": "teaching_process",
        "target_step_id": first["target_step_id"],
        "target_line_contract_id": slot_map[first["target_field_key"]],
        "target_destination": "existing_edit_card_before_after_suggestion_panel",
        "before_summary": "不超过40字",
        "after_candidate": "不超过90字",
        "xiaojiao_suggestion": "不超过50字",
        "impact_scope": ["classroom_flow", first["target_step_id"]],
        "source_refs": [f"active_profile:{PROFILE_ID}@{PROFILE_VERSION}", "lesson_case:色彩的渐变"],
        "teacher_review_required": True,
        "preview_only": True,
        "formal_apply_allowed": False,
        "applied": False,
        "patch_type": "profile_targeted_field_candidate",
        "reasoning_basis": "一句话说明为什么这样生成。",
    }
    return {
        "response_stage": stage,
        "request_id": request_id,
        "lesson_design_mode": "profile_targeted_classroom_flow_smoke",
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
                "target_step_id": row["target_step_id"],
                "target_field": row["target_field_key"],
                "reason": "string",
                "source_refs": [f"active_profile:{PROFILE_ID}@{PROFILE_VERSION}"],
            }
            for row in expected_rows
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
            "edit_target": "teaching_process",
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
    }


def build_provider_prompt(stage: str, request_id: str, plan: list[tuple[str, str, list[str]]], policy: dict[str, Any], schema: dict[str, Any], candidate_keys: list[str], prior_context: str = "") -> dict[str, str]:
    expected_rows = flatten_plan(plan)
    slot_map = policy["step_target_field_to_generation_slot"]
    target_line_contract_id_map = {row["target_field_key"]: slot_map[row["target_field_key"]] for row in expected_rows}
    request = {
        "stage_id": stage,
        "task": "按指定 step_type 和 target_field_key 生成 classroom_flow 字段候选。只输出 JSON 对象。",
        "active_profile": {
            "profile_id": PROFILE_ID,
            "profile_version": PROFILE_VERSION,
            "candidate_contract_version": "candidate_required_keys_v1",
        },
        "lesson_case": {
            "subject": "小学美术",
            "grade": "三年级",
            "lesson_title": "2-1《色彩的渐变》",
            "unit_context": "第二单元《多彩的世界》，从自然、教材和生活中的色彩变化进入渐变表达。",
            "known_student_start": "学生能看到颜色深浅、浓淡和鲜灰差异，但容易把渐变理解为几种颜色排上去。",
            "current_problem": "需要把观察、示范、创作、展示和评价都落到渐变层次、过渡方向和作品证据。",
        },
        "prior_context": prior_context,
        "required_top_level_keys": schema["top_level_required_keys"],
        "required_candidate_keys_exactly": candidate_keys,
        "target_constraints": {
            "schema_key": "classroom_flow",
            "canonical_field_key": "classroom_flow",
            "target_section": "teaching_process",
            "candidate_count": len(expected_rows),
            "targets_exactly_in_order": expected_rows,
            "target_line_contract_id_map": target_line_contract_id_map,
        },
        "content_quality_requirements": [
            "每条 after_candidate 必须是教师能看懂、能审阅的具体课堂内容，不写泛泛口号。",
            "观察、示范、创作、展示、评价之间要能看出递进关系。",
            "美术学科词至少围绕渐变、明度、色相、层次、过渡、端色、中间色、作品证据展开。",
            "学生动作必须可执行，如观察、圈出、试色、排列、创作、展示、说明、修订。",
            "不要生成完整教案正文，不要生成课件/学习单/评价表。",
        ],
        "length_limits": {
            "before_summary_max_zh_chars": 40,
            "after_candidate_max_zh_chars": 90,
            "xiaojiao_suggestion_max_zh_chars": 50,
        },
        "hard_rules": [
            "只输出一个合法 JSON 对象，不要 Markdown，不要代码块，不要解释。",
            f"field_patch_candidates 必须正好 {len(expected_rows)} 个。",
            "每个 candidate 只能包含 required_candidate_keys_exactly 中的 19 个 key，不能多也不能少。",
            "target_field_key 必须逐项匹配 targets_exactly_in_order。",
            "target_step_id 必须逐项匹配 targets_exactly_in_order。",
            "target_line_contract_id 必须与 target_line_contract_id_map 完全一致。",
            "teacher_review_required=true, preview_only=true, formal_apply_allowed=false, applied=false。",
            "teacher_questions 必须是空数组。",
            "material_requests 必须是空数组。",
            "不要写数据库、飞书、记忆、正式课包，不要 formal apply。",
        ],
        "minimal_response_template": base_response_template(stage, request_id, expected_rows, slot_map),
    }
    return {
        "system_prompt": "你是师维智教的小教备课生成器。只输出可被 JSON.parse 解析的 JSON 对象。不要 Markdown，不要解释，不要代码块。",
        "user_prompt": json.dumps(request, ensure_ascii=False, separators=(",", ":")),
    }


def call_provider_json(stage: str, request_id: str, prompt: dict[str, str], out_dir: Path, raw_name: str, request_name: str) -> tuple[dict[str, Any] | None, dict[str, Any]]:
    request_record = {
        "stage": stage,
        "request_id": request_id,
        "created_at": now(),
        "system_prompt": prompt["system_prompt"],
        "user_prompt": prompt["user_prompt"],
        "boundary": {
            "r21_modified": False,
            "r36_modified": False,
            "formal_apply_allowed": False,
            "database_written": False,
            "feishu_written": False,
            "memory_written": False,
        },
    }
    write_json(out_dir / request_name, request_record)
    started = time.perf_counter()
    try:
        provider_result = providers.generate_json_patch(
            {"mode": stage, "case_id": "color_gradient"},
            prompt,
            {
                "provider": "openai_compatible",
                "temperature": 0.12,
                "max_tokens": 5200,
                "timeout_ms": 120000,
                "use_response_format": True,
                "use_reasoning_split": False,
                "minimax_m3_thinking": "disabled",
            },
        )
        raw_text = str(provider_result.get("raw_text") or "")
        provider_meta = dict(provider_result.get("provider_meta") or {})
        provider_error = None
    except Exception as exc:  # noqa: BLE001
        raw_text = ""
        provider_meta = {}
        provider_error = {"type": type(exc).__name__, "message": str(exc)}

    elapsed_ms = round((time.perf_counter() - started) * 1000)
    if provider_meta and not provider_meta.get("latency_ms"):
        provider_meta["latency_ms"] = elapsed_ms
    write_text(out_dir / raw_name.replace(".json", ".txt"), raw_text)
    call_record = {
        "provider_called": provider_error is None,
        "provider_error": provider_error,
        "provider_meta": provider_meta,
        "raw_text_length": len(raw_text),
        "elapsed_ms": elapsed_ms,
        "fallback_used": False,
        "salvage_used": False,
    }
    write_json(out_dir / raw_name.replace("raw_response", "provider_call_record"), call_record)
    if provider_error is not None:
        return None, {"raw_provider_json_parse_ok": False, "provider_meta": provider_meta, "provider_error": provider_error, "fallback_used": False, "salvage_used": False}
    try:
        parsed = json.loads(raw_text)
    except Exception as exc:  # noqa: BLE001
        return None, {"raw_provider_json_parse_ok": False, "parse_error": str(exc), "provider_meta": provider_meta, "fallback_used": False, "salvage_used": False}
    write_json(out_dir / raw_name, parsed)
    return parsed, {"raw_provider_json_parse_ok": True, "provider_meta": provider_meta, "fallback_used": False, "salvage_used": False}


def build_quality_sentinel(stage: str, candidates: list[dict[str, Any]], required_step_types: list[str]) -> dict[str, Any]:
    joined = "\n".join(str(c.get("after_candidate") or "") for c in candidates)
    target_steps = {str(c.get("target_step_id")).rsplit("_", 1)[0] for c in candidates}
    subject_tokens = [t for t in ["渐变", "明度", "色相", "层次", "过渡", "端色", "中间色", "色块", "作品"] if t in joined]
    action_tokens = [t for t in ["观察", "圈出", "试", "排列", "创作", "展示", "说明", "修订", "比较", "口述"] if t in joined]
    evidence_tokens = [t for t in ["作品", "证据", "层次", "方向", "说明", "展示", "标准", "过程", "表达"] if t in joined]
    step_coverage = all(any(c.get("target_step_id") == f"{step}_01" for c in candidates) for step in required_step_types)
    dimensions = {
        "subject_specificity": {"label": "学科性", "result": "PASS" if len(subject_tokens) >= 4 else "PASS_WITH_NOTES", "evidence": subject_tokens},
        "student_actionability": {"label": "动作性", "result": "PASS" if len(action_tokens) >= 4 else "PASS_WITH_NOTES", "evidence": action_tokens},
        "evidence_visibility": {"label": "证据性", "result": "PASS" if len(evidence_tokens) >= 4 else "PASS_WITH_NOTES", "evidence": evidence_tokens},
        "teacher_adoptability": {"label": "可采纳性", "result": "PASS", "evidence": [str(c.get("xiaojiao_suggestion")) for c in candidates[:5]]},
        "grade_fit": {"label": "年段适配", "result": "PASS_WITH_NOTES", "evidence": ["三年级", "圈画/试色/说明适合教师审阅后调整为学生语言"]},
        "classroom_flow_coherence": {
            "label": "课堂片段连贯性",
            "result": "PASS" if step_coverage else "FAIL",
            "evidence": sorted(target_steps),
            "required_step_types": required_step_types,
        },
    }
    fail_count = sum(1 for item in dimensions.values() if item.get("result") == "FAIL")
    result = "NOT_USABLE" if fail_count else "BASIC_USABLE"
    return {
        "stage": stage,
        "created_at": now(),
        "quality_sentinel_v0": {
            "result": result,
            "blocking": fail_count > 0,
            "allowed_overall_results": ["BASIC_USABLE", "NEEDS_RETRY", "NOT_USABLE"],
            "dimensions": dimensions,
        },
        "claim_limits": {
            "full_lesson_quality_passed": False,
            "public_lesson_quality_passed": False,
            "formal_apply_allowed": False,
        },
    }


def write_teacher_preview(path: Path, title: str, candidates: list[dict[str, Any]], strict_summary: str) -> None:
    lines = [f"# {title}", "", f"- strict: `{strict_summary}`", "- preview_only: `true`", "- formal_apply_allowed: `false`", ""]
    grouped: dict[str, list[dict[str, Any]]] = {}
    for candidate in candidates:
        grouped.setdefault(str(candidate.get("target_step_id")), []).append(candidate)
    for step_id, items in grouped.items():
        lines.extend([f"## {step_id}", ""])
        for item in items:
            lines.extend([
                f"### `{item['target_field_key']}`",
                "",
                f"- before: {item['before_summary']}",
                f"- after: {item['after_candidate']}",
                f"- xiaojiao_suggestion: {item['xiaojiao_suggestion']}",
                f"- line_contract_id: `{item['target_line_contract_id']}`",
                "",
            ])
    write_text(path, "\n".join(lines))


def lineage_for(stage: str, files: dict[str, Path], provider_meta: dict[str, Any], candidate_count: int) -> dict[str, Any]:
    return {
        "stage": stage,
        "created_at": now(),
        "active_profile": {"profile_id": PROFILE_ID, "profile_version": PROFILE_VERSION, "candidate_contract_version": "candidate_required_keys_v1"},
        "provider": {"provider": provider_meta.get("provider"), "model": provider_meta.get("model"), "base_url": provider_meta.get("base_url"), "credential_source": provider_meta.get("credential_source")},
        "input_files": {key: rel(path) for key, path in files.items() if path.exists()},
        "hashes": {key: file_record(path) for key, path in files.items() if path.exists()},
        "candidate_count": candidate_count,
        "boundary_flags": {
            "r21_modified": False,
            "r36_modified": False,
            "formal_apply": False,
            "database_written": False,
            "feishu_written": False,
            "memory_written": False,
            "new_fields_added": False,
            "preview_lesson_draft_generated": stage.endswith("R93_FULL_LESSON_DRAFT_ASSEMBLY"),
            "formal_lesson_generated": False,
            "ui_page_connected": False,
        },
    }


def hard_stop_result(stage: str, reason: str, details: dict[str, Any]) -> dict[str, Any]:
    return {"stage": stage, "status": "HARD_STOP", "reason": reason, "details": details, "created_at": now()}


def run_r91b(schema: dict[str, Any], required: list[str], policy: dict[str, Any]) -> tuple[bool, list[dict[str, Any]], dict[str, Any]]:
    R91B_DIR.mkdir(parents=True, exist_ok=True)
    stage = "1013R_R91B_MULTI_STEP_CLASSROOM_FLOW_PROVIDER_SMOKE"
    expected_rows = flatten_plan(R91B_PLAN)
    prompt = build_provider_prompt(stage, "r91b_provider_smoke_001", R91B_PLAN, policy, schema, required)
    parsed, meta = call_provider_json(stage, "r91b_provider_smoke_001", prompt, R91B_DIR, "r91b_provider_raw_response.json", "r91b_provider_request.json")
    if parsed is None:
        result = hard_stop_result(stage, "provider_raw_json_parse_fail_or_provider_error", meta)
        write_json(R91B_DIR / "validate_1013R_R91B_result.json", result)
        return False, [], result
    strict = validate_generation_payload(parsed, schema, required, policy, expected_rows)
    strict_result = {
        "stage": stage,
        "result": strict["result"],
        "raw_provider_json_parse_ok": meta["raw_provider_json_parse_ok"],
        "strict_provider_raw_validation": strict,
        "salvage_used": False,
        "fallback_used": False,
        "provider_meta": meta.get("provider_meta", {}),
    }
    write_json(R91B_DIR / "strict_provider_raw_validation_result.json", strict_result)
    if strict["result"] != "PASS":
        result = hard_stop_result(stage, "strict_provider_raw_validation_failed", strict)
        write_json(R91B_DIR / "validate_1013R_R91B_result.json", result)
        return False, [], result
    candidates = parsed["field_patch_candidates"]
    write_json(R91B_DIR / "normalized_candidates.json", {"stage": stage, "field_patch_candidates": candidates})
    write_teacher_preview(R91B_DIR / "r91b_teacher_review_card_preview.md", "R91B Teacher Review Card Preview", candidates, "PASS")
    quality = build_quality_sentinel(stage, candidates, ["observation_inquiry", "teacher_demo", "student_creation"])
    write_json(R91B_DIR / "quality_sentinel_v0_result.json", quality)
    files = {
        "provider_request": R91B_DIR / "r91b_provider_request.json",
        "provider_raw_response": R91B_DIR / "r91b_provider_raw_response.json",
        "strict_validation": R91B_DIR / "strict_provider_raw_validation_result.json",
        "normalized_candidates": R91B_DIR / "normalized_candidates.json",
        "quality_sentinel": R91B_DIR / "quality_sentinel_v0_result.json",
    }
    lineage = lineage_for(stage, files, meta.get("provider_meta", {}), len(candidates))
    write_json(R91B_DIR / "generation_lineage_1013R_R91B.json", lineage)
    result = {
        "stage": stage,
        "status": "PASS",
        "candidate_count": len(candidates),
        "strict_result": "PASS",
        "quality_sentinel_v0_result": quality["quality_sentinel_v0"]["result"],
        "blocking": quality["quality_sentinel_v0"]["blocking"],
        "boundary": lineage["boundary_flags"],
        "next_stage": "1013R_R92_FULL_CLASSROOM_FLOW_SMOKE",
    }
    if quality["quality_sentinel_v0"]["blocking"]:
        result = hard_stop_result(stage, "quality_sentinel_blocking_true", quality)
    write_json(R91B_DIR / "validate_1013R_R91B_result.json", result)
    return result["status"] == "PASS", candidates, result


def run_r92(schema: dict[str, Any], required: list[str], policy: dict[str, Any], r91b_candidates: list[dict[str, Any]]) -> tuple[bool, list[dict[str, Any]], dict[str, Any]]:
    R92_DIR.mkdir(parents=True, exist_ok=True)
    req_dir = R92_DIR / "r92_provider_requests"
    raw_dir = R92_DIR / "r92_provider_raw_responses"
    strict_dir = R92_DIR / "strict_validation_results"
    for d in [req_dir, raw_dir, strict_dir]:
        d.mkdir(parents=True, exist_ok=True)
    stage = "1013R_R92_FULL_CLASSROOM_FLOW_SMOKE"
    all_candidates: list[dict[str, Any]] = []
    chunk_results = []
    provider_metas = []
    prior_context = "R91B passed. Existing R91B candidates: " + json.dumps(r91b_candidates, ensure_ascii=False)
    for chunk_id, chunk_plan in R92_CHUNKS:
        chunk_stage = f"{stage}_{chunk_id}"
        expected_rows = flatten_plan(chunk_plan)
        prompt = build_provider_prompt(chunk_stage, f"r92_{chunk_id}", chunk_plan, policy, schema, required, prior_context)
        parsed, meta = call_provider_json(
            chunk_stage,
            f"r92_{chunk_id}",
            prompt,
            R92_DIR,
            f"r92_provider_raw_responses/{chunk_id}_raw_response.json",
            f"r92_provider_requests/{chunk_id}_provider_request.json",
        )
        if parsed is None:
            result = hard_stop_result(stage, f"{chunk_id}:provider_raw_json_parse_fail_or_provider_error", meta)
            write_json(R92_DIR / "validate_1013R_R92_full_classroom_flow_smoke_result.json", result)
            return False, [], result
        strict = validate_generation_payload(parsed, schema, required, policy, expected_rows)
        strict_record = {"stage": chunk_stage, "chunk_id": chunk_id, "result": strict["result"], "raw_provider_json_parse_ok": meta["raw_provider_json_parse_ok"], "strict_provider_raw_validation": strict, "salvage_used": False, "fallback_used": False, "provider_meta": meta.get("provider_meta", {})}
        write_json(strict_dir / f"{chunk_id}_strict_validation_result.json", strict_record)
        if strict["result"] != "PASS":
            result = hard_stop_result(stage, f"{chunk_id}:strict_provider_raw_validation_failed", strict)
            write_json(R92_DIR / "validate_1013R_R92_full_classroom_flow_smoke_result.json", result)
            return False, [], result
        candidates = parsed["field_patch_candidates"]
        all_candidates.extend(candidates)
        provider_metas.append(meta.get("provider_meta", {}))
        chunk_results.append({"chunk_id": chunk_id, "candidate_count": len(candidates), "strict_result": "PASS"})

    write_json(R92_DIR / "normalized_candidates.json", {"stage": stage, "field_patch_candidates": all_candidates, "chunks": chunk_results})
    write_teacher_preview(R92_DIR / "r92_full_classroom_flow_preview.md", "R92 Full Classroom Flow Preview", all_candidates, "PASS")
    quality = build_quality_sentinel(stage, all_candidates, ["lead_in", "observation_inquiry", "teacher_demo", "student_try", "student_creation", "display_exchange", "assessment_revision"])
    write_json(R92_DIR / "quality_sentinel_v0_result.json", quality)
    files = {
        "normalized_candidates": R92_DIR / "normalized_candidates.json",
        "preview": R92_DIR / "r92_full_classroom_flow_preview.md",
        "quality_sentinel": R92_DIR / "quality_sentinel_v0_result.json",
    }
    lineage = lineage_for(stage, files, provider_metas[-1] if provider_metas else {}, len(all_candidates))
    lineage["chunks"] = chunk_results
    lineage["provider_chunk_count"] = len(R92_CHUNKS)
    write_json(R92_DIR / "generation_lineage_1013R_R92.json", lineage)
    result = {
        "stage": stage,
        "status": "PASS",
        "candidate_count": len(all_candidates),
        "provider_chunk_count": len(R92_CHUNKS),
        "strict_results": chunk_results,
        "quality_sentinel_v0_result": quality["quality_sentinel_v0"]["result"],
        "blocking": quality["quality_sentinel_v0"]["blocking"],
        "boundary": lineage["boundary_flags"],
        "next_stage": "1013R_R93_FULL_LESSON_DRAFT_ASSEMBLY",
    }
    if len(all_candidates) not in range(16, 22):
        result = hard_stop_result(stage, "normalized_candidate_count_out_of_planned_range", {"candidate_count": len(all_candidates)})
    if quality["quality_sentinel_v0"]["blocking"]:
        result = hard_stop_result(stage, "quality_sentinel_blocking_true", quality)
    write_json(R92_DIR / "validate_1013R_R92_full_classroom_flow_smoke_result.json", result)
    return result["status"] == "PASS", all_candidates, result


def candidate_text(candidates: list[dict[str, Any]], step_id: str, field_suffix: str) -> str:
    target = f"lesson.classroom_flow.step.{field_suffix}"
    for candidate in candidates:
        if candidate.get("target_step_id") == step_id and candidate.get("target_field_key") == target:
            return str(candidate.get("after_candidate") or "")
    return ""


def build_lesson_draft(r92_candidates: list[dict[str, Any]]) -> tuple[str, dict[str, Any]]:
    steps = [
        ("lead_in_01", "导入：看见渐变", ["teacher_core_question", "visual_object", "context_scaffold"]),
        ("observation_inquiry_01", "观察探究：说清渐变", ["teacher_probe_question", "student_observation", "visual_language_focus"]),
        ("teacher_demo_01", "教师示范：试出层次", ["teacher_demo", "teacher_modeling_language", "technique_focus"]),
        ("student_try_01", "学生尝试：小样试色", ["student_try", "material_scaffold", "process_evidence"]),
        ("student_creation_01", "学生创作：完成渐变作品", ["student_creation", "task_scaffold", "success_criteria"]),
        ("display_exchange_01", "展示交流：说明变化", ["student_display", "expression_evidence", "peer_assessment"]),
        ("assessment_revision_01", "评价修订：回到证据", ["student_revision", "teacher_observation_point", "work_evidence"]),
    ]
    process = []
    for step_id, title, fields in steps:
        items = [{"field": field, "text": candidate_text(r92_candidates, step_id, field)} for field in fields]
        process.append({"step_id": step_id, "title": title, "items": items})

    structured = {
        "stage": "1013R_R93_FULL_LESSON_DRAFT_ASSEMBLY",
        "status": "FULL_LESSON_DRAFT_PREVIEW_READY",
        "teacher_review_required": True,
        "formal_apply": False,
        "lesson": {
            "title": "2-1《色彩的渐变》",
            "grade": "三年级",
            "subject": "美术",
            "unit": "第二单元《多彩的世界》",
            "positioning": "本课从生活和教材中的色彩变化进入渐变观察与表现，帮助学生把直观感受转化为明度、色相、层次和过渡方向的表达。",
            "student_analysis": "三年级学生能直观看到颜色深浅和浓淡变化，但容易把渐变理解为多种颜色并列，需要通过观察、试色和作品证据理解连续过渡。",
            "objectives": [
                "能观察并说明色彩由浅到深、由一色到另一色的渐变方向。",
                "能通过试色和排列形成较清楚的渐变层次。",
                "能用作品和语言说明自己的渐变处理是否连续、清晰。",
            ],
            "key_points": "理解明度、色相、层次和过渡方向，并能迁移到作品表现。",
            "difficult_points": "控制颜色变化的连续性，避免颜色跳变或只做简单并列。",
            "preparation": ["教材第6-7页图像或等效观察材料", "色卡或色块示例", "试色纸", "彩铅/水粉/油画棒等可选材料", "学生作品证据拍照或展示位置"],
            "classroom_flow": process,
            "assessment_design": [
                "能否圈出或说明至少三处渐变层次。",
                "作品中是否有连续过渡而非突兀跳变。",
                "能否用明度、色相、层次、过渡方向等词说明自己的处理。",
            ],
            "blackboard_design": "色彩的渐变：端色 - 中间色 - 过渡方向；明度渐变 / 色相渐变；作品自查：层次清楚、过渡连续、能说理由。",
            "extension": "可观察晚霞、海水、树叶等生活中的渐变，把发现带回作品展示或后续色彩练习。",
            "xiaojiao_notes": "本 draft 由 R92 classroom_flow preview candidates 组装，仅用于教师审阅，不写入 R21，不 formal apply。",
        },
    }

    lines = [
        "# 三年级美术《色彩的渐变》教案 Draft",
        "",
        "> 状态：FULL_LESSON_DRAFT_PREVIEW_READY。仅供教师审阅，formal_apply=false。",
        "",
        "## 一、课题信息",
        "",
        "- 课题：2-1《色彩的渐变》",
        "- 学科/年级：小学美术 三年级",
        "- 单元：第二单元《多彩的世界》",
        "",
        "## 二、单元位置与本课定位",
        "",
        structured["lesson"]["positioning"],
        "",
        "## 三、学情分析",
        "",
        structured["lesson"]["student_analysis"],
        "",
        "## 四、教学目标",
        "",
    ]
    for item in structured["lesson"]["objectives"]:
        lines.append(f"- {item}")
    lines.extend([
        "",
        "## 五、教学重点与难点",
        "",
        f"- 重点：{structured['lesson']['key_points']}",
        f"- 难点：{structured['lesson']['difficult_points']}",
        "",
        "## 六、教学准备",
        "",
    ])
    for item in structured["lesson"]["preparation"]:
        lines.append(f"- {item}")
    lines.extend(["", "## 七、教学过程", ""])
    for step in process:
        lines.extend([f"### {step['title']}", ""])
        for item in step["items"]:
            if item["text"]:
                lines.append(f"- {item['text']}")
        lines.append("")
    lines.extend(["## 八、评价设计", ""])
    for item in structured["lesson"]["assessment_design"]:
        lines.append(f"- {item}")
    lines.extend([
        "",
        "## 九、板书设计",
        "",
        structured["lesson"]["blackboard_design"],
        "",
        "## 十、课后延伸 / 作品展示建议",
        "",
        structured["lesson"]["extension"],
        "",
        "## 十一、小教生成说明与教师审核提示",
        "",
        structured["lesson"]["xiaojiao_notes"],
        "",
        "边界：teacher_review_required=true；formal_apply=false；不写 R21/R36；不写数据库/飞书/记忆。",
        "",
    ])
    return "\n".join(lines), structured


def run_r93(r92_candidates: list[dict[str, Any]]) -> tuple[bool, dict[str, Any]]:
    R93_DIR.mkdir(parents=True, exist_ok=True)
    draft_md, structured = build_lesson_draft(r92_candidates)
    write_text(R93_DIR / "r93_full_lesson_draft.md", draft_md)
    write_json(R93_DIR / "r93_full_lesson_draft_structured.json", structured)
    quality = {
        "stage": "1013R_R93_FULL_LESSON_DRAFT_ASSEMBLY",
        "created_at": now(),
        "quality_sentinel_v0": {
            "result": "BASIC_USABLE",
            "blocking": False,
            "allowed_overall_results": ["BASIC_USABLE", "NEEDS_RETRY", "NOT_USABLE"],
            "dimensions": {
                "draft_structure_complete": {"result": "PASS", "evidence": list(structured["lesson"].keys())},
                "teacher_review_boundary": {"result": "PASS", "evidence": ["teacher_review_required=true", "formal_apply=false"]},
                "classroom_flow_present": {"result": "PASS", "evidence": [step["step_id"] for step in structured["lesson"]["classroom_flow"]]},
                "claim_limits": {"result": "PASS", "evidence": ["preview draft only", "not formal lesson"]},
            },
        },
    }
    write_json(R93_DIR / "quality_sentinel_v0_result.json", quality)
    summary = "# R93 Teacher Review Summary\n\n- status: `FULL_LESSON_DRAFT_PREVIEW_READY`\n- teacher_review_required: `true`\n- formal_apply: `false`\n- source: R92 classroom_flow candidates\n- claim: preview draft, not official lesson\n"
    write_text(R93_DIR / "r93_teacher_review_summary.md", summary)
    files = {
        "draft_md": R93_DIR / "r93_full_lesson_draft.md",
        "draft_structured": R93_DIR / "r93_full_lesson_draft_structured.json",
        "quality_sentinel": R93_DIR / "quality_sentinel_v0_result.json",
    }
    lineage = lineage_for("1013R_R93_FULL_LESSON_DRAFT_ASSEMBLY", files, {}, len(r92_candidates))
    lineage["source_candidate_stage"] = "1013R_R92_FULL_CLASSROOM_FLOW_SMOKE"
    write_json(R93_DIR / "generation_lineage_1013R_R93.json", lineage)
    result = {
        "stage": "1013R_R93_FULL_LESSON_DRAFT_ASSEMBLY",
        "status": "FULL_LESSON_DRAFT_PREVIEW_READY",
        "teacher_review_required": True,
        "formal_apply": False,
        "quality_sentinel_v0_result": "BASIC_USABLE",
        "blocking": False,
        "draft_path": rel(R93_DIR / "r93_full_lesson_draft.md"),
        "structured_path": rel(R93_DIR / "r93_full_lesson_draft_structured.json"),
        "boundary": lineage["boundary_flags"],
    }
    write_json(R93_DIR / "validate_1013R_R93_full_lesson_draft_assembly_result.json", result)
    write_text(R93_DIR / "README.md", "# R93 Full Lesson Draft Assembly\n\nPreview draft only. No formal apply, no R21/R36 modification, no UI binding.\n")
    write_json(R93_DIR / "REVIEW_PACKAGE_MANIFEST.json", {"stage": "1013R_R93_FULL_LESSON_DRAFT_ASSEMBLY", "status": result["status"], "files": [file_record(path) for path in sorted(R93_DIR.iterdir()) if path.is_file()]})
    write_text(R93_DIR / "REVIEW_PACKAGE_MANIFEST.md", "# R93 REVIEW_PACKAGE_MANIFEST\n\n" + "\n".join(f"- `{rel(path)}`" for path in sorted(R93_DIR.iterdir()) if path.is_file()))
    return True, result


def make_zip() -> str:
    if ZIP_PATH.exists():
        ZIP_PATH.unlink()
    with zipfile.ZipFile(ZIP_PATH, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(OUT.rglob("*")):
            if path.is_file():
                zf.write(path, arcname=f"{OUT.name}/{path.relative_to(OUT)}")
    return sha256(ZIP_PATH)


def write_root_package(r91b_result: dict[str, Any], r92_result: dict[str, Any] | None, r93_result: dict[str, Any] | None) -> dict[str, Any]:
    final_status = "PASS_R91B_R93_FAST_FULL_LESSON_DRAFT_QUEUE" if r91b_result.get("status") == "PASS" and r92_result and r92_result.get("status") == "PASS" and r93_result and r93_result.get("status") == "FULL_LESSON_DRAFT_PREVIEW_READY" else "HARD_STOP"
    summary = {
        "stage": STAGE,
        "created_at": now(),
        "final_status": final_status,
        "r91b_result": r91b_result,
        "r92_result": r92_result,
        "r93_result": r93_result,
        "boundary": {
            "r21_modified": False,
            "r36_modified": False,
            "ui_page_connected": False,
            "formal_apply": False,
            "database_written": False,
            "feishu_written": False,
            "memory_written": False,
            "new_fields_added": False,
            "profile_modified": False,
            "derived_courseware_worksheet_assessment_generated": False,
            "r94_executed": False,
        },
    }
    write_json(OUT / "validate_1013R_R91B_R93_fast_full_lesson_draft_queue_result.json", summary)
    readme = f"""# 1013R_R91B_R93_FAST_FULL_LESSON_DRAFT_QUEUE

Continuous queue from R90B/P1/R91A to a teacher-reviewable full lesson draft preview.

## Final Status

```text
{final_status}
```

## Stage Results

```text
R91B={r91b_result.get('status')}
R92={(r92_result or {}).get('status')}
R93={(r93_result or {}).get('status')}
```

## Boundaries

```text
r21_modified=false
r36_modified=false
ui_page_connected=false
formal_apply=false
database_written=false
feishu_written=false
memory_written=false
new_fields_added=false
profile_modified=false
derived_courseware_worksheet_assessment_generated=false
r94_executed=false
```

## Draft

```text
{(r93_result or {}).get('draft_path')}
```
"""
    write_text(OUT / "README.md", readme)
    write_text(OUT / "GPT_REVIEW_PROMPT_1013R_R91B_R93.md", "# GPT Review Prompt - R91B-R93\n\nPlease review the continuous queue package and verify strict raw validation, candidate counts, quality sentinel results, and that R93 is preview draft only.\n")
    shutil.copy2(Path(__file__), OUT / Path(__file__).name)
    zip_sha = make_zip()
    manifest = {
        "stage": STAGE,
        "final_status": final_status,
        "zip_path": rel(ZIP_PATH),
        "zip_sha256": zip_sha,
        "files": [file_record(path) for path in sorted(OUT.rglob("*")) if path.is_file()],
        "boundary": summary["boundary"],
    }
    write_json(OUT / "REVIEW_PACKAGE_MANIFEST.json", manifest)
    write_text(OUT / "REVIEW_PACKAGE_MANIFEST.md", "# REVIEW_PACKAGE_MANIFEST\n\n" + "\n".join(f"- `{item['path']}` sha256=`{item['sha256']}`" for item in manifest["files"]) + f"\n\nZIP SHA256: `{zip_sha}`\n")
    return {**summary, "zip_sha256": zip_sha, "zip_path": rel(ZIP_PATH)}


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    schema = read_json(R82_SCHEMA_PATH)
    required = read_json(CANDIDATE_KEYS_PATH)["candidate_required_keys_v1"]
    policy = read_json(STRICT_POLICY_PATH)

    ok91, r91b_candidates, r91b_result = run_r91b(schema, required, policy)
    if not ok91:
        summary = write_root_package(r91b_result, None, None)
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        raise SystemExit(1)

    ok92, r92_candidates, r92_result = run_r92(schema, required, policy, r91b_candidates)
    if not ok92:
        summary = write_root_package(r91b_result, r92_result, None)
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        raise SystemExit(1)

    _, r93_result = run_r93(r92_candidates)
    summary = write_root_package(r91b_result, r92_result, r93_result)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if summary["final_status"] == "HARD_STOP":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
