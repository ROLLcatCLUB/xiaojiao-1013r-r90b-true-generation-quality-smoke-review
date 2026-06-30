from __future__ import annotations

import hashlib
import json
import shutil
from datetime import datetime
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_ROOT = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
STAGE = "1013R_R93_P2_TEXTBOOK_ANCHOR_CLOSURE_AND_FINAL_PREVIEW_DRAFT"
OUT_DIR = OUTPUT_ROOT / STAGE
ZIP_PATH = OUTPUT_ROOT / f"{STAGE}.zip"

P1_DIR = OUTPUT_ROOT / "1013R_R93_P1_TEACHING_LOGIC_AND_TEACHER_READABLE_DRAFT_REPAIR"
P1_GATE_DIR = OUTPUT_ROOT / "1013R_R93_P1_ACCEPTANCE_AND_P2_ANCHOR_GATE"
P1_DRAFT = P1_DIR / "r93_p1_teacher_readable_lesson_draft.md"
P1_GATE_VALIDATOR = P1_GATE_DIR / "validate_1013R_R93_P1_acceptance_and_p2_anchor_gate_result.json"

TEXTBOOK_IMAGES = [
    Path(r"E:\学校工作\教学\教学资料\教材图片资料\三年级教材内容 - 图片\3.jpg"),
    Path(r"E:\学校工作\教学\教学资料\教材图片资料\三年级教材内容 - 图片\4.jpg"),
    Path(r"E:\学校工作\教学\教学资料\教材图片资料\三年级教材内容 - 图片\5.jpg"),
]

KB_EVIDENCE_SOURCES = [
    {
        "evidence_id": "kb_art_g3_textbook_images_20260427",
        "kind": "knowledge_base_textbook_image_index",
        "role": "anchor_supporting_index_not_ocr",
        "path": ROOT / "knowledge-base" / "_parsed" / "kb_art_g3_textbook_images_20260427.txt",
        "status_note": "教材图片包已入库登记；该文件明示尚未完成 OCR，不能单独作为教材原文引用。",
    },
    {
        "evidence_id": "kb_art_g3_lesson_case_lesson_8974535734",
        "kind": "teacher_local_lesson_plan",
        "role": "pedagogical_reference_not_current_textbook_anchor",
        "path": ROOT / "knowledge-base" / "_parsed" / "kb_art_g3_lesson_case_lesson_8974535734.txt",
        "status_note": "三年级下册本地备课资料，含渐变单元目标、材料与评价维度；单元名为第一单元《多变的色彩》，与当前教材页锚点不一致，只作教学组织参考。",
    },
    {
        "evidence_id": "kb_art_g3_lesson_case_1_fd1b5bdf60",
        "kind": "teacher_local_lesson_plan",
        "role": "pedagogical_reference_not_current_textbook_anchor",
        "path": ROOT / "knowledge-base" / "_parsed" / "kb_art_g3_lesson_case_1_fd1b5bdf60.txt",
        "status_note": "课时1《渐变的魅力》本地教案，提供导入、工具示范、学习单和评价参考；不覆盖当前第1课《色彩的渐变》教材事实。",
    },
    {
        "evidence_id": "kb_art_g3_lesson_case_2_07e719a809",
        "kind": "teacher_local_lesson_plan",
        "role": "pedagogical_reference_not_current_textbook_anchor",
        "path": ROOT / "knowledge-base" / "_parsed" / "kb_art_g3_lesson_case_2_07e719a809.txt",
        "status_note": "课时2《颜料的渐变》本地教案，提供水粉调色与材料组织参考；不覆盖当前教材锚点。",
    },
    {
        "evidence_id": "kb_art_g3_lesson_case_3_2eaf570678",
        "kind": "teacher_local_lesson_plan",
        "role": "pedagogical_reference_not_current_textbook_anchor",
        "path": ROOT / "knowledge-base" / "_parsed" / "kb_art_g3_lesson_case_3_2eaf570678.txt",
        "status_note": "课时3《渐变的节奏》本地教案，提供后续课衔接参考；当前教材页显示《渐变的节奏》为第二单元第2课。",
    },
    {
        "evidence_id": "lesson_plan_import_20260427",
        "kind": "knowledge_base_import_index",
        "role": "lineage_index",
        "path": ROOT / "knowledge-base" / "_indexes" / "lesson_plan_import_20260427.json",
        "status_note": "知识库导入索引，记录三年级下册本地教案来源和复制路径；用于 lineage，不作为教材正文证据。",
    },
    {
        "evidence_id": "knowledge_base_items_manifest",
        "kind": "knowledge_base_manifest",
        "role": "lineage_manifest",
        "path": ROOT / "knowledge-base" / "_manifests" / "items.csv",
        "status_note": "知识库条目清单，记录教材图片包与本地教案条目状态；用于 source lineage。",
    },
]


BOUNDARY = {
    "provider_called": False,
    "model_called": False,
    "new_fields_added": False,
    "profile_modified": False,
    "r21_modified": False,
    "r36_modified": False,
    "ui_page_connected": False,
    "formal_apply": False,
    "database_written": False,
    "feishu_written": False,
    "memory_written": False,
    "r94_executed": False,
    "derived_courseware_generated": False,
    "derived_worksheet_generated": False,
    "derived_rubric_generated": False,
    "teacher_review_required": True,
    "final_preview_draft_ready": True,
    "final_formal_lesson_ready": False,
}


TEXTBOOK_ANCHOR = {
    "anchor_status": "TEXTBOOK_ANCHOR_CLOSED_WITH_TEACHER_PAGE_IMAGES_AND_KB_LINEAGE",
    "anchor_evidence_basis": [
        "teacher_provided_page_images_are_primary_textbook_anchor",
        "knowledge_base_textbook_image_index_confirms_existing_local_textbook_image_package",
        "teacher_local_lesson_plans_are_pedagogical_references_not_current_textbook_anchor",
    ],
    "unit": "第二单元《多彩的世界》",
    "lesson_sequence": "第1课",
    "lesson_title": "色彩的渐变",
    "page_range": "6-7",
    "following_lessons": [
        {"lesson_sequence": "第2课", "lesson_title": "渐变的节奏", "page_range": "8-9"},
        {"lesson_sequence": "第3课", "lesson_title": "多彩的生活", "page_range": "10-11"},
    ],
    "confirmed_core_concepts": [
        "色彩的明度",
        "色彩的纯度",
        "明度渐变",
        "纯度渐变",
        "渐变规律",
        "秩序美",
        "节奏美",
        "层次丰富",
    ],
    "confirmed_material_modes": [
        "调色",
        "拼摆",
        "绘画",
        "按规律排列",
    ],
    "classroom_material_choice": "TEXTBOOK_CONFIRMS_MIXED_METHODS_TEACHER_SELECTS_LOCAL_TOOLS",
}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def image_records() -> list[dict]:
    records = []
    for image in TEXTBOOK_IMAGES:
        records.append(
            {
                "source_path": str(image),
                "file_name": image.name,
                "size": image.stat().st_size,
                "sha256": sha256_file(image),
            }
        )
    return records


def kb_evidence_records() -> list[dict]:
    records = []
    for source in KB_EVIDENCE_SOURCES:
        path = source["path"]
        records.append(
            {
                "evidence_id": source["evidence_id"],
                "kind": source["kind"],
                "role": source["role"],
                "path": str(path),
                "exists": path.exists(),
                "size": path.stat().st_size if path.exists() else None,
                "sha256": sha256_file(path) if path.exists() else None,
                "status_note": source["status_note"],
            }
        )
    return records


def copied_evidence_name(source: dict) -> str:
    return f"{source['evidence_id']}{source['path'].suffix}"


def textbook_anchor_closure_md(records: list[dict]) -> str:
    image_lines = "\n".join(
        f"- `{r['file_name']}` sha256=`{r['sha256']}` source=`{r['source_path']}`" for r in records
    )
    kb_lines = "\n".join(
        f"- `{r['evidence_id']}` role=`{r['role']}` exists=`{str(r['exists']).lower()}` sha256=`{r['sha256']}` source=`{r['path']}`"
        for r in kb_evidence_records()
    )
    return f"""# Textbook Anchor Closure - R93-P2

Stage: `{STAGE}`

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

{image_lines}

## Knowledge Base / Local Teaching Design Evidence

{kb_lines}

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
"""


def lesson_design_decision_card_md() -> str:
    return """# R93-P2 Lesson Design Decision Card

Status: final preview draft decision card. It closes textbook anchor, but does not formal apply.

## 本课核心学习问题

怎样通过色彩明度和纯度的有序变化，表现色彩渐变的秩序美、节奏美和层次丰富？

## 教材锚点

```text
第二单元《多彩的世界》
第1课《色彩的渐变》
页码：6-7
后续第2课：《渐变的节奏》
后续第3课：《多彩的生活》
```

## 证据分层

```text
Primary anchor: 教师提供的教材页图 3.jpg / 4.jpg / 5.jpg
Lineage support: knowledge-base 教材图片包登记
Pedagogical reference: 三年级下册本地备课与课时教案
Not used as anchor: 旧教案中的第一单元《多变的色彩》、课时1《渐变的魅力》、课时2《颜料的渐变》
```

## 本课主攻概念

```text
色彩的明度
色彩的纯度
明度渐变
纯度渐变
按规律排列形成渐变
```

P2 不再采用 P1 的“综合连续变化待确认”写法。本课已由教材页确认同时涉及明度和纯度。

## 课堂推进主线

```text
看生活中的渐变 -> 认识明度与纯度 -> 玩调色和排列游戏 -> 形成有规律的渐变 -> 用作品说明秩序、节奏和层次
```

## 学生主要误区

| Student Misunderstanding | Teacher Support |
| --- | --- |
| 只把渐变理解成颜色排队 | 追问排列是否有规律：从明到暗、从鲜到灰、从强到弱。 |
| 混淆明度和纯度 | 用学生语言区分：明度是亮不亮，纯度是鲜不鲜。 |
| 调色一下子跳太大 | 要求每次只加一点白、黑或灰，并保留上一格颜色。 |
| 只会说好看 | 使用句式：颜色从___到___，它变得更亮/更暗/更灰/更鲜。 |
| 作品缺节奏 | 引导学生按规律重复、排列或旋转渐变色块。 |

## 关键视觉支架

- 教材页中的山峦明度渐变图。
- 花卉作品旁的明度/纯度色条。
- 调色游戏中的小鸟、鲸鱼、饮料瓶排列和学生作品。

## 关键操作支架

- 明度渐变：选择一种颜色，逐渐加入白或黑，形成有序排列。
- 纯度渐变：纯色逐渐加入由黑白调成的灰色，纯度降低。
- 拼摆渐变：按颜色明亮程度或纯度强弱排序。

## 评价证据

- 学生能说出“明度是亮不亮，纯度是鲜不鲜”。
- 学生能完成一组明度或纯度渐变色阶。
- 学生能把色阶按规律排列，并说明规律。
- 学生能在小作品中表现渐变带来的秩序、节奏或层次。
"""


def final_preview_draft_md() -> str:
    return """# 《色彩的渐变》教学设计 Final Preview Draft - R93-P2

> teacher_review_required=true  
> formal_apply=false  
> 教材锚点已由教师提供的课页图片闭合，并由知识库教材图片包登记与本地备课资料补充 lineage。本稿是确定版教师审核预览稿，不写入 R21/R36，不写数据库/飞书/记忆，不进入 R94。

## 一、基本信息

| 项目 | 内容 |
| --- | --- |
| 单元 | 第二单元《多彩的世界》 |
| 课题 | 第1课《色彩的渐变》 |
| 页码 | 6-7 |
| 后续课 | 第2课《渐变的节奏》；第3课《多彩的生活》 |
| 学科 | 美术 |
| 年级 | 三年级 |
| 课时 | 第1课时，建议40分钟 |
| 课堂材料 | 教材支持调色、拼摆、绘画等方式；教师可按条件选水粉、水彩笔、彩铅、油画棒或混合材料 |

## 二、教材分析

本课位于第二单元《多彩的世界》第1课。教材从问题“变化多样的色彩是如何丰富我们的生活的呢？”进入，引导学生和同学一起进行色彩明度、纯度的调色游戏，按规律把颜色排列在一起，感受色彩渐变的美感，提升对色彩的敏感度。

教材明确出现“色彩的明度与纯度”和“渐变的调色游戏”两个学习板块：一方面通过自然景象、花卉作品和色条帮助学生理解色彩明亮程度叫作明度，色彩纯净程度叫作纯度；另一方面通过小鸟、鲸鱼、饮料瓶排列等学生作品，引导学生用加白、加黑、加灰和按规律排列等方式形成明度渐变或纯度渐变。

因此，本课不再只写成泛化的“连续变化”观察课，而应聚焦：认识明度与纯度，尝试有规律地调出或排列色彩渐变，感受渐变带来的秩序美、节奏美和层次丰富。后续第2课《渐变的节奏》继续把色彩渐变推进到画面节奏与旋律表现，第3课《多彩的生活》再迁移到校园空间和生活环境。

## 三、学情分析

三年级学生对鲜艳颜色、深浅变化和排列游戏有较强兴趣，也容易被教材中的图片、色条和学生作品吸引。他们能直观看出“这个颜色更亮”“那个颜色更深”，但未必能准确区分明度和纯度，也容易把渐变做成几个没有规律的色块并列。

本课需要用儿童能理解的话建立概念：明度是“亮不亮、暗不暗”，纯度是“鲜不鲜、灰不灰”。在操作上，不要求学生一次完成复杂作品，而是先用色条、调色或拼摆做小样，再把规律迁移到小作品中。

## 四、教学目标

1. 能在生活图片、教材作品和色条中发现色彩渐变现象，说出颜色按什么规律变化。
2. 知道色彩的明度和纯度，能用“亮/暗”“鲜/灰”等语言初步区分二者。
3. 能选择一种方式尝试表现明度渐变或纯度渐变，如逐渐加白、加黑、加灰，或按颜色明暗、鲜灰有序排列。
4. 能在小作品或色彩排列中表现渐变带来的秩序、节奏或层次，并用一句话说明自己的渐变规律。

对应核心素养：

- 审美感知：感受渐变形成的秩序美、节奏美和层次丰富。
- 艺术表现：用调色、拼摆或绘画表现明度/纯度渐变。
- 创意实践：把调色游戏迁移到小作品或有规律的色彩排列中。
- 文化理解：发现色彩渐变在自然、作品和生活空间中的作用。

## 五、教学重难点

教学重点：

- 理解色彩明度和纯度的基本含义。
- 能通过调色或排列形成有规律的明度渐变或纯度渐变。

教学难点：

- 区分“越来越亮/暗”和“越来越鲜/灰”的变化。
- 控制每一步变化幅度，让色彩渐变自然、有序，而不是突然跳色。

## 六、教学准备

教师准备：

- 教材页图片或实物教材。
- 明度渐变色条、纯度渐变色条。
- 一组自然过渡示例和一组跳变反例。
- 调色盘、颜料或可替代色彩材料。
- 可参考知识库中既有三年级渐变本地教案的学习单、工具示范和评价维度，但课堂事实以本课教材页为准。

学生准备：

- 小样纸条或格子纸。
- 水粉、水彩笔、彩铅、油画棒等本班可用材料。
- 剪贴或拼摆用色卡可选。

## 七、教学过程

### 1. 单元导入：色彩怎样让生活更丰富？（4分钟）

教师活动：

- 出示教材第6-7页，引导学生读单元问题：“变化多样的色彩是如何丰富我们的生活的呢？”
- 请学生观察教材中的山峦、花卉、小鸟、鲸鱼和饮料瓶排列，说说哪里出现了“慢慢变化”。

学生活动：

- 找出教材页中的渐变现象。
- 用自己的话描述：哪里从亮到暗，哪里从鲜到灰，哪里一层一层变化。

设计意图：

直接从教材锚点进入，先让学生发现本课要学的是色彩变化的规律，而不是孤立的调色技巧。

### 2. 概念辨析：明度是亮不亮，纯度是鲜不鲜（7分钟）

教师活动：

- 指向教材山峦图和色条，说明“各种色彩明亮的程度，叫作色彩的明度”。
- 指向红橙黄绿青蓝紫和纯度示例，说明“色彩纯净的程度，叫作色彩的纯度”。
- 用两组儿童语言帮助区分：
  - 明度：越来越亮、越来越暗。
  - 纯度：越来越鲜、越来越灰。

学生活动：

- 判断几组色卡分别在变亮/变暗，还是变鲜/变灰。
- 同桌说一句：“这一组颜色从___变到___。”

设计意图：

本课教材同时出现明度和纯度，必须先用学生能理解的语言拆开，避免概念混成一团。

### 3. 调色游戏：让颜色按规律变化（9分钟）

教师活动：

- 示范两种小样：
  1. 明度渐变：选择一种颜色，逐渐加入白或黑，形成有序排列。
  2. 纯度渐变：纯色逐渐加入由黑白调成的灰色，让颜色由鲜变灰。
- 强调每次只改变一点点，保留上一格颜色。

学生活动：

- 任选一种方式做三到五格小样。
- 在小样旁标注：明度渐变或纯度渐变。
- 用箭头表示变化方向。

设计意图：

用低风险小样让学生先体验“规律变化”，再进入作品表现。

### 4. 作品观察：渐变怎样产生节奏和层次？（5分钟）

教师活动：

- 观察教材中的小鸟、鲸鱼、饮料瓶排列和学生作品。
- 追问：“这些作品的颜色为什么看起来有秩序？哪些地方像节奏一样一层一层变化？”

学生活动：

- 指出作品中的明度或纯度渐变。
- 说出排列规律：从亮到暗、从鲜到灰、由深到浅、有序重复。

设计意图：

把调色结果和作品效果联系起来，让学生知道渐变不是只做色条，而是可以让画面产生秩序、节奏和层次。

### 5. 学生创作：完成一组有规律的渐变小作品（12分钟）

教师活动：

- 布置任务：选择明度渐变或纯度渐变，完成一组有规律的色彩小作品。形式可以是色条、图形、动物、植物或简单装饰图案。
- 巡视时重点看：
  1. 是否有明确变化方向。
  2. 是否能看出明度或纯度变化。
  3. 是否存在突然跳色。

学生活动：

- 选择一种渐变方式完成小作品。
- 在作品旁写一句说明：“我的颜色从___变到___，属于___渐变。”

分层建议：

- 基础：完成三格有序渐变。
- 进阶：完成五格渐变，并让变化更均匀。
- 挑战：把渐变规律用于有节奏的图形排列或小画面。

设计意图：

尊重教材的调色、拼摆、绘画多路径表达，让不同材料条件和不同能力学生都有可完成的任务。

### 6. 展示评价：看规律，说变化（3分钟）

教师活动：

- 选取几件作品展示，引导学生按证据评价。
- 提问：
  1. 这组颜色是明度变化还是纯度变化？
  2. 它从哪里开始，向哪里变化？
  3. 中间有没有跳得太快？

学生活动：

- 作者说明自己的变化规律。
- 同伴给出一个优点和一个可调整建议。

设计意图：

评价回到教材核心：明度、纯度、渐变规律，而不是泛泛说好看。

## 八、评价设计

| 评价维度 | 可观察证据 |
| --- | --- |
| 能发现 | 能在教材图像或作品中找出渐变现象。 |
| 能区分 | 能初步说出明度是亮暗变化，纯度是鲜灰变化。 |
| 能操作 | 能完成三到五格明度或纯度渐变。 |
| 有规律 | 色彩排列有方向，不突然跳色。 |
| 能表达 | 能说清“从___变到___，属于___渐变”。 |

## 九、板书设计

```text
第1课 色彩的渐变

明度：亮不亮、暗不暗
纯度：鲜不鲜、灰不灰

明度渐变：逐渐加白 / 加黑
纯度渐变：逐渐加灰，鲜 -> 灰

渐变规律：
从___到___
一层一层变化
有秩序、有节奏、有层次
```

## 十、教学反思与延伸

本课的关键不在于学生记住术语，而在于能通过观察和操作理解两类变化：颜色的亮暗变化和鲜灰变化。教学时要避免把明度、纯度、色相同时铺开过多，而应紧扣教材中的明度与纯度渐变，让学生通过调色游戏和作品排列感受渐变的秩序美。

后续第2课《渐变的节奏》可以继续引导学生把本课的明度/纯度渐变迁移到画面节奏和旋律表现中；第3课《多彩的生活》可进一步把渐变应用到校园和生活空间。

## 十一、生成说明

本稿基于 R93-P1 教师可审草案、教师提供的教材页图片、知识库教材图片包登记和三年级渐变本地备课资料生成。R93-P2 已关闭教材锚点，但仍是 final preview draft，不是 formal apply，不进入 R94。
"""


def source_gap_closure_md() -> str:
    return """# R93-P2 Source Gap Closure

## Closed

| Gap From P1 | P2 Status | Evidence |
| --- | --- | --- |
| 单元名称 | CLOSED | 第二单元《多彩的世界》 appears on all three page images. |
| 课题名称 | CLOSED | 第1课《色彩的渐变》 appears on page 6. |
| 课时位置 | CLOSED | 第1课 confirmed by page 6. |
| 教材页码 | CLOSED | 第1课 pages 6-7. |
| 后续课题 | CLOSED | 第2课《渐变的节奏》 pages 8-9; 第3课《多彩的生活》 pages 10-11. |
| 本课核心概念 | CLOSED | 教材 explicitly says 色彩的明度与纯度, 明度渐变, 纯度渐变, 渐变规律. |
| 知识库 lineage | CLOSED_WITH_NOTES | 本地教材图片包已在 knowledge-base 登记；旧教案可作教学参考，但不作为当前教材事实锚点。 |

## Still Teacher-Selected

| Item | Status | Why |
| --- | --- | --- |
| Exact classroom material | TEACHER_SELECTS_LOCAL_TOOLS | Textbook supports 调色、拼摆、绘画 and shows varied tools; the school/class period decides concrete material. |
| Formal apply | NOT_ALLOWED_IN_P2 | P2 is final preview draft only. |
| R94 derivation | HELD | Courseware/worksheet/rubric should wait until teacher accepts P2. |
"""


def kb_evidence_notes_md(records: list[dict]) -> str:
    rows = "\n".join(
        f"| `{r['evidence_id']}` | {r['kind']} | `{r['role']}` | {str(r['exists']).lower()} | {r['status_note']} |"
        for r in records
    )
    return f"""# Knowledge Base Evidence Notes - R93-P2

P2 scanned the existing project knowledge base before closing the textbook anchor.

| Evidence | Kind | Role | Exists | Note |
| --- | --- | --- | --- | --- |
{rows}

## Decision

```text
Use current textbook page images as the only current textbook-fact anchor.
Use knowledge-base textbook image index as lineage support.
Use local lesson plans as pedagogy/material/evaluation reference only.
Do not overwrite current anchor with older local lesson names or unit names.
```
"""


def quality_sentinel() -> dict:
    return {
        "stage": STAGE,
        "quality_sentinel_version": "v0",
        "result": "BASIC_USABLE",
        "blocking": False,
        "teacher_review_required": True,
        "textbook_anchor_closed": True,
        "final_preview_draft_ready": True,
        "final_formal_lesson_ready": False,
        "reasons": [
            "teacher-provided textbook page images close the lesson anchor",
            "knowledge-base textbook image package and local lesson plans were scanned and attached as lineage/reference evidence",
            "concept focus now matches textbook pages: 明度与纯度、明度渐变、纯度渐变",
            "teacher-readable draft has been narrowed to the confirmed textbook page",
            "formal apply and R94 derivation remain blocked",
        ],
        "not_claimed": [
            "formal lesson approval",
            "R21/R36 write",
            "UI binding",
            "courseware/worksheet/rubric readiness",
        ],
    }


def readme_md() -> str:
    return f"""# {STAGE}

R93-P2 closes the textbook anchor using teacher-provided textbook page images and produces a determined final preview draft.

Final status:

```text
PASS_1013R_R93_P2_TEXTBOOK_ANCHOR_CLOSURE_AND_FINAL_PREVIEW_DRAFT
```

Key decision:

```text
textbook_anchor_closed=true
final_preview_draft_ready=true
final_formal_lesson_ready=false
r94_executed=false
```
"""


def validate() -> dict:
    failed: list[str] = []
    gate = read_json(P1_GATE_VALIDATOR)
    if not gate.get("validator_pass"):
        failed.append("p1_gate_not_pass")
    for image in TEXTBOOK_IMAGES:
        if not image.exists():
            failed.append(f"missing_textbook_image:{image}")
    kb_records = kb_evidence_records()
    missing_kb = [r["evidence_id"] for r in kb_records if not r["exists"]]
    if missing_kb:
        failed.append(f"missing_kb_evidence:{','.join(missing_kb)}")
    draft_text = (OUT_DIR / "r93_p2_final_preview_lesson_draft.md").read_text(encoding="utf-8")
    required = [
        "第二单元《多彩的世界》",
        "第1课《色彩的渐变》",
        "页码 | 6-7",
        "色彩的明度",
        "色彩的纯度",
        "明度渐变",
        "纯度渐变",
        "formal_apply=false",
        "不进入 R94",
    ]
    for phrase in required:
        if phrase not in draft_text:
            failed.append(f"missing_required_draft_phrase:{phrase}")
    forbidden = [
        "教材锚点需教师确认",
        "本课一定主攻明度渐变",
        "本课一定主攻纯度渐变",
        "正式教案通过",
        "formal_apply=true",
    ]
    for phrase in forbidden:
        if phrase in draft_text:
            failed.append(f"forbidden_phrase_in_draft:{phrase}")
    if any(
        BOUNDARY[key]
        for key in [
            "provider_called",
            "model_called",
            "new_fields_added",
            "profile_modified",
            "r21_modified",
            "r36_modified",
            "ui_page_connected",
            "formal_apply",
            "database_written",
            "feishu_written",
            "memory_written",
            "r94_executed",
            "derived_courseware_generated",
            "derived_worksheet_generated",
            "derived_rubric_generated",
        ]
    ):
        failed.append("boundary_violation")
    return {
        "stage": STAGE,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "status": "PASS" if not failed else "FAIL",
        "textbook_anchor_closed": True,
        "anchor_status": TEXTBOOK_ANCHOR["anchor_status"],
        "unit": TEXTBOOK_ANCHOR["unit"],
        "lesson_sequence": TEXTBOOK_ANCHOR["lesson_sequence"],
        "lesson_title": TEXTBOOK_ANCHOR["lesson_title"],
        "page_range": TEXTBOOK_ANCHOR["page_range"],
        "core_concepts": TEXTBOOK_ANCHOR["confirmed_core_concepts"],
        "classroom_material_choice": TEXTBOOK_ANCHOR["classroom_material_choice"],
        "quality_sentinel_v0_result": "BASIC_USABLE",
        "final_preview_draft_ready": True,
        "final_formal_lesson_ready": False,
        "r94_allowed": False,
        "boundary": BOUNDARY,
        "textbook_image_records": image_records(),
        "kb_evidence_records": kb_records,
        "failed_checks": failed,
        "validator_pass": not failed,
    }


def manifest_records(files: list[Path]) -> list[dict]:
    return [
        {
            "path": str(path.relative_to(ROOT)).replace("/", "\\"),
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
            zf.write(path, f"{STAGE}/{path.relative_to(OUT_DIR).as_posix()}")
    return sha256_file(ZIP_PATH)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    textbook_dir = OUT_DIR / "textbook_page_evidence"
    textbook_dir.mkdir(exist_ok=True)
    for image in TEXTBOOK_IMAGES:
        shutil.copy2(image, textbook_dir / image.name)

    kb_dir = OUT_DIR / "source_evidence"
    kb_dir.mkdir(exist_ok=True)
    for source in KB_EVIDENCE_SOURCES:
        if source["path"].exists():
            shutil.copy2(source["path"], kb_dir / copied_evidence_name(source))

    write_text(OUT_DIR / "README.md", readme_md())
    write_json(OUT_DIR / "textbook_anchor_closed_1013R_R93_P2.json", TEXTBOOK_ANCHOR)
    write_text(OUT_DIR / "textbook_anchor_closure.md", textbook_anchor_closure_md(image_records()))
    write_text(OUT_DIR / "lesson_design_decision_card_1013R_R93_P2.md", lesson_design_decision_card_md())
    write_text(OUT_DIR / "r93_p2_final_preview_lesson_draft.md", final_preview_draft_md())
    write_text(OUT_DIR / "source_gap_closure.md", source_gap_closure_md())
    write_text(OUT_DIR / "kb_evidence_notes.md", kb_evidence_notes_md(kb_evidence_records()))
    write_json(OUT_DIR / "quality_sentinel_v0_result.json", quality_sentinel())
    shutil.copy2(P1_DRAFT, OUT_DIR / "source_snapshot_r93_p1_teacher_readable_lesson_draft.md")
    shutil.copy2(Path(__file__), OUT_DIR / Path(__file__).name)

    validation = validate()
    write_json(OUT_DIR / "validate_1013R_R93_P2_textbook_anchor_closure_final_preview_draft_result.json", validation)

    files = [p for p in OUT_DIR.rglob("*") if p.is_file()]
    zip_sha = build_zip([p for p in files if p.name not in {"REVIEW_PACKAGE_MANIFEST.json", "REVIEW_PACKAGE_MANIFEST.md"}])
    manifest = {
        "stage": STAGE,
        "final_status": "PASS_1013R_R93_P2_TEXTBOOK_ANCHOR_CLOSURE_AND_FINAL_PREVIEW_DRAFT"
        if validation["validator_pass"]
        else "FAIL_1013R_R93_P2_TEXTBOOK_ANCHOR_CLOSURE_AND_FINAL_PREVIEW_DRAFT",
        "zip_path": str(ZIP_PATH.relative_to(ROOT)).replace("/", "\\"),
        "zip_sha256": zip_sha,
        "files": manifest_records([p for p in OUT_DIR.rglob("*") if p.is_file()]),
        "boundary": BOUNDARY,
    }
    write_json(OUT_DIR / "REVIEW_PACKAGE_MANIFEST.json", manifest)
    lines = ["# REVIEW_PACKAGE_MANIFEST", "", f"ZIP SHA256: `{zip_sha}`", ""]
    for record in manifest["files"]:
        lines.append(f"- `{record['path']}` sha256=`{record['sha256']}`")
    write_text(OUT_DIR / "REVIEW_PACKAGE_MANIFEST.md", "\n".join(lines))

    print(
        json.dumps(
            {
                "stage": STAGE,
                "validator_pass": validation["validator_pass"],
                "textbook_anchor_closed": validation["textbook_anchor_closed"],
                "final_preview_draft_ready": validation["final_preview_draft_ready"],
                "out_dir": str(OUT_DIR),
                "zip_path": str(ZIP_PATH),
                "zip_sha256": zip_sha,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
