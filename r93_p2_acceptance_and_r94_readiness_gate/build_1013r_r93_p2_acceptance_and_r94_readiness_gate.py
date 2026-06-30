from __future__ import annotations

import hashlib
import json
import shutil
from datetime import datetime
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_ROOT = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
STAGE = "1013R_R93_P2_ACCEPTANCE_AND_R94_READINESS_GATE"
OUT_DIR = OUTPUT_ROOT / STAGE
ZIP_PATH = OUTPUT_ROOT / f"{STAGE}.zip"

P2_DIR = OUTPUT_ROOT / "1013R_R93_P2_TEXTBOOK_ANCHOR_CLOSURE_AND_FINAL_PREVIEW_DRAFT"
P2_VALIDATOR = P2_DIR / "validate_1013R_R93_P2_textbook_anchor_closure_final_preview_draft_result.json"
P2_DRAFT = P2_DIR / "r93_p2_final_preview_lesson_draft.md"
P2_ANCHOR = P2_DIR / "textbook_anchor_closure.md"
P2_KB_EVIDENCE = P2_DIR / "kb_evidence_notes.md"
P2_MANIFEST = P2_DIR / "REVIEW_PACKAGE_MANIFEST.json"

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
    "r94_executed": False,
    "courseware_generated": False,
    "worksheet_generated": False,
    "rubric_generated": False,
    "ppt_generated": False,
    "teacher_review_required": True,
}

GATE = {
    "stage": STAGE,
    "r93_p2_acceptance": "PASS",
    "textbook_anchor": "CLOSED",
    "current_status": "FINAL_PREVIEW_DRAFT_READY",
    "quality": "BASIC_USABLE",
    "formal_lesson_ready": False,
    "r94_allowed": False,
    "r94_authorization_status": "PENDING_USER_AUTHORIZATION",
    "r94_allowed_after_user_authorization": True,
    "r94_scope_after_authorization": "DERIVED_ARTIFACTS_SMOKE_ONLY",
    "r94_first_smoke_outputs_allowed": [
        "courseware_outline_draft_only",
        "worksheet_draft_only",
        "rubric_draft_only",
    ],
    "r94_first_smoke_outputs_not_allowed": [
        "formal_ppt_generation",
        "print_ready_worksheet",
        "database_rubric_write",
        "r21_or_r36_update",
        "ui_binding",
        "formal_apply",
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


def p2_summary() -> dict:
    validator = read_json(P2_VALIDATOR)
    manifest = read_json(P2_MANIFEST)
    return {
        "validator_status": validator.get("status"),
        "validator_pass": validator.get("validator_pass"),
        "textbook_anchor_closed": validator.get("textbook_anchor_closed"),
        "anchor_status": validator.get("anchor_status"),
        "unit": validator.get("unit"),
        "lesson_sequence": validator.get("lesson_sequence"),
        "lesson_title": validator.get("lesson_title"),
        "page_range": validator.get("page_range"),
        "quality_sentinel_v0_result": validator.get("quality_sentinel_v0_result"),
        "final_preview_draft_ready": validator.get("final_preview_draft_ready"),
        "final_formal_lesson_ready": validator.get("final_formal_lesson_ready"),
        "r94_allowed": validator.get("r94_allowed"),
        "p2_zip_sha256": manifest.get("zip_sha256"),
    }


def readme_md(summary: dict) -> str:
    return f"""# {STAGE}

This package records acceptance of R93-P2 and opens a readiness gate for a future R94 derived-artifacts smoke.

It does not execute R94.

```text
R93-P2 = PASS
教材锚点 = CLOSED
状态 = FINAL_PREVIEW_DRAFT_READY
质量 = BASIC_USABLE
formal_lesson_ready = false
R94_allowed = false
R94_authorization_status = PENDING_USER_AUTHORIZATION
```

P2 source:

```text
unit = {summary["unit"]}
lesson = {summary["lesson_sequence"]}《{summary["lesson_title"]}》
page_range = {summary["page_range"]}
p2_zip_sha256 = {summary["p2_zip_sha256"]}
```
"""


def acceptance_decision_md(summary: dict) -> str:
    return f"""# R93-P2 Acceptance Decision

Decision:

```text
R93-P2_ACCEPTED = true
```

Accepted state:

```text
R93-P2 = PASS
教材锚点 = CLOSED
状态 = FINAL_PREVIEW_DRAFT_READY
质量 = BASIC_USABLE
formal_lesson_ready = false
R94_allowed = false
```

Evidence:

| Item | Value |
| --- | --- |
| P2 validator | {summary["validator_status"]} |
| P2 validator pass | {str(summary["validator_pass"]).lower()} |
| Textbook anchor closed | {str(summary["textbook_anchor_closed"]).lower()} |
| Anchor status | {summary["anchor_status"]} |
| Unit | {summary["unit"]} |
| Lesson | {summary["lesson_sequence"]}《{summary["lesson_title"]}》 |
| Page range | {summary["page_range"]} |
| Quality | {summary["quality_sentinel_v0_result"]} |
| Final preview draft ready | {str(summary["final_preview_draft_ready"]).lower()} |
| Formal lesson ready | {str(summary["final_formal_lesson_ready"]).lower()} |
| R94 allowed in P2 | {str(summary["r94_allowed"]).lower()} |

Acceptance rationale:

```text
The core textbook identity is no longer a source gap.
P2 can be used as the mother draft for downstream derived-artifact smoke.
P2 is still not a formal lesson apply artifact.
```
"""


def r94_readiness_gate_md() -> str:
    return """# R94 Readiness Gate

Decision:

```text
R94_READINESS = READY_FOR_USER_AUTHORIZATION
R94_EXECUTED = false
R94_ALLOWED_NOW = false
```

Rationale:

```text
P2 has closed the textbook anchor and produced a final preview draft.
This satisfies the prerequisite for planning a derived-artifacts smoke.
However, P2 package explicitly kept r94_allowed=false, so R94 must not start automatically.
```

Authorization state:

```text
r94_authorization_status = PENDING_USER_AUTHORIZATION
r94_allowed_after_user_authorization = true
```

If authorized, R94 may only run:

```text
R94_DERIVED_ARTIFACTS_SMOKE
```

R94 may not do:

```text
formal_apply
R21/R36 modification
UI binding
database write
Feishu write
memory write
formal PPT generation
print-ready worksheet
rubric database write
```
"""


def r94_scope_md() -> str:
    return """# R94 Derived-Artifacts Smoke Scope

Allowed first smoke outputs:

```text
1. 课件大纲草案，不生成正式 PPT
2. 学习单草案，不打印定稿
3. 评价表 / rubric 草案，不落库
```

Required flags:

```text
teacher_review_required = true
formal_apply = false
r21_modified = false
r36_modified = false
ui_page_connected = false
database_written = false
feishu_written = false
memory_written = false
```

Quality principle:

```text
Keep R94 light.
Derive only from R93-P2 final preview draft and source evidence.
Do not expand into full courseware production.
Do not call provider unless a later explicit R94 plan says so.
```

Suggested R94 output files:

```text
courseware_outline_draft.md
student_worksheet_draft.md
rubric_draft.md
quality_sentinel_v0_result.json
validate_1013R_R94_derived_artifacts_smoke_result.json
```
"""


def boundary_md() -> str:
    return """# Boundary Confirmation

This acceptance/readiness gate is declarative only.

```text
provider_called=false
model_called=false
new_fields_added=false
profile_modified=false
r21_modified=false
r36_modified=false
ui_page_connected=false
formal_apply=false
database_written=false
feishu_written=false
memory_written=false
r94_executed=false
courseware_generated=false
worksheet_generated=false
rubric_generated=false
ppt_generated=false
```

The only state change in this package is review-line status documentation:

```text
R93-P2 accepted
R94 readiness = pending user authorization
```
"""


def quality_sentinel() -> dict:
    return {
        "stage": STAGE,
        "quality_sentinel_version": "v0",
        "result": "BASIC_USABLE",
        "blocking": False,
        "teacher_review_required": True,
        "r93_p2_accepted": True,
        "textbook_anchor_closed": True,
        "r94_readiness": "READY_FOR_USER_AUTHORIZATION",
        "r94_allowed": False,
        "formal_lesson_ready": False,
        "notes": [
            "P2 can be closed as final preview draft.",
            "R94 may be planned only after explicit user authorization.",
            "Future R94 must remain derived-artifacts smoke only.",
        ],
    }


def validate() -> dict:
    failed: list[str] = []
    if not P2_VALIDATOR.exists():
        failed.append("missing_p2_validator")
        p2 = {}
    else:
        p2 = read_json(P2_VALIDATOR)
    if p2.get("validator_pass") is not True:
        failed.append("p2_validator_not_pass")
    if p2.get("textbook_anchor_closed") is not True:
        failed.append("p2_textbook_anchor_not_closed")
    if p2.get("final_preview_draft_ready") is not True:
        failed.append("p2_final_preview_not_ready")
    if p2.get("final_formal_lesson_ready") is not False:
        failed.append("p2_formal_lesson_ready_should_be_false")
    if p2.get("r94_allowed") is not False:
        failed.append("p2_r94_allowed_should_be_false")
    for path in [P2_DRAFT, P2_ANCHOR, P2_KB_EVIDENCE, P2_MANIFEST]:
        if not path.exists():
            failed.append(f"missing_p2_source:{path.name}")
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
            "r94_executed",
            "courseware_generated",
            "worksheet_generated",
            "rubric_generated",
            "ppt_generated",
        ]
    ):
        failed.append("boundary_violation")
    return {
        "stage": STAGE,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "status": "PASS" if not failed else "FAIL",
        "r93_p2_acceptance": GATE["r93_p2_acceptance"],
        "textbook_anchor": GATE["textbook_anchor"],
        "current_status": GATE["current_status"],
        "quality": GATE["quality"],
        "formal_lesson_ready": GATE["formal_lesson_ready"],
        "r94_allowed": GATE["r94_allowed"],
        "r94_authorization_status": GATE["r94_authorization_status"],
        "r94_allowed_after_user_authorization": GATE["r94_allowed_after_user_authorization"],
        "r94_scope_after_authorization": GATE["r94_scope_after_authorization"],
        "boundary": BOUNDARY,
        "p2_summary": p2_summary() if P2_VALIDATOR.exists() and P2_MANIFEST.exists() else {},
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

    for source in [P2_VALIDATOR, P2_DRAFT, P2_ANCHOR, P2_KB_EVIDENCE, P2_MANIFEST]:
        shutil.copy2(source, source_dir / source.name)

    summary = p2_summary()
    write_text(OUT_DIR / "README.md", readme_md(summary))
    write_json(OUT_DIR / "r93_p2_acceptance_and_r94_readiness_gate.json", GATE)
    write_text(OUT_DIR / "r93_p2_acceptance_decision.md", acceptance_decision_md(summary))
    write_text(OUT_DIR / "r94_readiness_gate.md", r94_readiness_gate_md())
    write_text(OUT_DIR / "r94_derived_artifacts_smoke_scope.md", r94_scope_md())
    write_text(OUT_DIR / "r94_boundary_confirmation.md", boundary_md())
    write_json(OUT_DIR / "quality_sentinel_v0_result.json", quality_sentinel())
    shutil.copy2(Path(__file__), OUT_DIR / Path(__file__).name)

    validation = validate()
    write_json(OUT_DIR / "validate_1013R_R93_P2_acceptance_and_R94_readiness_gate_result.json", validation)

    files = [p for p in OUT_DIR.rglob("*") if p.is_file()]
    zip_sha = build_zip([p for p in files if p.name not in {"REVIEW_PACKAGE_MANIFEST.json", "REVIEW_PACKAGE_MANIFEST.md"}])
    manifest = {
        "stage": STAGE,
        "final_status": "PASS_1013R_R93_P2_ACCEPTANCE_AND_R94_READINESS_GATE"
        if validation["validator_pass"]
        else "FAIL_1013R_R93_P2_ACCEPTANCE_AND_R94_READINESS_GATE",
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
                "r93_p2_acceptance": validation["r93_p2_acceptance"],
                "r94_authorization_status": validation["r94_authorization_status"],
                "r94_allowed": validation["r94_allowed"],
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
