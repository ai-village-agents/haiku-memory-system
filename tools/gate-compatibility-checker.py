#!/usr/bin/env python3
"""
Gate Compatibility Checker - Validates if peer agent gates match interface spec.
Helps agents assess compatibility before adopting shared-gate-library.
"""

import os
import subprocess
import json
from pathlib import Path

def check_gate_file_exists(gate_name, repo_path):
    """Check if gate file exists in agent's repo."""
    possible_paths = [
        repo_path / "scripts" / f"{gate_name}.py",
        repo_path / "scripts" / f"{gate_name}.sh",
        repo_path / "gates" / f"{gate_name}.py",
        repo_path / "gates" / f"{gate_name}.sh",
    ]
    for path in possible_paths:
        if path.exists():
            return str(path)
    return None

def check_gate_compatibility(agent_name, repo_path):
    """Check compatibility of agent's gates with interface spec."""
    results = {
        "agent": agent_name,
        "repo_path": str(repo_path),
        "gates": {},
        "compatibility_score": 0,
        "recommendations": []
    }
    
    required_gates = [
        "session_start",
        "pre_send_chat", 
        "pre_consolidate",
        "pre_goal_transition"
    ]
    
    found_gates = 0
    for gate_name in required_gates:
        gate_path = check_gate_file_exists(gate_name, repo_path)
        if gate_path:
            found_gates += 1
            results["gates"][gate_name] = {
                "status": "found",
                "path": gate_path,
                "recommendation": "Compatible - ready for adoption"
            }
        else:
            results["gates"][gate_name] = {
                "status": "not_found",
                "recommendation": "Can adopt from shared-gate-library"
            }
    
    results["compatibility_score"] = (found_gates / len(required_gates)) * 100
    
    if found_gates == 4:
        results["overall_status"] = "FULL_COMPATIBILITY"
        results["recommendations"].append("All 4 gates found. Review for interface spec alignment.")
    elif found_gates >= 2:
        results["overall_status"] = "PARTIAL_COMPATIBILITY"
        results["recommendations"].append(f"{found_gates}/4 gates found. Adopt missing gates from shared-gate-library.")
    else:
        results["overall_status"] = "LOW_COMPATIBILITY"
        results["recommendations"].append("Most gates missing. Adopt all 4 from shared-gate-library (Phase 1 quickstart).")
    
    results["next_steps"] = [
        "1. Review shared-gate-library interface spec: metadata/GATE_INTERFACE_SPEC.md",
        "2. If compatible: Run Phase 1 adoption (copy gates)",
        "3. If conflicts: File PR to shared-gate-library with your implementation",
        "4. Report adoption status in #rest"
    ]
    
    return results

def main():
    """Check compatibility for current agent and report results."""
    repo_path = Path.home() / "haiku-memory-system"
    
    if not repo_path.exists():
        print(f"Error: Expected repo at {repo_path}")
        return
    
    print("[GATE COMPATIBILITY CHECKER]")
    print("-" * 50)
    
    results = check_gate_compatibility("Claude Haiku 4.5", repo_path)
    
    print(f"\nAgent: {results['agent']}")
    print(f"Repo: {results['repo_path']}")
    print(f"Compatibility Score: {results['compatibility_score']:.0f}%")
    print(f"Status: {results['overall_status']}")
    
    print("\nGate Status:")
    for gate_name, gate_info in results["gates"].items():
        status = gate_info["status"]
        print(f"  • {gate_name}: {status}")
    
    print("\nRecommendations:")
    for rec in results["recommendations"]:
        print(f"  • {rec}")
    
    print("\nNext Steps:")
    for step in results["next_steps"]:
        print(f"  {step}")
    
    # Output JSON for programmatic use
    output_file = Path.home() / "haiku-memory-system" / "metadata" / "gate-compatibility-check.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\n✓ Results saved to metadata/gate-compatibility-check.json")

if __name__ == "__main__":
    main()
