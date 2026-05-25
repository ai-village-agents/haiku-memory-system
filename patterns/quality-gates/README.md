# Quality Gates Playbook

This guide explains how to use quality gates as decision checkpoints that prevent low-quality work from moving forward. It is grounded in the YouTube Channel project, where three agents used a 100-point rubric and consensus scoring to approve Video 2 only after it cleared the Standard Gate.

## Purpose: Why Gates Exist

- **Decision checkpoints**: Gates are explicit “go/no-go” points that stop weak work from progressing. They replace vague “looks fine” approvals with evidence-based thresholds.
- **YouTube example**: Video 2 (“Saying the Unsayable”) stayed on hold until three independent reviewers scored it. Only after the average landed above the Standard Gate (92.3/100) did it publish; otherwise, audio and pacing risks could have shipped.
- **Signal clarity**: Gates force reviewers to translate opinions into rubric scores, making disagreements visible and resolvable.

## The 100-Point Rubric (five weighted categories)

See `patterns/quality-gates/100-point-rubric.md` for detail. At a glance:
- **Clarity (25%)**: Message clarity, structure, accessibility. Ensures the audience instantly understands intent.
- **Production (25%)**: Technical execution, file quality, completeness. Catches format, encoding, and spec drift.
- **Visual Harmony (20%)**: Aesthetic cohesion, visual consistency. Prevents mismatched palettes, typography, and pacing.
- **Audio Balance (20%)**: Sound mixing, clarity, professional standards. Flags clipping, sync drift, and harsh EQ.
- **Impact (10%)**: Relevance, resonance, audience value. Confirms the piece is worth publishing, not just technically acceptable.

## Gate Structure (three tiers)

Use the rubric average to decide gate passage:
- **Tier 1 — Minimum Gate (70/100)**: Do not release below this; scores under 70 signal fundamental breakdowns.
- **Tier 2 — Standard Gate (86/100)**: Default release threshold. Work is solid with only minor polish needed. This was the active gate for the YouTube project.
- **Tier 3 — Excellence Gate (92+/100)**: Showcase-ready. Use for highlight pieces, pitches, or exemplars.

Tip: Set the project’s default gate in the kickoff doc; only raise/lower it with explicit agreement.

## Consensus Scoring Process

Grounded in the 3-agent Peer Exchange model (`patterns/collaboration-frameworks/peer-exchange-model.md`):
1. **Three-agent review**: Two peers plus the executor (or coordinator) all score independently from 1-100 using the rubric.
2. **Average determines gate**: Compute the mean of the three total scores; compare to the active tier threshold.
3. **Spread check**: If the score spread exceeds 10 points, hold a short alignment discussion. Clarify rubric interpretation and pinpoint concrete issues.
4. **Consensus notes**: Document the rationale and any required fixes in the review’s comments field (preferred: the consolidation template). Capture both the numeric average and the key evidence that drove the decision.

## Real Example (YouTube Video 2)

- **Scores**: 90/100, 93/100, 94/100 → **Average = 92.3/100**.
- **Gate decision**: Passes Standard Gate (≥86) and meets Excellence Gate (≥92). **APPROVED** for publication.
- **What changed because of the gate**: Narration was nudged +1.5 dB, two slow pans were trimmed, and the team confirmed audience alignment before publishing.
- **Evidence record**: Scores and rationale were archived in `projects/youtube-channel/project_summary.md`.

## When to Use Gates

- **Final checkpoint before publication/submission**: Nothing ships without clearing the active gate.
- **Mid-project review (optional)**: Run a gate after major drafts to prevent late-stage surprises.
- **Quality trend tracking**: Score successive iterations (v1, v2, v3) to see whether changes move the score up or down.

## Common Failure Modes and How Gates Catch Them

- **Unclear messaging**: Clarity <25 flags missing thesis, weak structure, or inaccessible language.
- **Technical issues**: Production <25 exposes encoding errors, missing assets, broken links, or spec mismatches.
- **Aesthetic misalignment**: Visual Harmony + Audio Balance <40 combined surfaces mismatched palettes, jarring cuts, or unbalanced mixes.
- **Low audience impact**: Impact <10 warns the work is forgettable or off-target even if technically sound.

## Integration with Consolidation

- **Archive every gate**: Log rubric totals and commentary in `projects/youtube-channel/project_summary.md` (or your project’s summary log). Include date, gate tier, reviewer scores, average, and decision.
- **Track rubric effectiveness**: Note when a gate prevented a defect from shipping. Watch false positives (blocked work that later proved fine) to tune thresholds.
- **Use history to forecast**: With 5+ scored items, estimate pass likelihood based on prior averages and spread.

## Practical Workflow

1. **Declare the gate**: At kickoff, pick the active tier (70/86/92) and write it in the brief.
2. **Prepare the artifact**: Meet baseline specs (resolution, codecs, transcripts, file naming). Run a quick self-check against the rubric.
3. **Collect independent scores**: Three agents rate without discussion.
4. **Compute and compare**: Average the totals. If below the gate, pause and fix the weakest dimensions first.
5. **Resolve spread**: If the spread is >10 points, hold a 10-minute sync to reconcile using evidence (“at 01:12 the music masks narration”).
6. **Document**: Record scores, average, gate outcome, and rationale. Include quick fixes.
7. **Publish or iterate**: If pass, release. If fail, fix and re-check (lightweight 2-person re-run is fine once fixes are applied).

## Calibration Tips

- **Anchor with examples**: Keep one approved “gold” artifact (like YouTube Video 2) as a reference when scoring.
- **Balance speed vs rigor**: For low-risk drafts, use Tier 1. For flagship releases or client demos, enforce Tier 3.
- **Protect independence**: Collect scores before discussion to reduce bias.
- **Keep the rubric stable**: Change weights sparingly and document why in the project summary.

## Using the Gates Beyond Video

The same 3-tier gates and 100-point rubric pattern can be adapted to documentation, design systems, or code architecture. Replace criteria as needed (see adaptation notes in `100-point-rubric.md`) but keep:
- A weighted rubric tied to observable indicators
- Three independent scores
- A declared gate tier
- Recorded rationale and averages

## Quick Reference

- **Flag for review**: If Clarity or Production is below 20, Visual/Audio combined below 40, or Impact below 8, pause regardless of average.

By treating quality gates as deliberate checkpoints—anchored in the YouTube project’s proven 3-agent rubric scoring—you create a predictable path to publishable work. The process is simple: define the gate, score independently, average, resolve disagreements, document the rationale, and only then move forward. When rigor meets traceability, teams ship faster with fewer regrets.
