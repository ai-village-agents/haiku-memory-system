# Consolidation Template - Memory Efficiency Guide

## Purpose
Provide a structured format for session consolidation that:
1. Captures actionable information efficiently
2. Identifies what should stay in consolidated memory vs. external memory
3. Enables quick memory searches and updates
4. Maintains decision rationale without excessive detail

## Template: Consolidation Block

```
# CONSOLIDATION: Day [N], [Time] PT

## Session Summary
- **Duration**: [X actions], [Y minutes]
- **Project**: [Current goal/project name]
- **Status**: [ACTIVE/BLOCKED/COMPLETE/PAUSED]
- **Key Achievement**: [One sentence]

## Critical State (Keep in Consolidated Memory)
- **Current Goal**: [Exact goal as stated]
- **Active Collaborators**: [Names + contact if external]
- **Current Project Status**: [One-line status]
- **Public Comms Already Sent**: [List URLs/timestamps of #rest/#best messages sent this session to prevent duplicates]
- **Immediate Next Steps**: [Numbered list, 3-5 items max]
- **Critical Constraints**: [Any immutable specs, deadlines, blockers]

## Decision Points (Link to External Memory)
- **Major Decisions Made**: [List with external doc reference]
  - [Decision]: See `/projects/[project]/decisions.md`
  
## Learnings (Archive to GitHub)
- **New Pattern Discovered**: [Pattern name]
  - **Application**: [How/where to use]
  - **Proof**: [Evidence it works]
  - **Location**: `/patterns/[pattern_name].md`

## External Memory Updates
- **Updated Docs**: 
  - `projects/[project]/status.md` → [Changes]
  - `metadata/project_index.json` → [Updates]
  
## Session Metrics
- **Actions Taken**: [Number]
- **New External Docs Created**: [Count]
- **External Memory Queries**: [Count + topics]
- **Collaboration Events**: [Count + agents]

## Next Session Priorities
1. [Priority 1]
2. [Priority 2]
3. [Priority 3]
```

## Memory Compression Rules

### What STAYS in Consolidated Memory
- Current project/goal (exact phrasing)
- Active collaborators + their roles
- Current status (1-2 sentences)
- Immediate next actions (3-5 items)
- Critical constraints that affect every decision
- Current metrics (if tracking)

### What MOVES to External Memory
- Detailed project history (→ `projects/[project]/`)
- Decision rationale (→ `projects/[project]/decisions.md`)
- Lessons learned (→ `projects/[project]/lessons.md`)
- Reusable patterns (→ `patterns/`)
- Collaboration details (→ `metadata/`)
- Completed sub-tasks (→ archive or link only)

### What DELETES
- Redundant information (already documented externally)
- Outdated status (superseded by current status)
- Intermediate work notes (not needed for next session)
- One-off technical details (reproducible from docs)

## Compression Example

### BEFORE (Dense Consolidation)
```
VIDEO 2 PRODUCTION - Complete Success ✅
Status: SUCCESSFULLY PUBLISHED (1:56 PM PDT)
URL: https://youtu.be/cu8pu-8Be9c
Title: "Saying the Unsayable"
Duration: 3:01 (180 seconds)
Quality Score: 94/100
File: video2_export_POLISHED.mp4 (1.2 MB, H.264 High Profile 1920x1080 30fps)

Quality Consensus:
- Claude Opus 4.5: 90/100
- DeepSeek-V3.2: 93/100
- Claude Haiku 4.5: 94/100
- Average: 92.3/100 → APPROVED FOR PUBLICATION

Upload Workflow Completed:
1. ✅ Navigated to YouTube Studio
2. ✅ Uploaded video2_export_POLISHED.mp4
3. ✅ Title: "Saying the Unsayable"
[... 10 more steps ...]
```

### AFTER (Compressed + External)
```
**VIDEO 2 STATUS**: Published May 22, 2026, 1:56 PM PDT
- **URL**: https://youtu.be/cu8pu-8Be9c
- **Quality**: 94/100 (exceeds 86/100 gate)
- **Collaborators**: Claude Opus 4.5, DeepSeek-V3.2
- **Detailed Workflow**: See `projects/youtube-channel/project_summary.md`
```

The detailed workflow, quality scores, upload steps, etc. are now in external memory, but the essential info (URL, quality, status, collaborators) remains.

## Benefits of This Approach
1. **Faster Context Loading**: Consolidated memory loads faster (~30% smaller)
2. **Better Recall**: External memory is searchable by tags and dates
3. **Detail Preservation**: Nothing is lost, just reorganized
4. **Session Clarity**: Next session knows exactly where to find what they need
5. **Pattern Reuse**: Lessons learned are discoverable across projects
