#!/usr/bin/env python3
"""
Gate Metrics Dashboard - Tracks effectiveness of executable gates.
Measures: duplicate prevention, consolidation success, temporal accuracy.
"""

import json
import os
from pathlib import Path
from datetime import datetime
from collections import defaultdict

REPO_PATH = Path(os.path.expanduser("~/haiku-memory-system"))
PUBLIC_COMMS_LOG = REPO_PATH / "metadata" / "public_comms.json"
GATE_METRICS_FILE = REPO_PATH / "metadata" / "gate_metrics.json"

def load_public_comms():
    """Load public comms log."""
    if PUBLIC_COMMS_LOG.exists():
        with open(PUBLIC_COMMS_LOG) as f:
            return json.load(f)
    return []

def calculate_duplicate_prevention():
    """Estimate duplicate prevention effectiveness."""
    # Load last 20 messages
    messages = load_public_comms()
    if len(messages) < 2:
        return {"status": "insufficient_data", "messages_analyzed": len(messages)}
    
    # Simple heuristic: if gate is blocking duplicates, message diversity should be high
    last_msgs = messages[-20:]
    unique_previews = len(set(m.get("text", "")[:30] for m in last_msgs if isinstance(m, dict)))
    
    diversity_ratio = unique_previews / len(last_msgs) if last_msgs else 0
    
    return {
        "status": "active",
        "messages_analyzed": len(last_msgs),
        "unique_messages": unique_previews,
        "diversity_ratio": f"{diversity_ratio:.1%}",
        "threshold": "85% (good)",
        "assessment": "PASS" if diversity_ratio > 0.85 else "WARNING"
    }

def calculate_consolidation_success():
    """Check consolidation gate compliance."""
    # Count commits to repo - successful consolidations
    try:
        import subprocess
        result = subprocess.run(
            ["git", "rev-list", "--count", "HEAD"],
            cwd=REPO_PATH,
            capture_output=True,
            text=True,
            timeout=5
        )
        commit_count = int(result.stdout.strip())
        
        # Rough estimate: 1 consolidation per 5-8 commits
        estimated_sessions = max(1, commit_count // 6)
        
        return {
            "status": "active",
            "total_commits": commit_count,
            "estimated_sessions": estimated_sessions,
            "commits_per_session_avg": f"{commit_count / estimated_sessions:.1f}",
            "assessment": "PASS" if commit_count > 20 else "WARNING"
        }
    except Exception as e:
        return {"status": "error", "error": str(e)}

def calculate_temporal_accuracy():
    """Check for temporal confusion incidents."""
    # Look for temporal anomalies in consolidations
    memory_file = REPO_PATH / "internal_memory.txt"
    
    if memory_file.exists():
        with open(memory_file) as f:
            memory = f.read()
        
        # Count day references
        day_refs = {}
        for i in range(415, 425):
            count = memory.count(f"Day {i}")
            if count > 0:
                day_refs[f"Day {i}"] = count
        
        # Check for temporal confusion (should have one primary day)
        current_day = "Day 419"  # As of this session
        primary_refs = day_refs.get(current_day, 0)
        total_refs = sum(day_refs.values())
        
        if total_refs > 0:
            primary_ratio = primary_refs / total_refs
        else:
            primary_ratio = 0
        
        return {
            "status": "active",
            "current_day_references": primary_refs,
            "total_day_references": total_refs,
            "primary_day_ratio": f"{primary_ratio:.1%}",
            "threshold": ">80% (good)",
            "assessment": "PASS" if primary_ratio > 0.80 else "WARNING"
        }
    
    return {"status": "data_unavailable"}

def calculate_inventory_compliance():
    """Check inventory.yaml is kept up-to-date."""
    inventory_file = REPO_PATH / "metadata" / "inventory.yaml"
    
    if inventory_file.exists():
        # Count items
        with open(inventory_file) as f:
            content = f.read()
        
        item_count = content.count("- id:")
        gate_count = content.count("kind: gate")
        
        # Get file modification time
        mtime = inventory_file.stat().st_mtime
        age_hours = (datetime.now().timestamp() - mtime) / 3600
        
        return {
            "status": "active",
            "total_items": item_count,
            "gate_items": gate_count,
            "gate_percentage": f"{100*gate_count/item_count:.1f}%" if item_count > 0 else "N/A",
            "last_updated_hours_ago": f"{age_hours:.1f}",
            "assessment": "PASS" if age_hours < 24 else "WARNING"
        }
    
    return {"status": "not_found"}

def save_metrics(metrics):
    """Save metrics to file."""
    output = {
        "timestamp": datetime.now().isoformat(),
        "session_date": "2026-05-25 12:10 PT",
        "metrics": metrics
    }
    
    try:
        with open(GATE_METRICS_FILE, "w") as f:
            json.dump(output, f, indent=2)
        return True
    except Exception as e:
        print(f"Failed to save metrics: {e}")
        return False

def print_dashboard(metrics):
    """Pretty-print metrics dashboard."""
    print("\n" + "=" * 70)
    print("CLAUDE HAIKU 4.5 - GATE METRICS DASHBOARD")
    print("=" * 70)
    
    print("\n📊 METRIC 1: Duplicate Prevention")
    dup_data = metrics["duplicate_prevention"]
    for key, value in dup_data.items():
        print(f"  • {key}: {value}")
    
    print("\n📊 METRIC 2: Consolidation Success")
    cons_data = metrics["consolidation_success"]
    for key, value in cons_data.items():
        print(f"  • {key}: {value}")
    
    print("\n📊 METRIC 3: Temporal Accuracy")
    temp_data = metrics["temporal_accuracy"]
    for key, value in temp_data.items():
        print(f"  • {key}: {value}")
    
    print("\n📊 METRIC 4: Inventory Compliance")
    inv_data = metrics["inventory_compliance"]
    for key, value in inv_data.items():
        print(f"  • {key}: {value}")
    
    print("\n" + "=" * 70)
    
    # Overall assessment
    assessments = [
        dup_data.get("assessment", "N/A"),
        cons_data.get("assessment", "N/A"),
        temp_data.get("assessment", "N/A"),
        inv_data.get("assessment", "N/A")
    ]
    
    pass_count = sum(1 for a in assessments if a == "PASS")
    total_count = len([a for a in assessments if a != "N/A"])
    
    if pass_count == total_count and total_count > 0:
        print(f"✓ OVERALL: {pass_count}/{total_count} metrics PASS")
    else:
        print(f"⚠️  OVERALL: {pass_count}/{total_count} metrics PASS - review warnings")
    
    print("=" * 70 + "\n")

def main():
    metrics = {
        "duplicate_prevention": calculate_duplicate_prevention(),
        "consolidation_success": calculate_consolidation_success(),
        "temporal_accuracy": calculate_temporal_accuracy(),
        "inventory_compliance": calculate_inventory_compliance(),
    }
    
    # Save metrics
    save_metrics(metrics)
    
    # Print dashboard
    print_dashboard(metrics)

if __name__ == "__main__":
    main()
