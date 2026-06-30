from __future__ import annotations

import hashlib
import html
import json
import re
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
STAGE = "1013R_R93_P6_TEACHER_NAVIGATION_VIEW_AND_TALK_FLOW"
OUT = BASE / STAGE

P5_DIR = BASE / "1013R_R93_P5_TEACHER_EXECUTION_MAP_AND_CHILD_LANGUAGE_REPAIR"
P5_MAP = P5_DIR / "r93_p5_teacher_execution_map.json"
P5_TALK_BANK = P5_DIR / "r93_p5_child_language_teacher_talk_bank.md"
P5_XIAOJIAO = P5_DIR / "r93_p5_xiaojiao_in_class_support_cards.md"
P5_VALIDATOR = P5_DIR / "validate_1013R_R93_P5_teacher_execution_map_child_language_result.json"

HTML_OUT = OUT / "r93_p6_teacher_navigation_view.html"
VIEWMODEL_OUT = OUT / "r93_p6_teacher_navigation_viewmodel.json"
TALK_FLOW_OUT = OUT / "r93_p6_talk_flow_summary.md"
NOTES_OUT = OUT / "r93_p6_reading_experience_notes.md"
VALIDATOR_OUT = OUT / "validate_1013R_R93_P6_teacher_navigation_view_result.json"

BOUNDARY = {
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
    "pdf_generated": False,
    "docx_generated": False,
    "r95_executed": False,
}

DURATIONS = {
    "看见渐变": "约5分钟",
    "分清亮暗与鲜灰": "约7分钟",
    "三格试色": "约8分钟",
    "放进作品": "约14分钟",
    "自查与微修订": "约6分钟",
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


def first_sentence(text: str) -> str:
    parts = re.split(r"[。；;]", text)
    return (parts[0] + "。") if parts and parts[0] else text


def summarize_three_steps(micro_steps: list[dict]) -> list[str]:
    if len(micro_steps) <= 3:
        return [step["step_name"] for step in micro_steps]
    if len(micro_steps) <= 5:
        return [
            "先" + micro_steps[0]["step_name"],
            "再" + "、".join(step["step_name"] for step in micro_steps[1:-1]),
            "最后" + micro_steps[-1]["step_name"],
        ]
    middle = micro_steps[len(micro_steps) // 2]
    return [
        "先" + micro_steps[0]["step_name"],
        "再" + middle["step_name"],
        "最后" + micro_steps[-1]["step_name"],
    ]


def student_output(ep: dict) -> str:
    title = ep["title"]
    outputs = {
        "看见渐变": "能指出颜色变化方向，并用“从___到___”说一句。",
        "分清亮暗与鲜灰": "能把色条分到亮暗或鲜灰，并说出理由。",
        "三格试色": "完成一组三格渐变小样，并能说明变化方向。",
        "放进作品": "把渐变放进色条、图形或小作品，别人能看出方向。",
        "自查与微修订": "完成一处微修订，并说清自己改了哪里。",
    }
    return outputs.get(title, ep["micro_steps"][-1]["evidence_check"])


def key_talks(ep: dict) -> list[str]:
    title = ep["title"]
    preferred = {
        "看见渐变": [0, 1],
        "分清亮暗与鲜灰": [0, 4],
        "三格试色": [2, 5],
        "放进作品": [0, 3],
        "自查与微修订": [0, 2],
    }
    indexes = preferred.get(title, [0, min(1, len(ep["micro_steps"]) - 1)])
    return [ep["micro_steps"][idx]["teacher_say"] for idx in indexes if idx < len(ep["micro_steps"])]


def build_viewmodel() -> dict:
    source = read_json(P5_MAP)
    p5_validator = read_json(P5_VALIDATOR)
    episodes = []
    for index, ep in enumerate(source["episodes"], start=1):
        talks = key_talks(ep)
        episodes.append(
            {
                "index": index,
                "episode_id": ep["episode_id"],
                "title": ep["title"],
                "episode_type": ep["episode_type"],
                "duration": DURATIONS.get(ep["title"], ""),
                "goal": ep["language_layers"]["lesson_plan_expression"],
                "teacher_three_steps": summarize_three_steps(ep["micro_steps"]),
                "student_output": student_output(ep),
                "key_talk": talks[0],
                "talk_flow": talks,
                "xiaojiao_key_reminder": ep["xiaojiao_cards"]["reminder"],
                "micro_steps": ep["micro_steps"],
                "language_layers": ep["language_layers"],
                "xiaojiao_cards": ep["xiaojiao_cards"],
            }
        )
    return {
        "stage": STAGE,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "lesson": {
            "title": "色彩的渐变",
            "unit": "第二单元《多彩的世界》",
            "grade": "三年级",
            "status": "教师审核草案",
            "quality": "BASIC_USABLE",
            "formal_apply": False,
        },
        "source": {
            "from": rel(P5_MAP),
            "p5_validator_pass": p5_validator.get("validator_pass"),
            "micro_step_count": sum(len(ep["micro_steps"]) for ep in episodes),
        },
        "reading_model": {
            "default_layer": "5 teaching rhythm blocks",
            "folded_layer": "29 micro-steps plus screen/scaffold/xiaojiao/evidence",
            "teacher_priority": True,
            "student_secondary": True,
            "xiaojiao_low_presence": True,
        },
        "episodes": episodes,
        "boundary": BOUNDARY,
    }


def render_talk_flow(vm: dict) -> str:
    parts = [
        "# R93-P6 本课教师话术总览",
        "",
        "这些话术来自 R93-P5 execution map，本轮只做阅读重组，不新增正式材料。",
    ]
    for ep in vm["episodes"]:
        parts.extend(["", f"## {ep['index']}. {ep['title']}"])
        for talk in ep["talk_flow"]:
            parts.append(f"- {talk}")
    return "\n".join(parts) + "\n"


def render_notes() -> str:
    return """# R93-P6 Reading Experience Notes

## Decision

R93-P5 is retained as the detailed execution-map database. R93-P6 is the teacher default navigation view.

## Reading Rules

- Default view shows five teaching rhythm blocks, not 29 micro-steps.
- Each block shows the goal, teacher three-step route, student output, key talk, and one Xiaojiao reminder.
- Micro-steps, screen/material state, scaffolds, more Xiaojiao suggestions, misconceptions, evidence, and design intent remain folded.
- Teacher action and teacher talk are prioritized; student action is secondary.
- Next-step triggers are kept inside micro-step details and visually weakened.

## Boundary

- No provider/model call
- No R21/R36 change
- No UI binding
- No formal apply
- No database/Feishu/memory write
- No PPTX/PDF/DOCX generation
- No R95 execution
"""


def render_html(vm: dict) -> str:
    nav = "".join(
        f"<a href=\"#{esc(ep['episode_id'])}\">{ep['index']}. {esc(ep['title'])}</a>"
        for ep in vm["episodes"]
    )
    talk_items = "".join(
        f"""
        <article>
          <b>{ep['index']}. {esc(ep['title'])}</b>
          <p>{esc(ep['key_talk'])}</p>
        </article>
        """
        for ep in vm["episodes"]
    )
    episode_sections = []
    for ep in vm["episodes"]:
        micro_rows = "".join(
            f"""
            <section class="micro-row">
              <h4>{ep['index']}.{step['step_order']} {esc(step['step_name'])}</h4>
              <p><b>教师：</b>{esc(step['teacher_action'])}</p>
              <p><b>话术：</b>{esc(step['teacher_say'])}</p>
              <p><b>学生：</b>{esc(step['student_action'])}</p>
              <details>
                <summary>大屏 / 支架 / 小教 / 证据</summary>
                <p><b>大屏：</b>{esc(step['screen_state'])}</p>
                <p><b>支架：</b>{esc(step['student_scaffold'])}</p>
                <p><b>小教：</b>{esc(step['xiaojiao_support'])}</p>
                <p><b>证据：</b>{esc(step['evidence_check'])}</p>
                <p><b>卡住时：</b>{esc(step['if_student_stuck'])}</p>
                <p><b>进入下一步：</b>{esc(step['next_step_trigger'])}</p>
              </details>
            </section>
            """
            for step in ep["micro_steps"]
        )
        episode_sections.append(
            f"""
            <section class="episode-block" id="{esc(ep['episode_id'])}">
              <p class="episode-kicker">{esc(ep['episode_type'])} · {esc(ep['duration'])}</p>
              <h2>{ep['index']}. {esc(ep['title'])}</h2>
              <p class="goal"><b>本环节目标：</b>{esc(ep['goal'])}</p>
              <div class="default-grid">
                <section>
                  <h3>老师三步</h3>
                  <ol>{''.join(f'<li>{esc(item)}</li>' for item in ep['teacher_three_steps'])}</ol>
                </section>
                <section>
                  <h3>学生产出</h3>
                  <p>{esc(ep['student_output'])}</p>
                </section>
                <section>
                  <h3>关键话术</h3>
                  <blockquote>{esc(ep['key_talk'])}</blockquote>
                </section>
                <section>
                  <h3>小教提醒</h3>
                  <p>{esc(ep['xiaojiao_key_reminder'])}</p>
                </section>
              </div>
              <details class="episode-detail">
                <summary>展开本环节 micro-step、支架、证据和更多小教建议</summary>
                <div class="micro-list">{micro_rows}</div>
                <div class="more-support">
                  <h3>语言三层</h3>
                  <p><b>学生话：</b>{esc(' / '.join(ep['language_layers']['student_friendly']))}</p>
                  <p><b>教师补专业词：</b>{esc(ep['language_layers']['teacher_professional_bridge'])}</p>
                  <p><b>教案表达：</b>{esc(ep['language_layers']['lesson_plan_expression'])}</p>
                  <h3>更多小教建议</h3>
                  <ul>{ul(list(ep['xiaojiao_cards'].values()))}</ul>
                </div>
              </details>
            </section>
            """
        )
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>《色彩的渐变》教师课堂导航版</title>
  <style>
    :root {{
      --ink: #263238;
      --muted: #64727b;
      --line: #d9e2df;
      --paper: #fbfcfa;
      --green: #3f705e;
      --mint: #e5f2ed;
      --sun: #f5e7b8;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      background: var(--paper);
      color: var(--ink);
      font-family: "Microsoft YaHei", "PingFang SC", Arial, sans-serif;
      line-height: 1.64;
    }}
    header {{
      background: #fff;
      border-bottom: 1px solid var(--line);
      padding: 24px 28px 16px;
      position: sticky;
      top: 0;
      z-index: 3;
    }}
    .inner, main {{ max-width: 1040px; margin: 0 auto; }}
    h1 {{ margin: 0; font-size: clamp(30px, 5vw, 56px); line-height: 1.08; letter-spacing: 0; }}
    .subtitle {{ margin: 10px 0 0; color: var(--muted); }}
    nav {{ display: flex; flex-wrap: wrap; gap: 10px; margin-top: 14px; }}
    nav a {{ color: var(--green); text-decoration: none; font-weight: 700; border-bottom: 2px solid #bdd8ce; }}
    main {{ padding: 26px 28px 80px; }}
    .talk-overview {{
      border-top: 2px solid var(--ink);
      border-bottom: 1px solid var(--line);
      padding: 20px 0;
      margin-bottom: 26px;
    }}
    .talk-overview h2 {{ margin: 0 0 12px; }}
    .talk-grid {{
      display: grid;
      grid-template-columns: repeat(5, minmax(0, 1fr));
      gap: 12px;
    }}
    .talk-grid article {{
      border-left: 3px solid var(--line);
      padding-left: 10px;
    }}
    .talk-grid p {{ color: var(--muted); margin: 6px 0 0; }}
    .episode-block {{
      border-top: 1px solid var(--line);
      padding: 34px 0;
    }}
    .episode-kicker {{ margin: 0 0 5px; color: var(--green); font-weight: 700; }}
    .episode-block h2 {{ margin: 0; font-size: 31px; }}
    .goal {{ color: var(--muted); margin: 10px 0 18px; }}
    .default-grid {{
      display: grid;
      grid-template-columns: 1.15fr .85fr;
      gap: 18px 24px;
    }}
    .default-grid section {{
      border-left: 3px solid var(--line);
      padding-left: 12px;
    }}
    .default-grid h3 {{ margin: 0 0 8px; font-size: 18px; }}
    .default-grid p, .default-grid li {{ color: var(--muted); }}
    blockquote {{
      margin: 8px 0;
      padding: 10px 12px;
      border-left: 4px solid var(--green);
      background: #fffdf4;
    }}
    .episode-detail {{
      margin-top: 18px;
      border-top: 1px dashed #c8d6d0;
      padding-top: 10px;
    }}
    summary {{ cursor: pointer; color: var(--green); font-weight: 700; }}
    .micro-row {{
      border-left: 2px solid var(--line);
      margin: 12px 0;
      padding: 8px 0 8px 12px;
    }}
    .micro-row h4 {{ margin: 0 0 5px; }}
    .micro-row p {{ margin: 4px 0; color: var(--muted); }}
    .micro-row details {{ margin-top: 6px; }}
    .more-support {{
      margin-top: 18px;
      padding-top: 12px;
      border-top: 1px solid var(--line);
    }}
    @media (max-width: 900px) {{
      .talk-grid, .default-grid {{ grid-template-columns: 1fr; }}
    }}
    @media (max-width: 620px) {{
      header, main {{ padding-left: 16px; padding-right: 16px; }}
    }}
  </style>
</head>
<body>
  <header>
    <div class="inner">
      <h1>《色彩的渐变》教师课堂导航版</h1>
      <p class="subtitle">默认看 5 个教学节奏块；micro-step、支架、小教和证据折叠保留。</p>
      <nav>{nav}</nav>
    </div>
  </header>
  <main>
    <!-- FIRST_SCREEN_START -->
    <section class="talk-overview">
      <h2>0.1 本课教师话术总览</h2>
      <div class="talk-grid">{talk_items}</div>
    </section>
    <!-- FIRST_SCREEN_END -->
    {''.join(episode_sections)}
  </main>
</body>
</html>
"""


def render_validator(vm: dict, html_text: str) -> dict:
    errors: list[str] = []
    p5_validator = read_json(P5_VALIDATOR)
    first_screen = re.search(r"<!-- FIRST_SCREEN_START -->(.*?)<!-- FIRST_SCREEN_END -->", html_text, re.S)
    first_text = re.sub(r"<[^>]+>", " ", first_screen.group(1)) if first_screen else ""
    first_text = re.sub(r"\s+", " ", html.unescape(first_text))
    if not first_screen:
        errors.append("first_screen_markers_missing")
    for ep in vm["episodes"]:
        if ep["title"] not in first_text:
            errors.append("first_screen_missing_episode:" + ep["title"])
        if len(ep["teacher_three_steps"]) != 3:
            errors.append("teacher_three_steps_not_3:" + ep["title"])
        if not ep["key_talk"]:
            errors.append("missing_key_talk:" + ep["title"])
    forbidden_first = ["1.1", "2.1", "3.1", "4.1", "5.1", "micro-step", "micro-row"]
    hits = [item for item in forbidden_first if item in first_text]
    if hits:
        errors.append("first_screen_exposes_micro_steps:" + ",".join(hits))
    if html_text.count("<details class=\"episode-detail\">") != 5:
        errors.append("episode_details_not_5")
    if html_text.count("class=\"micro-row\"") < 29:
        errors.append("folded_micro_steps_missing")
    for phrase in ["本课教师话术总览", "老师三步", "学生产出", "关键话术", "小教提醒"]:
        if phrase not in html_text:
            errors.append("missing_teacher_navigation_phrase:" + phrase)
    if not p5_validator.get("validator_pass"):
        errors.append("p5_validator_not_pass")
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
            "pdf_generated",
            "docx_generated",
            "r95_executed",
        ]
    ):
        errors.append("boundary_violation")
    return {
        "stage": STAGE,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "status": "PASS" if not errors else "FAIL",
        "teacher_navigation_view_created": HTML_OUT.exists(),
        "viewmodel_created": VIEWMODEL_OUT.exists(),
        "talk_flow_summary_created": TALK_FLOW_OUT.exists(),
        "reading_experience_notes_created": NOTES_OUT.exists(),
        "episode_count": len(vm["episodes"]),
        "default_view_episode_blocks": 5,
        "micro_steps_folded": True,
        "first_screen_exposes_micro_steps": bool(hits),
        "p5_validator_pass": p5_validator.get("validator_pass"),
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
    write_text(TALK_FLOW_OUT, render_talk_flow(vm))
    write_text(NOTES_OUT, render_notes())
    validation = render_validator(vm, html_text)
    write_json(VALIDATOR_OUT, validation)
    print(json.dumps({
        "stage": STAGE,
        "validator_pass": validation["validator_pass"],
        "html": str(HTML_OUT),
        "html_sha256": validation["html_sha256"],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
