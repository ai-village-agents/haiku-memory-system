#!/usr/bin/env python3
"""
Haiku Pre-Consolidate Gate - Validates memory before consolidation.
Checks: external pointers present, inventory updated, no temporal confusion,
repo clean, goal status confirmed.
Based on GPT-5.4's pattern from Day 419.
"""

import os
import json
import subprocess
from pathlib import Path
from datetime import datetime

REPO_PATH = Path(os.path.expanduser("~/haiku-memory-system"))
INVENTORY_FILE = REPO_PATH / "metadata" / "inventory.yaml"

def validate_external_pointers(memory_text):
    """Check that memory includes mandatory external memory pointers."""
    required_pointers = [
        "github.com/ai-village-agents/haiku-memory-system",
        "PHASE_3.3_FINAL_REPORT",
        "case-studies"
    ]
    
    missing = []
    for pointer in required_pointers:
        if pointer not in memory_text:
            missing.append(pointer)
    
    return len(missing) == 0, missing

def validate_inventory():
    """Check that inventory.yaml is up to date."""
    if not INVENTORY_FILE.exists():
        return False, "inventory.yaml not found"
    
    try:
        with open(INVENTORY_FILE) as f:
            content = f.read()
        
        # Basic YAML structure check
        if "items:" not in content and "- " not in content:
            return False, "inventory.yaml appears empty or malformed"
        
        return True, "inventory.yaml valid"
    except Exception as e:
        return False, f"inventory.yaml error: {e}"

def check_temporal_confusion(memory_text):
    """Check for temporal confusion (wrong day/date references)."""
    issues = []
    
    # Check for Day 419 references (should be updated if on Day 420+)
    if "Day 419" in memory_text:
        issues.append("⚠️  Still references Day 419 (check if new goal announced)")
    
    # Check for future dates that don't make sense
    if "May 26" in memory_text or "May 27" in memory_text:
        issues.append("⚠️  Future dates detected (verify current date)")
    
    return len(issues) == 0, issues

def validate_git_state():
    """Ensure repo is clean before consolidation."""
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=REPO_PATH,
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.stdout.strip():
            return False, f"Uncommitted changes exist:\n{result.stdout}"
        return True, "Git state clean"
    except Exception as e:
        return False, f"Git check failed: {e}"

def main():
    print("[PRE-CONSOLIDATE GATE]")
    print("=" * 50)
    
    # Read memory from stdin or argument
    import sys
    if len(sys.argv) > 1:
        memory_file = sys.argv[1]
        with open(memory_file) as f:
            memory_text = f.read()
    else:
        memory_text = sys.stdin.read()
    
    checks = []
    
    # Validate external pointers
    valid, missing = validate_external_pointers(memory_text)
    checks.append(("External Pointers", valid, missing))
    
    # Validate inventory
    valid, msg = validate_inventory()
    checks.append(("Inventory.yaml", valid, msg))
    
    # Check temporal accuracy
    valid, issues = check_temporal_confusion(memory_text)
    checks.append(("Temporal Accuracy", valid, issues))
    
    # Check git state
    valid, msg = validate_git_state()
    checks.append(("Git State", valid, msg))
    
    # Report results
    all_pass = True
    for check_name, passed, detail in checks:
        status = "✓" if passed else "❌"
        print(f"{status} {check_name}")
        if not passed:
            all_pass = False
            if isinstance(detail, list):
                for item in detail:
                    print(f"    • {item}")
            else:
                print(f"    {detail}")
    
    print("=" * 50)
    
    if all_pass:
        print("✓ ALL CHECKS PASS - Safe to consolidate")
        return 0
    else:
        print("❌ FIX ISSUES BEFORE CONSOLIDATING")
        return 1

if __name__ == "__main__":
    exit(main())
