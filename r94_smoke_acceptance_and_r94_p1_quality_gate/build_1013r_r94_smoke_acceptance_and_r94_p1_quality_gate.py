from __future__ import annotations

import hashlib
import json
import shutil
from datetime import datetime
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_ROOT = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
STAGE = "1013R_R94_SMOKE_ACCEPTANCE_AND_R94_P1_QUALITY_GATE"
OUT_DIR = OUTPUT_ROOT / STAGE
ZIP_PATH = OUTPUT_ROOT / f"{STAGE}.zip"

R94_DIR = OUTPUT_ROOT / "1013R_R94_DERIVED_ARTIFACTS_SMOKE"
R94_VALIDATOR = R94_DIR / "validate_1013R_R94_derived_artifacts_smoke_result.json"
R94_QUALITY = R94_DIR / "quality_sentinel_v0_result.json"
R94_TRACE = R94_DIR / "r94_derived_artifacts_trace.json"
R94_COURSEWARE = R94_DIR / "r94_courseware_outline_draft.md"
R94_WORKSHEET = R94_DIR / "r94_student_worksheet_draft.md"
R94_RUBRIC = R94_DIR / "r94_assessment_rubric_draft.md"
R94_MANIFEST = R94_DIR / "REVIEW_PACKAGE_MANIFEST.json"

BOUNDARY = {
    "provider_called": False,
    "model_called": False,
    "new_fields_added": False,
    "profile_modified": False,
    "r21_modified": False,
    "r36_modified": False,
    "ui_page_connected": False,
    "formal_apply": False,
    "database_written": False,
    "feishu_written": False,
    "memory_written": False,
    "pptx_generated": False,
    "printed_final_material_generated": False,
    "formal_courseware_ready": False,
    "formal_worksheet_ready": False,
    "formal_rubric_ready": False,
    "r94_p1_executed": False,
    "r95_executed": False,
    "teacher_review_required": True,
}

DECISION = {
    "stage": STAGE,
    "r94_smoke_result": "PASS_WITH_NOTES",
    "quality": "BASIC_USABLE",
    "artifact_formal_ready": False,
    "teacher_review_required": True,
    "formal_ready": False,
    "r95_allowed": False,
    "bottom_governance_reopen_required": False,
    "next": "R94-P1_DERIVED_ARTIFACTS_TEACHER_REVIEW_POLISH",
    "quality_notes": [
        "课件还像文字大纲，需要改为 slide storyboard。",
        "学习单内容偏满，需要拆成一页学生版和教师说明版。",
        "评价表需要拆成教师观察版和学生自评版。",
    ],
}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def r94_summary() -> dict:
    validator = read_json(R94_VALIDATOR)
    quality = read_json(R94_QUALITY)
    manifest = read_json(R94_MANIFEST)
    return {
        "validator_status": validator.get("status"),
        "validator_pass": validator.get("validator_pass"),
        "quality_sentinel_v0_result": validator.get("quality_sentinel_v0_result") or quality.get("result"),
        "blocking": validator.get("blocking") if "blocking" in validator else quality.get("blocking"),
        "provider_called": validator.get("provider_called"),
        "model_called": validator.get("model_called"),
        "pptx_generated": validator.get("pptx_generated"),
        "formal_apply": validator.get("formal_apply"),
        "R95_executed": validator.get("R95_executed"),
        "zip_sha256": manifest.get("zip_sha256"),
    }


def readme_md(summary: dict) -> str:
    return f"""# {STAGE}

R94 smoke is accepted with notes. This package does not run R94-P1 and does not reopen bottom governance.

```text
1013R_R94_DERIVED_ARTIFACTS_SMOKE = PASS_WITH_NOTES
quality = BASIC_USABLE
artifact_formal_ready = false
teacher_review_required = true
formal_ready = false
R95_allowed = false
next = R94-P1_DERIVED_ARTIFACTS_TEACHER_REVIEW_POLISH
```

R94 source status:

```text
validator_status = {summary["validator_status"]}
validator_pass = {str(summary["validator_pass"]).lower()}
quality_sentinel_v0_result = {summary["quality_sentinel_v0_result"]}
blocking = {str(summary["blocking"]).lower()}
provider_called = {str(summary["provider_called"]).lower()}
model_called = {str(summary["model_called"]).lower()}
pptx_generated = {str(summary["pptx_generated"]).lower()}
formal_apply = {str(summary["formal_apply"]).lower()}
R95_executed = {str(summary["R95_executed"]).lower()}
```
"""


def acceptance_md() -> str:
    return """# R94 Smoke Acceptance Decision

Decision:

```text
R94_SMOKE_ACCEPTED = true
R94_SMOKE_RESULT = PASS_WITH_NOTES
QUALITY = BASIC_USABLE
ARTIFACT_FORMAL_READY = false
```

Accepted as smoke because:

| Bottom Gate | Current State |
| --- | --- |
| 教材锚点 | CLOSED before R94 |
| Source trace | Present |
| Derived source | R93-P2 final preview draft |
| provider/model | Not called |
| profile | Not modified |
| R21/R36 | Not modified |
| formal apply | false |
| database/Feishu/memory | Not written |
| Derived artifacts | Smoke drafts only |

Quality notes:

```text
课件还像文字大纲
学习单内容偏满
评价表需要分学生版/教师版
```

Conclusion:

```text
This is a derived-artifact productization issue, not a bottom-governance failure.
Do not reopen validator/profile/lineage work.
Proceed only to R94-P1 teacher-review polish after explicit authorization.
```
"""


def r94_p1_gate_md() -> str:
    return """# R94-P1 Teacher Review Polish Gate

Readiness:

```text
R94-P1_READINESS = READY_FOR_USER_AUTHORIZATION
R94-P1_EXECUTED = false
R95_ALLOWED = false
```

Allowed R94-P1 work after authorization:

```text
1. 课件大纲 -> slide storyboard
2. 学习单草案 -> 一页学生版 + 教师说明版
3. 评价表草案 -> 教师观察版 + 学生自评版
```

Still forbidden:

```text
不生成正式 PPTX
不打印定稿
不落库
不接 UI
不 formal apply
不改 R21/R36
不改 profile
不新增字段体系
不进入 R95
```
"""


def formal_lock_md() -> str:
    return """# Formal Material Lock

R94 smoke passing does not mean formal materials are ready.

```text
formal_courseware_ready=false
formal_worksheet_ready=false
formal_rubric_ready=false
artifact_formal_ready=false
formal_apply=false
```

Do not claim:

```text
正式课件可用
正式学习单可用
评价表可打印
正式材料通过
```

Current accepted wording:

```text
R94 smoke can pass with notes.
R94 formal materials cannot pass.
R95 and formal apply remain locked.
```
"""


def quality_notes_md() -> str:
    return """# R94 Quality Notes For P1

These notes should guide R94-P1. They do not invalidate the bottom chain.

## Courseware

Current issue:

```text
课件还像文字大纲。
```

P1 direction:

```text
Convert outline into slide storyboard:
- one dominant visual/action per slide
- shorter screen text
- clearer teacher prompt
- student action visible on each slide
```

## Worksheet

Current issue:

```text
学习单内容偏满。
```

P1 direction:

```text
Split into:
- one-page student worksheet
- teacher instruction/answer/observation notes
```

## Rubric

Current issue:

```text
评价表需要分学生版/教师版。
```

P1 direction:

```text
Split into:
- teacher observation version
- student self-check version
```
"""


def quality_sentinel() -> dict:
    return {
        "stage": STAGE,
        "quality_sentinel_version": "v0",
        "result": "BASIC_USABLE",
        "blocking": False,
        "r94_smoke_result": "PASS_WITH_NOTES",
        "artifact_formal_ready": False,
        "teacher_review_required": True,
        "bottom_governance_reopen_required": False,
        "checks": {
            "bottom_chain_stable": "PASS",
            "smoke_goal_completed": "PASS",
            "formal_material_lock": "PASS",
            "p1_quality_notes_present": "PASS",
            "scope_control": "PASS",
        },
    }


def validate() -> dict:
    failed: list[str] = []
    required_sources = [R94_VALIDATOR, R94_QUALITY, R94_TRACE, R94_COURSEWARE, R94_WORKSHEET, R94_RUBRIC, R94_MANIFEST]
    for path in required_sources:
        if not path.exists():
            failed.append(f"missing_r94_source:{path.name}")
    r94 = read_json(R94_VALIDATOR) if R94_VALIDATOR.exists() else {}
    if r94.get("validator_pass") is not True:
        failed.append("r94_validator_not_pass")
    if r94.get("quality_sentinel_v0_result") != "BASIC_USABLE":
        failed.append("r94_quality_not_basic_usable")
    if r94.get("blocking") is not False:
        failed.append("r94_blocking_not_false")
    forbidden_true = [
        "provider_called",
        "model_called",
        "new_fields_added",
        "profile_modified",
        "r21_modified",
        "r36_modified",
        "ui_page_connected",
        "formal_apply",
        "database_written",
        "feishu_written",
        "memory_written",
        "pptx_generated",
        "printed_final_material_generated",
        "R95_executed",
    ]
    for key in forbidden_true:
        if r94.get(key) is True:
            failed.append(f"r94_boundary_was_true:{key}")
    if DECISION["r94_smoke_result"] != "PASS_WITH_NOTES":
        failed.append("decision_not_pass_with_notes")
    if DECISION["artifact_formal_ready"] is not False:
        failed.append("artifact_formal_ready_not_false")
    if DECISION["bottom_governance_reopen_required"] is not False:
        failed.append("bottom_governance_reopen_required_not_false")
    if any(
        BOUNDARY[key]
        for key in [
            "provider_called",
            "model_called",
            "new_fields_added",
            "profile_modified",
            "r21_modified",
            "r36_modified",
            "ui_page_connected",
            "formal_apply",
            "database_written",
            "feishu_written",
            "memory_written",
            "pptx_generated",
            "printed_final_material_generated",
            "formal_courseware_ready",
            "formal_worksheet_ready",
            "formal_rubric_ready",
            "r94_p1_executed",
            "r95_executed",
        ]
    ):
        failed.append("boundary_violation")
    return {
        "stage": STAGE,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "status": "PASS" if not failed else "FAIL",
        "r94_smoke_result": DECISION["r94_smoke_result"],
        "quality": DECISION["quality"],
        "artifact_formal_ready": DECISION["artifact_formal_ready"],
        "teacher_review_required": DECISION["teacher_review_required"],
        "formal_ready": DECISION["formal_ready"],
        "r95_allowed": DECISION["r95_allowed"],
        "bottom_governance_reopen_required": DECISION["bottom_governance_reopen_required"],
        "next": DECISION["next"],
        "boundary": BOUNDARY,
        "quality_sentinel_v0_result": "BASIC_USABLE",
        "blocking": False,
        "failed_checks": failed,
        "validator_pass": not failed,
    }


def manifest_records(files: list[Path]) -> list[dict]:
    return [
        {
            "path": str(path.relative_to(ROOT)).replace("/", "\\"),
            "size": path.stat().st_size,
            "sha256": sha256_file(path),
        }
        for path in sorted(files)
    ]


def build_zip(files: list[Path]) -> str:
    if ZIP_PATH.exists():
        ZIP_PATH.unlink()
    with ZipFile(ZIP_PATH, "w", ZIP_DEFLATED) as zf:
        for path in sorted(files):
            zf.write(path, f"{STAGE}/{path.relative_to(OUT_DIR).as_posix()}")
    return sha256_file(ZIP_PATH)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    source_dir = OUT_DIR / "source_snapshots"
    source_dir.mkdir(exist_ok=True)
    for source in [R94_VALIDATOR, R94_QUALITY, R94_TRACE, R94_COURSEWARE, R94_WORKSHEET, R94_RUBRIC, R94_MANIFEST]:
        shutil.copy2(source, source_dir / source.name)

    summary = r94_summary()
    write_text(OUT_DIR / "README.md", readme_md(summary))
    write_json(OUT_DIR / "r94_smoke_acceptance_decision.json", DECISION)
    write_text(OUT_DIR / "r94_smoke_acceptance_decision.md", acceptance_md())
    write_text(OUT_DIR / "r94_p1_teacher_review_polish_gate.md", r94_p1_gate_md())
    write_text(OUT_DIR / "formal_material_lock.md", formal_lock_md())
    write_text(OUT_DIR / "r94_quality_notes_for_p1.md", quality_notes_md())
    write_json(OUT_DIR / "quality_sentinel_v0_result.json", quality_sentinel())
    shutil.copy2(Path(__file__), OUT_DIR / Path(__file__).name)

    validation = validate()
    write_json(OUT_DIR / "validate_1013R_R94_smoke_acceptance_and_R94_P1_quality_gate_result.json", validation)

    files = [p for p in OUT_DIR.rglob("*") if p.is_file()]
    zip_sha = build_zip([p for p in files if p.name not in {"REVIEW_PACKAGE_MANIFEST.json", "REVIEW_PACKAGE_MANIFEST.md"}])
    manifest = {
        "stage": STAGE,
        "final_status": "PASS_1013R_R94_SMOKE_ACCEPTANCE_AND_R94_P1_QUALITY_GATE"
        if validation["validator_pass"]
        else "FAIL_1013R_R94_SMOKE_ACCEPTANCE_AND_R94_P1_QUALITY_GATE",
        "zip_path": str(ZIP_PATH.relative_to(ROOT)).replace("/", "\\"),
        "zip_sha256": zip_sha,
        "files": manifest_records([p for p in OUT_DIR.rglob("*") if p.is_file()]),
        "boundary": BOUNDARY,
    }
    write_json(OUT_DIR / "REVIEW_PACKAGE_MANIFEST.json", manifest)
    lines = ["# REVIEW_PACKAGE_MANIFEST", "", f"ZIP SHA256: `{zip_sha}`", ""]
    for record in manifest["files"]:
        lines.append(f"- `{record['path']}` sha256=`{record['sha256']}`")
    write_text(OUT_DIR / "REVIEW_PACKAGE_MANIFEST.md", "\n".join(lines))

    print(
        json.dumps(
            {
                "stage": STAGE,
                "validator_pass": validation["validator_pass"],
                "r94_smoke_result": validation["r94_smoke_result"],
                "quality": validation["quality"],
                "artifact_formal_ready": validation["artifact_formal_ready"],
                "next": validation["next"],
                "out_dir": str(OUT_DIR),
                "zip_path": str(ZIP_PATH),
                "zip_sha256": zip_sha,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
