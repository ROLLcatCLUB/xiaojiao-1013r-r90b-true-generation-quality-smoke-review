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
STAGE = "1013R_R91A_R88_FIELD_LAB_CURRENT_BACKFILL"
OUT = BASE / STAGE

R88_DIR = BASE / "1013R_R88_FIELD_GENERATION_QUALITY_STATIC_LAB"
R88_HTML = R88_DIR / "field_generation_quality_static_lab_1013R_R88.html"
R88_LEDGER = R88_DIR / "field_generation_quality_static_lab_ledger_1013R_R88.json"
R90A_DIR = BASE / "1013R_R90A_TRUE_GENERATION_CONTRACT_AND_PROFILE_PREFLIGHT"
R90A_PROFILE = R90A_DIR / "r90a_art_lesson_design_profile_manifest_1013R_R90A.json"
R90A_COVERAGE = R90A_DIR / "r90a_r88_step_field_activation_coverage_audit_1013R_R90A.json"
R90B_DIR = BASE / "1013R_R90B_TRUE_GENERATION_QUALITY_SMOKE_V1"
R90B_CANDIDATES = R90B_DIR / "normalized_candidates.json"
P1_DIR = BASE / "1013R_R90B_P1_QUALITY_SENTINEL_V0_AND_LINEAGE_REPAIR"
P1_QUALITY = P1_DIR / "quality_sentinel_v0_result.json"
P1_LINEAGE = P1_DIR / "generation_lineage_1013R_R90B.json"
R91A_DIR = BASE / "1013R_R91A_SHELL_VIEWMODEL_FIXTURE_PREFLIGHT"
R91A_MAP = R91A_DIR / "teacher_review_card_viewmodel_map_1013R_R91A.json"
R91A_VALIDATOR = R91A_DIR / "validate_1013R_R91A_shell_viewmodel_fixture_preflight_result.json"

OUTPUT_HTML = OUT / "field_generation_quality_static_lab_1013R_R88_current_backfill.html"

R91B_TARGETS = {
    "observation_inquiry": [
        "lesson.classroom_flow.step.teacher_probe_question",
        "lesson.classroom_flow.step.student_observation",
        "lesson.classroom_flow.step.visual_language_focus",
    ],
    "teacher_demo": [
        "lesson.classroom_flow.step.teacher_demo",
        "lesson.classroom_flow.step.teacher_modeling_language",
        "lesson.classroom_flow.step.technique_focus",
    ],
    "student_creation": [
        "lesson.classroom_flow.step.student_creation",
        "lesson.classroom_flow.step.task_scaffold",
        "lesson.classroom_flow.step.success_criteria",
    ],
}


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT)).replace("/", "\\")


def esc(value: object) -> str:
    return html.escape("" if value is None else str(value), quote=True)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def field_key_from_candidate(candidate: dict) -> str:
    return str(candidate.get("target_field_key", ""))


def slot_id_for_key(key: str) -> str:
    return f"R88-GEN/{key}"


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
                end = match.end()
                return doc[:start] + new_block + doc[end:], True
    return doc, False


def render_filled_placeholder(candidate: dict, card: dict, dimension_note: str) -> str:
    payload = card.get("teacher_review_payload", {})
    slot = candidate.get("target_line_contract_id")
    return f"""
      <div class="placeholder r91a-current-filled" data-generation-slot-id="{esc(slot)}" data-r90b-provider-candidate="{esc(candidate.get('field_patch_id'))}" data-r91a-card-id="{esc(card.get('card_id'))}" data-preview-only="true" data-formal-apply-allowed="false">
        <div class="placeholder-title">R90B 已生成候选 · R91A 已映射 TeacherReviewCard</div>
        <div class="r91a-field-status">
          <span>target_step={esc(candidate.get('target_step_id'))}</span>
          <span>destination={esc(candidate.get('target_destination'))}</span>
          <span>preview_only=true</span>
          <span>formal_apply_allowed=false</span>
        </div>
        <div class="r91a-before-after">
          <section><strong>修改前</strong><p>{esc(candidate.get('before_summary'))}</p></section>
          <section><strong>修改后候选</strong><p>{esc(candidate.get('after_candidate'))}</p></section>
        </div>
        <div class="r91a-suggestion"><strong>小教建议</strong><p>{esc(candidate.get('xiaojiao_suggestion'))}</p></div>
        <div class="r91a-review-foot">
          <p><b>质量提示</b>{esc(dimension_note)}</p>
          <p><b>影响范围</b>{esc(' / '.join(candidate.get('impact_scope', [])))}</p>
          <p><b>审阅卡</b>{esc(card.get('component'))} · {esc(card.get('render_slot', {}).get('level_3_tool_id'))} / {esc(card.get('render_slot', {}).get('level_4_content_slot_id'))} / {esc(card.get('render_slot', {}).get('shell_render_slot'))}</p>
        </div>
      </div>
"""


def render_current_context_section(profile: dict, ledger: dict, coverage: dict, quality: dict, r91a_validator: dict, filled_count: int) -> str:
    status_counts = coverage.get("status_counts", {})
    q = quality.get("quality_sentinel_v0", {})
    dims = q.get("dimensions", {})
    dimension_items = "\n".join(
        f"<li><b>{esc(v.get('label', key))}</b><span>{esc(v.get('result'))}</span></li>"
        for key, v in dims.items()
    )
    r91b_rows = []
    coverage_by_key = {row.get("engineering_key"): row for row in coverage.get("rows", [])}
    for step_type, keys in R91B_TARGETS.items():
        for key in keys:
            row = coverage_by_key.get(key, {})
            r91b_rows.append(
                f"<tr><td>{esc(step_type)}</td><td>{esc(key)}</td><td>{esc(row.get('visible_label'))}</td><td>{esc(row.get('coverage_status'))}</td></tr>"
            )
    return f"""
      <section class="section r91a-current-context" id="current-backfill">
        <h2>当前闭环回填 · R90B / P1 / R91A</h2>
        <p class="section-note">本页保留 R88 的 83 个字段槽位，并把已经真实生成和通过壳层预检的 4 个候选回填到对应 `R88-GEN/...` 槽位。R91B 的 9 个目标字段只做预备标记，本轮不调用 provider。</p>
        <div class="r91a-summary-grid">
          <div><strong>active profile</strong><span>{esc(profile.get('profile_id'))}@{esc(profile.get('profile_version'))}</span></div>
          <div><strong>candidate contract</strong><span>{esc(profile.get('candidate_contract_version'))}</span></div>
          <div><strong>R88 fields</strong><span>{len(ledger.get('big_unit_fields', []))} + {len(ledger.get('lesson_fields', []))} + {len(ledger.get('step_contract_fields', []))} = {profile.get('field_counts', {}).get('total_profile_fields')}</span></div>
          <div><strong>R90 active rows</strong><span>{esc(status_counts.get('activated_in_r90'))}</span></div>
          <div><strong>filled candidates</strong><span>{filled_count}</span></div>
          <div><strong>quality sentinel</strong><span>{esc(q.get('result'))} · blocking={str(q.get('blocking')).lower()}</span></div>
          <div><strong>R91A validator</strong><span>{esc(r91a_validator.get('final_status'))}</span></div>
          <div><strong>boundary</strong><span>static copy only · no R36/R21 edit</span></div>
        </div>
        <ul class="r91a-quality-dimensions">
          {dimension_items}
        </ul>
        <h3>R91B 预备目标字段</h3>
        <table class="r91a-target-table">
          <thead><tr><th>step_type</th><th>target_field_key</th><th>页面字段名</th><th>R90A 覆盖状态</th></tr></thead>
          <tbody>{''.join(r91b_rows)}</tbody>
        </table>
      </section>
"""


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)

    source_html = R88_HTML.read_text(encoding="utf-8")
    ledger = read_json(R88_LEDGER)
    profile = read_json(R90A_PROFILE)
    coverage = read_json(R90A_COVERAGE)
    candidates_payload = read_json(R90B_CANDIDATES)
    quality = read_json(P1_QUALITY)
    lineage = read_json(P1_LINEAGE)
    r91a_map = read_json(R91A_MAP)
    r91a_validator = read_json(R91A_VALIDATOR)

    html_slots = set(re.findall(r'data-generation-slot-id="([^"]+)"', source_html))
    html_engineering_keys = set(re.findall(r'data-engineering-key="([^"]+)"', source_html))
    ledger_big = [x["engineering_key"] for x in ledger.get("big_unit_fields", [])]
    ledger_lesson = [x["engineering_key"] for x in ledger.get("lesson_fields", [])]
    ledger_step = [x["engineering_key"] for x in ledger.get("step_contract_fields", [])]
    ledger_slots = {slot_id_for_key(key) for key in ledger_big + ledger_lesson + ledger_step}

    errors: list[str] = []
    if html_slots != ledger_slots:
        errors.append("html_generation_slots_do_not_match_r88_ledger")
    if html_engineering_keys != set(ledger_big + ledger_lesson):
        errors.append("html_big_lesson_cards_do_not_match_r88_ledger")
    expected_counts = profile.get("field_counts", {})
    if len(ledger_big) != expected_counts.get("big_unit_fields"):
        errors.append("big_unit_field_count_mismatch")
    if len(ledger_lesson) != expected_counts.get("lesson_fields"):
        errors.append("lesson_field_count_mismatch")
    if len(ledger_step) != expected_counts.get("step_contract_fields"):
        errors.append("step_contract_field_count_mismatch")

    candidates = candidates_payload.get("field_patch_candidates", [])
    cards = r91a_map.get("cards", [])
    cards_by_candidate = {card.get("source_candidate_id"): card for card in cards}
    target_fields = {field_key_from_candidate(candidate) for candidate in candidates}
    for candidate in candidates:
        cid = candidate.get("field_patch_id")
        slot = candidate.get("target_line_contract_id")
        if slot not in html_slots:
            errors.append(f"candidate_slot_missing:{cid}:{slot}")
        if cid not in cards_by_candidate:
            errors.append(f"r91a_card_missing:{cid}")
        if candidate.get("target_destination") != "existing_edit_card_before_after_suggestion_panel":
            errors.append(f"candidate_destination_mismatch:{cid}")
        if candidate.get("preview_only") is not True or candidate.get("formal_apply_allowed") is not False:
            errors.append(f"candidate_boundary_mismatch:{cid}")

    q = quality.get("quality_sentinel_v0", {})
    if q.get("blocking") is not False:
        errors.append("quality_sentinel_blocking_not_false")
    if q.get("result") not in {"BASIC_USABLE", "NEEDS_RETRY"}:
        errors.append(f"quality_sentinel_result_not_allowed:{q.get('result')}")
    if r91a_validator.get("status") != "PASS":
        errors.append("r91a_validator_not_pass")

    result_path = OUT / "validate_1013R_R91A_R88_field_lab_current_backfill_result.json"
    if errors:
        write_json(result_path, {"stage": STAGE, "status": "FAIL", "errors": errors})
        raise SystemExit(1)

    css = """
  <style id="shiwei-r91a-r88-current-backfill-style">
    .nav-link.current-backfill-link { border-color: #1b5d52; background: #e8f6f1; }
    .r91a-current-context {
      border-color: #9bcdbf;
      background: linear-gradient(180deg, #fbfffc, #f3faf6);
    }
    .section-note { color: var(--muted); margin-top: -6px; }
    .r91a-summary-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(190px, 1fr));
      gap: 10px;
      margin: 14px 0;
    }
    .r91a-summary-grid div {
      border: 1px solid rgba(45, 127, 114, .18);
      background: #fff;
      border-radius: 8px;
      padding: 10px 12px;
    }
    .r91a-summary-grid strong,
    .r91a-summary-grid span { display: block; }
    .r91a-summary-grid strong { color: var(--green-dark); font-size: 12px; text-transform: uppercase; }
    .r91a-summary-grid span { color: var(--ink); margin-top: 4px; font-weight: 700; }
    .r91a-quality-dimensions {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
      gap: 8px;
      list-style: none;
      padding: 0;
      margin: 14px 0;
    }
    .r91a-quality-dimensions li {
      border: 1px solid rgba(201, 117, 25, .22);
      background: #fffaf2;
      border-radius: 8px;
      padding: 9px 10px;
      display: flex;
      justify-content: space-between;
      gap: 8px;
    }
    .r91a-target-table {
      width: 100%;
      border-collapse: collapse;
      background: #fff;
      border: 1px solid var(--line);
      border-radius: 8px;
      overflow: hidden;
    }
    .r91a-target-table th,
    .r91a-target-table td {
      border-bottom: 1px solid var(--line);
      padding: 8px 10px;
      text-align: left;
      vertical-align: top;
      font-size: 13px;
    }
    .r91a-target-table th { color: var(--green-dark); background: #eef9f5; }
    .placeholder.r91a-current-filled {
      border-color: #7fbdad;
      background: #fbfffc;
    }
    .placeholder.r91a-current-filled .placeholder-title {
      color: var(--green-dark);
      font-weight: 800;
    }
    .r91a-field-status {
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      margin: 8px 0;
    }
    .r91a-field-status span {
      border: 1px solid rgba(45, 127, 114, .18);
      border-radius: 999px;
      background: #eef9f5;
      color: var(--green-dark);
      padding: 3px 8px;
      font-size: 12px;
      font-weight: 700;
    }
    .r91a-before-after {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 8px;
      margin: 8px 0;
    }
    .r91a-before-after section,
    .r91a-suggestion,
    .r91a-review-foot {
      border-left: 3px solid #7fbdad;
      background: #fff;
      padding: 8px 10px;
    }
    .r91a-before-after p,
    .r91a-suggestion p,
    .r91a-review-foot p { margin: 4px 0; }
    .r91a-review-foot b {
      display: inline-block;
      min-width: 66px;
      color: var(--green-dark);
    }
  </style>
"""
    doc = source_html.replace(
        "<title>1013R R88 字段生成质量静态验证页</title>",
        "<title>1013R R88 字段生成质量静态验证页 · 当前回填</title>",
    )
    doc = doc.replace("</head>", css + "\n</head>")
    doc = doc.replace(
        '<a class="nav-link" href="#quality">质量观察</a>',
        '<a class="nav-link current-backfill-link" href="#current-backfill">当前回填</a>\n        <a class="nav-link" href="#quality">质量观察</a>',
    )

    dimension_note = "R90B-P1: " + str(q.get("result")) + " / blocking=" + str(q.get("blocking")).lower()
    filled_count = 0
    for candidate in candidates:
        card = cards_by_candidate[candidate.get("field_patch_id")]
        block = render_filled_placeholder(candidate, card, dimension_note)
        doc, replaced = replace_placeholder_block(doc, candidate["target_line_contract_id"], block)
        if replaced:
            filled_count += 1
        else:
            errors.append(f"placeholder_replace_failed:{candidate['target_line_contract_id']}")

    context_section = render_current_context_section(profile, ledger, coverage, quality, r91a_validator, filled_count)
    doc = doc.replace('<section class="section" id="quality">', context_section + '\n      <section class="section" id="quality">')

    write_text(OUTPUT_HTML, doc)
    shutil.copy2(Path(__file__), OUT / Path(__file__).name)

    validation = {
        "stage": STAGE,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "status": "PASS" if not errors and filled_count == len(candidates) else "FAIL",
        "source_html": rel(R88_HTML),
        "output_html": rel(OUTPUT_HTML),
        "field_match": {
            "html_generation_slot_count": len(html_slots),
            "ledger_slot_count": len(ledger_slots),
            "profile_total_field_count": expected_counts.get("total_profile_fields"),
            "missing_slots": sorted(ledger_slots - html_slots),
            "extra_slots": sorted(html_slots - ledger_slots),
            "big_unit_field_count": len(ledger_big),
            "lesson_field_count": len(ledger_lesson),
            "step_contract_field_count": len(ledger_step),
            "matches_current_profile": len(html_slots) == expected_counts.get("total_profile_fields") and html_slots == ledger_slots,
        },
        "current_backfill": {
            "r90b_candidate_count": len(candidates),
            "r91a_card_count": len(cards),
            "filled_slot_count": filled_count,
            "target_fields": sorted(target_fields),
            "quality_sentinel_v0_result": q.get("result"),
            "quality_sentinel_v0_blocking": q.get("blocking"),
            "r91b_reserved_target_count": sum(len(v) for v in R91B_TARGETS.values()),
        },
        "provider_lineage": {
            "provider": lineage.get("provider", {}).get("provider"),
            "model": lineage.get("provider", {}).get("model"),
            "source_provider_call_round": lineage.get("provider", {}).get("source_provider_call_round"),
            "provider_called_in_this_round": False,
        },
        "errors": errors,
        "boundary": {
            "static_copy_only": True,
            "source_r88_modified": False,
            "r36_modified": False,
            "r21_modified": False,
            "provider_called": False,
            "model_called": False,
            "database_written": False,
            "feishu_written": False,
            "memory_written": False,
            "formal_apply_performed": False,
            "r91b_executed": False,
        },
    }
    write_json(result_path, validation)

    readme = f"""# 1013R_R91A_R88_FIELD_LAB_CURRENT_BACKFILL

This stage copies the original R88 field generation quality static lab and adapts it to the current frozen profile plus R90B/P1/R91A results.

## Answer

The original R88 page matches the current frozen field system structurally:

```text
big_unit_fields=22
lesson_fields=14
step_contract_fields=47
total_profile_fields=83
html_generation_slots=83
missing_slots=0
extra_slots=0
```

It did not yet match the current generated content because R90B provider candidates, R90B-P1 quality sentinel, and R91A TeacherReviewCard mapping were not filled into the corresponding R88 slots.

## Output

```text
{rel(OUTPUT_HTML)}
```

## Boundary

```text
source_r88_modified=false
r36_modified=false
r21_modified=false
provider_called=false
formal_apply_performed=false
r91b_executed=false
```
"""
    write_text(OUT / "README.md", readme)
    manifest = {
        "stage": STAGE,
        "status": validation["status"],
        "files": [
            rel(OUTPUT_HTML),
            rel(result_path),
            rel(OUT / "README.md"),
            rel(OUT / Path(__file__).name),
        ],
        "output_html_sha256": sha256(OUTPUT_HTML),
        "boundary": validation["boundary"],
    }
    write_json(OUT / "REVIEW_PACKAGE_MANIFEST.json", manifest)
    print(json.dumps({
        "stage": STAGE,
        "status": validation["status"],
        "output_html": rel(OUTPUT_HTML),
        "output_html_sha256": manifest["output_html_sha256"],
    }, ensure_ascii=False, indent=2))
    if validation["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
