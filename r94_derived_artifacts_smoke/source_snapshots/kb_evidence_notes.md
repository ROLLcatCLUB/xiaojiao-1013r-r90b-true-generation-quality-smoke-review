# Knowledge Base Evidence Notes - R93-P2

P2 scanned the existing project knowledge base before closing the textbook anchor.

| Evidence | Kind | Role | Exists | Note |
| --- | --- | --- | --- | --- |
| `kb_art_g3_textbook_images_20260427` | knowledge_base_textbook_image_index | `anchor_supporting_index_not_ocr` | true | 教材图片包已入库登记；该文件明示尚未完成 OCR，不能单独作为教材原文引用。 |
| `kb_art_g3_lesson_case_lesson_8974535734` | teacher_local_lesson_plan | `pedagogical_reference_not_current_textbook_anchor` | true | 三年级下册本地备课资料，含渐变单元目标、材料与评价维度；单元名为第一单元《多变的色彩》，与当前教材页锚点不一致，只作教学组织参考。 |
| `kb_art_g3_lesson_case_1_fd1b5bdf60` | teacher_local_lesson_plan | `pedagogical_reference_not_current_textbook_anchor` | true | 课时1《渐变的魅力》本地教案，提供导入、工具示范、学习单和评价参考；不覆盖当前第1课《色彩的渐变》教材事实。 |
| `kb_art_g3_lesson_case_2_07e719a809` | teacher_local_lesson_plan | `pedagogical_reference_not_current_textbook_anchor` | true | 课时2《颜料的渐变》本地教案，提供水粉调色与材料组织参考；不覆盖当前教材锚点。 |
| `kb_art_g3_lesson_case_3_2eaf570678` | teacher_local_lesson_plan | `pedagogical_reference_not_current_textbook_anchor` | true | 课时3《渐变的节奏》本地教案，提供后续课衔接参考；当前教材页显示《渐变的节奏》为第二单元第2课。 |
| `lesson_plan_import_20260427` | knowledge_base_import_index | `lineage_index` | true | 知识库导入索引，记录三年级下册本地教案来源和复制路径；用于 lineage，不作为教材正文证据。 |
| `knowledge_base_items_manifest` | knowledge_base_manifest | `lineage_manifest` | true | 知识库条目清单，记录教材图片包与本地教案条目状态；用于 source lineage。 |

## Decision

```text
Use current textbook page images as the only current textbook-fact anchor.
Use knowledge-base textbook image index as lineage support.
Use local lesson plans as pedagogy/material/evaluation reference only.
Do not overwrite current anchor with older local lesson names or unit names.
```
