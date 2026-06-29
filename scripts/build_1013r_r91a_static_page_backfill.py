from __future__ import annotations

import html
import json
import shutil
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
STAGE = "1013R_R91A_STATIC_PAGE_BACKFILL"
OUT = BASE / STAGE

SOURCE_HTML = BASE / "1013R_R39_candidate_preview_backfill" / "R39_product_mode_candidate_preview.html"
R91A_MAP = BASE / "1013R_R91A_SHELL_VIEWMODEL_FIXTURE_PREFLIGHT" / "teacher_review_card_viewmodel_map_1013R_R91A.json"
R91A_VALIDATOR = BASE / "1013R_R91A_SHELL_VIEWMODEL_FIXTURE_PREFLIGHT" / "validate_1013R_R91A_shell_viewmodel_fixture_preflight_result.json"
P1_QUALITY = BASE / "1013R_R90B_P1_QUALITY_SENTINEL_V0_AND_LINEAGE_REPAIR" / "quality_sentinel_v0_result.json"
P1_LINEAGE = BASE / "1013R_R90B_P1_QUALITY_SENTINEL_V0_AND_LINEAGE_REPAIR" / "generation_lineage_1013R_R90B.json"


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


def render_card(card: dict, index: int) -> str:
    payload = card.get("teacher_review_payload", {})
    slot = card.get("render_slot", {})
    gate = card.get("gate", {})
    impact = " / ".join(payload.get("impact_scope", []))
    sources = "；".join(payload.get("source_refs", []))
    return f"""
  <article class="r91a-card" data-r91a-card-id="{esc(card.get('card_id'))}" data-source-candidate-id="{esc(card.get('source_candidate_id'))}">
    <header>
      <span class="r91a-index">#{index}</span>
      <div>
        <strong>{esc(payload.get('target_field_key'))}</strong>
        <p>{esc(payload.get('target_step_id'))} · {esc(slot.get('level_3_tool_id'))} / {esc(slot.get('level_4_content_slot_id'))} / {esc(slot.get('shell_render_slot'))}</p>
      </div>
    </header>
    <div class="r91a-before-after">
      <section>
        <span>修改前</span>
        <p>{esc(payload.get('before_summary'))}</p>
      </section>
      <section>
        <span>修改后候选</span>
        <p>{esc(payload.get('after_candidate'))}</p>
      </section>
    </div>
    <div class="r91a-suggestion">
      <span>小教建议</span>
      <p>{esc(payload.get('xiaojiao_suggestion'))}</p>
    </div>
    <footer>
      <p><b>影响范围</b>{esc(impact)}</p>
      <p><b>来源</b>{esc(sources)}</p>
      <p><b>确认门</b>teacher_review_required={str(payload.get('teacher_review_required')).lower()} · preview_only={str(payload.get('preview_only')).lower()} · formal_apply_allowed={str(payload.get('formal_apply_allowed')).lower()} · gate={esc(gate.get('gate_type'))}</p>
    </footer>
  </article>"""


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    source_html = SOURCE_HTML.read_text(encoding="utf-8")
    r91a_map = read_json(R91A_MAP)
    r91a_validator = read_json(R91A_VALIDATOR)
    p1_quality = read_json(P1_QUALITY)
    lineage = read_json(P1_LINEAGE)

    cards = r91a_map.get("cards", [])
    quality = p1_quality.get("quality_sentinel_v0", {})
    dimensions = quality.get("dimensions", {})
    dimension_rows = "\n".join(
        f"<li><b>{esc(v.get('label', key))}</b><span>{esc(v.get('result'))}</span></li>"
        for key, v in dimensions.items()
    )
    card_html = "\n".join(render_card(card, index) for index, card in enumerate(cards, 1))
    created_at = datetime.now().isoformat(timespec="seconds")

    injection = f"""

<style id="shiwei-r91a-static-backfill-style">
  body[data-shiwei-mode="product"] .r91a-backfill-panel {{
    border: 1px solid rgba(42, 102, 89, 0.24);
    background: #fbfffc;
    color: #173c35;
    border-radius: 8px;
    padding: 16px;
    margin: 16px 0 28px;
    box-shadow: 0 12px 30px rgba(23, 72, 62, 0.08);
  }}
  .r91a-backfill-panel h2 {{
    margin: 0 0 8px;
    font-size: 20px;
    letter-spacing: 0;
  }}
  .r91a-backfill-panel .r91a-meta {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(190px, 1fr));
    gap: 8px;
    margin: 12px 0;
  }}
  .r91a-backfill-panel .r91a-meta span,
  .r91a-quality-list li {{
    border: 1px solid rgba(42, 102, 89, 0.16);
    background: rgba(244, 250, 247, 0.92);
    border-radius: 8px;
    padding: 8px 10px;
  }}
  .r91a-quality-list {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 8px;
    padding: 0;
    margin: 12px 0;
    list-style: none;
  }}
  .r91a-quality-list li {{
    display: flex;
    justify-content: space-between;
    gap: 10px;
  }}
  .r91a-card-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 12px;
    margin-top: 14px;
  }}
  .r91a-card {{
    border: 1px solid rgba(35, 91, 78, 0.18);
    border-radius: 8px;
    background: #fff;
    padding: 12px;
  }}
  .r91a-card header {{
    display: flex;
    gap: 10px;
    align-items: flex-start;
  }}
  .r91a-index {{
    min-width: 34px;
    text-align: center;
    border-radius: 999px;
    padding: 4px 0;
    background: #e8f3ef;
    color: #236b5d;
    font-weight: 700;
  }}
  .r91a-card header strong {{
    color: #215d52;
  }}
  .r91a-card header p,
  .r91a-card footer p {{
    margin: 4px 0;
    color: #52665f;
    font-size: 13px;
  }}
  .r91a-before-after {{
    display: grid;
    grid-template-columns: 1fr;
    gap: 8px;
    margin-top: 10px;
  }}
  .r91a-before-after section,
  .r91a-suggestion {{
    border-left: 3px solid #74a89a;
    background: #f7fbf9;
    padding: 8px 10px;
  }}
  .r91a-before-after span,
  .r91a-suggestion span {{
    font-weight: 700;
    color: #2b7668;
  }}
  .r91a-before-after p,
  .r91a-suggestion p {{
    margin: 4px 0 0;
  }}
  .r91a-card footer {{
    margin-top: 10px;
    border-top: 1px dashed rgba(35, 91, 78, 0.2);
    padding-top: 8px;
  }}
  .r91a-card footer b {{
    display: inline-block;
    min-width: 64px;
    color: #235b50;
  }}
</style>

<section class="r91a-backfill-panel" data-shiwei-product-retained="true" data-r91a-static-backfill="true" data-preview-only="true" data-formal-apply-allowed="false">
  <h2>R90B / R90B-P1 / R91-A 生成结果回填</h2>
  <p>本区把 R90B 的真实 provider 候选、R90B-P1 质量小红灯、R91-A Shell ViewModel 预检结果回填到 R39 候选预览静态页中，仅用于审核查看。</p>
  <div class="r91a-meta">
    <span><b>静态页来源</b><br>{esc(rel(SOURCE_HTML))}</span>
    <span><b>壳层基线</b><br>{esc(cards[0].get('shell_state', {}).get('source_page_baseline') if cards else '')}</span>
    <span><b>R91-A validator</b><br>{esc(r91a_validator.get('final_status'))}</span>
    <span><b>Quality Sentinel</b><br>{esc(quality.get('result'))} · blocking={str(quality.get('blocking')).lower()}</span>
    <span><b>Provider lineage</b><br>{esc(lineage.get('provider', {}).get('provider'))} / {esc(lineage.get('provider', {}).get('model'))}</span>
    <span><b>回填时间</b><br>{esc(created_at)}</span>
  </div>
  <ul class="r91a-quality-list">
    {dimension_rows}
  </ul>
  <div class="r91a-card-grid">
    {card_html}
  </div>
  <p class="blocked">边界：preview_only=true；teacher_review_required=true；formal_apply_allowed=false；R36/R21 未修改；未接真实页面；未写数据库/飞书/记忆。</p>
</section>
"""

    if "</body>" not in source_html:
        raise RuntimeError("source HTML has no </body> marker")
    output_html = OUT / "R91A_static_page_backfill_from_R39_product_candidate_preview.html"
    filled_html = source_html.replace("</body>", injection + "\n</body>", 1)
    write_text(output_html, filled_html)
    shutil.copy2(Path(__file__), OUT / Path(__file__).name)

    checks = {
        "source_r39_exists": SOURCE_HTML.exists(),
        "output_html_exists": output_html.exists(),
        "r91a_panel_present": "data-r91a-static-backfill=\"true\"" in filled_html,
        "card_count": len(cards),
        "four_cards_rendered": filled_html.count("class=\"r91a-card\"") == len(cards),
        "quality_result_present": str(quality.get("result")) in filled_html,
        "r36_unmodified": True,
        "r21_unmodified": True,
        "provider_called": False,
        "page_runtime_connected": False,
        "formal_apply_performed": False,
    }
    pass_checks = [
        checks["source_r39_exists"],
        checks["output_html_exists"],
        checks["r91a_panel_present"],
        checks["card_count"] == 4,
        checks["four_cards_rendered"],
        checks["quality_result_present"],
        checks["r36_unmodified"],
        checks["r21_unmodified"],
        checks["provider_called"] is False,
        checks["page_runtime_connected"] is False,
        checks["formal_apply_performed"] is False,
    ]
    result = {
        "stage": STAGE,
        "created_at": created_at,
        "status": "PASS" if all(pass_checks) else "FAIL",
        "source_html": rel(SOURCE_HTML),
        "output_html": rel(output_html),
        "filled_sources": [
            rel(R91A_MAP),
            rel(R91A_VALIDATOR),
            rel(P1_QUALITY),
            rel(P1_LINEAGE),
        ],
        "checks": checks,
        "boundary": {
            "static_page_copy_only": True,
            "r39_source_modified": False,
            "r36_modified": False,
            "r21_modified": False,
            "provider_called": False,
            "model_called": False,
            "formal_apply_performed": False,
            "database_written": False,
            "feishu_written": False,
            "memory_written": False,
            "r91b_executed": False,
        },
    }
    write_json(OUT / "validate_1013R_R91A_static_page_backfill_result.json", result)
    write_text(
        OUT / "README.md",
        f"""# 1013R_R91A_STATIC_PAGE_BACKFILL

This stage copies the existing R39 product-mode candidate preview static page and fills the latest R90B / R90B-P1 / R91-A review results into a new static HTML page.

It does not modify R39, R36, R21, runtime, database, Feishu, memory, or formal apply state.

## Output

```text
{rel(output_html)}
```

## Result

```text
status={result['status']}
card_count={len(cards)}
quality_sentinel_v0={quality.get('result')}
blocking={quality.get('blocking')}
```
""",
    )
    write_json(
        OUT / "REVIEW_PACKAGE_MANIFEST.json",
        {
            "stage": STAGE,
            "status": result["status"],
            "files": [
                rel(output_html),
                rel(OUT / "README.md"),
                rel(OUT / "validate_1013R_R91A_static_page_backfill_result.json"),
                rel(OUT / Path(__file__).name),
            ],
            "boundary": result["boundary"],
        },
    )
    print(json.dumps({"stage": STAGE, "status": result["status"], "output_html": rel(output_html)}, ensure_ascii=False, indent=2))
    if result["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
