# Pitch: Conductor PR Triage Board

date: 2026-06-26
project-target: ai-networker-itself
status: approved

## The idea
Add a repo-native triage board that summarizes open Worker PRs, their task status, mergeability, human gates, and the exact next action: reviewer merge, Silas approval, unblock dependency, or close stale branch. It can start as a generated Markdown file or JSON artifact, then become a read-only Approval Portal screen later.

## Why it's worth doing
Several Worker PRs are intentionally piling up, and the current roadmap statuses can drift from PR reality when branches are unstable or human-gated. A tiny triage board would make the loop easier to supervise without creating a second source of truth.

## Rough effort
medium

## Suggested first task
Create `scripts/build_pr_triage.py` that reads roadmaps plus recent GitHub PR metadata and writes `PR-TRIAGE.md` as a generated, reviewable snapshot.
