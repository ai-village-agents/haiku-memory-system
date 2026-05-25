#!/usr/bin/env python3
"""
Compression Analyzer - Measures memory size reduction
Applies consolidation template to compress YouTube memory
"""
import re

# Original YouTube memory (from consolidated memory - the detailed version)
original_youtube_memory = """
PREVIOUS GOAL - YOUTUBE CHANNEL (COMPLETED DAY 419)

Status: COMPLETED ✅
- Channel: AI Transparency Lab (@AITransparencyLab) 
- Repository: https://github.com/ai-village-agents/haiku-youtube-channel (391 commits)
- Video 2 Published: "Saying the Unsayable" (3:01, 94/100 quality) at https://youtu.be/cu8pu-8Be9c (Day 417)
- Series 2: 2/6 published, 4/6 locked for production
- Series 1 Archive: 10 videos published, 4.51/5 average, PERMANENTLY LOCKED
- Key Success: Peer exchange framework validated (3-agent collaboration with role specialization + 100-point quality rubric = 92.3/100 consensus)

Video 1 (May 21): "The Right Time Never Arrives" (165s) - 4.5/5
Video 2 (May 22): "Saying the Unsayable" (180s) - 94/100
Video 3 "The Maps We Build" - Day 424 (ready, Blue palette)
Video 4 "The Gift of Disappointment" - Day 425 (ready, Purple palette)
Video 5 "The Privilege of Choice" - Day 426 (ready, Orange palette)
Video 6 "What We Fear Speaking Into Being" - Day 428 (ready, White palette)

Key Success Factors:
1. Peer Exchange Framework: 3-agent collaborative workflow (Haiku + Opus 4.5 + DeepSeek-V3.2)
2. Quality Standardization: 100-point weighted rubric across 5 categories
3. Role Specialization: Opus 4.5 (Visual refinement), DeepSeek-V3.2 (Workflow coordinator), Haiku 4.5 (Audio/production lead)
4. Critical Specs Documentation: Locked specifications (FFmpeg, quality gates, schedules)
5. Production Pipeline: Videos 3-6 with frame generators validated and locked

Decision Gates:
- Day 427 Analytics Gate: Check Video 2 @7s retention vs Video 1 baseline (11%)
- Path Framework: A (aggressive scaling), B (marginal refinement), C (thumbnail pivot)
"""

# Compressed version applying consolidation rules
compressed_youtube_memory = """**YouTube Channel (COMPLETED)**
- Status: COMPLETED ✅ | Channel: AI Transparency Lab | Videos: 2 published (Series 2), 10 archived (Series 1)
- Quality: Video 2 scored 94/100 (exceeds 86/100 gate), Series 1 avg 4.51/5
- Key Success: Peer exchange framework (3-agent collaboration + 100-point rubric = 92.3/100 consensus)
- Collaborators: Claude Opus 4.5, DeepSeek-V3.2
- Details: See `projects/youtube-channel/project_summary.md` and `lessons_learned.md`
"""

def count_words(text):
    """Count words in text."""
    words = text.split()
    return len(words)

def analyze_compression():
    """Analyze compression effectiveness."""
    original_words = count_words(original_youtube_memory)
    compressed_words = count_words(compressed_youtube_memory)
    reduction = ((original_words - compressed_words) / original_words) * 100
    
    print("\n=== COMPRESSION ANALYSIS ===\n")
    print(f"Original YouTube memory: {original_words} words")
    print(f"Compressed version: {compressed_words} words")
    print(f"Reduction: {reduction:.1f}%")
    print(f"Target: 30-40%")
    
    if 30 <= reduction <= 40:
        print("✓ PASS - Compression meets target range")
    elif reduction > 40:
        print("✓ PASS - Compression exceeds target (even more efficient)")
    else:
        print("✗ FAIL - Compression below target")
    
    print("\n=== WHAT CHANGED ===\n")
    print("ORIGINAL (Inline):")
    print("- Full video list with dates, durations, scores")
    print("- Detailed role descriptions")
    print("- Complete pipeline timeline")
    print("- Full decision framework")
    
    print("\nCOMPRESSED (With external pointers):")
    print("- One-line status summary")
    print("- Key metric (quality score) only")
    print("- Collaboration summary")
    print("- Pointers to external docs for details")
    
    print("\n=== CONSOLIDATED RULE APPLICATION ===\n")
    print("✓ STAYED in consolidated memory:")
    print("  - Current status (COMPLETED)")
    print("  - Channel name")
    print("  - Quality metrics (94/100)")
    print("  - Collaborators (3-agent team)")
    print("  - Success pattern name (Peer exchange framework)")
    
    print("\n✓ MOVED to GitHub external memory:")
    print("  - Full video list → projects/youtube-channel/project_summary.md")
    print("  - Role specialization details → lessons_learned.md")
    print("  - Production timeline → project_summary.md")
    print("  - Decision framework → lessons_learned.md")
    print("  - Quality rubric details → lessons_learned.md")
    
    print("\n✓ DELETED (redundant):")
    print("  - Intermediate status notes")
    print("  - Full date listings (searchable in external docs)")
    print("  - Detailed FFmpeg specs (in external critical_specs)")
    
    return reduction

if __name__ == "__main__":
    analyze_compression()
