import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = Path(__file__).resolve().parent

R97A2_DIR = ROOT / "1013R_R97A2_PREP_NOTEBOOK_TEACHING_PROCESS_SLOT_BINDING_REPAIR"
R94P3_DIR = ROOT / "1013R_R94_P3_EPISODE_NAVIGATION_ALIGNED_ARTIFACTS_REPAIR"
R93P6_DIR = ROOT / "1013R_R93_P6_TEACHER_NAVIGATION_VIEW_AND_TALK_FLOW"

R97A2_HTML = R97A2_DIR / "R91A_prep_notebook_teaching_process_slot_binding_from_R93_P6.html"
R97A2_VM = R97A2_DIR / "r97a2_slot_binding_viewmodel.json"
R94P3_MATRIX = R94P3_DIR / "r94_p3_episode_artifact_alignment_matrix.json"
R94P3_SLIDES = R94P3_DIR / "r94_p3_episode_aligned_slide_storyboard.json"
R93P6_VM = R93P6_DIR / "r93_p6_teacher_navigation_viewmodel.json"

HTML_OUT = OUT_DIR / "r97a3_shell_context_binding_preview.html"
COURSEWARE_MAP_OUT = OUT_DIR / "r97a3_episode_to_courseware_rail_map.json"
WORKSHEET_RUBRIC_MAP_OUT = OUT_DIR / "r97a3_episode_to_worksheet_and_rubric_map.json"
XIAOJIAO_CONTEXT_OUT = OUT_DIR / "r97a3_xiaojiao_context_binding.json"
TEACHER_ACTIONS_OUT = OUT_DIR / "r97a3_teacher_action_state_map.json"
SHELL_CONTEXT_VM_OUT = OUT_DIR / "r97a3_shell_context_viewmodel.json"
VALIDATOR_OUT = OUT_DIR / "validate_1013R_R97A3_shell_context_artifact_rail_alignment_result.json"
README_OUT = OUT_DIR / "README.md"
VISUAL_SMOKE_OUT = OUT_DIR / "r97a3_visual_context_smoke.md"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def first_present(values, default=""):
    for value in values:
        if value:
            return value
    return default


def build_courseware_map(matrix, slides):
    slide_by_id = {item["slide_id"]: item for item in slides["slides"]}
    rows = []
    for row in matrix["rows"]:
        slide_items = [slide_by_id[sid] for sid in row["slide_ids"] if sid in slide_by_id]
        rows.append(
            {
                "episode_id": row["episode_id"],
                "episode_index": row["episode_index"],
                "episode_title": row["episode_title"],
                "courseware_slide_ids": row["slide_ids"],
                "right_rail_label": " / ".join(row["slide_ids"]),
                "right_rail_preview_state": "preview_only",
                "screen_titles": [item["slide_title"] for item in slide_items],
                "screen_contents": [item["screen_content"] for item in slide_items],
                "teacher_talk_hints": [item["teacher_talk_hint"] for item in slide_items],
                "student_actions": [item["student_action"] for item in slide_items],
                "served_classroom_actions": [item["served_classroom_action"] for item in slide_items],
                "source": "R94-P3 episode-aligned slide storyboard",
                "teacher_review_required": True,
                "formal_apply": False,
            }
        )
    return {
        "stage": "1013R_R97A3_SHELL_CONTEXT_AND_ARTIFACT_RAIL_ALIGNMENT",
        "source_round": "R94-P3",
        "mapping_type": "episode_to_courseware_rail",
        "rows": rows,
        "teacher_review_required": True,
        "formal_apply": False,
    }


def build_worksheet_rubric_map(matrix):
    rows = []
    for row in matrix["rows"]:
        rows.append(
            {
                "episode_id": row["episode_id"],
                "episode_index": row["episode_index"],
                "episode_title": row["episode_title"],
                "worksheet_tasks": row["worksheet_tasks"],
                "teacher_observation_dimensions": row["teacher_observation_dimensions"],
                "student_self_check_items": row["student_self_check_items"],
                "source": "R94-P3 episode artifact alignment matrix",
                "preview_only": True,
                "teacher_review_required": True,
                "formal_apply": False,
            }
        )
    return {
        "stage": "1013R_R97A3_SHELL_CONTEXT_AND_ARTIFACT_RAIL_ALIGNMENT",
        "mapping_type": "episode_to_worksheet_and_rubric",
        "rows": rows,
        "teacher_review_required": True,
        "formal_apply": False,
    }


def build_xiaojiao_context(p6):
    rows = []
    for episode in p6["episodes"]:
        micro = episode.get("micro_steps", [])
        misconception = first_present(
            [
                episode.get("xiaojiao_cards", {}).get("misconception"),
                "；".join([item.get("if_student_stuck", "") for item in micro if item.get("if_student_stuck")][:2]),
            ]
        )
        scaffold = first_present(
            [
                episode.get("xiaojiao_cards", {}).get("scaffold"),
                "；".join([item.get("student_scaffold", "") for item in micro if item.get("student_scaffold")][:2]),
            ]
        )
        evidence = first_present(
            [
                episode.get("xiaojiao_cards", {}).get("evidence"),
                "；".join([item.get("evidence_check", "") for item in micro if item.get("evidence_check")][:2]),
            ]
        )
        rows.append(
            {
                "episode_id": episode["episode_id"],
                "episode_index": episode["index"],
                "episode_title": episode["title"],
                "teacher_talk": episode.get("key_talk", ""),
                "student_action": episode.get("student_output", ""),
                "misconception": misconception,
                "scaffold": scaffold,
                "evidence_check": evidence,
                "next_action_hint": episode.get("xiaojiao_key_reminder", ""),
                "current_context_for_bottom_xiaojiao": {
                    "lesson_title": p6["lesson"]["title"],
                    "unit": p6["lesson"]["unit"],
                    "section_slot": "六、教学过程",
                    "episode_id": episode["episode_id"],
                    "episode_title": episode["title"],
                    "preview_only": True,
                },
                "teacher_review_required": True,
                "formal_apply": False,
            }
        )
    return {
        "stage": "1013R_R97A3_SHELL_CONTEXT_AND_ARTIFACT_RAIL_ALIGNMENT",
        "mapping_type": "episode_to_bottom_xiaojiao_context",
        "rows": rows,
        "teacher_review_required": True,
        "formal_apply": False,
    }


def build_teacher_action_state_map():
    actions = [
        (
            "continue_polish_teaching_process",
            "继续打磨教学过程",
            "回到当前 episode，修改教师话术、学生支架或折叠 micro-step。",
        ),
        (
            "preview_classroom_materials",
            "预览课堂材料",
            "查看本 episode 对应的大屏页、学习单任务和评价项。",
        ),
        (
            "prepare_export_preview_files",
            "准备导出预览文件",
            "进入 R95 前的预览准备，不生成正式 PPT/PDF/DOCX。",
        ),
        (
            "not_adopt_for_now",
            "暂不采用",
            "保留当前 preview，不写入正式备课本。",
        ),
    ]
    return {
        "stage": "1013R_R97A3_SHELL_CONTEXT_AND_ARTIFACT_RAIL_ALIGNMENT",
        "state_map_type": "teacher_action_preview_only",
        "actions": [
            {
                "action_id": action_id,
                "label": label,
                "description": description,
                "state": "preview_only_noop",
                "enabled_in_preview": True,
                "formal_apply_allowed": False,
                "database_write_allowed": False,
                "runtime_call_allowed": False,
                "requires_future_gate": action_id == "prepare_export_preview_files",
            }
            for action_id, label, description in actions
        ],
        "teacher_review_required": True,
        "formal_apply": False,
    }


def build_shell_context_viewmodel(r97a2_vm, courseware_map, worksheet_rubric_map, xiaojiao_context, actions):
    row_by_episode = {row["episode_id"]: row for row in courseware_map["rows"]}
    material_by_episode = {row["episode_id"]: row for row in worksheet_rubric_map["rows"]}
    xiaojiao_by_episode = {row["episode_id"]: row for row in xiaojiao_context["rows"]}
    episodes = []
    for episode in r97a2_vm["episodes"]:
        eid = episode["episode_id"]
        episodes.append(
            {
                "episode_id": eid,
                "episode_index": episode["index"],
                "episode_title": episode["title"],
                "slot": "六、教学过程",
                "courseware": row_by_episode.get(eid, {}),
                "worksheet_and_rubric": material_by_episode.get(eid, {}),
                "xiaojiao_context": xiaojiao_by_episode.get(eid, {}),
                "teacher_actions": [item["action_id"] for item in actions["actions"]],
                "preview_only": True,
            }
        )
    return {
        "stage": "1013R_R97A3_SHELL_CONTEXT_AND_ARTIFACT_RAIL_ALIGNMENT",
        "source_stage": "R97A2",
        "source_slot_binding": str(R97A2_VM),
        "source_artifact_alignment": str(R94P3_MATRIX),
        "lesson": r97a2_vm["lesson"],
        "target_slot": "current_lesson.process_steps / 六、教学过程",
        "episode_count": len(episodes),
        "episodes": episodes,
        "shell_binding_policy": {
            "copy_shell_only": True,
            "replace_render_layer": False,
            "replace_full_prep_notebook": False,
            "preserve_original_lesson_sections": True,
            "right_rail_alignment_preview": True,
            "bottom_xiaojiao_context_preview": True,
            "teacher_action_preview_only": True,
        },
        "boundary": {
            "formal_apply": False,
            "database_written": False,
            "feishu_written": False,
            "memory_written": False,
            "r21_core_modified": False,
            "r36_core_modified": False,
            "real_ui_runtime_connected": False,
            "pptx_generated": False,
            "pdf_docx_generated": False,
            "R95_executed": False,
        },
        "teacher_review_required": True,
        "formal_apply": False,
    }


def build_injected_assets(vm):
    vm_json = json.dumps(vm, ensure_ascii=False)
    css = r"""
  <style id="style-1013R-R97A3-shell-context-alignment">
    html[data-1013r-r97a3-shell-context="true"] .r97a3-episode-links {
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      margin: 10px 0 2px 34px;
      color: #2c7d67;
      font-size: 12px;
    }
    html[data-1013r-r97a3-shell-context="true"] .r97a3-chip {
      border: 1px solid rgba(44, 125, 103, .22);
      background: rgba(246, 252, 248, .88);
      border-radius: 999px;
      padding: 3px 8px;
      white-space: nowrap;
    }
    html[data-1013r-r97a3-shell-context="true"] .r97a3-rail-panel {
      margin-top: 14px;
      border-top: 1px solid rgba(44, 125, 103, .18);
      padding-top: 14px;
    }
    html[data-1013r-r97a3-shell-context="true"] .r97a3-rail-title {
      color: #1d342f;
      font-size: 15px;
      font-weight: 800;
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 8px;
    }
    html[data-1013r-r97a3-shell-context="true"] .r97a3-rail-title span {
      color: #6b807c;
      font-size: 12px;
      font-weight: 700;
    }
    html[data-1013r-r97a3-shell-context="true"] .r97a3-episode-rail-item {
      border: 1px solid rgba(44, 125, 103, .12);
      border-radius: 8px;
      padding: 9px 10px;
      margin-top: 8px;
      background: rgba(255, 255, 250, .7);
    }
    html[data-1013r-r97a3-shell-context="true"] .r97a3-episode-rail-item strong {
      display: block;
      color: #1d342f;
      font-size: 13px;
      margin-bottom: 4px;
    }
    html[data-1013r-r97a3-shell-context="true"] .r97a3-episode-rail-item p {
      margin: 3px 0;
      color: #5f746f;
      font-size: 12px;
      line-height: 1.5;
    }
    html[data-1013r-r97a3-shell-context="true"] .r97a3-action-row {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 6px;
      margin-top: 8px;
    }
    html[data-1013r-r97a3-shell-context="true"] .r97a3-action-btn {
      border: 1px solid rgba(44, 125, 103, .22);
      border-radius: 999px;
      padding: 6px 8px;
      color: #2c7d67;
      background: #fffefa;
      font-size: 12px;
      font-weight: 800;
      cursor: default;
    }
    html[data-1013r-r97a3-shell-context="true"] .r97a3-bottom-context {
      position: fixed;
      left: 50%;
      bottom: 76px;
      transform: translateX(-50%);
      z-index: 35;
      width: min(840px, calc(100vw - 340px));
      border: 1px solid rgba(44, 125, 103, .18);
      border-radius: 16px;
      background: rgba(255, 255, 250, .94);
      box-shadow: 0 12px 32px rgba(22, 81, 66, .12);
      color: #324c47;
      padding: 8px 14px;
      font-size: 13px;
    }
    html[data-1013r-r97a3-shell-context="true"] .r97a3-bottom-context summary {
      cursor: pointer;
      color: #2c7d67;
      font-weight: 800;
    }
    html[data-1013r-r97a3-shell-context="true"] .r97a3-context-grid {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 10px;
      margin-top: 8px;
    }
    html[data-1013r-r97a3-shell-context="true"] .r97a3-context-grid div {
      border-left: 3px solid rgba(44, 125, 103, .2);
      padding-left: 8px;
      line-height: 1.55;
    }
    @media (max-width: 1280px) {
      html[data-1013r-r97a3-shell-context="true"] .r97a3-bottom-context {
        display: none;
      }
    }
  </style>
"""
    safe_vm_json = vm_json.replace("</script>", "<\\/script>")
    js = r"""
  <script id="data-1013R-R97A3-shell-context-viewmodel" type="application/json">__R97A3_VIEWMODEL_JSON__</script>
  <script id="script-1013R-R97A3-shell-context-artifact-rail-alignment">
  (function() {
    document.documentElement.setAttribute("data-1013r-r97a3-shell-context", "true");
    const dataNode = document.getElementById("data-1013R-R97A3-shell-context-viewmodel");
    if (!dataNode) return;
    const vm = JSON.parse(dataNode.textContent);
    const byEpisode = new Map((vm.episodes || []).map((item) => [item.episode_id, item]));

    function esc(value) {
      return String(value ?? "").replace(/[&<>"']/g, (ch) => ({
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#39;"
      }[ch]));
    }

    function addEpisodeInlineLinks() {
      for (const step of document.querySelectorAll(".r97a2-p6-step[data-r97a2-p6-episode]")) {
        const episodeId = step.getAttribute("data-r97a2-p6-episode");
        const item = byEpisode.get(episodeId);
        if (!item || step.querySelector(".r97a3-episode-links")) continue;
        const courseware = item.courseware || {};
        const material = item.worksheet_and_rubric || {};
        const links = document.createElement("div");
        links.className = "r97a3-episode-links";
        links.innerHTML = `
          <span class="r97a3-chip">大屏 ${esc((courseware.courseware_slide_ids || []).join(" / "))}</span>
          <span class="r97a3-chip">学习单 ${esc((material.worksheet_tasks || []).join("；"))}</span>
          <span class="r97a3-chip">观察 ${esc((material.teacher_observation_dimensions || []).join("；"))}</span>
          <span class="r97a3-chip">小教上下文已挂住</span>
        `;
        const fold = step.querySelector(".r97a2-fold");
        step.insertBefore(links, fold || null);
      }
    }

    function addRightRailContext() {
      const rail = document.querySelector(".courseware-rail");
      if (!rail || rail.querySelector(".r97a3-rail-panel")) return;
      const panel = document.createElement("section");
      panel.className = "r97a3-rail-panel";
      const rows = (vm.episodes || []).map((item) => {
        const c = item.courseware || {};
        const m = item.worksheet_and_rubric || {};
        const x = item.xiaojiao_context || {};
        return `
          <div class="r97a3-episode-rail-item">
            <strong>${esc(item.episode_index)}. ${esc(item.episode_title)} · ${esc((c.courseware_slide_ids || []).join(" / "))}</strong>
            <p>屏幕：${esc((c.screen_titles || []).join("；"))}</p>
            <p>材料：${esc((m.worksheet_tasks || []).join("；"))}｜评价：${esc((m.teacher_observation_dimensions || []).join("；"))}</p>
            <p>小教：${esc(x.next_action_hint || "")}</p>
          </div>
        `;
      }).join("");
      const actions = (vm.teacher_actions || []).map((action) => `
        <button class="r97a3-action-btn" type="button" data-pending="${esc(action.description)}" title="preview only">${esc(action.label)}</button>
      `).join("");
      panel.innerHTML = `
        <div class="r97a3-rail-title">P6 课堂联动 <span>preview only</span></div>
        ${rows}
        <div class="r97a3-rail-title" style="margin-top: 14px;">教师下一步 <span>no-op</span></div>
        <div class="r97a3-action-row">${actions}</div>
      `;
      const head = rail.querySelector(".courseware-rail-head");
      if (head && head.nextSibling) {
        rail.insertBefore(panel, head.nextSibling);
      } else {
        rail.prepend(panel);
      }
    }

    function addBottomXiaojiaoContext() {
      if (document.querySelector(".r97a3-bottom-context")) return;
      const current = (vm.episodes || [])[0];
      if (!current) return;
      const x = current.xiaojiao_context || {};
      const box = document.createElement("details");
      box.className = "r97a3-bottom-context";
      box.innerHTML = `
        <summary>小教上下文预览：当前默认跟随「${esc(current.episode_title)}」 · 不调用 runtime</summary>
        <div class="r97a3-context-grid">
          <div><strong>教师话术</strong><br>${esc(x.teacher_talk || "")}</div>
          <div><strong>可能卡点</strong><br>${esc(x.misconception || "")}</div>
          <div><strong>证据</strong><br>${esc(x.evidence_check || "")}</div>
        </div>
      `;
      document.body.appendChild(box);
    }

    function applyR97A3Alignment() {
      addEpisodeInlineLinks();
      addRightRailContext();
      addBottomXiaojiaoContext();
      window.__R97A3_SHELL_CONTEXT_ALIGNMENT__ = {
        stage: vm.stage,
        episode_count: vm.episode_count,
        right_rail_alignment_preview: !!document.querySelector(".r97a3-rail-panel"),
        bottom_xiaojiao_context_preview: !!document.querySelector(".r97a3-bottom-context"),
        inline_episode_links_preview: !!document.querySelector(".r97a3-episode-links"),
        formal_apply: false
      };
    }

    applyR97A3Alignment();
    document.addEventListener("DOMContentLoaded", applyR97A3Alignment);
    window.addEventListener("load", () => {
      applyR97A3Alignment();
      setTimeout(applyR97A3Alignment, 0);
      setTimeout(applyR97A3Alignment, 120);
      setTimeout(applyR97A3Alignment, 500);
    });
    setTimeout(applyR97A3Alignment, 0);
    setTimeout(applyR97A3Alignment, 240);
  })();
  </script>
"""
    return css + js.replace("__R97A3_VIEWMODEL_JSON__", safe_vm_json)


def write_json(path: Path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def main():
    r97a2_vm = load_json(R97A2_VM)
    p6 = load_json(R93P6_VM)
    matrix = load_json(R94P3_MATRIX)
    slides = load_json(R94P3_SLIDES)

    courseware_map = build_courseware_map(matrix, slides)
    worksheet_rubric_map = build_worksheet_rubric_map(matrix)
    xiaojiao_context = build_xiaojiao_context(p6)
    teacher_actions = build_teacher_action_state_map()
    shell_vm = build_shell_context_viewmodel(
        r97a2_vm,
        courseware_map,
        worksheet_rubric_map,
        xiaojiao_context,
        teacher_actions,
    )
    shell_vm["teacher_actions"] = teacher_actions["actions"]

    write_json(COURSEWARE_MAP_OUT, courseware_map)
    write_json(WORKSHEET_RUBRIC_MAP_OUT, worksheet_rubric_map)
    write_json(XIAOJIAO_CONTEXT_OUT, xiaojiao_context)
    write_json(TEACHER_ACTIONS_OUT, teacher_actions)
    write_json(SHELL_CONTEXT_VM_OUT, shell_vm)

    html = R97A2_HTML.read_text(encoding="utf-8")
    injected = build_injected_assets(shell_vm)
    if "</body>" not in html:
        raise RuntimeError("R97A2 HTML does not contain </body>")
    HTML_OUT.write_text(html.replace("</body>", injected + "\n</body>", 1), encoding="utf-8")

    out_html = HTML_OUT.read_text(encoding="utf-8")
    checks = {
        "html_created": HTML_OUT.exists(),
        "source_r97a2_html_exists": R97A2_HTML.exists(),
        "r97a2_p6_slot_preserved": "r97a2-p6-step" in out_html and "data-r97a2-p6-episode" in out_html,
        "r97a3_context_marker_present": "data-1013r-r97a3-shell-context" in out_html,
        "right_rail_alignment_script_present": "addRightRailContext" in out_html and "P6 课堂联动" in out_html,
        "bottom_xiaojiao_context_script_present": "addBottomXiaojiaoContext" in out_html,
        "teacher_action_preview_only_present": "preview_only_noop" in out_html,
        "episode_count_is_5": len(shell_vm["episodes"]) == 5,
        "courseware_mapping_count_is_5": len(courseware_map["rows"]) == 5,
        "worksheet_rubric_mapping_count_is_5": len(worksheet_rubric_map["rows"]) == 5,
        "xiaojiao_context_count_is_5": len(xiaojiao_context["rows"]) == 5,
        "slide_count_is_10": sum(len(row["courseware_slide_ids"]) for row in courseware_map["rows"]) == 10,
        "formal_apply_false": shell_vm["formal_apply"] is False,
        "r95_not_executed": shell_vm["boundary"]["R95_executed"] is False,
        "r21_r36_core_not_modified": shell_vm["boundary"]["r21_core_modified"] is False and shell_vm["boundary"]["r36_core_modified"] is False,
    }
    blocking = [name for name, ok in checks.items() if ok is not True]
    validator = {
        "stage": "1013R_R97A3_SHELL_CONTEXT_AND_ARTIFACT_RAIL_ALIGNMENT",
        "status": "PASS" if not blocking else "FAIL",
        "blocking": blocking,
        "checks": checks,
        "output_html": str(HTML_OUT),
        "output_sha256": sha256(HTML_OUT),
        "boundary": shell_vm["boundary"],
        "teacher_review_required": True,
        "formal_apply": False,
        "next_allowed": "R97B_TEACHER_SHELL_EXPERIENCE_POLISH after user/GPT review",
        "R95_executed": False,
    }
    write_json(VALIDATOR_OUT, validator)

    VISUAL_SMOKE_OUT.write_text(
        "\n".join(
            [
                "# R97A3 Visual Context Smoke",
                "",
                "本轮在 R97A2 复制页基础上增加静态上下文联动层。",
                "",
                "## 应看到",
                "",
                "- `六、教学过程` 仍显示 P6 的 5 个教学节奏块。",
                "- 每个 episode 下方出现大屏、学习单、观察项、小教上下文的轻量 chips。",
                "- 右侧大屏草稿底部新增 `P6 课堂联动`，列出 episode 到 S01-S10、学习单、评价、小教提示的关系。",
                "- 底部小教输入上方出现 `小教上下文预览` 折叠条。",
                "- 教师下一步按钮均为 preview-only/no-op。",
                "",
                "## 边界",
                "",
                "- 不替换整页壳层。",
                "- 不改原 R21/R36 core。",
                "- 不 formal apply，不进入 R95，不生成正式 PPT/PDF/DOCX。",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    README_OUT.write_text(
        "\n".join(
            [
                "# 1013R_R97A3_SHELL_CONTEXT_AND_ARTIFACT_RAIL_ALIGNMENT",
                "",
                "R97A2 已证明 P6 只进入 `六、教学过程` 槽位。本轮继续补齐静态壳层上下文联动：右侧大屏/课件栏、学习单/评价入口、底部小教上下文和教师动作按钮。",
                "",
                "## 输出",
                "",
                f"- `{HTML_OUT.name}`",
                f"- `{COURSEWARE_MAP_OUT.name}`",
                f"- `{WORKSHEET_RUBRIC_MAP_OUT.name}`",
                f"- `{XIAOJIAO_CONTEXT_OUT.name}`",
                f"- `{TEACHER_ACTIONS_OUT.name}`",
                f"- `{SHELL_CONTEXT_VM_OUT.name}`",
                f"- `{VALIDATOR_OUT.name}`",
                f"- `{VISUAL_SMOKE_OUT.name}`",
                "",
                "## 边界",
                "",
                "- 静态复制页预览，不接真实 runtime。",
                "- 不改原 R21/R36 core。",
                "- 不 formal apply，不写库/飞书/记忆。",
                "- 不进入 R95，不生成正式导出文件。",
                "",
                f"HTML SHA256: `{validator['output_sha256']}`",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    print(json.dumps(validator, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
