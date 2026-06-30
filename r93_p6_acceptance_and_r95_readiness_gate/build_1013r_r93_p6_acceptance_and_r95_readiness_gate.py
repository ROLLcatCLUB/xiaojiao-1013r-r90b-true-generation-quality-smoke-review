from __future__ import annotations

import hashlib
import json
import re
import shutil
from datetime import datetime
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
STAGE = "1013R_R93_P6_ACCEPTANCE_AND_R95_READINESS_GATE"
OUT = BASE / STAGE
ZIP_PATH = BASE / f"{STAGE}.zip"

P6_DIR = BASE / "1013R_R93_P6_TEACHER_NAVIGATION_VIEW_AND_TALK_FLOW"
P6_HTML = P6_DIR / "r93_p6_teacher_navigation_view.html"
P6_VIEWMODEL = P6_DIR / "r93_p6_teacher_navigation_viewmodel.json"
P6_TALK_FLOW = P6_DIR / "r93_p6_talk_flow_summary.md"
P6_NOTES = P6_DIR / "r93_p6_reading_experience_notes.md"
P6_VALIDATOR = P6_DIR / "validate_1013R_R93_P6_teacher_navigation_view_result.json"

P5_DIR = BASE / "1013R_R93_P5_TEACHER_EXECUTION_MAP_AND_CHILD_LANGUAGE_REPAIR"
P5_VALIDATOR = P5_DIR / "validate_1013R_R93_P5_teacher_execution_map_child_language_result.json"
P5_MAP = P5_DIR / "r93_p5_teacher_execution_map.json"

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
    "pdf_generated": False,
    "docx_generated": False,
    "printed_final_material_generated": False,
    "r95_executed": False,
}

DECISION = {
    "stage": STAGE,
    "r93_p6_result": "PASS_WITH_NOTES",
    "teacher_default_reading_page_ready": True,
    "reading_hierarchy_accepted": True,
    "quality": "BASIC_USABLE",
    "formal_ready": False,
    "r95_allowed_now": False,
    "r95_authorization_status": "PENDING_USER_AUTHORIZATION",
    "next": "R95_STATIC_ARTIFACT_EXPORT_PREVIEW_AFTER_USER_AUTHORIZATION",
    "notes": [
        "P6 can be accepted as the current teacher default reading surface.",
        "Do not keep looping on reading hierarchy before R95.",
        "Some teacher-three-step summaries should be polished during R95 preview preparation.",
        "R95 remains locked until user authorization.",
    ],
}


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT)).replace("/", "\\")


def first_screen_text(html_text: str) -> str:
    match = re.search(r"<!-- FIRST_SCREEN_START -->(.*?)<!-- FIRST_SCREEN_END -->", html_text, re.S)
    if not match:
        return ""
    text = re.sub(r"<[^>]+>", " ", match.group(1))
    return re.sub(r"\s+", " ", text).strip()


def source_summary() -> dict:
    p6_validator = read_json(P6_VALIDATOR)
    viewmodel = read_json(P6_VIEWMODEL)
    return {
        "p6_status": p6_validator.get("status"),
        "p6_validator_pass": p6_validator.get("validator_pass"),
        "episode_count": p6_validator.get("episode_count"),
        "default_view_episode_blocks": p6_validator.get("default_view_episode_blocks"),
        "micro_steps_folded": p6_validator.get("micro_steps_folded"),
        "first_screen_exposes_micro_steps": p6_validator.get("first_screen_exposes_micro_steps"),
        "html_sha256": p6_validator.get("html_sha256"),
        "viewmodel_sha256": p6_validator.get("viewmodel_sha256"),
        "lesson": viewmodel.get("lesson", {}),
        "micro_step_count": viewmodel.get("source", {}).get("micro_step_count"),
        "reading_model": viewmodel.get("reading_model", {}),
    }


def readme_md(summary: dict) -> str:
    return f"""# {STAGE}

This gate accepts R93-P6 as the current teacher default reading page and prepares a locked readiness gate for R95 static export preview.

```text
R93-P6 = PASS_WITH_NOTES
teacher_default_reading_page_ready = true
quality = BASIC_USABLE
formal_ready = false
R95_allowed_now = false
R95_authorization_status = PENDING_USER_AUTHORIZATION
```

Source:

```text
P6 HTML = {rel(P6_HTML)}
P6 validator = {summary["p6_status"]}
episode_count = {summary["episode_count"]}
default_view_episode_blocks = {summary["default_view_episode_blocks"]}
micro_steps_folded = {str(summary["micro_steps_folded"]).lower()}
first_screen_exposes_micro_steps = {str(summary["first_screen_exposes_micro_steps"]).lower()}
```
"""


def acceptance_decision_md(summary: dict) -> str:
    return f"""# R93-P6 Acceptance Decision

Decision:

```text
R93-P6 教师课堂导航版 = PASS_WITH_NOTES
可以作为当前教师默认阅读页阶段性收口
可以进入下一步
不需要再卡在阅读层级上反复修
```

Accepted evidence:

| Check | Value |
| --- | --- |
| P6 validator | {summary["p6_status"]} |
| validator_pass | {str(summary["p6_validator_pass"]).lower()} |
| first_screen_exposes_micro_steps | {str(summary["first_screen_exposes_micro_steps"]).lower()} |
| default_view_episode_blocks | {summary["default_view_episode_blocks"]} |
| micro_steps_folded | {str(summary["micro_steps_folded"]).lower()} |
| episode_count | {summary["episode_count"]} |
| micro_step_count retained | {summary["micro_step_count"]} |

Teacher reading conclusion:

```text
第一屏不再直接铺 29 个 micro-step。
先显示本课教师话术总览。
每个环节默认只显示老师三步、学生产出、关键话术、小教提醒。
micro-step、支架、小教、证据都折叠保留。
```

Status boundary:

```text
正式文件未生成
正式应用未开放
R95 未执行
R95 仍需用户授权
```
"""


def r95_readiness_gate_md() -> str:
    return """# R95 Export Preview Readiness Gate

Decision:

```text
R95_READINESS = READY_FOR_USER_AUTHORIZATION
R95_ALLOWED_NOW = false
R95_EXECUTED = false
```

Why R95 can be prepared next:

```text
P6 has solved the basic teacher reading hierarchy.
The next risk is no longer "how the teacher reads the lesson".
The next risk is whether classroom materials can be exported into previewable teacher-facing files.
```

Allowed R95 scope after explicit user authorization:

```text
PPTX preview
A4 学习单 preview
A4 教师观察表 / 学生自评表 preview
```

Still forbidden:

```text
不 formal apply
不写 R21/R36
不落库
不接真实 UI
不进入正式发布
不把预览文件标记为正式可用
```

Required R95 posture:

```text
preview only
teacher_review_required = true
formal_apply = false
```
"""


def quality_notes_md() -> str:
    return """# R93-P6 Quality Notes For R95

These notes should travel into R95. They do not block P6 acceptance.

## 1. Teacher Three-Step Summary Polish

Some auto summaries are structurally useful but not yet natural enough.

Example to fix during R95 preparation:

```text
Current:
先拿出三格小样纸 / 再画第三格 / 最后巡视并点拨

Preferred:
1. 示范三格渐变小样
2. 对比自然渐变和跳色反例
3. 让学生试做并巡视点拨
```

Principle:

```text
The teacher first sees a smooth teaching route, not raw micro-step compression.
```

## 2. Xiaojiao Placement

P6 can keep one Xiaojiao reminder inside the default view.

For shell/R95 preview, Xiaojiao should feel like a light side assistant:

```text
主流程优先显示教师动作。
学生动作次级显示。
小教、支架、证据继续折叠或侧栏化。
```

## 3. R95 Preview Files

R95 should validate export readability, not formal release:

```text
PPTX preview only
A4 worksheet preview only
A4 rubric/self-check preview only
teacher_review_required=true
formal_apply=false
```
"""


def boundary_md() -> str:
    return """# Boundary Confirmation

This gate is declarative. It does not execute R95.

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
pptx_generated=false
pdf_generated=false
docx_generated=false
printed_final_material_generated=false
r95_executed=false
```
"""


def quality_sentinel() -> dict:
    return {
        "stage": STAGE,
        "quality_sentinel_version": "v1_preview",
        "result": "BASIC_USABLE",
        "blocking": False,
        "r93_p6_result": "PASS_WITH_NOTES",
        "teacher_default_reading_page_ready": True,
        "r95_readiness": "READY_FOR_USER_AUTHORIZATION",
        "r95_allowed_now": False,
        "teacher_review_required": True,
        "formal_apply": False,
        "notes": DECISION["notes"],
    }


def validate() -> dict:
    failed: list[str] = []
    required = [P6_HTML, P6_VIEWMODEL, P6_TALK_FLOW, P6_NOTES, P6_VALIDATOR, P5_VALIDATOR, P5_MAP]
    for path in required:
        if not path.exists():
            failed.append(f"missing_source:{path.name}")

    p6_validator = read_json(P6_VALIDATOR) if P6_VALIDATOR.exists() else {}
    html_text = P6_HTML.read_text(encoding="utf-8") if P6_HTML.exists() else ""
    first_text = first_screen_text(html_text)

    if p6_validator.get("validator_pass") is not True:
        failed.append("p6_validator_not_pass")
    if p6_validator.get("status") != "PASS":
        failed.append("p6_status_not_pass")
    if p6_validator.get("episode_count") != 5:
        failed.append("p6_episode_count_not_5")
    if p6_validator.get("default_view_episode_blocks") != 5:
        failed.append("default_view_episode_blocks_not_5")
    if p6_validator.get("micro_steps_folded") is not True:
        failed.append("micro_steps_not_folded")
    if p6_validator.get("first_screen_exposes_micro_steps") is not False:
        failed.append("first_screen_exposes_micro_steps")
    if "本课教师话术总览" not in html_text:
        failed.append("teacher_talk_overview_missing")
    for phrase in ["engineering_key", "canonical", "R88-GEN", "22 字段", "14 字段", "47 字段"]:
        if phrase in first_text:
            failed.append(f"first_screen_exposes_engineering_field:{phrase}")
    for key, value in BOUNDARY.items():
        if value is True:
            failed.append(f"boundary_violation:{key}")

    return {
        "stage": STAGE,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "status": "PASS" if not failed else "FAIL",
        "r93_p6_result": DECISION["r93_p6_result"],
        "teacher_default_reading_page_ready": DECISION["teacher_default_reading_page_ready"],
        "reading_hierarchy_accepted": DECISION["reading_hierarchy_accepted"],
        "quality": DECISION["quality"],
        "formal_ready": DECISION["formal_ready"],
        "r95_allowed_now": DECISION["r95_allowed_now"],
        "r95_authorization_status": DECISION["r95_authorization_status"],
        "next": DECISION["next"],
        "provider_called": BOUNDARY["provider_called"],
        "model_called": BOUNDARY["model_called"],
        "new_fields_added": BOUNDARY["new_fields_added"],
        "profile_modified": BOUNDARY["profile_modified"],
        "r21_modified": BOUNDARY["r21_modified"],
        "r36_modified": BOUNDARY["r36_modified"],
        "ui_page_connected": BOUNDARY["ui_page_connected"],
        "formal_apply": BOUNDARY["formal_apply"],
        "database_written": BOUNDARY["database_written"],
        "feishu_written": BOUNDARY["feishu_written"],
        "memory_written": BOUNDARY["memory_written"],
        "pptx_generated": BOUNDARY["pptx_generated"],
        "pdf_generated": BOUNDARY["pdf_generated"],
        "docx_generated": BOUNDARY["docx_generated"],
        "printed_final_material_generated": BOUNDARY["printed_final_material_generated"],
        "r95_executed": BOUNDARY["r95_executed"],
        "source_summary": source_summary() if P6_VALIDATOR.exists() and P6_VIEWMODEL.exists() else {},
        "failed_checks": failed,
        "validator_pass": not failed,
    }


def manifest_records(files: list[Path]) -> list[dict]:
    return [
        {
            "path": rel(path),
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
            zf.write(path, f"{STAGE}/{path.relative_to(OUT).as_posix()}")
    return sha256_file(ZIP_PATH)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    source_dir = OUT / "source_snapshots"
    source_dir.mkdir(exist_ok=True)
    for source in [P6_HTML, P6_VIEWMODEL, P6_TALK_FLOW, P6_NOTES, P6_VALIDATOR, P5_VALIDATOR, P5_MAP]:
        shutil.copy2(source, source_dir / source.name)

    summary = source_summary()
    write_text(OUT / "README.md", readme_md(summary))
    write_json(OUT / "r93_p6_acceptance_and_r95_readiness_gate.json", DECISION)
    write_text(OUT / "r93_p6_acceptance_decision.md", acceptance_decision_md(summary))
    write_text(OUT / "r95_export_preview_readiness_gate.md", r95_readiness_gate_md())
    write_text(OUT / "r93_p6_quality_notes_for_r95.md", quality_notes_md())
    write_text(OUT / "r93_p6_boundary_confirmation.md", boundary_md())
    write_json(OUT / "quality_sentinel_v1_preview.json", quality_sentinel())
    shutil.copy2(Path(__file__), OUT / Path(__file__).name)

    validation = validate()
    write_json(OUT / "validate_1013R_R93_P6_acceptance_and_R95_readiness_gate_result.json", validation)

    files_for_zip = [
        p
        for p in OUT.rglob("*")
        if p.is_file() and p.name not in {"REVIEW_PACKAGE_MANIFEST.json", "REVIEW_PACKAGE_MANIFEST.md"}
    ]
    zip_sha = build_zip(files_for_zip)
    all_files = [p for p in OUT.rglob("*") if p.is_file()]
    manifest = {
        "stage": STAGE,
        "final_status": "PASS_1013R_R93_P6_ACCEPTANCE_AND_R95_READINESS_GATE"
        if validation["validator_pass"]
        else "FAIL_1013R_R93_P6_ACCEPTANCE_AND_R95_READINESS_GATE",
        "zip_path": rel(ZIP_PATH),
        "zip_sha256": zip_sha,
        "files": manifest_records(all_files),
        "boundary": BOUNDARY,
    }
    write_json(OUT / "REVIEW_PACKAGE_MANIFEST.json", manifest)
    lines = ["# REVIEW_PACKAGE_MANIFEST", "", f"ZIP SHA256: `{zip_sha}`", ""]
    for record in manifest["files"]:
        lines.append(f"- `{record['path']}` sha256=`{record['sha256']}`")
    write_text(OUT / "REVIEW_PACKAGE_MANIFEST.md", "\n".join(lines))

    print(
        json.dumps(
            {
                "stage": STAGE,
                "validator_pass": validation["validator_pass"],
                "r93_p6_result": validation["r93_p6_result"],
                "r95_authorization_status": validation["r95_authorization_status"],
                "r95_allowed_now": validation["r95_allowed_now"],
                "out_dir": str(OUT),
                "zip_path": str(ZIP_PATH),
                "zip_sha256": zip_sha,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
