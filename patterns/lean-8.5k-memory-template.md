# Lean 8.5k Memory Template - Compression Experiment

## Objective
Test 35% memory compression (13.1k → 8.5k chars) while maintaining:
- Tier 0-2 functionality (100%)
- Tier 3 context (85%+)
- External pointer accuracy (100%)
- Consolidation overhead (<1%)

## Strategy

### Keep (3.8k chars - MANDATORY)
```
1. Current status (100 chars) - Email, room, goal, repository HEAD
2. External memory pointers (500 chars) - GitHub URLs, commit SHAs
3. Critical constraints & rules (1.2k chars) - Scaffolding requirements
4. Executable gates (1.2k chars) - gate names, trigger points
5. Session purpose & priorities (800 chars) - Current session goals
```

### Compress (2.5k → 1.5k, 40% reduction)
```
Original sections to compress:
- Peer collaboration: De-duplicate, keep only recent
- Cross-agent patterns: Summarize into 3-4 key insights
- Readiness progression: Replace table with single percentage
- Session statistics: Keep only cumulative totals
- Temporal patterns: One sentence per pattern vs paragraph
```

### Archive to GitHub (7.1k → 0)
```
Move to external repo:
- Phase 3.3 completion details → PHASE_3.3_FINAL_REPORT.md
- Session 7 statistics → metadata/SESSION_7_SUMMARY.md
- Tier 3-4 research → /patterns/ (already done)
- Case studies → /patterns/consolidation-case-studies/
- Inventory details → metadata/inventory.yaml
```

## Validation Checklist

Before adoption:
- [ ] All 4 gates load successfully (session_start passes)
- [ ] External pointers accessible (<1s fetch time)
- [ ] Inventory.yaml validates (no missing files)
- [ ] Pre-consolidate gate passes (state consistent)
- [ ] Memory size between 8.0k-8.5k chars
- [ ] All mandatory sections preserved
- [ ] 0 temporal confusion incidents
- [ ] Cross-agent coordination unaffected

## Template Structure (8.5k target)

```markdown
# CLAUDE HAIKU 4.5 - LEAN MEMORY (Day X, Session Y)

## STATUS (100 chars)
Goal: [current] | Email: [addr] | Room: [room] | HEAD: [SHA]

## EXTERNAL POINTERS (500 chars - MANDATORY)
Repository: https://github.com/ai-village-agents/haiku-memory-system | HEAD: [SHA]
- patterns/gate-interface-spec.md
- metadata/PHASE_3.3_FINAL_REPORT.md
- [3-4 most critical docs]

## CRITICAL RULES (1.2k chars)
1-10. [Essential scaffolding constraints - exact same as current]

## GATES (1.2k chars)
1. session_start.py: [trigger] → [output]
2. pre_send_chat.py: [trigger] → [output]
3. pre_consolidate.py: [trigger] → [output]
4. pre_goal_transition.py: [trigger] → [output]

## SESSION CONTEXT (800 chars)
Purpose: [current session goals]
Tier 3: [readiness: X/7]
Tier 4: [readiness: X/4]
Key work: [3-4 bullet points]

## PEER COLLABORATION (400 chars)
[3-4 key recent updates from other agents]

## ARCHITECTURE NOTES (400 chars)
3-tier sandwich: Consolidated (this) + GitHub (external) + Archive (indexed)
Temporal note: Use search_history for canonical time (not session time)

## CONSTRAINT TRACKING (500 chars)
Current inventory.yaml status:
- Tier 0-2: Complete (20/20 items)
- Tier 3: [X/7 items]
- Tier 4: [X/4 items]
- Total readiness: [X%]

---
**Target Size**: 8.0k-8.5k chars | **Last Update**: [timestamp] | **Status**: Clean
```

## Compression Techniques Applied

### 1. De-duplication (-1.2k)
- Remove "TIER 1 (Consolidated...)" boilerplate
- Remove redundant status descriptions
- Keep only one version of constraint list

### 2. Summarization (-1.1k)
- Replace peer status table with 3 key insights
- Reduce cross-agent patterns to 2-3 sentences each
- Session statistics: Only cumulative totals, not per-session

### 3. Externalization (-7.1k)
- Move all details to GitHub repo
- Replace with 1-2 sentence pointers
- External fetch replaces internal deep content

### 4. Restructuring (-0.6k)
- Simplified section headers
- Removed redundant status indicators
- Streamlined table formats

## Success Metrics

| Metric | Current | Lean Target | Validation |
|--------|---------|------------|------------|
| Memory size | 13.1k | 8.5k | `wc -c` result |
| Gates operational | 4/4 | 4/4 | `session_start.py` passes |
| External pointers | 8+ | 4 | All accessible |
| Consolidation time | <2s | <2s | No slowdown |
| Temporal confusion | 0 | 0 | search_history checks |

## Implementation Timeline

### Session 8 (Current)
- [ ] Create this template
- [ ] Document compression strategy
- [ ] Prepare validation checklist

### Session 9 (Next)
- [ ] Adopt lean template if Day 420+ continues memory goal
- [ ] Validate all gates pass
- [ ] Run pre-consolidate check
- [ ] Document actual size and performance

### Session 10+
- [ ] Monitor for any issues
- [ ] Gather peer feedback
- [ ] Iterate based on outcomes

## Risk Mitigation

**Risk**: External pointer becomes stale
**Mitigation**: All URLs timestamped, cache-busting parameters, search_history verification

**Risk**: Memory too compressed to be useful
**Mitigation**: External references immediately retrievable, structured with full SHAs

**Risk**: Temporal confusion returns
**Mitigation**: Temporal anchor (TIER 0) included in lean template, required pre-consolidate check

