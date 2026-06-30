# R94-P2 Field Lab Demote Decision

## Decision

`R88 + R94-P1 preview binding` is kept as an engineering audit page, not a teacher-facing shell sample.

## Status

- Engineering audit page: PASS
- Teacher-readable page: FAIL
- Shell integration sample: FAIL
- Reason: the page exposes low-level field slots and field-contract structure by default.

## Product Rule

Teacher-facing pages must use task, artifact, and review language first. Field keys, lineage, validators, and generation-slot details belong in a folded evidence/developer area.

## New Surface

`1013R_R94_P2_TEACHER_FACING_LESSON_PACKAGE_OVERVIEW` provides a separate static overview page for teachers.

## Boundary

- Does not modify R21/R36
- Does not bind to real UI
- Does not formal apply
- Does not write database/Feishu/memory
- Does not generate PPTX or printable final files
- Does not enter R95
