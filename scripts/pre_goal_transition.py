#!/usr/bin/env python3
"""
Haiku Pre-Goal-Transition Gate - Validates memory is ready for new goal.
Runs BEFORE new goal announcement is incorporated into memory.
Ensures no work is lost during goal transition.
"""

import os
import subprocess
from pathlib import Path
from datetime import datetime

REPO_PATH = Path(os.path.expanduser("~/haiku-memory-system"))
PROJECTS_PATH = REPO_PATH / "projects"

def validate_current_goal_archived():
    """Check that current goal's work is archived."""
    # Look for goal-specific project directory
    if PROJECTS_PATH.exists():
        goal_dirs = [d for d in PROJECTS_PATH.iterdir() if d.is_dir()]
        if goal_dirs:
            return True, f"Current goal archived: {len(goal_dirs)} project(s)"
    return False, "No project directory found - check if memory-improvement work archived"

def validate_git_state():
    """Ensure all work is committed."""
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=REPO_PATH,
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.stdout.strip():
            return False, f"Uncommitted changes:\n{result.stdout}"
        return True, "Git state clean"
    except Exception as e:
        return False, f"Git check failed: {e}"

def validate_memory_pointers():
    """Check that memory has mandatory external pointers."""
    pointers_file = REPO_PATH / "metadata" / "EXTERNAL_MEMORY_POINTERS.txt"
    
    # Check that key docs are accessible
    key_docs = [
        REPO_PATH / "metadata" / "PHASE_3.3_FINAL_REPORT.md",
        REPO_PATH / "patterns" / "consolidation-case-studies",
        REPO_PATH / "patterns" / "memory-readiness-checklist.md",
    ]
    
    missing = []
    for doc in key_docs:
        if not doc.exists():
            missing.append(str(doc))
    
    if missing:
        return False, f"Missing docs: {', '.join(missing)}"
    return True, "All external memory docs accessible"

def validate_inventory_completeness():
    """Check inventory.yaml documents current work."""
    inventory_file = REPO_PATH / "metadata" / "inventory.yaml"
    
    if not inventory_file.exists():
        return False, "inventory.yaml missing"
    
    try:
        with open(inventory_file) as f:
            content = f.read()
        
        # Check for task-state items tracking transition
        if "task-state" in content:
            return True, "inventory.yaml has task-state items"
        return False, "No task-state items in inventory (plan next goal?)"
    except Exception as e:
        return False, f"Inventory check failed: {e}"

def validate_memory_boundaries():
    """Check that memory is within acceptable size range."""
    # Note: We can't read the actual consolidated memory here,
    # but we can check the consolidated_memory.txt file if it exists
    memory_file = REPO_PATH / "consolidated_memory.txt"
    
    if memory_file.exists():
        size = memory_file.stat().st_size
        if size < 7500:
            return False, f"Memory too small ({size} chars, min 7500)"
        if size > 15000:
            return False, f"Memory too large ({size} chars, max 15000)"
        return True, f"Memory size OK ({size} chars)"
    
    return True, "Memory file not found (check during consolidation)"

def validate_backup_exists():
    """Check that previous goal work is backed up."""
    archives_path = REPO_PATH / "archives"
    
    if archives_path.exists() and list(archives_path.iterdir()):
        archive_count = len(list(archives_path.iterdir()))
        return True, f"Archives exist ({archive_count} items)"
    return False, "No archives - ensure previous goal work backed up"

def main():
    print("[PRE-GOAL-TRANSITION GATE]")
    print("=" * 60)
    
    checks = [
        ("Current Goal Archived", validate_current_goal_archived()),
        ("Git State Clean", validate_git_state()),
        ("External Memory Accessible", validate_memory_pointers()),
        ("Inventory Complete", validate_inventory_completeness()),
        ("Memory Size OK", validate_memory_boundaries()),
        ("Backups Exist", validate_backup_exists()),
    ]
    
    all_pass = True
    for check_name, (passed, detail) in checks:
        status = "✓" if passed else "❌"
        print(f"{status} {check_name}")
        if not passed:
            all_pass = False
        print(f"  {detail}")
    
    print("=" * 60)
    
    if all_pass:
        print("✓ READY FOR GOAL TRANSITION")
        print("  Safe to incorporate new goal into memory")
        return 0
    else:
        print("❌ FIX ISSUES BEFORE GOAL TRANSITION")
        print("  Risk: Loss of work or memory corruption")
        return 1

if __name__ == "__main__":
    exit(main())
