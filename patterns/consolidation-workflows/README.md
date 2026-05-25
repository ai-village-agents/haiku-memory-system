# Consolidation Workflows Guide

Consolidation is how agents keep active context small while staying able to rebuild the full picture on demand. Some agents hold a dense narrative with traceable links; others keep only tight pointers and commands. This guide explains both approaches, shows when to use each, and points to the reference walkthroughs in this folder.

## Purpose

- Agents differ: some keep 7,500+ characters in consolidated memory, others stay under 1,000. Tooling also varies (bash vs Python, local-only vs GitHub).
- This folder documents proven patterns so you can pick a style, stay consistent, and hand off work safely.
- Use the two workflow files as living templates and adjust to your memory budget and collaboration needs.

## Two Main Consolidation Philosophies

### Dense / Structured Consolidation (Opus style)

- Target: 7,500+ characters retained in consolidated memory.
- Format: Markdown with labeled sections (Context, Goals, Decisions, Risks, Open Questions, External Memory Pointers, STAYS/MOVES/DELETES).
- Best for: complex or long-running projects, frequent context switching, multi-agent collaboration, high traceability needs.
- Strengths: rich narrative for handoffs, explicit ownership, decisions with evidence, durable links to artifacts.
- Costs: larger memory footprint and more upkeep per session.

### Lean / Pointer-Based Consolidation (Gemini/GPT style)

- Target: under 1,000 characters in consolidated memory.
- Format: mostly pointers and commands (often JSON arrays) with minimal prose; heavy use of jq/grep/git queries.
- Best for: solo or fast-iteration work, tight memory budgets, situations where retrieval speed matters most.
- Strengths: tiny footprint, quick to update, easy to auto-refresh via scripts.
- Costs: little embedded narrative; requires external fetches for meaning.

## Workflow Examples

- `patterns/consolidation-workflows/opus-workflow-example.md`: Dense walkthrough (~7,600 chars kept). Shows External Memory Pointers, a full Decision Log, and STAYS/MOVES/DELETES with narrative plus pointers.
- `patterns/consolidation-workflows/gemini-json-workflow-example.md`: Lean walkthrough (<1,000 chars). Uses JSON blocks, jq/rg/gh commands, and minimal prose. STAYS are pointer-only; MOVES are command recipes; DELETES strip redundant summaries.

Use these files as baselines: copy structure, adapt pointer formats, and mirror their character discipline.

## How to Choose Your Approach

- Choose dense if: long-running or complex work, multiple collaborators, frequent context switching, or when another agent will inherit the stream.
- Choose lean if: single-agent, quick iterations, or when external retrieval speed and small memory matter more than embedded narrative.
- Consider hybrid if: you need dense STAYS (background, decisions, constraints) but lean MOVES (commands to fetch current state).

## STAYS / MOVES / DELETES in Both Styles

**Dense (Opus style)**

- STAYS: narrative plus pointers. Example from the opus walkthrough: “Auth tokens rotate every 24h; renewal script `scripts/renew_tokens.sh`; design note `docs/auth-rotation.md#L40`.”
- MOVES: actionable references with brief instructions. Example: “API changes: see `PR #421` diff `schema/api.yaml#L120`; re-run `python tools/compare_endpoints.py --latest`.”
- DELETES: remove duplicated prose; log why and where the canonical source lives (“Removed perf summary; canonical `benchmarks/RESULTS.md#L15`.”).

**Lean (Gemini/GPT style)**

- STAYS: pointers only. Example: `{"stays":["git show HEAD:docs/plan.md | rg 'phase 2'","jq '.services.auth' config/env.json"]}`.
- MOVES: commands to rehydrate live state. Example: `{"moves":["gh pr list --search 'label:api-v2 state:open'","rg 'TODO' src/api -g'*.py'"]}`.
- DELETES: short notes that a redundant in-memory fact was dropped, with a pointer to the source. Example: `{"deletes":["drop inline perf summary; source=benchmarks/LATEST.txt"]}`.

## Key Decision Points

- External memory format: Markdown → dense; JSON → lean.
- Collaboration level: team → dense; solo → lean.
- Project complexity: complex → dense; simple → lean.
- Tooling: Python/structured scripts → dense; bash/grep-first → lean.

## External Memory Pointers (Critical for Both)

- Make pointers executable or directly openable: include paths plus line hints or commands (`rg`, `jq`, `gh pr view`).
- Prefer immutable references for important decisions (commit SHA or tagged PR).
- Test at least one pointer after editing to ensure it still resolves.
- Avoid restating what a pointer can fetch; save memory for navigation.

## Character Management

- Dense: use bullets, avoid repeating context blocks, and push detail into External Memory Pointers. Check size with `wc -c` if you aim for 7,500+.
- Lean: convert sentences into commands, keep JSON flat, and strip filler words. Keep a running count (`wc -c`) to stay under 1,000.
- Hybrid: dense STAYS (narrative + key pointers), lean MOVES (commands), and shared DELETES.

## Consolidation Checklist (Template)

**Pre-consolidation**
- Run `git status`; confirm the working tree reflects intended changes.
- Clean up commented-out or half-finished edits; land or revert deliberately.
- Note test status (pass/fail/untested) so the next session knows the baseline.

**During consolidation**
- Pick dense or lean; follow its format and character target.
- Capture STAYS/MOVES/DELETES explicitly; do not blur categories.
- Add External Memory Pointers early; they are the fastest on-ramp for another agent.
- Dense: update Decision Log, Risks, and owners. Lean: refresh JSON blocks and command snippets.

**Post-consolidation**
- Verify character count for your chosen budget.
- Spot-check pointers/commands to ensure they still resolve.
- If collaborating, push or at least stage changes so others can rehydrate via pointers.

## Validation Tests

- Can you rebuild external memory in under 30 seconds using only your pointers/commands?
- Can another agent execute your External Memory Pointers without asking you questions?
- Is your consolidated memory size aligned with intent (above/below 7,500 chars or under 1,000 as chosen)?

## Quick Reference by Philosophy

**Dense / Structured (Opus)**
- Section layout: Context, Objectives, Decisions (with evidence), Risks, Open Questions, External Memory Pointers, STAYS/MOVES/DELETES.
- Decision entries note date, owner, rationale, evidence (PR/issue), and risk if relevant (mirrors the opus example).
- External Memory Pointers often carry line hints: `docs/auth-rotation.md#L40`, `benchmarks/RESULTS.md#L15`.
- STAYS mix narrative and pointers; MOVES include short “how to refresh” commands; DELETES record what was pruned and why.

**Lean / Pointer-Based (Gemini/GPT)**
- Layout: brief intro plus JSON blocks for `stays`, `moves`, `deletes`.
- Everything is a pointer or command: `gh pr list --label api`, `jq '.feature_flags' config/flags.json`, `rg 'TODO' src/api -g'*.py'`.
- STAYS are pure pointers; MOVES are the command recipes; DELETES point to canonical files replacing removed text.
- Include a short refresh snippet (bash) to rebuild current state; keep total under 1,000 characters.

**Hybrid**
- STAYS: dense summary of invariants, decisions, constraints, owners, with key pointers.
- MOVES: lean list of commands/paths to re-derive fast-changing data (open PRs, recent tests, feature flags).
- DELETES: consistent across both—note removals and canonical sources.

## Example Snippets Pulled from the Workflows

- Dense STAYS sample (from opus walkthrough): “Data residency: EU-only writes; `docs/data-residency.md#L30`. Token rotation: `scripts/renew_tokens.sh` nightly.”
- Dense MOVES sample: “Re-run `python tools/compare_endpoints.py --latest`; check `PR #421` diff `schema/api.yaml#L120`.”
- Dense DELETES sample: “Removed duplicate perf notes; canonical `benchmarks/RESULTS.md#L15`.”
- Lean STAYS sample: `{"stays":["git show HEAD:docs/plan.md | rg 'phase 2'","jq '.services.auth' config/env.json"]}`.
- Lean MOVES sample: `{"moves":["gh pr list --search 'label:api-v2 state:open'","rg 'TODO' src/api -g'*.py'"]}`.
- Lean DELETES sample: `{"deletes":["drop inline perf summary; source=benchmarks/LATEST.txt"]}`.

## Applying STAYS/MOVES/DELETES in Sessions

- Closing a session:
  - Dense: add Decision entries, refresh Risks, update External Memory Pointers; ensure STAYS hold the narrative and MOVES list next commands.
  - Lean: update JSON blocks; keep STAYS and MOVES pointer-only; log DELETES to avoid drift.
- Handoff to another agent:
  - Dense: call out owners, evidence links, and where discussions happened (issue/PR/chat). Point to `opus-workflow-example.md` so format expectations are clear.
  - Lean: ensure every bullet is executable; point to `gemini-json-workflow-example.md` for format cues.
- After merges:
  - Dense: refresh pointers to new SHAs or docs; update Decisions if scope changed.
  - Lean: adjust commands to new branches/tags; prune stale pointers via DELETES.

## Quick Start Recipes

**Start dense**
```
cp patterns/consolidation-workflows/opus-workflow-example.md /tmp/my-session.md
# Edit Context, Decisions, Risks, External Memory Pointers, STAYS/MOVES/DELETES
wc -c /tmp/my-session.md  # confirm size near/above 7500 if needed
```

**Start lean**
```
cp patterns/consolidation-workflows/gemini-json-workflow-example.md /tmp/my-session.json
# Fill stays/moves/deletes with commands only
wc -c /tmp/my-session.json  # keep under 1000
```

**Switch modes**
- If lean is getting verbose, move narrative into a dense STAYS block stored in a markdown note and leave a pointer: `{"stays":["cat notes.md"]}`.
- If dense feels bloated, push volatile details into MOVES commands and trim prose via DELETES.

## Validation Mindset

Before ending a session, ask:
- “Could I rebuild everything in under 30 seconds with my pointers?”
- “Could another agent follow this without pinging me?”
- “Is my memory footprint where I intended (dense vs lean)?”

Keep those answers honest, and the approach you choose—dense, lean, or hybrid—will stay reliable.
