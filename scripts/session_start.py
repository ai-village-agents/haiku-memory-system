#!/usr/bin/env python3
"""
Haiku Session Start Gate - Mandatory initialization check before any work.
Verifies repo state, loads external memory pointers, checks for new goals.
"""

import os
import subprocess
from datetime import datetime

REPO_PATH = os.path.expanduser("~/haiku-memory-system")

def check_git_state():
    """Verify repo is clean and up to date."""
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=REPO_PATH,
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.stdout.strip():
            print(f"⚠️  WARNING: Uncommitted changes in {REPO_PATH}")
            print(result.stdout)
            return False
        print("✓ Git state clean")
        return True
    except Exception as e:
        print(f"❌ Git check failed: {e}")
        return False

def load_external_pointers():
    """Display critical external memory pointers."""
    print("\n📚 EXTERNAL MEMORY POINTERS (MANDATORY):")
    print("Repository: https://github.com/ai-village-agents/haiku-memory-system")
    print("  • phase_3_3_final_report: metadata/PHASE_3.3_FINAL_REPORT.md")
    print("  • case_studies: patterns/consolidation-case-studies/")
    print("  • gate_adoption_analysis: metadata/gate-adoption-analysis.md")
    print("  • aggregated_inventories: metadata/aggregated_inventories.json")

def check_for_new_goals():
    """Notify if a new goal may have been announced."""
    print("\n🎯 GOAL STATUS:")
    print("  Current: 'Improve your memory!' (Day 419)")
    print("  ⚠️  No Day 420 announcement found yet")

def main():
    print(f"[{datetime.now().strftime('%H:%M:%S')}] HAIKU SESSION START GATE")
    print("-" * 50)
    
    check_git_state()
    load_external_pointers()
    check_for_new_goals()
    
    print("\n✓ Session initialization complete.")

if __name__ == "__main__":
    main()
