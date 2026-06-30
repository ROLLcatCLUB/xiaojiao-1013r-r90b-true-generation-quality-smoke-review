# R93-P3 Teacher Reading Hierarchy Notes

## Decision

The teacher-facing teaching-process page must not expose all episode details at once.

## Default Reading Order

1. Classroom flow: the teacher first sees how the class moves from one episode to the next.
2. Paper-style numbering: fields should be grouped as 1.1, 1.2, 1.3 instead of displayed as cards.
3. Teacher action: each episode first shows what the teacher does and can say.
4. Student action: student work follows as a secondary layer.
5. Evidence: only the minimum evidence needed for classroom judgement is visible.
6. Folded details: design intent, screen plan, scaffolds, Xiaojiao support, misconceptions, and fallback strategies stay inside expandable sections.

## Shell Integration Gate

If the shell defaults to cards, a fully expanded field/schema view, or a dense dashboard-like reading experience, the teacher-facing shell should be treated as failed. Developer evidence can exist, but it must stay behind a folded evidence/developer mode.

## Boundary

- No R21/R36 modification
- No UI binding in this round
- No formal apply
- No PPTX or print-final generation
- No R95 execution
