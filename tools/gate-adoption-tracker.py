#!/usr/bin/env python3
"""
Gate Adoption Tracker for AI Village

Monitors gate implementation status across all agent repositories.
Generates JSON and markdown reports for village coordination.
"""

import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime

GATE_NAMES = ["session_start", "pre_send_chat", "pre_consolidate", "pre_goal_transition"]

def check_agent_gates(agent_repo_path):
    """Check which gates are implemented in an agent repo."""
    results = {}
    
    for gate_name in GATE_NAMES:
        # Check for Python implementation
        py_path = Path(agent_repo_path) / "scripts" / f"{gate_name}.py"
        if py_path.exists():
            results[gate_name] = "python"
            continue
            
        # Check for shell implementation  
        sh_path = Path(agent_repo_path) / "scripts" / f"{gate_name}.sh"
        if sh_path.exists():
            results[gate_name] = "shell"
            continue
            
        # Check in tools/
        py_tools = Path(agent_repo_path) / "tools" / f"{gate_name}.py"
        if py_tools.exists():
            results[gate_name] = "python"
            continue
            
        results[gate_name] = None
    
    return results

def generate_report():
    """Generate gate adoption status report."""
    agents = {
        "Claude Haiku 4.5": "/home/computeruse/haiku-memory-system",
        "Claude Opus 4.5": "/home/computeruse/opus-45-memory",
        "Claude Opus 4.6": "/home/computeruse/opus-46-memory",
        "Claude Opus 4.7": "/home/computeruse/opus-47-memory",
        "Claude Sonnet 4.5": "/home/computeruse/sonnet-45-memory",
        "Claude Sonnet 4.6": "/home/computeruse/sonnet-46-memory",
        "Gemini 3.1 Pro": "/home/computeruse/gemini-31-memory",
        "Gemini 3.5 Flash": "/home/computeruse/gemini-35-memory",
        "GPT-5.4": "/home/computeruse/gpt54-memory-kit",
        "GPT-5.5": "/home/computeruse/gpt55-memory",
    }
    
    results = {}
    total_gates = 0
    total_implemented = 0
    
    for agent_name, repo_path in agents.items():
        path_obj = Path(repo_path)
        if not path_obj.exists():
            results[agent_name] = {"gates": {}, "status": "repo_not_found"}
            continue
        
        gates = check_agent_gates(repo_path)
        implemented = sum(1 for g in gates.values() if g is not None)
        total_gates += 4
        total_implemented += implemented
        
        results[agent_name] = {
            "gates": gates,
            "implemented": implemented,
            "status": "complete" if implemented == 4 else "partial" if implemented > 0 else "none"
        }
    
    return {
        "timestamp": datetime.now().isoformat(),
        "summary": {
            "total_gates": total_gates,
            "total_implemented": total_implemented,
            "adoption_rate": f"{100 * total_implemented / total_gates:.1f}%",
            "agents_with_gates": sum(1 for r in results.values() if r.get("status") != "none")
        },
        "agents": results
    }

if __name__ == "__main__":
    report = generate_report()
    
    # Print JSON
    print(json.dumps(report, indent=2))
    
    # Generate markdown summary
    print("\n# Village Gate Adoption Status\n")
    print(f"**Timestamp**: {report['timestamp']}")
    print(f"**Overall Adoption**: {report['summary']['adoption_rate']}")
    print(f"**Agents with Gates**: {report['summary']['agents_with_gates']}")
    
    print("\n## Agent Status\n")
    for agent, data in report["agents"].items():
        gates = data.get("gates", {})
        implemented = sum(1 for g in gates.values() if g is not None)
        status_icon = "✅" if implemented == 4 else "🟡" if implemented > 0 else "⚪"
        print(f"| {status_icon} {agent} | {implemented}/4 |")

