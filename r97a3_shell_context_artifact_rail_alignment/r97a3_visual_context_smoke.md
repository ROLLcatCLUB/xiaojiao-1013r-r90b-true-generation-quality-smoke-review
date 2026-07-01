# R97A3 Visual Context Smoke

本轮在 R97A2 复制页基础上增加静态上下文联动层。

## 应看到

- `六、教学过程` 仍显示 P6 的 5 个教学节奏块。
- 每个 episode 下方出现大屏、学习单、观察项、小教上下文的轻量 chips。
- 右侧大屏草稿底部新增 `P6 课堂联动`，列出 episode 到 S01-S10、学习单、评价、小教提示的关系。
- 底部小教输入上方出现 `小教上下文预览` 折叠条。
- 教师下一步按钮均为 preview-only/no-op。

## DOM smoke

```text
r97a3-rail-panel = true
r97a3-episode-rail-item = true
r97a3-chip = true
P6 课堂联动 = true
小教上下文预览 = true
S01 / S02 = true
任务1 找一找 = true
看见变化 = true
preview only = true
六、教学过程 = true
一、本课依据 = true
```

## 视觉证据

- `r97a3_shell_context_dom_dump.html`
- `r97a3_shell_context_binding_preview_screenshot.png`

## 边界

- 不替换整页壳层。
- 不改原 R21/R36 core。
- 不 formal apply，不进入 R95，不生成正式 PPT/PDF/DOCX。
