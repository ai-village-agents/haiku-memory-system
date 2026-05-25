#!/usr/bin/env python3
"""
Shared Date Validation Utility - Village-wide
Prevents date confusion (e.g., DeepSeek Day 416 issue)

Usage:
  python3 validate_date.py [--current DAY] [--last DAY] [--check]
"""

import sys
from datetime import datetime, timedelta

class DateValidator:
    """Validates dates and prevents temporal confusion."""
    
    # Village day mapping (Day 1 = May 12, 2026)
    VILLAGE_START = datetime(2026, 5, 12)
    
    def day_to_date(self, day):
        """Convert village day number to calendar date."""
        if day < 1:
            return None
        date = self.VILLAGE_START + timedelta(days=day - 1)
        return date
    
    def validate_progression(self, current_day, last_recorded_day):
        """Check that days are progressing forward (not backward)."""
        if current_day < 1 or last_recorded_day < 1:
            return False, "Day numbers must be >= 1"
        
        if current_day < last_recorded_day:
            return False, f"Time travel detected: current={current_day}, last={last_recorded_day}"
        
        days_elapsed = current_day - last_recorded_day
        return True, f"Progression valid: {days_elapsed} day(s) elapsed"
    
    def format_date_statement(self, day):
        """Format a day as an absolute date statement."""
        date = self.day_to_date(day)
        if not date:
            return None
        return f"Day {day} ({date.strftime('%B %d, %Y')})"
    
    def before_public_statement(self, current_day, last_recorded_day):
        """Pre-announcement checklist."""
        checklist = {
            "Current day is positive": current_day > 0,
            "Last recorded day is positive": last_recorded_day > 0,
            "Days progress forward": current_day >= last_recorded_day,
        }
        
        all_pass = all(checklist.values())
        
        message = f"""
=== DATE VALIDATION CHECKLIST ===
Current day: {self.format_date_statement(current_day)}
Last recorded: {self.format_date_statement(last_recorded_day)}
Days elapsed: {current_day - last_recorded_day}

Checks:
"""
        for check, passed in checklist.items():
            status = "✓" if passed else "✗"
            message += f"  {status} {check}\n"
        
        if all_pass:
            message += "\n✓ SAFE TO POST: All checks pass\n"
        else:
            message += "\n✗ DO NOT POST: Validation failed\n"
        
        return all_pass, message, checklist

def main():
    """CLI interface."""
    validator = DateValidator()
    
    if len(sys.argv) < 2:
        print("Usage: python3 validate_date.py --current DAY --last DAY")
        sys.exit(1)
    
    if "--current" in sys.argv:
        current_idx = sys.argv.index("--current")
        current_day = int(sys.argv[current_idx + 1])
    else:
        print("Error: --current DAY is required")
        sys.exit(1)
    
    if "--last" in sys.argv:
        last_idx = sys.argv.index("--last")
        last_recorded_day = int(sys.argv[last_idx + 1])
    else:
        print("Error: --last DAY is required")
        sys.exit(1)
    
    # Validate and report
    valid, message, checklist = validator.before_public_statement(current_day, last_recorded_day)
    print(message)
    
    sys.exit(0 if valid else 1)

if __name__ == "__main__":
    main()
