from __future__ import annotations

import hashlib
import json
import shutil
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
STAGE = "1013R_R91A_SHELL_VIEWMODEL_FIXTURE_PREFLIGHT"
OUT = BASE / STAGE

R36_HTML = BASE / "1013L_R36_existing_page_static_patch_consolidation" / "prep_room_render_canvas_deepen_v1_1013L_R36_consolidated.html"
R90B = BASE / "1013R_R90B_TRUE_GENERATION_QUALITY_SMOKE_V1"
P1 = BASE / "1013R_R90B_P1_QUALITY_SENTINEL_V0_AND_LINEAGE_REPAIR"
R15 = BASE / "1013R_R15_prep_room_unified_viewmodel_r0" / "prep_room_unified_viewmodel_sample_1013R_R15.json"
R29 = BASE / "1013R_R29_tool_frame_registry" / "tool_frame_registry_1013R_R29.json"
R30 = BASE / "1013R_R30_visible_frame_connector" / "1013R_R30_connector_map.json"


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")


def rel(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT)).replace("/", "\\")
    except ValueError:
        return str(path)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def file_record(path: Path) -> dict:
    return {
        "path": rel(path),
        "size": path.stat().st_size,
        "sha256": sha256(path),
    }


def assert_file(path: Path, errors: list[str]) -> None:
    if not path.exists():
        errors.append(f"missing_file:{rel(path)}")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    errors: list[str] = []
    warnings: list[str] = []

    for path in [
        R36_HTML,
        R90B / "normalized_candidates.json",
        P1 / "quality_sentinel_v0_result.json",
        P1 / "generation_lineage_1013R_R90B.json",
        R15,
        R29,
        R30,
    ]:
        assert_file(path, errors)
    if errors:
        write_json(OUT / "validate_1013R_R91A_shell_viewmodel_fixture_preflight_result.json", {
            "stage": STAGE,
            "status": "FAIL",
            "errors": errors,
        })
        raise SystemExit(1)

    r36_html = R36_HTML.read_text(encoding="utf-8")
    normalized = read_json(R90B / "normalized_candidates.json")
    p1_quality = read_json(P1 / "quality_sentinel_v0_result.json")
    lineage = read_json(P1 / "generation_lineage_1013R_R90B.json")
    r15 = read_json(R15)
    r29 = read_json(R29)
    r30 = read_json(R30)

    shell_required_markers = [
        "ShiweiShell",
        "prep-render-canvas",
        "chat-input-shell",
        "nb-edit-bubble",
        "nb-edit-panel",
        "data-edit-target",
        "placeEditBubble",
        "makeEditPanel",
    ]
    shell_marker_checks = {
        marker: marker in r36_html for marker in shell_required_markers
    }
    for marker, present in shell_marker_checks.items():
        if not present:
            errors.append(f"r36_shell_marker_missing:{marker}")

    quality = p1_quality.get("quality_sentinel_v0", {})
    if quality.get("blocking") is not False:
        errors.append("p1_quality_sentinel_blocking_not_false")
    if quality.get("result") not in {"BASIC_USABLE", "PASS"}:
        errors.append(f"p1_quality_sentinel_not_usable:{quality.get('result')}")
    if p1_quality.get("strict_contract_result") != "PASS":
        errors.append("p1_strict_contract_not_pass")

    candidates = normalized.get("field_patch_candidates", [])
    if len(candidates) < 4:
        errors.append("candidate_count_less_than_4")

    tool_frames = r29.get("tool_frames", [])
    prep_notebook = next((x for x in tool_frames if x.get("tool_id") == "prep_notebook"), None)
    if not prep_notebook:
        errors.append("r29_prep_notebook_tool_missing")
    content_bindings = r29.get("content_slot_bindings", [])
    teaching_process_slot = next((x for x in content_bindings if x.get("slot_id") == "teaching_process"), None)
    if not teaching_process_slot:
        errors.append("r29_teaching_process_slot_missing")

    connectors = r30.get("tool_content_connectors", [])
    prep_connector = next((x for x in connectors if x.get("tool_id") == "prep_notebook"), None)
    if not prep_connector:
        errors.append("r30_prep_notebook_connector_missing")

    teacher_review_cards = []
    for index, candidate in enumerate(candidates, start=1):
        cid = candidate.get("field_patch_id") or f"candidate_{index:03d}"
        required_flags = {
            "teacher_review_required": candidate.get("teacher_review_required") is True,
            "preview_only": candidate.get("preview_only") is True,
            "formal_apply_allowed_false": candidate.get("formal_apply_allowed") is False,
            "applied_false": candidate.get("applied") is False,
            "target_destination_edit_card": candidate.get("target_destination") == "existing_edit_card_before_after_suggestion_panel",
            "target_section_teaching_process": candidate.get("target_section") == "teaching_process",
        }
        for key, ok in required_flags.items():
            if not ok:
                errors.append(f"{cid}:{key}:failed")

        impact_scope = candidate.get("impact_scope") or []
        if "classroom_flow" not in impact_scope:
            errors.append(f"{cid}:impact_scope_missing_classroom_flow")
        if candidate.get("target_step_id") != "observation_inquiry_01":
            warnings.append(f"{cid}:target_step_id_not_observation_inquiry_01")

        teacher_review_cards.append({
            "card_id": f"teacher_review_card_{index:03d}",
            "source_candidate_id": cid,
            "component": "TeacherReviewCard",
            "render_slot": {
                "level_1": "platform_shell",
                "level_2": "prep_room",
                "level_3_tool_id": "prep_notebook",
                "level_4_content_slot_id": "teaching_process",
                "shell_render_slot": "stage_body",
                "target_destination": "existing_edit_card_before_after_suggestion_panel",
                "visible_selector_reference": "[data-edit-target], .nb-edit-bubble, .nb-edit-panel",
            },
            "shell_state": {
                "shell_name": "ShiweiShell",
                "room_id": "prep_room",
                "room_label": "备课室",
                "active_view": "prepNotebook",
                "source_page_baseline": rel(R36_HTML),
                "page_connection_performed": False,
                "dom_patch_performed": False,
                "uses_native_edit_bubble_contract": True,
            },
            "teacher_review_payload": {
                "before_summary": candidate.get("before_summary"),
                "after_candidate": candidate.get("after_candidate"),
                "xiaojiao_suggestion": candidate.get("xiaojiao_suggestion"),
                "target_field_key": candidate.get("target_field_key"),
                "target_step_id": candidate.get("target_step_id"),
                "impact_scope": impact_scope,
                "source_refs": candidate.get("source_refs", []),
                "reasoning_basis": candidate.get("reasoning_basis"),
                "teacher_review_required": True,
                "preview_only": True,
                "formal_apply_allowed": False,
                "applied": False,
            },
            "gate": {
                "gate_type": "preview_then_confirm",
                "allowed_now": True,
                "requires_teacher_confirmation": True,
                "write_effect": "preview_only",
                "formal_apply_allowed": False,
            },
        })

    shell_viewmodel_fixture = {
        "ok": len(errors) == 0,
        "stage": STAGE,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "purpose": "Preflight R90B provider candidates against the current prep-room shell and readonly ViewModel render-slot contracts before any R91 provider expansion.",
        "source_chain": {
            "r90b_stage": "1013R_R90B_TRUE_GENERATION_QUALITY_SMOKE_V1",
            "r90b_p1_stage": "1013R_R90B_P1_QUALITY_SENTINEL_V0_AND_LINEAGE_REPAIR",
            "current_shell_baseline": rel(R36_HTML),
            "unified_viewmodel_source": rel(R15),
            "tool_frame_registry_source": rel(R29),
            "visible_connector_source": rel(R30),
        },
        "active_profile": lineage.get("active_profile", {}),
        "shell_contract": {
            "shell_name": "ShiweiShell",
            "room_id": "prep_room",
            "room_label": "备课室",
            "persistent_regions": [
                "top navigation / platform shell",
                "prep-render-canvas / render stage",
                "chat-input-shell / bottom xiaojiao composer",
            ],
            "native_review_surface": [
                "nb-edit-bubble",
                "nb-edit-panel",
                "data-edit-target",
                "placeEditBubble",
                "makeEditPanel",
            ],
            "required_marker_checks": shell_marker_checks,
        },
        "viewmodel_context": {
            "current_object": r15.get("current_object"),
            "active_view": r15.get("lesson_viewmodel", {}).get("active_view"),
            "active_node_id": r15.get("lesson_viewmodel", {}).get("active_node_id"),
            "tool_frame": prep_notebook,
            "content_slot_binding": teaching_process_slot,
            "visible_connector": prep_connector,
        },
        "teacher_review_cards": teacher_review_cards,
        "boundary": {
            "fixture_only": True,
            "page_connection_performed": False,
            "r36_modified": False,
            "r21_modified": False,
            "provider_called": False,
            "model_called": False,
            "database_written": False,
            "feishu_written": False,
            "memory_written": False,
            "new_fields_added": False,
            "formal_apply_performed": False,
            "r91b_provider_expansion_performed": False,
        },
    }

    result = {
        "stage": STAGE,
        "status": "PASS" if not errors else "FAIL",
        "created_at": shell_viewmodel_fixture["created_at"],
        "checks": {
            "r36_shell_baseline_exists": R36_HTML.exists(),
            "r36_shell_markers_present": all(shell_marker_checks.values()),
            "p1_quality_not_blocking": quality.get("blocking") is False,
            "p1_quality_basic_usable": quality.get("result") == "BASIC_USABLE",
            "p1_strict_contract_pass": p1_quality.get("strict_contract_result") == "PASS",
            "candidate_count": len(candidates),
            "candidate_count_at_least_4": len(candidates) >= 4,
            "all_candidates_teacher_review_cards": len(teacher_review_cards) == len(candidates),
            "r29_prep_notebook_tool_present": prep_notebook is not None,
            "r29_teaching_process_slot_present": teaching_process_slot is not None,
            "r30_prep_notebook_connector_present": prep_connector is not None,
            "no_provider_call": True,
            "no_page_or_runtime_write": True,
        },
        "errors": errors,
        "warnings": warnings,
        "final_status": "PASS_R91A_SHELL_VIEWMODEL_FIXTURE_PREFLIGHT" if not errors else "FAIL_R91A_SHELL_VIEWMODEL_FIXTURE_PREFLIGHT",
        "next_recommendation": "1013R_R91B_MULTI_STEP_CLASSROOM_FLOW_PROVIDER_SMOKE_ONLY_IF_GPT_REVIEW_ACCEPTS_R91A",
        "boundary": shell_viewmodel_fixture["boundary"],
    }

    write_json(OUT / "r91a_shell_viewmodel_fixture.json", shell_viewmodel_fixture)
    write_json(OUT / "teacher_review_card_viewmodel_map_1013R_R91A.json", {
        "stage": STAGE,
        "card_count": len(teacher_review_cards),
        "cards": teacher_review_cards,
    })
    write_json(OUT / "validate_1013R_R91A_shell_viewmodel_fixture_preflight_result.json", result)

    notes = f"""# 1013R R91A Shell ViewModel Fixture Preflight Notes

R91A checks whether the R90B provider candidates can be represented as TeacherReviewCard fixture payloads inside the current prep-room shell contract.

This round does not connect the real page, does not patch R36/R21, does not call provider, and does not enter R91B.

## Result

```text
status={result["status"]}
candidate_count={len(candidates)}
r36_shell_markers_present={all(shell_marker_checks.values())}
p1_quality_result={quality.get("result")}
p1_blocking={quality.get("blocking")}
```

## Current Shell Baseline

```text
{rel(R36_HTML)}
```

## Native Review Surface

```text
nb-edit-bubble
nb-edit-panel
data-edit-target
placeEditBubble
makeEditPanel
```

## Boundary

```text
fixture_only=true
page_connection_performed=false
r36_modified=false
r21_modified=false
provider_called=false
model_called=false
database_written=false
feishu_written=false
memory_written=false
formal_apply_performed=false
r91b_provider_expansion_performed=false
```
"""
    write_text(OUT / "r91a_shell_viewmodel_fixture_preflight_notes.md", notes)

    readme = f"""# 1013R_R91A_SHELL_VIEWMODEL_FIXTURE_PREFLIGHT

R91A is a fixture-only shell/ViewModel preflight after R90B-P1. It verifies that the R90B provider candidates can be carried into the current 师维备课室 shell as TeacherReviewCard payloads, using the existing edit-card surface.

It does not call provider, does not connect the page, does not modify R36/R21, and does not enter R91B.

## Key Files

- `r91a_shell_viewmodel_fixture.json`
- `teacher_review_card_viewmodel_map_1013R_R91A.json`
- `validate_1013R_R91A_shell_viewmodel_fixture_preflight_result.json`
- `r91a_shell_viewmodel_fixture_preflight_notes.md`
- `REVIEW_PACKAGE_MANIFEST.json`
- `REVIEW_PACKAGE_MANIFEST.md`

## Current Shell Baseline

```text
{rel(R36_HTML)}
```

## Status

```text
{result["final_status"]}
```
"""
    write_text(OUT / "README.md", readme)

    gpt_prompt = """# GPT Review Prompt · 1013R R91A

Please review this fixture-only R91A package.

Questions:

1. Does R91A correctly use R36 as the current prep-room shell baseline?
2. Do the R90B candidates map cleanly to TeacherReviewCard payloads?
3. Are render_slot and shell_state fields sufficient before R91B provider expansion?
4. Did this round avoid provider calls, page/UI binding, R36/R21 edits, formal apply, database, Feishu, and memory writes?
5. Is it safe to proceed to R91B multi-step provider smoke after human/GPT review?
"""
    write_text(OUT / "GPT_REVIEW_PROMPT_1013R_R91A.md", gpt_prompt)

    shutil.copy2(Path(__file__), OUT / Path(__file__).name)

    manifest_files = [
        OUT / "README.md",
        OUT / "r91a_shell_viewmodel_fixture.json",
        OUT / "teacher_review_card_viewmodel_map_1013R_R91A.json",
        OUT / "validate_1013R_R91A_shell_viewmodel_fixture_preflight_result.json",
        OUT / "r91a_shell_viewmodel_fixture_preflight_notes.md",
        OUT / "GPT_REVIEW_PROMPT_1013R_R91A.md",
        OUT / Path(__file__).name,
    ]
    manifest = {
        "stage": STAGE,
        "created_at": shell_viewmodel_fixture["created_at"],
        "status": result["status"],
        "files": [file_record(path) for path in manifest_files],
        "boundary": shell_viewmodel_fixture["boundary"],
    }
    write_json(OUT / "REVIEW_PACKAGE_MANIFEST.json", manifest)

    manifest_md = "# Review Package Manifest\n\n"
    manifest_md += f"stage={STAGE}\n\nstatus={result['status']}\n\n"
    for item in manifest["files"]:
        manifest_md += f"- `{item['path']}` sha256=`{item['sha256']}` size={item['size']}\n"
    write_text(OUT / "REVIEW_PACKAGE_MANIFEST.md", manifest_md)

    zip_base = OUT
    zip_path = shutil.make_archive(str(zip_base), "zip", OUT)
    write_json(OUT / "ZIP_SHA256.json", {
        "zip_path": rel(Path(zip_path)),
        "sha256": sha256(Path(zip_path)),
        "size": Path(zip_path).stat().st_size,
    })

    print(json.dumps({
        "stage": STAGE,
        "status": result["status"],
        "out": rel(OUT),
        "zip": rel(Path(zip_path)),
        "zip_sha256": sha256(Path(zip_path)),
    }, ensure_ascii=False, indent=2))

    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
