# R97B Teacher Action Preview State Smoke

四个教师动作均为 preview_only/no-op：

- `继续打磨教学过程`：state=preview_only_noop，formal_apply_allowed=false，database_write_allowed=false，runtime_call_allowed=false。
- `预览课堂材料`：state=preview_only_noop，formal_apply_allowed=false，database_write_allowed=false，runtime_call_allowed=false。
- `准备导出预览文件`：state=preview_only_noop，formal_apply_allowed=false，database_write_allowed=false，runtime_call_allowed=false。
- `暂不采用`：state=preview_only_noop，formal_apply_allowed=false，database_write_allowed=false，runtime_call_allowed=false。

结果：PASS，未进入保存、导出、formal apply 或 R95。
