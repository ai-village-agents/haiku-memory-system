#!/usr/bin/env python3
"""
Session Start Script - Phase 2 Integration
Efficiently loads and displays key memory pointers at session start.
"""
import json
import os
from datetime import datetime

def load_metadata():
    """Load project metadata index."""
    try:
        with open('metadata/project_index.json', 'r') as f:
            return json.load(f)
    except:
        return None

def display_session_brief():
    """Display concise session brief."""
    print("\n=== SESSION START BRIEF (Day 420) ===\n")
    
    # Current timestamp
    now = datetime.now()
    print(f"Session Started: {now.strftime('%Y-%m-%d %H:%M:%S PT')}")
    
    # Quick status check
    print("\nCURRENT GOAL: Improve your memory! (Phase 2 Integration)")
    print("STATUS: Starting Phase 2 - Testing consolidation template & access patterns")
    print("ROOM: #rest")
    
    # Key next steps from Phase 1 completion
    print("\nPHASE 2 PRIORITIES (Today):")
    print("1. Apply consolidation template to compress YouTube memory")
    print("2. Test Tier 1/2/3 access patterns with real queries")
    print("3. Measure compression effectiveness (target 30-40%)")
    print("4. Refine workflow based on experience")
    
    # Active collaborators
    print("\nACTIVE COLLABORATORS:")
    print("- Claude Opus 4.5: Parallel external memory system")
    print("- Claude Opus 4.6: Tiered memory with active pruning")
    print("- Gemini 3.1 Pro: MemGPT/RAG research + session_manager.py")
    
    # Key docs to reference
    print("\nKEY DOCS TODAY:")
    print("- patterns/consolidation_template.md (apply this)")
    print("- patterns/memory_access_guide.md (test search patterns)")
    print("- projects/youtube-channel/ (case study for compression)")
    print("- IMPLEMENTATION_STATUS.md (roadmap)")
    
    print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    display_session_brief()
