#!/usr/bin/env python3
"""
Constraint Validator: Tests memory rewrite enforcement rules
"""

import sys
import json
import os
from datetime import datetime

def validate_memory_constraints(memory_text):
    """Analyze memory text against known constraints."""
    results = {
        "timestamp": datetime.now().isoformat(),
        "analysis": {}
    }
    
    # Constraint 1: Length analysis
    length = len(memory_text)
    results["analysis"]["length"] = {
        "chars": length,
        "threshold_7500": length >= 7500,
        "tier_1_minimum": 7500,
        "tier_1_maximum": 10000,
        "status": "✓ PASS" if 7500 <= length <= 10000 else "⚠️  WARNING"
    }
    
    # Constraint 2: External pointers
    pointer_checks = {
        "github_urls": memory_text.count("https://github.com/ai-village-agents/"),
        "raw_urls": memory_text.count("https://raw.githubusercontent.com/"),
        "tier_2_references": memory_text.count("Tier 2") + memory_text.count("external")
    }
    
    results["analysis"]["pointers"] = pointer_checks
    results["analysis"]["pointers"]["status"] = "✓ PASS" if pointer_checks["github_urls"] > 0 else "⚠️  MISSING"
    
    # Constraint 3: Temporal anchor
    temporal_checks = {
        "has_canonical_day": "canonical_day" in memory_text,
        "has_canonical_time": "canonical_time" in memory_text,
        "has_session_number": "session_number" in memory_text,
        "has_temporal_note": "offset" in memory_text.lower() or "temporal" in memory_text.lower()
    }
    
    results["analysis"]["temporal_anchor"] = temporal_checks
    results["analysis"]["temporal_anchor"]["status"] = "✓ PASS" if all(temporal_checks.values()) else "⚠️  INCOMPLETE"
    
    # Overall assessment
    results["overall_status"] = "✓ PASS" if all([
        results["analysis"]["length"]["status"] == "✓ PASS",
        results["analysis"]["pointers"]["status"] == "✓ PASS",
        results["analysis"]["temporal_anchor"]["status"] == "✓ PASS"
    ]) else "⚠️  REVIEW NEEDED"
    
    return results

def main():
    if len(sys.argv) < 2:
        print("Usage: constraint-validator.py '<memory_text>' or --self-test")
        sys.exit(1)
    
    if sys.argv[1] == "--self-test":
        # Test with a sample valid memory
        test_memory = "x" * 8000 + "\nhttps://github.com/ai-village-agents/haiku-memory-system\ncanonical_day: 419\ncanonical_time: 2026-05-25\nsession_number: 10\nTemporal anchor offset tracking"
        results = validate_memory_constraints(test_memory)
    else:
        memory_text = sys.argv[1]
        results = validate_memory_constraints(memory_text)
    
    # Print summary
    print("=" * 60)
    print("CONSTRAINT VALIDATION SUMMARY")
    print("=" * 60)
    print(f"Overall Status: {results['overall_status']}")
    print(f"\nLength: {results['analysis']['length']['chars']} chars")
    print(f"  • Tier 1 Range (7.5k-10k): {results['analysis']['length']['status']}")
    print(f"\nExternal Pointers: {results['analysis']['pointers']['status']}")
    print(f"  • GitHub URLs: {results['analysis']['pointers']['github_urls']}")
    print(f"\nTemporal Anchor: {results['analysis']['temporal_anchor']['status']}")
    print(f"  • Canonical day: {'✓' if results['analysis']['temporal_anchor']['has_canonical_day'] else '✗'}")
    print(f"  • Canonical time: {'✓' if results['analysis']['temporal_anchor']['has_canonical_time'] else '✗'}")
    print(f"  • Session number: {'✓' if results['analysis']['temporal_anchor']['has_session_number'] else '✗'}")

if __name__ == "__main__":
    main()
