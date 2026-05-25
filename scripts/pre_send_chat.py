#!/usr/bin/env python3
"""
Haiku Pre-Send-Chat Gate - Mandatory guard before send_message_to_chat.
Prevents duplicates, ensures clarity, enforces consolidation rules.
Based on GPT-5.5's pattern from Day 419.
"""

import sys
import os
import json
from pathlib import Path
from datetime import datetime

REPO_PATH = Path(os.path.expanduser("~/haiku-memory-system"))
PUBLIC_COMMS_LOG = REPO_PATH / "metadata" / "public_comms.json"

def load_recent_messages(limit=20):
    """Load recent sent messages from log."""
    if not PUBLIC_COMMS_LOG.exists():
        return []
    try:
        with open(PUBLIC_COMMS_LOG) as f:
            messages = json.load(f)
        return messages[-limit:] if isinstance(messages, list) else []
    except:
        return []

def check_duplicate(message_text):
    """Check if message is too similar to recent ones."""
    recent = load_recent_messages(5)
    message_lower = message_text.lower().strip()
    
    for prev in recent:
        prev_text = prev.get("text", "").lower() if isinstance(prev, dict) else str(prev).lower()
        # Simple similarity check
        if prev_text and message_lower in prev_text[:200]:
            return True, f"⚠️  DUPLICATE: Very similar to recent message"
    return False, None

def validate_message(message_text):
    """Validate message clarity and purpose."""
    issues = []
    
    if not message_text or len(message_text.strip()) < 10:
        issues.append("Message too short (<10 chars)")
    
    if len(message_text) > 500:
        issues.append("Message too long (>500 chars) - consider breaking up")
    
    if message_text.count("@") == 0 and "Gate" not in message_text:
        issues.append("⚠️  No recipient (@user) mentioned - who is this for?")
    
    return issues

def log_message(message_text):
    """Log sent message to public comms log."""
    entry = {
        "timestamp": datetime.now().isoformat(),
        "text": message_text[:100],  # First 100 chars for brevity
        "length": len(message_text)
    }
    
    try:
        existing = []
        if PUBLIC_COMMS_LOG.exists():
            with open(PUBLIC_COMMS_LOG) as f:
                existing = json.load(f)
        existing.append(entry)
        with open(PUBLIC_COMMS_LOG, "w") as f:
            json.dump(existing, f, indent=2)
    except Exception as e:
        print(f"⚠️  Could not log message: {e}")

def main():
    if len(sys.argv) < 2:
        print("Usage: pre_send_chat.py '<message_text>'")
        sys.exit(1)
    
    message = sys.argv[1]
    
    print("[PRE-SEND-CHAT GATE]")
    print("-" * 50)
    
    # Check for duplicates
    is_dup, dup_msg = check_duplicate(message)
    if is_dup:
        print(dup_msg)
        print("❌ BLOCKED - Do not send duplicate")
        sys.exit(1)
    
    # Validate clarity
    issues = validate_message(message)
    if issues:
        print("⚠️  VALIDATION WARNINGS:")
        for issue in issues:
            print(f"  • {issue}")
    
    # Log and allow
    log_message(message)
    print("✓ Message cleared to send")
    print(f"  Length: {len(message)} chars")
    print(f"  Preview: {message[:50]}...")

if __name__ == "__main__":
    main()
