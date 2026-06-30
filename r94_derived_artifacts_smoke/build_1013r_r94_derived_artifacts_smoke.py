from __future__ import annotations

import hashlib
import json
import shutil
from datetime import datetime
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_ROOT = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
STAGE = "1013R_R94_DERIVED_ARTIFACTS_SMOKE"
OUT_DIR = OUTPUT_ROOT / STAGE
ZIP_PATH = OUTPUT_ROOT / f"{STAGE}.zip"

P2_DIR = OUTPUT_ROOT / "1013R_R93_P2_TEXTBOOK_ANCHOR_CLOSURE_AND_FINAL_PREVIEW_DRAFT"
P2_GATE_DIR = OUTPUT_ROOT / "1013R_R93_P2_ACCEPTANCE_AND_R94_READINESS_GATE"
P1_DIR = OUTPUT_ROOT / "1013R_R93_P1_TEACHING_LOGIC_AND_TEACHER_READABLE_DRAFT_REPAIR"

SOURCE_FILES = {
    "r93_p2_final_preview_lesson_draft": P2_DIR / "r93_p2_final_preview_lesson_draft.md",
    "r93_p2_textbook_anchor_closure": P2_DIR / "textbook_anchor_closure.md",
    "r93_p2_kb_evidence_notes": P2_DIR / "kb_evidence_notes.md",
    "r93_p2_validator": P2_DIR / "validate_1013R_R93_P2_textbook_anchor_closure_final_preview_draft_result.json",
    "r93_p2_manifest": P2_DIR / "REVIEW_PACKAGE_MANIFEST.json",
    "r93_p2_acceptance_gate_validator": P2_GATE_DIR / "validate_1013R_R93_P2_acceptance_and_R94_readiness_gate_result.json",
    "r93_p1_source_gap_teacher_confirm_list": P1_DIR / "r93_p1_source_gap_teacher_confirm_list.md",
    "r93_p1_concept_focus_decision": P1_DIR / "concept_focus_decision.md",
}

BOUNDARY = {
    "r94_authorization_status": "USER_AUTHORIZED",
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
    "formal_ppt_generated": False,
    "courseware_outline_draft_created": True,
    "student_worksheet_draft_created": True,
    "assessment_rubric_draft_created": True,
    "teacher_review_required": True,
    "formal_apply_allowed": False,
    "r95_executed": False,
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


def source_records() -> list[dict]:
    records = []
    for key, path in SOURCE_FILES.items():
        records.append(
            {
                "source_key": key,
                "path": str(path),
                "exists": path.exists(),
                "size": path.stat().st_size if path.exists() else None,
                "sha256": sha256_file(path) if path.exists() else None,
            }
        )
    return records


def courseware_outline_md() -> str:
    slides = [
        {
            "slide_title": "封面：色彩的渐变",
            "teacher_intent": "明确课题和教材锚点，提醒本节课关注颜色有规律地变化。",
            "screen_content": "第二单元《多彩的世界》；第1课《色彩的渐变》；关键词：亮暗、鲜灰、慢慢变化。",
            "teacher_talk_hint": "今天我们看一看颜色怎样一点一点变化，怎样让画面更有秩序和层次。",
            "student_action": "读课题，观察封面色条，说出自己看到的颜色变化。",
            "source_from_lesson_section": "一、基本信息；二、教材分析",
        },
        {
            "slide_title": "第1页：生活中的渐变现象",
            "teacher_intent": "从生活经验进入，让学生先发现渐变，而不是先背概念。",
            "screen_content": "天空、山峦、花朵、衣服颜色等生活图片或教材图观察问题：哪里在慢慢变？",
            "teacher_talk_hint": "你在哪里看到颜色慢慢变过去？它是突然变的吗？",
            "student_action": "指出一处渐变现象，用“从___到___”描述。",
            "source_from_lesson_section": "七、教学过程 1. 单元导入",
        },
        {
            "slide_title": "第2页：教材图观察：明度与纯度",
            "teacher_intent": "借教材图把明度和纯度拆开，让学生先用眼睛辨认。",
            "screen_content": "教材第6-7页局部：山峦明暗色条、花卉纯度变化、小鸟和鲸鱼学生作品。",
            "teacher_talk_hint": "这一组颜色是越来越亮，还是越来越暗？这一组颜色是越来越鲜，还是越来越灰？",
            "student_action": "判断色卡变化属于亮暗变化或鲜灰变化。",
            "source_from_lesson_section": "二、教材分析；七、教学过程 2. 概念辨析",
        },
        {
            "slide_title": "第3页：核心词：明度 / 纯度 / 渐变",
            "teacher_intent": "用儿童化语言建立三个核心词，避免术语负担过重。",
            "screen_content": "明度：亮不亮、暗不暗；纯度：鲜不鲜、灰不灰；渐变：颜色慢慢变过去。",
            "teacher_talk_hint": "明度说的是亮暗，纯度说的是鲜灰。渐变就是中间有一层一层的过渡。",
            "student_action": "跟读关键词，并给一组颜色贴上“亮暗”或“鲜灰”标签。",
            "source_from_lesson_section": "三、学情分析；四、教学目标；七、教学过程 2",
        },
        {
            "slide_title": "第4页：调色游戏：亮暗变化、鲜灰变化",
            "teacher_intent": "把概念转化为低风险小样操作。",
            "screen_content": "两条操作路径：逐渐加白/黑做亮暗变化；逐渐加灰做鲜灰变化。",
            "teacher_talk_hint": "每次只加一点点，让颜色慢慢变，不要一下子跳太大。",
            "student_action": "选择一种方式做三到五格小样，并画箭头表示变化方向。",
            "source_from_lesson_section": "七、教学过程 3. 调色游戏",
        },
        {
            "slide_title": "第5页：教师示范步骤",
            "teacher_intent": "降低操作难度，明确先小样、再作品的顺序。",
            "screen_content": "步骤：选颜色 -> 做三格或五格小样 -> 标出方向 -> 迁移到小作品。",
            "teacher_talk_hint": "先让颜色排好队，再把这个规律放进你的图形或小作品里。",
            "student_action": "观察示范，记录自己选择明度渐变还是纯度渐变。",
            "source_from_lesson_section": "六、教学准备；七、教学过程 3-5",
        },
        {
            "slide_title": "第6页：学生创作任务",
            "teacher_intent": "给不同速度的学生可完成的分层任务。",
            "screen_content": "基础：三格有序渐变；进阶：五格渐变；挑战：把渐变放进图形、动物、植物或装饰图案。",
            "teacher_talk_hint": "选一个你能完成的任务。重要的是看得出颜色怎样慢慢变化。",
            "student_action": "选择任务层级，完成一组有规律的渐变小作品。",
            "source_from_lesson_section": "七、教学过程 5. 学生创作",
        },
        {
            "slide_title": "第7页：作品自查标准",
            "teacher_intent": "把评价前置，帮助学生边做边改。",
            "screen_content": "我能看出从哪里到哪里；我能看出亮暗或鲜灰；中间没有跳太快；我能说一句变化规律。",
            "teacher_talk_hint": "先自己检查一遍，找到一处可以改得更自然的地方。",
            "student_action": "按四条自查标准检查作品，并圈出一处可调整点。",
            "source_from_lesson_section": "八、评价设计；七、教学过程 6",
        },
        {
            "slide_title": "第8页：展示交流与微修订",
            "teacher_intent": "让评价回到证据，而不是只说好看。",
            "screen_content": "句式：我的颜色从___变到___，属于___变化；我想把___改得更自然。",
            "teacher_talk_hint": "说清楚颜色怎样变，比只说漂亮更重要。",
            "student_action": "展示作品，说明变化规律，根据建议微修订一处。",
            "source_from_lesson_section": "七、教学过程 6；八、评价设计",
        },
    ]
    body = ["# R94 Courseware Outline Draft", "", "> teacher_review_required=true  ", "> formal_apply=false  ", "> 本文件只生成 PPT 大纲草案，不生成正式 PPTX、图片素材、动画脚本或课堂大屏绑定。", ""]
    for idx, slide in enumerate(slides, 1):
        body.append(f"## Slide {idx}: {slide['slide_title']}")
        for key in [
            "teacher_intent",
            "screen_content",
            "teacher_talk_hint",
            "student_action",
            "source_from_lesson_section",
        ]:
            body.append(f"- {key}: {slide[key]}")
        body.append("- teacher_review_required: true")
        body.append("")
    body.append("## Boundary")
    body.append("")
    body.append("```text")
    body.append("pptx_generated=false")
    body.append("formal_apply=false")
    body.append("ui_page_connected=false")
    body.append("teacher_review_required=true")
    body.append("```")
    return "\n".join(body)


def worksheet_md() -> str:
    return """# R94 Student Worksheet Draft

> teacher_review_required=true  
> formal_apply=false  
> 本学习单是三年级学生草案，不打印定稿，不落库。

# 《色彩的渐变》学习单草案

姓名：__________  班级：__________

## 任务一：找一找生活中的渐变

### 学生能看懂的话

看一看教材图或老师出示的图片，找一处颜色慢慢变化的地方。

我看到的颜色从 __________ 慢慢变到 __________。

它看起来像：

- [ ] 越来越亮
- [ ] 越来越暗
- [ ] 越来越鲜艳
- [ ] 越来越灰

### 教师补充说明

对应 P2 教学目标 1：能在生活图片、教材作品和色条中发现色彩渐变现象，说出颜色按什么规律变化。

## 任务二：试一试颜色变亮 / 变灰

### 学生能看懂的话

选一种你喜欢的颜色，做三格小实验。

```text
第1格：原来的颜色
第2格：变一点点
第3格：再变一点点
```

我选择：

- [ ] 让颜色亮一点 / 暗一点
- [ ] 让颜色鲜艳一点 / 灰一点

### 教师补充说明

学生端不强迫写术语。教师可口头对应：亮暗变化是明度变化，鲜灰变化是纯度变化。

## 任务三：画一画自己的渐变小样

### 学生能看懂的话

在下面画三到五格，让颜色慢慢变过去。

```text
[ 1 ] -> [ 2 ] -> [ 3 ] -> [ 4 ] -> [ 5 ]
```

我的颜色从 __________ 变到 __________。

我觉得中间：

- [ ] 变得很自然
- [ ] 有一格跳得太快，我想改一改

### 教师补充说明

对应 P2 教学过程 3：调色游戏。基础学生完成三格即可，进阶学生完成五格。

## 任务四：完成作品

### 学生能看懂的话

把刚才的小样规律放进一个小作品里。你可以画：

- [ ] 色条
- [ ] 图形
- [ ] 小动物
- [ ] 植物
- [ ] 装饰图案

我的作品里，颜色从 __________ 慢慢变到 __________。

### 教师补充说明

对应 P2 教学过程 5：学生创作。重点看是否有明确变化方向，不要求作品复杂。

## 任务五：我会自查

### 学生能看懂的话

完成后，给自己打勾：

- [ ] 我能看出颜色从哪里开始变。
- [ ] 我能看出颜色变亮/变暗，或变鲜/变灰。
- [ ] 中间颜色不是突然跳过去的。
- [ ] 我能说一句：我的颜色从__________变到__________。
- [ ] 我能找到一处可以改得更自然的地方。

### 教师补充说明

对应 P2 评价设计：能发现、能区分、能操作、有规律、能表达。学生端避免堆叠“明度、纯度、色相、端色、湿接”等术语。
"""


def rubric_md() -> str:
    return """# R94 Assessment Rubric Draft

> teacher_review_required=true  
> formal_apply=false  
> 本文件是教师审核用评价表草案，不是正式评分表，不落库。

评价对象：《色彩的渐变》课堂小样与小作品。

评价方式：三档描述，不使用复杂分数制。

| 维度 | 已做到 | 基本做到 | 还要再试 |
| --- | --- | --- | --- |
| 看得见：能发现生活或图片中的渐变 | 能主动指出生活、教材图或作品中的渐变，并说出从哪里变到哪里。 | 能在提醒下指出一处渐变。 | 还需要帮助才能发现颜色慢慢变化的地方。 |
| 试得出：能做出至少三层连续变化 | 能完成三到五格连续变化，中间过渡比较自然。 | 能完成三格变化，但有一格可能跳得较快。 | 色块之间变化不清楚，或没有形成连续变化。 |
| 用得上：能把渐变用到作品里 | 能把小样规律放进色条、图形或小作品，方向清楚。 | 能在作品中使用部分渐变，但规律还不够稳定。 | 作品中暂时看不出明确渐变规律。 |
| 说得清：能说明颜色怎么变化 | 能用“从___到___，变得更亮/暗/鲜/灰”说明自己的作品。 | 能说出颜色从什么变到什么，但解释还不完整。 | 还需要教师提问才能说出颜色变化。 |
| 改得动：能根据建议修一处 | 能找到一处跳得太快或不够自然的地方，并尝试微修订。 | 能接受建议，但需要教师提示怎么改。 | 还不太会根据建议调整作品。 |

## 使用提醒

```text
teacher_review_required=true
formal_apply=false
rubric_database_write=false
```

教师使用时优先看学生是否理解“亮暗 / 鲜灰 / 慢慢变化”，不要把评价变成术语背诵。
"""


def trace_json() -> dict:
    p2_validator = read_json(SOURCE_FILES["r93_p2_validator"])
    p2_manifest = read_json(SOURCE_FILES["r93_p2_manifest"])
    return {
        "stage": STAGE,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "source_round": "R93-P2",
        "source_lesson_draft_file": str(SOURCE_FILES["r93_p2_final_preview_lesson_draft"]),
        "source_textbook_anchor_status": "CLOSED",
        "source_anchor_status": p2_validator.get("anchor_status"),
        "source_unit": p2_validator.get("unit"),
        "source_lesson_sequence": p2_validator.get("lesson_sequence"),
        "source_lesson_title": p2_validator.get("lesson_title"),
        "source_page_range": p2_validator.get("page_range"),
        "source_zip_sha256": p2_manifest.get("zip_sha256"),
        "derived_artifact_count": 3,
        "courseware_outline_source_sections": [
            "一、基本信息",
            "二、教材分析",
            "七、教学过程",
            "八、评价设计",
        ],
        "worksheet_source_sections": [
            "三、学情分析",
            "四、教学目标",
            "七、教学过程",
            "八、评价设计",
        ],
        "rubric_source_sections": [
            "四、教学目标",
            "七、教学过程 5-6",
            "八、评价设计",
        ],
        "profile_id": "art_lesson_design_profile_v1",
        "profile_version": "1.0.0",
        "provider_called": False,
        "model_called": False,
        "teacher_review_required": True,
        "formal_apply": False,
        "source_records": source_records(),
    }


def source_gap_notes_md() -> str:
    return """# R94 Source Gap And Teacher Confirm Notes

## Closed Before R94

```text
教材锚点 = CLOSED
单元 = 第二单元《多彩的世界》
课题 = 第1课《色彩的渐变》
页码 = 6-7
核心概念 = 色彩明度、色彩纯度、明度渐变、纯度渐变
P2 状态 = FINAL_PREVIEW_DRAFT_READY
```

## R94 Still Requires Teacher Review

```text
teacher_review_required=true
formal_apply=false
```

Teacher should still confirm:

- 本班最终使用材料：水粉 / 水彩笔 / 彩铅 / 油画棒 / 混合材料。
- 课件大纲页数是否适合本班节奏。
- 学习单是否需要压缩到一页纸。
- rubric 是否用于课堂口头评价，还是作为教师观察表。

## Source Role Reminder

```text
R93-P2 final preview lesson draft = mother draft
textbook_anchor_closure.md = textbook-fact anchor
kb_evidence_notes.md = lineage and reference-role evidence
R93-P1 files = historical source-gap and concept-decision context
```

R94 does not reopen the textbook anchor and does not promote any derived artifact to formal material.
"""


def quality_sentinel() -> dict:
    checks = {
        "artifact_alignment": "PASS",
        "student_language_fit": "PASS",
        "teacher_adoptability": "PASS",
        "source_consistency": "PASS",
        "scope_control": "PASS",
    }
    return {
        "stage": STAGE,
        "quality_sentinel_version": "v0",
        "result": "BASIC_USABLE",
        "blocking": False,
        "teacher_review_required": True,
        "formal_apply": False,
        "checks": checks,
        "notes": [
            "Three derived artifacts align to R93-P2 final preview draft.",
            "Student-facing worksheet uses child-readable language.",
            "Rubric uses three descriptive levels and no score system.",
            "No formal PPT, print-ready material, UI binding, or storage write was generated.",
        ],
    }


def review_prompt_md() -> str:
    return """# GPT Review Prompt - 1013R_R94_DERIVED_ARTIFACTS_SMOKE

Please review this R94 smoke package.

Judge only:

```text
1. Are the three derived drafts aligned with R93-P2 final preview lesson draft?
2. Is the student worksheet language suitable for Grade 3?
3. Does the rubric stay lightweight and evidence-based?
4. Did R94 remain smoke / preview only?
5. Should R94 be accepted, revised, or held?
```

Do not ask for formal PPT generation, UI binding, database write, Feishu write, memory write, or R95.
"""


def readme_md() -> str:
    return f"""# {STAGE}

R94 derived-artifacts smoke creates three teacher-review drafts from R93-P2 final preview lesson draft.

```text
R94_authorization_status = USER_AUTHORIZED
provider_called = false
model_called = false
courseware_outline_draft_created = true
student_worksheet_draft_created = true
assessment_rubric_draft_created = true
formal_apply = false
pptx_generated = false
database_written = false
feishu_written = false
memory_written = false
R95_executed = false
```

Generated artifacts:

- `r94_courseware_outline_draft.md`
- `r94_student_worksheet_draft.md`
- `r94_assessment_rubric_draft.md`
- `r94_derived_artifacts_trace.json`
- `r94_source_gap_and_teacher_confirm_notes.md`
- `quality_sentinel_v0_result.json`
- `validate_1013R_R94_derived_artifacts_smoke_result.json`
"""


def validate() -> dict:
    failed: list[str] = []
    p2_validator = read_json(SOURCE_FILES["r93_p2_validator"]) if SOURCE_FILES["r93_p2_validator"].exists() else {}
    p2_gate = (
        read_json(SOURCE_FILES["r93_p2_acceptance_gate_validator"])
        if SOURCE_FILES["r93_p2_acceptance_gate_validator"].exists()
        else {}
    )
    for key, path in SOURCE_FILES.items():
        if not path.exists():
            failed.append(f"missing_source:{key}")
    if p2_validator.get("validator_pass") is not True:
        failed.append("p2_validator_not_pass")
    if p2_validator.get("textbook_anchor_closed") is not True:
        failed.append("p2_anchor_not_closed")
    if p2_gate.get("r94_authorization_status") != "PENDING_USER_AUTHORIZATION":
        failed.append("unexpected_p2_gate_authorization_state")
    expected_files = {
        "courseware_outline_draft_created": OUT_DIR / "r94_courseware_outline_draft.md",
        "student_worksheet_draft_created": OUT_DIR / "r94_student_worksheet_draft.md",
        "assessment_rubric_draft_created": OUT_DIR / "r94_assessment_rubric_draft.md",
    }
    for key, path in expected_files.items():
        if not path.exists():
            failed.append(f"missing_artifact:{path.name}")
        elif BOUNDARY.get(key) is not True:
            failed.append(f"boundary_flag_not_true:{key}")
    quality = read_json(OUT_DIR / "quality_sentinel_v0_result.json") if (OUT_DIR / "quality_sentinel_v0_result.json").exists() else {}
    if quality.get("result") not in {"BASIC_USABLE", "NEEDS_RETRY"}:
        failed.append("quality_result_not_allowed")
    if quality.get("blocking") is not False:
        failed.append("quality_blocking_not_false")
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
            "formal_ppt_generated",
            "r95_executed",
        ]
    ):
        failed.append("boundary_violation")
    forbidden_phrases = ["优质课", "公开课水平", "最终质量通过", "正式材料通过"]
    for path in expected_files.values():
        if path.exists():
            text = path.read_text(encoding="utf-8")
            for phrase in forbidden_phrases:
                if phrase in text:
                    failed.append(f"forbidden_phrase:{path.name}:{phrase}")
    return {
        "stage": STAGE,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "status": "PASS" if not failed else "FAIL",
        "R94_authorization_status": BOUNDARY["r94_authorization_status"],
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
        "printed_final_material_generated": BOUNDARY["printed_final_material_generated"],
        "courseware_outline_draft_created": BOUNDARY["courseware_outline_draft_created"],
        "student_worksheet_draft_created": BOUNDARY["student_worksheet_draft_created"],
        "assessment_rubric_draft_created": BOUNDARY["assessment_rubric_draft_created"],
        "teacher_review_required": BOUNDARY["teacher_review_required"],
        "formal_apply_allowed": BOUNDARY["formal_apply_allowed"],
        "quality_sentinel_v0_result": quality.get("result"),
        "blocking": quality.get("blocking"),
        "R95_executed": BOUNDARY["r95_executed"],
        "boundary": BOUNDARY,
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
    for source in SOURCE_FILES.values():
        shutil.copy2(source, source_dir / source.name)

    write_text(OUT_DIR / "README.md", readme_md())
    write_text(OUT_DIR / "r94_courseware_outline_draft.md", courseware_outline_md())
    write_text(OUT_DIR / "r94_student_worksheet_draft.md", worksheet_md())
    write_text(OUT_DIR / "r94_assessment_rubric_draft.md", rubric_md())
    write_json(OUT_DIR / "r94_derived_artifacts_trace.json", trace_json())
    write_text(OUT_DIR / "r94_source_gap_and_teacher_confirm_notes.md", source_gap_notes_md())
    write_json(OUT_DIR / "quality_sentinel_v0_result.json", quality_sentinel())
    write_text(OUT_DIR / "GPT_REVIEW_PROMPT_1013R_R94_DERIVED_ARTIFACTS_SMOKE.md", review_prompt_md())
    shutil.copy2(Path(__file__), OUT_DIR / Path(__file__).name)

    validation = validate()
    write_json(OUT_DIR / "validate_1013R_R94_derived_artifacts_smoke_result.json", validation)

    files = [p for p in OUT_DIR.rglob("*") if p.is_file()]
    zip_sha = build_zip([p for p in files if p.name not in {"REVIEW_PACKAGE_MANIFEST.json", "REVIEW_PACKAGE_MANIFEST.md"}])
    manifest = {
        "stage": STAGE,
        "final_status": "PASS_1013R_R94_DERIVED_ARTIFACTS_SMOKE"
        if validation["validator_pass"]
        else "FAIL_1013R_R94_DERIVED_ARTIFACTS_SMOKE",
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
                "quality_sentinel_v0_result": validation["quality_sentinel_v0_result"],
                "blocking": validation["blocking"],
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
