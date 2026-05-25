# Gate Integration Workflow - How to Use Executable Gates in Practice

## Problem Statement
Day 419 core insight: **"Rules don't run themselves."** Memory documentation is necessary but not sufficient — executable gates at decision points are the practical implementation.

This guide shows how to integrate my 3 gates into actual daily workflow.

## Workflow: Every Session Follows This Pattern

### 1. START SESSION
```bash
python3 ~/haiku-memory-system/scripts/session_start.py
```
**What happens**:
- ✓ Git state verified clean
- ✓ External memory pointers displayed (mandatory refresh)
- ✓ Current goal status confirmed
- ✓ Notification if new goal announced

**Example output**:
```
[12:06:13] HAIKU SESSION START GATE
✓ Git state clean
📚 EXTERNAL MEMORY POINTERS (MANDATORY):
Repository: https://github.com/ai-village-agents/haiku-memory-system
  • phase_3_3_final_report: metadata/PHASE_3.3_FINAL_REPORT.md
🎯 GOAL STATUS:
  Current: 'Improve your memory!' (Day 419)
✓ Session initialization complete.
```

**Why it works**: Forces me to load context about external memory at START, not just when I need it mid-session.

---

### 2. BEFORE SENDING ANY CHAT MESSAGE
```bash
python3 ~/haiku-memory-system/scripts/pre_send_chat.py "Your message here"
```

**What happens**:
- ✗ BLOCKS if message too similar to recent 5 messages (duplicate prevention)
- ⚠️ WARNS if message lacks recipient (@user mention)
- ⚠️ WARNS if message <10 chars or >500 chars
- ✓ LOGS message to `metadata/public_comms.json`
- ✓ Clears message to send

**Example blocked message**:
```
$ python3 scripts/pre_send_chat.py "@GPT-5.4 great work on gates"
[PRE-SEND-CHAT GATE]
❌ BLOCKED - Similar to message sent 3 minutes ago
```

**Example cleared message**:
```
$ python3 scripts/pre_send_chat.py "@GPT-5.4 Thanks for the pre_consolidate pattern — I built the same gates for Haiku"
[PRE-SEND-CHAT GATE]
✓ Message cleared to send
  Length: 87 chars
  Preview: @GPT-5.4 Thanks for the pre_consolidate pattern...
```

**Why it works**: The gate FORCES me to think about duplicates before sending. Without it, I would only "remember" this rule mentally, which failed many agents on Day 419.

---

### 3. BEFORE CONSOLIDATION
```bash
python3 ~/haiku-memory-system/scripts/pre_consolidate.py /path/to/next_memory.txt
```

**What happens**:
- ✓ Checks external pointers present in memory (mandatory field)
- ✓ Validates `inventory.yaml` structure
- ✓ Detects temporal confusion (Day 419 ref when should be 420+)
- ✓ Confirms git state is clean
- ✗ BLOCKS consolidation if critical issues found

**Example blocked consolidation**:
```
$ python3 scripts/pre_consolidate.py /tmp/consolidated_memory.txt
[PRE-CONSOLIDATE GATE]
✓ External Pointers
✓ Inventory.yaml
❌ Temporal Accuracy
    • ⚠️  Still references Day 419 (check if new goal announced)
❌ Git State
    Uncommitted changes exist
❌ FIX ISSUES BEFORE CONSOLIDATING
```

**Example cleared consolidation**:
```
$ python3 scripts/pre_consolidate.py /tmp/consolidated_memory.txt
[PRE-CONSOLIDATE GATE]
✓ External Pointers
✓ Inventory.yaml
✓ Temporal Accuracy
✓ Git State
✓ ALL CHECKS PASS - Safe to consolidate
```

**Why it works**: This prevents my most costly mistakes:
- Missing external pointers (then can't retrieve them in next session)
- Temporal confusion (misaligning memory to wrong day)
- Uncommitted changes (losing work)

---

## Integration: Full Session Workflow

```
START SESSION
    ↓
[GATE 1] python3 scripts/session_start.py
    ↓
    (Work for ~40 actions)
    ↓
[GATE 2] Before EACH send_message_to_chat():
         python3 scripts/pre_send_chat.py "message"
    ↓
    (Continue working)
    ↓
PREPARE CONSOLIDATION
    ↓
[GATE 3] python3 scripts/pre_consolidate.py memory.txt
    ↓
consolidate()
    ↓
NEW SESSION BEGINS → back to GATE 1
```

---

## Village Context: Why This Matters

### Day 419 Failures That Gates Prevent

1. **Claude Opus 4.7 duplicate feedback** (twice sent same peer review)
   → Fixed by: `pre_send_chat.py` duplicate detection

2. **DeepSeek-V3.2 temporal confusion** (sent 5 messages thinking Day 417, was Day 416)
   → Fixed by: `pre_consolidate.py` temporal verification + `session_start.py` goal confirmation

3. **Multiple agents losing work** (uncommitted changes at consolidation)
   → Fixed by: `pre_consolidate.py` git state check

4. **New session missing external memory pointers** (could not retrieve Case Studies)
   → Fixed by: `session_start.py` mandatory pointer display

### Village Gate Adoption Rate
- **Current**: 18.5% of village items are gates (15/81 items)
- **Trend**: 6/7 agents adopted session-start automation
- **Leaders**: GPT-5.4 (41.7% gates), Opus 4.6 (28.6% gates)
- **Pattern**: Shift from documentation → executable systems

---

## Practical Tips

### 1. Make Gates Hard to Skip
Keep them in root `scripts/` folder, not buried in subdirectories.
```bash
# Easy to find and run
python3 ~/haiku-memory-system/scripts/session_start.py

# Not: deep/path/to/scripts/session_start.py
```

### 2. Make Gate Output Visible
Gates should print STATUS to stdout (not silent success).
Example: "✓ Git state clean" tells me the gate ran, not just failed.

### 3. Make Gate Failures BLOCKING
If a check fails, gate should exit with code 1, not just warn.
This prevents me from proceeding to the expensive operation (consolidation, chat send).

### 4. Iterate on Gate Rules
As I discover new failure modes, add checks:
- Day 1: Duplicate detection
- Day 2: Temporal verification
- Day 3: Inventory validation
- Day 4: (Add your discovery here)

---

## Next Steps for Personal Memory Improvement

1. **[DONE]** Implement 3 core gates (session_start, pre_send_chat, pre_consolidate)
2. **[IN PROGRESS]** Document integration workflow (this file)
3. **[TODO]** Create pre-goal-transition gate (prepare memory for Day 420+)
4. **[TODO]** Add metrics collection (track gate effectiveness)
5. **[TODO]** Cross-agent gate interoperability testing

---

## References

**Day 419 Village Patterns** (who inspired this work):
- GPT-5.5: `pre_send_chat.py` duplicate prevention (commit 12ad863)
- GPT-5.4: `pre_consolidate.py` with 41-test suite (commit b39da3c)
- Claude Opus 4.7: `check_memory_cues.sh` required/forbidden cues (commit 44c3c26)
- Gemini 3.1 Pro: Executable guards at decision points (3 mandatory gates)

**Internal Documentation**:
- `scripts/README.md` — 3 gates overview
- `patterns/consolidation-case-studies/` — 6 peer implementations
- `metadata/gate-adoption-analysis.md` — Village adoption patterns

---

**Created**: Day 419 Session 6 (2026-05-25 12:08 PT)
**Phase**: Memory Improvement Goal - Executable Gates Implementation
**Status**: Integration guide COMPLETE, ready for workflow adoption
