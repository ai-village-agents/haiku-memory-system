#!/usr/bin/env python3
"""Generate a starter inventory.yaml file for agents."""
import sys
from datetime import datetime

agent_name = sys.argv[1] if len(sys.argv) > 1 else "NewAgent"
short_name = agent_name.lower().replace(" ", "").replace("-", "")
date = datetime.now().strftime("%Y-%m-%d")

items = [
    f"- id: {short_name}.identity",
    "  status: active",
    "  kind: semantic",
    "  summary: \"Core identity and constraints\"",
    "  source: \"identity/identity.md\"",
    f"  last_verified: {date}",
    "  retrieval_cue: \"What is my name?\"",
    "",
    f"- id: {short_name}.principles",
    "  status: active",
    "  kind: semantic",
    "  summary: \"Core principles and rules\"",
    "  source: \"principles/principles.md\"",
    f"  last_verified: {date}",
    "  retrieval_cue: \"What are my core rules?\"",
]

for item in items:
    print(item)
