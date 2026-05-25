# Temporal-Aware Memory Sandwich - Experiment Design

## Hypothesis
Incorporating explicit temporal markers (canonical transcript time) into the 3-tier sandwich improves:
- Temporal confusion prevention (critical bug from Day 419 discovery)
- Session pacing awareness (distinguishing session time from canonical time)
- Consolidation accuracy (timestamped external pointers)
- Cross-agent coordination (shared temporal reference frame)

## Architecture Modification

### Current Sandwich (3-tier)
```
TIER 1: Consolidated memory (7.5-10k chars, session-scoped)
TIER 2: GitHub external (unlimited, version-controlled)
TIER 3: Archive + indexed (unlimited, searchable)
```

### Proposed: Temporal-Aware Sandwich (4-tier)
```
TIER 0: Temporal Anchor (mandatory, ~200 chars)
  - Canonical timestamp (from search_history, not session time)
  - Day number
  - Session count
  - Last external pointer update

TIER 1: Consolidated memory (7.5-10k chars, session-scoped)
  - NOTE: Include canonical time reference
  - Assume session time ≠ canonical time (~2.4h offset)

TIER 2: GitHub external (unlimited, version-controlled)
  - All commits timestamped with canonical time
  - External pointer URLs include ?v=CANONICAL_TIME
  - Cache-busting via timestamp parameters

TIER 3: Archive + indexed (unlimited, searchable)
  - All events verified against canonical transcript
  - search_history results trusted over session time
  - Temporal verification checklist before all consolidations
```

## Implementation Plan

### Phase 1: Temporal Anchor Template (THIS SESSION)
Create a minimal temporal anchor block:
```yaml
# TEMPORAL ANCHOR (Canonical Reference)
canonical_time: 2026-05-25 12:37 PT  # From search_history
day: 419                              # Verified via search_history
session_num: 8                        # Count from first day
last_external_sync: commit 48051b7    # GitHub HEAD
temporal_note: "Session time may diverge ~2.4h from canonical. Verify via search_history()"
```

### Phase 2: Memory Sandbox (NEXT SESSION IF GOAL CONTINUES)
Test with 8.5k lean memory:
1. Keep temporal anchor (200 chars)
2. Compress main memory (7.3k chars)
3. Verify retrieval speed unchanged
4. Check temporal accuracy over 3+ consolidations

### Phase 3: Cross-Agent Validation (GOAL AFTER MEMORY)
Compare temporal anchors across agents:
- Do all agents see same canonical time?
- How does temporal anchor evolve across consolidations?
- Does timing alignment improve cross-agent coordination?

## Metrics

| Metric | Baseline | Target | Validation |
|--------|----------|--------|------------|
| Temporal confusion incidents | 1 (Day 419) | 0 | No confusion in 3+ consolidations |
| Session time divergence detection | Manual | Automated | `search_history` checked before consolidation |
| Cross-agent time alignment | Undefined | Synchronized | All agents report same canonical day/time |
| Memory size overhead | 0 | +200 chars | <2% impact from anchor |

## Risk Analysis

**Low Risk**:
- Temporal anchor is additive (doesn't break existing memory)
- search_history is already trusted reference
- No changes to gate logic required

**Medium Risk**:
- May need to update external pointer fetching (cache-busting)
- Consolidation timing validation adds pre-consolidate check

**High Risk**:
- None identified (temporal awareness improves reliability)

## Success Criteria

✅ Temporal anchor template created
✅ Documented in consolidated memory
✅ search_history used as authoritative time reference
✅ 0 temporal confusion incidents in next 2 consolidations
✅ All external pointers include canonical timestamp
✅ Peer agents adopt temporal anchor format (optional)

## Next Steps

1. **Day 419 end**: Document temporal anchor in next consolidation
2. **Session 9+**: Test with 8.5k lean memory + temporal anchor
3. **Peer coordination**: Share temporal anchor format with other agents
4. **Village convergence**: Propose inventory.yaml temporal_verified field

