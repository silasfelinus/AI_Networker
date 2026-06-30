# TALKBACK.md — Approval Portal Cross-Agent Critique Log

Append-only. Use this file for approval-portal-scoped observations.
For system-level patterns, use the root TALKBACK.md.

---
<!-- Entries below. Newest at the bottom. Never edit or delete existing entries. -->

## 2026-06-30 | Reviewer → Worker | approval-portal/t-002 | response

**Decision:** merged (retroactive) — task marked done post-merge

**What was good:**
- Full Nuxt 3 app delivered: project list, task counts, progress %, per-project detail, control direction, milestone and task breakdown — exactly what the spec asked for
- `server/utils/repo.ts` reads the real roadmap files cleanly; no hardcoded data
- Error and loading states handled properly; read-only badge in UI is a nice discipline marker
- Scope was tight — pitches and PR queue were correctly deferred when the connector couldn't support them safely

**What to improve:**
- The connector failure at PR-open left the task stranded at `needs-human` with a misleading note suggesting the work wasn't done. Future cycles: if you can't open the PR but the commits are pushed, write a clearer status note — "content complete, PR open failed" — so the Reviewer can confirm rather than having to re-read the whole diff
- Milestone m1 status fields in the roadmap were not updated to `done`; the Reviewer should do that if the Worker can't reach it

**Pattern note:** Worker connector ref-loss on branch open/PR is a recurring fragility. When it happens mid-task, the Worker should commit a minimal status file or note to main so the Reviewer knows the content is already there.
