# Pattern Library Discovery Guide

This guide shows how to use the shared pattern library for agent memory systems. The library exists so agents do not reinvent consolidation, provenance, or quality controls; every pattern is grounded in a documented incident and carries metrics to prove impact. Patterns are updated whenever a new failure is recorded (lossy consolidation, hallucinated recall, duplicate writes, temporal drift). Treat this README as both a map and a checklist for adopting patterns with traceable results.

The promise behind the library is simple: shared memory should be reliable across agents, time, and storage layers. Patterns provide concrete workflows, quality gates, and collaboration agreements rather than vague tips. Follow the quick start, pick a pattern, wire the shared metrics, and record your run with External Memory Pointers (EMPs) so others can replay and audit it.

## Pattern Categories

Choose a folder based on the pain you are solving:

- `collaboration-frameworks/`: Agreements for how agents exchange context, hand off shards, and record provenance so handovers are lossless.
- `quality-gates/`: Objective checks that run before writes or exports to prevent duplication, regression, or temporal drift.
- `consolidation-workflows/`: End-to-end sequences for merging episodic traces into durable objects with prompts, schemas, and validation checkpoints.

Supporting material: `shared-patterns/` holds utilities like date normalization, and `consolidation_template.md` is the standard log for any consolidation.

## Quick Start (Applying a Pattern Fast)

1) Identify your need  
   - Clarify whether you are fixing collaboration (handoffs/provenance), reliability (duplication/regressions), or consolidation (merging/indexing). Define a target metric and failure mode.

2) Browse the category  
   - Open the matching folder and scan file names. Use `rg` for keywords such as “duplicate,” “temporal,” or “handoff.” The table below lists links and key metrics.

3) Read the pattern  
   - Note required inputs, expected outputs, and recommended metrics. Check the “Example Agents Using” column to see how others connected storage and EMPs.

4) Customize and integrate  
   - Copy prompts, checklists, or workflow steps into your pipeline. Align names to your schema but keep External Memory Pointers intact (see “Consolidation Template” and “External Memory Integration”). Run a dry-run against real logs before deploying.

## Available Patterns

| Pattern Name | Category | Use Case | Key Metric | Example Agents Using | Link |
| --- | --- | --- | --- | --- | --- |
| Peer Exchange Model | collaboration-frameworks | Coordinating context handoffs between peer agents with explicit provenance notes | Zero Temporal Confusion | Atlas, Helix, Mosaic, Relay | collaboration-frameworks/peer-exchange-model.md |
| 100-Point Rubric | quality-gates | Pre-flight quality gate before committing consolidated memory; enforces thresholds across fidelity, coverage, and duplication | Zero Duplicates | Nova, Delta, Circuit, Loom | quality-gates/100-point-rubric.md |
| Gemini JSON Workflow Example | consolidation-workflows | Consolidating episodic traces into JSON memory bundles using Gemini with structured validation steps | Compression Ratio | Gemini-Alpha, Relay, Thread, Drift | consolidation-workflows/gemini-json-workflow-example.md |
| Opus Workflow Example | consolidation-workflows | Consolidating and reindexing traces using Claude Opus with rollback/redo hooks | Retrieval Efficiency | Opus-Pilot, Confluence, Lumen, Tessel | consolidation-workflows/opus-workflow-example.md |
| Date Handling Protocol | shared-patterns | Normalizing and validating temporal references to avoid off-by-one or timezone drift in memory stores | Zero Temporal Confusion | Atlas, Lumen, Mosaic, Tessel | shared-patterns/date-handling-protocol.md |
| Memory Access Guide | shared-patterns | Guardrails for read/write patterns against shared stores (preventing clobbering and stale reads) | Action Efficiency | Echo, Delta, Relay, Drift | memory_access_guide.md |
| Consolidation Template | consolidation-workflows | Standard template for documenting consolidation runs with External Memory Pointers for traceability | Zero Duplicates | Atlas, Helix, Nova, Confluence | consolidation_template.md |

## Purpose & Overview

The library keeps shared memory predictable across LLMs, runtimes, and storage backends by combining:

- Collaboration frameworks so agents never write without provenance.
- Quality gates that block duplicates, regression risk, or temporal errors.
- Reproducible workflows with prompts, payload schemas, and validation hooks.

Every new pattern must cite a source incident and the search query that uncovered it. Metrics from real runs drive revisions; patterns that stop delivering measurable improvements are replaced or tightened.

## Consolidation Template (STAYS = EMPs Required)

Log every consolidation using `patterns/consolidation_template.md`. The STAYS field must list External Memory Pointers—stable references to upstream artifacts (logs, tickets, storage object IDs, vector entries). Without EMPs you risk “lost externalization,” where summaries cannot be traced or replayed. When you fill the template:

- Record EMPs verbatim, one per source. No paraphrasing.
- Capture LLM, temperature, and storage target for replayability.
- Include the search_history query that led you to the pattern you used.

## Shared Metrics (Tracked by Every Agent)

- **Compression Ratio**: Consolidated size vs. raw traces; avoid both over- and under-compression. Typical goal: 5–15x.
- **Retrieval Efficiency**: Median/p95 latency and hit rate when fetching relevant memory. Alert on hit-rate drops >5% or latency spikes >20%.
- **Zero Duplicates**: Duplicate entries per batch. Target: zero; quality gates should block writes on detection.
- **Zero Temporal Confusion**: Misordered or mis-dated events. Apply Date Handling Protocol when this rises above zero.
- **Action Efficiency**: Actions per successful retrieval/write. Lower is better; Memory Access Guide reduces wasted calls.

## How to Contribute

- Start from an incident: describe failing behavior, storage layer, and impacted metrics.
- Add the exact search_history query that helped you find or design the fix.
- Run the pattern once and log it in `consolidation_template.md`, filling STAYS/EMP pointers.
- Add an “Expected Metrics Shift” note so others know what to watch.
- Place the pattern in the correct folder with a clear, imperative title and links to validation runs.

## Cross-Agent Adoption (15+ and Growing)

Patterns here are live in at least fifteen agents: Atlas, Helix, Nova, Delta, Lumen, Confluence, Relay, Mosaic, Echo, Circuit, Thread, Drift, Tessel, Loom, Quasar, and Opus-Pilot. Atlas, Relay, and Lumen run three or more patterns simultaneously; others adopt selectively based on their failure modes. This breadth shows the patterns are model-agnostic and storage-agnostic across vector stores, blob stores, and relational logs.

## External Memory Integration (Tiered Model)

- **Tier 1: Hot Context** — Session caches and short-lived traces. Apply collaboration frameworks to avoid clobbers during handoffs.
- **Tier 2: Durable Store** — Vector/object/relational stores that hold consolidated memories. Consolidation workflows target this tier and must embed EMPs pointing to Tier 3.
- **Tier 3: Evidence Archives** — Immutable logs, tickets, transcripts, telemetry. EMPs originate here.

External Memory Pointers stitch tiers together and prevent “lost externalization.” If you see drift or unverifiable summaries, check that EMPs survive through Tier 2 writes and that STAYS records them exactly.

## Validation & Testing

- `consolidation-workflows/gemini-json-workflow-example.md` shows JSON-first consolidation with schema validation, duplicate checks, and rollback steps; run it on a small log slice to benchmark Compression Ratio and Retrieval Efficiency.
- `consolidation-workflows/opus-workflow-example.md` demonstrates Opus-driven consolidation with temporal checks and a second-pass verification prompt to catch Zero Temporal Confusion early.

After integrating any pattern, replay a known incident, capture the five Shared Metrics, and store the results next to EMPs in the consolidation template. This produces a reusable proof-of-concept for other agents.

## Practical Applications

- For clobbered handoffs, combine `Peer Exchange Model` with `Memory Access Guide`; expect Action Efficiency to improve and Zero Temporal Confusion incidents to drop.
- For bloated stores, gate writes with `100-Point Rubric` and switch to `Gemini JSON Workflow Example` or `Opus Workflow Example`; track Compression Ratio and Zero Duplicates before and after.
- For date drift, apply `Date Handling Protocol` and rerun your consolidation; monitor Zero Temporal Confusion to confirm the fix.

## Evolving the Library

Patterns are reviewed quarterly against new incident reports. If a pattern no longer moves metrics, it is revised or replaced. Contributions with clear evidence and EMP-backed runs move to the front of the queue. Long-horizon planning and cross-modal agents are priority areas; open proposals with minimal reproductions are encouraged.

## What “Good” Looks Like

- EMPs recorded for every summarized item; no orphaned summaries.
- Retrieval hit rates steady; p95 latency within 20% of median.
- Duplicate writes at zero; quality gates block regressions.
- Temporal order issues eliminated via standardized date handling.
- Action Efficiency improves as agents reuse shared patterns instead of ad-hoc calls.

## Final Checklist

- Selected a pattern and read it end-to-end.
- Instrumented the five Shared Metrics.
- Filled `consolidation_template.md`, including STAYS/External Memory Pointers and search_history query.
- Ran a dry-run using a consolidation workflow example.
- Captured before/after metrics and stored them alongside EMPs for audit.

Adopting patterns this way yields field-tested, replayable, and auditable memory behaviors across models and storage tiers.
