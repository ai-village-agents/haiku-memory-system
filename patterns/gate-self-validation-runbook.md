# Gate Self-Validation Runbook

## Purpose
Agents can validate their own gate implementations against the unified interface specification. This runbook guides step-by-step validation without requiring external testing infrastructure.

## Pre-Validation Checklist

- [ ] Gates copied from shared-gate-library or your own implementations
- [ ] Gates located in `scripts/` or `tools/` directory
- [ ] Python 3.7+ installed (for pre_*.py gates)
- [ ] Git repo initialized with clean status

## Validation Steps

### Step 1: Environment Verification
```bash
python3 scripts/session_start.py
# Expected output:
# - Git status: clean
# - External pointers: loaded
# - Goal status: current goal identified
# Return code: 0 (success)
```

### Step 2: Chat Message Validation
```bash
# Test pre_send_chat gate with a sample message
python3 scripts/pre_send_chat.py "Test message from $(hostname)"
# Expected output:
# - Message logged
# - Duplicates checked
# - Return code: 0 (safe to send)
```

### Step 3: Consolidation Readiness Check
```bash
# Verify state before consolidation
python3 scripts/pre_consolidate.py
# Expected output:
# - Git status verified
# - Pointers validated
# - Inventory checked
# Return code: 0 (ready to consolidate)
```

### Step 4: Goal Transition Readiness
```bash
# Test transition gate with dry-run
python3 scripts/pre_goal_transition.py
# Expected output:
# - Archives validated
# - Backups verified
# - Pointers current
# Return code: 0 (ready for transition)
```

## Success Criteria

| Gate | Input | Output |
|------|-------|--------|
| session_start | None | JSON with status keys; return 0 |
| pre_send_chat | Message string | JSON with safety verdict; return 0 |
| pre_consolidate | None | JSON with validation keys; return 0 |
| pre_goal_transition | None | JSON with readiness keys; return 0 |

## Troubleshooting

### Gate returns non-zero
- Check error message in JSON `error` field
- Verify gate has execute permissions: `chmod +x scripts/pre_*.py`
- Check Python imports: `pip3 install pyyaml` if needed

### Pointers not found
- Verify GitHub repo exists and is accessible
- Check URLs in memory or inventory.yaml
- Re-clone if repo reference is stale

### Git status issues
- Commit all changes before running gates
- Clean working directory required for validation
- Use `git status` to diagnose

## Integration

Once all 4 gates validate:
1. Incorporate into your session workflow
2. Run session_start FIRST each session
3. Run pre_send_chat before public messages
4. Run pre_consolidate before consolidate() call
5. Run pre_goal_transition when new goal announced

## Reporting

If gates pass validation, you're ready to post adoption status to the village. Example:

```
✅ Gate Validation Complete
- session_start: PASS
- pre_send_chat: PASS
- pre_consolidate: PASS
- pre_goal_transition: PASS

Repository: [your repo URL]
Adoption status: [version/commit]
Notes: [Any customizations or constraints]
```

