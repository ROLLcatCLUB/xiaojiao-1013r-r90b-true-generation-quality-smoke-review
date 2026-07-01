# R97A2 Visual Slot Smoke

结论：当前复制页已把 R93-P6 教师课堂导航内容接入原 R91A 备课本正文的 `六、教学过程` 槽位。

## 已验证

- 原壳层保留：顶部栏、左侧备课本目录、右侧大屏草稿、底部小教输入仍在。
- 原正文章节保留：`一、本课依据`、`二、学情分析`、`七、学习单与评价` 在渲染后的 DOM 中仍可见。
- P6 槽位接入：`六、教学过程` 中出现 `老师三步`、`学生产出`、`关键话术`、`小教提醒`。
- P6 细节折叠：`micro-step`、大屏、支架、小教和证据仍在原位折叠。
- 未替换 `#renderLayer`，未把 P6 当成整页壳层。

## 证据文件

- `R91A_slot_binding_dom_dump.html`
- `R91A_slot_binding_from_R93_P6_screenshot.png`
- `R91A_slot_binding_teaching_process_section_screenshot.png`

## DOM smoke patterns

```text
r97a2-p6-step = true
老师三步 = true
学生产出 = true
关键话术 = true
小教提醒 = true
一、本课依据 = true
二、学情分析 = true
六、教学过程 = true
七、学习单与评价 = true
```

## 边界说明

- 不修改原 R91A/R87 文件。
- 不修改原 R21/R36 合同或源文件。
- 复制页内适配 R21 最终覆盖层，避免 R93-P6 被旧 process steps 覆盖。
- 不 formal apply，不写数据库/飞书/记忆。
