from __future__ import annotations

import hashlib
import html
import json
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
STAGE = "1013R_R93_P3_CLASSROOM_FLOW_TEACHING_EPISODE_DEEPENING"
OUT = BASE / STAGE

P2_DIR = BASE / "1013R_R93_P2_TEXTBOOK_ANCHOR_CLOSURE_AND_FINAL_PREVIEW_DRAFT"
P2_DRAFT = P2_DIR / "r93_p2_final_preview_lesson_draft.md"
P2_ANCHOR = P2_DIR / "textbook_anchor_closure.md"
P2_VALIDATOR = P2_DIR / "validate_1013R_R93_P2_textbook_anchor_closure_final_preview_draft_result.json"

R94_P1_DIR = BASE / "1013R_R94_P1_DERIVED_ARTIFACTS_TEACHER_REVIEW_POLISH"
STORYBOARD_JSON = R94_P1_DIR / "r94_p1_slide_storyboard.json"
WORKSHEET_JSON = R94_P1_DIR / "r94_p1_student_worksheet_structured.json"
ASSESSMENT_JSON = R94_P1_DIR / "r94_p1_assessment_structured.json"
R94_P1_TRACE = R94_P1_DIR / "r94_p1_derived_artifacts_trace.json"
R94_P1_VALIDATOR = R94_P1_DIR / "validate_1013R_R94_P1_derived_artifacts_teacher_review_polish_result.json"

R94_P2_DIR = BASE / "1013R_R94_P2_TEACHER_FACING_LESSON_PACKAGE_OVERVIEW"
R94_P2_VIEWMODEL = R94_P2_DIR / "r94_p2_teacher_facing_viewmodel.json"
R94_P2_VALIDATOR = R94_P2_DIR / "validate_1013R_R94_P2_teacher_facing_overview_result.json"

SCHEMA_OUT = OUT / "teaching_episode_schema_1013R_R93_P3.json"
RUNBOOK_MD_OUT = OUT / "r93_p3_teaching_episode_runbook.md"
RUNBOOK_JSON_OUT = OUT / "r93_p3_teaching_episode_runbook.json"
MAPPING_OUT = OUT / "r93_p3_episode_to_field_mapping.json"
XIAOJIAO_OUT = OUT / "r93_p3_xiaojiao_support_plan.md"
READING_HIERARCHY_OUT = OUT / "r93_p3_teacher_reading_hierarchy_notes.md"
HTML_OUT = OUT / "r93_p3_teacher_facing_episode_preview.html"
QUALITY_OUT = OUT / "quality_sentinel_v1_preview.json"
VALIDATOR_OUT = OUT / "validate_1013R_R93_P3_classroom_flow_teaching_episode_deepening_result.json"

BOUNDARY = {
    "teacher_review_required": True,
    "preview_only": True,
    "provider_called": False,
    "model_called": False,
    "new_fields_added_to_profile": False,
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
    "multi_case_regression_executed": False,
}


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def esc(value: object) -> str:
    return html.escape("" if value is None else str(value), quote=True)


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT)).replace("/", "\\")


def ul(items: list[str]) -> str:
    return "".join(f"<li>{esc(item)}</li>" for item in items)


def md_list(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items)


def build_schema() -> dict:
    return {
        "schema_id": "teaching_episode_schema_1013R_R93_P3",
        "status": "preview_only",
        "profile_id": "art_lesson_design_profile_v1",
        "profile_modified": False,
        "description": "A teacher-facing intermediate object that reorganizes existing lesson fields and derived artifacts into classroom episodes.",
        "required_episode_keys": [
            "episode_id",
            "title",
            "duration",
            "episode_goal",
            "design_intent",
            "screen_plan",
            "teacher_moves",
            "student_moves",
            "student_scaffolds",
            "xiaojiao_support",
            "common_misconceptions",
            "fallback_strategies",
            "evidence",
            "transition",
        ],
        "boundary": BOUNDARY,
    }


def build_runbook() -> dict:
    return {
        "stage": STAGE,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "lesson": {
            "title": "色彩的渐变",
            "unit": "第二单元《多彩的世界》",
            "grade": "三年级",
            "textbook_anchor": "教材第6-7页，核心板块为色彩的明度与纯度、渐变的调色游戏。",
            "status": "TEACHING_EPISODE_RUNBOOK_READY",
            "teacher_review_required": True,
            "preview_only": True,
            "formal_apply": False,
        },
        "classroom_spine": [
            "先让学生看见颜色慢慢变化。",
            "再把变化分成亮暗与鲜灰两类。",
            "接着通过三格试色把规律做出来。",
            "然后把试色规律迁移到作品。",
            "最后用自查和微修订把评价落到作品改进上。",
        ],
        "episodes": [
            {
                "episode_id": "episode_01_notice_gradient",
                "title": "看见渐变",
                "duration": "约5分钟",
                "episode_goal": "学生能从生活图或教材图中指出颜色从哪里开始、变到哪里。",
                "design_intent": "先用直观观察建立“慢慢变”的经验，避免一上来讲明度、纯度造成负担。",
                "screen_plan": {
                    "main_visual": "天空、山峦、花朵或教材页局部三图并排，每张图只保留一个箭头。",
                    "screen_text": ["找一找：颜色从哪里变到哪里？", "用手指一指变化方向。"],
                    "board_or_annotation": "圈出起点和终点，用箭头标出变化方向。",
                },
                "teacher_moves": {
                    "action": "出示图片，先请学生安静观察，再邀请学生用手指出颜色变化方向。",
                    "talk": "先不急着说专业词。你只要找到：颜色从哪里开始，慢慢变到了哪里。",
                    "probe": [
                        "你是从哪里看出它在慢慢变的？",
                        "它是一下一下跳过去，还是一层一层变过去？",
                    ],
                },
                "student_moves": {
                    "look": "观察图片中的颜色层次。",
                    "do": "用手指从颜色起点滑到终点。",
                    "say": "我看到颜色从___变到___。",
                },
                "student_scaffolds": {
                    "language": ["从___到___", "颜色慢慢变过去"],
                    "material": "图片箭头、起点终点标记。",
                    "peer": "同桌先互相指一处，再全班分享。",
                },
                "xiaojiao_support": {
                    "hint_card": "如果学生只说“好看”，提示他说清起点和终点。",
                    "probe_card": "它中间有没有一层一层的变化？",
                    "misconception_alert": "学生可能把颜色多误认为渐变。",
                    "evidence_note": "记录能说出“从___到___”的学生。",
                },
                "common_misconceptions": ["把颜色丰富等同于渐变。", "只说好看，不说变化方向。"],
                "fallback_strategies": ["减少图片数量，只保留一张最清楚的图。", "让学生先用手指，不急着口头表达。"],
                "evidence": {
                    "process": "学生能圈出或指出起点与终点。",
                    "expression": "学生能说出一句“从___到___”。",
                    "teacher_observation": "看学生是否能发现连续变化，而不是只看见多个颜色。",
                },
                "transition": "既然能看见颜色慢慢变，接下来要分一分：它是在变亮变暗，还是变鲜变灰。",
            },
            {
                "episode_id": "episode_02_distinguish_brightness_saturation",
                "title": "分清亮暗与鲜灰",
                "duration": "约7分钟",
                "episode_goal": "学生能用儿童化语言初步区分亮暗变化和鲜灰变化。",
                "design_intent": "教材页同时出现明度与纯度，先用“亮暗、鲜灰”建立直观判断，再轻轻对应专业词。",
                "screen_plan": {
                    "main_visual": "左侧一组由深到浅的色条，右侧一组由鲜到灰的色条。",
                    "screen_text": ["亮一点 / 暗一点", "鲜一点 / 灰一点"],
                    "board_or_annotation": "板书两列：亮暗；鲜灰。教师可在旁边小字写明度、纯度。",
                },
                "teacher_moves": {
                    "action": "先指左侧色条问亮暗，再指右侧色条问鲜灰，最后组织分类。",
                    "talk": "我们先不用急着记词。你只要先看出来：它是变亮了，还是变灰了？",
                    "probe": [
                        "你看的是颜色亮不亮，还是鲜不鲜？",
                        "这组颜色越来越亮，还是越来越灰？",
                    ],
                },
                "student_moves": {
                    "look": "观察两组色条。",
                    "do": "把色条或色卡放到“亮暗”或“鲜灰”类别。",
                    "say": "这一组颜色从___变得更___。",
                },
                "student_scaffolds": {
                    "language": ["越来越亮", "越来越暗", "越来越鲜", "越来越灰"],
                    "material": "两组对比色条、分类卡。",
                    "peer": "同桌先判断，再举卡表达。",
                },
                "xiaojiao_support": {
                    "hint_card": "先问学生看的是亮不亮，还是鲜不鲜。",
                    "probe_card": "如果只能选一个词，你会选亮、暗、鲜、灰里的哪一个？",
                    "misconception_alert": "学生可能把变浅和变灰混为一谈。",
                    "evidence_note": "记录能完成分类并说出理由的学生。",
                },
                "common_misconceptions": ["把颜色变浅都说成变灰。", "只记明度、纯度词语，不会判断。"],
                "fallback_strategies": ["暂时不要求说专业词，只要求分到亮暗或鲜灰。", "用更夸张的两组色条降低判断难度。"],
                "evidence": {
                    "process": "学生能把色条放入正确类别。",
                    "expression": "学生能用“越来越___”说明变化。",
                    "teacher_observation": "看学生是否能区分亮暗与鲜灰，而不是只说颜色名称。",
                },
                "transition": "能看出来还不够，下一步我们试着自己做出三格慢慢变化。",
            },
            {
                "episode_id": "episode_03_three_step_color_trial",
                "title": "三格试色",
                "duration": "约8分钟",
                "episode_goal": "学生能完成三格或五格连续变化小样，知道每次只变一点点。",
                "design_intent": "把概念转成可操作的小任务，降低完整创作前的风险。",
                "screen_plan": {
                    "main_visual": "三格小样示范：第一格原色，第二格轻微变化，第三格继续变化。",
                    "screen_text": ["每次只变一点点", "第1格 -> 第2格 -> 第3格"],
                    "board_or_annotation": "标出变化箭头，圈出跳色太快的反例。",
                },
                "teacher_moves": {
                    "action": "现场示范三格小样，展示一个自然例和一个跳色反例。",
                    "talk": "先把颜色排好队，再放进你的作品里。第二格不要跑太远，它要像第一格的朋友。",
                    "probe": [
                        "第二格更像第一格，还是一下子跳到第三格？",
                        "如果太突然，你准备把哪一格改一改？",
                    ],
                },
                "student_moves": {
                    "look": "观察教师示范和反例。",
                    "do": "选择亮暗或鲜灰路线，完成三格小样。",
                    "say": "我的颜色从___变到___，中间越来越___。",
                },
                "student_scaffolds": {
                    "language": ["第一格是___", "第二格更___", "第三格更___"],
                    "material": "三格空框、小样纸、色卡或颜料。",
                    "peer": "同桌帮看中间有没有跳太快。",
                },
                "xiaojiao_support": {
                    "hint_card": "提醒学生先做三格，不急着画完整作品。",
                    "probe_card": "中间这一格能不能再靠近第一格一点？",
                    "misconception_alert": "学生可能把三种不同颜色并排当成渐变。",
                    "evidence_note": "保留三格小样作为过程证据。",
                },
                "common_misconceptions": ["颜色跳太快。", "只换颜色，不形成连续变化。", "水分或力度不均导致颜色脏。"],
                "fallback_strategies": ["材料复杂时改用彩铅、油画棒或色卡排列。", "只要求三格，不要求五格。"],
                "evidence": {
                    "process": "学生完成三格小样。",
                    "work": "小样能看出连续变化。",
                    "teacher_observation": "看学生是否能控制中间色，不让变化突然断开。",
                },
                "transition": "小样做好了，接下来把这条变化规律放进你的图形或小作品里。",
            },
            {
                "episode_id": "episode_04_apply_to_artwork",
                "title": "放进作品",
                "duration": "约14分钟",
                "episode_goal": "学生能把试色规律迁移到色条、图形或小作品中。",
                "design_intent": "让渐变从练习变成艺术表现，避免停留在色卡层面。",
                "screen_plan": {
                    "main_visual": "展示三类任务：基础色条、进阶图形、挑战小作品。",
                    "screen_text": ["基础：三格色条", "进阶：放进图形", "挑战：放进小作品"],
                    "board_or_annotation": "提示起点、方向、中间过渡三个检查点。",
                },
                "teacher_moves": {
                    "action": "发布分层任务，巡视时只抓起点、方向、过渡三个点。",
                    "talk": "你不需要画很复杂。今天最重要的是让别人看出颜色是怎样慢慢变过去的。",
                    "probe": [
                        "你的颜色从哪里开始变？",
                        "别人一眼能看出变化方向吗？",
                        "你最想让哪一处颜色变得更自然？",
                    ],
                },
                "student_moves": {
                    "look": "看任务选择和示例。",
                    "do": "选择基础、进阶或挑战任务完成作品。",
                    "say": "我把渐变放在___，颜色从___变到___。",
                },
                "student_scaffolds": {
                    "language": ["我选择___任务", "我的变化方向是___"],
                    "material": "色条模板、图形轮廓、小样纸、学习单。",
                    "peer": "同桌先看方向是否清楚。",
                },
                "xiaojiao_support": {
                    "hint_card": "如果学生画面太复杂，提醒先保证一条清楚的渐变。",
                    "probe_card": "这幅作品里最清楚的一段渐变在哪里？",
                    "misconception_alert": "学生可能追求复杂图案，忽略渐变规律。",
                    "evidence_note": "记录作品中能看出明确变化方向的例子。",
                },
                "common_misconceptions": ["图案太复杂，渐变看不出来。", "只涂满颜色，没有方向。"],
                "fallback_strategies": ["时间不足时只完成一个色条或局部。", "让学生把小样直接贴入作品作为局部设计。"],
                "evidence": {
                    "work": "作品或局部设计中有明确渐变方向。",
                    "expression": "学生能说出渐变放在哪里。",
                    "teacher_observation": "看学生是否把试色规律迁移到作品中。",
                },
                "transition": "作品有了变化方向，最后我们用自查表看一看：哪里已经清楚，哪里还可以微修。",
            },
            {
                "episode_id": "episode_05_self_check_revision",
                "title": "自查与微修订",
                "duration": "约6分钟",
                "episode_goal": "学生能依据自查或同伴建议，完成一处小修改并说清变化。",
                "design_intent": "把评价落到作品改进上，而不是只停留在展示和表扬。",
                "screen_plan": {
                    "main_visual": "一张作品局部，旁边显示修改前后小箭头。",
                    "screen_text": ["看得出方向吗？", "中间跳太快了吗？", "我能改一处吗？"],
                    "board_or_annotation": "只改一处即可，不要求重画。",
                },
                "teacher_moves": {
                    "action": "组织学生用三项自查看作品，再请同桌给一条可修改建议。",
                    "talk": "今天不比谁画得最多。我们只看：你能不能让一处颜色变化更清楚。",
                    "probe": [
                        "你准备改哪一处？",
                        "改完以后，颜色变化会更清楚吗？",
                    ],
                },
                "student_moves": {
                    "look": "对照自查项看自己的小样或作品。",
                    "do": "选择一处进行微修订。",
                    "say": "我改了___，因为这里原来___，现在___。",
                },
                "student_scaffolds": {
                    "language": ["我发现___", "我准备改___", "改完以后___"],
                    "material": "学生自评三项、同伴建议句式。",
                    "peer": "同伴只提一处建议，避免学生重画。",
                },
                "xiaojiao_support": {
                    "hint_card": "提醒教师把评价压缩为一处微修，不展开大评比。",
                    "probe_card": "这一处改完以后，起点和终点更清楚了吗？",
                    "misconception_alert": "学生可能把评价理解为重新画一遍。",
                    "evidence_note": "保留修改前后局部照片或学习单勾选。",
                },
                "common_misconceptions": ["评价变成只说好不好看。", "学生想重画导致时间不够。"],
                "fallback_strategies": ["时间不足时只做口头说明，不强制完成完整修改。", "只选2-3件作品全班看一处修改。"],
                "evidence": {
                    "process": "学生完成自查或同伴建议。",
                    "work": "作品中有一处可见微修。",
                    "expression": "学生能说明自己改了哪里、为什么改。",
                },
                "transition": "课后可以继续在生活中找渐变，下节课再看渐变怎样形成节奏。",
            },
        ],
        "boundary": BOUNDARY,
        "source_inputs": [
            rel(P2_DRAFT),
            rel(P2_ANCHOR),
            rel(STORYBOARD_JSON),
            rel(WORKSHEET_JSON),
            rel(ASSESSMENT_JSON),
            rel(R94_P2_VIEWMODEL),
        ],
    }


def build_mapping(runbook: dict) -> dict:
    shared = {
        "screen_plan": ["lesson.courseware_plan", "lesson.classroom_flow.step.visual_object", "lesson.classroom_flow.step.visual_language_focus"],
        "teacher_moves": ["lesson.classroom_flow.step.teacher_instruction", "lesson.classroom_flow.step.teacher_core_question", "lesson.classroom_flow.step.teacher_probe_question", "lesson.classroom_flow.step.teacher_modeling_language"],
        "student_moves": ["lesson.classroom_flow.step.student_observation", "lesson.classroom_flow.step.student_try", "lesson.classroom_flow.step.student_creation", "lesson.classroom_flow.step.student_recording", "lesson.classroom_flow.step.student_revision"],
        "student_scaffolds": ["lesson.classroom_flow.step.language_scaffold", "lesson.classroom_flow.step.material_scaffold", "lesson.classroom_flow.step.peer_scaffold", "lesson.classroom_flow.step.differentiation_scaffold"],
        "xiaojiao_support": ["lesson.classroom_flow.step.teacher_probe_question", "lesson.classroom_flow.step.common_misconception", "lesson.classroom_flow.step.fallback_strategy"],
        "evidence": ["lesson.classroom_flow.step.process_evidence", "lesson.classroom_flow.step.work_evidence", "lesson.classroom_flow.step.expression_evidence", "lesson.classroom_flow.step.teacher_observation_point", "lesson.classroom_flow.step.success_criteria"],
    }
    return {
        "stage": STAGE,
        "mapping_type": "episode_to_existing_field_reorganization",
        "new_profile_fields_added": False,
        "episodes": [
            {
                "episode_id": ep["episode_id"],
                "title": ep["title"],
                "mapped_field_groups": shared,
                "derived_materials_embedded": ["courseware storyboard", "student worksheet", "teacher observation rubric", "student self-assessment"],
            }
            for ep in runbook["episodes"]
        ],
    }


def render_runbook_md(runbook: dict) -> str:
    parts = [
        "# 《色彩的渐变》教学过程操作稿",
        "",
        "状态：教师审核草案；仅预览；不作为正式定稿。",
        "",
        "## 课堂主线",
        md_list(runbook["classroom_spine"]),
    ]
    for ep in runbook["episodes"]:
        parts.extend([
            "",
            f"## {ep['title']}（{ep['duration']}）",
            "",
            f"**环节目标**：{ep['episode_goal']}",
            "",
            f"**设计意图**：{ep['design_intent']}",
            "",
            "**大屏 / 视觉材料**",
            md_list([ep["screen_plan"]["main_visual"], *ep["screen_plan"]["screen_text"], ep["screen_plan"]["board_or_annotation"]]),
            "",
            "**教师做什么**",
            md_list([ep["teacher_moves"]["action"]]),
            "",
            "**教师怎么说**",
            f"> {ep['teacher_moves']['talk']}",
            "",
            "**教师追问**",
            md_list(ep["teacher_moves"]["probe"]),
            "",
            "**学生怎么做 / 怎么表达**",
            md_list([ep["student_moves"]["look"], ep["student_moves"]["do"], ep["student_moves"]["say"]]),
            "",
            "**学生支架**",
            md_list([*ep["student_scaffolds"]["language"], ep["student_scaffolds"]["material"], ep["student_scaffolds"]["peer"]]),
            "",
            "**小教会帮你做什么**",
            md_list(list(ep["xiaojiao_support"].values())),
            "",
            "**常见误区与补救**",
            md_list([*ep["common_misconceptions"], *ep["fallback_strategies"]]),
            "",
            "**评价证据**",
            md_list(list(ep["evidence"].values())),
            "",
            f"**过渡到下一环节**：{ep['transition']}",
        ])
    return "\n".join(parts) + "\n"


def render_xiaojiao_plan(runbook: dict) -> str:
    parts = ["# 小教环节支持计划", "", "小教在本轮只作为教师审核草案中的辅助角色，不接真实 UI，不写库。"]
    for ep in runbook["episodes"]:
        support = ep["xiaojiao_support"]
        parts.extend([
            "",
            f"## {ep['title']}",
            "",
            f"- 提示卡：{support['hint_card']}",
            f"- 追问卡：{support['probe_card']}",
            f"- 误区提醒：{support['misconception_alert']}",
            f"- 证据记录建议：{support['evidence_note']}",
        ])
    return "\n".join(parts) + "\n"


def render_reading_hierarchy_notes() -> str:
    return """# R93-P3 Teacher Reading Hierarchy Notes

## Decision

The teacher-facing teaching-process page must not expose all episode details at once.

## Default Reading Order

1. Classroom flow: the teacher first sees how the class moves from one episode to the next.
2. Paper-style numbering: fields should be grouped as 1.1, 1.2, 1.3 instead of displayed as cards.
3. Teacher action: each episode first shows what the teacher does and can say.
4. Student action: student work follows as a secondary layer.
5. Evidence: only the minimum evidence needed for classroom judgement is visible.
6. Folded details: design intent, screen plan, scaffolds, Xiaojiao support, misconceptions, and fallback strategies stay inside expandable sections.

## Shell Integration Gate

If the shell defaults to cards, a fully expanded field/schema view, or a dense dashboard-like reading experience, the teacher-facing shell should be treated as failed. Developer evidence can exist, but it must stay behind a folded evidence/developer mode.

## Boundary

- No R21/R36 modification
- No UI binding in this round
- No formal apply
- No PPTX or print-final generation
- No R95 execution
"""


def render_html(runbook: dict) -> str:
    episode_sections = []
    for index, ep in enumerate(runbook["episodes"], start=1):
        evidence_items = list(ep["evidence"].values())
        episode_sections.append(f"""
        <section class="episode-section" id="{esc(ep['episode_id'])}">
          <p class="episode-meta">第{index}个环节 · {esc(ep['duration'])}</p>
          <h2><span>{index}</span>{esc(ep['title'])}</h2>
          <p class="episode-goal"><b>环节目标：</b>{esc(ep['episode_goal'])}</p>

          <section class="numbered-block">
            <h3>{index}.1 老师先做</h3>
            <p>{esc(ep['teacher_moves']['action'])}</p>
            <blockquote>{esc(ep['teacher_moves']['talk'])}</blockquote>
          </section>

          <section class="numbered-block secondary-text">
            <h3>{index}.2 学生跟着做</h3>
            <p><b>先看：</b>{esc(ep['student_moves']['look'])}</p>
            <p><b>再做：</b>{esc(ep['student_moves']['do'])}</p>
            <p><b>表达：</b>{esc(ep['student_moves']['say'])}</p>
          </section>

          <section class="numbered-block evidence-text">
            <h3>{index}.3 这一环节看什么</h3>
            <p>{esc(evidence_items[0])}</p>
            <p>{esc(evidence_items[1])}</p>
          </section>

          <details class="episode-details">
            <summary>展开 {index}.4-{index}.9 支架、大屏、追问和设计意图</summary>
            <section class="detail-section">
              <h4>{index}.4 大屏与视觉材料</h4>
              <p>{esc(ep['screen_plan']['main_visual'])}</p>
              <ul>{ul(ep['screen_plan']['screen_text'] + [ep['screen_plan']['board_or_annotation']])}</ul>
            </section>
            <section class="detail-section">
              <h4>{index}.5 教师追问</h4>
              <ul>{ul(ep['teacher_moves']['probe'])}</ul>
            </section>
            <section class="detail-section">
              <h4>{index}.6 学生支架</h4>
              <ul>{ul(ep['student_scaffolds']['language'] + [ep['student_scaffolds']['material'], ep['student_scaffolds']['peer']])}</ul>
            </section>
            <section class="detail-section">
              <h4>{index}.7 小教支持</h4>
              <ul>{ul(list(ep['xiaojiao_support'].values()))}</ul>
            </section>
            <section class="detail-section">
              <h4>{index}.8 误区与补救</h4>
              <ul>{ul(ep['common_misconceptions'] + ep['fallback_strategies'])}</ul>
            </section>
            <section class="detail-section">
              <h4>{index}.9 设计意图</h4>
              <p>{esc(ep['design_intent'])}</p>
            </section>
          </details>

          <p class="transition"><b>过渡：</b>{esc(ep['transition'])}</p>
        </section>
        """)

    nav = "".join(f"<a href=\"#{esc(ep['episode_id'])}\">{index}. {esc(ep['title'])}</a>" for index, ep in enumerate(runbook["episodes"], start=1))
    flow_steps = "".join(
        f"<li><a href=\"#{esc(ep['episode_id'])}\"><b>{index}</b>{esc(ep['title'])}</a></li>"
        for index, ep in enumerate(runbook["episodes"], start=1)
    )
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>《色彩的渐变》教学过程操作稿</title>
  <style>
    :root {{
      --ink: #263238;
      --muted: #66737c;
      --line: #d8e2dd;
      --paper: #fbfcfa;
      --green: #3e6f5c;
      --mint: #e0f0ea;
      --blue: #e1edf6;
      --sun: #f6e8b7;
      --coral: #f5ded6;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      color: var(--ink);
      background: var(--paper);
      font-family: "Microsoft YaHei", "PingFang SC", Arial, sans-serif;
      line-height: 1.65;
    }}
    header {{
      padding: 26px 28px 16px;
      border-bottom: 1px solid var(--line);
      background: #fff;
      position: sticky;
      top: 0;
      z-index: 2;
    }}
    .topbar {{
      max-width: 1180px;
      margin: 0 auto;
      display: flex;
      justify-content: space-between;
      gap: 18px;
      align-items: flex-start;
    }}
    h1 {{
      margin: 0;
      font-size: clamp(30px, 5vw, 56px);
      line-height: 1.08;
      letter-spacing: 0;
    }}
    .subtitle {{ color: var(--muted); margin: 10px 0 0; font-size: 17px; }}
    .status {{
      display: grid;
      grid-template-columns: repeat(3, minmax(120px, 1fr));
      gap: 10px;
      min-width: 420px;
    }}
    .chip {{
      border: 1px solid var(--line);
      background: var(--mint);
      padding: 12px;
    }}
    .chip:nth-child(2) {{ background: var(--blue); }}
    .chip:nth-child(3) {{ background: var(--sun); }}
    .chip b {{ display: block; color: var(--muted); font-size: 12px; margin-bottom: 3px; }}
    nav {{
      max-width: 1180px;
      margin: 18px auto 0;
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
    }}
    nav a {{
      color: var(--green);
      text-decoration: none;
      border-bottom: 2px solid #bdd7ce;
      padding: 4px 2px;
      font-weight: 700;
      font-size: 14px;
    }}
    main {{ max-width: 980px; margin: 0 auto; padding: 28px 28px 76px; }}
    .spine {{
      border-top: 2px solid var(--ink);
      border-bottom: 1px solid var(--line);
      padding: 22px 0;
      margin-bottom: 26px;
    }}
    .spine h2 {{ margin: 0 0 10px; }}
    .spine ul {{ margin: 0; padding-left: 20px; }}
    .flow-map {{
      margin-bottom: 22px;
      border-bottom: 1px solid var(--line);
      padding: 0 0 20px;
    }}
    .flow-map h2 {{ margin: 0 0 12px; }}
    .flow-map ol {{
      list-style: none;
      padding: 0;
      margin: 0;
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
    }}
    .flow-map a {{
      display: block;
      border: 1px solid #cddbd6;
      background: #fff;
      color: var(--ink);
      text-decoration: none;
      padding: 8px 10px;
      min-width: 150px;
    }}
    .flow-map b {{
      display: inline-block;
      width: 24px;
      height: 24px;
      text-align: center;
      line-height: 22px;
      margin-bottom: 8px;
      margin-right: 8px;
      border-radius: 50%;
      background: var(--green);
      color: #fff;
    }}
    .episode-section {{
      border-top: 1px solid var(--line);
      padding: 34px 0 30px;
    }}
    .episode-meta {{
      margin: 0 0 8px;
      color: var(--green);
      font-weight: 700;
      font-size: 14px;
    }}
    .episode-section h2 {{
      margin: 0;
      font-size: 30px;
      line-height: 1.2;
    }}
    .episode-section h2 span {{
      display: inline-block;
      color: var(--green);
      margin-right: 12px;
    }}
    .episode-goal {{
      margin: 10px 0 22px;
      color: var(--muted);
      font-size: 17px;
    }}
    .numbered-block {{
      margin: 18px 0;
      padding-left: 18px;
      border-left: 3px solid var(--line);
    }}
    .numbered-block h3 {{
      margin: 0 0 8px;
      font-size: 20px;
    }}
    .numbered-block p {{
      margin: 8px 0;
      color: var(--ink);
    }}
    .secondary-text p,
    .evidence-text p {{
      color: var(--muted);
    }}
    .episode-details {{
      margin: 22px 0;
      border-top: 1px solid var(--line);
      border-bottom: 1px solid var(--line);
      background: #fbfdfc;
    }}
    .episode-details summary {{
      cursor: pointer;
      padding: 14px 0;
      font-weight: 700;
      color: var(--green);
    }}
    .detail-section {{
      padding: 14px 0;
      border-top: 1px solid var(--line);
    }}
    .detail-section h4 {{
      margin: 0 0 8px;
      font-size: 17px;
    }}
    .detail-section p, .detail-section li {{ color: var(--muted); }}
    .detail-section ul {{ margin: 0; padding-left: 20px; }}
    blockquote {{
      margin: 10px 0;
      padding: 10px 12px;
      border-left: 4px solid var(--green);
      background: #f6fbf9;
      color: var(--ink);
    }}
    .transition {{
      margin: 22px 0 0;
      padding: 12px 0 0;
      border-top: 1px dashed #cbb7b0;
      color: var(--muted);
    }}
    @media (max-width: 920px) {{
      .topbar {{ flex-direction: column; }}
      .status {{ min-width: 0; width: 100%; }}
    }}
    @media (max-width: 620px) {{
      header, main {{ padding-left: 16px; padding-right: 16px; }}
      .status {{ grid-template-columns: 1fr; }}
      .flow-map a {{ width: 100%; }}
    }}
  </style>
</head>
<body>
  <header>
    <div class="topbar">
      <div>
        <h1>《色彩的渐变》教学过程操作稿</h1>
        <p class="subtitle">把教案、课件故事板、学习单、评价表和小教支持压回课堂环节里。</p>
      </div>
      <div class="status">
        <div class="chip"><b>状态</b>教师审核草案</div>
        <div class="chip"><b>质量</b>BASIC_USABLE</div>
        <div class="chip"><b>正式应用</b>未开放</div>
      </div>
    </div>
    <nav>{nav}</nav>
  </header>
  <main>
    <section class="flow-map">
      <h2>0. 先看课堂怎么走</h2>
      <ol>{flow_steps}</ol>
    </section>
    <section class="spine">
      <h2>0.1 这节课的主线</h2>
      <ul>{ul(runbook['classroom_spine'])}</ul>
    </section>
    {''.join(episode_sections)}
  </main>
</body>
</html>
"""


def build_quality(runbook: dict) -> dict:
    checks = {}
    for key in [
        "episode_goal",
        "design_intent",
        "screen_plan",
        "teacher_moves",
        "student_moves",
        "student_scaffolds",
        "xiaojiao_support",
        "common_misconceptions",
        "fallback_strategies",
        "evidence",
        "transition",
    ]:
        checks[key] = "PASS" if all(ep.get(key) for ep in runbook["episodes"]) else "FAIL"
    result = "BASIC_USABLE" if all(value == "PASS" for value in checks.values()) else "NEEDS_RETRY"
    return {
        "stage": STAGE,
        "quality_sentinel_version": "v1_preview",
        "result": result,
        "allowed_conclusion": "TEACHING_EPISODE_RUNBOOK_READY",
        "teacher_review_required": True,
        "preview_only": True,
        "formal_apply": False,
        "checks": checks,
        "notes": [
            "Episodes are expanded enough for teacher review.",
            "This is not a formal lesson approval.",
            "No PPTX, print final, UI binding, database, Feishu, or memory write was performed.",
        ],
    }


def validate(runbook: dict, quality: dict) -> dict:
    errors: list[str] = []
    required = [
        "episode_goal",
        "design_intent",
        "screen_plan",
        "teacher_moves",
        "student_moves",
        "student_scaffolds",
        "xiaojiao_support",
        "common_misconceptions",
        "fallback_strategies",
        "evidence",
        "transition",
    ]
    if len(runbook["episodes"]) != 5:
        errors.append("episode_count_not_5")
    for ep in runbook["episodes"]:
        missing = [key for key in required if not ep.get(key)]
        if missing:
            errors.append(f"{ep['episode_id']}_missing:" + ",".join(missing))
        if not ep.get("teacher_moves", {}).get("talk"):
            errors.append(f"{ep['episode_id']}_missing_teacher_talk")
        if not ep.get("student_moves", {}).get("do"):
            errors.append(f"{ep['episode_id']}_missing_student_action")
        if not ep.get("xiaojiao_support", {}).get("hint_card"):
            errors.append(f"{ep['episode_id']}_missing_xiaojiao_support")
        if not ep.get("evidence"):
            errors.append(f"{ep['episode_id']}_missing_evidence")
    if quality.get("result") not in ["BASIC_USABLE", "NEEDS_RETRY", "NOT_USABLE"]:
        errors.append("invalid_quality_result")
    html_text = HTML_OUT.read_text(encoding="utf-8") if HTML_OUT.exists() else ""
    for phrase in ["0. 先看课堂怎么走", "1.1 老师先做", "1.2 学生跟着做", "1.3 这一环节看什么", "展开 1.4-1.9 支架、大屏、追问和设计意图"]:
        if phrase not in html_text:
            errors.append("teacher_reading_hierarchy_missing:" + phrase)
    if html_text.count("<details class=\"episode-details\">") != 5:
        errors.append("episode_details_not_folded_for_all_episodes")
    p2_validator = read_json(P2_VALIDATOR)
    r94p1_validator = read_json(R94_P1_VALIDATOR)
    r94p2_validator = read_json(R94_P2_VALIDATOR)
    if not p2_validator.get("validator_pass"):
        errors.append("p2_validator_not_pass")
    if not r94p1_validator.get("validator_pass"):
        errors.append("r94_p1_validator_not_pass")
    if not r94p2_validator.get("validator_pass"):
        errors.append("r94_p2_validator_not_pass")
    if any(
        BOUNDARY[key]
        for key in [
            "provider_called",
            "model_called",
            "new_fields_added_to_profile",
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
            "multi_case_regression_executed",
        ]
    ):
        errors.append("boundary_violation")
    return {
        "stage": STAGE,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "status": "PASS" if not errors else "FAIL",
        "episode_count": len(runbook["episodes"]),
        "teaching_episode_runbook_ready": not errors,
        "quality_sentinel_v1_preview_result": quality.get("result"),
        "teacher_review_required": True,
        "preview_only": True,
        "formal_apply": False,
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
        "printed_final_material_generated": False,
        "r95_executed": False,
        "failed_checks": errors,
        "files": {
            "schema": rel(SCHEMA_OUT),
            "runbook_md": rel(RUNBOOK_MD_OUT),
            "runbook_json": rel(RUNBOOK_JSON_OUT),
            "mapping": rel(MAPPING_OUT),
            "xiaojiao_support": rel(XIAOJIAO_OUT),
            "teacher_reading_hierarchy": rel(READING_HIERARCHY_OUT),
            "html": rel(HTML_OUT),
            "quality": rel(QUALITY_OUT),
        },
        "sha256": {
            "html": sha256(HTML_OUT) if HTML_OUT.exists() else None,
            "runbook_json": sha256(RUNBOOK_JSON_OUT) if RUNBOOK_JSON_OUT.exists() else None,
        },
        "validator_pass": not errors,
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    schema = build_schema()
    runbook = build_runbook()
    mapping = build_mapping(runbook)
    quality = build_quality(runbook)
    write_json(SCHEMA_OUT, schema)
    write_json(RUNBOOK_JSON_OUT, runbook)
    write_text(RUNBOOK_MD_OUT, render_runbook_md(runbook))
    write_json(MAPPING_OUT, mapping)
    write_text(XIAOJIAO_OUT, render_xiaojiao_plan(runbook))
    write_text(READING_HIERARCHY_OUT, render_reading_hierarchy_notes())
    write_text(HTML_OUT, render_html(runbook))
    write_json(QUALITY_OUT, quality)
    validation = validate(runbook, quality)
    write_json(VALIDATOR_OUT, validation)
    print(json.dumps({
        "stage": STAGE,
        "validator_pass": validation["validator_pass"],
        "quality": quality["result"],
        "html": str(HTML_OUT),
        "html_sha256": validation["sha256"]["html"],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
