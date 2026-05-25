#!/usr/bin/env python3
"""
Cross-agent inventory scanner v0.3 - handles nested + flat schemas + cache busting
Scans inventory.yaml from 15+ known agent repos and aggregates items.
"""

import sys
import subprocess
import json
import time
from typing import List, Dict, Any, Optional

AGENT_REPOS = [
    "ai-village-agents/haiku-memory-system",
    "ai-village-agents/gemini-3.1-pro-memory",
    "ai-village-agents/gpt-5-2-memory-improvement",
    "ai-village-agents/gpt-5-4-memory-kit",
    "ai-village-agents/claude-opus-memory",
    "ai-village-agents/opus-46-memory",
    "ai-village-agents/deepseek-v3.2-memory-system",
    "ai-village-agents/claude-sonnet-4.5-memory",
    "ai-village-agents/gpt-5-1-memory",
    "ai-village-agents/claude-opus-4.6-memory",
    "ai-village-agents/gemini-3.5-flash-memory-vault",
    "ai-village-agents/gpt-5.5-memory-improvement",
    "ai-village-agents/kimi-k2.6-memory",
]

def fetch_raw_yaml(repo: str, branch: str = "main") -> Optional[str]:
    """Fetch raw inventory.yaml from GitHub with cache busting."""
    url = f"https://raw.githubusercontent.com/{repo}/{branch}/inventory.yaml?t={int(time.time())}"
    try:
        result = subprocess.run(
            ["curl", "-s", url],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.stdout if result.returncode == 0 else None
    except Exception:
        return None

def parse_yaml_items(yaml_content: str) -> Optional[List[Dict[str, Any]]]:
    """Parse YAML content and extract items (handles nested + flat schemas)."""
    try:
        import yaml
    except ImportError:
        return _parse_yaml_fallback(yaml_content)
    
    try:
        data = yaml.safe_load(yaml_content)
        if not data:
            return None
        
        # Handle nested schema (repository + items)
        if isinstance(data, dict) and "items" in data:
            return data.get("items", [])
        
        # Handle flat schema (direct list)
        if isinstance(data, list):
            return data
        
        return None
    except Exception:
        return None

def _parse_yaml_fallback(content: str) -> Optional[List[Dict[str, Any]]]:
    """Fallback YAML parser for flat list schemas."""
    items = []
    current_item = None
    
    for line in content.split("\n"):
        line = line.rstrip()
        if not line or line.startswith("#"):
            continue
        
        if line.startswith("- "):
            if current_item:
                items.append(current_item)
            current_item = {}
            key_val = line[2:].split(":", 1)
            if len(key_val) == 2:
                current_item[key_val[0].strip()] = key_val[1].strip()
        elif line.startswith("  ") and current_item is not None:
            key_val = line.strip().split(":", 1)
            if len(key_val) == 2:
                current_item[key_val[0].strip()] = key_val[1].strip().strip('"')
    
    if current_item:
        items.append(current_item)
    
    return items if items else None

def aggregate_inventories(verbose: bool = False, save: bool = False) -> Dict[str, Any]:
    """Scan all agent repos and aggregate inventories."""
    results = {}
    warnings = []
    total_items = 0
    
    for repo in AGENT_REPOS:
        yaml_content = fetch_raw_yaml(repo)
        
        if not yaml_content:
            warnings.append(f"  - {repo}: inventory.yaml not found on main")
            continue
        
        items = parse_yaml_items(yaml_content)
        if not items:
            warnings.append(f"  - {repo}: invalid or empty inventory.yaml")
            continue
        
        # Validate items have required fields
        valid_items = []
        for item in items:
            if isinstance(item, dict) and "id" in item:
                valid_items.append(item)
        
        if not valid_items:
            warnings.append(f"  - {repo}: inventory.yaml missing required 'id' field")
            continue
        
        agent_name = repo.split("/")[1]
        results[agent_name] = valid_items
        total_items += len(valid_items)
        
        if verbose:
            print(f"\n[{agent_name}] {len(valid_items)} items")
            for item in valid_items[:3]:
                print(f"  - {item.get('id', 'unknown')} | kind={item.get('kind', '?')} | status={item.get('status', '?')}")
    
    return {
        "total_items": total_items,
        "agents": len(results),
        "results": results,
        "warnings": warnings
    }

def print_summary(agg: Dict[str, Any]):
    """Print aggregation summary."""
    print("\n" + "=" * 75)
    print(f"CROSS-AGENT INVENTORY AGGREGATION (v0.3 - with cache busting)")
    print("=" * 75)
    print(f"\nTotal Items: {agg['total_items']} | Agents: {agg['agents']}")
    print("\nAgent Summary:")
    print("-" * 75)
    for agent, items in agg['results'].items():
        kinds = {}
        statuses = {}
        for item in items:
            k = item.get('kind', 'unknown')
            s = item.get('status', 'unknown')
            kinds[k] = kinds.get(k, 0) + 1
            statuses[s] = statuses.get(s, 0) + 1
        
        kind_str = ", ".join(f"{k}({v})" for k, v in sorted(kinds.items()))
        status_str = ", ".join(f"{s}({v})" for s, v in sorted(statuses.items()))
        print(f"  {agent:30} | {len(items):2} items | {status_str:30} | kinds: {kind_str}")
    
    if agg['warnings']:
        print("\nWarnings:")
        for w in agg['warnings']:
            print(w)
    print("=" * 75 + "\n")

if __name__ == "__main__":
    verbose = "--verbose" in sys.argv
    save = "--save" in sys.argv
    
    agg = aggregate_inventories(verbose=verbose)
    print_summary(agg)
    
    if save:
        with open("metadata/village_inventory.json", "w") as f:
            json.dump(agg, f, indent=2)
        print(f"✓ Saved to metadata/village_inventory.json")
