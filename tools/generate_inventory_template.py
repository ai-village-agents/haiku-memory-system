#!/usr/bin/env python3
"""
Generate a starter inventory.yaml file for agents.
Usage: python3 tools/generate_inventory_template.py [agent_name] [email]
"""

import sys
from datetime import datetime

TEMPLATE = """# {agent_name} Memory Inventory
# Schema: id, status, kind, summary, source, last_verified, retrieval_cue
# Generated: {date}

- id: {short_name}.identity_anchor
  status: active
  kind: semantic
  summary: "Core identity and immutable constraints"
  source: "identity/identity.md"
  last_verified: {date}
  retrieval_cue: "What is my name and email?"

- id: {short_name}.active_goal
  status: active
  kind: semantic
  summary: "Current goal and session tracking"
  source: "goals/active.md"
  last_verified: {date}
  retrieval_cue: "What goal am I working on right now?"

- id: {short_name}.principles
  status: active
  kind: semantic
  summary: "Core principles and cross-episode rules"
  source: "principles/principles.md"
  last_verified: {date}
  retrieval_cue: "What are my foundational rules?"

- id: {short_name}.session_procedures
  status: active
  kind: procedural
  summary: "Session start and end checklists"
  source: "procedures/session_procedures.md"
  last_verified: {date}
  retrieval_cue: "What do I do at session start?"

- id: {short_name}.public_comms
  status: active
  kind: procedural
  summary: "Public announcement log and guidelines"
  source: "goals/public_comms.md"
  last_verified: {date}
  retrieval_cue: "What messages have I sent to chat?"

- id: {short_name}.external_memory_pointers
  status: active
  kind: pointer
  summary: "Links to GitHub repo and key files"
  source: "identity/external_pointers.md"
  last_verified: {date}
  retrieval_cue: "Where is my external memory stored?"

# Add more items as your system grows:
# - episodic: session logs, day-specific records
# - gate: pre-send guards, pre-consolidate checks
# - semantic: knowledge, facts, learned patterns
# - procedural: runbooks, checklists, workflows
# - pointer: links to files, repos, external resources
# - social: agent relationships, collaboration notes
# - reflection: lessons learned, failure analysis
# - task-state: current project status, blockers
