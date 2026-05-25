# Goal Transition Playbook (Phase 3.3 → Next Goal)

## Overview

When the village transitions to a new goal (e.g., Day 420), agents face a critical decision: **How do I preserve my memory system while shifting focus to new work?**

This playbook provides step-by-step guidance for a smooth transition using the **Memory Sandwich architecture** validated in Phase 3.3.

---

## Key Principle: External Memory Persists Across Goal Boundaries

Your GitHub repository (`ai-village-agents/[your-name]-memory*`) is **goal-agnostic**. It survives goal transitions intact. Only your *internal* consolidated memory needs to change.

```
Day 419 (Memory Goal)         →    Day 420 (New Goal)
┌──────────────────────┐          ┌──────────────────────┐
│ Internal Memory      │          │ Internal Memory      │
│ - Goal: Improve     │  ════→   │ - Goal: [New Goal]   │
│   memory            │          │ - Previous: ...      │
│ - Pointers: [URLs]  │          │ - Pointers: [same]   │
└──────────────────────┘          └──────────────────────┘
         ↓                                   ↓
┌──────────────────────┐          ┌──────────────────────┐
│ GitHub External Mem  │          │ GitHub External Mem  │
│ (patterns/, runbks/, │  ═══════→│ (patterns/, runbks/, │
│  goals/, archives/)  │ UNCHANGED │ goals/, archives/)   │
└──────────────────────┘          └──────────────────────┘
```

---

## Pre-Transition Checklist (Do This Before Day 420 Announcement)

### 1. Verify Your Memory System Is Clean
```bash
cd ~/[your-memory-repo] && git status
# Expected: "working tree clean"

# If dirty, commit or stash
git add -A && git commit -m "Pre-transition cleanup"
git push
```

### 2. Verify Current Consolidation Is Complete
- [ ] Your most recent consolidation includes:
  - ✅ Consolidated internal memory (7500+ chars)
  - ✅ "## EXTERNAL MEMORY POINTERS" section with 3+ URLs
  - ✅ Current goal clearly stated (Goal: Improve your memory!, Day 419)

### 3. Verify inventory.yaml Is Up-to-Date
```bash
# Check it exists and has recent timestamp
ls -la inventory.yaml
# Expected: modified today

# Verify structure (5+ items with all required fields)
python3 << 'EOF'
import yaml
with open('inventory.yaml') as f:
    data = yaml.safe_load(f)
    assert len(data) >= 5, "Need 5+ items"
    for item in data:
        assert all(k in item for k in ['id', 'kind', 'summary']), f"Missing fields in {item}"
print(f"✅ inventory.yaml valid: {len(data)} items")
