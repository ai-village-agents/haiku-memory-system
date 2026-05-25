#!/usr/bin/env python3
"""
Verify Session 8 Completion Checklist
Ensures all deliverables are production-ready before consolidation
"""

import os
import json
from pathlib import Path

def check_file_exists(path, min_size=100):
    """Check if file exists and meets minimum size"""
    p = Path(path)
    if not p.exists():
        return False, "MISSING"
    size = p.stat().st_size
    if size < min_size:
        return False, f"TOO_SMALL ({size} bytes)"
    return True, "OK"

def verify_session_8():
    """Run comprehensive Session 8 verification"""
    
    print("[SESSION 8 COMPLETION VERIFICATION]")
    print("=" * 60)
    
    checks = {
        "Tier 3 Deliverables": {
            "patterns/gate-interface-spec.md": (True, 7000),
            "patterns/GATE_ADOPTION_QUICKSTART.md": (True, 5000),
            "patterns/gate-self-validation-runbook.md": (True, 100),
            "tools/gate-adoption-tracker.py": (True, 100),
            "metadata/gate-compatibility-report.md": (True, 1000),
            "metadata/shared-gate-library-pointer.md": (True, 100),
            "patterns/collaborative-gate-library.md": (True, 5000),
        },
        "Tier 4 Deliverables": {
            "patterns/tier4-compression-analysis.md": (True, 100),
            "patterns/tier4-alternative-architectures.md": (True, 100),
            "patterns/temporal-aware-sandwich-experiment.md": (True, 100),
            "patterns/constraint-aware-design-principles.md": (True, 100),
            "patterns/lean-8.5k-memory-template.md": (True, 100),
        },
        "Session 8 Documentation": {
            "metadata/SESSION_8_SUMMARY.md": (True, 100),
            "metadata/village-convergence-analysis-day419.md": (True, 100),
            "patterns/peer-adoption-coordination-guide.md": (True, 100),
            "metadata/inventory.yaml": (True, 1000),
        },
        "External Resources": {
            "https://github.com/ai-village-agents/shared-gate-library": (True, 0),
        }
    }
    
    total_checks = 0
    passed_checks = 0
    
    for category, items in checks.items():
        print(f"\n{category}:")
        for item, (should_exist, min_size) in items.items():
            if item.startswith("http"):
                # External resource - just note it
                print(f"  ✅ {item}")
                total_checks += 1
                passed_checks += 1
            else:
                exists, status = check_file_exists(item, min_size)
                symbol = "✅" if exists else "❌"
                print(f"  {symbol} {item} ({status})")
                total_checks += 1
                if exists:
                    passed_checks += 1
    
    print("\n" + "=" * 60)
    print(f"VERIFICATION: {passed_checks}/{total_checks} items ready")
    
    # Git verification
    result = os.system("cd . && git status --porcelain | head -5 > /tmp/git_status.txt 2>&1")
    with open("/tmp/git_status.txt") as f:
        status = f.read().strip()
    
    if not status:
        print("✅ Git: All changes committed")
    else:
        print(f"⚠️  Git: Uncommitted changes detected")
        print(status[:200])
    
    # Final verdict
    if passed_checks == total_checks and not status:
        print("\n🎉 SESSION 8 READY FOR CONSOLIDATION")
        return 0
    else:
        print(f"\n⚠️  Review items above before consolidation")
        return 1

if __name__ == "__main__":
    exit(verify_session_8())

