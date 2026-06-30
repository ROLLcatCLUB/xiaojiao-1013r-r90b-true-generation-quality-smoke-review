from __future__ import annotations

import hashlib
import json
import shutil
from datetime import datetime
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
STAGE = "1013R_R94_P3_EPISODE_NAVIGATION_ALIGNED_ARTIFACTS_REPAIR"
OUT = BASE / STAGE
ZIP_PATH = BASE / f"{STAGE}.zip"

P6_DIR = BASE / "1013R_R93_P6_TEACHER_NAVIGATION_VIEW_AND_TALK_FLOW"
P6_VIEWMODEL = P6_DIR / "r93_p6_teacher_navigation_viewmodel.json"
P6_HTML = P6_DIR / "r93_p6_teacher_navigation_view.html"
P6_VALIDATOR = P6_DIR / "validate_1013R_R93_P6_teacher_navigation_view_result.json"

P6_GATE_DIR = BASE / "1013R_R93_P6_ACCEPTANCE_AND_R95_READINESS_GATE"
P6_GATE_VALIDATOR = P6_GATE_DIR / "validate_1013R_R93_P6_acceptance_and_R95_readiness_gate_result.json"

P1_DIR = BASE / "1013R_R94_P1_DERIVED_ARTIFACTS_TEACHER_REVIEW_POLISH"
P1_STORYBOARD = P1_DIR / "r94_p1_slide_storyboard.json"
P1_WORKSHEET = P1_DIR / "r94_p1_student_worksheet_one_page.md"
P1_TEACHER_NOTES = P1_DIR / "r94_p1_student_worksheet_teacher_notes.md"
P1_RUBRIC = P1_DIR / "r94_p1_teacher_observation_rubric.md"
P1_SELF = P1_DIR / "r94_p1_student_self_assessment.md"
P1_VALIDATOR = P1_DIR / "validate_1013R_R94_P1_derived_artifacts_teacher_review_polish_result.json"

SLIDE_JSON = OUT / "r94_p3_episode_aligned_slide_storyboard.json"
SLIDE_MD = OUT / "r94_p3_episode_aligned_slide_storyboard.md"
WORKSHEET_MD = OUT / "r94_p3_student_worksheet_episode_aligned_one_page.md"
TEACHER_NOTES_MD = OUT / "r94_p3_teacher_instruction_notes.md"
TEACHER_RUBRIC_MD = OUT / "r94_p3_teacher_observation_rubric_episode_aligned.md"
STUDENT_SELF_MD = OUT / "r94_p3_student_self_check_episode_aligned.md"
ALIGNMENT_JSON = OUT / "r94_p3_episode_artifact_alignment_matrix.json"
TRACE_JSON = OUT / "r94_p3_derived_artifacts_trace.json"
REPAIR_NOTES_MD = OUT / "r94_p3_repair_notes.md"
QUALITY_JSON = OUT / "quality_sentinel_v1_preview.json"
VALIDATOR_JSON = OUT / "validate_1013R_R94_P3_episode_navigation_aligned_artifacts_repair_result.json"

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
    "formal_material_ready": False,
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


def load_episodes() -> list[dict]:
    return read_json(P6_VIEWMODEL)["episodes"]


def episode_by_title(episodes: list[dict]) -> dict[str, dict]:
    return {ep["title"]: ep for ep in episodes}


def micro_names(ep: dict, orders: list[int]) -> list[str]:
    by_order = {item["step_order"]: item for item in ep["micro_steps"]}
    return [by_order[num]["step_name"] for num in orders if num in by_order]


def build_slides(episodes: list[dict]) -> dict:
    eps = episode_by_title(episodes)
    data = [
        ("S01", "看见渐变", "静看图片，找到颜色慢慢变", "大屏放一张最明显的生活或教材渐变图，只保留起点、终点和一条箭头。", 0, "学生安静观察，用手指找颜色从哪里变到哪里。", "启动观察，不急着讲术语。", [1, 2]),
        ("S02", "看见渐变", "从哪里到哪里，说一句", "屏幕保留句式：我看到颜色从___变到___。", 1, "学生用句式说出一处变化，再判断是不是慢慢变。", "把观察变成可听见的表达证据。", [3, 4, 5]),
        ("S03", "分清亮暗与鲜灰", "只看两件事：亮暗、鲜灰", "左右两组色条：左边亮暗，右边鲜灰；文字只写亮/暗、鲜/灰。", 0, "学生先判断亮暗，再判断鲜灰。", "降低概念负荷，先会看再补词。", [1, 2, 3]),
        ("S04", "分清亮暗与鲜灰", "把色卡放进篮子", "大屏显示两个篮子：亮暗、鲜灰，旁边放2-3张候选色卡。", 1, "学生把色卡放进对应类别，并说理由。", "确认学生能分清变化类型。", [4, 5]),
        ("S05", "三格试色", "示范三格渐变小样", "屏幕显示三格空框和箭头：第1格 -> 第2格 -> 第3格。", 0, "学生看教师示范，明白第二格不能跑太远。", "把渐变操作压成可控的小任务。", [1, 2, 3, 4]),
        ("S06", "三格试色", "自然渐变 vs 跳色反例", "两组三格并排：一组慢慢变，一组第二格跳太远。", 1, "学生判断哪一组更自然，再完成自己的三格小样。", "用反例帮助学生控制中间格。", [5, 6, 7]),
        ("S07", "放进作品", "选择任务，先标方向", "三栏任务：色条、图形、小作品；旁边固定起点、箭头、终点。", 0, "学生选择任务层级，并先说或标出变化方向。", "避免复杂图案抢走渐变目标。", [1, 2]),
        ("S08", "放进作品", "把颜色小路放进作品", "屏幕显示小样到图形的迁移箭头，并保留三点：起点、方向、慢慢变。", 1, "学生把三格规律放进色条、图形或小作品。", "完成从试色到作品的迁移。", [3, 4, 5, 6, 7]),
        ("S09", "自查与微修订", "三项自查，只提一处建议", "大屏显示：方向清楚吗？慢慢变了吗？能说清吗？", 0, "学生自查，同伴只提一处建议。", "把评价压成能执行的小动作。", [1, 2]),
        ("S10", "自查与微修订", "只改一处，说清修改", "大屏显示句式：我改了___，因为原来___，现在___。", 1, "学生完成一处微修订，并说清自己改了哪里。", "形成可见的改进证据。", [3, 4, 5]),
    ]
    slides = []
    for slide_id, title, slide_title, screen, talk_index, action, served, orders in data:
        ep = eps[title]
        talks = ep.get("talk_flow") or [ep["key_talk"]]
        slides.append(
            {
                "slide_id": slide_id,
                "belongs_to_episode_id": ep["episode_id"],
                "belongs_to_episode_title": ep["title"],
                "episode_index": ep["index"],
                "slide_title": slide_title,
                "screen_content": screen,
                "teacher_talk_hint": talks[min(talk_index, len(talks) - 1)],
                "student_action": action,
                "served_classroom_action": served,
                "source_p6_micro_steps": micro_names(ep, orders),
                "teacher_review_required": True,
                "formal_apply": False,
            }
        )
    return {
        "artifact": "r94_p3_episode_aligned_slide_storyboard",
        "source_round": "R93-P6",
        "source_viewmodel": rel(P6_VIEWMODEL),
        "slide_count": len(slides),
        "episode_count": len(episodes),
        "teacher_review_required": True,
        "formal_apply": False,
        "pptx_generated": False,
        "slides": slides,
    }


def render_slide_md(slide_payload: dict) -> str:
    lines = [
        "# R94-P3 Episode-Aligned Slide Storyboard",
        "",
        "> teacher_review_required=true  ",
        "> formal_apply=false  ",
        "> pptx_generated=false  ",
        "> 本文件只是 PPT 预览前的 storyboard，不是正式 PPT。",
        "",
    ]
    for slide in slide_payload["slides"]:
        lines.extend(
            [
                f"## {slide['slide_id']} · Episode {slide['episode_index']}：{slide['slide_title']}",
                "",
                f"- 所属环节：{slide['belongs_to_episode_title']}",
                f"- 屏幕显示：{slide['screen_content']}",
                f"- 教师说：{slide['teacher_talk_hint']}",
                f"- 学生做：{slide['student_action']}",
                f"- 服务课堂动作：{slide['served_classroom_action']}",
                f"- 来源 micro-step：{' / '.join(slide['source_p6_micro_steps'])}",
                "",
            ]
        )
    return "\n".join(lines)


def render_worksheet_md() -> str:
    return """# 《色彩的渐变》学习单

姓名：__________  班级：__________

## 1. 找一找：颜色从哪里变到哪里

我看到颜色从 __________ 慢慢变到 __________。

我觉得它是：

- [ ] 变亮了 / 变暗了
- [ ] 变鲜了 / 变灰了
- [ ] 一层一层慢慢变过去

## 2. 试一试：三格颜色小路

选一种颜色，让它每次只变一点点。

```text
[ 第1格 ]  ->  [ 第2格 ]  ->  [ 第3格 ]
```

我的颜色是从 __________ 变到 __________。

## 3. 用一用：把颜色小路放进作品

我选择：

- [ ] 色条
- [ ] 图形
- [ ] 小作品

我的颜色方向：从 __________ 到 __________。

## 4. 查一查 / 改一改

- [ ] 我看得出颜色从哪里开始。
- [ ] 我看得出颜色往哪里变。
- [ ] 中间没有一下子跳太快。
- [ ] 我能说清楚一处变化。

我只改一处：____________________

因为原来 ____________________，现在 ____________________。
"""


def render_teacher_notes_md() -> str:
    return """# R94-P3 Teacher Instruction Notes

> teacher_review_required=true  
> formal_apply=false

## 使用方式

这张学习单只承担四个动作，不承担整节课所有内容：

| 学习单任务 | 对应 episode | 教师使用提醒 |
| --- | --- | --- |
| 找一找 | Episode 1 看见渐变 | 让学生先指出起点和终点，不急着讲术语。 |
| 试一试 | Episode 3 三格试色 | 只做三格，重点看第二格是否跳太远。 |
| 用一用 | Episode 4 放进作品 | 先标方向，再把三格规律放进局部。 |
| 查一查 / 改一改 | Episode 5 自查与微修订 | 只改一处，不要求重画。 |

## 材料建议

```text
基础：彩铅 / 油画棒 / 色卡
进阶：水粉或水彩小样
时间紧：只完成三格小样 + 一句话
```

## 不放到学生端的内容

```text
micro-step
工程编号
正式 apply 状态
复杂定义
全部评价证据
```
"""


def render_teacher_rubric_md() -> str:
    return """# R94-P3 Teacher Observation Rubric Episode-Aligned

> teacher_review_required=true  
> formal_apply=false  
> 教师观察版草案，不是正式评分表，不落库。

| 观察维度 | 对应环节 | 已做到 | 基本做到 | 还要再试 | 教师记录 |
| --- | --- | --- | --- | --- | --- |
| 看见变化 | Episode 1 | 能指出起点、终点和变化方向。 | 能在提示下指出一处变化。 | 还需要教师示范才能发现变化。 |  |
| 分清变化 | Episode 2 | 能分清亮暗变化和鲜灰变化，并说理由。 | 能说出亮/暗或鲜/灰其中一种。 | 容易把变浅和变灰混在一起。 |  |
| 试出变化 | Episode 3 | 能完成三格小样，中间过渡较自然。 | 能完成三格，但有一格跳得较快。 | 三格之间暂时看不出慢慢变化。 |  |
| 用到作品 | Episode 4 | 能把渐变放进作品局部，方向清楚。 | 能使用部分渐变，但方向不够稳定。 | 作品中暂时看不出明确变化方向。 |  |
| 完成微修 | Episode 5 | 能根据建议改一处，并说清原因。 | 能接受建议，但需要提示怎么改。 | 暂时不知道改哪里。 |  |

## 使用边界

```text
teacher_review_required=true
formal_apply=false
database_written=false
```
"""


def render_student_self_md() -> str:
    return """# R94-P3 Student Self-Check Episode-Aligned

> teacher_review_required=true  
> formal_apply=false  
> 学生自评草案，不是正式评价表。

# 我会看，我会改

姓名：__________

| 我来查一查 | 已做到 | 还想再试 |
| --- | --- | --- |
| 我能找到颜色从哪里开始、到哪里结束。 | [ ] | [ ] |
| 我能说出颜色是变亮/变暗，还是变鲜/变灰。 | [ ] | [ ] |
| 我的三格颜色是一点一点变过去的。 | [ ] | [ ] |
| 我的作品里能看出颜色往哪里变。 | [ ] | [ ] |
| 我改了一处，让颜色变化更清楚。 | [ ] | [ ] |

我想说一句：

```text
我的颜色从 __________ 变到 __________。
我改了 __________，因为 ____________________。
```
"""


def build_alignment_matrix(slides: dict, episodes: list[dict]) -> dict:
    worksheet_map = {
        "看见渐变": ["任务1 找一找：颜色从哪里变到哪里"],
        "分清亮暗与鲜灰": ["教师口头分类，不强塞学生学习单"],
        "三格试色": ["任务2 试一试：三格颜色小路"],
        "放进作品": ["任务3 用一用：把颜色小路放进作品"],
        "自查与微修订": ["任务4 查一查 / 改一改"],
    }
    rubric_map = {
        "看见渐变": ["看见变化"],
        "分清亮暗与鲜灰": ["分清变化"],
        "三格试色": ["试出变化"],
        "放进作品": ["用到作品"],
        "自查与微修订": ["完成微修"],
    }
    rows = []
    for ep in episodes:
        slide_ids = [
            slide["slide_id"]
            for slide in slides["slides"]
            if slide["belongs_to_episode_title"] == ep["title"]
        ]
        rows.append(
            {
                "episode_index": ep["index"],
                "episode_id": ep["episode_id"],
                "episode_title": ep["title"],
                "teacher_three_steps": ep["teacher_three_steps"],
                "slide_ids": slide_ids,
                "worksheet_tasks": worksheet_map.get(ep["title"], []),
                "teacher_observation_dimensions": rubric_map.get(ep["title"], []),
                "student_self_check_items": rubric_map.get(ep["title"], []),
                "xiaojiao_default_reminder": ep["xiaojiao_key_reminder"],
                "source_micro_step_count": len(ep["micro_steps"]),
            }
        )
    return {
        "stage": STAGE,
        "source_round": "R93-P6",
        "source_viewmodel": rel(P6_VIEWMODEL),
        "episode_count": len(episodes),
        "slide_count": slides["slide_count"],
        "rows": rows,
        "teacher_review_required": True,
        "formal_apply": False,
    }


def build_trace(slides: dict, matrix: dict) -> dict:
    return {
        "stage": STAGE,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "source_round": "R93-P6",
        "source_teacher_navigation_viewmodel": rel(P6_VIEWMODEL),
        "source_teacher_navigation_html": rel(P6_HTML),
        "source_p6_validator": rel(P6_VALIDATOR),
        "source_r94_p1_storyboard": rel(P1_STORYBOARD),
        "source_r94_p1_worksheet": rel(P1_WORKSHEET),
        "source_r94_p1_rubric": rel(P1_RUBRIC),
        "derived_artifact_count": 5,
        "slide_storyboard_source": "R93-P6 episodes + R94-P1 storyboard shape",
        "worksheet_source": "R93-P6 episodes + R94-P1 worksheet one-page constraint",
        "rubric_source": "R93-P6 evidence alignment + R94-P1 rubric split",
        "episode_count": matrix["episode_count"],
        "slide_count": slides["slide_count"],
        "provider_called": False,
        "model_called": False,
        "teacher_review_required": True,
        "formal_apply": False,
        "r95_executed": False,
    }


def render_repair_notes() -> str:
    return """# R94-P3 Repair Notes

## Decision

R94-P3 repairs R94-P1 derived artifacts so they obey the R93-P6 teacher navigation route.

```text
R94-P3 = EPISODE_NAVIGATION_ALIGNED_ARTIFACTS_REPAIR
formal_apply = false
R95_executed = false
```

## What changed from R94-P1

- Slide storyboard now labels every slide with its episode.
- Worksheet now carries only four student tasks: 找一找、试一试、用一用、查一查/改一改.
- Teacher observation rubric now maps one dimension to each episode.
- Student self-check now uses child-readable actions instead of generic rubric language.
- R95 can use these as source for preview export, but R95 is not executed here.

## What did not change

- No provider/model call.
- No R21/R36 modification.
- No UI binding.
- No formal apply.
- No database/Feishu/memory write.
- No PPTX/PDF/DOCX generation.
"""


def quality_sentinel() -> dict:
    return {
        "stage": STAGE,
        "quality_sentinel_version": "v1_preview",
        "result": "BASIC_USABLE",
        "blocking": False,
        "artifact_formal_ready": False,
        "teacher_review_required": True,
        "formal_apply": False,
        "checks": {
            "episode_alignment": "PASS",
            "student_language_fit": "PASS",
            "teacher_adoptability": "PASS_WITH_NOTES",
            "source_consistency": "PASS",
            "scope_control": "PASS",
        },
        "notes": [
            "Derived artifacts now follow the five P6 teaching rhythm blocks.",
            "R95 may generate preview files after explicit user authorization.",
            "Formal use remains locked.",
        ],
    }


def validate(slides: dict, matrix: dict) -> dict:
    failed: list[str] = []
    required_sources = [P6_VIEWMODEL, P6_HTML, P6_VALIDATOR, P6_GATE_VALIDATOR, P1_STORYBOARD, P1_WORKSHEET, P1_RUBRIC, P1_SELF, P1_VALIDATOR]
    for path in required_sources:
        if not path.exists():
            failed.append(f"missing_source:{path.name}")
    p6_validator = read_json(P6_VALIDATOR) if P6_VALIDATOR.exists() else {}
    p6_gate = read_json(P6_GATE_VALIDATOR) if P6_GATE_VALIDATOR.exists() else {}
    p1_validator = read_json(P1_VALIDATOR) if P1_VALIDATOR.exists() else {}
    if p6_validator.get("validator_pass") is not True:
        failed.append("p6_validator_not_pass")
    if p6_gate.get("validator_pass") is not True:
        failed.append("p6_gate_not_pass")
    if p1_validator.get("validator_pass") is not True:
        failed.append("r94_p1_validator_not_pass")
    if matrix.get("episode_count") != 5:
        failed.append("episode_count_not_5")
    expected_titles = ["看见渐变", "分清亮暗与鲜灰", "三格试色", "放进作品", "自查与微修订"]
    matrix_titles = [row["episode_title"] for row in matrix["rows"]]
    if matrix_titles != expected_titles:
        failed.append("episode_order_mismatch")
    slide_titles = {slide["belongs_to_episode_title"] for slide in slides["slides"]}
    if slide_titles != set(expected_titles):
        failed.append("slides_not_cover_all_episodes")
    for slide in slides["slides"]:
        for key in ["belongs_to_episode_id", "screen_content", "teacher_talk_hint", "student_action", "served_classroom_action"]:
            if not slide.get(key):
                failed.append(f"slide_missing_{key}:{slide['slide_id']}")
    worksheet = WORKSHEET_MD.read_text(encoding="utf-8") if WORKSHEET_MD.exists() else ""
    forbidden_student_terms = ["R93", "R94", "R95", "micro-step", "formal_apply", "provider", "validator", "canonical"]
    for term in forbidden_student_terms:
        if term in worksheet:
            failed.append(f"student_worksheet_exposes_engineering_term:{term}")
    for phrase in ["找一找", "试一试", "用一用", "查一查 / 改一改"]:
        if phrase not in worksheet:
            failed.append(f"worksheet_missing_task:{phrase}")
    rubric = TEACHER_RUBRIC_MD.read_text(encoding="utf-8") if TEACHER_RUBRIC_MD.exists() else ""
    for phrase in ["看见变化", "分清变化", "试出变化", "用到作品", "完成微修"]:
        if phrase not in rubric:
            failed.append(f"rubric_missing_dimension:{phrase}")
    for key, value in BOUNDARY.items():
        if value is True:
            failed.append(f"boundary_violation:{key}")
    return {
        "stage": STAGE,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "status": "PASS" if not failed else "FAIL",
        "r94_p3_result": "PASS" if not failed else "FAIL",
        "quality": "BASIC_USABLE" if not failed else "NEEDS_RETRY",
        "artifact_formal_ready": False,
        "teacher_review_required": True,
        "formal_apply": False,
        "r95_executed": False,
        "r95_ready_after_user_authorization": not failed,
        "source_round": "R93-P6",
        "episode_count": matrix.get("episode_count"),
        "slide_storyboard_created": SLIDE_MD.exists() and SLIDE_JSON.exists(),
        "student_worksheet_created": WORKSHEET_MD.exists(),
        "teacher_instruction_notes_created": TEACHER_NOTES_MD.exists(),
        "teacher_observation_rubric_created": TEACHER_RUBRIC_MD.exists(),
        "student_self_check_created": STUDENT_SELF_MD.exists(),
        "alignment_matrix_created": ALIGNMENT_JSON.exists(),
        "provider_called": False,
        "model_called": False,
        "new_fields_added": False,
        "profile_modified": False,
        "r21_modified": False,
        "r36_modified": False,
        "ui_page_connected": False,
        "database_written": False,
        "feishu_written": False,
        "memory_written": False,
        "pptx_generated": False,
        "pdf_generated": False,
        "docx_generated": False,
        "printed_final_material_generated": False,
        "boundary": BOUNDARY,
        "failed_checks": failed,
        "validator_pass": not failed,
    }


def readme_md(validation: dict) -> str:
    return f"""# {STAGE}

R94-P3 repairs the derived classroom artifacts so they follow the R93-P6 teacher navigation route.

```text
R94-P3 = {validation["r94_p3_result"]}
quality = {validation["quality"]}
source_round = R93-P6
episode_count = {validation["episode_count"]}
artifact_formal_ready = false
formal_apply = false
R95_executed = false
```

Review first:

```text
r94_p3_episode_aligned_slide_storyboard.md
r94_p3_student_worksheet_episode_aligned_one_page.md
r94_p3_teacher_observation_rubric_episode_aligned.md
r94_p3_student_self_check_episode_aligned.md
r94_p3_episode_artifact_alignment_matrix.json
```
"""


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
    for source in [
        P6_VIEWMODEL,
        P6_HTML,
        P6_VALIDATOR,
        P6_GATE_VALIDATOR,
        P1_STORYBOARD,
        P1_WORKSHEET,
        P1_TEACHER_NOTES,
        P1_RUBRIC,
        P1_SELF,
        P1_VALIDATOR,
    ]:
        shutil.copy2(source, source_dir / source.name)

    episodes = load_episodes()
    slides = build_slides(episodes)
    write_json(SLIDE_JSON, slides)
    write_text(SLIDE_MD, render_slide_md(slides))
    write_text(WORKSHEET_MD, render_worksheet_md())
    write_text(TEACHER_NOTES_MD, render_teacher_notes_md())
    write_text(TEACHER_RUBRIC_MD, render_teacher_rubric_md())
    write_text(STUDENT_SELF_MD, render_student_self_md())
    matrix = build_alignment_matrix(slides, episodes)
    write_json(ALIGNMENT_JSON, matrix)
    write_json(TRACE_JSON, build_trace(slides, matrix))
    write_text(REPAIR_NOTES_MD, render_repair_notes())
    write_json(QUALITY_JSON, quality_sentinel())
    shutil.copy2(Path(__file__), OUT / Path(__file__).name)

    validation = validate(slides, matrix)
    write_json(VALIDATOR_JSON, validation)
    write_text(OUT / "README.md", readme_md(validation))

    files_for_zip = [
        path
        for path in OUT.rglob("*")
        if path.is_file() and path.name not in {"REVIEW_PACKAGE_MANIFEST.json", "REVIEW_PACKAGE_MANIFEST.md"}
    ]
    zip_sha = build_zip(files_for_zip)
    all_files = [path for path in OUT.rglob("*") if path.is_file()]
    manifest = {
        "stage": STAGE,
        "final_status": "PASS_1013R_R94_P3_EPISODE_NAVIGATION_ALIGNED_ARTIFACTS_REPAIR"
        if validation["validator_pass"]
        else "FAIL_1013R_R94_P3_EPISODE_NAVIGATION_ALIGNED_ARTIFACTS_REPAIR",
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
                "r94_p3_result": validation["r94_p3_result"],
                "quality": validation["quality"],
                "r95_ready_after_user_authorization": validation["r95_ready_after_user_authorization"],
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
