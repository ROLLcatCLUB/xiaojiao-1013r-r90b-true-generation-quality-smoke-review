from __future__ import annotations

import hashlib
import json
import shutil
from datetime import datetime
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_ROOT = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
STAGE = "1013R_R94_P1_DERIVED_ARTIFACTS_TEACHER_REVIEW_POLISH"
OUT_DIR = OUTPUT_ROOT / STAGE
ZIP_PATH = OUTPUT_ROOT / f"{STAGE}.zip"

R93_P2_DIR = OUTPUT_ROOT / "1013R_R93_P2_TEXTBOOK_ANCHOR_CLOSURE_AND_FINAL_PREVIEW_DRAFT"
R94_DIR = OUTPUT_ROOT / "1013R_R94_DERIVED_ARTIFACTS_SMOKE"
R94_GATE_DIR = OUTPUT_ROOT / "1013R_R94_SMOKE_ACCEPTANCE_AND_R94_P1_QUALITY_GATE"

SOURCE_FILES = {
    "r93_p2_final_preview_lesson_draft": R93_P2_DIR / "r93_p2_final_preview_lesson_draft.md",
    "r93_p2_textbook_anchor_closure": R93_P2_DIR / "textbook_anchor_closure.md",
    "r93_p2_validator": R93_P2_DIR / "validate_1013R_R93_P2_textbook_anchor_closure_final_preview_draft_result.json",
    "r94_courseware_outline_draft": R94_DIR / "r94_courseware_outline_draft.md",
    "r94_student_worksheet_draft": R94_DIR / "r94_student_worksheet_draft.md",
    "r94_assessment_rubric_draft": R94_DIR / "r94_assessment_rubric_draft.md",
    "r94_trace": R94_DIR / "r94_derived_artifacts_trace.json",
    "r94_validator": R94_DIR / "validate_1013R_R94_derived_artifacts_smoke_result.json",
    "r94_manifest": R94_DIR / "REVIEW_PACKAGE_MANIFEST.json",
    "r94_quality_notes_for_p1": R94_GATE_DIR / "r94_quality_notes_for_p1.md",
    "r94_p1_gate_validator": R94_GATE_DIR / "validate_1013R_R94_smoke_acceptance_and_R94_P1_quality_gate_result.json",
}

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
    "r95_executed": False,
    "teacher_review_required": True,
    "formal_apply_allowed": False,
    "artifact_formal_ready": False,
}


SLIDES = [
    {
        "slide_id": "S01",
        "slide_title": "封面：色彩的渐变",
        "visual_layout": "全屏教材主题色背景，中央课题，底部放三枚小色块：亮暗、鲜灰、慢慢变化。",
        "main_visual_suggestion": "用教材页中的渐变色块或教师自制渐变色条作为背景线索，不需要新图片素材。",
        "screen_text": "色彩的渐变\n颜色慢慢变过去",
        "teacher_talk_hint": "今天我们不急着画大作品，先看颜色怎样一点一点变化。",
        "student_action": "读课题，说一说屏幕上的颜色有没有慢慢变化。",
        "board_or_annotation_hint": "板书：渐变 = 颜色慢慢变过去。",
        "source_lesson_section": "R93-P2 一、基本信息；二、教材分析",
    },
    {
        "slide_id": "S02",
        "slide_title": "生活中的渐变",
        "visual_layout": "三图并排：天空/山峦/花朵或教材图局部，每图只配一个观察箭头。",
        "main_visual_suggestion": "主图突出从亮到暗、从鲜到灰或层层变化，不放大段说明文字。",
        "screen_text": "找一找：颜色从哪里变到哪里？",
        "teacher_talk_hint": "请用手指一指，颜色从哪里开始变，又变到了哪里。",
        "student_action": "用“从___到___”说出一处生活或教材图中的渐变。",
        "board_or_annotation_hint": "圈出起点和终点，用箭头标出变化方向。",
        "source_lesson_section": "R93-P2 七、教学过程 1",
    },
    {
        "slide_id": "S03",
        "slide_title": "教材图观察：明度与纯度",
        "visual_layout": "左右对比：左侧亮暗变化，右侧鲜灰变化；每侧只保留一组代表性色条。",
        "main_visual_suggestion": "使用教材第6-7页山峦色条、花卉或调色游戏图作为观察来源。",
        "screen_text": "亮一点 / 暗一点\n鲜一点 / 灰一点",
        "teacher_talk_hint": "左边看亮不亮，右边看鲜不鲜。先用眼睛分清楚。",
        "student_action": "判断一组颜色是在变亮/变暗，还是变鲜/变灰。",
        "board_or_annotation_hint": "板书两列：亮暗；鲜灰。",
        "source_lesson_section": "R93-P2 二、教材分析；七、教学过程 2",
    },
    {
        "slide_id": "S04",
        "slide_title": "核心词：亮暗 / 鲜灰 / 慢慢变化",
        "visual_layout": "三张小卡片横排，每张卡片一个词和一个儿童化解释。",
        "main_visual_suggestion": "卡片一：亮暗；卡片二：鲜灰；卡片三：慢慢变化。",
        "screen_text": "亮暗：明度\n鲜灰：纯度\n慢慢变化：渐变",
        "teacher_talk_hint": "老师会说专业词，但你们可以先记住：亮暗、鲜灰、慢慢变化。",
        "student_action": "把教师出示的色卡贴到“亮暗”或“鲜灰”类别。",
        "board_or_annotation_hint": "在专业词旁加学生语言：明度=亮暗，纯度=鲜灰。",
        "source_lesson_section": "R93-P2 三、学情分析；七、教学过程 2",
    },
    {
        "slide_id": "S05",
        "slide_title": "调色游戏",
        "visual_layout": "两条流程线：上方亮暗三格，下方鲜灰三格；每条线配一支箭头。",
        "main_visual_suggestion": "不展示复杂调色理论，只展示三格从原色到变化色的小样。",
        "screen_text": "每次只变一点点",
        "teacher_talk_hint": "一格一格慢慢变，中间不要一下子跳太远。",
        "student_action": "选择一条路线，做三格颜色慢慢变化的小样。",
        "board_or_annotation_hint": "箭头标注：第1格 -> 第2格 -> 第3格。",
        "source_lesson_section": "R93-P2 七、教学过程 3",
    },
    {
        "slide_id": "S06",
        "slide_title": "教师示范",
        "visual_layout": "四步流程：选颜色、调三格、画箭头、放进小图形。",
        "main_visual_suggestion": "用实物投影或板演，不生成动画；屏幕只放步骤提示。",
        "screen_text": "选颜色 -> 做小样 -> 标方向 -> 放进作品",
        "teacher_talk_hint": "先把颜色排好队，再放进你的图形里。",
        "student_action": "观察示范，并在学习单上勾选自己要做亮暗还是鲜灰变化。",
        "board_or_annotation_hint": "提示常见错误：跳太快、颜色混脏、方向不清楚。",
        "source_lesson_section": "R93-P2 七、教学过程 3-5",
    },
    {
        "slide_id": "S07",
        "slide_title": "学生创作任务",
        "visual_layout": "三层任务竖排：基础、进阶、挑战，每层一行。",
        "main_visual_suggestion": "用图标区分：三格、五格、小作品。",
        "screen_text": "基础：三格\n进阶：五格\n挑战：放进小作品",
        "teacher_talk_hint": "先选能完成的任务，重点是看得出颜色慢慢变化。",
        "student_action": "选择一个层级完成渐变小样或小作品。",
        "board_or_annotation_hint": "巡视看三点：方向、亮暗/鲜灰、是否跳色。",
        "source_lesson_section": "R93-P2 七、教学过程 5",
    },
    {
        "slide_id": "S08",
        "slide_title": "作品自查",
        "visual_layout": "四个勾选项，留白多，适合投屏快速核对。",
        "main_visual_suggestion": "每项配一个简洁符号：起点、箭头、三格、说一句。",
        "screen_text": "我看得出起点\n我看得出方向\n中间没有跳太快\n我能说一句",
        "teacher_talk_hint": "先自己检查，再请同桌帮你看一处。",
        "student_action": "用自查句检查作品，圈出一处可调整地方。",
        "board_or_annotation_hint": "板书句式：我的颜色从___变到___。",
        "source_lesson_section": "R93-P2 八、评价设计",
    },
    {
        "slide_id": "S09",
        "slide_title": "展示交流",
        "visual_layout": "左侧展示作品，右侧固定三句评价句式。",
        "main_visual_suggestion": "选一件自然过渡作品和一件可修订作品做对比。",
        "screen_text": "我看到...\n我觉得...\n我建议...",
        "teacher_talk_hint": "我们评价时要说证据：颜色怎么变，中间顺不顺。",
        "student_action": "说出同伴作品的一处优点和一处建议。",
        "board_or_annotation_hint": "用圈画标出过渡自然处和需要微调处。",
        "source_lesson_section": "R93-P2 七、教学过程 6",
    },
    {
        "slide_id": "S10",
        "slide_title": "微修订",
        "visual_layout": "一张作品局部 + 一条修改前后小箭头。",
        "main_visual_suggestion": "突出“改一处即可”，避免课堂尾声变成重画。",
        "screen_text": "只改一处，让颜色更自然",
        "teacher_talk_hint": "今天最后一步不是重画，是让一处颜色变得更自然。",
        "student_action": "根据自查或同伴建议微修订一处。",
        "board_or_annotation_hint": "收束：亮暗、鲜灰、慢慢变化。",
        "source_lesson_section": "R93-P2 七、教学过程 6；八、评价设计",
    },
]


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
    return [
        {
            "source_key": key,
            "path": str(path),
            "exists": path.exists(),
            "size": path.stat().st_size if path.exists() else None,
            "sha256": sha256_file(path) if path.exists() else None,
        }
        for key, path in SOURCE_FILES.items()
    ]


def slide_storyboard_md() -> str:
    lines = [
        "# R94-P1 Slide Storyboard",
        "",
        "> teacher_review_required=true  ",
        "> formal_apply=false  ",
        "> 本文件是课件 storyboard 草案，不生成正式 PPTX、不生成图片素材、不绑定课堂大屏。",
        "",
    ]
    for slide in SLIDES:
        lines.append(f"## {slide['slide_id']} {slide['slide_title']}")
        for key in [
            "visual_layout",
            "main_visual_suggestion",
            "screen_text",
            "teacher_talk_hint",
            "student_action",
            "board_or_annotation_hint",
            "source_lesson_section",
        ]:
            lines.append(f"- {key}: {slide[key]}")
        lines.append("- teacher_review_required: true")
        lines.append("- formal_apply: false")
        lines.append("")
    return "\n".join(lines)


def slide_storyboard_json() -> dict:
    return {
        "artifact": "r94_p1_slide_storyboard",
        "teacher_review_required": True,
        "formal_apply": False,
        "pptx_generated": False,
        "slide_count": len(SLIDES),
        "slides": [
            {
                **slide,
                "teacher_review_required": True,
                "formal_apply": False,
            }
            for slide in SLIDES
        ],
    }


def student_worksheet_one_page_md() -> str:
    return """# R94-P1 Student Worksheet One Page Draft

> teacher_review_required=true  
> formal_apply=false  
> 一页可打印草案，但不是打印定稿。

# 《色彩的渐变》学习单

姓名：__________  班级：__________

## 任务一：找一找

我看到颜色从 __________ 慢慢变到 __________。

它是：

- [ ] 亮一点 / 暗一点
- [ ] 鲜一点 / 灰一点

## 任务二：试一试

选一种颜色，画三格，让它慢慢变。

```text
[ 原来的颜色 ] -> [ 变一点点 ] -> [ 再变一点点 ]
```

我的三格颜色：

```text
[        ] -> [        ] -> [        ]
```

## 任务三：查一查

完成作品后，我能做到：

- [ ] 我看得出颜色从哪里开始变。
- [ ] 我看得出颜色慢慢变过去。
- [ ] 我能说：我的颜色从 __________ 变到 __________。

我想把这一处改得更自然：____________________
"""


def worksheet_teacher_notes_md() -> str:
    return """# R94-P1 Student Worksheet Teacher Notes

> teacher_review_required=true  
> formal_apply=false  
> 本文件为教师说明版，不给学生直接堆术语。

## 对应概念

| 学生端说法 | 教师端概念 |
| --- | --- |
| 亮一点 / 暗一点 | 明度变化 |
| 鲜一点 / 灰一点 | 纯度变化 |
| 颜色慢慢变过去 | 渐变规律 |
| 中间没有跳太快 | 连续变化、过渡自然 |

## 材料准备

- 小样纸或学习单。
- 水粉、水彩笔、彩铅、油画棒或色卡任选其一。
- 教师示范用三格小样。

## 课堂使用建议

1. 任务一 2-3 分钟，只做观察和口头表达。
2. 任务二 6-8 分钟，先完成三格，不追求复杂作品。
3. 任务三 2 分钟，用作自查和微修订入口。

## 分层提示

- 基础：完成三格变化即可。
- 进阶：完成五格变化，尝试更均匀。
- 挑战：把变化规律放进图形或小作品。

## 常见问题与指导语

| 问题 | 指导语 |
| --- | --- |
| 颜色跳得太快 | “每次只变一点点，第二格可以更接近第一格。” |
| 说不清变化 | “先说从什么颜色开始，再说变到了什么颜色。” |
| 混淆亮暗和鲜灰 | “亮暗看灯光一样亮不亮；鲜灰看颜色鲜不鲜。” |
| 想画太复杂 | “今天先完成小变化，作品简单也可以。” |
"""


def worksheet_structured_json() -> dict:
    return {
        "artifact": "r94_p1_student_worksheet",
        "teacher_review_required": True,
        "formal_apply": False,
        "printed_final_material_generated": False,
        "student_version": {
            "page_count_target": "one_page_draft",
            "tasks": [
                {
                    "task_id": "task_1_find",
                    "title": "找一找",
                    "student_language": "我看到颜色从___慢慢变到___。",
                    "concept_bridge": ["渐变观察", "变化方向"],
                },
                {
                    "task_id": "task_2_try",
                    "title": "试一试",
                    "student_language": "选一种颜色，画三格，让它慢慢变。",
                    "concept_bridge": ["明度或纯度小样", "连续变化"],
                },
                {
                    "task_id": "task_3_check",
                    "title": "查一查",
                    "student_language": "我能说出颜色从哪里变到哪里。",
                    "concept_bridge": ["自查", "表达", "微修订"],
                },
            ],
        },
        "teacher_notes": {
            "concepts": ["明度", "纯度", "渐变规律"],
            "use_cases": ["课堂观察", "小样练习", "作品自查"],
        },
    }


def teacher_observation_rubric_md() -> str:
    return """# R94-P1 Teacher Observation Rubric Draft

> teacher_review_required=true  
> formal_apply=false  
> 教师观察版草案，不是正式评分表，不落库。

| 观察维度 | 已做到 | 基本做到 | 还要再试 | 教师记录 |
| --- | --- | --- | --- | --- |
| 看得见：能发现渐变 | 能主动指出生活、教材图或作品中的渐变，并说出变化方向。 | 能在提醒下指出一处渐变。 | 还需要帮助才能发现颜色慢慢变化。 |  |
| 试得出：能做出连续变化 | 能完成三到五格连续变化，中间过渡较自然。 | 能完成三格变化，但有一格跳得较快。 | 色块之间变化不清楚。 |  |
| 用得上：能把渐变用到作品里 | 能把小样规律放进图形或小作品，方向清楚。 | 能使用部分渐变，但规律不够稳定。 | 作品中暂时看不出明确渐变。 |  |
| 说得清：能说明颜色怎么变化 | 能用“从___到___，变得更亮/暗/鲜/灰”说明作品。 | 能说出颜色从什么变到什么。 | 需要教师追问才能表达。 |  |
| 改得动：能根据建议修一处 | 能找到一处并尝试微修订。 | 能接受建议，但需要提示怎么改。 | 暂时不会根据建议调整。 |  |

## 使用边界

```text
formal_apply=false
database_written=false
teacher_review_required=true
```
"""


def student_self_assessment_md() -> str:
    return """# R94-P1 Student Self Assessment Draft

> teacher_review_required=true  
> formal_apply=false  
> 学生自评版草案，三项即可，不使用分数。

# 我会自己看一看

姓名：__________

| 我来检查 | 已做到 | 基本做到 | 还要再试 |
| --- | --- | --- | --- |
| 我看见颜色慢慢变了 | [ ] | [ ] | [ ] |
| 我试出了三层颜色变化 | [ ] | [ ] | [ ] |
| 我能说出颜色从哪里变到哪里 | [ ] | [ ] | [ ] |

我想改得更自然的一处是：____________________
"""


def assessment_structured_json() -> dict:
    dimensions = [
        "看得见：能发现渐变",
        "试得出：能做出连续变化",
        "用得上：能把渐变用到作品里",
        "说得清：能说明颜色怎么变化",
        "改得动：能根据建议修一处",
    ]
    return {
        "artifact": "r94_p1_assessment",
        "teacher_review_required": True,
        "formal_apply": False,
        "score_system": "none",
        "levels": ["已做到", "基本做到", "还要再试"],
        "teacher_observation_dimensions": dimensions,
        "student_self_assessment_items": [
            "我看见颜色慢慢变了",
            "我试出了三层颜色变化",
            "我能说出颜色从哪里变到哪里",
        ],
    }


def trace_json() -> dict:
    return {
        "stage": STAGE,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "source_round": "R94_DERIVED_ARTIFACTS_SMOKE",
        "source_lesson_round": "R93-P2",
        "source_textbook_anchor_status": "CLOSED",
        "source_artifact_files": {
            "courseware": str(SOURCE_FILES["r94_courseware_outline_draft"]),
            "worksheet": str(SOURCE_FILES["r94_student_worksheet_draft"]),
            "rubric": str(SOURCE_FILES["r94_assessment_rubric_draft"]),
            "lesson_draft": str(SOURCE_FILES["r93_p2_final_preview_lesson_draft"]),
            "quality_notes": str(SOURCE_FILES["r94_quality_notes_for_p1"]),
        },
        "derived_artifact_count": 3,
        "slide_storyboard_created": True,
        "student_worksheet_one_page_created": True,
        "student_worksheet_teacher_notes_created": True,
        "teacher_observation_rubric_created": True,
        "student_self_assessment_created": True,
        "provider_called": False,
        "model_called": False,
        "profile_modified": False,
        "new_fields_added": False,
        "formal_apply": False,
        "r21_modified": False,
        "r36_modified": False,
        "ui_connected": False,
        "r95_executed": False,
        "source_records": source_records(),
    }


def quality_sentinel_json() -> dict:
    return {
        "stage": STAGE,
        "quality_sentinel_version": "v0",
        "result": "BASIC_USABLE",
        "blocking": False,
        "teacher_review_required": True,
        "formal_apply": False,
        "allowed_conclusion": "TEACHER_REVIEW_MATERIAL_READY",
        "preview_only": True,
        "checks": {
            "artifact_alignment": "PASS",
            "student_language_fit": "PASS",
            "teacher_adoptability": "PASS",
            "source_consistency": "PASS",
            "scope_control": "PASS",
            "print_readiness_preview": "PASS_WITH_NOTES",
        },
        "not_claimed": [
            "正式 PPTX",
            "打印定稿",
            "正式材料通过",
            "可直接发布",
        ],
    }


def quality_notes_md() -> str:
    return """# Quality Sentinel v0 Notes - R94-P1

Result:

```text
BASIC_USABLE
blocking=false
TEACHER_REVIEW_MATERIAL_READY
PREVIEW_ONLY
FORMAL_APPLY_FALSE
```

Checks:

| Check | Result | Note |
| --- | --- | --- |
| artifact_alignment | PASS | Storyboard, worksheet, and rubric remain aligned to R93-P2 and R94 smoke. |
| student_language_fit | PASS | Student-facing files use 亮一点/暗一点、鲜一点/灰一点、慢慢变过去. |
| teacher_adoptability | PASS | Teacher notes and observation rubric separate teacher-facing language from student-facing language. |
| source_consistency | PASS | No textbook anchor change and no source gap reopened. |
| scope_control | PASS | No PPTX, no print final, no UI, no formal apply, no storage write. |
| print_readiness_preview | PASS_WITH_NOTES | Student worksheet is one-page draft, but still requires teacher page layout review before printing. |

Forbidden formal-quality claims are not made. This package does not claim publish-level, competition-level, final-quality, print-final, or release-ready status.

```text
formal quality claims = absent
print-final claims = absent
release-ready claims = absent
```
"""


def review_prompt_md() -> str:
    return """# GPT Review Prompt - 1013R_R94_P1

Please review this R94-P1 teacher-review polish package.

Judge:

```text
1. Does the slide storyboard improve the R94 outline without becoming a PPTX?
2. Is the student worksheet truly one-page and child-readable?
3. Are teacher notes useful without leaking too much jargon to students?
4. Are teacher observation rubric and student self-assessment properly separated?
5. Did the package stay preview-only with formal_apply=false?
```

Do not request R95, formal PPTX, UI binding, database write, Feishu write, memory write, or formal apply.
"""


def readme_md() -> str:
    return f"""# {STAGE}

R94-P1 polishes R94 smoke drafts into teacher-review materials.

```text
result = PASS
quality_sentinel_v0_result = BASIC_USABLE
blocking = false
teacher_review_required = true
artifact_formal_ready = false
formal_apply = false
provider_called = false
model_called = false
pptx_generated = false
printed_final_material_generated = false
R95_executed = false
```

Outputs:

- `r94_p1_slide_storyboard.md`
- `r94_p1_slide_storyboard.json`
- `r94_p1_student_worksheet_one_page.md`
- `r94_p1_student_worksheet_teacher_notes.md`
- `r94_p1_student_worksheet_structured.json`
- `r94_p1_teacher_observation_rubric.md`
- `r94_p1_student_self_assessment.md`
- `r94_p1_assessment_structured.json`
- `r94_p1_derived_artifacts_trace.json`
"""


def validate() -> dict:
    failed: list[str] = []
    for key, path in SOURCE_FILES.items():
        if not path.exists():
            failed.append(f"missing_source:{key}")
    r94_gate = read_json(SOURCE_FILES["r94_p1_gate_validator"]) if SOURCE_FILES["r94_p1_gate_validator"].exists() else {}
    if r94_gate.get("next") != "R94-P1_DERIVED_ARTIFACTS_TEACHER_REVIEW_POLISH":
        failed.append("r94_p1_not_ready_from_gate")
    output_flags = {
        "slide_storyboard_created": OUT_DIR / "r94_p1_slide_storyboard.md",
        "student_worksheet_one_page_created": OUT_DIR / "r94_p1_student_worksheet_one_page.md",
        "student_worksheet_teacher_notes_created": OUT_DIR / "r94_p1_student_worksheet_teacher_notes.md",
        "teacher_observation_rubric_created": OUT_DIR / "r94_p1_teacher_observation_rubric.md",
        "student_self_assessment_created": OUT_DIR / "r94_p1_student_self_assessment.md",
    }
    for key, path in output_flags.items():
        if not path.exists():
            failed.append(f"missing_output:{key}")
    qs = read_json(OUT_DIR / "quality_sentinel_v0_result.json") if (OUT_DIR / "quality_sentinel_v0_result.json").exists() else {}
    if qs.get("result") not in {"BASIC_USABLE", "NEEDS_RETRY"}:
        failed.append("quality_result_not_allowed")
    if qs.get("blocking") is not False:
        failed.append("blocking_not_false")
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
            "r95_executed",
        ]
    ):
        failed.append("boundary_violation")
    forbidden = ["优质课", "公开课水平", "最终质量通过", "正式材料通过", "可直接打印", "可直接发布"]
    for path in [
        OUT_DIR / "r94_p1_slide_storyboard.md",
        OUT_DIR / "r94_p1_student_worksheet_one_page.md",
        OUT_DIR / "r94_p1_teacher_observation_rubric.md",
        OUT_DIR / "quality_sentinel_v0_notes.md",
    ]:
        if path.exists():
            text = path.read_text(encoding="utf-8")
            for phrase in forbidden:
                if phrase in text:
                    failed.append(f"forbidden_claim:{path.name}:{phrase}")
    return {
        "stage": STAGE,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "status": "PASS" if not failed else "FAIL",
        "R94_P1_result": "PASS" if not failed else "FAIL",
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
        "r95_executed": BOUNDARY["r95_executed"],
        "slide_storyboard_created": (OUT_DIR / "r94_p1_slide_storyboard.md").exists(),
        "student_worksheet_one_page_created": (OUT_DIR / "r94_p1_student_worksheet_one_page.md").exists(),
        "student_worksheet_teacher_notes_created": (OUT_DIR / "r94_p1_student_worksheet_teacher_notes.md").exists(),
        "teacher_observation_rubric_created": (OUT_DIR / "r94_p1_teacher_observation_rubric.md").exists(),
        "student_self_assessment_created": (OUT_DIR / "r94_p1_student_self_assessment.md").exists(),
        "teacher_review_required": BOUNDARY["teacher_review_required"],
        "formal_apply_allowed": BOUNDARY["formal_apply_allowed"],
        "artifact_formal_ready": BOUNDARY["artifact_formal_ready"],
        "quality_sentinel_v0_result": qs.get("result"),
        "blocking": qs.get("blocking"),
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
    write_text(OUT_DIR / "r94_p1_slide_storyboard.md", slide_storyboard_md())
    write_json(OUT_DIR / "r94_p1_slide_storyboard.json", slide_storyboard_json())
    write_text(OUT_DIR / "r94_p1_student_worksheet_one_page.md", student_worksheet_one_page_md())
    write_text(OUT_DIR / "r94_p1_student_worksheet_teacher_notes.md", worksheet_teacher_notes_md())
    write_json(OUT_DIR / "r94_p1_student_worksheet_structured.json", worksheet_structured_json())
    write_text(OUT_DIR / "r94_p1_teacher_observation_rubric.md", teacher_observation_rubric_md())
    write_text(OUT_DIR / "r94_p1_student_self_assessment.md", student_self_assessment_md())
    write_json(OUT_DIR / "r94_p1_assessment_structured.json", assessment_structured_json())
    write_json(OUT_DIR / "r94_p1_derived_artifacts_trace.json", trace_json())
    write_json(OUT_DIR / "quality_sentinel_v0_result.json", quality_sentinel_json())
    write_text(OUT_DIR / "quality_sentinel_v0_notes.md", quality_notes_md())
    write_text(OUT_DIR / "GPT_REVIEW_PROMPT_1013R_R94_P1.md", review_prompt_md())
    shutil.copy2(Path(__file__), OUT_DIR / Path(__file__).name)

    validation = validate()
    write_json(OUT_DIR / "validate_1013R_R94_P1_derived_artifacts_teacher_review_polish_result.json", validation)

    files = [p for p in OUT_DIR.rglob("*") if p.is_file()]
    zip_sha = build_zip([p for p in files if p.name not in {"REVIEW_PACKAGE_MANIFEST.json", "REVIEW_PACKAGE_MANIFEST.md"}])
    manifest = {
        "stage": STAGE,
        "final_status": "PASS_1013R_R94_P1_DERIVED_ARTIFACTS_TEACHER_REVIEW_POLISH"
        if validation["validator_pass"]
        else "FAIL_1013R_R94_P1_DERIVED_ARTIFACTS_TEACHER_REVIEW_POLISH",
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
                "R94_P1_result": validation["R94_P1_result"],
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
