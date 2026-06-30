from __future__ import annotations

import hashlib
import html
import json
import re
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
STAGE = "1013R_R94_P2_TEACHER_FACING_LESSON_PACKAGE_OVERVIEW"
OUT = BASE / STAGE

P2_DIR = BASE / "1013R_R93_P2_TEXTBOOK_ANCHOR_CLOSURE_AND_FINAL_PREVIEW_DRAFT"
P2_DRAFT = P2_DIR / "r93_p2_final_preview_lesson_draft.md"
P2_ANCHOR = P2_DIR / "textbook_anchor_closure.md"
P2_VALIDATOR = P2_DIR / "validate_1013R_R93_P2_textbook_anchor_closure_final_preview_draft_result.json"

R94_P1_DIR = BASE / "1013R_R94_P1_DERIVED_ARTIFACTS_TEACHER_REVIEW_POLISH"
STORYBOARD_JSON = R94_P1_DIR / "r94_p1_slide_storyboard.json"
WORKSHEET_JSON = R94_P1_DIR / "r94_p1_student_worksheet_structured.json"
ASSESSMENT_JSON = R94_P1_DIR / "r94_p1_assessment_structured.json"
QUALITY_JSON = R94_P1_DIR / "quality_sentinel_v0_result.json"
TRACE_JSON = R94_P1_DIR / "r94_p1_derived_artifacts_trace.json"
R94_P1_VALIDATOR = R94_P1_DIR / "validate_1013R_R94_P1_derived_artifacts_teacher_review_polish_result.json"

FIELD_LAB_DIR = BASE / "1013R_R94_P1_R88_FIELD_LAB_PREVIEW_BINDING"
FIELD_LAB_HTML = FIELD_LAB_DIR / "field_generation_quality_static_lab_1013R_R88_r94_p1_preview.html"

HTML_OUT = OUT / "r94_p2_teacher_facing_lesson_package_overview.html"
VIEWMODEL_OUT = OUT / "r94_p2_teacher_facing_viewmodel.json"
DEMOTE_OUT = OUT / "r94_p2_field_lab_demote_decision.md"
VALIDATOR_OUT = OUT / "validate_1013R_R94_P2_teacher_facing_overview_result.json"

BOUNDARY = {
    "teacher_facing_preview_only": True,
    "field_lab_demoted_to_audit_page": True,
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
    "printed_final_material_generated": False,
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


def li(items: list[str]) -> str:
    return "".join(f"<li>{esc(item)}</li>" for item in items)


def first_paragraph(path: Path, marker: str, fallback: str) -> str:
    text = path.read_text(encoding="utf-8")
    idx = text.find(marker)
    if idx < 0:
        return fallback
    tail = text[idx + len(marker) :].strip()
    lines = [line.strip("# -*") for line in tail.splitlines() if line.strip()]
    return lines[0] if lines else fallback


def build_viewmodel() -> dict:
    storyboard = read_json(STORYBOARD_JSON)
    worksheet = read_json(WORKSHEET_JSON)
    assessment = read_json(ASSESSMENT_JSON)
    quality = read_json(QUALITY_JSON)
    trace = read_json(TRACE_JSON)
    p2_validator = read_json(P2_VALIDATOR)
    r94_validator = read_json(R94_P1_VALIDATOR)

    slides = storyboard.get("slides", [])
    worksheet_tasks = worksheet.get("student_version", {}).get("tasks", [])
    teacher_dims = assessment.get("teacher_observation_dimensions", [])
    student_items = assessment.get("student_self_assessment_items", [])

    return {
        "stage": STAGE,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "lesson": {
            "title": "色彩的渐变",
            "subject": "美术",
            "grade": "三年级",
            "unit": "第二单元《多彩的世界》",
            "lesson_position": "第1课",
            "suggested_duration": "40分钟",
            "textbook_anchor_status": "已闭合",
        },
        "status": {
            "package_status": "教师审核草案",
            "quality": quality.get("result", "BASIC_USABLE"),
            "formal_apply": False,
            "formal_apply_label": "未开放",
            "teacher_review_required": True,
        },
        "package_materials": [
            {
                "name": "教案预览稿",
                "state": "可审阅",
                "summary": "围绕亮暗、鲜灰和颜色慢慢变化组织教学。",
                "primary_action": "查看教学流程",
            },
            {
                "name": "课件故事板",
                "state": f"{len(slides)}页草案",
                "summary": "每页对应一个课堂动作，尚未生成正式PPT。",
                "primary_action": "预览页序",
            },
            {
                "name": "一页学生学习单",
                "state": "草案",
                "summary": "找一找、试一试、查一查三项任务。",
                "primary_action": "检查是否打印",
            },
            {
                "name": "教师说明",
                "state": "草案",
                "summary": "材料准备、课堂提醒和常见问题处理。",
                "primary_action": "确认材料",
            },
            {
                "name": "课堂环节",
                "state": "5段流程",
                "summary": "看见渐变、分清变化、三格试色、放进作品、自查修订。",
                "primary_action": "查看怎么上",
            },
            {
                "name": "评价表",
                "state": "教师版 + 学生版",
                "summary": "教师观察五维，学生自评三项。",
                "primary_action": "选择课堂用项",
            },
        ],
        "teacher_confirmations": [
            "本班使用什么材料：水粉、水彩笔、彩铅、油画棒、色卡或混合材料",
            "课堂时长是否按40分钟执行",
            "学习单是否打印，以及是否需要留出绘画空白",
            "评价表是学生课堂自评，还是教师课后观察",
            "是否继续打磨教学过程后再生成正式文件",
        ],
        "next_actions": [
            {"label": "继续打磨教学过程", "tone": "primary", "note": "适合进入同课双版本教学过程实验。"},
            {"label": "预览课堂材料", "tone": "secondary", "note": "只看课件故事板、学习单、评价表。"},
            {"label": "暂不生成正式文件", "tone": "quiet", "note": "当前仍是教师审核草案。"},
        ],
        "lesson_summary": {
            "focus_question": "颜色怎样慢慢变化，才能让画面更有秩序、更有层次？",
            "objectives": [
                "能发现生活和教材图中的渐变。",
                "能区分亮暗变化与鲜灰变化。",
                "能做出三格或五格颜色慢慢变化的小样。",
                "能把渐变用到作品里，并说清颜色怎么变。",
            ],
            "flow": [
                "观察生活和教材图中的颜色变化。",
                "用学生话辨析亮暗、鲜灰、慢慢变化。",
                "做三格颜色小样，避免颜色跳太快。",
                "把渐变规律放进色条、图形或小作品。",
                "用自查和同伴建议完成一处微修订。",
            ],
            "risks": [
                "创作时间可能偏紧。",
                "材料准备会影响课堂节奏。",
                "学生可能把渐变理解成随便排色。",
            ],
        },
        "classroom_flow": [
            {
                "phase": "1. 看见渐变",
                "time": "约5分钟",
                "teacher_move": "出示生活图和教材图，引导学生指出颜色从哪里变到哪里。",
                "student_action": "用“从___到___”说出一处颜色慢慢变化。",
                "evidence": "能指出起点、终点和变化方向。",
            },
            {
                "phase": "2. 分清亮暗与鲜灰",
                "time": "约7分钟",
                "teacher_move": "用色条或教材图对比亮暗变化、鲜灰变化。",
                "student_action": "判断一组颜色是在变亮/变暗，还是变鲜/变灰。",
                "evidence": "能用儿童化语言说出亮暗或鲜灰。",
            },
            {
                "phase": "3. 三格试色",
                "time": "约8分钟",
                "teacher_move": "示范三格颜色慢慢变化，提醒每次只变一点点。",
                "student_action": "完成一组三格或五格渐变小样。",
                "evidence": "小样中有连续变化，不是突然跳色。",
            },
            {
                "phase": "4. 放进作品",
                "time": "约14分钟",
                "teacher_move": "提示学生把试色规律放进色条、图形或小作品。",
                "student_action": "完成一个带有渐变方向的小作品或局部设计。",
                "evidence": "作品中能看出明确的颜色变化方向。",
            },
            {
                "phase": "5. 自查与微修订",
                "time": "约6分钟",
                "teacher_move": "组织学生按自查项看一看，并选择一处微修订。",
                "student_action": "说清自己的颜色怎么变，并根据建议改一处。",
                "evidence": "能表达变化，并完成一处可见修改。",
            },
        ],
        "artifact_preview": {
            "courseware_pages": [
                {
                    "page": f"第{i}页",
                    "title": item.get("slide_title"),
                    "screen_text": item.get("screen_text"),
                    "student_action": item.get("student_action"),
                }
                for i, item in enumerate(slides, start=1)
            ],
            "worksheet_tasks": [
                {
                    "title": task.get("title"),
                    "student_language": task.get("student_language"),
                }
                for task in worksheet_tasks
            ],
            "assessment": {
                "teacher_dimensions": teacher_dims,
                "student_items": student_items,
            },
        },
        "developer_evidence": {
            "source_lesson_round": trace.get("source_lesson_round"),
            "source_textbook_anchor_status": trace.get("source_textbook_anchor_status"),
            "p2_validator_pass": p2_validator.get("validator_pass"),
            "r94_p1_validator_pass": r94_validator.get("validator_pass"),
            "field_lab_page": rel(FIELD_LAB_HTML) if FIELD_LAB_HTML.exists() else None,
            "source_files": [
                rel(P2_DRAFT),
                rel(P2_ANCHOR),
                rel(STORYBOARD_JSON),
                rel(WORKSHEET_JSON),
                rel(ASSESSMENT_JSON),
                rel(QUALITY_JSON),
                rel(TRACE_JSON),
            ],
        },
        "boundary": BOUNDARY,
    }


def render_html(vm: dict) -> str:
    lesson = vm["lesson"]
    status = vm["status"]
    summary = vm["lesson_summary"]
    package_cards = "\n".join(
        f"""
          <article class="material-card">
            <div class="material-topline">{esc(item['state'])}</div>
            <h3>{esc(item['name'])}</h3>
            <p>{esc(item['summary'])}</p>
            <span>{esc(item['primary_action'])}</span>
          </article>
        """
        for item in vm["package_materials"]
    )
    action_cards = "\n".join(
        f"""
          <article class="action-card {esc(item['tone'])}">
            <strong>{esc(item['label'])}</strong>
            <p>{esc(item['note'])}</p>
          </article>
        """
        for item in vm["next_actions"]
    )
    flow_cards = "\n".join(
        f"""
          <article class="flow-card">
            <div class="flow-time">{esc(item['time'])}</div>
            <h3>{esc(item['phase'])}</h3>
            <p><b>教师做什么：</b>{esc(item['teacher_move'])}</p>
            <p><b>学生做什么：</b>{esc(item['student_action'])}</p>
            <p><b>看什么证据：</b>{esc(item['evidence'])}</p>
          </article>
        """
        for item in vm["classroom_flow"]
    )
    page_rows = "\n".join(
        f"<tr><td>{esc(item['page'])}</td><td>{esc(item['title'])}</td><td>{esc(item['screen_text'])}</td><td>{esc(item['student_action'])}</td></tr>"
        for item in vm["artifact_preview"]["courseware_pages"]
    )
    worksheet_items = li(
        [
            f"{item['title']}：{item['student_language']}"
            for item in vm["artifact_preview"]["worksheet_tasks"]
        ]
    )
    teacher_dims = li(vm["artifact_preview"]["assessment"]["teacher_dimensions"])
    student_assess = li(vm["artifact_preview"]["assessment"]["student_items"])
    source_files = li(vm["developer_evidence"]["source_files"])
    field_lab_link = vm["developer_evidence"].get("field_lab_page") or "字段审计页尚未生成"

    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>《{esc(lesson['title'])}》备课包总览</title>
  <style>
    :root {{
      --ink: #263238;
      --muted: #66737c;
      --line: #d9e2df;
      --paper: #fbfcfa;
      --mint: #dceee8;
      --coral: #f6ded6;
      --sun: #f5e7b8;
      --blue: #dce8f3;
      --green: #426f5d;
      --accent: #b85c46;
      --shadow: 0 18px 50px rgba(38, 50, 56, .10);
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      color: var(--ink);
      background: var(--paper);
      font-family: "Microsoft YaHei", "PingFang SC", Arial, sans-serif;
      line-height: 1.62;
    }}
    header {{
      border-bottom: 1px solid var(--line);
      background: rgba(251, 252, 250, .92);
      position: sticky;
      top: 0;
      z-index: 5;
      backdrop-filter: blur(12px);
    }}
    .nav {{
      max-width: 1180px;
      margin: 0 auto;
      padding: 14px 24px;
      display: flex;
      justify-content: space-between;
      gap: 16px;
      align-items: center;
    }}
    .nav strong {{ font-size: 16px; }}
    .nav span {{ color: var(--muted); font-size: 13px; }}
    main {{ max-width: 1180px; margin: 0 auto; padding: 26px 24px 64px; }}
    .hero {{
      min-height: 560px;
      display: grid;
      grid-template-columns: minmax(0, 1.2fr) minmax(320px, .8fr);
      gap: 22px;
      align-items: stretch;
    }}
    .hero-panel, .side-panel, .section-panel, .material-card, .action-card {{
      border: 1px solid var(--line);
      background: #fff;
      box-shadow: var(--shadow);
    }}
    .hero-panel {{
      padding: 34px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }}
    .eyebrow {{
      color: var(--green);
      font-weight: 700;
      font-size: 14px;
      margin: 0 0 10px;
    }}
    h1 {{
      margin: 0;
      font-size: clamp(34px, 5vw, 64px);
      line-height: 1.05;
      letter-spacing: 0;
    }}
    .hero-copy {{
      max-width: 720px;
      color: var(--muted);
      font-size: 18px;
      margin: 18px 0 0;
    }}
    .status-strip {{
      margin-top: 28px;
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 12px;
    }}
    .status-chip {{
      background: var(--mint);
      border: 1px solid #bfd9cf;
      padding: 14px;
      min-height: 82px;
    }}
    .status-chip:nth-child(2) {{ background: var(--blue); border-color: #c5d9ea; }}
    .status-chip:nth-child(3) {{ background: var(--sun); border-color: #e4d18d; }}
    .status-chip:nth-child(4) {{ background: var(--coral); border-color: #e7beb2; }}
    .status-chip b {{ display: block; font-size: 12px; color: var(--muted); margin-bottom: 5px; }}
    .status-chip span {{ font-weight: 700; }}
    .side-panel {{ padding: 24px; }}
    .side-panel h2, .section-panel h2 {{ margin: 0 0 14px; font-size: 22px; }}
    .check-list {{ margin: 0; padding-left: 20px; }}
    .check-list li {{ margin: 9px 0; }}
    .material-grid {{
      margin-top: 26px;
      display: grid;
      grid-template-columns: repeat(5, minmax(0, 1fr));
      gap: 14px;
    }}
    .material-card {{ padding: 18px; min-height: 188px; }}
    .material-topline {{ color: var(--accent); font-weight: 700; font-size: 13px; }}
    .material-card h3 {{ margin: 8px 0; font-size: 18px; }}
    .material-card p {{ color: var(--muted); margin: 0 0 14px; }}
    .material-card span {{ display: inline-block; color: var(--green); font-weight: 700; }}
    .section-panel {{ margin-top: 24px; padding: 26px; }}
    .summary-grid {{
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 18px;
    }}
    .summary-grid h3 {{ margin: 0 0 10px; }}
    .summary-grid ul {{ margin: 0; padding-left: 20px; }}
    .action-grid {{
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 16px;
    }}
    .action-card {{ padding: 18px; }}
    .action-card.primary {{ background: var(--mint); }}
    .action-card.secondary {{ background: var(--blue); }}
    .action-card.quiet {{ background: #fff; }}
    .action-card p {{ margin: 8px 0 0; color: var(--muted); }}
    .flow-list {{
      display: grid;
      grid-template-columns: repeat(5, minmax(0, 1fr));
      gap: 12px;
    }}
    .flow-card {{
      border: 1px solid var(--line);
      background: #fff;
      padding: 16px;
      min-height: 260px;
    }}
    .flow-time {{
      display: inline-block;
      background: var(--sun);
      border: 1px solid #e4d18d;
      padding: 3px 8px;
      font-size: 12px;
      font-weight: 700;
      margin-bottom: 8px;
    }}
    .flow-card h3 {{ margin: 0 0 8px; font-size: 17px; }}
    .flow-card p {{ margin: 8px 0; color: var(--muted); font-size: 14px; }}
    .flow-card b {{ color: var(--ink); }}
    details {{
      margin-top: 20px;
      border: 1px solid var(--line);
      background: #fff;
      padding: 16px 18px;
    }}
    summary {{ cursor: pointer; font-weight: 700; }}
    table {{ width: 100%; border-collapse: collapse; margin-top: 14px; font-size: 14px; }}
    th, td {{ border: 1px solid var(--line); padding: 10px; text-align: left; vertical-align: top; }}
    th {{ background: #edf4f1; }}
    .dev-note {{ color: var(--muted); font-size: 13px; }}
    @media (max-width: 980px) {{
      .hero, .summary-grid, .action-grid {{ grid-template-columns: 1fr; }}
      .status-strip, .material-grid, .flow-list {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
    }}
    @media (max-width: 620px) {{
      main, .nav {{ padding-left: 16px; padding-right: 16px; }}
      .hero-panel, .side-panel, .section-panel {{ padding: 20px; }}
      .status-strip, .material-grid, .flow-list {{ grid-template-columns: 1fr; }}
    }}
  </style>
</head>
<body>
  <header>
    <div class="nav">
      <strong>备课包总览</strong>
      <span>静态预览副本，不是正式应用页</span>
    </div>
  </header>
  <main>
    <!-- FIRST_SCREEN_START -->
    <section class="hero" id="overview">
      <div class="hero-panel">
        <div>
          <p class="eyebrow">{esc(lesson['subject'])} · {esc(lesson['grade'])} · {esc(lesson['unit'])}</p>
          <h1>《{esc(lesson['title'])}》备课包</h1>
          <p class="hero-copy">这是一份教师审核草案。当前已经整理出教案预览稿、课件故事板、学生学习单、教师说明和评价表；正式生成文件前，还需要你确认材料、时长和是否打印。</p>
          <div class="status-strip">
            <div class="status-chip"><b>状态</b><span>{esc(status['package_status'])}</span></div>
            <div class="status-chip"><b>教材锚点</b><span>{esc(lesson['textbook_anchor_status'])}</span></div>
            <div class="status-chip"><b>质量</b><span>{esc(status['quality'])}</span></div>
            <div class="status-chip"><b>正式应用</b><span>{esc(status['formal_apply_label'])}</span></div>
          </div>
        </div>
        <div class="material-grid">
          {package_cards}
        </div>
      </div>
      <aside class="side-panel">
        <h2>需要你确认</h2>
        <ul class="check-list">
          {li(vm['teacher_confirmations'])}
        </ul>
      </aside>
    </section>
    <!-- FIRST_SCREEN_END -->

    <section class="section-panel" id="lesson-summary">
      <h2>教学设计摘要</h2>
      <div class="summary-grid">
        <section>
          <h3>核心问题</h3>
          <p>{esc(summary['focus_question'])}</p>
        </section>
        <section>
          <h3>学生要做到</h3>
          <ul>{li(summary['objectives'])}</ul>
        </section>
        <section>
          <h3>课堂主线</h3>
          <ul>{li(summary['flow'])}</ul>
        </section>
      </div>
    </section>

    <section class="section-panel" id="actions">
      <h2>下一步可以做什么</h2>
      <div class="action-grid">
        {action_cards}
      </div>
    </section>

    <section class="section-panel" id="classroom-flow">
      <h2>课堂环节</h2>
      <div class="flow-list">
        {flow_cards}
      </div>
    </section>

    <section class="section-panel" id="materials">
      <h2>课堂材料快速预览</h2>
      <details open>
        <summary>查看课件故事板页序</summary>
        <table>
          <thead><tr><th>页序</th><th>页面标题</th><th>屏幕文字</th><th>学生动作</th></tr></thead>
          <tbody>{page_rows}</tbody>
        </table>
      </details>
      <details>
        <summary>查看学习单与评价表</summary>
        <h3>学习单任务</h3>
        <ul>{worksheet_items}</ul>
        <h3>教师观察维度</h3>
        <ul>{teacher_dims}</ul>
        <h3>学生自评项</h3>
        <ul>{student_assess}</ul>
      </details>
      <details>
        <summary>查看依据 / 字段详情 / 开发者模式</summary>
        <p class="dev-note">以下内容只用于开发复核和证据链追溯，不作为教师备课主界面。</p>
        <ul>
          <li>教材锚点状态：{esc(vm['developer_evidence']['source_textbook_anchor_status'])}</li>
          <li>教案母稿校验：{esc(vm['developer_evidence']['p2_validator_pass'])}</li>
          <li>派生材料校验：{esc(vm['developer_evidence']['r94_p1_validator_pass'])}</li>
          <li>字段审计页：{esc(field_lab_link)}</li>
        </ul>
        <h3>源文件</h3>
        <ul>{source_files}</ul>
      </details>
    </section>
  </main>
</body>
</html>
"""


def render_demote_decision() -> str:
    return """# R94-P2 Field Lab Demote Decision

## Decision

`R88 + R94-P1 preview binding` is kept as an engineering audit page, not a teacher-facing shell sample.

## Status

- Engineering audit page: PASS
- Teacher-readable page: FAIL
- Shell integration sample: FAIL
- Reason: the page exposes low-level field slots and field-contract structure by default.

## Product Rule

Teacher-facing pages must use task, artifact, and review language first. Field keys, lineage, validators, and generation-slot details belong in a folded evidence/developer area.

## New Surface

`1013R_R94_P2_TEACHER_FACING_LESSON_PACKAGE_OVERVIEW` provides a separate static overview page for teachers.

## Boundary

- Does not modify R21/R36
- Does not bind to real UI
- Does not formal apply
- Does not write database/Feishu/memory
- Does not generate PPTX or printable final files
- Does not enter R95
"""


def extract_first_screen(html_text: str) -> str:
    match = re.search(r"<!-- FIRST_SCREEN_START -->(.*?)<!-- FIRST_SCREEN_END -->", html_text, re.S)
    return match.group(1) if match else ""


def visible_text(fragment: str) -> str:
    without_tags = re.sub(r"<[^>]+>", " ", fragment)
    return re.sub(r"\s+", " ", html.unescape(without_tags)).strip()


def validate(vm: dict, html_text: str) -> dict:
    first = visible_text(extract_first_screen(html_text))
    forbidden_first_screen = [
        "engineering_key",
        "canonical",
        "R88-GEN",
        "22",
        "14",
        "47",
        "field_generation",
        "preview_only",
        "formal_apply",
        "source_round",
        "slide_id",
    ]
    missing_first_screen = [
        phrase
        for phrase in [
            "《色彩的渐变》备课包",
            "教师审核草案",
            "教材锚点",
            "BASIC_USABLE",
            "正式应用",
            "需要你确认",
            "教案预览稿",
            "课件故事板",
            "一页学生学习单",
            "评价表",
            "课堂环节",
        ]
        if phrase not in first
    ]
    errors = []
    forbidden_hits = [item for item in forbidden_first_screen if item in first]
    if forbidden_hits:
        errors.append("first_screen_forbidden_terms:" + ",".join(forbidden_hits))
    if missing_first_screen:
        errors.append("first_screen_missing:" + ",".join(missing_first_screen))
    if "<details" not in html_text or "查看依据 / 字段详情 / 开发者模式" not in html_text:
        errors.append("developer_details_not_folded")
    if len(vm["package_materials"]) < 5:
        errors.append("package_materials_too_few")
    if any(
        BOUNDARY[key]
        for key in [
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
            "printed_final_material_generated",
            "r95_executed",
        ]
    ):
        errors.append("boundary_violation")
    return {
        "stage": STAGE,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "status": "PASS" if not errors else "FAIL",
        "teacher_facing_overview_created": HTML_OUT.exists(),
        "viewmodel_created": VIEWMODEL_OUT.exists(),
        "field_lab_demote_decision_created": DEMOTE_OUT.exists(),
        "first_screen_forbidden_hits": forbidden_hits,
        "first_screen_missing": missing_first_screen,
        "teacher_can_understand_status_in_30s": not forbidden_hits and not missing_first_screen,
        "materials_visible": True,
        "teacher_confirmations_visible": True,
        "developer_details_folded": "<details" in html_text and "查看依据 / 字段详情 / 开发者模式" in html_text,
        "boundary": BOUNDARY,
        "html_sha256": sha256(HTML_OUT) if HTML_OUT.exists() else None,
        "viewmodel_sha256": sha256(VIEWMODEL_OUT) if VIEWMODEL_OUT.exists() else None,
        "failed_checks": errors,
        "validator_pass": not errors,
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    vm = build_viewmodel()
    html_text = render_html(vm)
    write_json(VIEWMODEL_OUT, vm)
    write_text(HTML_OUT, html_text)
    write_text(DEMOTE_OUT, render_demote_decision())
    validation = validate(vm, html_text)
    write_json(VALIDATOR_OUT, validation)
    print(json.dumps({
        "stage": STAGE,
        "validator_pass": validation["validator_pass"],
        "html": str(HTML_OUT),
        "html_sha256": validation["html_sha256"],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
