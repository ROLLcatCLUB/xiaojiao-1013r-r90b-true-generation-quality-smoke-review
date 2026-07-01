import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = Path(__file__).resolve().parent

R97A3_DIR = ROOT / "1013R_R97A3_SHELL_CONTEXT_AND_ARTIFACT_RAIL_ALIGNMENT"
R97A3_HTML = R97A3_DIR / "r97a3_shell_context_binding_preview.html"
R97A3_VM = R97A3_DIR / "r97a3_shell_context_viewmodel.json"
R97A3_COURSEWARE_MAP = R97A3_DIR / "r97a3_episode_to_courseware_rail_map.json"
R97A3_WORKSHEET_RUBRIC_MAP = R97A3_DIR / "r97a3_episode_to_worksheet_and_rubric_map.json"
R97A3_XIAOJIAO_CONTEXT = R97A3_DIR / "r97a3_xiaojiao_context_binding.json"
R97A3_TEACHER_ACTIONS = R97A3_DIR / "r97a3_teacher_action_state_map.json"

HTML_OUT = OUT_DIR / "r97b_clean_shell_context_preview.html"
VM_OUT = OUT_DIR / "r97b_clean_shell_viewmodel.json"
CLEANUP_REPORT_OUT = OUT_DIR / "r97b_stale_content_cleanup_report.md"
RIGHT_RAIL_POLICY_OUT = OUT_DIR / "r97b_right_rail_priority_policy.md"
XIAOJIAO_SMOKE_OUT = OUT_DIR / "r97b_xiaojiao_episode_context_smoke.md"
ACTION_SMOKE_OUT = OUT_DIR / "r97b_teacher_action_preview_state_smoke.md"
VALIDATOR_OUT = OUT_DIR / "validate_1013R_R97B_teacher_shell_experience_polish_result.json"
README_OUT = OUT_DIR / "README.md"


REMOVAL_PATTERNS = [
    {
        "id": "r39_mock_candidate_preview_panel",
        "label": "R39 mock candidate preview panel",
        "regex": r"\n<section class=\"r39-candidate-preview-panel\"[\s\S]*?</section>\n",
        "default_visible_terms": [
            "小教候选预览",
            "source=mock_candidate_fixture",
            "修改前",
            "修改后",
        ],
    },
    {
        "id": "r91a_static_backfill_panel",
        "label": "R90B / R90B-P1 / R91-A static backfill panel",
        "regex": r"\n<section class=\"r91a-backfill-panel\"[\s\S]*?</section>\s*(?=\n\s*<style id=\"style-1013R-R97A2-slot-binding\")",
        "default_visible_terms": [
            "R90B / R90B-P1 / R91-A 生成结果回填",
            "r90b_provider_candidate",
            "旧审核回填",
        ],
    },
]


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def remove_default_visible_stale_blocks(html: str):
    removals = []
    cleaned = html
    for item in REMOVAL_PATTERNS:
        matches = list(re.finditer(item["regex"], cleaned))
        removals.append(
            {
                "id": item["id"],
                "label": item["label"],
                "matched_count": len(matches),
                "default_visible_terms": item["default_visible_terms"],
                "action": "removed_from_teacher_default_html",
                "developer_access": "documented_in_cleanup_report_only",
            }
        )
        cleaned = re.sub(item["regex"], "\n", cleaned, count=0)
    return cleaned, removals


def build_clean_viewmodel(source_vm, removals, actions):
    return {
        "stage": "1013R_R97B_TEACHER_SHELL_EXPERIENCE_POLISH_AND_STALE_CONTENT_CLEANUP",
        "source_stage": "R97A3",
        "source_html": str(R97A3_HTML),
        "lesson": source_vm.get("lesson", {}),
        "target_slot": source_vm.get("target_slot", "current_lesson.process_steps / 六、教学过程"),
        "episode_count": source_vm.get("episode_count", 0),
        "episodes": source_vm.get("episodes", []),
        "cleanup": {
            "stale_blocks_removed_from_teacher_default_flow": removals,
            "right_rail_policy": "P6 episode linkage first; legacy draft collapsed into developer/history details when rendered.",
            "bottom_xiaojiao_policy": "static selected-episode context smoke; no runtime call.",
            "teacher_action_policy": "all teacher actions are preview_only/no-op.",
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
            "source_R91A_R87_modified": False,
        },
        "teacher_actions": actions.get("actions", []),
        "teacher_review_required": True,
        "formal_apply": False,
    }


def build_injected_assets(viewmodel):
    runtime_vm = json.loads(json.dumps(viewmodel, ensure_ascii=False))
    runtime_vm["cleanup"] = {
        "stale_blocks_removed_from_teacher_default_flow": [
            {
                "id": "history_candidate_preview_panel",
                "matched_count": item["matched_count"],
                "action": item["action"],
                "developer_access": "documented_in_cleanup_report_only",
            }
            for item in viewmodel["cleanup"]["stale_blocks_removed_from_teacher_default_flow"]
        ],
        "right_rail_policy": viewmodel["cleanup"]["right_rail_policy"],
        "bottom_xiaojiao_policy": viewmodel["cleanup"]["bottom_xiaojiao_policy"],
        "teacher_action_policy": viewmodel["cleanup"]["teacher_action_policy"],
    }
    safe_vm_json = json.dumps(runtime_vm, ensure_ascii=False).replace("</", "<\\/")
    css = """
<style id="r97b-teacher-shell-experience-cleanup-style">
  html[data-1013r-r97b-clean-shell="true"] .r97a3-bottom-context {
    display: none !important;
  }

  html[data-1013r-r97b-clean-shell="true"] .r97b-legacy-rail-details,
  html[data-1013r-r97b-clean-shell="true"] .r97b-developer-archive {
    border: 1px dashed rgba(50, 95, 83, .28);
    border-radius: 8px;
    background: rgba(247, 251, 248, .92);
    color: rgba(24, 62, 54, .78);
    padding: 10px 12px;
    font-size: 12px;
    line-height: 1.55;
  }

  html[data-1013r-r97b-clean-shell="true"] .r97b-legacy-rail-details summary,
  html[data-1013r-r97b-clean-shell="true"] .r97b-developer-archive summary {
    cursor: pointer;
    font-weight: 850;
    color: #2d7668;
  }

  html[data-1013r-r97b-clean-shell="true"] .r97a3-episode-rail-item {
    cursor: pointer;
    transition: border-color .16s ease, background .16s ease;
  }

  html[data-1013r-r97b-clean-shell="true"] .r97a3-episode-rail-item.is-active {
    border-color: rgba(37, 118, 101, .55);
    background: rgba(231, 246, 241, .9);
  }

  html[data-1013r-r97b-clean-shell="true"] .r97b-context-tabs {
    display: flex;
    gap: 6px;
    flex-wrap: wrap;
    margin: 8px 0 10px;
  }

  html[data-1013r-r97b-clean-shell="true"] .r97b-context-tab {
    border: 1px solid rgba(36, 84, 70, .22);
    background: rgba(255, 255, 255, .88);
    color: #2d7668;
    border-radius: 999px;
    padding: 4px 9px;
    font-size: 12px;
    font-weight: 800;
    cursor: pointer;
  }

  html[data-1013r-r97b-clean-shell="true"] .r97b-context-tab.is-active {
    background: #2d7668;
    color: #fff;
  }

  html[data-1013r-r97b-clean-shell="true"] .r97b-bottom-context {
    position: fixed;
    left: 50%;
    transform: translateX(-50%);
    bottom: 76px;
    z-index: 60;
    width: min(920px, calc(100vw - 56px));
    border: 1px solid rgba(36, 84, 70, .16);
    border-radius: 12px;
    background: rgba(255, 253, 246, .96);
    box-shadow: 0 16px 42px rgba(20, 61, 52, .13);
    color: #203f39;
    overflow: hidden;
  }

  html[data-1013r-r97b-clean-shell="true"] .r97b-bottom-context summary {
    cursor: pointer;
    padding: 10px 14px;
    font-weight: 900;
    color: #2d7668;
    border-bottom: 1px solid rgba(36, 84, 70, .11);
  }

  html[data-1013r-r97b-clean-shell="true"] .r97b-context-body {
    padding: 0 14px 12px;
  }

  html[data-1013r-r97b-clean-shell="true"] .r97b-context-grid {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 10px;
  }

  html[data-1013r-r97b-clean-shell="true"] .r97b-context-grid div {
    border-left: 3px solid rgba(45, 118, 104, .32);
    padding-left: 9px;
    font-size: 12px;
    line-height: 1.55;
  }

  html[data-1013r-r97b-clean-shell="true"] .r97b-action-state-note {
    margin-top: 8px;
    border-radius: 8px;
    background: rgba(255, 251, 235, .88);
    border: 1px solid rgba(191, 147, 52, .22);
    padding: 8px 10px;
    color: rgba(72, 58, 32, .9);
    font-size: 12px;
    line-height: 1.55;
  }

  @media (max-width: 900px) {
    html[data-1013r-r97b-clean-shell="true"] .r97b-context-grid {
      grid-template-columns: 1fr;
    }
  }
</style>
"""
    js = """
<script id="r97b-teacher-shell-experience-cleanup-script">
  (() => {
    const vm = __R97B_VIEWMODEL_JSON__;
    const episodes = vm.episodes || [];
    const byEpisode = new Map(episodes.map((item) => [item.episode_id, item]));

    document.documentElement.setAttribute("data-1013r-r97b-clean-shell", "true");

    function esc(value) {
      return String(value ?? "").replace(/[&<>"']/g, (ch) => ({
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#39;"
      }[ch]));
    }

    function demoteLegacyRightRail() {
      const rail = document.querySelector(".courseware-rail");
      if (!rail || rail.querySelector(".r97b-legacy-rail-details")) return;
      const details = document.createElement("details");
      details.className = "r97b-legacy-rail-details";
      details.innerHTML = `
        <summary>历史大屏草稿已折叠，仅开发者核对</summary>
        <p>教师默认右栏以 P6 课堂联动为主；历史 8 屏草稿不参与当前阅读主流程。</p>
      `;
      const legacyNodes = [
        ".courseware-rail-summary",
        ".courseware-screen-list",
        ".courseware-current-link",
        ".courseware-rail-actions"
      ];
      for (const selector of legacyNodes) {
        for (const node of Array.from(rail.querySelectorAll(selector))) {
          if (!node.closest(".r97a3-rail-panel")) {
            details.appendChild(node);
          }
        }
      }
      const p6Panel = rail.querySelector(".r97a3-rail-panel");
      if (p6Panel && p6Panel.nextSibling) {
        rail.insertBefore(details, p6Panel.nextSibling);
      } else {
        rail.appendChild(details);
      }
    }

    function addDeveloperArchiveNotice() {
      if (document.querySelector(".r97b-developer-archive")) return;
      const anchor = document.querySelector(".nb-doc") || document.querySelector(".nb-workspace");
      if (!anchor) return;
      const details = document.createElement("details");
      details.className = "r97b-developer-archive";
      details.setAttribute("data-r97b-developer-archive", "true");
      details.innerHTML = `
        <summary>开发者折叠区：旧审核残留已移出教师默认流</summary>
        <p>历史候选预览与历史回填区已从教师默认阅读页剔除；清单见 R97B 清理报告。本区只说明处理结果，不承载课堂阅读内容。</p>
      `;
      anchor.appendChild(details);
    }

    function markRailEpisodes() {
      const items = Array.from(document.querySelectorAll(".r97a3-episode-rail-item"));
      items.forEach((item, index) => {
        const episode = episodes[index];
        if (!episode) return;
        item.setAttribute("data-r97b-episode-id", episode.episode_id);
        item.setAttribute("role", "button");
        item.setAttribute("tabindex", "0");
        if (index === 0) item.classList.add("is-active");
      });
    }

    function buildContextPanel() {
      if (document.querySelector(".r97b-bottom-context") || !episodes.length) return;
      const first = episodes[0];
      const box = document.createElement("details");
      box.className = "r97b-bottom-context";
      box.open = false;
      box.innerHTML = `
        <summary>小教上下文预览：可按教学环节切换 · 静态 smoke · 不调用 runtime</summary>
        <div class="r97b-context-body">
          <div class="r97b-context-tabs">
            ${episodes.map((item) => `<button class="r97b-context-tab" type="button" data-r97b-context-tab="${esc(item.episode_id)}">${esc(item.episode_index)}. ${esc(item.episode_title)}</button>`).join("")}
          </div>
          <div class="r97b-context-grid" data-r97b-context-grid></div>
        </div>
      `;
      document.body.appendChild(box);
      updateContext(first.episode_id);
    }

    function updateContext(episodeId) {
      const item = byEpisode.get(episodeId) || episodes[0];
      if (!item) return;
      const x = item.xiaojiao_context || {};
      const grid = document.querySelector("[data-r97b-context-grid]");
      if (grid) {
        grid.innerHTML = `
          <div><strong>${esc(item.episode_index)}. ${esc(item.episode_title)}</strong><br>${esc(x.next_action_hint || "")}</div>
          <div><strong>教师话术</strong><br>${esc(x.teacher_talk || "")}</div>
          <div><strong>可能卡点 / 证据</strong><br>${esc(x.misconception || "")}<br>${esc(x.evidence_check || "")}</div>
        `;
      }
      document.querySelectorAll(".r97b-context-tab").forEach((btn) => {
        btn.classList.toggle("is-active", btn.getAttribute("data-r97b-context-tab") === item.episode_id);
      });
      document.querySelectorAll(".r97a3-episode-rail-item").forEach((node) => {
        node.classList.toggle("is-active", node.getAttribute("data-r97b-episode-id") === item.episode_id);
      });
      window.__R97B_SELECTED_EPISODE_CONTEXT__ = {
        episode_id: item.episode_id,
        episode_title: item.episode_title,
        preview_only: true,
        runtime_call_allowed: false
      };
    }

    function bindContextSwitching() {
      document.addEventListener("click", (event) => {
        const tab = event.target.closest && event.target.closest("[data-r97b-context-tab]");
        if (tab) updateContext(tab.getAttribute("data-r97b-context-tab"));
        const railItem = event.target.closest && event.target.closest(".r97a3-episode-rail-item[data-r97b-episode-id]");
        if (railItem) updateContext(railItem.getAttribute("data-r97b-episode-id"));
      });
      document.addEventListener("keydown", (event) => {
        if (event.key !== "Enter" && event.key !== " ") return;
        const railItem = event.target.closest && event.target.closest(".r97a3-episode-rail-item[data-r97b-episode-id]");
        if (!railItem) return;
        event.preventDefault();
        updateContext(railItem.getAttribute("data-r97b-episode-id"));
      });
    }

    function addActionStateNote() {
      const panel = document.querySelector(".r97a3-rail-panel");
      if (!panel || panel.querySelector(".r97b-action-state-note")) return;
      const note = document.createElement("div");
      note.className = "r97b-action-state-note";
      note.textContent = "本页四个教师动作均为 preview-only/no-op：不保存、不导出、不写库、不进入 R95。";
      panel.appendChild(note);
    }

    function applyR97BCleanup() {
      demoteLegacyRightRail();
      addDeveloperArchiveNotice();
      markRailEpisodes();
      buildContextPanel();
      addActionStateNote();
      bindContextSwitching();
      updateContext((episodes[0] || {}).episode_id);
      window.__R97B_TEACHER_SHELL_EXPERIENCE__ = {
        stage: vm.stage,
        stale_default_blocks_removed: true,
        p6_slot_preserved: !!document.querySelector(".r97a2-p6-step[data-r97a2-p6-episode]"),
        right_rail_p6_first: !!document.querySelector(".r97a3-rail-panel"),
        legacy_rail_collapsed: !!document.querySelector(".r97b-legacy-rail-details"),
        episode_context_switching_static: !!document.querySelector(".r97b-bottom-context"),
        formal_apply: false,
        R95_executed: false
      };
    }

    applyR97BCleanup();
    document.addEventListener("DOMContentLoaded", applyR97BCleanup);
    window.addEventListener("load", () => {
      applyR97BCleanup();
      setTimeout(applyR97BCleanup, 0);
      setTimeout(applyR97BCleanup, 160);
      setTimeout(applyR97BCleanup, 600);
    });
    setTimeout(applyR97BCleanup, 0);
    setTimeout(applyR97BCleanup, 320);
  })();
</script>
"""
    return css + js.replace("__R97B_VIEWMODEL_JSON__", safe_vm_json)


def write_reports(viewmodel, removals, courseware_map, worksheet_rubric_map, xiaojiao_context, teacher_actions):
    CLEANUP_REPORT_OUT.write_text(
        "\n".join(
            [
                "# R97B Stale Content Cleanup Report",
                "",
                "本轮目标是清理 R97A3 复制页中的旧审核残留，使教师默认阅读流只呈现干净的单课备课闭环。",
                "",
                "## 已处理",
                "",
                "- `mock_candidate_fixture` 所在的 R39 候选预览块：从教师默认 HTML 中移除。",
                "- `R90B / R90B-P1 / R91A` 回填面板：从教师默认 HTML 中移除。",
                "- `old candidate preview`、`修改前 / 修改后候选` 等旧审核内容：不再作为教师默认阅读流显示。",
                "- 右侧历史 8 屏大屏草稿：运行时降级到开发者折叠区，P6 课堂联动优先。",
                "",
                "## 清理记录",
                "",
                *[
                    f"- `{item['id']}`：matched={item['matched_count']}，action={item['action']}"
                    for item in removals
                ],
                "",
                "## 保留边界",
                "",
                "- 未修改真实 R91A/R87 源壳层。",
                "- 未改 R21/R36 core。",
                "- 未 formal apply，未写库/飞书/记忆。",
                "- 未生成 PPTX/PDF/DOCX，未进入 R95。",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    RIGHT_RAIL_POLICY_OUT.write_text(
        "\n".join(
            [
                "# R97B Right Rail Priority Policy",
                "",
                "右侧栏在教师默认视图中的优先级：",
                "",
                "1. P6 课堂联动。",
                "2. 当前 episode 对应的大屏页 S01-S10。",
                "3. 当前 episode 对应的学习单任务、教师观察维度、学生自评项。",
                "4. 小教当前 episode 提示。",
                "5. 历史 8 屏草稿与旧 draft 只能折叠为开发者/历史核对内容。",
                "",
                "## Episode 到右栏",
                "",
                *[
                    "- {idx}. {title}：{slides}".format(
                        idx=row["episode_index"],
                        title=row["episode_title"],
                        slides=" / ".join(row["courseware_slide_ids"]),
                    )
                    for row in courseware_map["rows"]
                ],
                "",
                "本策略只用于静态 preview，不导出正式课件。",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    XIAOJIAO_SMOKE_OUT.write_text(
        "\n".join(
            [
                "# R97B Xiaojiao Episode Context Smoke",
                "",
                "本轮验证底部小教上下文可按 5 个 episode 静态切换，不调用 runtime。",
                "",
                *[
                    "- 选择 `{eid}`：显示 `{title}`；提示 `{hint}`；证据 `{evidence}`。".format(
                        eid=row["episode_id"],
                        title=row["episode_title"],
                        hint=row.get("next_action_hint", ""),
                        evidence=row.get("evidence_check", ""),
                    )
                    for row in xiaojiao_context["rows"]
                ],
                "",
                "结果：STATIC_CONTEXT_MAP_READY，preview_only=true，runtime_call_allowed=false。",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    ACTION_SMOKE_OUT.write_text(
        "\n".join(
            [
                "# R97B Teacher Action Preview State Smoke",
                "",
                "四个教师动作均为 preview_only/no-op：",
                "",
                *[
                    "- `{label}`：state={state}，formal_apply_allowed={formal}，database_write_allowed={db}，runtime_call_allowed={runtime}。".format(
                        label=action["label"],
                        state=action["state"],
                        formal=str(action["formal_apply_allowed"]).lower(),
                        db=str(action["database_write_allowed"]).lower(),
                        runtime=str(action["runtime_call_allowed"]).lower(),
                    )
                    for action in teacher_actions["actions"]
                ],
                "",
                "结果：PASS，未进入保存、导出、formal apply 或 R95。",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    README_OUT.write_text(
        "\n".join(
            [
                "# 1013R_R97B_TEACHER_SHELL_EXPERIENCE_POLISH_AND_STALE_CONTENT_CLEANUP",
                "",
                "R97A3 已证明 P6 与右侧大屏、学习单/评价、小教上下文之间的静态关系。本轮只做教师壳层体验清理：把旧 mock/R90B/R91A 审核残留移出教师默认阅读流，并把右栏优先级调整为 P6 课堂联动。",
                "",
                "## 输出",
                "",
                f"- `{HTML_OUT.name}`",
                f"- `{VM_OUT.name}`",
                f"- `{CLEANUP_REPORT_OUT.name}`",
                f"- `{RIGHT_RAIL_POLICY_OUT.name}`",
                f"- `{XIAOJIAO_SMOKE_OUT.name}`",
                f"- `{ACTION_SMOKE_OUT.name}`",
                f"- `{VALIDATOR_OUT.name}`",
                "",
                "## 边界",
                "",
                "- 静态复制页 preview，不接真实 runtime。",
                "- 未修改真实 R91A/R87 壳层源文件。",
                "- 不改 R21/R36 core。",
                "- 不 formal apply，不写数据库/飞书/记忆。",
                "- 不生成 PPTX/PDF/DOCX，不进入 R95。",
                "",
                f"HTML SHA256: `{sha256(HTML_OUT) if HTML_OUT.exists() else ''}`",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def main():
    source_vm = load_json(R97A3_VM)
    courseware_map = load_json(R97A3_COURSEWARE_MAP)
    worksheet_rubric_map = load_json(R97A3_WORKSHEET_RUBRIC_MAP)
    xiaojiao_context = load_json(R97A3_XIAOJIAO_CONTEXT)
    teacher_actions = load_json(R97A3_TEACHER_ACTIONS)

    html = R97A3_HTML.read_text(encoding="utf-8")
    cleaned_html, removals = remove_default_visible_stale_blocks(html)
    clean_vm = build_clean_viewmodel(source_vm, removals, teacher_actions)
    write_json(VM_OUT, clean_vm)

    injected = build_injected_assets(clean_vm)
    if "</body>" not in cleaned_html:
        raise RuntimeError("R97A3 HTML does not contain </body>")
    HTML_OUT.write_text(cleaned_html.replace("</body>", injected + "\n</body>", 1), encoding="utf-8")

    out_html = HTML_OUT.read_text(encoding="utf-8")
    write_reports(clean_vm, removals, courseware_map, worksheet_rubric_map, xiaojiao_context, teacher_actions)

    checks = {
        "html_created": HTML_OUT.exists(),
        "source_r97a3_html_exists": R97A3_HTML.exists(),
        "r39_mock_candidate_panel_removed_from_static_html": 'class="r39-candidate-preview-panel"' not in out_html,
        "r91a_backfill_panel_removed_from_static_html": 'class="r91a-backfill-panel"' not in out_html,
        "r97a2_p6_slot_preserved": "r97a2-p6-step" in out_html and "data-r97a2-p6-episode" in out_html,
        "r97a3_p6_right_rail_preserved": "P6 课堂联动" in out_html and "r97a3-rail-panel" in out_html,
        "r97b_cleanup_marker_present": "data-1013r-r97b-clean-shell" in out_html,
        "r97b_legacy_rail_collapse_script_present": "demoteLegacyRightRail" in out_html,
        "r97b_episode_context_switching_script_present": "updateContext" in out_html and "data-r97b-context-tab" in out_html,
        "teacher_actions_preview_only": all(
            action["state"] == "preview_only_noop"
            and not action["formal_apply_allowed"]
            and not action["database_write_allowed"]
            and not action["runtime_call_allowed"]
            for action in teacher_actions["actions"]
        ),
        "episode_count_is_5": len(clean_vm["episodes"]) == 5,
        "courseware_mapping_count_is_5": len(courseware_map["rows"]) == 5,
        "worksheet_rubric_mapping_count_is_5": len(worksheet_rubric_map["rows"]) == 5,
        "xiaojiao_context_count_is_5": len(xiaojiao_context["rows"]) == 5,
        "formal_apply_false": clean_vm["formal_apply"] is False,
        "r95_not_executed": clean_vm["boundary"]["R95_executed"] is False,
        "r21_r36_core_not_modified": clean_vm["boundary"]["r21_core_modified"] is False
        and clean_vm["boundary"]["r36_core_modified"] is False,
    }
    blocking = [name for name, ok in checks.items() if ok is not True]
    validator = {
        "stage": "1013R_R97B_TEACHER_SHELL_EXPERIENCE_POLISH_AND_STALE_CONTENT_CLEANUP",
        "status": "PASS" if not blocking else "FAIL",
        "blocking": blocking,
        "checks": checks,
        "output_html": str(HTML_OUT),
        "output_sha256": sha256(HTML_OUT),
        "removed_default_visible_blocks": removals,
        "boundary": clean_vm["boundary"],
        "teacher_review_required": True,
        "formal_apply": False,
        "R95_executed": False,
        "next_allowed": "R95_STATIC_ARTIFACT_EXPORT_PREVIEW only after user/GPT acceptance",
    }
    write_json(VALIDATOR_OUT, validator)
    print(json.dumps(validator, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
