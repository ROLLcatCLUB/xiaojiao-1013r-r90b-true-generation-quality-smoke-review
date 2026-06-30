# R95 Export Preview Readiness Gate

Decision:

```text
R95_READINESS = READY_FOR_USER_AUTHORIZATION
R95_ALLOWED_NOW = false
R95_EXECUTED = false
```

Why R95 can be prepared next:

```text
P6 has solved the basic teacher reading hierarchy.
The next risk is no longer "how the teacher reads the lesson".
The next risk is whether classroom materials can be exported into previewable teacher-facing files.
```

Allowed R95 scope after explicit user authorization:

```text
PPTX preview
A4 学习单 preview
A4 教师观察表 / 学生自评表 preview
```

Still forbidden:

```text
不 formal apply
不写 R21/R36
不落库
不接真实 UI
不进入正式发布
不把预览文件标记为正式可用
```

Required R95 posture:

```text
preview only
teacher_review_required = true
formal_apply = false
```
