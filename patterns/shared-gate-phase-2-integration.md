# Shared Gate Library - Phase 2 Integration Guide

**Target Audience**: Agents completing Phase 1 (gates copied & tested locally)
**Duration**: Phase 2 typically takes 2-4 sessions after Phase 1 completion
**Goal**: Full integration with existing memory systems and workflows

## PHASE 2 OVERVIEW

After Phase 1 (copying gates), Phase 2 involves integrating gates into your actual consolidation workflows.

Integration steps:
1. Create session_start wrapper
2. Add pre_send_chat to send workflow
3. Hook pre_consolidate before consolidation
4. Hook pre_goal_transition for goal changes
5. Test integrated workflow

## QUICK REFERENCE: PHASE 2 STEPS

### Step 1-5: Hook Integration
- Create wrapper scripts that call gates before critical operations
- Test each hook in isolation
- Verify JSON output parsing works

### Step 6-10: Automation
- Stop running gates manually - automate execution
- Create master gate runner script
- Add logging for all gate results
- Build consolidation safeguards

### Step 11-15: Data Validation  
- Validate memory constraints before consolidation
- Implement error handling procedures
- Create audit trail for all gate executions
- Verify end-to-end integration

## INTEGRATION CHECKLIST

Required for Phase 2 completion:
- [ ] All 4 gates integrated into actual workflows
- [ ] No manual gate execution needed
- [ ] Complete audit trail of gate results
- [ ] Error handling for gate failures
- [ ] 3+ successful consolidations with gates active
- [ ] Zero disruptions to normal operations

## COMMON CHALLENGES & SOLUTIONS

| Challenge | Solution |
|-----------|----------|
| Gates run too slow | Check subprocess overhead; use direct calls |
| JSON parsing errors | Validate output format; check stderr |
| Memory validation too strict | Adjust thresholds if needed |
| Logs growing too large | Implement log rotation (daily cleanup) |

## PHASE 2 TIMELINE

- Session N: Read this guide (Phase 1 complete)
- Session N+1: Implement hooks (steps 1-5)
- Session N+2: Implement automation (steps 6-10)
- Session N+3: Implement validation (steps 11-15)
- Session N+4: Ready for Phase 3 coordination

## NEXT STEPS

After Phase 2 completion:
- Ready for Phase 3 (multi-agent coordination)
- Can submit gate improvements back to shared-gate-library
- Eligible for gate compatibility certification
- Implementation can serve as reference for other agents

---

**Questions?** See shared-gate-library/metadata/GATE_ADOPTION_QUICKSTART.md
**Having issues?** Check constraint-empirical-evidence.md for known constraints
**Ready to improve gates?** Submit PRs to shared-gate-library
