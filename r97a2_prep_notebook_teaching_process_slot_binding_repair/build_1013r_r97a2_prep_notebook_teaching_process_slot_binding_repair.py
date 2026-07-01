import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = Path(__file__).resolve().parent

SHELL_SOURCE = ROOT / "1013R_R91A_STATIC_PAGE_BACKFILL" / "R91A_static_page_backfill_from_R39_product_candidate_preview.html"
P6_VIEWMODEL = ROOT / "1013R_R93_P6_TEACHER_NAVIGATION_VIEW_AND_TALK_FLOW" / "r93_p6_teacher_navigation_viewmodel.json"

HTML_OUT = OUT_DIR / "R91A_prep_notebook_teaching_process_slot_binding_from_R93_P6.html"
VIEWMODEL_OUT = OUT_DIR / "r97a2_slot_binding_viewmodel.json"
AUDIT_OUT = OUT_DIR / "r97a2_original_shell_slot_audit.md"
DEMOTE_OUT = OUT_DIR / "r97a2_previous_r97a_demote_decision.md"
VALIDATOR_OUT = OUT_DIR / "validate_1013R_R97A2_prep_notebook_teaching_process_slot_binding_repair_result.json"
README_OUT = OUT_DIR / "README.md"


PROCESS_STEP_START = "    function renderProcessStep(view, step, index) {"
PROCESS_STEP_END = "    function renderEditBubble(view, title) {"
R21_DATA_SCRIPT_MARKER = '<script id="data-1013R-R21-unified-package" type="application/json">'
R21_BINDING_SCRIPT_MARKER = '<script id="script-1013R-R21-internal-prototype-binding">'
R21_NORMALIZE_PROCESS_STEP_START = "      function normalizeProcessSteps(steps, links) {"
R21_NORMALIZE_PROCESS_STEP_END = "      function normalizeCoursewareScreens(screens) {"


R97A2_RENDER_PROCESS_STEP_SOURCE = r'''    function renderProcessStep(view, step, index) {
      const episode = step?.p6;
      if (!episode) {
        const mode = prepNotebookMode(view);
        const target = prepActiveTarget(view);
        const isFocused = mode === "edit" && target.stepId === step.id;
        const plan = readableStepPlan(step);
        return `
          <article class="nb-readable-step ${isFocused ? "edit-focus" : ""}" id="nb-step-${html(step.id)}">
            <div class="nb-readable-head">
              <div class="nb-readable-title">
                ${index + 1}. ${html(step.name)}：${html((step.summary || step.name).split("，")[0])}
                <span>${html(step.time)} · ${html((step.tags || []).join(" / "))}</span>
              </div>
              <div class="nb-edit-tools">
                <button class="nb-soft-button" type="button" data-edit-target="process:${html(step.id)}">${isFocused ? "收起" : "编辑"}</button>
              </div>
            </div>
            <div class="nb-readable-body">
              ${renderCoursewareStepMarkers(step.id)}
              <ol class="nb-step-detail-list">
              ${(plan.paragraphs || [step.summary]).map((paragraph, paragraphIndex) => {
                const paragraphId = paragraphAnchorId(step, paragraphIndex);
                const selected = isFocused && target.paragraphId === paragraphId;
                const microTitle = microStepTitle(step.id, paragraphIndex, paragraph);
                return `
                  <li class="nb-anchor-paragraph nb-step-detail-item ${selected ? "selected" : ""}"
                     data-edit-target="process:${html(step.id)}:${html(paragraphId)}"
                     data-hover-note="${html(plan.hover)}"><span class="nb-micro-title">${html(microTitle)}</span><span class="nb-micro-text">${html(paragraph)}</span></li>
                `;
              }).join("")}
              </ol>
            </div>
            ${isFocused ? renderEditBubble(view, `${step.name}环节`) : ""}
          </article>
        `;
      }

      const mode = prepNotebookMode(view);
      const target = prepActiveTarget(view);
      const isFocused = mode === "edit" && target.stepId === step.id;
      const microSteps = episode.micro_steps || [];
      const teacherSteps = episode.teacher_three_steps || [];
      return `
        <article class="nb-readable-step r97a2-p6-step ${isFocused ? "edit-focus" : ""}" id="nb-step-${html(step.id)}" data-r97a2-p6-episode="${html(episode.episode_id)}">
          <div class="r97a2-step-head">
            <div>
              <div class="r97a2-step-kicker">${html(episode.episode_type)} · ${html(episode.duration)}</div>
              <div class="r97a2-step-title">${index + 1}. ${html(episode.title)}</div>
            </div>
            <button class="nb-soft-button" type="button" data-edit-target="process:${html(step.id)}">${isFocused ? "收起" : "进入编辑"}</button>
          </div>
          <p class="r97a2-step-goal">${html(episode.goal)}</p>
          ${renderCoursewareStepMarkers(step.id)}
          <div class="r97a2-main-row">
            <div>
              <div class="r97a2-line-title"><span class="r97a2-icon">师</span><span>老师三步</span></div>
              <ol class="r97a2-list">
                ${teacherSteps.map((item) => `<li>${html(item)}</li>`).join("")}
              </ol>
            </div>
            <div>
              <div class="r97a2-line-title"><span class="r97a2-icon">生</span><span>学生产出</span></div>
              <p class="r97a2-student-output">${html(episode.student_output)}</p>
            </div>
          </div>
          <div class="r97a2-talk-row">
            <div>
              <div class="r97a2-line-title"><span class="r97a2-icon">话</span><span>关键话术</span></div>
              <p class="r97a2-talk">${html(episode.key_talk)}</p>
            </div>
            <div>
              <div class="r97a2-line-title"><span class="r97a2-icon">助</span><span>小教提醒</span></div>
              <p class="r97a2-reminder">${html(episode.xiaojiao_key_reminder)}</p>
            </div>
          </div>
          <details class="r97a2-fold">
            <summary>展开本环节 micro-step、大屏、支架、小教和证据</summary>
            <div class="r97a2-micro-table">
              ${microSteps.map((item, microIndex) => `
                <div class="r97a2-micro-item">
                  <div class="r97a2-micro-no">${microIndex + 1}</div>
                  <div>
                    <div class="r97a2-micro-title">${html(item.step_name)}</div>
                    <div class="r97a2-micro-meta"><strong>教师</strong> ${html(item.teacher_action)}｜<strong>学生</strong> ${html(item.student_action)}</div>
                    <div class="r97a2-micro-meta"><strong>大屏</strong> ${html(item.screen_state)}｜<strong>支架</strong> ${html(item.student_scaffold)}</div>
                    <div class="r97a2-micro-meta"><strong>小教</strong> ${html(item.xiaojiao_support)}｜<strong>证据</strong> ${html(item.evidence_check)}</div>
                  </div>
                </div>
              `).join("")}
            </div>
          </details>
          ${isFocused ? renderEditBubble(view, `${step.name}环节`) : ""}
        </article>
      `;
    }

'''


R97A2_R21_NORMALIZE_PROCESS_STEPS_SOURCE = r'''      function normalizeProcessSteps(steps, links) {
        const linkList = Array.isArray(links) ? links : [];
        const linkMap = new Map(linkList.map((item) => [String(item.process_step_id || ""), item]));
        const times = ["4分钟", "8分钟", "10分钟", "13分钟", "5分钟"];
        const detailMap = typeof processDetailMap === "function" ? processDetailMap() : {};
        return (Array.isArray(steps) ? steps : []).map((step, index) => {
          if (step && step.p6) {
            const episode = step.p6 || {};
            const micro = Array.isArray(episode.micro_steps) ? episode.micro_steps : [];
            const stepId = step.id || `p6_${index + 1}`;
            const teacherLine = Array.isArray(episode.teacher_three_steps) ? episode.teacher_three_steps.join(" → ") : "";
            return {
              id: stepId,
              name: step.name || step.title || episode.title || `教学步骤 ${index + 1}`,
              time: step.time || String(episode.duration || "").replace(/^约/, "") || times[index] || "",
              summary: step.summary || episode.goal || "",
              readable_hover: episode.goal || "",
              readable_details: [],
              tags: step.tags || [episode.episode_type, "P6教师导航"].filter(Boolean),
              p6_episode_id: step.p6_episode_id || episode.episode_id || stepId,
              p6: episode,
              intent: step.intent || {
                role: episode.goal || "",
                design: "R97A2 只将 R93-P6 教师导航内容接入六、教学过程槽位，不覆盖本课依据等其他章节。",
                transition: micro[micro.length - 1]?.next_step_trigger || "",
                student: episode.student_output || "",
                teacher: teacherLine,
                activity: micro.map((item) => item.student_action).filter(Boolean).slice(0, 3).join("；"),
                screen: micro.map((item) => item.screen_state).filter(Boolean).slice(0, 2).join("；"),
                material: micro.map((item) => item.student_scaffold).filter(Boolean).slice(0, 2).join("；"),
                evidence: episode.xiaojiao_cards?.evidence || micro.map((item) => item.evidence_check).filter(Boolean).slice(0, 2).join("；"),
                risk: episode.xiaojiao_cards?.misconception || micro.map((item) => item.if_student_stuck).filter(Boolean).slice(0, 2).join("；"),
              },
            };
          }
          const link = linkMap.get(String(step.id || "")) || linkList[index] || {};
          const stepId = `r21_${step.id || index + 1}`;
          const detail = detailMap[stepId] || {};
          return {
            id: stepId,
            name: step.title || `教学步骤 ${index + 1}`,
            time: times[index] || "",
            summary: [step.teacher_action, step.student_action].filter(Boolean).join(" "),
            readable_hover: detail.hover || "",
            readable_details: detail.details || [],
            tags: [
              link.courseware_screen?.title,
              link.classroom_display?.student_visible_prompt,
              link.worksheet?.render_state,
              link.assessment_rubric?.render_state,
            ].filter(Boolean).slice(0, 3),
            intent: {
              role: detail.role || "",
              design: detail.design || "",
              transition: detail.transition || "",
              student: detail.student || "",
              teacher: step.teacher_action || "",
              activity: step.student_action || "",
              screen: link.classroom_display?.student_visible_prompt || step.screen_seed || "",
              material: link.worksheet?.capture_prompt || "",
              evidence: link.assessment_rubric?.evidence || step.evidence || "",
              risk: detail.risk || "",
            },
          };
        });
      }

'''


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def compact_episode(ep):
    return {
        "index": ep["index"],
        "episode_id": ep["episode_id"],
        "title": ep["title"],
        "episode_type": ep["episode_type"],
        "duration": ep["duration"],
        "goal": ep["goal"],
        "teacher_three_steps": ep["teacher_three_steps"],
        "student_output": ep["student_output"],
        "key_talk": ep["key_talk"],
        "xiaojiao_key_reminder": ep["xiaojiao_key_reminder"],
        "micro_steps": ep["micro_steps"],
        "language_layers": ep.get("language_layers", {}),
        "xiaojiao_cards": ep.get("xiaojiao_cards", {}),
    }


def duration_to_time(duration):
    return str(duration or "").removeprefix("约") or "待定"


def build_process_steps_from_episodes(episodes):
    step_ids = ["intro", "sense", "explore", "make", "share"]
    steps = []
    for index, episode in enumerate(episodes):
      teacher_line = " → ".join(episode.get("teacher_three_steps", []))
      micro = episode.get("micro_steps", [])
      steps.append({
          "id": step_ids[index] if index < len(step_ids) else f"episode_{index + 1}",
          "name": episode.get("title", f"环节{index + 1}"),
          "time": duration_to_time(episode.get("duration")),
          "summary": episode.get("goal", ""),
          "tags": [item for item in [episode.get("episode_type"), "P6教师导航"] if item],
          "p6_episode_id": episode.get("episode_id"),
          "p6": episode,
          "intent": {
              "role": episode.get("goal", ""),
              "design": "本轮只将 R93-P6 教师导航内容接入六、教学过程，不覆盖本课依据等其他备课章节。",
              "transition": micro[-1].get("next_step_trigger", "") if micro else "",
              "student": episode.get("student_output", ""),
              "teacher": teacher_line,
              "activity": "；".join([item.get("student_action", "") for item in micro if item.get("student_action")][:3]),
              "screen": "；".join([item.get("screen_state", "") for item in micro if item.get("screen_state")][:2]),
              "material": "；".join([item.get("student_scaffold", "") for item in micro if item.get("student_scaffold")][:2]),
              "evidence": episode.get("xiaojiao_cards", {}).get("evidence", "") or "；".join([item.get("evidence_check", "") for item in micro if item.get("evidence_check")][:2]),
              "risk": episode.get("xiaojiao_cards", {}).get("misconception", "") or "；".join([item.get("if_student_stuck", "") for item in micro if item.get("if_student_stuck")][:2]),
          },
      })
    return steps


def build_injected_assets(vm):
    slot_vm = {
        "stage": "1013R_R97A2_PREP_NOTEBOOK_TEACHING_PROCESS_SLOT_BINDING_REPAIR",
        "source_shell": str(SHELL_SOURCE),
        "source_p6_viewmodel": str(P6_VIEWMODEL),
        "binding_policy": {
            "copy_shell_only": True,
            "replace_render_layer": False,
            "replace_full_prep_notebook": False,
            "target_slot": "model.views.prepNotebook.current_lesson.process_steps",
            "target_visible_section": "六、教学过程",
            "preserve_lesson_sections": [
                "basis",
                "analysis",
                "goals",
                "keypoints",
                "preparation",
                "assessment",
                "reflection",
            ],
            "preserve_original_shell": [
                "topbar",
                "context-bar",
                "viewTabs",
                "renderLayer",
                "nb-tree",
                "nb-workspace",
                "courseware-rail",
                "xiaobei-chat-entry",
            ],
        },
        "lesson": vm["lesson"],
        "episodes": [compact_episode(ep) for ep in vm["episodes"]],
        "process_steps": build_process_steps_from_episodes([compact_episode(ep) for ep in vm["episodes"]]),
        "teacher_review_required": True,
        "formal_apply": False,
    }

    slot_json = json.dumps(slot_vm, ensure_ascii=False)

    css = r"""
  <style id="style-1013R-R97A2-slot-binding">
    html[data-1013r-r97a2-slot-binding="true"] .nb-process-section {
      scroll-margin-top: 120px;
    }
    html[data-1013r-r97a2-slot-binding="true"] .r97a2-p6-step {
      border: 0;
      border-top: 1px solid rgba(37, 111, 91, 0.18);
      border-radius: 0;
      box-shadow: none;
      background: transparent;
      padding: 18px 0 16px;
      margin: 0;
    }
    html[data-1013r-r97a2-slot-binding="true"] .r97a2-p6-step:first-child {
      border-top: 0;
    }
    html[data-1013r-r97a2-slot-binding="true"] .r97a2-step-head {
      display: grid;
      grid-template-columns: minmax(0, 1fr) auto;
      gap: 14px;
      align-items: baseline;
      margin-bottom: 8px;
    }
    html[data-1013r-r97a2-slot-binding="true"] .r97a2-step-kicker {
      color: #2c7d67;
      font-size: 12px;
      font-weight: 700;
      margin-bottom: 3px;
    }
    html[data-1013r-r97a2-slot-binding="true"] .r97a2-step-title {
      color: #1c2d2a;
      font-size: 22px;
      line-height: 1.2;
      font-weight: 800;
    }
    html[data-1013r-r97a2-slot-binding="true"] .r97a2-step-goal {
      margin: 8px 0 12px;
      color: #556a66;
      line-height: 1.75;
      font-size: 14px;
    }
    html[data-1013r-r97a2-slot-binding="true"] .r97a2-main-row {
      display: grid;
      grid-template-columns: minmax(0, 1.15fr) minmax(0, 0.85fr);
      gap: 18px;
      margin: 12px 0;
      border-left: 3px solid rgba(44, 125, 103, 0.22);
      padding-left: 12px;
    }
    html[data-1013r-r97a2-slot-binding="true"] .r97a2-line-title {
      display: flex;
      align-items: center;
      gap: 8px;
      color: #1d342f;
      font-weight: 800;
      margin-bottom: 6px;
      font-size: 14px;
    }
    html[data-1013r-r97a2-slot-binding="true"] .r97a2-icon {
      display: inline-grid;
      place-items: center;
      width: 22px;
      height: 22px;
      border-radius: 999px;
      background: #2c7d67;
      color: #fff;
      font-size: 12px;
      font-weight: 800;
      flex: 0 0 auto;
    }
    html[data-1013r-r97a2-slot-binding="true"] .r97a2-list {
      margin: 0;
      padding-left: 28px;
      color: #58716c;
      line-height: 1.75;
      font-size: 14px;
    }
    html[data-1013r-r97a2-slot-binding="true"] .r97a2-student-output {
      color: #58716c;
      line-height: 1.8;
      font-size: 14px;
      margin: 0;
    }
    html[data-1013r-r97a2-slot-binding="true"] .r97a2-talk-row {
      display: grid;
      grid-template-columns: minmax(0, 1.1fr) minmax(0, 0.9fr);
      gap: 18px;
      margin: 12px 0 10px;
      border-left: 3px solid rgba(44, 125, 103, 0.22);
      padding-left: 12px;
    }
    html[data-1013r-r97a2-slot-binding="true"] .r97a2-talk {
      margin: 0;
      color: #1d342f;
      background: #fffdf6;
      border-left: 4px solid #2c7d67;
      padding: 10px 12px;
      line-height: 1.75;
      font-size: 14px;
    }
    html[data-1013r-r97a2-slot-binding="true"] .r97a2-reminder {
      color: #58716c;
      line-height: 1.75;
      font-size: 14px;
      margin: 0;
    }
    html[data-1013r-r97a2-slot-binding="true"] .r97a2-fold {
      margin-top: 12px;
      border-top: 1px dashed rgba(37, 111, 91, 0.22);
      padding-top: 10px;
    }
    html[data-1013r-r97a2-slot-binding="true"] .r97a2-fold summary {
      color: #2c7d67;
      cursor: pointer;
      font-size: 14px;
      font-weight: 800;
      list-style-position: inside;
    }
    html[data-1013r-r97a2-slot-binding="true"] .r97a2-micro-table {
      display: grid;
      gap: 10px;
      margin-top: 12px;
    }
    html[data-1013r-r97a2-slot-binding="true"] .r97a2-micro-item {
      display: grid;
      grid-template-columns: 26px minmax(0, 1fr);
      gap: 10px;
      padding: 10px 0;
      border-top: 1px solid rgba(37, 111, 91, 0.1);
    }
    html[data-1013r-r97a2-slot-binding="true"] .r97a2-micro-no {
      color: #2c7d67;
      font-weight: 800;
      font-size: 13px;
    }
    html[data-1013r-r97a2-slot-binding="true"] .r97a2-micro-title {
      color: #1d342f;
      font-weight: 800;
      margin-bottom: 3px;
    }
    html[data-1013r-r97a2-slot-binding="true"] .r97a2-micro-meta {
      color: #58716c;
      font-size: 13px;
      line-height: 1.7;
    }
    @media (max-width: 1180px) {
      html[data-1013r-r97a2-slot-binding="true"] .r97a2-main-row,
      html[data-1013r-r97a2-slot-binding="true"] .r97a2-talk-row {
        grid-template-columns: 1fr;
      }
    }
  </style>
"""

    js = f"""
  <script id="data-1013R-R97A2-slot-binding-viewmodel" type="application/json">{slot_json}</script>
  <script id="script-1013R-R97A2-prep-notebook-teaching-process-slot-binding">
  (function() {{
    const stageId = "1013R_R97A2_PREP_NOTEBOOK_TEACHING_PROCESS_SLOT_BINDING_REPAIR";
    document.documentElement.setAttribute("data-1013r-r97a2-slot-binding", "true");
    const dataNode = document.getElementById("data-1013R-R97A2-slot-binding-viewmodel");
    if (!dataNode) return;
    const slotVm = JSON.parse(dataNode.textContent);
    const stepIds = ["intro", "sense", "explore", "make", "share"];

    function safeHtml(value) {{
      return String(value ?? "").replace(/[&<>"']/g, (ch) => ({{
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#39;"
      }}[ch]));
    }}

    function durationToTime(duration) {{
      return String(duration || "").replace(/^约/, "") || "待定";
    }}

    function mapEpisodesToSteps(episodes) {{
      return episodes.map((episode, index) => {{
        const teacherLine = (episode.teacher_three_steps || []).join(" → ");
        const micro = episode.micro_steps || [];
        return {{
          id: stepIds[index] || `episode_${{index + 1}}`,
          name: episode.title,
          time: durationToTime(episode.duration),
          summary: episode.goal,
          tags: [episode.episode_type, "P6教师导航"].filter(Boolean),
          p6_episode_id: episode.episode_id,
          p6: episode,
          intent: {{
            role: episode.goal,
            design: "本轮只将 R93-P6 教师导航内容接入六、教学过程，不覆盖本课依据等其他备课章节。",
            transition: micro[micro.length - 1]?.next_step_trigger || "",
            student: episode.student_output,
            teacher: teacherLine,
            activity: micro.map((item) => item.student_action).filter(Boolean).slice(0, 3).join("；"),
            screen: micro.map((item) => item.screen_state).filter(Boolean).slice(0, 2).join("；"),
            material: micro.map((item) => item.student_scaffold).filter(Boolean).slice(0, 2).join("；"),
            evidence: episode.xiaojiao_cards?.evidence || micro.map((item) => item.evidence_check).filter(Boolean).slice(0, 2).join("；"),
            risk: episode.xiaojiao_cards?.misconception || micro.map((item) => item.if_student_stuck).filter(Boolean).slice(0, 2).join("；")
          }}
        }};
      }});
    }}

    function p6ReadableStepPlan(step) {{
      const episode = step?.p6;
      if (!episode) return null;
      return {{
        paragraphs: episode.teacher_three_steps || [step.summary || ""],
        hover: episode.goal || "",
        note: [
          ["为什么这样安排", episode.goal || ""],
          ["学生可能卡在哪里", episode.xiaojiao_cards?.misconception || ""],
          ["可以怎么支架", (episode.micro_steps || []).map((item) => item.student_scaffold).filter(Boolean).slice(0, 2).join("；")],
          ["会带动什么", (episode.micro_steps || []).map((item) => item.screen_state).filter(Boolean).slice(0, 2).join("；")]
        ]
      }};
    }}

    if (typeof readableStepPlan === "function" && !window.__R97A2_ORIGINAL_READABLE_STEP_PLAN__) {{
      window.__R97A2_ORIGINAL_READABLE_STEP_PLAN__ = readableStepPlan;
      readableStepPlan = function(step) {{
        return p6ReadableStepPlan(step) || window.__R97A2_ORIGINAL_READABLE_STEP_PLAN__(step);
      }};
    }}

    function applySlotBinding() {{
      if (typeof model === "undefined" || !Array.isArray(model.views)) return false;
      const prepView = model.views.find((view) => view.id === "prepNotebook");
      if (!prepView || !prepView.current_lesson) return false;
      const lesson = prepView.current_lesson;
      const existingSections = Array.isArray(lesson.sections) ? lesson.sections : [];
      const existingStatusCards = Array.isArray(lesson.status_cards) ? lesson.status_cards : [];
      lesson.process_steps = slotVm.process_steps || mapEpisodesToSteps(slotVm.episodes || []);
      lesson.status = "可阅读 · 教学过程P6预览";
      lesson.sections = existingSections;
      lesson.status_cards = existingStatusCards.map((item) => Array.isArray(item) && item[0] === "渐变示范" ? ["教学过程", "P6预览", "done"] : item);
      if (!lesson.status_cards.some((item) => Array.isArray(item) && item[0] === "教学过程")) {{
        lesson.status_cards.push(["教学过程", "P6预览", "done"]);
      }}
      lesson.reasoning_binding_1013F = {{
        ...(lesson.reasoning_binding_1013F || {{}}),
        status: "R97A2槽位绑定 · 只读预览",
        judgment: "本轮只把 R93-P6 教师课堂导航内容放回“六、教学过程”槽位；本课依据、学情分析、目标、重难点、准备、评价和后记均保留原壳结构。",
        route_summary: (slotVm.episodes || []).map((item) => item.title).join(" → "),
        events: (slotVm.episodes || []).map((item, index) => ({{
          id: `P6_EVT_${{index + 1}}`,
          label: item.title,
          minutes: item.duration,
          focus: item.goal,
          question: item.key_talk,
          task: item.teacher_three_steps?.join(" / ") || "",
          evidence: item.student_output,
          change: item.xiaojiao_key_reminder
        }})),
        active_event_id: "P6_EVT_3"
      }};
      prepView.active_node = "nb-lesson-2-1";
      prepView.prep_notebook_mode = "view";
      prepView.active_big_unit_id = "";
      prepView.prep_start_surface = false;
      prepView.courseware_workspace_expanded = false;
      model.active_view = "prepNotebook";
      window.__PREP_ROOM_R97A2_SLOT_BINDING__ = {{
        stage: stageId,
        target_slot: "current_lesson.process_steps",
        preserved_sections: existingSections.map((item) => item.id),
        process_step_count: lesson.process_steps.length,
        replace_render_layer: false,
        formal_apply: false
      }};
      return true;
    }}

    const ok = applySlotBinding();
    if (ok && typeof renderPrepRoomCanvas === "function") {{
      renderPrepRoomCanvas({{ animate: false }});
      if (typeof markTeacherRouteAnchors === "function") markTeacherRouteAnchors();
      if (typeof markFrameLevels1013R25 === "function") markFrameLevels1013R25();
    }}
  }})();
  </script>
"""
    return slot_vm, css + js


def patch_process_step_renderer(shell: str) -> str:
    start = shell.find(PROCESS_STEP_START)
    end = shell.find(PROCESS_STEP_END, start)
    if start < 0 or end < 0:
        raise RuntimeError("cannot find renderProcessStep renderer boundaries")
    return shell[:start] + R97A2_RENDER_PROCESS_STEP_SOURCE + shell[end:]


def patch_r9_process_steps(shell: str, process_steps) -> str:
    func_marker = "    function applyR9RealTextbookPrepPageSync() {"
    func_start = shell.find(func_marker)
    if func_start < 0:
        raise RuntimeError("cannot find applyR9RealTextbookPrepPageSync")
    start = shell.find("        process_steps: [", func_start)
    end = shell.find("        help: {", start)
    if start < 0 or end < 0:
        raise RuntimeError("cannot find R9 process_steps boundaries")
    process_steps_js = json.dumps(process_steps, ensure_ascii=False, indent=10)
    replacement = "        process_steps: " + process_steps_js + ",\n"
    return shell[:start] + replacement + shell[end:]


def patch_r21_package_process_steps(shell: str, process_steps) -> str:
    script_start = shell.find(R21_DATA_SCRIPT_MARKER)
    if script_start < 0:
        raise RuntimeError("cannot find R21 unified package data script")
    json_start = shell.find(">", script_start)
    json_end = shell.find("</script>", json_start)
    if json_start < 0 or json_end < 0:
        raise RuntimeError("cannot find R21 unified package JSON boundaries")
    json_start += 1
    package_data = json.loads(shell[json_start:json_end])
    lesson = package_data.setdefault("lesson", {})
    existing_sections = lesson.get("sections", [])
    lesson["process_steps"] = process_steps
    lesson["sections"] = existing_sections
    package_json = json.dumps(package_data, ensure_ascii=False, separators=(",", ":"))
    return shell[:json_start] + package_json + shell[json_end:]


def patch_r21_normalize_process_steps(shell: str) -> str:
    binding_start = shell.find(R21_BINDING_SCRIPT_MARKER)
    if binding_start < 0:
        raise RuntimeError("cannot find R21 internal prototype binding script")
    start = shell.find(R21_NORMALIZE_PROCESS_STEP_START, binding_start)
    end = shell.find(R21_NORMALIZE_PROCESS_STEP_END, start)
    if start < 0 or end < 0:
        raise RuntimeError("cannot find R21 normalizeProcessSteps boundaries")
    return shell[:start] + R97A2_R21_NORMALIZE_PROCESS_STEPS_SOURCE + shell[end:]


def main():
    shell = SHELL_SOURCE.read_text(encoding="utf-8")
    p6 = load_json(P6_VIEWMODEL)
    slot_vm, injected = build_injected_assets(p6)
    shell = patch_process_step_renderer(shell)
    shell = patch_r9_process_steps(shell, slot_vm["process_steps"])
    shell = patch_r21_package_process_steps(shell, slot_vm["process_steps"])
    shell = patch_r21_normalize_process_steps(shell)
    if "</body>" not in shell:
        raise RuntimeError("source shell does not contain </body>")
    output = shell.replace("</body>", injected + "\n</body>", 1)
    HTML_OUT.write_text(output, encoding="utf-8")
    VIEWMODEL_OUT.write_text(json.dumps(slot_vm, ensure_ascii=False, indent=2), encoding="utf-8")

    preserved = slot_vm["binding_policy"]["preserve_lesson_sections"]
    AUDIT_OUT.write_text(
        "\n".join(
            [
                "# R97A2 原壳槽位审计",
                "",
                "结论：P6 不是整页壳层，只能接入原备课本正文中的 `六、教学过程` 槽位。",
                "",
                "## 原页结构",
                "",
                "- `#renderLayer` 是当前视图渲染层，不是单课内容槽位。",
                "- `renderPrepNotebookCanvas(view)` 保留备课室三栏：左侧备课本目录、中间单课正文、右侧大屏/课件草稿。",
                "- 中间单课正文由 `beforeProcess -> renderProcessSection -> afterProcess` 组成。",
                "- `beforeProcess` 包含本课依据、学情分析、教学目标、教学重难点、教学准备。",
                "- `renderProcessSection(view, \"六\")` 对应教学过程，是本轮唯一绑定槽位。",
                "- `afterProcess` 包含学习单与评价、课堂后记。",
                "",
                "## 本轮绑定",
                "",
                "- 复制原 R91A 壳层页。",
                "- 不替换 `#renderLayer`。",
                "- 不替换 `current_lesson.sections`。",
                "- 仅用 R93-P6 的 5 个 episode 替换 `current_lesson.process_steps`。",
                "- 同步修补 R21 unified package 的 `lesson.process_steps`，因为它是页面加载后的最终覆盖层。",
                "- 同步修补 R21 `normalizeProcessSteps()`，让 P6 episode 不被压扁成旧的普通流程字段。",
                "- 原壳的 `renderPrepRoomCanvas()` 负责重新渲染页面。",
                "",
                "## 必须保留的章节",
                "",
                *[f"- `{item}`" for item in preserved],
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    DEMOTE_OUT.write_text(
        "\n".join(
            [
                "# 上一版 R97A 降级决定",
                "",
                "上一版 `1013R_R97A_R91A_SHELL_COPY_BINDING_PREVIEW_FROM_R93_P6` 应降级为 `FAIL_AS_SLOT_BINDING`。",
                "",
                "原因：它把 P6 当作中间主舞台整页内容接入，破坏了原备课本正文的章节层级。",
                "",
                "正确边界：P6 只对应 `六、教学过程`，不能覆盖 `本课依据`、`学情分析`、`教学目标`、`教学重难点`、`教学准备`、`学习单与评价` 和 `课堂后记`。",
                "",
                "本轮 R97A2 仅做复制页修复，不改原 R91A/R87 文件，不 formal apply。",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    html = HTML_OUT.read_text(encoding="utf-8")
    r21_package_sections_count = 0
    r21_package_process_has_p6 = False
    try:
        script_start = html.find(R21_DATA_SCRIPT_MARKER)
        json_start = html.find(">", script_start) + 1
        json_end = html.find("</script>", json_start)
        r21_pkg = json.loads(html[json_start:json_end])
        r21_lesson = r21_pkg.get("lesson", {})
        r21_package_sections_count = len(r21_lesson.get("sections", []))
        r21_package_process_has_p6 = all("p6" in item and "p6_episode_id" in item for item in r21_lesson.get("process_steps", []))
    except Exception:
        pass
    checks = {
        "html_created": HTML_OUT.exists(),
        "source_shell_exists": SHELL_SOURCE.exists(),
        "p6_viewmodel_exists": P6_VIEWMODEL.exists(),
        "render_layer_preserved": 'id="renderLayer"' in html,
        "topbar_preserved": 'class="topbar"' in html,
        "context_bar_preserved": 'class="context-bar"' in html,
        "bottom_xiaojiao_preserved": "xiaobei-chat-entry" in html,
        "left_tree_renderer_preserved": "function renderPrepNotebookTree" in html,
        "lesson_section_renderer_preserved": "function renderLessonSection" in html,
        "process_section_renderer_preserved": "function renderProcessSection" in html,
        "courseware_rail_preserved": "courseware-rail" in html,
        "r21_anchor_script_preserved": "data-r21-route-anchor" in html,
        "slot_binding_marker_present": "data-1013r-r97a2-slot-binding" in html,
        "target_process_steps_only": '"p6_episode_id"' in html and '"target_slot": "model.views.prepNotebook.current_lesson.process_steps"' in html,
        "sections_preserved_by_patch": "lesson.sections = existingSections" in html,
        "r21_package_process_steps_patched": r21_package_process_has_p6 is True,
        "r21_package_sections_still_present": r21_package_sections_count >= 7,
        "r21_normalize_preserves_p6": "if (step && step.p6)" in html and "p6_episode_id: step.p6_episode_id" in html,
        "p6_renderer_present": "r97a2-p6-step" in html and "老师三步" in html and "学生产出" in html,
        "previous_whole_render_replacement_absent": "R97A_SHELL_COPY_BINDING_PREVIEW_FROM_R93_P6" not in html,
        "teacher_review_required": slot_vm["teacher_review_required"] is True,
        "formal_apply_false": slot_vm["formal_apply"] is False,
        "episode_count": len(slot_vm["episodes"]) == 5,
    }
    blocking = [name for name, ok in checks.items() if ok is not True]
    validator = {
        "stage": "1013R_R97A2_PREP_NOTEBOOK_TEACHING_PROCESS_SLOT_BINDING_REPAIR",
        "status": "PASS" if not blocking else "FAIL",
        "blocking": blocking,
        "source_shell": str(SHELL_SOURCE),
        "output_html": str(HTML_OUT),
        "output_sha256": sha256(HTML_OUT),
        "checks": checks,
        "boundary": {
            "source_shell_modified": False,
            "copy_created": True,
            "replace_render_layer": False,
            "replace_full_prep_notebook": False,
            "target_slot": "current_lesson.process_steps",
            "formal_apply": False,
            "database_written": False,
            "feishu_written": False,
            "memory_written": False,
            "r21_core_modified": False,
            "r36_core_modified": False,
            "copied_shell_r21_package_process_steps_patched": True,
            "copied_shell_r21_normalize_adapter_patched": True,
            "copied_shell_r36_adapter_patched": False,
            "real_ui_runtime_connected": False,
        },
    }
    VALIDATOR_OUT.write_text(json.dumps(validator, ensure_ascii=False, indent=2), encoding="utf-8")

    README_OUT.write_text(
        "\n".join(
            [
                "# 1013R_R97A2_PREP_NOTEBOOK_TEACHING_PROCESS_SLOT_BINDING_REPAIR",
                "",
                "本轮修复上一版壳层接入粒度错误：P6 教师导航内容只接入原备课本 `六、教学过程` 槽位。",
                "",
                "## 输出",
                "",
                f"- `{HTML_OUT.name}`",
                f"- `{VIEWMODEL_OUT.name}`",
                f"- `{AUDIT_OUT.name}`",
                f"- `{DEMOTE_OUT.name}`",
                f"- `{VALIDATOR_OUT.name}`",
                "- `r97a2_visual_slot_smoke.md`",
                "- `R91A_slot_binding_dom_dump.html`",
                "- `R91A_slot_binding_from_R93_P6_screenshot.png`",
                "- `R91A_slot_binding_teaching_process_section_screenshot.png`",
                "",
                "## 边界",
                "",
                "- 不改原 R91A/R87 壳层源文件。",
                "- 不替换整页 `#renderLayer`。",
                "- 不覆盖单课正文其他章节。",
                "- 复制页内适配 R21 最终覆盖层；不修改原 R21/R36 合同或源文件。",
                "- 不 formal apply，不写数据库/飞书/记忆，不改 R21/R36。",
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
