# Changelog — task

Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Versioning: [SemVer](https://semver.org/).

## [0.5.0] — 2026-09-07

### Changed
- Orca dispatch sequence and honest-supervision rules moved verbatim to `references/orca.md`; Fase 6 keeps a short pointer and the one-line `check --wait` command.
- Pre-flight CodeGraph rules replace index-age check: read both `status` lines (content vs engine version), `sync` does not replace full `index`, each worktree gets its own index at creation (`codegraph init` before dispatch, never during a worker run).
- Added common-error rows for wrong-tree index queries and judging an index by file date; warn never to stage `.codegraph/` inside a worktree (~201MB, often untracked).

## [0.4.0] — 2026-09-07

### Changed
- Fase 7 closes against FRD criteria **this subtask covers**, not the whole FRD; closing table gains owner column (`Dueño si no cumple`); unmet criteria owned by sibling subtasks are hand-offs, not failures.
- Fase 6 gains delegated code review method: brief without coordinator conclusions, fresh detached worktree at pushed commit, pre-existing-debt filter against base commit; coordinator re-verifies every finding and criteria row.
- `No tocar` git prohibitions now name safe alternatives: `git show` to read/compare commits, `git worktree add --detach` to work against another ref.
- Pre-flight and dispatch brief strengthen CodeGraph-before-grep: `codegraph explore`, `projectPath` filtering for mixed workspace indexes, index age check.
- Closing and resume checklist add stale worktree list/prune step (closing only, never mid-work).

## [0.3.0] — 2026-09-07

### Changed
- Removed Mill/`/delegate` dependency; `task` owns the five-part dispatch brief and talks to Orca orchestration directly (`orca-ide`, `check --wait`, `terminal send`, `worker-release`).
- Precedence ladder now matches document chain: FRD > Propuesta Técnica > Spec > Jira; Propuesta Técnica wins over Spec on conflict.
- FRD authorizes scope — Cambios Técnicos table is reference, not ceiling; shared paths (components, tokens, published contracts) still require raised hand.
- Fase 5 searches FRD for acceptance criteria without table rows; Fase 7 closes against FRD criteria, not rows implemented.
- Frontmatter description rewritten as triggering conditions only (no workflow summary).
- Backend reference: mocha reality documented — many specs cannot run under mocha yet; raise hand with alternative criterion instead of reporting green jest.
- Added branch confirmation before every audit pass, delegated code review gate before commit, one-commit-per-feature rule, and coordinator resume checklist.
- Supervision rules: `check --wait` timeout is checkpoint not failure, pending brief requires `terminal send --enter`, `worker: failed` with live terminal is not proof of failure.
- Dispatch step names `--from <coordinator_handle>` and states where the coordinator runs: inside an Orca terminal Orca resolves the sender itself, from outside `worker-start` fails with `no_active_sender_terminal`.
- The 9-criteria cap is per dispatch, not per subtask: when ticket plus FRD criteria exceed it, split the dispatch rather than dropping criteria.

## [0.2.0] — 2026-09-03

### Changed
- Skill rewritten as coordinator: locate documents, verify rows, convert acceptance criteria to runnable commands, delegate implementation via `/delegate` and Orca orchestration — no direct code writing in the working tree.
- Document chain enforced: FRD → Propuesta Técnica → Spec → Jira subtask; FRD must be opened, not just named.
- Branch/worktree mechanics, safety rules, and closing diff checks deferred to `/delegate` and Orca; wait contract is `check --wait` for `worker_done` / `escalation` / `question`.
- Closing requires FRD criteria table with evidence, not only green row tests.

### Added
- Mandatory `Do not touch` prohibition of `git reset`, `git checkout`, `git stash`, `git restore`, and `git clean` in every dispatch brief.
- Backend reference: `tsc -p tsconfig.build.json --noEmit` per row, project test command (`npm test` / mocha), forbid `jest <directory>`, `name.kind.ts` naming, throwaway scripts in `functions/scripts/`.

## [0.1.0] — 2026-08-31

### Added
- Initial `task` skill: execute a single Jira Development subtask against a refined Spec Técnica.
- Phases for locate, route front/back, contract precedence (FRD > Spec > Jira), branch check, verify-before-write, build, and close.
- Safety rules: blast radius, ownership zones, additive-over-mutative, design tokens, raised-hand shape, scope from table only, closing diff check.
- Reference files for frontend (Figma-first) and backend (repo context) workflows.
