# Textbook Anchor Audit - R93-P1

Stage: `1013R_R93_P1_TEACHING_LOGIC_AND_TEACHER_READABLE_DRAFT_REPAIR`

Conclusion: `TEXTBOOK_ANCHOR_NEEDS_TEACHER_CONFIRM`

This audit treats public web resources as conflict evidence, not as final textbook truth. The repair must not write a fixed textbook version, page number, lesson sequence, or concept focus until the teacher provides the actual textbook page or official material.

| Item | Status | Evidence | Safe Write Rule |
| --- | --- | --- | --- |
| 教材版本 | SOURCE_CONFLICT | Public resources mix 苏少版 / 苏教版 / 2024 / 2025-2026 / 2012 old labels. | Write only as candidate. Do not write a fixed version in the lesson body. |
| 年级册次 | SOURCE_CONFLICT | R93 and newer resource snippets point to 三年级下册, while 明度渐变 appears in 三年级上册 catalog pages. | Use 三年级候选; require teacher confirmation before finalizing 上册/下册. |
| 课题名称 | SOURCE_CONFLICT | Observed labels include 色彩的渐变, 色彩明度渐变, 色彩的纯度渐变. | Use 《色彩的渐变》 as candidate title only; keep teacher_review_required=true. |
| 单元名称 | NEEDS_TEACHER_CONFIRM | R93 and a public resource snippet mention 第二单元《多彩的世界》, but no official textbook page was verified. | Do not write as confirmed. Mark 第二单元《多彩的世界》 as candidate. |
| 第几课 | NEEDS_TEACHER_CONFIRM | Newer resource snippets say 第1课, but official textbook pages were not verified. | Use 第1课候选 only. |
| 教材页码 | DO_NOT_WRITE_AS_FACT | No reliable page image or official page number was verified in this repair. | Remove page-number claims such as 教材第6-7页. |
| 后续课题 | NEEDS_TEACHER_CONFIRM | A public resource snippet mentions 第2课《渐变的节奏》; no official textbook source was verified. | Keep as source gap and teacher-confirm item. |
| 本课核心概念 | SOURCE_CONFLICT | IMA and public resources mix 明度 / 纯度 / 色相 / 综合渐变. | Until teacher confirms textbook, use safe preview focus: color continuous change,端色,中间色,过渡方向,层次变化. |

Allowed status values:

```text
CONFIRMED
NEEDS_TEACHER_CONFIRM
SOURCE_CONFLICT
DO_NOT_WRITE_AS_FACT
```

Source references used for conflict audit:

- `zxxk_2025_2026_sync_snippet`: https://www.zxxk.com/docpack/3659930.html；2025-2026学年苏少版美术三年级下册同步课件 includes 第二单元第1课《色彩的渐变》 and 第2课《渐变的节奏》.；audit_use=Supports that this newer-looking naming exists, but not enough to write as official textbook fact.
- `dzkbw_org_susan_3s`: https://www.dzkbw.org/book/7402.html；Page says the listed 苏少版三年级美术上册 book is not in the 2025 national textbook catalog, and lists 第1课 色彩明度渐变.；audit_use=Shows 明度渐变 is associated with 三年级上册 on at least one catalog page, and the page itself warns current-use risk.
- `haoduoyun_2012_susan_3x_snippet`: https://www.haoduoyun.cc/book/sjb/meishu/mi3x/3.shtml；Old 2012 苏少/苏教三年级美术下册 catalog snippet lists 第1课 色彩的纯度渐变.；audit_use=Shows older 三下 resources may anchor the first lesson to 纯度渐变 rather than general 色彩的渐变.
- `yanxiuwang_video_resource_snippet`: https://m.yanxiuwang.cn/Course/play/course_id/31173.html；Video resources list 苏少版三年级下册 色彩的明度渐变 and nearby 色彩的纯度渐变 entries.；audit_use=Shows teaching-resource pages mix 明度 and 纯度 labels; not authoritative enough for final anchor.

Do not write as confirmed fact in R93-P1:

```text
苏少版2026春三年级下册第二单元第1课
教材第6-7页
后续第2课必为《渐变的节奏》
本课一定主攻明度渐变
本课一定主攻纯度渐变
本课同时完整主攻明度、纯度、色相
```
