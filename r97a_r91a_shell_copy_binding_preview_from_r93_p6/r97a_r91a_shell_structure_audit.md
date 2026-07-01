# R97A R91A Shell Structure Audit

Source shell:

```text
outputs\PREP_ROOM_RENDER_CANVAS_DEEPEN_V1\1013R_R91A_STATIC_PAGE_BACKFILL\R91A_static_page_backfill_from_R39_product_candidate_preview.html
sha256=db101cc33f01d3fb2683ef6a019abae62f8da4c1851a8fc1830f9c389ccd44bc
size=1110210
```

Structural landmarks:

| Check | Present |
| --- | --- |
| has_topbar | true |
| has_context_bar | true |
| has_workspace | true |
| has_canvas_stage | true |
| has_render_layer | true |
| has_bottom_xiaojiao_entry | true |
| has_status_strip | true |
| has_prep_room_view_model | true |
| has_init_function | true |
| has_r91a_backfill_panel | true |

Binding decision:

```text
Use R91A as the authoritative shell copy.
Do not modify the original file.
Mount the P6 teacher navigation payload into #renderLayer in the copied shell.
Preserve topbar, context bar, canvas stage, bottom Xiaojiao input, and status strip.
Hide old R39/R91A backfill audit panels inside the copy so the teacher first screen is not polluted.
```
