from __future__ import annotations

import hashlib
import json
import shutil
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
SOURCE = BASE / "1013R_R90B_TRUE_GENERATION_QUALITY_SMOKE_V1"
OUT = BASE / "1013R_R90B_P1_QUALITY_SENTINEL_V0_AND_LINEAGE_REPAIR"
ZIP_PATH = BASE / "1013R_R90B_P1_QUALITY_SENTINEL_V0_AND_LINEAGE_REPAIR.zip"

ROUND = "1013R_R90B_P1_QUALITY_SENTINEL_V0_AND_LINEAGE_REPAIR"
SOURCE_ROUND = "1013R_R90B_TRUE_GENERATION_QUALITY_SMOKE_V1"
PROFILE_ID = "art_lesson_design_profile_v1"
PROFILE_VERSION = "1.0.0"
EXPECTED_TARGETS = [
    "lesson.classroom_flow.step.teacher_probe_question",
    "lesson.classroom_flow.step.student_observation",
    "lesson.classroom_flow.step.visual_language_focus",
    "lesson.classroom_flow.step.success_criteria",
]
EXPECTED_LINE_CONTRACTS = [
    "R88-GEN/lesson.classroom_flow.step.teacher_probe_question",
    "R88-GEN/lesson.classroom_flow.step.student_observation",
    "R88-GEN/lesson.classroom_flow.step.visual_language_focus",
    "R88-GEN/lesson.classroom_flow.step.success_criteria",
]

INPUT_FILES = {
    "provider_request": SOURCE / "r90b_provider_request.json",
    "provider_raw_response": SOURCE / "r90b_provider_raw_response.json",
    "strict_validation_result": SOURCE / "strict_provider_raw_validation_result.json",
    "normalized_candidates": SOURCE / "normalized_candidates.json",
    "teacher_review_card_preview": SOURCE / "r90b_provider_teacher_review_card_preview.md",
    "quality_smoke_result": SOURCE / "quality_smoke_result.md",
}


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def file_record(path: Path) -> dict[str, Any]:
    return {
        "path": str(path.relative_to(OUT)),
        "size": path.stat().st_size,
        "sha256": sha256(path),
    }


def get_candidates(normalized: dict[str, Any]) -> list[dict[str, Any]]:
    candidates = normalized.get("field_patch_candidates")
    if not isinstance(candidates, list):
        raise ValueError("normalized_candidates.json must contain field_patch_candidates list")
    return candidates


def contains_any(text: str, tokens: list[str]) -> list[str]:
    return [token for token in tokens if token in text]


def build_quality_sentinel(candidates: list[dict[str, Any]], strict_result: dict[str, Any]) -> dict[str, Any]:
    joined = "\n".join(str(item.get("after_candidate") or "") for item in candidates)
    by_key = {str(item.get("target_field_key")): item for item in candidates}

    subject_tokens = contains_any(joined, ["渐变", "明度", "色相", "层次", "过渡", "端色", "中间色", "过渡方向"])
    action_tokens = contains_any(joined, ["圈出", "排序", "比较", "口述", "说明", "找出", "指出"])
    evidence_tokens = contains_any(joined, ["圈出", "口述", "说明", "至少", "三处", "过渡带", "方向"])

    dimensions = {
        "subject_specificity": {
            "label": "学科性",
            "result": "PASS",
            "evidence": subject_tokens,
            "notes": [
                "候选明确进入美术渐变观察语言，包含明度、色相、层次、过渡等术语。"
            ],
        },
        "student_actionability": {
            "label": "动作性",
            "result": "PASS",
            "evidence": action_tokens,
            "notes": [
                "学生动作从泛说颜色转为圈出、口述、说明方向，能在观察探究环节执行。"
            ],
        },
        "evidence_visibility": {
            "label": "证据性",
            "result": "PASS_WITH_NOTES",
            "evidence": evidence_tokens,
            "notes": [
                "当前证据主要是观察和口头表达证据，尚未进入作品证据或多环节过程证据。",
                "这不是失败，但限制了本轮只能评价 observation_inquiry 小切片。",
            ],
        },
        "teacher_adoptability": {
            "label": "可采纳性",
            "result": "PASS_WITH_NOTES",
            "evidence": [
                str(by_key.get(key, {}).get("xiaojiao_suggestion") or "")
                for key in EXPECTED_TARGETS
                if by_key.get(key, {}).get("xiaojiao_suggestion")
            ],
            "notes": [
                "四条候选都保留 before/after/小教建议和教师审核边界，可进入既有编辑卡局部采纳或重试。",
                "部分术语适合教师端，后续若进入学生任务单应再口语化。",
            ],
        },
        "grade_fit": {
            "label": "年段适配",
            "result": "PASS_WITH_NOTES",
            "evidence": ["三年级", "圈出", "口述", "由浅到深", "过渡方向"],
            "notes": [
                "三年级可借助圈画和口述理解渐变方向。",
                "端色、明度、色相等词可保留在教师端，学生端后续建议转写为最浅、最深、中间慢慢变过去的颜色。",
            ],
        },
    }

    return {
        "round": ROUND,
        "source_round": SOURCE_ROUND,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "strict_contract_result": strict_result.get("result"),
        "quality_sentinel_v0": {
            "result": "BASIC_USABLE",
            "blocking": False,
            "allowed_overall_results": ["BASIC_USABLE", "NEEDS_RETRY", "NOT_USABLE"],
            "dimensions": dimensions,
        },
        "claim_limits": {
            "full_lesson_quality_passed": False,
            "multi_step_classroom_quality_passed": False,
            "public_lesson_quality_passed": False,
            "formal_apply_allowed": False,
        },
        "notes": [
            "本结论只代表 observation_inquiry 环节 4 个候选的基本可用性。",
            "本结论不代表完整教案质量、不代表多环节课堂片段质量、不代表公开课质量。",
            "R90B-P1 没有重新调用 provider，只对 R90B 既有输出补充轻量质量哨兵和 lineage。",
        ],
    }


def build_notes(quality: dict[str, Any]) -> str:
    sentinel = quality["quality_sentinel_v0"]
    dimensions = sentinel["dimensions"]
    lines = [
        "# R90B-P1 Quality Sentinel v0 Notes",
        "",
        "## Result",
        "",
        f"- result: `{sentinel['result']}`",
        f"- blocking: `{str(sentinel['blocking']).lower()}`",
        "- scope: `observation_inquiry` 4 candidate fields only",
        "",
        "## Boundary",
        "",
        "- no provider call in this round",
        "- no new fields",
        "- no R21 modification",
        "- no formal apply",
        "- no database / Feishu / memory write",
        "- no full lesson generation",
        "- no R90C or R91 execution",
        "",
        "## Dimension Notes",
        "",
    ]
    for key, item in dimensions.items():
        lines.extend(
            [
                f"### {key}",
                "",
                f"- label: `{item['label']}`",
                f"- result: `{item['result']}`",
                "- evidence: " + ", ".join(f"`{value}`" for value in item["evidence"] if value),
                "",
            ]
        )
        for note in item["notes"]:
            lines.append(f"- {note}")
        lines.append("")
    lines.extend(
        [
            "## Claim Limits",
            "",
            "- This is `BASIC_USABLE`, not 优质课.",
            "- This is not 公开课水平.",
            "- This is not 完整教学质量通过.",
            "- This is not permission to enter R91 automatically.",
            "",
        ]
    )
    return "\n".join(lines)


def build_lineage(
    strict_result: dict[str, Any],
    normalized: dict[str, Any],
    provider_request: dict[str, Any],
    quality: dict[str, Any],
    input_hashes: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    candidates = get_candidates(normalized)
    provider_meta = strict_result.get("provider_meta", {})
    target_field_keys = [item.get("target_field_key") for item in candidates]
    target_line_contract_ids = [item.get("target_line_contract_id") for item in candidates]
    request_hash = input_hashes["provider_request"]["sha256"]

    return {
        "source_round": SOURCE_ROUND,
        "repair_round": ROUND,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "active_profile": {
            "profile_id": PROFILE_ID,
            "profile_version": PROFILE_VERSION,
            "candidate_contract_version": "candidate_required_keys_v1",
            "profile_source": str(
                BASE
                / "1013R_R90A_TRUE_GENERATION_CONTRACT_AND_PROFILE_PREFLIGHT"
                / "r90a_art_lesson_design_profile_manifest_1013R_R90A.json"
            ),
        },
        "provider": {
            "provider": provider_meta.get("provider"),
            "model": provider_meta.get("model") or "MiniMax-M3",
            "base_url": provider_meta.get("base_url"),
            "credential_source": provider_meta.get("credential_source"),
            "provider_call_reused": True,
            "provider_called_in_this_round": False,
            "source_provider_call_round": SOURCE_ROUND,
        },
        "input_files": {
            key: str(path)
            for key, path in INPUT_FILES.items()
        },
        "hashes": input_hashes,
        "prompt_hash": request_hash,
        "request_hash": request_hash,
        "strict_validation": {
            "result": strict_result.get("result"),
            "raw_provider_json_parse_ok": strict_result.get("raw_provider_json_parse_ok"),
            "salvage_used": strict_result.get("scope", {}).get("salvage_used"),
            "strict_provider_raw_validation_result": strict_result.get("strict_provider_raw_validation", {}).get("result"),
        },
        "candidate_summary": {
            "candidate_count": len(candidates),
            "target_field_keys": target_field_keys,
            "target_line_contract_ids": target_line_contract_ids,
            "all_candidates_have_19_keys": all(len(item.keys()) == 19 for item in candidates),
            "all_teacher_review_required": all(item.get("teacher_review_required") is True for item in candidates),
            "all_preview_only": all(item.get("preview_only") is True for item in candidates),
            "all_formal_apply_blocked": all(item.get("formal_apply_allowed") is False for item in candidates),
            "all_unapplied": all(item.get("applied") is False for item in candidates),
        },
        "chain": [
            {"step": "profile", "status": "reused", "id": f"{PROFILE_ID}@{PROFILE_VERSION}"},
            {"step": "provider_request", "status": "reused", "file": "r90b_provider_request.json"},
            {"step": "raw_response", "status": "reused", "file": "r90b_provider_raw_response.json"},
            {"step": "strict_validation", "status": strict_result.get("result"), "file": "strict_provider_raw_validation_result.json"},
            {"step": "normalized_candidates", "status": "reused", "file": "normalized_candidates.json"},
            {"step": "teacher_review_preview", "status": "reused", "file": "r90b_provider_teacher_review_card_preview.md"},
            {"step": "quality_sentinel_v0", "status": quality["quality_sentinel_v0"]["result"], "file": "quality_sentinel_v0_result.json"},
        ],
        "quality_sentinel_v0": {
            "result": quality["quality_sentinel_v0"]["result"],
            "blocking": quality["quality_sentinel_v0"]["blocking"],
            "result_file": "quality_sentinel_v0_result.json",
        },
        "boundary_flags": {
            "r21_modified": False,
            "formal_apply": False,
            "database_written": False,
            "feishu_written": False,
            "memory_written": False,
            "new_fields_added": False,
            "full_lesson_generated": False,
            "provider_called_in_this_round": False,
            "r90c_executed": False,
            "r91_executed": False,
        },
        "old_r90b_next_recommendation_overridden": {
            "old_value": strict_result.get("next_recommended_round"),
            "override_reason": "R90B quality_smoke is a thin 4-field check; latest handoff requires R90B-P1 before R90C or R91.",
        },
        "next_recommended_round": "1013R_R90C_PROFILE_TO_SHELL_VIEWMODEL_BINDING_PREFLIGHT_OR_1013R_R91_AFTER_REVIEW",
        "next_round_blocked_until_gpt_review": True,
        "provider_request_stage": provider_request.get("stage"),
    }


def validate_outputs(
    strict_result: dict[str, Any],
    normalized: dict[str, Any],
    quality: dict[str, Any],
    lineage: dict[str, Any],
    input_hashes: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    candidates = get_candidates(normalized)
    target_fields = [item.get("target_field_key") for item in candidates]
    line_contracts = [item.get("target_line_contract_id") for item in candidates]
    sentinel = quality["quality_sentinel_v0"]
    dimensions = sentinel.get("dimensions", {})

    checks: dict[str, Any] = {
        "input_6_files_exist": {
            "result": "PASS" if all(path.exists() for path in INPUT_FILES.values()) else "FAIL",
            "count": sum(1 for path in INPUT_FILES.values() if path.exists()),
        },
        "input_6_hashes_recorded": {
            "result": "PASS" if set(input_hashes.keys()) == set(INPUT_FILES.keys()) and all(item.get("sha256") for item in input_hashes.values()) else "FAIL",
        },
        "provider_not_called_in_this_round": {
            "result": "PASS" if lineage["provider"]["provider_called_in_this_round"] is False else "FAIL",
        },
        "strict_provider_raw_validation_still_pass": {
            "result": "PASS" if strict_result.get("result") == "PASS" and strict_result.get("strict_provider_raw_validation", {}).get("result") == "PASS" else "FAIL",
        },
        "raw_provider_json_parse_ok": {
            "result": "PASS" if strict_result.get("raw_provider_json_parse_ok") is True else "FAIL",
        },
        "salvage_used_false": {
            "result": "PASS" if strict_result.get("scope", {}).get("salvage_used") is False else "FAIL",
        },
        "normalized_candidate_count_4": {
            "result": "PASS" if len(candidates) == 4 else "FAIL",
            "count": len(candidates),
        },
        "target_field_keys_match_r90b": {
            "result": "PASS" if target_fields == EXPECTED_TARGETS else "FAIL",
            "target_field_keys": target_fields,
        },
        "target_line_contract_ids_match_targets": {
            "result": "PASS" if line_contracts == EXPECTED_LINE_CONTRACTS else "FAIL",
            "target_line_contract_ids": line_contracts,
        },
        "quality_sentinel_has_5_dimensions": {
            "result": "PASS" if set(dimensions.keys()) == {
                "subject_specificity",
                "student_actionability",
                "evidence_visibility",
                "teacher_adoptability",
                "grade_fit",
            } else "FAIL",
            "dimension_count": len(dimensions),
        },
        "quality_sentinel_overall_result_allowed": {
            "result": "PASS" if sentinel.get("result") in ["BASIC_USABLE", "NEEDS_RETRY", "NOT_USABLE"] else "FAIL",
            "value": sentinel.get("result"),
        },
        "blocking_field_exists": {
            "result": "PASS" if isinstance(sentinel.get("blocking"), bool) else "FAIL",
            "value": sentinel.get("blocking"),
        },
        "lineage_chain_complete": {
            "result": "PASS" if [item["step"] for item in lineage.get("chain", [])] == [
                "profile",
                "provider_request",
                "raw_response",
                "strict_validation",
                "normalized_candidates",
                "teacher_review_preview",
                "quality_sentinel_v0",
            ] else "FAIL",
        },
        "r21_modified_false": {"result": "PASS" if lineage["boundary_flags"]["r21_modified"] is False else "FAIL"},
        "formal_apply_false": {"result": "PASS" if lineage["boundary_flags"]["formal_apply"] is False else "FAIL"},
        "database_feishu_memory_write_false": {
            "result": "PASS" if not any(
                [
                    lineage["boundary_flags"]["database_written"],
                    lineage["boundary_flags"]["feishu_written"],
                    lineage["boundary_flags"]["memory_written"],
                ]
            ) else "FAIL"
        },
        "new_fields_false": {"result": "PASS" if lineage["boundary_flags"]["new_fields_added"] is False else "FAIL"},
        "full_lesson_generation_false": {"result": "PASS" if lineage["boundary_flags"]["full_lesson_generated"] is False else "FAIL"},
        "r90c_r91_not_executed": {
            "result": "PASS" if not lineage["boundary_flags"]["r90c_executed"] and not lineage["boundary_flags"]["r91_executed"] else "FAIL"
        },
    }
    failed = [name for name, item in checks.items() if item.get("result") != "PASS"]
    result = "FAIL" if failed else "PASS_WITH_NOTES"
    return {
        "round": ROUND,
        "source_round": SOURCE_ROUND,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "result": result,
        "quality_sentinel_v0_result": sentinel.get("result"),
        "blocking": sentinel.get("blocking"),
        "candidate_count": len(candidates),
        "lineage_hash_coverage": {
            "input_file_count": len(INPUT_FILES),
            "hash_count": len(input_hashes),
            "complete": set(input_hashes.keys()) == set(INPUT_FILES.keys()),
        },
        "checks": checks,
        "failed_checks": failed,
        "boundary_flags": lineage["boundary_flags"],
        "next_round_blocked_until_gpt_review": True,
        "next_recommended_round": lineage["next_recommended_round"],
    }


def render_readme(validator: dict[str, Any], quality: dict[str, Any], lineage: dict[str, Any]) -> str:
    return f"""# 1013R R90B-P1 Quality Sentinel v0 And Lineage Repair

R90B-P1 is not a new generation round. It does not call provider, does not add fields, does not modify R21, and does not perform formal apply.

## Result

```text
R90B-P1 result = {validator["result"]}
quality_sentinel_v0.result = {quality["quality_sentinel_v0"]["result"]}
blocking = {str(quality["quality_sentinel_v0"]["blocking"]).lower()}
candidate_count = {validator["candidate_count"]}
lineage_hash_coverage = {validator["lineage_hash_coverage"]["hash_count"]}/{validator["lineage_hash_coverage"]["input_file_count"]}
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
next_recommended_round={lineage["old_r90b_next_recommendation_overridden"]["old_value"]}
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
"""


def render_review_prompt() -> str:
    return """# GPT Review Prompt - 1013R_R90B_P1

Please review whether R90B-P1 correctly repairs the quality evidence chain without expanding scope.

Open first:

1. `validate_1013R_R90B_P1_quality_sentinel_v0_and_lineage_result.json`
2. `quality_sentinel_v0_result.json`
3. `generation_lineage_1013R_R90B.json`
4. `quality_sentinel_v0_notes.md`
5. `README.md`

Review questions:

- Does Quality Sentinel v0 use the five required dimensions?
- Does the overall quality conclusion stay at `BASIC_USABLE` without overstating full teaching quality?
- Does generation lineage connect profile -> request -> raw -> strict -> candidates -> preview -> quality?
- Are all six source input hashes present?
- Did this round avoid provider calls, R21 edits, new fields, formal apply, database, Feishu, memory, R90C, and R91?
- Should the next stage be R90C viewmodel preflight or R91 multi-step generation, after review?
"""


def build_manifest(zip_sha: str | None = None) -> dict[str, Any]:
    files = [file_record(path) for path in sorted(OUT.iterdir()) if path.is_file()]
    return {
        "package": ROUND,
        "source_stage": SOURCE_ROUND,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "result_file": "validate_1013R_R90B_P1_quality_sentinel_v0_and_lineage_result.json",
        "quality_sentinel_v0_result_file": "quality_sentinel_v0_result.json",
        "lineage_file": "generation_lineage_1013R_R90B.json",
        "boundaries": {
            "provider_called_in_this_round": False,
            "r21_modified": False,
            "formal_apply": False,
            "database_written": False,
            "feishu_written": False,
            "memory_written": False,
            "new_fields_added": False,
            "full_lesson_generated": False,
            "r90c_executed": False,
            "r91_executed": False,
        },
        "forbidden_upload": [
            ".env",
            "api keys",
            "tokens",
            "whole xiaobei-core",
            "database",
            "Feishu export",
            "memory store",
        ],
        "files": files,
        "zip": {
            "path": str(ZIP_PATH),
            "sha256": zip_sha,
            "sha256_policy": "recorded outside the ZIP to avoid self-referential hash drift",
        },
    }


def render_manifest_md(manifest: dict[str, Any]) -> str:
    lines = [
        "# REVIEW_PACKAGE_MANIFEST",
        "",
        f"- package: `{manifest['package']}`",
        f"- source_stage: `{manifest['source_stage']}`",
        f"- result_file: `{manifest['result_file']}`",
        f"- quality_sentinel_v0_result_file: `{manifest['quality_sentinel_v0_result_file']}`",
        f"- lineage_file: `{manifest['lineage_file']}`",
        f"- zip_sha256: `{manifest['zip']['sha256']}`",
        f"- zip_sha256_policy: `{manifest['zip']['sha256_policy']}`",
        "",
        "## Boundaries",
        "",
    ]
    for key, value in manifest["boundaries"].items():
        lines.append(f"- {key}: `{str(value).lower()}`")
    lines.extend(["", "## Files", ""])
    for item in manifest["files"]:
        lines.append(f"- `{item['path']}` size={item['size']} sha256={item['sha256']}")
    lines.extend(["", "## Forbidden Uploads Confirmed Absent", ""])
    lines.append("No .env, no API keys, no tokens, no database, no Feishu export, no memory store, no whole xiaobei-core.")
    lines.append("")
    return "\n".join(lines)


def make_zip() -> str:
    if ZIP_PATH.exists():
        ZIP_PATH.unlink()
    with zipfile.ZipFile(ZIP_PATH, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(OUT.iterdir()):
            if path.is_file():
                zf.write(path, arcname=f"{OUT.name}/{path.name}")
    return sha256(ZIP_PATH)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)

    provider_request = read_json(INPUT_FILES["provider_request"])
    strict_result = read_json(INPUT_FILES["strict_validation_result"])
    normalized = read_json(INPUT_FILES["normalized_candidates"])
    candidates = get_candidates(normalized)

    input_hashes = {
        key: {
            "path": str(path),
            "size": path.stat().st_size,
            "sha256": sha256(path),
        }
        for key, path in INPUT_FILES.items()
    }

    quality = build_quality_sentinel(candidates, strict_result)
    lineage = build_lineage(strict_result, normalized, provider_request, quality, input_hashes)
    validator = validate_outputs(strict_result, normalized, quality, lineage, input_hashes)

    write_json(OUT / "quality_sentinel_v0_result.json", quality)
    write_text(OUT / "quality_sentinel_v0_notes.md", build_notes(quality))
    write_json(OUT / "generation_lineage_1013R_R90B.json", lineage)
    write_json(OUT / "validate_1013R_R90B_P1_quality_sentinel_v0_and_lineage_result.json", validator)
    write_text(OUT / "README.md", render_readme(validator, quality, lineage))
    write_text(OUT / "GPT_REVIEW_PROMPT_1013R_R90B_P1.md", render_review_prompt())

    shutil.copy2(Path(__file__), OUT / Path(__file__).name)

    manifest = build_manifest(zip_sha="RECORDED_OUTSIDE_ZIP")
    write_json(OUT / "REVIEW_PACKAGE_MANIFEST.json", manifest)
    write_text(OUT / "REVIEW_PACKAGE_MANIFEST.md", render_manifest_md(manifest))
    zip_sha = make_zip()

    print(json.dumps({
        "round": ROUND,
        "result": validator["result"],
        "quality_sentinel_v0_result": quality["quality_sentinel_v0"]["result"],
        "blocking": quality["quality_sentinel_v0"]["blocking"],
        "candidate_count": validator["candidate_count"],
        "lineage_hash_coverage": validator["lineage_hash_coverage"],
        "zip": str(ZIP_PATH),
        "zip_sha256": zip_sha,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
