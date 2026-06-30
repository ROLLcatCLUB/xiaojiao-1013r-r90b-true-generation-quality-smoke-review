from __future__ import annotations

import hashlib
import json
import shutil
from datetime import datetime
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_ROOT = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
STAGE = "1013R_R93_P1_ACCEPTANCE_AND_P2_ANCHOR_GATE"
OUT_DIR = OUTPUT_ROOT / STAGE
ZIP_PATH = OUTPUT_ROOT / f"{STAGE}.zip"

P1_DIR = OUTPUT_ROOT / "1013R_R93_P1_TEACHING_LOGIC_AND_TEACHER_READABLE_DRAFT_REPAIR"
P1_VALIDATOR = P1_DIR / "validate_1013R_R93_P1_teaching_logic_teacher_readable_repair_result.json"
P1_MANIFEST = P1_DIR / "REVIEW_PACKAGE_MANIFEST.json"
P1_ZIP = OUTPUT_ROOT / "1013R_R93_P1_TEACHING_LOGIC_AND_TEACHER_READABLE_DRAFT_REPAIR.zip"

P1_GITHUB_COMMIT = "cc8405318e2de72094a70cf441d0f55fa5abe6dd"
P1_GITHUB_DIR = "r93_p1_teaching_logic_teacher_readable_repair"
REVIEW_REPO = "ROLLcatCLUB/xiaojiao-1013r-r90b-true-generation-quality-smoke-review"

BOUNDARY = {
    "accepts_r93_p1": True,
    "teacher_review_draft_ready": True,
    "final_lesson_ready": False,
    "textbook_anchor_closed": False,
    "p2_allowed_after_teacher_anchor_confirm": True,
    "r94_allowed": False,
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


def p1_raw_url(file_name: str) -> str:
    return (
        f"https://raw.githubusercontent.com/{REVIEW_REPO}/{P1_GITHUB_COMMIT}/"
        f"{P1_GITHUB_DIR}/{file_name}"
    )


def readme() -> str:
    return f"""# {STAGE}

This package closes R93-P1 as a teacher-review draft and opens only the P2 textbook-anchor closure gate.

Decision:

```text
R93-P1 = PASS
status = TEACHER_REVIEW_DRAFT_READY
quality = BASIC_USABLE
textbook_anchor = NEEDS_TEACHER_CONFIRM
final_lesson_ready = false
R94_allowed = false
```

This is a closure/gate package. It does not revise the R93-P1 teacher draft.
"""


def acceptance_decision(p1_validator: dict, p1_manifest: dict, p1_zip_sha: str) -> str:
    return f"""# R93-P1 Acceptance Decision

Decision date: 2026-06-30

## Accepted Status

```text
R93-P1 = PASS
quality_conclusion = BASIC_USABLE
status = TEACHER_REVIEW_DRAFT_READY
textbook_anchor = NEEDS_TEACHER_CONFIRM
final_lesson_ready = false
```

## Why It Can Be Closed

- R93-P1 did not continue surface-level polishing. It added textbook-anchor audit, concept-focus decision, teaching-logic diagnosis, lesson-design decision card, source gap list, and teacher-readable repair.
- R93-P1 validator is `PASS`.
- R93-P1 quality sentinel is `BASIC_USABLE`.
- R93-P1 keeps `teacher_review_required=true` and `preview_draft_only=true`.

## Why It Cannot Become Final Yet

The textbook anchor is still not closed. The confirmed textbook page, cover, or catalog evidence has not been provided in this thread. Therefore R93-P1 is a safe teacher-review draft, not a final lesson plan.

## P1 Evidence

```text
validator_pass = {p1_validator.get("validator_pass")}
quality_sentinel_v0_result = {p1_validator.get("quality_sentinel_v0_result")}
textbook_anchor_status = {p1_validator.get("textbook_anchor_status")}
concept_focus_route = {p1_validator.get("concept_focus_route")}
p1_zip_sha256 = {p1_zip_sha}
p1_manifest_zip_sha256 = {p1_manifest.get("zip_sha256")}
```

## Raw Review Links

- Validator: {p1_raw_url("validate_1013R_R93_P1_teaching_logic_teacher_readable_repair_result.json")}
- Textbook anchor audit: {p1_raw_url("textbook_anchor_audit.md")}
- Concept focus decision: {p1_raw_url("concept_focus_decision.md")}
- Teacher-readable draft: {p1_raw_url("r93_p1_teacher_readable_lesson_draft.md")}
- Source gap list: {p1_raw_url("r93_p1_source_gap_teacher_confirm_list.md")}
"""


def p2_gate_checklist() -> str:
    return """# P2 Textbook Anchor Closure Input Checklist

P2 may start only after the teacher provides enough evidence to close the anchor.

## Required Teacher Confirmation

1. Actual textbook cover or official catalog page.
2. Lesson title as printed in the textbook.
3. Grade and volume: 三年级上册 or 三年级下册.
4. Unit title and lesson sequence.
5. Textbook lesson pages or clear page screenshots.
6. Core concept confirmed by the textbook page:
   - 明度渐变
   - 纯度渐变
   - 色相渐变
   - 综合色彩连续变化
7. Classroom material choice:
   - 水粉
   - 水彩笔
   - 彩铅
   - 油画棒
   - 混合材料

## P2 Allowed Output

```text
R93-P2_TEXTBOOK_ANCHOR_CLOSURE_AND_FINAL_PREVIEW_DRAFT
```

P2 may convert R93-P1 from safe preview wording to a determined teacher-review draft. It still may not declare final formal lesson approval unless the teacher explicitly approves.
"""


def r94_hold_decision() -> str:
    return """# R94 Hold Decision

R94 is held.

Reason:

```text
Textbook anchor is not closed.
R93-P1 is teacher-review draft ready, but not final lesson ready.
Derived courseware, worksheet, rubric, or assessment generation would amplify unresolved textbook-anchor risk.
```

Blocked until:

```text
P2 closes textbook anchor and produces a determined final preview draft.
```

Current disallowed work:

- no courseware derivation
- no worksheet derivation
- no rubric derivation
- no assessment derivation
- no UI binding
- no formal apply
"""


def source_gap_summary() -> str:
    return """# Source Gap Summary For Teacher

R93-P1 can be reviewed as a safe generic draft, but these facts remain unconfirmed:

| Item | Status |
| --- | --- |
| 苏少版 / 苏教版 / 新版艺术教材 | NEEDS_TEACHER_CONFIRM |
| 2024 / 2026春 / other edition | NEEDS_TEACHER_CONFIRM |
| 三年级上册 / 三年级下册 | NEEDS_TEACHER_CONFIRM |
| 《色彩的渐变》/《色彩明度渐变》/《色彩的纯度渐变》 | NEEDS_TEACHER_CONFIRM |
| 第二单元《多彩的世界》 | NEEDS_TEACHER_CONFIRM |
| 第1课 / 第1课时 | NEEDS_TEACHER_CONFIRM |
| 教材页码 | DO_NOT_WRITE_AS_FACT |
| 后续《渐变的节奏》 | NEEDS_TEACHER_CONFIRM |
| 本课主攻明度 / 纯度 / 色相 / 综合渐变 | SOURCE_CONFLICT |

Teacher action:

```text
Provide cover/catalog/page evidence before P2.
```
"""


def gpt_review_prompt() -> str:
    return """# GPT Review Prompt - R93-P1 Acceptance And P2 Anchor Gate

Please review this package as a closure/gate decision, not as a lesson rewrite.

Check:

1. R93-P1 is accepted only as `TEACHER_REVIEW_DRAFT_READY`.
2. It does not claim `FINAL_LESSON_READY`.
3. It blocks R94 derived artifacts until textbook anchor closure.
4. It lists the minimal teacher confirmation inputs required for P2.
5. It preserves boundaries: no provider call, no field/profile changes, no R21/R36/UI/formal apply/database/Feishu/memory writes.
"""


def quality_sentinel() -> dict:
    return {
        "stage": STAGE,
        "quality_sentinel_version": "v0",
        "result": "BASIC_USABLE",
        "blocking": False,
        "teacher_review_required": True,
        "final_lesson_ready": False,
        "reasons": [
            "R93-P1 validator passed",
            "R93-P1 is appropriate as a teacher-review draft",
            "textbook anchor remains unresolved",
            "R94 is correctly held until P2 closes the anchor",
        ],
        "not_claimed": [
            "final lesson approval",
            "textbook anchor closure",
            "courseware or worksheet readiness",
            "formal apply",
        ],
    }


def validate(p1_validator: dict, p1_manifest: dict, p1_zip_sha: str) -> dict:
    failed: list[str] = []
    if p1_validator.get("status") != "PASS":
        failed.append("p1_status_not_pass")
    if not p1_validator.get("validator_pass"):
        failed.append("p1_validator_not_pass")
    if p1_validator.get("quality_sentinel_v0_result") != "BASIC_USABLE":
        failed.append("p1_quality_not_basic_usable")
    if p1_validator.get("textbook_anchor_status") != "TEXTBOOK_ANCHOR_NEEDS_TEACHER_CONFIRM":
        failed.append("p1_anchor_status_not_needs_teacher_confirm")
    if p1_manifest.get("zip_sha256") != p1_zip_sha:
        failed.append("p1_zip_sha_mismatch")
    if BOUNDARY["final_lesson_ready"]:
        failed.append("final_lesson_ready_must_be_false")
    if BOUNDARY["r94_allowed"]:
        failed.append("r94_must_be_held")

    return {
        "stage": STAGE,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "status": "PASS" if not failed else "FAIL",
        "r93_p1_status": "PASS",
        "decision": "TEACHER_REVIEW_DRAFT_READY",
        "quality": "BASIC_USABLE",
        "textbook_anchor": "NEEDS_TEACHER_CONFIRM",
        "final_lesson_ready": False,
        "p2_next_stage": "R93-P2_TEXTBOOK_ANCHOR_CLOSURE_AND_FINAL_PREVIEW_DRAFT",
        "p2_requires_teacher_anchor_evidence": True,
        "r94_allowed": False,
        "boundary": BOUNDARY,
        "p1_reference": {
            "local_dir": str(P1_DIR.relative_to(ROOT)).replace("/", "\\"),
            "github_commit": P1_GITHUB_COMMIT,
            "github_dir": P1_GITHUB_DIR,
            "zip_sha256": p1_zip_sha,
        },
        "failed_checks": failed,
        "validator_pass": not failed,
    }


def manifest_records(files: list[Path]) -> list[dict]:
    records = []
    for path in sorted(files):
        records.append(
            {
                "path": str(path.relative_to(ROOT)).replace("/", "\\"),
                "size": path.stat().st_size,
                "sha256": sha256_file(path),
            }
        )
    return records


def build_zip(files: list[Path]) -> str:
    if ZIP_PATH.exists():
        ZIP_PATH.unlink()
    with ZipFile(ZIP_PATH, "w", ZIP_DEFLATED) as zf:
        for path in sorted(files):
            zf.write(path, f"{STAGE}/{path.relative_to(OUT_DIR).as_posix()}")
    return sha256_file(ZIP_PATH)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    p1_validator = read_json(P1_VALIDATOR)
    p1_manifest = read_json(P1_MANIFEST)
    p1_zip_sha = sha256_file(P1_ZIP)

    outputs = {
        "README.md": OUT_DIR / "README.md",
        "r93_p1_acceptance_decision.md": OUT_DIR / "r93_p1_acceptance_decision.md",
        "p2_textbook_anchor_closure_input_checklist.md": OUT_DIR / "p2_textbook_anchor_closure_input_checklist.md",
        "r94_hold_decision.md": OUT_DIR / "r94_hold_decision.md",
        "source_gap_summary_for_teacher.md": OUT_DIR / "source_gap_summary_for_teacher.md",
        "GPT_REVIEW_PROMPT_1013R_R93_P1_ACCEPTANCE_AND_P2_GATE.md": OUT_DIR
        / "GPT_REVIEW_PROMPT_1013R_R93_P1_ACCEPTANCE_AND_P2_GATE.md",
        "quality_sentinel_v0_result.json": OUT_DIR / "quality_sentinel_v0_result.json",
        "validate_1013R_R93_P1_acceptance_and_p2_anchor_gate_result.json": OUT_DIR
        / "validate_1013R_R93_P1_acceptance_and_p2_anchor_gate_result.json",
    }

    write_text(outputs["README.md"], readme())
    write_text(outputs["r93_p1_acceptance_decision.md"], acceptance_decision(p1_validator, p1_manifest, p1_zip_sha))
    write_text(outputs["p2_textbook_anchor_closure_input_checklist.md"], p2_gate_checklist())
    write_text(outputs["r94_hold_decision.md"], r94_hold_decision())
    write_text(outputs["source_gap_summary_for_teacher.md"], source_gap_summary())
    write_text(outputs["GPT_REVIEW_PROMPT_1013R_R93_P1_ACCEPTANCE_AND_P2_GATE.md"], gpt_review_prompt())
    write_json(outputs["quality_sentinel_v0_result.json"], quality_sentinel())

    validation = validate(p1_validator, p1_manifest, p1_zip_sha)
    write_json(outputs["validate_1013R_R93_P1_acceptance_and_p2_anchor_gate_result.json"], validation)
    shutil.copy2(Path(__file__), OUT_DIR / Path(__file__).name)

    files = [p for p in OUT_DIR.rglob("*") if p.is_file()]
    zip_sha = build_zip([p for p in files if p.name not in {"REVIEW_PACKAGE_MANIFEST.json", "REVIEW_PACKAGE_MANIFEST.md"}])
    manifest = {
        "stage": STAGE,
        "final_status": "PASS_1013R_R93_P1_ACCEPTANCE_AND_P2_ANCHOR_GATE"
        if validation["validator_pass"]
        else "FAIL_1013R_R93_P1_ACCEPTANCE_AND_P2_ANCHOR_GATE",
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
                "decision": validation["decision"],
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
