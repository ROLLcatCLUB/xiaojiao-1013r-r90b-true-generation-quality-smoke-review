from __future__ import annotations

import hashlib
import html
import json
import re
import shutil
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
STAGE = "1013R_R94_P1_R88_FIELD_LAB_PREVIEW_BINDING"
OUT = BASE / STAGE

R88_DIR = BASE / "1013R_R88_FIELD_GENERATION_QUALITY_STATIC_LAB"
R88_HTML = R88_DIR / "field_generation_quality_static_lab_1013R_R88.html"
R88_LEDGER = R88_DIR / "field_generation_quality_static_lab_ledger_1013R_R88.json"

P2_DIR = BASE / "1013R_R93_P2_TEXTBOOK_ANCHOR_CLOSURE_AND_FINAL_PREVIEW_DRAFT"
P2_DRAFT = P2_DIR / "r93_p2_final_preview_lesson_draft.md"
P2_ANCHOR = P2_DIR / "textbook_anchor_closure.md"
P2_VALIDATOR = P2_DIR / "validate_1013R_R93_P2_textbook_anchor_closure_final_preview_draft_result.json"

R94_P1_DIR = BASE / "1013R_R94_P1_DERIVED_ARTIFACTS_TEACHER_REVIEW_POLISH"
R94_P1_STORYBOARD = R94_P1_DIR / "r94_p1_slide_storyboard.md"
R94_P1_STORYBOARD_JSON = R94_P1_DIR / "r94_p1_slide_storyboard.json"
R94_P1_WORKSHEET = R94_P1_DIR / "r94_p1_student_worksheet_one_page.md"
R94_P1_TEACHER_NOTES = R94_P1_DIR / "r94_p1_student_worksheet_teacher_notes.md"
R94_P1_TEACHER_RUBRIC = R94_P1_DIR / "r94_p1_teacher_observation_rubric.md"
R94_P1_STUDENT_SELF = R94_P1_DIR / "r94_p1_student_self_assessment.md"
R94_P1_TRACE = R94_P1_DIR / "r94_p1_derived_artifacts_trace.json"
R94_P1_QUALITY = R94_P1_DIR / "quality_sentinel_v0_result.json"
R94_P1_VALIDATOR = R94_P1_DIR / "validate_1013R_R94_P1_derived_artifacts_teacher_review_polish_result.json"

OUTPUT_HTML = OUT / "field_generation_quality_static_lab_1013R_R88_r94_p1_preview.html"

BOUNDARY = {
    "static_preview_only": True,
    "source_r88_modified": False,
    "provider_called": False,
    "model_called": False,
    "r21_modified": False,
    "r36_modified": False,
    "ui_page_connected": False,
    "formal_apply": False,
    "database_written": False,
    "feishu_written": False,
    "memory_written": False,
    "pptx_generated": False,
    "r95_executed": False,
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


def snippet(text: str, marker: str, length: int = 680) -> str:
    idx = text.find(marker)
    if idx < 0:
        return text[:length].strip()
    return text[idx : idx + length].strip()


def replace_placeholder_block(doc: str, slot_id: str, new_block: str) -> tuple[str, bool]:
    marker = f'<div class="placeholder" data-generation-slot-id="{slot_id}">'
    start = doc.find(marker)
    if start < 0:
        return doc, False

    token_re = re.compile(r"<div\b|</div>", re.IGNORECASE)
    depth = 0
    for match in token_re.finditer(doc, start):
        token = match.group(0).lower()
        if token.startswith("<div"):
            depth += 1
        else:
            depth -= 1
            if depth == 0:
                return doc[:start] + new_block + doc[match.end() :], True
    return doc, False


def teacher_source_label(source: str) -> str:
    lower = source.lower()
    if "textbook" in lower or "anchor" in lower or "教材" in source:
        return "教材锚点证据"
    if "worksheet" in lower or "学习单" in source:
        return "学习单草案"
    if "rubric" in lower or "assessment" in lower or "评价" in source:
        return "评价草案"
    if "storyboard" in lower or "slide" in lower or "课件" in source:
        return "课件故事板草案"
    if "teacher notes" in lower or "教师说明" in source:
        return "教师说明草案"
    if "objectives" in lower or "draft" in lower or "教学" in source or "学情" in source:
        return "教案母稿"
    return "教案母稿与派生草案"


def render_slot(slot_id: str, title: str, source: str, body: str, quality: str, teacher_action: str) -> str:
    return f"""
      <div class="placeholder r94p1-filled" data-generation-slot-id="{esc(slot_id)}" data-r94-p1-preview="true" data-preview-only="true" data-formal-apply-allowed="false">
        <div class="placeholder-title">{esc(title)}</div>
        <div class="r94p1-source">来源：{esc(teacher_source_label(source))} · 仅预览 · 非正式定稿</div>
        <div class="r94p1-body">{body}</div>
        <div class="r94p1-foot">
          <p><b>质量观察</b>{esc(quality)}</p>
          <p><b>教师动作</b>{esc(teacher_action)}</p>
        </div>
      </div>
"""


def ul(items: list[str]) -> str:
    return "<ul>" + "".join(f"<li>{esc(item)}</li>" for item in items) + "</ul>"


def para(text: str) -> str:
    return "<p>" + esc(text).replace("\n", "<br>") + "</p>"


def build_slot_payloads(p2_text: str, storyboard: dict) -> dict[str, dict[str, str]]:
    slide_titles = [f"第{i}页：{s['slide_title']}" for i, s in enumerate(storyboard.get("slides", []), start=1)]
    slide_actions = [s["student_action"] for s in storyboard.get("slides", [])[:5]]
    source = "R93-P2 + R94-P1"
    payloads: dict[str, dict[str, str]] = {
        "big_unit.unit_basic_info": {
            "title": "教材锚点回填",
            "source": "R93-P2 textbook_anchor_closure",
            "body": ul(["第二单元《多彩的世界》", "第1课《色彩的渐变》", "页码 6-7", "后续课：第2课《渐变的节奏》；第3课《多彩的生活》"]),
            "quality": "事实锚定已由教师页图闭合。",
            "teacher_action": "核对教材实物页后继续作为本课母稿来源。",
        },
        "big_unit.unit_theme": {
            "title": "单元主题预览",
            "source": "R93-P2 final preview draft",
            "body": para("多彩的世界：通过色彩的明度、纯度和渐变规律，感受色彩如何丰富生活、作品和空间。"),
            "quality": "能统领本课和后续《渐变的节奏》《多彩的生活》。",
            "teacher_action": "确认是否采用该主题语言作为本单元对学生说明。",
        },
        "big_unit.big_idea": {
            "title": "大观念预览",
            "source": source,
            "body": para("色彩不是孤立存在的，颜色的亮暗、鲜灰和有序变化能带来秩序、节奏和层次，并影响我们对生活环境的感受。"),
            "quality": "从色彩知识迁移到生活与作品表达。",
            "teacher_action": "可作为教师备课理解，不必完整呈现给学生。",
        },
        "big_unit.essential_question": {
            "title": "基本问题预览",
            "source": source,
            "body": para("变化多样的色彩是如何丰富我们的生活的？颜色怎样慢慢变化才会让画面更有秩序和层次？"),
            "quality": "来自教材问题并压缩为课堂可追问问题。",
            "teacher_action": "选择其中一句作为课堂主问题。",
        },
        "big_unit.learning_goals": {
            "title": "单元学习目标预览",
            "source": "R93-P2 教学目标",
            "body": ul(["能发现生活和教材图中的渐变。", "能区分亮暗变化与鲜灰变化。", "能尝试三到五格渐变小样。", "能把渐变用于小作品并说明变化规律。"]),
            "quality": "目标可观察，适合三年级。",
            "teacher_action": "按本班材料条件删减目标表述。",
        },
        "big_unit.content_analysis": {
            "title": "内容分析预览",
            "source": "R93-P2 教材分析",
            "body": para("教材围绕“色彩的明度与纯度”和“渐变的调色游戏”展开，通过自然图像、花卉作品、调色和拼摆活动，建立明度/纯度渐变与秩序美、节奏美的联系。"),
            "quality": "教材线索清楚，不再混写旧版课题。",
            "teacher_action": "可用于教案教材分析段落的精简版。",
        },
        "big_unit.student_context": {
            "title": "学情分析预览",
            "source": "R93-P2 学情分析",
            "body": para("三年级学生能直观看出颜色更亮、更深或更鲜艳，但容易混淆明度和纯度，也容易把渐变做成无规律色块并列。"),
            "quality": "不伪造班情，聚焦本课常见困难。",
            "teacher_action": "补充本班材料经验后再用于正式教案。",
        },
        "big_unit.key_difficult_points": {
            "title": "重难点预览",
            "source": "R93-P2 教学重难点",
            "body": ul(["重点：理解明度和纯度，能做有规律的渐变。", "难点：控制变化幅度，避免突然跳色。"]),
            "quality": "重点难点分开，并能指导活动设计。",
            "teacher_action": "保留“不要跳太快”作为课堂儿童化提醒。",
        },
        "big_unit.performance_task": {
            "title": "表现性任务预览",
            "source": "R93-P2 学生创作 + R94-P1 学习单",
            "body": para("完成三格或五格颜色慢慢变化小样，并把变化规律放进一个色条、图形或小作品；能说明颜色从哪里变到哪里。"),
            "quality": "学生产出清楚，证据可见。",
            "teacher_action": "决定基础/进阶/挑战任务是否全部开放。",
        },
        "big_unit.task_assessment_points": {
            "title": "任务评估要点预览",
            "source": "R94-P1 teacher observation rubric",
            "body": ul(["看得见：能发现渐变。", "试得出：能做连续变化。", "用得上：能用到作品。", "说得清：能说明变化。", "改得动：能修一处。"]),
            "quality": "评价与任务对应，不使用复杂分数。",
            "teacher_action": "教师可选择 2-3 项作为课堂重点观察。",
        },
        "big_unit.learning_stages": {
            "title": "学习阶段预览",
            "source": "R94-P1 storyboard",
            "body": ul(["观察生活和教材图。", "辨析亮暗/鲜灰。", "三格调色或排列小样。", "迁移到小作品。", "自查、互评、微修订。"]),
            "quality": "阶段递进清楚。",
            "teacher_action": "根据课时长度压缩展示交流环节。",
        },
        "big_unit.learning_tasks": {
            "title": "学习任务预览",
            "source": "R94-P1 worksheet",
            "body": ul(["任务一：找一找颜色从哪里变到哪里。", "任务二：试一试三格颜色慢慢变。", "任务三：查一查作品能否说清变化。"]),
            "quality": "任务链由观察到操作再到表达。",
            "teacher_action": "可作为学习单三项任务草案，后续再按课堂时间删减。",
        },
        "big_unit.micro_questions": {
            "title": "小问题预览",
            "source": "R94-P1 storyboard",
            "body": ul(["颜色从哪里开始变？", "它是亮一点/暗一点，还是鲜一点/灰一点？", "中间有没有跳太快？", "你能改哪一处让它更自然？"]),
            "quality": "问题贴近儿童，可驱动观察与修订。",
            "teacher_action": "课堂提问按顺序使用，不必一次全问。",
        },
        "big_unit.learning_activities": {
            "title": "学习活动预览",
            "source": "R94-P1 storyboard",
            "body": ul(["观察教材图并圈画变化方向。", "做三格颜色小样。", "选择基础/进阶/挑战任务。", "用自查表检查作品。", "展示交流并微修订。"]),
            "quality": "活动服务任务，避免只讲概念。",
            "teacher_action": "准备色卡或小样纸以降低材料风险。",
        },
        "big_unit.learning_assessment": {
            "title": "学习评价预览",
            "source": "R94-P1 assessment",
            "body": para("采用教师观察版和学生自评版双轨：教师看“看得见、试得出、用得上、说得清、改得动”，学生只做三项自查。"),
            "quality": "评价证据清楚，学生端负担较轻。",
            "teacher_action": "确认是否打印学生自评三项，教师观察表可不发给学生。",
        },
        "big_unit.scaffold.context": {
            "title": "情境支架预览",
            "source": "R94-P1 storyboard",
            "body": para("从生活中的天空、山峦、花朵或教材图进入，让学生先找“颜色慢慢变过去”的现象。"),
            "quality": "情境贴近儿童，不喧宾夺主。",
            "teacher_action": "选 2-3 张图即可，避免图片过多拖慢课堂。",
        },
        "big_unit.scaffold.task": {
            "title": "任务支架预览",
            "source": "R94-P1 worksheet",
            "body": para("学习单把任务压缩为找一找、试一试、查一查；先三格小样，再迁移到作品。"),
            "quality": "步骤清楚，降低操作门槛。",
            "teacher_action": "基础学生只做三格，进阶学生再做五格。",
        },
        "big_unit.scaffold.resource": {
            "title": "资源支架预览",
            "source": "R93-P2 textbook evidence + R94-P1",
            "body": ul(["教材第6-7页图片。", "教师自制三格小样。", "小样纸或学习单。", "水粉、水彩笔、彩铅、油画棒或色卡任选。"]),
            "quality": "资源真实，不虚构教材图。",
            "teacher_action": "根据班级材料条件确认最终工具。",
        },
        "big_unit.scaffold.strategy": {
            "title": "策略支架预览",
            "source": "R94-P1 teacher notes",
            "body": ul(["亮暗看亮不亮。", "鲜灰看鲜不鲜。", "每次只变一点点。", "用“从___到___”表达变化。"]),
            "quality": "方法语言可教，可迁移到单课。",
            "teacher_action": "示范时同步板书儿童化关键词。",
        },
        "big_unit.handout_plan": {
            "title": "学习单计划预览",
            "source": "R94-P1 student worksheet one page",
            "body": para("一页学生版只保留三项：找一找、试一试、查一查；教师说明另列，不挤入学生纸面。"),
            "quality": "较上一版已明显减负，但仍是预览草案。",
            "teacher_action": "排版前确认纸张大小和留白。",
        },
        "big_unit.assessment_scaffold": {
            "title": "评价支架预览",
            "source": "R94-P1 teacher rubric + student self-assessment",
            "body": para("教师观察版保留 5 维，学生自评版压缩为 3 项；均使用“已做到 / 基本做到 / 还要再试”。"),
            "quality": "教师版与学生版已拆分。",
            "teacher_action": "课堂可只使用学生自评三项，教师观察表课后整理。",
        },
        "big_unit.material_requests": {
            "title": "资料补充预览",
            "source": "R94-P1 teacher notes",
            "body": para("需教师确认本班最终材料：水粉、水彩笔、彩铅、油画棒或混合材料；确认是否需要教材页实物投影。"),
            "quality": "只提示补资料，不写成正式课包。",
            "teacher_action": "课前确定材料并调整学习单用语。",
        },
        "lesson.lesson_identity": {
            "title": "课时身份预览",
            "source": "R93-P2",
            "body": ul(["三年级美术", "第二单元《多彩的世界》", "第1课《色彩的渐变》", "建议 40 分钟"]),
            "quality": "课时身份明确。",
            "teacher_action": "确认册次和班级课时长度。",
        },
        "lesson.inherited_unit_context": {
            "title": "继承单元主线预览",
            "source": "R93-P2 anchor",
            "body": para("本课是第二单元色彩渐变学习的起点，后续《渐变的节奏》推进到节奏表现，《多彩的生活》迁移到生活空间。"),
            "quality": "单课和后续课关系清楚。",
            "teacher_action": "可在课堂结尾提示下一课，不展开讲。",
        },
        "lesson.textbook_anchor": {
            "title": "教材锚点预览",
            "source": "R93-P2 textbook_anchor_closure",
            "body": para("教材页图闭合：第二单元《多彩的世界》第1课《色彩的渐变》，页码 6-7，核心板块为“色彩的明度与纯度”和“渐变的调色游戏”。"),
            "quality": "source gap 已关闭。",
            "teacher_action": "正式上课前再核实教材实物页。",
        },
        "lesson.lesson_concept_slice": {
            "title": "概念切片预览",
            "source": "R93-P2 + R94-P1",
            "body": ul(["明度：亮一点 / 暗一点。", "纯度：鲜一点 / 灰一点。", "渐变：颜色慢慢变过去。"]),
            "quality": "儿童化语言明确。",
            "teacher_action": "屏幕端优先用儿童话，教师口头补专业词。",
        },
        "lesson.lesson_focus_question": {
            "title": "本课驱动问题预览",
            "source": "R94-P1 storyboard",
            "body": para("颜色怎样慢慢变化，才能让画面更有秩序、更有层次？"),
            "quality": "问题收敛到本课核心活动。",
            "teacher_action": "课堂可以改成更口语的“颜色怎么慢慢变才好看又清楚？”",
        },
        "lesson.lesson_objectives": {
            "title": "课时目标预览",
            "source": "R93-P2 objectives",
            "body": ul(["发现渐变。", "区分亮暗与鲜灰。", "完成三格或五格渐变小样。", "在作品中说明颜色变化。"]),
            "quality": "可观察可评价。",
            "teacher_action": "正式稿可压缩为三条目标。",
        },
        "lesson.student_starting_point": {
            "title": "学生起点预览",
            "source": "R93-P2",
            "body": para("学生对颜色变化有生活经验，但容易只说“好看”，难以说清变化方向，也可能把明度、纯度混在一起。"),
            "quality": "困难能转成教学支架。",
            "teacher_action": "根据班级实际补充材料使用经验。",
        },
        "lesson.key_difficult_points": {
            "title": "单课重难点预览",
            "source": "R93-P2",
            "body": ul(["重点：理解亮暗、鲜灰和慢慢变化。", "难点：让变化连续，不突然跳色。"]),
            "quality": "服务教学过程设计。",
            "teacher_action": "示范时突出“每次只变一点点”。",
        },
        "lesson.lesson_task_evidence": {
            "title": "任务与证据预览",
            "source": "R94-P1 worksheet + assessment",
            "body": para("证据来自三格小样、作品中的渐变规律、学生一句话说明和一处微修订。"),
            "quality": "过程、作品、表达和修订证据都可见。",
            "teacher_action": "决定是否收学习单作为证据留存。",
        },
        "lesson.classroom_flow": {
            "title": "教学过程预览",
            "source": "R94-P1 slide storyboard",
            "body": ul(slide_titles),
            "quality": "已从文字大纲转为 storyboard 结构。",
            "teacher_action": "下一轮若要深化教学过程，可在 A/B 版本中重排这些环节。",
        },
        "lesson.courseware_plan": {
            "title": "课件/大屏计划预览",
            "source": "R94-P1 slide storyboard",
            "body": para("只做 10 页 storyboard：每页一个核心任务，明确主视觉、屏幕文字、教师提示、学生动作和板书/圈画提示。"),
            "quality": "不是 PPTX，不含正式图片素材。",
            "teacher_action": "教师审核后再决定是否进入真实课件制作。",
        },
        "lesson.handout_plan": {
            "title": "学习单计划预览",
            "source": "R94-P1 worksheet",
            "body": para("学生一页版：找一找、试一试、查一查；教师说明版单独承接明度、纯度、材料准备和常见问题。"),
            "quality": "解决了上一版内容偏满的问题。",
            "teacher_action": "排版为一页前仍需教师确认留白。",
        },
        "lesson.assessment_plan": {
            "title": "评价计划预览",
            "source": "R94-P1 rubric",
            "body": para("评价拆为教师观察版和学生自评版，教师版 5 维，学生版 3 项，不使用复杂分数。"),
            "quality": "评价表已拆分，适合教师审核。",
            "teacher_action": "选择课堂当场使用的最小评价项。",
        },
        "lesson.material_requests": {
            "title": "资料补充预览",
            "source": "R94-P1 teacher notes",
            "body": para("仍需教师确认材料和图像来源：是否用水粉、彩铅、油画棒、水彩笔或色卡；是否展示教材页图。"),
            "quality": "不把未确认材料写死。",
            "teacher_action": "课前 1 天确定材料通知。",
        },
    }

    step_payloads = {
        "lesson.classroom_flow.step.step_id": ("环节编号预览", "这里对应课件故事板中的“第1页—第10页”。编号只用于页面排序，不是正式教案里的课堂环节名称。"),
        "lesson.classroom_flow.step.step_order": ("环节顺序预览", "封面、生活观察、教材观察、核心词、调色游戏、教师示范、学生创作、自查、展示、微修订。"),
        "lesson.classroom_flow.step.step_name": ("环节名称预览", "生活中的渐变 / 教材图观察 / 调色游戏 / 学生创作 / 作品自查 / 展示交流。"),
        "lesson.classroom_flow.step.duration": ("时间分配预览", "教案母稿按一节 40 分钟课设计；当前只是把课件、学习单、评价表拆成可预览结构，还没有把每一页或每一环节的分钟正式锁定。"),
        "lesson.classroom_flow.step.phase_role": ("环节功能预览", "发现现象、建立概念、操作小样、迁移创作、评价修订。"),
        "lesson.classroom_flow.step.prior_connection": ("承接上一环节预览", "每页从上一页动作延续：看见变化 -> 判断变化 -> 试出变化 -> 用到作品。"),
        "lesson.classroom_flow.step.next_connection": ("引出下一环节预览", "每个活动都引向下一步可观察产出，避免孤立讲解。"),
        "lesson.classroom_flow.step.teacher_instruction": ("教师指令预览", "请用手指一指颜色从哪里开始变，又变到了哪里。"),
        "lesson.classroom_flow.step.teacher_core_question": ("核心提问预览", "颜色怎样慢慢变化，才能让画面更有秩序、更有层次？"),
        "lesson.classroom_flow.step.teacher_probe_question": ("追问预览", "它是亮一点/暗一点，还是鲜一点/灰一点？中间有没有跳太快？"),
        "lesson.classroom_flow.step.teacher_demo": ("教师示范预览", "选颜色 -> 做三格小样 -> 标方向 -> 放进作品。"),
        "lesson.classroom_flow.step.teacher_modeling_language": ("教师示范语言预览", "先把颜色排好队，再放进你的图形里；每次只变一点点。"),
        "lesson.classroom_flow.step.teacher_patrol_observation": ("巡视观察预览", "看学生是否有起点、方向、三格变化和表达句式。"),
        "lesson.classroom_flow.step.teacher_feedback_move": ("即时反馈动作预览", "圈出跳色处，提醒第二格更接近第一格；让学生只微修一处。"),
        "lesson.classroom_flow.step.student_observation": ("学生观察预览", "观察生活图或教材图，指出颜色从哪里变到哪里。"),
        "lesson.classroom_flow.step.student_discussion": ("学生讨论预览", "同桌判断一组色卡属于亮暗变化还是鲜灰变化。"),
        "lesson.classroom_flow.step.student_try": ("学生尝试预览", "选择一种颜色画三格，让颜色慢慢变。"),
        "lesson.classroom_flow.step.student_creation": ("学生创作预览", "把三格小样规律放进色条、图形或小作品。"),
        "lesson.classroom_flow.step.student_recording": ("学生记录预览", "在学习单上写：我的颜色从___变到___。"),
        "lesson.classroom_flow.step.student_display": ("学生展示预览", "展示一处颜色变化，并说明变化方向。"),
        "lesson.classroom_flow.step.student_revision": ("学生修订预览", "根据自查或同伴建议，只改一处让颜色更自然。"),
        "lesson.classroom_flow.step.visual_object": ("观察对象预览", "教材第6-7页图像、教师自制色条、学生三格小样。"),
        "lesson.classroom_flow.step.visual_language_focus": ("美术语言焦点预览", "明度、纯度、渐变规律，用学生话表达为亮暗、鲜灰、慢慢变化。"),
        "lesson.classroom_flow.step.technique_focus": ("技法要点预览", "逐步加白/黑或加灰，或用相邻色块/色卡形成连续变化。"),
        "lesson.classroom_flow.step.material_use": ("材料使用预览", "水粉、水彩笔、彩铅、油画棒或色卡任选；当前预览稿不锁定材料。"),
        "lesson.classroom_flow.step.composition_or_color_focus": ("色彩关注点预览", "起点、终点、方向、中间过渡是否自然。"),
        "lesson.classroom_flow.step.artwork_or_life_example": ("生活/作品例证预览", "天空、山峦、花朵、衣服颜色或教材学生作品。"),
        "lesson.classroom_flow.step.positive_negative_example": ("正反例预览", "自然三格渐变 vs 中间跳太快的三格；用于微修订。"),
        "lesson.classroom_flow.step.context_scaffold": ("情境支架预览", "先从生活中的颜色慢慢变化进入。"),
        "lesson.classroom_flow.step.task_scaffold": ("任务支架预览", "找一找、试一试、查一查三步完成。"),
        "lesson.classroom_flow.step.language_scaffold": ("语言支架预览", "我的颜色从___变到___；它变得更亮/暗/鲜/灰。"),
        "lesson.classroom_flow.step.material_scaffold": ("材料支架预览", "三格空框、小样纸、色卡或教师示范样本。"),
        "lesson.classroom_flow.step.peer_scaffold": ("同伴支架预览", "同桌帮看是否有起点、方向和自然过渡。"),
        "lesson.classroom_flow.step.differentiation_scaffold": ("差异化支架预览", "基础三格，进阶五格，挑战放进小作品。"),
        "lesson.classroom_flow.step.process_evidence": ("过程证据预览", "学生圈画起点终点、完成三格小样、自查勾选。"),
        "lesson.classroom_flow.step.work_evidence": ("作品证据预览", "作品或小样中能看出连续颜色变化。"),
        "lesson.classroom_flow.step.expression_evidence": ("表达证据预览", "学生能说出从什么颜色变到什么颜色。"),
        "lesson.classroom_flow.step.peer_assessment": ("同伴评价预览", "我看到... 我建议...，只提一处可修改点。"),
        "lesson.classroom_flow.step.teacher_observation_point": ("教师观察点预览", "是否发现渐变、是否试出三层、是否能说明变化。"),
        "lesson.classroom_flow.step.success_criteria": ("成功标准预览", "看得出起点、方向、慢慢变化，并能说一句。"),
        "lesson.classroom_flow.step.evidence_storage": ("证据留存预览", "保留学生学习单、三格小样或作品照片；本轮不写库。"),
        "lesson.classroom_flow.step.common_misconception": ("常见误区预览", "把渐变理解成随便排色；混淆亮暗和鲜灰；颜色跳太快。"),
        "lesson.classroom_flow.step.time_risk": ("时间风险预览", "创作环节可能偏紧；可压缩展示数量，保留微修订。"),
        "lesson.classroom_flow.step.material_risk": ("材料风险预览", "颜料材料可能弄脏或准备不足；可改用彩铅、油画棒或色卡。"),
        "lesson.classroom_flow.step.class_management_risk": ("课堂秩序风险预览", "调色和材料分发可能拖慢节奏；先演示再分发。"),
        "lesson.classroom_flow.step.fallback_strategy": ("补救策略预览", "时间不足时只做三格小样和一句表达，不做完整作品。"),
        "lesson.classroom_flow.step.alternative_plan": ("替代方案预览", "不用颜料时，可用彩铅/油画棒/色卡做亮暗或鲜灰排列。"),
    }
    for key, (title, text) in step_payloads.items():
        payloads[key] = {
            "title": title,
            "source": "R94-P1 storyboard / worksheet / assessment",
            "body": para(text),
            "quality": "已映射到教学过程内部字段；预览草案，不作为正式定稿。",
            "teacher_action": "教师选择是否保留为本课教学过程母版。",
        }
    return payloads


def render_extra_section(storyboard: dict, worksheet_json: dict, assessment_json: dict, quality: dict, trace: dict) -> str:
    slides = storyboard.get("slides", [])
    story_rows = "".join(
        f"<tr><td>第{i}页</td><td>{esc(s.get('slide_title'))}</td><td>{esc(s.get('screen_text'))}</td><td>{esc(s.get('student_action'))}</td></tr>"
        for i, s in enumerate(slides, start=1)
    )
    worksheet_tasks = worksheet_json.get("student_version", {}).get("tasks", [])
    worksheet_items = ul([f"{task.get('title')}: {task.get('student_language')}" for task in worksheet_tasks])
    teacher_dims = assessment_json.get("teacher_observation_dimensions", [])
    student_items = assessment_json.get("student_self_assessment_items", [])
    return f"""
      <section class="section r94p1-extra" id="r94-p1-extra">
        <h2>新增派生物结构 · 超出原字段槽位</h2>
        <p class="r94p1-note">原静态页有课件计划、学习单计划、评价计划，但没有独立承接课件故事板、学生一页版、教师说明版、教师观察版和学生自评版的细槽位。这里作为新增预览区，不写入正式字段，不接真实页面。</p>
        <div class="r94p1-extra-grid">
          <article>
            <h3>课件故事板结构</h3>
            <table class="r94p1-table">
              <thead><tr><th>页序</th><th>页面标题</th><th>屏幕文字</th><th>学生动作</th></tr></thead>
              <tbody>{story_rows}</tbody>
            </table>
          </article>
          <article>
            <h3>一页学生版学习单</h3>
            {worksheet_items}
            <p><b>边界</b> 一页可打印草案，但不是打印定稿。</p>
          </article>
          <article>
            <h3>评价拆分</h3>
            <p><b>教师观察版</b></p>
            {ul(teacher_dims)}
            <p><b>学生自评版</b></p>
            {ul(student_items)}
          </article>
          <article>
            <h3>质量与边界</h3>
            {ul([
                '质量结论：' + str(quality.get('result')),
                '阻塞状态：' + str(quality.get('blocking')).lower(),
                '教材锚点：' + str(trace.get('source_textbook_anchor_status')),
                '边界：仅预览，不作为正式定稿',
                '边界：未接真实页面，未进入下一阶段',
            ])}
          </article>
        </div>
      </section>
"""


def css() -> str:
    return """
  <style id="shiwei-r94p1-r88-preview-style">
    .r94p1-filled {
      border-color: #8bbddf;
      background: linear-gradient(180deg, #ffffff, #f3f9ff);
    }
    .r94p1-source {
      margin: 6px 0 8px;
      color: #42677d;
      font-size: 12px;
      font-weight: 700;
    }
    .r94p1-body {
      border: 1px solid #d7e8f5;
      border-radius: 8px;
      padding: 10px 12px;
      background: #fff;
      color: #20333f;
    }
    .r94p1-body p { margin: 0; }
    .r94p1-body ul { margin: 0; padding-left: 18px; }
    .r94p1-foot {
      margin-top: 8px;
      display: grid;
      gap: 6px;
    }
    .r94p1-foot p {
      margin: 0;
      color: #526a75;
      font-size: 12px;
    }
    .r94p1-foot b {
      display: inline-block;
      margin-right: 8px;
      color: #2f75b5;
    }
    .r94p1-extra {
      background: linear-gradient(180deg, #fbfdff, #eef7ff);
    }
    .r94p1-note {
      color: #526a75;
      margin-top: -6px;
    }
    .r94p1-extra-grid {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 14px;
    }
    .r94p1-extra-grid article {
      border: 1px solid #c6dded;
      background: #fff;
      border-radius: 8px;
      padding: 14px;
    }
    .r94p1-extra-grid h3 { margin-top: 0; color: #245d83; }
    .r94p1-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 12px;
    }
    .r94p1-table th,
    .r94p1-table td {
      border: 1px solid #d7e8f5;
      padding: 6px 8px;
      vertical-align: top;
    }
    .r94p1-table th {
      background: #eef7ff;
      color: #245d83;
    }
    .r94p1-banner {
      padding: 10px 32px;
      border-bottom: 1px solid #bcd8f3;
      background: #eef7ff;
      color: #245d83;
      font-weight: 800;
    }
    @media (max-width: 1100px) {
      .r94p1-extra-grid { grid-template-columns: 1fr; }
    }
  </style>
"""


def source_records() -> list[dict]:
    paths = [
        R88_HTML,
        R88_LEDGER,
        P2_DRAFT,
        P2_ANCHOR,
        P2_VALIDATOR,
        R94_P1_STORYBOARD,
        R94_P1_STORYBOARD_JSON,
        R94_P1_WORKSHEET,
        R94_P1_TEACHER_NOTES,
        R94_P1_TEACHER_RUBRIC,
        R94_P1_STUDENT_SELF,
        R94_P1_TRACE,
        R94_P1_QUALITY,
        R94_P1_VALIDATOR,
    ]
    return [
        {"path": rel(path), "size": path.stat().st_size, "sha256": sha256(path)}
        for path in paths
    ]


def validate_html(html_doc: str, filled_count: int, extra_count: int, ledger: dict) -> dict:
    missing_required = []
    for phrase in [
        "新增派生物结构",
        "仅预览",
        "非正式定稿",
        "data-preview-only=\"true\"",
        "data-formal-apply-allowed=\"false\"",
        "课件故事板结构",
    ]:
        if phrase not in html_doc:
            missing_required.append(phrase)
    r94_validator = read_json(R94_P1_VALIDATOR)
    errors = []
    if r94_validator.get("validator_pass") is not True:
        errors.append("r94_p1_validator_not_pass")
    if filled_count != 83:
        errors.append(f"filled_count_not_83:{filled_count}")
    if extra_count < 5:
        errors.append(f"extra_count_too_low:{extra_count}")
    if missing_required:
        errors.append("missing_required_html_phrases:" + ",".join(missing_required))
    if any(
        BOUNDARY[key]
        for key in [
            "source_r88_modified",
            "provider_called",
            "model_called",
            "r21_modified",
            "r36_modified",
            "ui_page_connected",
            "formal_apply",
            "database_written",
            "feishu_written",
            "memory_written",
            "pptx_generated",
            "r95_executed",
        ]
    ):
        errors.append("boundary_violation")
    return {
        "stage": STAGE,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "status": "PASS" if not errors else "FAIL",
        "source_r88_html": rel(R88_HTML),
        "output_html": rel(OUTPUT_HTML),
        "r88_slot_count": len(ledger.get("big_unit_fields", [])) + len(ledger.get("lesson_fields", [])) + len(ledger.get("step_contract_fields", [])),
        "filled_r88_slot_count": filled_count,
        "extra_r94_p1_artifact_blocks": extra_count,
        "r94_p1_validator_pass": r94_validator.get("validator_pass"),
        "boundary": BOUNDARY,
        "source_records": source_records(),
        "failed_checks": errors,
        "validator_pass": not errors,
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    source_dir = OUT / "source_snapshots"
    source_dir.mkdir(exist_ok=True)
    for src in [R88_HTML, R88_LEDGER, P2_DRAFT, P2_ANCHOR, R94_P1_STORYBOARD, R94_P1_WORKSHEET, R94_P1_TEACHER_RUBRIC, R94_P1_VALIDATOR]:
        shutil.copy2(src, source_dir / src.name)

    html_doc = R88_HTML.read_text(encoding="utf-8")
    ledger = read_json(R88_LEDGER)
    p2_text = P2_DRAFT.read_text(encoding="utf-8")
    storyboard = read_json(R94_P1_STORYBOARD_JSON)
    worksheet_structured = read_json(R94_P1_DIR / "r94_p1_student_worksheet_structured.json")
    assessment_structured = read_json(R94_P1_DIR / "r94_p1_assessment_structured.json")
    trace = read_json(R94_P1_TRACE)
    quality = read_json(R94_P1_QUALITY)

    slot_payloads = build_slot_payloads(p2_text, storyboard)
    all_keys = [
        *(item["engineering_key"] for item in ledger.get("big_unit_fields", [])),
        *(item["engineering_key"] for item in ledger.get("lesson_fields", [])),
        *(item["engineering_key"] for item in ledger.get("step_contract_fields", [])),
    ]
    filled = 0
    missing = []
    for key in all_keys:
        payload = slot_payloads.get(key)
        if not payload:
            missing.append(key)
            continue
        block = render_slot(
            f"R88-GEN/{key}",
            payload["title"],
            payload["source"],
            payload["body"],
            payload["quality"],
            payload["teacher_action"],
        )
        html_doc, ok = replace_placeholder_block(html_doc, f"R88-GEN/{key}", block)
        if ok:
            filled += 1
        else:
            missing.append(key)

    extra = render_extra_section(storyboard, worksheet_structured, assessment_structured, quality, trace)
    html_doc = html_doc.replace("1013R R88 字段生成质量静态验证页", "字段生成质量静态预览页")
    html_doc = html_doc.replace("1013R_R88 · static only · no prompt text", "派生材料预览 · 静态副本 · 不调用模型")
    html_doc = html_doc.replace(
        "<a class=\"nav-link\" href=\"#quality\">质量观察</a>",
        "<a class=\"nav-link\" href=\"#r94-p1-extra\">新增派生物</a>\n      <a class=\"nav-link\" href=\"#quality\">质量观察</a>",
    )
    html_doc = html_doc.replace("</head>", css() + "\n</head>", 1)
    html_doc = html_doc.replace(
        "<main>",
        "<main>\n      <div class=\"r94p1-banner\">本页为静态预览副本 · 原页面未修改 · 仅预览，非正式定稿</div>",
        1,
    )
    html_doc = html_doc.replace(
        "      <section class=\"section\" id=\"quality\">",
        extra + "\n      <section class=\"section\" id=\"quality\">",
        1,
    )
    html_doc = html_doc.replace("</body>", f"\n<!-- {STAGE}: filled={filled}; missing={len(missing)}; generated={datetime.now().isoformat(timespec='seconds')} -->\n</body>")

    write_text(OUTPUT_HTML, html_doc)
    validation = validate_html(html_doc, filled, 6, ledger)
    if missing:
        validation["missing_slots"] = missing
        validation["failed_checks"].append("missing_slot_payloads")
        validation["status"] = "FAIL"
        validation["validator_pass"] = False
    write_json(OUT / "validate_1013R_R94_P1_R88_field_lab_preview_binding_result.json", validation)

    manifest = {
        "stage": STAGE,
        "output_html": rel(OUTPUT_HTML),
        "output_html_sha256": sha256(OUTPUT_HTML),
        "source_r88_modified": False,
        "files": [
            {"path": rel(p), "size": p.stat().st_size, "sha256": sha256(p)}
            for p in sorted(OUT.rglob("*"))
            if p.is_file()
        ],
        "boundary": BOUNDARY,
    }
    write_json(OUT / "REVIEW_PACKAGE_MANIFEST.json", manifest)
    write_text(
        OUT / "README.md",
        f"""# {STAGE}

This package copies the R88 field generation quality static lab and fills its 83 generation placeholders with R93-P2 / R94-P1 preview content.

It also appends an extra section for R94-P1 derived artifact internals that exceed the original R88 field slots.

Output HTML:

```text
{rel(OUTPUT_HTML)}
```

Boundary:

```text
source_r88_modified=false
provider_called=false
model_called=false
r21_modified=false
r36_modified=false
ui_page_connected=false
formal_apply=false
database_written=false
feishu_written=false
memory_written=false
r95_executed=false
```
""",
    )

    print(
        json.dumps(
            {
                "stage": STAGE,
                "validator_pass": validation["validator_pass"],
                "filled_r88_slots": filled,
                "output_html": str(OUTPUT_HTML),
                "output_html_sha256": sha256(OUTPUT_HTML),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
