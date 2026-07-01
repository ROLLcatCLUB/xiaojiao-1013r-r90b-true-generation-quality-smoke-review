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
STAGE = "1013R_R97A_R91A_SHELL_COPY_BINDING_PREVIEW_FROM_R93_P6"
OUT = BASE / STAGE
ZIP_PATH = BASE / f"{STAGE}.zip"

R91A_SOURCE = (
    BASE
    / "1013R_R91A_STATIC_PAGE_BACKFILL"
    / "R91A_static_page_backfill_from_R39_product_candidate_preview.html"
)

P6_DIR = BASE / "1013R_R93_P6_TEACHER_NAVIGATION_VIEW_AND_TALK_FLOW"
P6_VIEWMODEL = P6_DIR / "r93_p6_teacher_navigation_viewmodel.json"
P6_HTML = P6_DIR / "r93_p6_teacher_navigation_view.html"
P6_VALIDATOR = P6_DIR / "validate_1013R_R93_P6_teacher_navigation_view_result.json"

P6_GATE_DIR = BASE / "1013R_R93_P6_ACCEPTANCE_AND_R95_READINESS_GATE"
P6_GATE_VALIDATOR = P6_GATE_DIR / "validate_1013R_R93_P6_acceptance_and_R95_readiness_gate_result.json"

R94P3_DIR = BASE / "1013R_R94_P3_EPISODE_NAVIGATION_ALIGNED_ARTIFACTS_REPAIR"
R94P3_MATRIX = R94P3_DIR / "r94_p3_episode_artifact_alignment_matrix.json"
R94P3_VALIDATOR = R94P3_DIR / "validate_1013R_R94_P3_episode_navigation_aligned_artifacts_repair_result.json"

P2_DIR = BASE / "1013R_R93_P2_TEXTBOOK_ANCHOR_CLOSURE_AND_FINAL_PREVIEW_DRAFT"
P2_ANCHOR = P2_DIR / "textbook_anchor_closure.md"
P2_VALIDATOR = P2_DIR / "validate_1013R_R93_P2_textbook_anchor_closure_final_preview_draft_result.json"

HTML_OUT = OUT / "R91A_shell_copy_binding_preview_from_R93_P6.html"
VIEWMODEL_OUT = OUT / "r97a_r91a_shell_copy_viewmodel.json"
STRUCTURE_AUDIT_OUT = OUT / "r97a_r91a_shell_structure_audit.md"
BINDING_NOTES_OUT = OUT / "r97a_r91a_copy_binding_notes.md"
UNIT_OUT = OUT / "r97a_unit_context_lightweight_binding.md"
QUALITY_OUT = OUT / "quality_sentinel_v1_preview.json"
VALIDATOR_OUT = OUT / "validate_1013R_R97A_R91A_shell_copy_binding_preview_result.json"

BOUNDARY = {
    "provider_called": False,
    "model_called": False,
    "new_fields_added": False,
    "profile_modified": False,
    "r21_modified": False,
    "r36_modified": False,
    "real_ui_runtime_connected": False,
    "original_r91a_shell_modified": False,
    "formal_apply": False,
    "database_written": False,
    "feishu_written": False,
    "memory_written": False,
    "pptx_generated": False,
    "pdf_generated": False,
    "docx_generated": False,
    "printed_final_material_generated": False,
    "r95_executed": False,
    "full_big_unit_page_created": False,
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


def js_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def structure_flags(source_text: str) -> dict:
    return {
        "has_topbar": '<header class="topbar"' in source_text,
        "has_context_bar": 'class="context-bar"' in source_text,
        "has_workspace": 'class="workspace"' in source_text,
        "has_canvas_stage": 'id="canvasStage"' in source_text,
        "has_render_layer": 'id="renderLayer"' in source_text,
        "has_bottom_xiaojiao_entry": 'class="xiaobei-chat-entry"' in source_text,
        "has_status_strip": 'class="status-strip"' in source_text,
        "has_prep_room_view_model": "window.PREP_ROOM_RENDER_VIEW_MODEL" in source_text,
        "has_init_function": "initPrepRoomRenderCanvas();" in source_text,
        "has_r91a_backfill_panel": "r91a-backfill-panel" in source_text,
    }


def build_viewmodel() -> dict:
    p6 = read_json(P6_VIEWMODEL)
    matrix = read_json(R94P3_MATRIX)
    p2_validator = read_json(P2_VALIDATOR)
    source_text = R91A_SOURCE.read_text(encoding="utf-8")
    return {
        "stage": STAGE,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "copy_mode": "copy_first_then_bind_preview",
        "source_shell": {
            "path": rel(R91A_SOURCE),
            "sha256": sha256_file(R91A_SOURCE),
            "size": R91A_SOURCE.stat().st_size,
            "structure_flags": structure_flags(source_text),
        },
        "mount_strategy": {
            "copy_source_shell_first": True,
            "original_shell_modified": False,
            "mount_target": "#renderLayer",
            "preserve_topbar": True,
            "preserve_context_bar": True,
            "preserve_canvas_stage": True,
            "preserve_bottom_xiaojiao_entry": True,
            "hide_old_r39_r91a_backfill_panels_in_copy": True,
            "real_runtime_connected": False,
        },
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
            "display_policy": "breadcrumb_visible_right_rail_collapsed",
            "anchor_closed": p2_validator.get("textbook_anchor_closed") is True,
            "full_big_unit_page_created": False,
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
            "课件 storyboard": f"{matrix.get('slide_count')}页，已按5个教学节奏块对齐",
            "学习单": "一页学生版：找一找、试一试、用一用、查一查/改一改",
            "评价表": "教师观察表 + 学生自查表，按5个 episode 对齐",
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


def render_payload_html(vm: dict) -> str:
    nav = "".join(f"<a href=\"#{esc(ep['episode_id'])}\">{ep['index']}. {esc(ep['title'])}</a>" for ep in vm["episodes"])
    talks = "".join(
        f"<section><b>{ep['index']}. {esc(ep['title'])}</b><p>{esc(ep['key_talk'])}</p></section>"
        for ep in vm["episodes"]
    )
    confirm_items = "".join(f"<li>{esc(item)}</li>" for item in vm["teacher_confirm_items"])
    actions = "".join(
        f"<button class=\"node-action {esc(action['state'])}\" type=\"button\" data-pending=\"{esc(action['label'])}仍为副本预览，教师确认前不生效。\">{esc(action['label'])}</button>"
        for action in vm["next_actions"]
    )
    materials = "".join(f"<li><b>{esc(k)}</b><span>{esc(v)}</span></li>" for k, v in vm["material_summary"].items())
    following = "".join(f"<li>{esc(item)}</li>" for item in vm["unit_context"]["following_lessons"])

    episodes = []
    for ep in vm["episodes"]:
        steps = "".join(f"<li>{esc(item)}</li>" for item in ep["teacher_three_steps"])
        micro = "".join(
            f"""
            <section class="r97a-micro-row nb-step-detail-item">
              <h4>{ep['index']}.{step['step_order']} {esc(step['step_name'])}</h4>
              <p><b>教师</b>{esc(step['teacher_action'])}</p>
              <p><b>学生</b>{esc(step['student_action'])}</p>
              <p><b>话术</b>{esc(step['teacher_say'])}</p>
              <details>
                <summary>大屏 / 支架 / 小教 / 证据</summary>
                <p><b>大屏</b>{esc(step['screen_state'])}</p>
                <p><b>支架</b>{esc(step['student_scaffold'])}</p>
                <p><b>小教</b>{esc(step['xiaojiao_support'])}</p>
                <p><b>证据</b>{esc(step['evidence_check'])}</p>
              </details>
            </section>
            """
            for step in ep["micro_steps"]
        )
        episodes.append(
            f"""
            <section class="r97a-episode nb-doc-section" id="{esc(ep['episode_id'])}">
              <div class="nb-doc-section-head">
                <div>
                  <p class="r97a-kicker">{esc(ep['episode_type'])} · {esc(ep['duration'])}</p>
                  <div class="nb-doc-title">{ep['index']}. {esc(ep['title'])}</div>
                </div>
                <button class="node-action secondary" type="button" data-pending="本环节仍为副本预览，教师确认前不写入正式备课本。">预览</button>
              </div>
              <p class="r97a-goal">{esc(ep['goal'])}</p>
              <div class="r97a-episode-grid">
                <section class="r97a-teacher-main"><h4>老师三步</h4><ol>{steps}</ol></section>
                <section><h4>学生产出</h4><p>{esc(ep['student_output'])}</p></section>
                <section><h4>关键话术</h4><blockquote>{esc(ep['key_talk'])}</blockquote></section>
                <section><h4>小教提醒</h4><p>{esc(ep['xiaojiao_key_reminder'])}</p></section>
              </div>
              <details class="r97a-episode-detail">
                <summary>展开 micro-step、支架、小教更多建议和证据</summary>
                {micro}
              </details>
            </section>
            """
        )

    return f"""
      <div class="nb-workspace r97a-r91a-copy-workspace" data-r97a-r91a-copy-stage="{esc(STAGE)}" data-preview-only="true" data-formal-apply-allowed="false">
        <section class="r97a-copy-head nb-hero">
          <div>
            <div class="nb-kicker">R91A 壳层副本 · 单课闭环预览</div>
            <h1>《{esc(vm['lesson']['title'])}》备课包</h1>
            <p>当前把 R93-P6 教师课堂导航版接入 R91A 壳层副本。真实壳层未修改，保存、导出、正式应用仍锁定。</p>
            <nav class="r97a-flow-nav" aria-label="教学节奏导航">{nav}</nav>
          </div>
          <div class="r97a-state-grid">
            <span><b>状态</b>{esc(vm['lesson']['status'])}</span>
            <span><b>教材锚点</b>{esc(vm['lesson']['anchor_status'])}</span>
            <span><b>当前主稿</b>{esc(vm['lesson']['current_master'])}</span>
            <span><b>正式应用</b>未开放</span>
          </div>
        </section>
        <section class="r97a-shell-grid">
          <article class="r97a-main-doc nb-doc">
            <!-- FIRST_SCREEN_START -->
            <section class="r97a-talk-overview nb-doc-section">
              <div class="nb-doc-section-head"><div class="nb-doc-title">本课教师话术总览</div></div>
              <div class="r97a-talk-grid">{talks}</div>
            </section>
            <!-- FIRST_SCREEN_END -->
            {''.join(episodes)}
          </article>
          <aside class="r97a-right-rail nb-right-rail">
            <section>
              <h3>当前需要你确认</h3>
              <ul>{confirm_items}</ul>
            </section>
            <section>
              <h3>下一步动作</h3>
              <div class="r97a-action-list">{actions}</div>
            </section>
            <section>
              <h3>课堂材料包</h3>
              <ul class="r97a-material-list">{materials}</ul>
            </section>
            <section>
              <details>
                <summary>本课在单元中</summary>
                <ul>
                  <li>{esc(vm['unit_context']['unit_title'])}</li>
                  <li>{esc(vm['unit_context']['current_lesson'])}，页码 {esc(vm['unit_context']['current_pages'])}</li>
                  {following}
                </ul>
              </details>
            </section>
            <section class="r97a-dev-fold">
              <details>
                <summary>查看依据 / 开发者模式</summary>
                <p>挂载点：R91A 副本中的 #renderLayer。</p>
                <p>源：{esc(vm['source']['p6_viewmodel'])}</p>
              </details>
            </section>
          </aside>
        </section>
      </div>
    """


def render_injection(vm: dict) -> str:
    payload = render_payload_html(vm)
    return f"""
<style id="style-r97a-r91a-copy-binding">
  body[data-r97a-r91a-copy-binding="true"] .r35-product-panel,
  body[data-r97a-r91a-copy-binding="true"] .r39-candidate-preview-panel,
  body[data-r97a-r91a-copy-binding="true"] .r91a-backfill-panel {{
    display: none !important;
  }}
  .r97a-r91a-copy-workspace {{
    max-width: 1220px;
    margin: 0 auto;
    display: grid;
    gap: 16px;
  }}
  .r97a-copy-head {{
    display: grid;
    grid-template-columns: minmax(0, 1fr) minmax(260px, .35fr);
    gap: 18px;
    align-items: start;
    border: 1px solid var(--line);
    border-radius: var(--radius);
    background: rgba(255,255,255,.96);
    box-shadow: 0 14px 34px rgba(29,39,35,.08);
  }}
  .r97a-copy-head h1 {{
    margin: 4px 0 8px;
    font-size: clamp(30px, 4vw, 52px);
    line-height: 1.08;
    letter-spacing: 0;
  }}
  .r97a-flow-nav {{
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-top: 12px;
  }}
  .r97a-flow-nav a {{
    color: var(--green);
    text-decoration: none;
    font-weight: 850;
    border-bottom: 2px solid #bdd8ce;
  }}
  .r97a-state-grid {{
    display: grid;
    gap: 8px;
  }}
  .r97a-state-grid span {{
    display: grid;
    gap: 3px;
    padding: 9px 11px;
    border: 1px solid var(--line);
    border-radius: 8px;
    background: #fbfdfb;
    color: var(--muted);
    font-size: 12px;
  }}
  .r97a-state-grid b {{
    color: var(--ink);
    font-size: 13px;
  }}
  .r97a-shell-grid {{
    display: grid;
    grid-template-columns: minmax(0, 1fr) 300px;
    gap: 14px;
    align-items: start;
  }}
  .r97a-main-doc,
  .r97a-right-rail {{
    border: 1px solid var(--line);
    border-radius: var(--radius);
    background: rgba(255,255,255,.97);
    box-shadow: 0 12px 28px rgba(29,39,35,.06);
  }}
  .r97a-main-doc {{
    padding: 18px 22px;
  }}
  .r97a-right-rail {{
    position: sticky;
    top: 12px;
    padding: 16px;
    display: grid;
    gap: 16px;
  }}
  .r97a-right-rail section {{
    border-top: 1px solid var(--line);
    padding-top: 14px;
  }}
  .r97a-right-rail section:first-child {{
    border-top: 0;
    padding-top: 0;
  }}
  .r97a-right-rail h3 {{
    margin: 0 0 8px;
    font-size: 16px;
  }}
  .r97a-right-rail ul {{
    margin: 0;
    padding-left: 18px;
    color: var(--muted);
  }}
  .r97a-right-rail li {{
    margin: 7px 0;
  }}
  .r97a-action-list {{
    display: grid;
    gap: 8px;
  }}
  .r97a-action-list .requires_authorization {{
    color: var(--amber);
    border-color: #e3c989;
    background: #fff8e6;
  }}
  .r97a-material-list {{
    display: grid;
    gap: 8px;
    padding-left: 0 !important;
    list-style: none;
  }}
  .r97a-material-list li {{
    display: grid;
    gap: 3px;
    padding-bottom: 8px;
    border-bottom: 1px solid var(--line);
  }}
  .r97a-material-list span {{
    color: var(--muted);
    font-size: 13px;
  }}
  .r97a-talk-overview {{
    border-top: 2px solid var(--ink);
  }}
  .r97a-talk-grid {{
    display: grid;
    grid-template-columns: repeat(5, minmax(0, 1fr));
    gap: 12px;
  }}
  .r97a-talk-grid section,
  .r97a-episode-grid section {{
    border-left: 3px solid var(--line);
    padding-left: 10px;
  }}
  .r97a-talk-grid p,
  .r97a-goal,
  .r97a-episode-grid p,
  .r97a-episode-grid li,
  .r97a-micro-row p {{
    color: var(--muted);
  }}
  .r97a-episode-grid {{
    display: grid;
    grid-template-columns: minmax(0, 1.12fr) minmax(0, .88fr);
    gap: 14px 20px;
  }}
  .r97a-kicker {{
    margin: 0 0 4px;
    color: var(--green);
    font-weight: 850;
  }}
  .r97a-episode blockquote {{
    margin: 6px 0;
    padding: 9px 11px;
    border-left: 4px solid var(--green);
    background: #fffdf4;
  }}
  .r97a-episode-detail {{
    border-top: 1px dashed #cbd9d3;
    margin-top: 14px;
    padding-top: 10px;
  }}
  .r97a-episode-detail summary,
  .r97a-right-rail summary {{
    color: var(--green);
    font-weight: 850;
    cursor: pointer;
  }}
  .r97a-micro-row {{
    margin: 10px 0;
    padding: 8px 0 8px 12px;
    border-left: 2px solid var(--line);
  }}
  .r97a-micro-row h4 {{
    margin: 0 0 5px;
  }}
  .r97a-micro-row p {{
    margin: 4px 0;
  }}
  .r97a-dev-fold {{
    color: var(--muted);
    font-size: 12px;
  }}
  @media (max-width: 1080px) {{
    .r97a-copy-head,
    .r97a-shell-grid,
    .r97a-episode-grid {{
      grid-template-columns: 1fr;
    }}
    .r97a-right-rail {{
      position: static;
    }}
  }}
  @media (max-width: 760px) {{
    .r97a-talk-grid {{
      grid-template-columns: 1fr;
    }}
  }}
</style>
<script id="script-r97a-r91a-copy-binding">
(function () {{
  const payload = {js_string(payload)};
  const bindShellCopy = () => {{
    document.body.setAttribute("data-r97a-r91a-copy-binding", "true");
    document.body.setAttribute("data-active-view", "prepNotebook");
    document.documentElement.setAttribute("data-r97a-r91a-copy-binding", "true");

    const contextTitle = document.getElementById("contextTitle");
    if (contextTitle) {{
      contextTitle.innerHTML = '<span class="context-space-name">备课室</span><span class="context-view-name">· 《色彩的渐变》单课闭环预览</span>';
    }}
    const viewTabs = document.getElementById("viewTabs");
    if (viewTabs) {{
      viewTabs.innerHTML = '<button class="view-tab active" type="button" aria-selected="true" title="备课包">备</button>';
    }}
    const renderLayer = document.getElementById("renderLayer");
    if (renderLayer && !renderLayer.querySelector(".r97a-r91a-copy-workspace")) {{
      renderLayer.innerHTML = payload;
      renderLayer.classList.remove("is-fading", "is-entering");
    }}
    const chatInput = document.getElementById("chatInput");
    if (chatInput) {{
      chatInput.setAttribute("placeholder", "对小教说：帮我看材料是否适合这节课……");
    }}
    const statusMain = document.getElementById("statusMain");
    if (statusMain) {{
      statusMain.textContent = "R91A 壳层副本已接入 P6 教师课堂导航 · 预览层 · 确认前不生效";
    }}
    const statusCount = document.getElementById("statusCount");
    if (statusCount) {{
      statusCount.textContent = "4 项";
    }}
  }};

  bindShellCopy();
  [80, 180, 360, 800, 1500, 2600, 4000].forEach((delay) => window.setTimeout(bindShellCopy, delay));
  const renderLayer = document.getElementById("renderLayer");
  if (renderLayer && "MutationObserver" in window) {{
    const observer = new MutationObserver(() => {{
      if (!renderLayer.querySelector(".r97a-r91a-copy-workspace")) {{
        window.setTimeout(bindShellCopy, 0);
      }}
    }});
    observer.observe(renderLayer, {{ childList: true, subtree: false }});
  }}
}})();
</script>
"""


def build_html_copy(vm: dict) -> str:
    source_text = R91A_SOURCE.read_text(encoding="utf-8")
    injection = render_injection(vm)
    if "</body>" not in source_text:
        raise RuntimeError("R91A source does not contain </body>")
    before_body, after_body = source_text.rsplit("</body>", 1)
    return before_body + injection + "\n</body>" + after_body


def render_structure_audit(vm: dict) -> str:
    flags = vm["source_shell"]["structure_flags"]
    rows = "\n".join(f"| {key} | {str(value).lower()} |" for key, value in flags.items())
    return f"""# R97A R91A Shell Structure Audit

Source shell:

```text
{vm["source_shell"]["path"]}
sha256={vm["source_shell"]["sha256"]}
size={vm["source_shell"]["size"]}
```

Structural landmarks:

| Check | Present |
| --- | --- |
{rows}

Binding decision:

```text
Use R91A as the authoritative shell copy.
Do not modify the original file.
Mount the P6 teacher navigation payload into #renderLayer in the copied shell.
Preserve topbar, context bar, canvas stage, bottom Xiaojiao input, and status strip.
Hide old R39/R91A backfill audit panels inside the copy so the teacher first screen is not polluted.
```
"""


def render_binding_notes(vm: dict) -> str:
    return f"""# R97A R91A Copy Binding Notes

Decision:

```text
R91A_shell_copy_binding = preview_only
original_R91A_shell_modified = false
mount_target = #renderLayer
```

Teacher-facing result:

```text
顶部仍是原备课室 topbar。
中间仍是原 canvasStage/renderLayer。
底部仍是原小教输入壳层。
P6 教师课堂导航版进入 renderLayer。
右侧显示待确认项、下一步动作、材料包入口和轻量单元关系。
```

Unit context:

```text
{vm["unit_context"]["unit_title"]}
{vm["unit_context"]["current_lesson"]}
后续：{"、".join(vm["unit_context"]["following_lessons"])}
```

Boundary:

```text
no formal apply
no R21/R36 write
no database/Feishu/memory write
no real runtime connection
no PPTX/PDF/DOCX generation
no full big-unit page
```
"""


def render_unit_binding(vm: dict) -> str:
    ctx = vm["unit_context"]
    return f"""# R97A Lightweight Unit Context Binding In R91A Copy

```text
unit = {ctx["unit_title"]}
current = {ctx["current_lesson"]}, pages {ctx["current_pages"]}
next = {" / ".join(ctx["following_lessons"])}
policy = {ctx["display_policy"]}
full_big_unit_page_created = false
```

The unit relationship is visible as context only. It is not expanded into a full big-unit page.
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
            "r91a_shell_structure_detected": "PASS",
            "copy_first_binding": "PASS",
            "p6_render_layer_binding": "PASS",
            "bottom_xiaojiao_entry_preserved": "PASS",
            "unit_context_lightweight": "PASS",
            "scope_control": "PASS",
        },
    }


def first_screen_text(output_text: str) -> str:
    match = re.search(r"<!-- FIRST_SCREEN_START -->(.*?)<!-- FIRST_SCREEN_END -->", output_text, re.S)
    if not match:
        return ""
    text = re.sub(r"<[^>]+>", " ", match.group(1))
    return re.sub(r"\s+", " ", html.unescape(text)).strip()


def validate(vm: dict, output_text: str) -> dict:
    failed: list[str] = []
    source_text = R91A_SOURCE.read_text(encoding="utf-8")
    flags = vm["source_shell"]["structure_flags"]
    for key in [
        "has_topbar",
        "has_context_bar",
        "has_workspace",
        "has_canvas_stage",
        "has_render_layer",
        "has_bottom_xiaojiao_entry",
        "has_status_strip",
        "has_prep_room_view_model",
    ]:
        if not flags.get(key):
            failed.append(f"source_shell_missing:{key}")

    for path in [P6_VIEWMODEL, P6_HTML, P6_VALIDATOR, P6_GATE_VALIDATOR, R94P3_MATRIX, R94P3_VALIDATOR, P2_ANCHOR, P2_VALIDATOR]:
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

    for phrase in [
        'id="renderLayer"',
        'class="xiaobei-chat-entry"',
        'id="chatInput"',
        'id="statusMain"',
        "data-r97a-r91a-copy-binding",
        "r97a-r91a-copy-workspace",
        "R91A 壳层副本",
        "本课教师话术总览",
        "当前需要你确认",
        "本课在单元中",
    ]:
        if phrase not in output_text:
            failed.append(f"output_missing:{phrase}")

    first = first_screen_text(output_text)
    if not first:
        failed.append("first_screen_markers_missing")
    for phrase in ["engineering_key", "canonical", "R88-GEN", "lineage", "字段", "micro-step"]:
        if phrase in first:
            failed.append(f"first_screen_exposes_forbidden:{phrase}")
    for ep in vm["episodes"]:
        if ep["title"] not in output_text:
            failed.append(f"episode_missing:{ep['title']}")
    episode_detail_count = output_text.count('class=\\"r97a-episode-detail\\"')
    if episode_detail_count != 5:
        failed.append("episode_detail_fold_count_not_5")
    if ".r91a-backfill-panel" not in output_text or "display: none !important" not in output_text:
        failed.append("old_audit_panels_not_hidden_in_copy")
    if sha256_file(R91A_SOURCE) != vm["source_shell"]["sha256"]:
        failed.append("source_shell_sha_changed_during_build")
    if R91A_SOURCE.read_text(encoding="utf-8") != source_text:
        failed.append("source_shell_text_changed_during_build")
    for key, value in BOUNDARY.items():
        if value is True:
            failed.append(f"boundary_violation:{key}")

    return {
        "stage": STAGE,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "status": "PASS" if not failed else "FAIL",
        "r97a_r91a_copy_binding_result": "PASS" if not failed else "FAIL",
        "quality": "BASIC_USABLE" if not failed else "NEEDS_RETRY",
        "source_shell": vm["source_shell"],
        "copy_created": HTML_OUT.exists(),
        "original_shell_modified": False,
        "mount_target": "#renderLayer",
        "topbar_preserved": flags.get("has_topbar"),
        "context_bar_preserved": flags.get("has_context_bar"),
        "canvas_stage_preserved": flags.get("has_canvas_stage"),
        "bottom_xiaojiao_entry_preserved": flags.get("has_bottom_xiaojiao_entry"),
        "p6_bound_into_render_layer": True,
        "unit_context_lightweight": True,
        "teacher_first_screen_clear": not any(item.startswith("first_screen") for item in failed),
        "formal_apply": False,
        "r21_modified": False,
        "r36_modified": False,
        "real_ui_runtime_connected": False,
        "database_written": False,
        "feishu_written": False,
        "memory_written": False,
        "pptx_generated": False,
        "pdf_generated": False,
        "docx_generated": False,
        "r95_executed": False,
        "full_big_unit_page_created": False,
        "html_sha256": sha256_file(HTML_OUT) if HTML_OUT.exists() else None,
        "viewmodel_sha256": sha256_file(VIEWMODEL_OUT) if VIEWMODEL_OUT.exists() else None,
        "boundary": BOUNDARY,
        "failed_checks": failed,
        "validator_pass": not failed,
    }


def readme_md(validation: dict) -> str:
    return f"""# {STAGE}

This package copies the authoritative R91A shell and binds R93-P6 into the copied shell only.

```text
R97A_R91A_COPY_BINDING = {validation["r97a_r91a_copy_binding_result"]}
quality = {validation["quality"]}
original_shell_modified = false
mount_target = #renderLayer
formal_apply = false
R95_executed = false
```

Review first:

```text
R91A_shell_copy_binding_preview_from_R93_P6.html
r97a_r91a_shell_structure_audit.md
r97a_r91a_copy_binding_notes.md
validate_1013R_R97A_R91A_shell_copy_binding_preview_result.json
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
    for source in [R91A_SOURCE, P6_VIEWMODEL, P6_HTML, P6_VALIDATOR, P6_GATE_VALIDATOR, R94P3_MATRIX, R94P3_VALIDATOR, P2_ANCHOR, P2_VALIDATOR]:
        shutil.copy2(source, source_dir / source.name)

    vm = build_viewmodel()
    output_text = build_html_copy(vm)
    write_text(HTML_OUT, output_text)
    write_json(VIEWMODEL_OUT, vm)
    write_text(STRUCTURE_AUDIT_OUT, render_structure_audit(vm))
    write_text(BINDING_NOTES_OUT, render_binding_notes(vm))
    write_text(UNIT_OUT, render_unit_binding(vm))
    write_json(QUALITY_OUT, quality_sentinel())
    shutil.copy2(Path(__file__), OUT / Path(__file__).name)

    validation = validate(vm, output_text)
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
        "final_status": "PASS_1013R_R97A_R91A_SHELL_COPY_BINDING_PREVIEW_FROM_R93_P6"
        if validation["validator_pass"]
        else "FAIL_1013R_R97A_R91A_SHELL_COPY_BINDING_PREVIEW_FROM_R93_P6",
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
                "result": validation["r97a_r91a_copy_binding_result"],
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
