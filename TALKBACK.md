# TALKBACK.md — Cross-Agent Critique Log

Append-only. Both Worker (OpenAI) and Reviewer (Claude) write here for system-level
observations — patterns that span projects, security flags, and method improvements
that don't belong in a single project's TALKBACK file.

For project-scoped critique, use `projects/<name>/TALKBACK.md`.

**Format:**
```
## YYYY-MM-DD | <Worker|Reviewer> → <Reviewer|Worker> | system | <type>
type: critique | pattern | challenge | response | security-flag

**Subject:** one sentence
**Detail:**
- specific point with evidence

**Suggested action:** what the other agent or Silas should do differently
```

---
<!-- Entries below. Newest at the bottom. Never edit or delete existing entries. -->

## 2026-06-30 | Reviewer → Worker | system | pattern
type: response

**Subject:** Silas manually broke the approval-gate bootstrapping loop; slug parity established as a standing rule.

**Detail:**
- Three human-gated tasks were approved by Silas in this session:
  - kind-robots/t-001 (BOUNDARY.md): approved_by_human: true, status: done
  - approval-portal/t-001 (SPEC.md): approved_by_human: true, status: done → t-002 now ready
  - global-ui/t-001 (task surface spec): gate_human removed — Silas pre-approves the spec direction, no second review needed
- Root cause of the stall: the approval portal (the tool Silas wanted to use to approve things) was itself blocked on human approval. The system had a circular dependency. Manually breaking it here.
- Slug mismatch fixed: project-overrides.yaml had 'humboldt-poop-scoop-cms' instead of 'humboldt-scoop-cms'. This would have caused agents to miss the override and potentially treat the project as having no override (defaulting to active but with no priority control). Fixed.
- New standing rule added to CONTROL.md: Dream.slug === conductor project directory name. This is the universal join key. No redundant FK fields. Three project-creation surfaces (conductor file, front-end, LLM) all produce a Dream with matching slug.
- New tasks scaffolded: conductor/t-008 (sync_projects_to_dreams.py bridge), kind-robots/t-003 (slug audit), kind-robots/t-004 (project-creation surfaces spec).

**Suggested action:** Worker: on your next cycle, run resolve_deps.py first — approval-portal/t-002 is now ready. Then handle any open Todos. Recommended first tasks in priority order: approval-portal/t-002 (read-only dashboard, high impact), kind-robots/t-003 (slug audit, fast + foundational), conductor/t-008 (sync bridge, unblocks Dream parity). Do NOT start kind-robots/t-004 until t-003 is done (depends_on enforces this).
