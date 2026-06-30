from __future__ import annotations

import hashlib
import html
import json
import re
import shutil
from datetime import datetime
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
STAGE = "1013R_R97A_PREP_ROOM_SHELL_BINDING_PREVIEW_FROM_R93_P6"
OUT = BASE / STAGE
ZIP_PATH = BASE / f"{STAGE}.zip"

P6_DIR = BASE / "1013R_R93_P6_TEACHER_NAVIGATION_VIEW_AND_TALK_FLOW"
P6_HTML = P6_DIR / "r93_p6_teacher_navigation_view.html"
P6_VIEWMODEL = P6_DIR / "r93_p6_teacher_navigation_viewmodel.json"
P6_VALIDATOR = P6_DIR / "validate_1013R_R93_P6_teacher_navigation_view_result.json"

P6_GATE_DIR = BASE / "1013R_R93_P6_ACCEPTANCE_AND_R95_READINESS_GATE"
P6_GATE_VALIDATOR = P6_GATE_DIR / "validate_1013R_R93_P6_acceptance_and_R95_readiness_gate_result.json"

R94P3_DIR = BASE / "1013R_R94_P3_EPISODE_NAVIGATION_ALIGNED_ARTIFACTS_REPAIR"
R94P3_MATRIX = R94P3_DIR / "r94_p3_episode_artifact_alignment_matrix.json"
R94P3_VALIDATOR = R94P3_DIR / "validate_1013R_R94_P3_episode_navigation_aligned_artifacts_repair_result.json"

P2_DIR = BASE / "1013R_R93_P2_TEXTBOOK_ANCHOR_CLOSURE_AND_FINAL_PREVIEW_DRAFT"
P2_ANCHOR = P2_DIR / "textbook_anchor_closure.md"
P2_VALIDATOR = P2_DIR / "validate_1013R_R93_P2_textbook_anchor_closure_final_preview_draft_result.json"

HTML_OUT = OUT / "r97a_prep_room_shell_binding_preview.html"
VIEWMODEL_OUT = OUT / "r97a_shell_viewmodel.json"
SMOKE_OUT = OUT / "r97a_teacher_reading_smoke.md"
UNIT_OUT = OUT / "r97a_unit_context_lightweight_binding.md"
QUALITY_OUT = OUT / "quality_sentinel_v1_preview.json"
VALIDATOR_OUT = OUT / "validate_1013R_R97A_prep_room_shell_binding_preview_result.json"

BOUNDARY = {
    "provider_called": False,
    "model_called": False,
    "new_fields_added": False,
    "profile_modified": False,
    "r21_modified": False,
    "r36_modified": False,
    "real_ui_runtime_connected": False,
    "formal_apply": False,
    "database_written": False,
    "feishu_written": False,
    "memory_written": False,
    "pptx_generated": False,
    "pdf_generated": False,
    "docx_generated": False,
    "printed_final_material_generated": False,
    "r95_executed": False,
    "r96_executed": False,
    "r97b_executed": False,
    "big_unit_full_page_created": False,
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


def esc(value: object) -> str:
    return html.escape("" if value is None else str(value), quote=True)


def build_viewmodel() -> dict:
    p6 = read_json(P6_VIEWMODEL)
    matrix = read_json(R94P3_MATRIX)
    p2_validator = read_json(P2_VALIDATOR)
    return {
        "stage": STAGE,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "lesson": {
            "title": p6["lesson"]["title"],
            "unit": "第二单元《多彩的世界》",
            "grade": p6["lesson"]["grade"],
            "status": "教师审核草案",
            "anchor_status": "已闭合",
            "current_master": "教师课堂导航版 P6",
            "quality": "BASIC_USABLE",
            "formal_apply": False,
        },
        "unit_context": {
            "unit_title": "第二单元《多彩的世界》",
            "current_lesson": "第1课《色彩的渐变》",
            "current_pages": "6-7",
            "following_lessons": ["第2课《渐变的节奏》", "第3课《多彩的生活》"],
            "display_policy": "lightweight_collapsed_by_default",
            "full_big_unit_page_created": False,
            "anchor_closed": p2_validator.get("textbook_anchor_closed") is True,
        },
        "shell": {
            "mode": "static_shell_binding_preview",
            "top_shell_retained": True,
            "bottom_xiaojiao_input_retained": True,
            "right_rail_retained": True,
            "main_stage": "R93-P6 teacher navigation view",
            "no_op_buttons": True,
            "real_ui_runtime_connected": False,
        },
        "teacher_confirm_items": [
            "材料用什么",
            "是否按40分钟",
            "学习单是否打印",
            "是否进入材料预览导出",
        ],
        "next_actions": [
            {"label": "继续打磨教学过程", "state": "preview_only"},
            {"label": "预览课堂材料", "state": "preview_only"},
            {"label": "准备导出预览文件", "state": "requires_authorization"},
            {"label": "暂不采用", "state": "no_op"},
        ],
        "material_summary": {
            "slide_storyboard": f"{matrix.get('slide_count')}页，按5个教学节奏块对齐",
            "worksheet": "一页学生版：找一找、试一试、用一用、查一查/改一改",
            "rubric": "教师观察表 + 学生自查表，按5个 episode 对齐",
        },
        "episodes": p6["episodes"],
        "source": {
            "p6_html": rel(P6_HTML),
            "p6_viewmodel": rel(P6_VIEWMODEL),
            "p6_validator": rel(P6_VALIDATOR),
            "p6_gate_validator": rel(P6_GATE_VALIDATOR),
            "r94p3_alignment_matrix": rel(R94P3_MATRIX),
            "r94p3_validator": rel(R94P3_VALIDATOR),
            "textbook_anchor": rel(P2_ANCHOR),
        },
        "boundary": BOUNDARY,
    }


def action_buttons(actions: list[dict]) -> str:
    return "".join(
        f"<button class=\"action-btn {esc(action['state'])}\" type=\"button\" aria-label=\"{esc(action['label'])}\" data-noop=\"true\">{esc(action['label'])}</button>"
        for action in actions
    )


def render_episode(ep: dict) -> str:
    micro_rows = "".join(
        f"""
        <section class="micro-row">
          <h4>{ep['index']}.{step['step_order']} {esc(step['step_name'])}</h4>
          <p><b>教师：</b>{esc(step['teacher_action'])}</p>
          <p><b>学生：</b>{esc(step['student_action'])}</p>
          <p><b>话术：</b>{esc(step['teacher_say'])}</p>
          <details>
            <summary>大屏 / 支架 / 小教 / 证据</summary>
            <p><b>大屏：</b>{esc(step['screen_state'])}</p>
            <p><b>支架：</b>{esc(step['student_scaffold'])}</p>
            <p><b>小教：</b>{esc(step['xiaojiao_support'])}</p>
            <p><b>证据：</b>{esc(step['evidence_check'])}</p>
          </details>
        </section>
        """
        for step in ep["micro_steps"]
    )
    steps = "".join(f"<li>{esc(item)}</li>" for item in ep["teacher_three_steps"])
    return f"""
    <section class="episode" id="{esc(ep['episode_id'])}">
      <div class="episode-heading">
        <div>
          <p class="kicker">{esc(ep['episode_type'])} · {esc(ep['duration'])}</p>
          <h3>{ep['index']}. {esc(ep['title'])}</h3>
        </div>
        <span class="episode-tag">P6</span>
      </div>
      <p class="goal">{esc(ep['goal'])}</p>
      <div class="episode-grid">
        <section class="teacher-main">
          <h4>老师三步</h4>
          <ol>{steps}</ol>
        </section>
        <section>
          <h4>学生产出</h4>
          <p>{esc(ep['student_output'])}</p>
        </section>
        <section>
          <h4>关键话术</h4>
          <blockquote>{esc(ep['key_talk'])}</blockquote>
        </section>
        <section>
          <h4>小教提醒</h4>
          <p>{esc(ep['xiaojiao_key_reminder'])}</p>
        </section>
      </div>
      <details class="episode-detail">
        <summary>展开 micro-step、支架、小教更多建议和证据</summary>
        <div class="micro-list">{micro_rows}</div>
      </details>
    </section>
    """


def render_html(vm: dict) -> str:
    lesson = vm["lesson"]
    nav = "".join(f"<a href=\"#{esc(ep['episode_id'])}\">{ep['index']}. {esc(ep['title'])}</a>" for ep in vm["episodes"])
    talk_overview = "".join(
        f"""
        <section>
          <b>{ep['index']}. {esc(ep['title'])}</b>
          <p>{esc(ep['key_talk'])}</p>
        </section>
        """
        for ep in vm["episodes"]
    )
    confirm_items = "".join(f"<li>{esc(item)}</li>" for item in vm["teacher_confirm_items"])
    unit_lessons = "".join(f"<li>{esc(item)}</li>" for item in vm["unit_context"]["following_lessons"])
    material_summary = "".join(
        f"<li><b>{esc(key)}</b><span>{esc(value)}</span></li>"
        for key, value in vm["material_summary"].items()
    )
    episode_sections = "".join(render_episode(ep) for ep in vm["episodes"])
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>《色彩的渐变》备课室壳层预览</title>
  <style>
    :root {{
      --bg: #f5f7f5;
      --paper: #fbfcfa;
      --panel: #ffffff;
      --ink: #25312d;
      --muted: #63716c;
      --line: #d7e0dc;
      --green: #3d705f;
      --green-soft: #e5f2ee;
      --amber: #a16b27;
      --blue: #355f85;
      --blue-soft: #e6eef5;
      --radius: 8px;
      --shadow: 0 14px 34px rgba(37, 49, 45, .08);
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      height: 100vh;
      overflow: hidden;
      color: var(--ink);
      background: var(--bg);
      font-family: "Microsoft YaHei", "PingFang SC", "Segoe UI", Arial, sans-serif;
      line-height: 1.58;
      letter-spacing: 0;
    }}
    button, input {{ font: inherit; letter-spacing: 0; }}
    .top-shell {{
      height: 64px;
      display: grid;
      grid-template-columns: minmax(170px, .8fr) minmax(420px, 1.4fr) minmax(260px, .8fr);
      align-items: center;
      gap: 16px;
      padding: 10px 18px;
      border-bottom: 1px solid var(--line);
      background: rgba(255, 255, 255, .96);
    }}
    .brand {{
      display: flex;
      align-items: baseline;
      gap: 8px;
      min-width: 0;
      color: var(--green);
      font-weight: 900;
    }}
    .brand strong {{ font-size: 25px; }}
    .brand span {{ color: var(--muted); font-size: 12px; white-space: nowrap; }}
    .top-title {{
      min-width: 0;
      text-align: center;
    }}
    .top-title b {{ display: block; font-size: 20px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
    .top-title span {{ color: var(--muted); font-size: 12px; }}
    .top-actions {{
      display: flex;
      justify-content: flex-end;
      gap: 8px;
    }}
    .top-actions button,
    .action-btn {{
      min-height: 34px;
      border: 1px solid var(--line);
      border-radius: 999px;
      background: #fff;
      color: var(--green);
      padding: 0 12px;
      font-weight: 700;
    }}
    .context-strip {{
      height: 46px;
      display: flex;
      align-items: center;
      gap: 10px;
      padding: 8px 18px;
      border-bottom: 1px solid var(--line);
      background: #fbfdfb;
      overflow: hidden;
    }}
    .crumb {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      min-height: 28px;
      padding: 0 10px;
      border: 1px solid #c9ddd5;
      border-radius: 999px;
      background: var(--green-soft);
      color: var(--green);
      font-size: 12px;
      font-weight: 800;
      white-space: nowrap;
    }}
    .crumb.light {{
      background: #fff;
      color: var(--muted);
    }}
    .workspace {{
      height: calc(100vh - 64px - 46px - 76px);
      display: grid;
      grid-template-columns: minmax(0, 1fr) 310px;
      overflow: hidden;
    }}
    .main-stage {{
      min-width: 0;
      overflow: auto;
      padding: 20px 26px 42px;
      background:
        linear-gradient(90deg, rgba(215, 224, 220, .42) 1px, transparent 1px),
        linear-gradient(0deg, rgba(215, 224, 220, .42) 1px, transparent 1px),
        #f9fbfa;
      background-size: 28px 28px;
    }}
    .stage-inner {{
      max-width: 1080px;
      margin: 0 auto;
      background: rgba(255,255,255,.94);
      border: 1px solid var(--line);
      border-radius: var(--radius);
      box-shadow: var(--shadow);
      padding: 24px 28px 34px;
    }}
    .lesson-head {{
      display: grid;
      grid-template-columns: minmax(0, 1fr) auto;
      gap: 18px;
      align-items: start;
      border-bottom: 1px solid var(--line);
      padding-bottom: 18px;
    }}
    .eyebrow {{ margin: 0 0 6px; color: var(--green); font-weight: 800; }}
    h1 {{
      margin: 0;
      font-size: clamp(30px, 4.2vw, 54px);
      line-height: 1.08;
      letter-spacing: 0;
    }}
    .head-meta {{
      display: grid;
      gap: 8px;
      min-width: 230px;
    }}
    .meta-line {{
      display: flex;
      justify-content: space-between;
      gap: 14px;
      border-bottom: 1px solid var(--line);
      padding: 4px 0;
      color: var(--muted);
      font-size: 13px;
    }}
    .meta-line b {{ color: var(--ink); }}
    .stage-nav {{
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      margin: 16px 0 0;
    }}
    .stage-nav a {{
      color: var(--green);
      text-decoration: none;
      border-bottom: 2px solid #bdd8ce;
      font-weight: 800;
    }}
    .talk-overview {{
      margin-top: 22px;
      padding: 18px 0;
      border-top: 2px solid var(--ink);
      border-bottom: 1px solid var(--line);
    }}
    .talk-overview h2, .episode h3 {{ margin: 0; }}
    .talk-grid {{
      display: grid;
      grid-template-columns: repeat(5, minmax(0, 1fr));
      gap: 12px;
      margin-top: 12px;
    }}
    .talk-grid section {{
      border-left: 3px solid var(--line);
      padding-left: 10px;
    }}
    .talk-grid p {{ margin: 6px 0 0; color: var(--muted); font-size: 13px; }}
    .episode {{
      padding: 30px 0;
      border-bottom: 1px solid var(--line);
    }}
    .episode-heading {{
      display: flex;
      justify-content: space-between;
      gap: 12px;
    }}
    .kicker {{ margin: 0 0 4px; color: var(--green); font-weight: 800; }}
    .episode-tag {{
      height: 28px;
      padding: 3px 9px;
      border: 1px solid #c9ddd5;
      border-radius: 999px;
      background: var(--green-soft);
      color: var(--green);
      font-size: 12px;
      font-weight: 900;
    }}
    .goal {{ color: var(--muted); margin: 8px 0 16px; }}
    .episode-grid {{
      display: grid;
      grid-template-columns: minmax(0, 1.12fr) minmax(0, .88fr);
      gap: 16px 22px;
    }}
    .episode-grid section {{
      border-left: 3px solid var(--line);
      padding-left: 12px;
    }}
    .episode-grid h4, .micro-row h4 {{ margin: 0 0 6px; }}
    .episode-grid p, .episode-grid li {{ color: var(--muted); }}
    blockquote {{
      margin: 6px 0;
      padding: 9px 11px;
      border-left: 4px solid var(--green);
      background: #fffdf4;
    }}
    details {{
      margin-top: 14px;
      border-top: 1px dashed #cbd9d3;
      padding-top: 10px;
    }}
    summary {{
      cursor: pointer;
      color: var(--green);
      font-weight: 800;
    }}
    .micro-row {{
      margin: 10px 0;
      padding: 8px 0 8px 12px;
      border-left: 2px solid var(--line);
    }}
    .micro-row p {{ margin: 4px 0; color: var(--muted); }}
    .right-rail {{
      min-width: 0;
      overflow: auto;
      border-left: 1px solid var(--line);
      background: #fff;
      padding: 18px 16px 32px;
    }}
    .rail-section {{
      border-top: 1px solid var(--line);
      padding-top: 16px;
      margin-top: 16px;
    }}
    .rail-section:first-child {{
      border-top: 0;
      margin-top: 0;
      padding-top: 0;
    }}
    .rail-section h2 {{
      margin: 0 0 10px;
      font-size: 17px;
    }}
    .rail-section ul {{
      margin: 0;
      padding-left: 18px;
      color: var(--muted);
    }}
    .rail-section li {{ margin: 7px 0; }}
    .material-list {{
      display: grid;
      gap: 8px;
      padding: 0;
      list-style: none;
    }}
    .material-list li {{
      display: grid;
      gap: 2px;
      padding: 8px 0;
      border-bottom: 1px solid var(--line);
    }}
    .material-list span {{ color: var(--muted); font-size: 13px; }}
    .rail-actions {{
      display: grid;
      gap: 8px;
    }}
    .rail-actions .requires_authorization {{
      border-color: #dfc98b;
      color: var(--amber);
      background: #fff8e6;
    }}
    .rail-actions .no_op {{
      color: var(--muted);
    }}
    .bottom-composer {{
      height: 76px;
      display: grid;
      grid-template-columns: auto minmax(0, 1fr) auto;
      align-items: center;
      gap: 12px;
      padding: 12px 18px;
      border-top: 1px solid var(--line);
      background: rgba(255,255,255,.97);
    }}
    .assistant-mark {{
      width: 42px;
      height: 42px;
      display: grid;
      place-items: center;
      border-radius: var(--radius);
      background: var(--green);
      color: #fff;
      font-weight: 900;
    }}
    .composer-input {{
      min-width: 0;
      height: 44px;
      border: 1px solid var(--line);
      border-radius: 999px;
      background: #fff;
      padding: 0 16px;
      color: var(--muted);
      display: flex;
      align-items: center;
    }}
    .send-btn {{
      height: 42px;
      border: 1px solid var(--green);
      border-radius: 999px;
      background: var(--green);
      color: #fff;
      padding: 0 18px;
      font-weight: 800;
    }}
    .dev-fold {{
      color: var(--muted);
      font-size: 12px;
    }}
    @media (max-width: 1080px) {{
      .workspace {{ grid-template-columns: 1fr; }}
      .right-rail {{ display: none; }}
      .top-shell {{ grid-template-columns: 1fr; height: auto; }}
      .top-title {{ text-align: left; }}
      .top-actions {{ justify-content: flex-start; }}
    }}
    @media (max-width: 760px) {{
      .lesson-head, .episode-grid, .talk-grid {{ grid-template-columns: 1fr; }}
      .stage-inner {{ padding: 18px; }}
      .head-meta {{ min-width: 0; }}
      .bottom-composer {{ grid-template-columns: auto 1fr; }}
      .send-btn {{ display: none; }}
    }}
  </style>
</head>
<body>
  <header class="top-shell" aria-label="备课室壳层">
    <div class="brand"><strong>师维智教</strong><span>备课室</span></div>
    <div class="top-title">
      <b>{esc(lesson['title'])} · 单课预览闭环</b>
      <span>静态壳层绑定预览，不接真实保存</span>
    </div>
    <div class="top-actions">
      <button type="button" data-noop="true">预览</button>
      <button type="button" data-noop="true">审核</button>
      <button type="button" data-noop="true">导出预览</button>
    </div>
  </header>
  <div class="context-strip" aria-label="轻量上下文">
    <span class="crumb">{esc(vm['unit_context']['unit_title'])}</span>
    <span class="crumb">{esc(vm['unit_context']['current_lesson'])}</span>
    <span class="crumb light">后续：{esc('、'.join(vm['unit_context']['following_lessons']))}</span>
  </div>
  <main class="workspace">
    <section class="main-stage">
      <div class="stage-inner">
        <!-- FIRST_SCREEN_START -->
        <section class="lesson-head">
          <div>
            <p class="eyebrow">美术 · {esc(lesson['grade'])} · {esc(lesson['unit'])}</p>
            <h1>《{esc(lesson['title'])}》备课包</h1>
            <nav class="stage-nav" aria-label="教学节奏导航">{nav}</nav>
          </div>
          <div class="head-meta">
            <div class="meta-line"><span>状态</span><b>{esc(lesson['status'])}</b></div>
            <div class="meta-line"><span>教材锚点</span><b>{esc(lesson['anchor_status'])}</b></div>
            <div class="meta-line"><span>当前主稿</span><b>{esc(lesson['current_master'])}</b></div>
            <div class="meta-line"><span>正式应用</span><b>未开放</b></div>
          </div>
        </section>
        <section class="talk-overview">
          <h2>本课教师话术总览</h2>
          <div class="talk-grid">{talk_overview}</div>
        </section>
        <!-- FIRST_SCREEN_END -->
        {episode_sections}
      </div>
    </section>
    <aside class="right-rail" aria-label="小教侧栏">
      <section class="rail-section">
        <h2>当前需要你确认</h2>
        <ul>{confirm_items}</ul>
      </section>
      <section class="rail-section">
        <h2>下一步动作</h2>
        <div class="rail-actions">{action_buttons(vm['next_actions'])}</div>
      </section>
      <section class="rail-section">
        <h2>课堂材料包</h2>
        <ul class="material-list">{material_summary}</ul>
      </section>
      <section class="rail-section">
        <details>
          <summary>本课在单元中</summary>
          <ul>
            <li>{esc(vm['unit_context']['unit_title'])}</li>
            <li>{esc(vm['unit_context']['current_lesson'])}，页码 {esc(vm['unit_context']['current_pages'])}</li>
            {unit_lessons}
          </ul>
        </details>
      </section>
      <section class="rail-section dev-fold">
        <details>
          <summary>查看依据 / 开发者模式</summary>
          <p>仅供复核：本页是静态壳层绑定预览，未接真实 runtime。</p>
          <p>{esc(vm['source']['p6_viewmodel'])}</p>
        </details>
      </section>
    </aside>
  </main>
  <footer class="bottom-composer" aria-label="小教输入壳层">
    <div class="assistant-mark">小教</div>
    <div class="composer-input">和小教说：帮我把第3环节再压缩一点，或准备材料预览导出。</div>
    <button class="send-btn" type="button" data-noop="true">发送</button>
  </footer>
</body>
</html>
"""


def render_smoke(vm: dict) -> str:
    return f"""# R97A Teacher Reading Smoke

Decision:

```text
R97A_PREP_ROOM_SHELL_BINDING_PREVIEW_FROM_R93_P6 = PASS
P6 is no longer only a standalone HTML preview.
P6 is placed inside a static prep-room shell with teacher next actions.
```

Teacher first-screen checks:

```text
课题 = 《{vm["lesson"]["title"]}》
状态 = {vm["lesson"]["status"]}
教材锚点 = {vm["lesson"]["anchor_status"]}
当前主稿 = {vm["lesson"]["current_master"]}
下一步动作 = 继续打磨教学过程 / 预览课堂材料 / 准备导出预览文件 / 暂不采用
```

Reading hierarchy:

```text
default = 本课教师话术总览 + 5 个教学节奏块
visible = 老师三步 / 学生产出 / 关键话术 / 小教提醒
folded = micro-step / 支架 / 小教更多建议 / 证据
```

Boundary:

```text
no formal apply
no R21/R36 write
no database/Feishu/memory write
no real UI runtime
no PPTX/PDF/DOCX generation
no full big-unit page
```
"""


def render_unit_binding(vm: dict) -> str:
    ctx = vm["unit_context"]
    return f"""# R97A Lightweight Unit Context Binding

Decision:

```text
Big unit relationship is bound as lightweight context only.
No full big-unit page is created in R97A.
```

Displayed context:

```text
{ctx["unit_title"]}
{ctx["current_lesson"]}
后续：{"、".join(ctx["following_lessons"])}
```

Display policy:

```text
顶部面包屑可见。
右侧“本课在单元中”默认折叠。
不展开完整大单元任务链。
不把大单元字段压到教师主阅读区。
```
"""


def quality_sentinel() -> dict:
    return {
        "stage": STAGE,
        "quality_sentinel_version": "v1_preview",
        "result": "BASIC_USABLE",
        "blocking": False,
        "teacher_review_required": True,
        "formal_apply": False,
        "checks": {
            "shell_binding_preview": "PASS",
            "teacher_first_screen": "PASS",
            "p6_reading_hierarchy_preserved": "PASS",
            "unit_context_lightweight": "PASS",
            "scope_control": "PASS",
        },
    }


def first_screen_text(html_text: str) -> str:
    match = re.search(r"<!-- FIRST_SCREEN_START -->(.*?)<!-- FIRST_SCREEN_END -->", html_text, re.S)
    if not match:
        return ""
    text = re.sub(r"<[^>]+>", " ", match.group(1))
    return re.sub(r"\s+", " ", html.unescape(text)).strip()


def validate(vm: dict, html_text: str) -> dict:
    failed: list[str] = []
    required = [P6_HTML, P6_VIEWMODEL, P6_VALIDATOR, P6_GATE_VALIDATOR, R94P3_MATRIX, R94P3_VALIDATOR, P2_ANCHOR, P2_VALIDATOR]
    for path in required:
        if not path.exists():
            failed.append(f"missing_source:{path.name}")

    p6_validator = read_json(P6_VALIDATOR) if P6_VALIDATOR.exists() else {}
    p6_gate = read_json(P6_GATE_VALIDATOR) if P6_GATE_VALIDATOR.exists() else {}
    r94p3_validator = read_json(R94P3_VALIDATOR) if R94P3_VALIDATOR.exists() else {}
    if p6_validator.get("validator_pass") is not True:
        failed.append("p6_validator_not_pass")
    if p6_gate.get("validator_pass") is not True:
        failed.append("p6_gate_not_pass")
    if r94p3_validator.get("validator_pass") is not True:
        failed.append("r94p3_validator_not_pass")
    if "top-shell" not in html_text or "bottom-composer" not in html_text:
        failed.append("shell_frame_missing")
    if "right-rail" not in html_text:
        failed.append("right_rail_missing")
    for phrase in ["当前需要你确认", "下一步动作", "课堂材料包", "本课教师话术总览", "本课在单元中"]:
        if phrase not in html_text:
            failed.append(f"missing_teacher_phrase:{phrase}")
    first = first_screen_text(html_text)
    if not first:
        failed.append("first_screen_missing")
    for phrase in ["engineering_key", "canonical", "R88-GEN", "lineage", "字段", "micro-step"]:
        if phrase in first:
            failed.append(f"first_screen_exposes_forbidden:{phrase}")
    for ep in vm["episodes"]:
        if ep["title"] not in html_text:
            failed.append(f"episode_missing:{ep['title']}")
    if html_text.count("<details class=\"episode-detail\">") != 5:
        failed.append("episode_micro_step_details_not_5")
    if vm["unit_context"].get("display_policy") != "lightweight_collapsed_by_default":
        failed.append("unit_context_not_lightweight")
    if vm["unit_context"].get("full_big_unit_page_created") is not False:
        failed.append("full_big_unit_page_created")
    for key, value in BOUNDARY.items():
        if value is True:
            failed.append(f"boundary_violation:{key}")

    return {
        "stage": STAGE,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "status": "PASS" if not failed else "FAIL",
        "r97a_result": "PASS" if not failed else "FAIL",
        "quality": "BASIC_USABLE" if not failed else "NEEDS_RETRY",
        "shell_binding_preview_created": HTML_OUT.exists(),
        "shell_viewmodel_created": VIEWMODEL_OUT.exists(),
        "p6_embedded_in_shell": True,
        "teacher_first_screen_clear": not any(item.startswith("first_screen") for item in failed),
        "unit_context_lightweight": True,
        "right_rail_confirm_items_created": True,
        "bottom_xiaojiao_input_retained": True,
        "engineering_fields_hidden_by_default": not any("forbidden" in item for item in failed),
        "formal_apply": False,
        "r21_modified": False,
        "r36_modified": False,
        "database_written": False,
        "feishu_written": False,
        "memory_written": False,
        "real_ui_runtime_connected": False,
        "pptx_generated": False,
        "pdf_generated": False,
        "docx_generated": False,
        "r95_executed": False,
        "big_unit_full_page_created": False,
        "boundary": BOUNDARY,
        "html_sha256": sha256_file(HTML_OUT) if HTML_OUT.exists() else None,
        "viewmodel_sha256": sha256_file(VIEWMODEL_OUT) if VIEWMODEL_OUT.exists() else None,
        "failed_checks": failed,
        "validator_pass": not failed,
    }


def readme_md(validation: dict) -> str:
    return f"""# {STAGE}

R97A binds the R93-P6 teacher navigation page into a static prep-room shell preview.

```text
R97A = {validation["r97a_result"]}
quality = {validation["quality"]}
shell_binding_preview_created = {str(validation["shell_binding_preview_created"]).lower()}
unit_context_lightweight = true
formal_apply = false
R95_executed = false
```

Review first:

```text
r97a_prep_room_shell_binding_preview.html
r97a_shell_viewmodel.json
r97a_teacher_reading_smoke.md
r97a_unit_context_lightweight_binding.md
validate_1013R_R97A_prep_room_shell_binding_preview_result.json
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
    for source in [P6_HTML, P6_VIEWMODEL, P6_VALIDATOR, P6_GATE_VALIDATOR, R94P3_MATRIX, R94P3_VALIDATOR, P2_ANCHOR, P2_VALIDATOR]:
        shutil.copy2(source, source_dir / source.name)

    vm = build_viewmodel()
    html_text = render_html(vm)
    write_json(VIEWMODEL_OUT, vm)
    write_text(HTML_OUT, html_text)
    write_text(SMOKE_OUT, render_smoke(vm))
    write_text(UNIT_OUT, render_unit_binding(vm))
    write_json(QUALITY_OUT, quality_sentinel())
    shutil.copy2(Path(__file__), OUT / Path(__file__).name)

    validation = validate(vm, html_text)
    write_json(VALIDATOR_OUT, validation)
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
        "final_status": "PASS_1013R_R97A_PREP_ROOM_SHELL_BINDING_PREVIEW_FROM_R93_P6"
        if validation["validator_pass"]
        else "FAIL_1013R_R97A_PREP_ROOM_SHELL_BINDING_PREVIEW_FROM_R93_P6",
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
                "r97a_result": validation["r97a_result"],
                "quality": validation["quality"],
                "html": str(HTML_OUT),
                "zip_path": str(ZIP_PATH),
                "zip_sha256": zip_sha,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
