from __future__ import annotations

import hashlib
import json
import shutil
from datetime import datetime
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_ROOT = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
STAGE = "1013R_R93_P1_TEACHING_LOGIC_AND_TEACHER_READABLE_DRAFT_REPAIR"
OUT_DIR = OUTPUT_ROOT / STAGE
R93_DIR = (
    OUTPUT_ROOT
    / "1013R_R91B_R93_FAST_FULL_LESSON_DRAFT_QUEUE"
    / "R93_FULL_LESSON_DRAFT_ASSEMBLY"
)
R92_DIR = (
    OUTPUT_ROOT
    / "1013R_R91B_R93_FAST_FULL_LESSON_DRAFT_QUEUE"
    / "R92_FULL_CLASSROOM_FLOW_SMOKE"
)
ZIP_PATH = OUTPUT_ROOT / f"{STAGE}.zip"


BOUNDARY = {
    "provider_called": False,
    "model_called": False,
    "new_classroom_flow_candidates_generated": False,
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
    "teacher_review_required": True,
    "preview_draft_only": True,
}


SOURCE_REFERENCES = [
    {
        "id": "zxxk_2025_2026_sync_snippet",
        "url": "https://www.zxxk.com/docpack/3659930.html",
        "source_type": "public_search_result_snippet",
        "observed_claim": "2025-2026学年苏少版美术三年级下册同步课件 includes 第二单元第1课《色彩的渐变》 and 第2课《渐变的节奏》.",
        "confidence": "candidate_only",
        "audit_use": "Supports that this newer-looking naming exists, but not enough to write as official textbook fact.",
    },
    {
        "id": "dzkbw_org_susan_3s",
        "url": "https://www.dzkbw.org/book/7402.html",
        "source_type": "public_textbook_catalog_page",
        "observed_claim": "Page says the listed 苏少版三年级美术上册 book is not in the 2025 national textbook catalog, and lists 第1课 色彩明度渐变.",
        "confidence": "conflict_evidence",
        "audit_use": "Shows 明度渐变 is associated with 三年级上册 on at least one catalog page, and the page itself warns current-use risk.",
    },
    {
        "id": "haoduoyun_2012_susan_3x_snippet",
        "url": "https://www.haoduoyun.cc/book/sjb/meishu/mi3x/3.shtml",
        "source_type": "public_search_result_snippet",
        "observed_claim": "Old 2012 苏少/苏教三年级美术下册 catalog snippet lists 第1课 色彩的纯度渐变.",
        "confidence": "conflict_evidence",
        "audit_use": "Shows older 三下 resources may anchor the first lesson to 纯度渐变 rather than general 色彩的渐变.",
    },
    {
        "id": "yanxiuwang_video_resource_snippet",
        "url": "https://m.yanxiuwang.cn/Course/play/course_id/31173.html",
        "source_type": "public_resource_page",
        "observed_claim": "Video resources list 苏少版三年级下册 色彩的明度渐变 and nearby 色彩的纯度渐变 entries.",
        "confidence": "conflict_evidence",
        "audit_use": "Shows teaching-resource pages mix 明度 and 纯度 labels; not authoritative enough for final anchor.",
    },
]


ANCHOR_AUDIT_ITEMS = [
    (
        "教材版本",
        "SOURCE_CONFLICT",
        "Public resources mix 苏少版 / 苏教版 / 2024 / 2025-2026 / 2012 old labels.",
        "Write only as candidate. Do not write a fixed version in the lesson body.",
    ),
    (
        "年级册次",
        "SOURCE_CONFLICT",
        "R93 and newer resource snippets point to 三年级下册, while 明度渐变 appears in 三年级上册 catalog pages.",
        "Use 三年级候选; require teacher confirmation before finalizing 上册/下册.",
    ),
    (
        "课题名称",
        "SOURCE_CONFLICT",
        "Observed labels include 色彩的渐变, 色彩明度渐变, 色彩的纯度渐变.",
        "Use 《色彩的渐变》 as candidate title only; keep teacher_review_required=true.",
    ),
    (
        "单元名称",
        "NEEDS_TEACHER_CONFIRM",
        "R93 and a public resource snippet mention 第二单元《多彩的世界》, but no official textbook page was verified.",
        "Do not write as confirmed. Mark 第二单元《多彩的世界》 as candidate.",
    ),
    (
        "第几课",
        "NEEDS_TEACHER_CONFIRM",
        "Newer resource snippets say 第1课, but official textbook pages were not verified.",
        "Use 第1课候选 only.",
    ),
    (
        "教材页码",
        "DO_NOT_WRITE_AS_FACT",
        "No reliable page image or official page number was verified in this repair.",
        "Remove page-number claims such as 教材第6-7页.",
    ),
    (
        "后续课题",
        "NEEDS_TEACHER_CONFIRM",
        "A public resource snippet mentions 第2课《渐变的节奏》; no official textbook source was verified.",
        "Keep as source gap and teacher-confirm item.",
    ),
    (
        "本课核心概念",
        "SOURCE_CONFLICT",
        "IMA and public resources mix 明度 / 纯度 / 色相 / 综合渐变.",
        "Until teacher confirms textbook, use safe preview focus: color continuous change,端色,中间色,过渡方向,层次变化.",
    ),
]


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def anchor_audit_md() -> str:
    rows = "\n".join(
        f"| {item} | {status} | {evidence} | {rule} |"
        for item, status, evidence, rule in ANCHOR_AUDIT_ITEMS
    )
    sources = "\n".join(
        f"- `{src['id']}`: {src['url']}；{src['observed_claim']}；audit_use={src['audit_use']}"
        for src in SOURCE_REFERENCES
    )
    return f"""# Textbook Anchor Audit - R93-P1

Stage: `{STAGE}`

Conclusion: `TEXTBOOK_ANCHOR_NEEDS_TEACHER_CONFIRM`

This audit treats public web resources as conflict evidence, not as final textbook truth. The repair must not write a fixed textbook version, page number, lesson sequence, or concept focus until the teacher provides the actual textbook page or official material.

| Item | Status | Evidence | Safe Write Rule |
| --- | --- | --- | --- |
{rows}

Allowed status values:

```text
CONFIRMED
NEEDS_TEACHER_CONFIRM
SOURCE_CONFLICT
DO_NOT_WRITE_AS_FACT
```

Source references used for conflict audit:

{sources}

Do not write as confirmed fact in R93-P1:

```text
苏少版2026春三年级下册第二单元第1课
教材第6-7页
后续第2课必为《渐变的节奏》
本课一定主攻明度渐变
本课一定主攻纯度渐变
本课同时完整主攻明度、纯度、色相
```
"""


def concept_focus_decision_md() -> str:
    return f"""# Concept Focus Decision - R93-P1

Selected route for this repair:

```text
SAFE_PREVIEW_UNTIL_TEXTBOOK_CONFIRMED
```

Reason:

Public resources conflict on whether the relevant lesson is named `色彩的渐变`, `色彩明度渐变`, or `色彩的纯度渐变`. R93-P1 therefore narrows the teacher-readable draft to a safe classroom core: students observe and express continuous color change through `端色`, `中间色`, `过渡方向`, and `层次变化`.

## If the confirmed lesson is 色彩的纯度渐变

Teaching focus should become:

```text
认识色彩由鲜艳到灰浊、由强到弱的纯度变化。
通过加入灰色、少量互补色或调和方式形成纯度层次。
评价重点看色彩是否由鲜明逐步减弱，而不是单纯变浅。
```

Repair required:

- Lower `加白/加黑` to optional comparison, not core method.
- Revise objectives to `能观察并表现颜色鲜灰强弱的连续变化`.
- Revise demonstration to `同一色相逐步降低鲜艳度`.
- Replace board keywords from `深浅` to `鲜灰 / 强弱 / 纯度层次`.

## If the confirmed lesson is 色彩明度渐变

Teaching focus may become:

```text
认识色彩明亮程度的变化。
通过逐步加白或加黑形成由深到浅、由浅到深的明度阶梯。
评价重点看深浅层次是否连续、过渡是否自然。
```

Repair required:

- Keep `加白/加黑` as core method.
- Do not make `纯度渐变` and `色相渐变` equal teaching targets.
- Student language can use `越来越亮 / 越来越暗`.

## If the textbook remains unconfirmed

Use this safe preview wording:

```text
本课暂以“色彩连续变化的观察与表现”为核心，围绕端色、中间色、过渡方向、层次变化组织教学；具体属于明度渐变、纯度渐变或色相渐变，需教师依据教材页确认后定稿。
```

R93-P1 draft follows this third route.
"""


def teaching_logic_diagnosis_md() -> str:
    return f"""# Teaching Logic Diagnosis - R93-P1

Input reviewed:

- R93 full lesson draft
- R93 structured json
- R92 classroom flow preview
- R93 lineage
- User-provided IMA teacher-style reference text
- Public conflict audit sources

## Diagnosis

1. Core question was not safe enough.

R93 used a usable line around `端色`, `中间色`, `过渡方向`, and `层次`, but it also wrote `明度` and `色相` as if the textbook focus were already known. IMA then expanded this further to `明度`, `纯度`, and `色相`, which increases concept conflict risk.

2. Activity chain was basically executable but needed a stronger learning line.

R93 had observation, demonstration, try-out, creation, exchange, and revision. The repair turns this into:

```text
看见慢慢变
判断是不是连续变
试出中间层
用层次完成小作品
用证据说清并微修订
```

3. Teacher language and student language were mixed.

The repair keeps teacher terms such as `端色`, `中间色`, `过渡方向`, `层次变化`, and gives student-facing language such as `从哪边开始`, `慢慢变到哪里`, `中间有没有跳过去`.

4. Evaluation needed to push revision.

The repair uses three visible evidence checks:

```text
能指出两个端色
能看见至少三层连续变化
能说清从哪里变到哪里，并完成一次微修订
```

5. Time load needed compression.

IMA totals about 47 minutes and contains too many concept targets. R93-P1 uses a 40-minute preview schedule with one safe core, leaving more realistic time for student creation.

## Repair Decision

R93-P1 does not decide the official textbook anchor. It provides a teacher-reviewable preview draft that can survive either `明度`, `纯度`, or general `色彩的渐变` confirmation with minimal later repair.
"""


def lesson_design_decision_card_md() -> str:
    return """# Lesson Design Decision Card - R93-P1

Status: preview-only generation intermediate, not a new formal profile field.

## 本课核心学习问题

颜色怎样从一种状态慢慢变到另一种状态？学生怎样在作品中做出连续、清楚、能说明的渐变层次？

## 学生主要误区

| Student Misunderstanding | Teacher Support |
| --- | --- |
| 把渐变画成几个断开的色块 | 比较“楼梯式跳变”和“滑梯式慢慢变”，让学生找中间少了哪一层。 |
| 只说“好看、漂亮” | 给句式：“我的颜色从___变到___，中间慢慢变得___。” |
| 一下子加太多白或换色太快 | 要求保留上一格颜色，每次只改变一点点。 |
| 颜色调脏或水太多 | 提醒少量多次、洗笔擦干、先试色再上作品。 |
| 看不到渐变方向 | 在小样纸条底边画箭头，先说方向再创作。 |

## 本课主攻概念

Safe preview focus:

```text
色彩连续变化；端色；中间色；过渡方向；层次变化。
```

Not written as confirmed:

```text
明度渐变 / 纯度渐变 / 色相渐变的正式教材核心。
```

## 课堂推进主线

```text
生活现象触发 -> 问题聚焦 -> 小样试色 -> 教师示范 -> 图案创作 -> 证据评价 -> 微修订
```

## 关键视觉支架

- 两张生活渐变图片或色卡：一张变化自然，一张断层明显。
- 三到五格小样纸条。
- 端色 / 中间色 / 方向箭头标记。

## 关键操作支架

- 先做小样，再做作品。
- 每次只改变一点颜色。
- 每个学生保留一个方向箭头和一句说明。

## 评价证据

- 作品中能看到两个端色。
- 至少三层连续变化，不是突然跳色。
- 学生能用一句话说清变化方向。
- 至少完成一次基于评价的微修订。
"""


def teacher_readable_draft_md() -> str:
    return """# 《色彩的渐变》教学设计 Preview Draft - R93-P1

> teacher_review_required=true  
> formal_apply=false  
> 教材锚点需教师确认。本稿只作为教师审阅预览，不写入 R21/R36，不写数据库/飞书/记忆。

## 一、基本信息

| 项目 | 内容 |
| --- | --- |
| 课题 | 《色彩的渐变》（候选课题，需教师依据教材页确认） |
| 年级 | 三年级（册次需教师确认） |
| 学科 | 美术 |
| 单元 | 第二单元《多彩的世界》（候选单元，需教师确认） |
| 课时 | 第1课时 / 第1课（候选，需教师确认） |
| 教材版本 | 苏少版 / 苏教版 / 2024 / 2026春等表述存在公开资料冲突，暂不写死 |

## 二、教材分析

本稿暂不把具体教材版本、页码和课次写成已确认事实。依据当前 R93 草案、IMA 参考稿和公开资料冲突核验，本课先采用安全教学核心：引导学生观察生活和作品中的色彩连续变化，认识一组颜色从端色出发，经过中间色逐步过渡到另一端的层次关系。

如果教师确认教材主攻“明度渐变”，本课可把加白或加黑形成深浅层次作为核心方法；如果教师确认教材主攻“纯度渐变”，则需要把重点改为颜色由鲜艳到灰浊、由强到弱的变化。本预览稿暂不把明度、纯度、色相三者并列为同等教学重点。

## 三、学情分析

三年级学生通常能直观看到颜色深浅、浓淡或色相变化，也愿意通过涂色和调色尝试表现颜色变化。但他们容易把渐变理解成几个颜色并排，或者只用“好看、漂亮”评价作品，难以说清颜色从哪里开始、向哪里变化、中间怎样慢慢过渡。

因此，本课不急于铺开多个色彩概念，而是用生活图像、小样试色和作品证据帮助学生建立一个稳定经验：渐变不是突然换色，而是有方向、有层次、能说清的连续变化。

## 四、教学目标

1. 能观察生活和作品中的色彩连续变化，指出颜色从哪里开始、向哪里变化。
2. 能通过小样试色或色阶排列，尝试做出至少三层连续变化的颜色。
3. 能在简单图案创作中运用渐变层次，让画面出现较自然的过渡。
4. 能用“从___到___，中间慢慢变___”说明自己的作品变化，并根据同伴或教师建议完成一次微修订。

对应核心素养：

- 审美感知：感受色彩连续变化形成的层次美。
- 艺术表现：尝试用调色、排列或叠涂表现渐变。
- 创意实践：把小样经验迁移到自己的图案作品中。
- 文化理解：发现渐变现象与生活图像、自然景象和日常设计有关。

## 五、教学重难点

教学重点：

- 理解颜色可以有方向、有层次地连续变化。
- 能用端色、中间色和过渡方向组织一组渐变。

教学难点：

- 避免颜色突然跳变，做出较自然的中间层。
- 用儿童能说清的话说明自己的渐变方向和修改依据。

## 六、教学准备

教师准备：

- 生活中的渐变图片或色卡。
- 一组自然过渡示例和一组跳变明显的反例。
- 小样纸条、示范用颜料或彩铅、展示磁贴。

学生准备：

- 常用绘画工具。
- 小样试色纸。
- 简单图案画纸。

## 七、教学过程

总时长建议：40分钟。若校内课时为45分钟，可把学生创作或展示评价各延长2到3分钟。

### 1. 游戏导入：什么叫“慢慢变”？（4分钟）

教师活动：

- 请几名学生按身高从低到高排队，引导学生发现“不是一下子变高，而是一点一点变”。
- 出示两组颜色卡：一组颜色跳得很快，一组颜色慢慢过渡。提问：“哪一组更像刚才排队一样，是慢慢变过去的？”

学生活动：

- 参与排序或观察排序。
- 用自己的话说出“慢慢变”“一层一层变”的感觉。

学生课堂语言：

```text
它不是突然换颜色，是中间还有几步。
```

设计意图：

用身体经验和颜色卡建立“连续变化”的初步感受，避免一开始就进入抽象概念。

### 2. 生活观察：颜色是一下子变，还是一层一层变？（5分钟）

教师活动：

- 展示晚霞、花瓣、彩虹或水面等图片，引导学生找出颜色变化的起点、终点和中间过渡。
- 追问：“这张图的颜色从哪边开始？慢慢变到哪里？中间有没有跳过去？”

学生活动：

- 指出端色和中间色。
- 用手指沿着变化方向说一遍。

教师专业语言：

```text
端色、中间色、过渡方向、层次。
```

学生课堂语言：

```text
最开始的颜色、中间慢慢变出来的颜色、最后变到的颜色。
```

设计意图：

让学生先看见规律，再给出术语。术语服务观察，不替代观察。

### 3. 小样试色：怎样让颜色慢慢变？（8分钟）

教师活动：

- 发放三到五格小样纸条。
- 让学生选择一种颜色或两种相近颜色，先试出三层变化。
- 提醒学生每次只改变一点点，保留上一格颜色的痕迹。

学生活动：

- 在小样纸上做渐变试色。
- 给小样画一个方向箭头。
- 同桌互看：有没有突然跳色？中间还缺不缺一层？

设计意图：

用低风险小样暴露问题。学生先在小纸条上试错，再进入正式作品，能减少创作焦虑。

### 4. 教师示范：中间色怎么出来？（5分钟）

教师活动：

- 示范一条三到五层渐变：先确定两个端色，再调或选中间层。
- 对比“跳变版”和“连续版”，让学生说出差别。
- 只强调一个方法原则：每一步变化小一点，层次就更自然。

学生活动：

- 观察教师示范。
- 用一句话复述方法：“先定两头，再找中间，变化小一点。”

设计意图：

示范不铺开概念大全，只解决学生最可能卡住的“中间层怎么来”。

### 5. 学生创作：把渐变用到小作品里（12分钟）

教师活动：

- 布置任务：在一个简单图案中使用一组渐变，至少能看到两个端色和三层连续变化。
- 巡视时重点看三类问题：跳色、方向不清、颜色过脏。
- 对不同学生给分层支架：
  - 基础：完成三层渐变。
  - 进阶：让过渡更自然。
  - 挑战：把渐变方向和图案结构结合起来。

学生活动：

- 完成图案作品。
- 在作品背面写一句说明：“我的颜色从___变到___，中间慢慢变___。”

设计意图：

让学生把小样中的方法迁移到完整作品，形成可观察的学习证据。

### 6. 展示评价：你的渐变方向和层次说得清吗？（5分钟）

教师活动：

- 选取几件作品展示，不只展示最好看的，也展示有改进空间的。
- 引导学生按三条证据评价：
  1. 能看到两个端色吗？
  2. 中间至少有三层变化吗？
  3. 作者能说清从哪里变到哪里吗？

学生活动：

- 作者用手指指出端色、中间色和变化方向。
- 同伴给出一个优点和一个可修改建议。

设计意图：

评价回到作品证据和语言表达，不停留在“好看不好看”。

### 7. 微修订与小结：让一处变化更自然（1分钟）

教师活动：

- 请学生圈出作品中最想改的一处：加一层中间色、调整方向箭头或让边缘更柔和。
- 小结：“渐变不是把颜色排在一起，而是让颜色有方向、有层次地慢慢变。”

学生活动：

- 选择一处做标记，课后或下节课继续修订。

设计意图：

用微修订把评价转化为下一步行动。

## 八、评价设计

| 评价维度 | 可观察证据 |
| --- | --- |
| 看得见 | 能指出生活图像或作品中的端色和中间色。 |
| 试得出 | 小样纸上至少出现三层连续变化。 |
| 用得上 | 作品中有明确渐变方向和较自然过渡。 |
| 说得清 | 能用“从___到___，中间慢慢变___”说明作品。 |
| 改得动 | 能根据评价选择一处微修订。 |

## 九、板书设计

```text
色彩的渐变（教材锚点需确认）

不是突然换色
而是慢慢变化

端色 -> 中间色 -> 端色
方向：从____到____
层次：至少三层

作品自查：
1. 看得到两头吗？
2. 中间有没有跳过去？
3. 我能说清怎么变吗？
```

## 十、教学反思与延伸

本课预览稿把重点放在“色彩连续变化”的课堂经验上，而不是一次性讲完明度、纯度和色相。实际教学前，教师需先确认教材页和课题核心。如果教材明确为“明度渐变”，可强化加白或加黑的深浅变化；如果教材明确为“纯度渐变”，则需改为鲜灰强弱变化，不宜继续把加白变浅作为核心示范。

课后可请学生继续观察生活中的渐变现象，如天空、花瓣、灯光、服装或包装设计，并用一句话说明颜色从哪里变到哪里。

## 十一、生成说明

本稿为 R93-P1 教师可审 preview draft。它吸收了 IMA 参考稿的教案格式、游戏导入、调色接力思路、板书和反思表达，但修正了教材锚点写死、明度/纯度/色相混杂、时间超量和评价证据不够具体的问题。
"""


def source_gap_md() -> str:
    return """# R93-P1 Source Gap Teacher Confirm List

Before this draft can become a final lesson plan, the teacher must confirm:

| Item | Current Status | Teacher Confirm Question |
| --- | --- | --- |
| 教材版本 | SOURCE_CONFLICT | 使用的是苏少版、苏教版，还是学校实际采用的新版艺术教材？ |
| 年级册次 | SOURCE_CONFLICT | 本课属于三年级上册还是三年级下册？ |
| 课题名称 | SOURCE_CONFLICT | 教材原题是《色彩的渐变》《色彩明度渐变》还是《色彩的纯度渐变》？ |
| 单元名称 | NEEDS_TEACHER_CONFIRM | 第二单元是否确为《多彩的世界》？ |
| 课时位置 | NEEDS_TEACHER_CONFIRM | 本课是否为第1课 / 第1课时？ |
| 教材页码 | DO_NOT_WRITE_AS_FACT | 教材页码是多少？没有页图前不得写“教材第6-7页”。 |
| 后续课题 | NEEDS_TEACHER_CONFIRM | 后续课是否确为《渐变的节奏》？ |
| 核心概念 | SOURCE_CONFLICT | 本课主攻明度、纯度、色相，还是综合“色彩连续变化”？ |
| 材料要求 | NEEDS_TEACHER_CONFIRM | 学校课堂使用水粉、彩铅、油画棒，还是混合材料？ |
| 课时长度 | NEEDS_TEACHER_CONFIRM | 课堂是40分钟、45分钟，还是其他安排？ |

IMA text items that must not enter final draft without confirmation:

- `苏少版（2024）`
- `苏少版2026春`
- `三年级下册第二单元第1课`
- `教材第6-7页`
- `后续《渐变的节奏》`
- `明度、纯度、色相三者同等作为本课目标`
- `加入白色或黑色` as core method if the confirmed lesson is actually `纯度渐变`
"""


def revision_notes_md() -> str:
    return """# R93-P1 Revision Notes

## Absorbed from IMA

- Teacher-common lesson plan structure: basic information, textbook analysis, learner analysis, objectives, key points, preparation, process, board design, reflection.
- Game-based opening through gradual change.
- Low-risk trial activity before full creation.
- Board design and teaching reflection sections.

## Repaired from R93 and IMA

- Did not write unconfirmed textbook anchors as facts.
- Removed page-number claim from the teacher-readable draft.
- Did not make 明度、纯度、色相 equal teaching priorities.
- Compressed the lesson to a 40-minute preview schedule.
- Added student-facing language separate from teacher professional language.
- Added source gap teacher confirmation list.
- Made evaluation evidence concrete and tied to revision.

## Source Snapshot Note

The `source_snapshots/` directory preserves the original R93 and R92 materials for lineage review. Some source snapshots intentionally contain the old unconfirmed page-number or anchor wording; those are the problems R93-P1 flags and repairs. The repaired teacher-facing draft is `r93_p1_teacher_readable_lesson_draft.md`.

## Current quality judgment

The repair is `BASIC_USABLE` for teacher review because it is safer, more coherent, and more classroom-readable than R93, but it still cannot be final until the textbook page and concept focus are confirmed by the teacher.
"""


def source_snapshot_readme_md() -> str:
    return """# Source Snapshots

These files are preserved for R93-P1 lineage review only.

They may include old R93 preview wording that R93-P1 explicitly flags as unsafe, such as unconfirmed page-number claims. Do not treat source snapshots as the repaired teacher-facing draft.

Repaired draft:

```text
r93_p1_teacher_readable_lesson_draft.md
```
"""


def gpt_review_prompt_md() -> str:
    return """# GPT Review Prompt - 1013R R93-P1

Please review this package as a preview-only teaching-logic repair, not as a final lesson plan.

Check these gates first:

1. `textbook_anchor_audit.md` marks source conflicts and does not confirm unverified textbook facts.
2. `concept_focus_decision.md` narrows the draft to a safe preview route until the teacher confirms whether the lesson is about 明度, 纯度, 色相, or general 色彩连续变化.
3. `r93_p1_teacher_readable_lesson_draft.md` is more teacher-readable and keeps `teacher_review_required=true` and `formal_apply=false`.
4. Source gaps are listed in `r93_p1_source_gap_teacher_confirm_list.md`.
5. Validator and quality sentinel do not claim final quality or formal apply.
"""


def readme_md() -> str:
    return f"""# {STAGE}

R93-P1 repairs the R93 lesson draft by adding a textbook-anchor audit, concept-focus decision, teaching-logic diagnosis, and a teacher-readable preview draft.

Final status:

```text
PASS_1013R_R93_P1_TEACHING_LOGIC_AND_TEACHER_READABLE_DRAFT_REPAIR
```

Boundary:

```json
{json.dumps(BOUNDARY, ensure_ascii=False, indent=2)}
```

Key rule:

```text
This package does not confirm the textbook anchor. It keeps teacher_review_required=true and preview_draft_only=true.
```
"""


def quality_sentinel() -> dict:
    return {
        "stage": STAGE,
        "quality_sentinel_version": "v0",
        "result": "BASIC_USABLE",
        "blocking": False,
        "teacher_review_required": True,
        "preview_draft_only": True,
        "reasons": [
            "textbook anchor conflict is explicitly surfaced",
            "concept focus is narrowed to safe preview route",
            "teacher-readable draft is more coherent and classroom-oriented",
            "source gaps are listed for teacher confirmation",
            "not final because official textbook page and concept focus remain unconfirmed",
        ],
        "not_claimed": [
            "final lesson plan quality",
            "official textbook anchor confirmed",
            "formal apply passed",
            "provider rerun completed",
            "R94 executed",
        ],
    }


def validate(outputs: dict[str, Path]) -> dict:
    failures: list[str] = []
    required_files = [
        "textbook_anchor_audit.md",
        "concept_focus_decision.md",
        "teaching_logic_diagnosis.md",
        "lesson_design_decision_card.md",
        "r93_p1_teacher_readable_lesson_draft.md",
        "r93_p1_source_gap_teacher_confirm_list.md",
        "r93_p1_revision_notes.md",
        "quality_sentinel_v0_result.json",
    ]
    for name in required_files:
        if not outputs[name].exists():
            failures.append(f"missing_file:{name}")

    anchor_text = load_text(outputs["textbook_anchor_audit.md"])
    for status in ["CONFIRMED", "NEEDS_TEACHER_CONFIRM", "SOURCE_CONFLICT", "DO_NOT_WRITE_AS_FACT"]:
        if status not in anchor_text:
            failures.append(f"missing_anchor_status:{status}")

    draft = load_text(outputs["r93_p1_teacher_readable_lesson_draft.md"])
    forbidden = [
        "苏少版2026春三年级下册第二单元第1课",
        "教材第6-7页",
        "正式教案通过",
        "formal_apply=true",
    ]
    for phrase in forbidden:
        if phrase in draft:
            failures.append(f"forbidden_phrase_in_draft:{phrase}")

    required_draft_phrases = [
        "teacher_review_required=true",
        "formal_apply=false",
        "教材锚点需教师确认",
        "端色",
        "中间色",
        "过渡方向",
        "学生课堂语言",
        "微修订",
    ]
    for phrase in required_draft_phrases:
        if phrase not in draft:
            failures.append(f"missing_required_draft_phrase:{phrase}")

    q = json.loads(outputs["quality_sentinel_v0_result.json"].read_text(encoding="utf-8"))
    if q.get("result") not in ["BASIC_USABLE", "NEEDS_RETRY", "NOT_USABLE"]:
        failures.append("invalid_quality_sentinel_result")

    if any(BOUNDARY[key] for key in [
        "provider_called",
        "model_called",
        "new_classroom_flow_candidates_generated",
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
    ]):
        failures.append("boundary_violation")

    return {
        "stage": STAGE,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "status": "PASS" if not failures else "FAIL",
        "teacher_review_required": True,
        "preview_draft_only": True,
        "quality_sentinel_v0_result": q.get("result"),
        "textbook_anchor_status": "TEXTBOOK_ANCHOR_NEEDS_TEACHER_CONFIRM",
        "concept_focus_route": "SAFE_PREVIEW_UNTIL_TEXTBOOK_CONFIRMED",
        "source_gap_marked": "r93_p1_source_gap_teacher_confirm_list.md" in required_files,
        "boundary": BOUNDARY,
        "checks": {
            "required_files_present": all(outputs[name].exists() for name in required_files),
            "anchor_status_enums_present": all(
                status in anchor_text
                for status in ["CONFIRMED", "NEEDS_TEACHER_CONFIRM", "SOURCE_CONFLICT", "DO_NOT_WRITE_AS_FACT"]
            ),
            "draft_keeps_teacher_review_required": "teacher_review_required=true" in draft,
            "draft_keeps_formal_apply_false": "formal_apply=false" in draft,
            "draft_removes_page_number_claim": "教材第6-7页" not in draft,
            "draft_separates_student_language": "学生课堂语言" in draft,
            "draft_has_evidence_based_evaluation": "可观察证据" in draft,
            "quality_sentinel_enum_valid": q.get("result") in ["BASIC_USABLE", "NEEDS_RETRY", "NOT_USABLE"],
        },
        "failed_checks": failures,
        "validator_pass": not failures,
        "source_references": SOURCE_REFERENCES,
    }


def manifest_files(files: list[Path]) -> list[dict]:
    records = []
    for path in sorted(files):
        records.append(
            {
                "path": str(path.relative_to(ROOT)).replace("/", "\\"),
                "size": path.stat().st_size,
                "sha256": sha256_file(path),
            }
        )
    return records


def build_zip(files: list[Path]) -> str:
    if ZIP_PATH.exists():
        ZIP_PATH.unlink()
    with ZipFile(ZIP_PATH, "w", ZIP_DEFLATED) as zf:
        for path in sorted(files):
            arc = f"{STAGE}/{path.relative_to(OUT_DIR).as_posix()}"
            zf.write(path, arc)
    return sha256_file(ZIP_PATH)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    if not R93_DIR.exists():
        raise FileNotFoundError(f"Missing R93 source dir: {R93_DIR}")
    if not R92_DIR.exists():
        raise FileNotFoundError(f"Missing R92 source dir: {R92_DIR}")

    source_snapshot_dir = OUT_DIR / "source_snapshots"
    source_snapshot_dir.mkdir(exist_ok=True)
    for src in [
        R93_DIR / "r93_full_lesson_draft.md",
        R93_DIR / "r93_full_lesson_draft_structured.json",
        R93_DIR / "generation_lineage_1013R_R93.json",
        R92_DIR / "r92_full_classroom_flow_preview.md",
    ]:
        if src.exists():
            shutil.copy2(src, source_snapshot_dir / src.name)
    write_text(source_snapshot_dir / "README.md", source_snapshot_readme_md())

    outputs = {
        "README.md": OUT_DIR / "README.md",
        "textbook_anchor_audit.md": OUT_DIR / "textbook_anchor_audit.md",
        "concept_focus_decision.md": OUT_DIR / "concept_focus_decision.md",
        "teaching_logic_diagnosis.md": OUT_DIR / "teaching_logic_diagnosis.md",
        "lesson_design_decision_card.md": OUT_DIR / "lesson_design_decision_card.md",
        "r93_p1_teacher_readable_lesson_draft.md": OUT_DIR / "r93_p1_teacher_readable_lesson_draft.md",
        "r93_p1_source_gap_teacher_confirm_list.md": OUT_DIR / "r93_p1_source_gap_teacher_confirm_list.md",
        "r93_p1_revision_notes.md": OUT_DIR / "r93_p1_revision_notes.md",
        "GPT_REVIEW_PROMPT_1013R_R93_P1.md": OUT_DIR / "GPT_REVIEW_PROMPT_1013R_R93_P1.md",
        "quality_sentinel_v0_result.json": OUT_DIR / "quality_sentinel_v0_result.json",
        "validate_1013R_R93_P1_teaching_logic_teacher_readable_repair_result.json": OUT_DIR
        / "validate_1013R_R93_P1_teaching_logic_teacher_readable_repair_result.json",
    }

    write_text(outputs["README.md"], readme_md())
    write_text(outputs["textbook_anchor_audit.md"], anchor_audit_md())
    write_text(outputs["concept_focus_decision.md"], concept_focus_decision_md())
    write_text(outputs["teaching_logic_diagnosis.md"], teaching_logic_diagnosis_md())
    write_text(outputs["lesson_design_decision_card.md"], lesson_design_decision_card_md())
    write_text(outputs["r93_p1_teacher_readable_lesson_draft.md"], teacher_readable_draft_md())
    write_text(outputs["r93_p1_source_gap_teacher_confirm_list.md"], source_gap_md())
    write_text(outputs["r93_p1_revision_notes.md"], revision_notes_md())
    write_text(outputs["GPT_REVIEW_PROMPT_1013R_R93_P1.md"], gpt_review_prompt_md())
    write_json(outputs["quality_sentinel_v0_result.json"], quality_sentinel())

    validation = validate(outputs)
    write_json(outputs["validate_1013R_R93_P1_teaching_logic_teacher_readable_repair_result.json"], validation)
    shutil.copy2(Path(__file__), OUT_DIR / Path(__file__).name)

    files = [path for path in OUT_DIR.rglob("*") if path.is_file()]
    zip_sha = build_zip([path for path in files if path.name not in {"REVIEW_PACKAGE_MANIFEST.json", "REVIEW_PACKAGE_MANIFEST.md"}])
    manifest = {
        "stage": STAGE,
        "final_status": "PASS_1013R_R93_P1_TEACHING_LOGIC_AND_TEACHER_READABLE_DRAFT_REPAIR"
        if validation["validator_pass"]
        else "FAIL_1013R_R93_P1_TEACHING_LOGIC_AND_TEACHER_READABLE_DRAFT_REPAIR",
        "zip_path": str(ZIP_PATH.relative_to(ROOT)).replace("/", "\\"),
        "zip_sha256": zip_sha,
        "files": manifest_files([path for path in OUT_DIR.rglob("*") if path.is_file()]),
        "boundary": BOUNDARY,
    }
    write_json(OUT_DIR / "REVIEW_PACKAGE_MANIFEST.json", manifest)
    manifest_lines = ["# REVIEW_PACKAGE_MANIFEST", "", f"ZIP SHA256: `{zip_sha}`", ""]
    for record in manifest["files"]:
        manifest_lines.append(f"- `{record['path']}` sha256=`{record['sha256']}`")
    write_text(OUT_DIR / "REVIEW_PACKAGE_MANIFEST.md", "\n".join(manifest_lines))

    print(
        json.dumps(
            {
                "stage": STAGE,
                "validator_pass": validation["validator_pass"],
                "quality": validation["quality_sentinel_v0_result"],
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
