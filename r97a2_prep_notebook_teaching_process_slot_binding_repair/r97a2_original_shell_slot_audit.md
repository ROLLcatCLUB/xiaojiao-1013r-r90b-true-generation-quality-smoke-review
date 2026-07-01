# R97A2 原壳槽位审计

结论：P6 不是整页壳层，只能接入原备课本正文中的 `六、教学过程` 槽位。

## 原页结构

- `#renderLayer` 是当前视图渲染层，不是单课内容槽位。
- `renderPrepNotebookCanvas(view)` 保留备课室三栏：左侧备课本目录、中间单课正文、右侧大屏/课件草稿。
- 中间单课正文由 `beforeProcess -> renderProcessSection -> afterProcess` 组成。
- `beforeProcess` 包含本课依据、学情分析、教学目标、教学重难点、教学准备。
- `renderProcessSection(view, "六")` 对应教学过程，是本轮唯一绑定槽位。
- `afterProcess` 包含学习单与评价、课堂后记。

## 本轮绑定

- 复制原 R91A 壳层页。
- 不替换 `#renderLayer`。
- 不替换 `current_lesson.sections`。
- 仅用 R93-P6 的 5 个 episode 替换 `current_lesson.process_steps`。
- 同步修补 R21 unified package 的 `lesson.process_steps`，因为它是页面加载后的最终覆盖层。
- 同步修补 R21 `normalizeProcessSteps()`，让 P6 episode 不被压扁成旧的普通流程字段。
- 原壳的 `renderPrepRoomCanvas()` 负责重新渲染页面。

## 必须保留的章节

- `basis`
- `analysis`
- `goals`
- `keypoints`
- `preparation`
- `assessment`
- `reflection`
