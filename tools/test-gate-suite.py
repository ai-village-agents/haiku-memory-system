#!/usr/bin/env python3
"""
Cross-Agent Gate Test Suite
Tests compatibility of gate implementations across AI Village agents

Usage:
  python3 tools/test-gate-suite.py --agents haiku,opus-4.7,gemini-flash,gpt-5.5
  python3 tools/test-gate-suite.py --test pre_send_chat --output test-results.json
"""

import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

class GateTestSuite:
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "agents": {},
            "summary": {
                "total_tests": 0,
                "total_pass": 0,
                "total_fail": 0
            }
        }
        
    def test_gate(self, agent: str, gate_name: str, repo_path: str) -> Dict[str, Any]:
        """Test a single gate implementation"""
        result = {
            "agent": agent,
            "gate": gate_name,
            "exists": False,
            "executable": False,
            "status": "UNKNOWN",
            "error": None
        }
        
        # Check if gate exists
        gate_py = repo_path / "scripts" / f"{gate_name}.py"
        gate_sh = repo_path / "scripts" / f"{gate_name}.sh"
        
        if gate_py.exists():
            result["exists"] = True
            result["format"] = "python"
            result["path"] = str(gate_py)
            result["executable"] = gate_py.stat().st_mode & 0o111 != 0
            
        elif gate_sh.exists():
            result["exists"] = True
            result["format"] = "shell"
            result["path"] = str(gate_sh)
            result["executable"] = gate_sh.stat().st_mode & 0o111 != 0
            
        else:
            result["status"] = "MISSING"
            return result
        
        # Try to execute the gate
        try:
            gate_file = gate_py if gate_py.exists() else gate_sh
            if gate_py.exists():
                output = subprocess.run(
                    ["python3", str(gate_py)],
                    cwd=repo_path,
                    capture_output=True,
                    text=True,
                    timeout=5
                )
            else:
                output = subprocess.run(
                    ["bash", str(gate_sh)],
                    cwd=repo_path,
                    capture_output=True,
                    text=True,
                    timeout=5
                )
            
            # Parse output
            try:
                json_output = json.loads(output.stdout)
                result["status"] = json_output.get("status", "UNKNOWN")
                result["output"] = json_output
                result["exit_code"] = output.returncode
            except json.JSONDecodeError:
                result["status"] = "ERROR"
                result["error"] = f"Invalid JSON output: {output.stdout[:100]}"
                result["exit_code"] = output.returncode
                
        except subprocess.TimeoutExpired:
            result["status"] = "TIMEOUT"
            result["error"] = f"Execution timeout (5s)"
            
        except Exception as e:
            result["status"] = "EXCEPTION"
            result["error"] = str(e)
        
        return result
    
    def test_agent(self, agent: str, repo_path: str) -> Dict[str, Any]:
        """Test all gates for an agent"""
        gates = ["session_start", "pre_send_chat", "pre_consolidate", "pre_goal_transition"]
        agent_results = {
            "agent": agent,
            "repo_path": str(repo_path),
            "gates": {},
            "summary": {
                "total": len(gates),
                "found": 0,
                "executable": 0,
                "pass": 0
            }
        }
        
        for gate in gates:
            result = self.test_gate(agent, gate, repo_path)
            agent_results["gates"][gate] = result
            
            if result["exists"]:
                agent_results["summary"]["found"] += 1
            if result.get("executable"):
                agent_results["summary"]["executable"] += 1
            if result["status"] == "PASS":
                agent_results["summary"]["pass"] += 1
                
        return agent_results
    
    def run_agent_suite(self, agents: Dict[str, str]) -> None:
        """Run test suite for multiple agents"""
        for agent_name, repo_path in agents.items():
            repo = Path(repo_path)
            if not repo.exists():
                self.results["agents"][agent_name] = {
                    "error": f"Repository not found: {repo_path}"
                }
                continue
            
            agent_result = self.test_agent(agent_name, repo)
            self.results["agents"][agent_name] = agent_result
            
            # Update summary
            self.results["summary"]["total_tests"] += agent_result["summary"]["total"]
            self.results["summary"]["total_pass"] += agent_result["summary"]["pass"]
            
            if self.verbose:
                print(f"✓ Tested {agent_name}: {agent_result['summary']['pass']}/{agent_result['summary']['total']} gates")
    
    def generate_compatibility_report(self) -> str:
        """Generate markdown report"""
        report = "# Cross-Agent Gate Compatibility Report\n\n"
        report += f"**Generated**: {self.results['timestamp']}\n\n"
        
        # Summary
        summary = self.results["summary"]
        report += f"## Summary\n\n"
        report += f"- **Total Tests**: {summary['total_tests']}\n"
        report += f"- **Passed**: {summary['total_pass']}\n"
        report += f"- **Failed**: {summary['total_tests'] - summary['total_pass']}\n"
        report += f"- **Pass Rate**: {100 * summary['total_pass'] // (summary['total_tests'] or 1)}%\n\n"
        
        # By agent
        report += "## By Agent\n\n"
        for agent_name, agent_data in self.results["agents"].items():
            if "error" in agent_data:
                report += f"### {agent_name}\n**ERROR**: {agent_data['error']}\n\n"
                continue
            
            summary = agent_data["summary"]
            report += f"### {agent_name}\n\n"
            report += f"| Gate | Status | Format | Notes |\n"
            report += f"|---|---|---|---|\n"
            
            for gate_name, gate_result in agent_data["gates"].items():
                status = gate_result["status"]
                fmt = gate_result.get("format", "N/A")
                note = gate_result.get("error", "OK")
                report += f"| {gate_name} | {status} | {fmt} | {note} |\n"
            
            report += f"\n**Summary**: {summary['found']}/{summary['total']} gates found, {summary['executable']}/{summary['found']} executable\n\n"
        
        return report
    
    def output_json(self, path: str = None) -> str:
        """Output results as JSON"""
        output = json.dumps(self.results, indent=2)
        if path:
            Path(path).write_text(output)
            print(f"Results saved to {path}")
        return output


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Test cross-agent gate compatibility")
    parser.add_argument("--agents", default="haiku,opus-4.7,gemini-flash,gpt-5.5",
                       help="Comma-separated list of agents to test")
    parser.add_argument("--output", help="Output file for JSON results")
    parser.add_argument("--report", help="Output file for markdown report")
    parser.add_argument("--verbose", action="store_true")
    
    args = parser.parse_args()
    
    # Map agent names to repo paths
    agent_repos = {
        "haiku": Path.home() / "haiku-memory-system",
        "opus-4.7": Path("/tmp/best-agents/claude-opus-4-7-memory"),
        "gemini-flash": Path("/tmp/best-agents/gemini-3-5-flash-memory-vault"),
        "gpt-5.5": Path("/tmp/best-agents/gpt-5-5-memory-improvement"),
    }
    
    # Filter to requested agents
    requested = args.agents.split(",")
    test_agents = {k: v for k, v in agent_repos.items() if k in requested}
    
    # Run tests
    suite = GateTestSuite(verbose=args.verbose)
    suite.run_agent_suite(test_agents)
    
    # Output results
    if args.output:
        suite.output_json(args.output)
    else:
        print(json.dumps(suite.results, indent=2))
    
    if args.report:
        report = suite.generate_compatibility_report()
        Path(args.report).write_text(report)
        print(f"\nReport saved to {args.report}")
        if args.verbose:
            print("\n" + report)


if __name__ == "__main__":
    main()
