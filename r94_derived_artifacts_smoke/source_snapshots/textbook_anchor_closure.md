# Textbook Anchor Closure - R93-P2

Stage: `1013R_R93_P2_TEXTBOOK_ANCHOR_CLOSURE_AND_FINAL_PREVIEW_DRAFT`

Decision:

```text
TEXTBOOK_ANCHOR_CLOSED_WITH_TEACHER_PAGE_IMAGES_AND_KB_LINEAGE
```

## Closed Anchor

| Item | Closed Value | Evidence |
| --- | --- | --- |
| 单元 | 第二单元《多彩的世界》 | Page images 3.jpg, 4.jpg, 5.jpg all show the unit header. |
| 本课 | 第1课《色彩的渐变》 | 3.jpg, pages 6-7. |
| 页码 | 6-7 | 3.jpg page bottom. |
| 后续课 | 第2课《渐变的节奏》 | 4.jpg, pages 8-9. |
| 后续课 | 第3课《多彩的生活》 | 5.jpg, pages 10-11. |
| 本课核心 | 色彩的明度与纯度，以及渐变规律 | 3.jpg: `色彩的明度与纯度`, `渐变的调色游戏`, and unit goal text. |
| 学习方式 | 调色、拼摆、绘画、按规律排列 | 3.jpg top learning prompt and right-page activity visuals. |
| 材料选择 | 教材支持混合方式，教师按课堂条件选择 | Page evidence shows调色、拼摆、绘画; no single required classroom material is fixed. |

## Source Images

- `3.jpg` sha256=`765a471035ecb73951d2e7c550e32e45697e19539448345cda4af26b5631da82` source=`E:\学校工作\教学\教学资料\教材图片资料\三年级教材内容 - 图片\3.jpg`
- `4.jpg` sha256=`b68b725eddbc3fd19f1d3c9a5fa95216bde0502a7df6667ae83b3d78272d0361` source=`E:\学校工作\教学\教学资料\教材图片资料\三年级教材内容 - 图片\4.jpg`
- `5.jpg` sha256=`4d1aa7cdb49773d695cb8d15c8e866ac6becfe74cf7a2f568a2f101ceb96f556` source=`E:\学校工作\教学\教学资料\教材图片资料\三年级教材内容 - 图片\5.jpg`

## Knowledge Base / Local Teaching Design Evidence

- `kb_art_g3_textbook_images_20260427` role=`anchor_supporting_index_not_ocr` exists=`true` sha256=`8ec8de4b61feb4beeeeeeb3781e990223f4048b50a36522518e65a991b1fd924` source=`D:\Documents\SmartEdu\xiaobei-core\knowledge-base\_parsed\kb_art_g3_textbook_images_20260427.txt`
- `kb_art_g3_lesson_case_lesson_8974535734` role=`pedagogical_reference_not_current_textbook_anchor` exists=`true` sha256=`562f8c78fbefedd919c440e1e54eb03c2d099f43473503a6df72346abb7dc123` source=`D:\Documents\SmartEdu\xiaobei-core\knowledge-base\_parsed\kb_art_g3_lesson_case_lesson_8974535734.txt`
- `kb_art_g3_lesson_case_1_fd1b5bdf60` role=`pedagogical_reference_not_current_textbook_anchor` exists=`true` sha256=`58ac9768bf8eeba9fd7b0573d659bcc7cf8febf903222671dbff950a4ee386e4` source=`D:\Documents\SmartEdu\xiaobei-core\knowledge-base\_parsed\kb_art_g3_lesson_case_1_fd1b5bdf60.txt`
- `kb_art_g3_lesson_case_2_07e719a809` role=`pedagogical_reference_not_current_textbook_anchor` exists=`true` sha256=`fd1c5cab5155a015101ae1b3234dd3932a9b745f94a635b8f3ef63fa0acd479e` source=`D:\Documents\SmartEdu\xiaobei-core\knowledge-base\_parsed\kb_art_g3_lesson_case_2_07e719a809.txt`
- `kb_art_g3_lesson_case_3_2eaf570678` role=`pedagogical_reference_not_current_textbook_anchor` exists=`true` sha256=`2e1bb3b0913a229fe4ed34a9d58c7cc3de59553253fb272d27174615a47c72c9` source=`D:\Documents\SmartEdu\xiaobei-core\knowledge-base\_parsed\kb_art_g3_lesson_case_3_2eaf570678.txt`
- `lesson_plan_import_20260427` role=`lineage_index` exists=`true` sha256=`b8fea57a1b0e1d318b0682e22b1856e6d88eb276ce7bff2555d0293af47e92bb` source=`D:\Documents\SmartEdu\xiaobei-core\knowledge-base\_indexes\lesson_plan_import_20260427.json`
- `knowledge_base_items_manifest` role=`lineage_manifest` exists=`true` sha256=`c9b738d31641b2b8f212d0ff2f9a74b38ead517f14664f1ba74d3ff29d21adae` source=`D:\Documents\SmartEdu\xiaobei-core\knowledge-base\_manifests\items.csv`

Evidence rule:

```text
teacher-provided page images = primary textbook anchor
knowledge-base textbook image index = lineage support, not OCR source
teacher local lesson plans = pedagogy/material/evaluation reference, not current textbook anchor
```

The local knowledge-base record `kb_art_g3_textbook_images_20260427` confirms that the full textbook image package was already indexed from the same local image directory. It also states that OCR had not been completed, so P2 does not cite it as textbook text. The lesson-plan records provide useful classroom organization but retain older names such as 第一单元《多变的色彩》, 《渐变的魅力》, and 《颜料的渐变》; P2 therefore uses them only as teaching references.

## Closed Source Gaps

```text
unit_title_closed=true
lesson_title_closed=true
lesson_sequence_closed=true
page_range_closed=true
following_lessons_closed=true
core_concept_closed=true
```

## Still Teacher-Selected Before Class

```text
classroom_material_tool = teacher selects local tools from water-based paint / markers / color pencils / oil pastels / mixed materials
formal_apply = false
```
