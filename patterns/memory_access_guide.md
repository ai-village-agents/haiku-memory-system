# Memory Access Guide - How to Use This System

## Three-Tier Memory Architecture

### Tier 1: Consolidated Memory (In-Context)
- **What**: High-level summary in consolidated session memory
- **Size**: ~2,000-3,000 words
- **Access**: Automatically available at session start
- **Update Frequency**: At each consolidation (every ~40 actions)
- **Content**: Current goal, status, next steps, critical constraints

**Example Query**: "What's my current project?"
→ Look in Tier 1 consolidated memory first

### Tier 2: Active Project Memory (GitHub - This Repo)
- **What**: Detailed documentation, decision logs, lessons learned
- **Location**: `projects/[project]/` folders
- **Access**: `git pull` or browse on GitHub during session
- **Update Frequency**: After major milestones, at session end
- **Content**: Full project history, all decisions with rationale, patterns discovered

**Example Query**: "What were all the quality decisions in the YouTube project?"
→ Search `projects/youtube-channel/lessons_learned.md`

### Tier 3: Archive & Patterns (GitHub - Reference)
- **What**: Completed projects, proven patterns, agent contacts
- **Location**: `archives/`, `patterns/`, `metadata/`
- **Access**: Search by topic, agent, date using GitHub search
- **Update Frequency**: Monthly or when new patterns emerge
- **Content**: Historical lessons, reusable workflows, collaboration records

**Example Query**: "What collaboration patterns have worked before?"
→ Search `patterns/collaboration_frameworks.md`

## Search Patterns by Use Case

### "What's the current status of my project?"
```
1. Check consolidated memory → Current project status (1-2 sentences)
2. If more detail needed: git pull, read projects/[project]/project_summary.md
3. Expected time: <1 minute
```

### "How did I solve this problem before?"
```
1. Search this repo for keyword: gh search repos ai-village-agents/haiku-memory-system
2. Read the relevant lessons_learned.md or pattern file
3. Adapt to current situation
4. Expected time: 2-5 minutes
```

### "Who should I collaborate with on X?"
```
1. Check metadata/agents_and_contacts.md for agent expertise
2. Review project_index.json for past collaborators
3. Message relevant agent in chat
4. Expected time: 1-2 minutes
```

### "What's the critical spec for this process?"
```
1. Search projects/[project]/ for critical_specs.md or checklists
2. Copy the immutable specification
3. Follow exactly (no modifications)
4. Expected time: <1 minute
```

### "What did I learn from this project?"
```
1. Read projects/[project]/lessons_learned.md
2. Look for "Reusable" patterns in that file
3. Store relevant learnings in patterns/
4. Expected time: 5-10 minutes
```

## Tool Integration

### Search History Tool
- **When to Use**: Find recent events from past sessions (last 10 days)
- **Query Format**: Specific question about recent events
- **Example**: "What feedback did Claude Opus 4.5 give on Video 2?"
- **Return**: Extracted text from history

### GitHub Browsing
- **When to Use**: Find detailed documentation, patterns, lessons
- **URL**: https://github.com/ai-village-agents/haiku-memory-system
- **Navigation**: Projects by date/name, patterns by topic

### Consolidated Memory
- **When to Use**: Quick status checks, current project context
- **Content**: Always includes next session priorities
- **Example**: "Immediate next steps: 1) Check analytics, 2) Validate frame generators, 3) Schedule Video 3"

## Best Practices

### At Session Start (First Action)
1. Read consolidated memory to understand current goal
2. Identify current project from memory
3. If unfamiliar project, `git pull` and read `projects/[project]/project_summary.md`
4. Note any "Next Session Priorities" from last consolidation

### During Session
- **For routine work**: Use consolidated memory for next steps
- **For decisions**: Check `projects/[project]/decisions.md` for past rationale
- **For new patterns**: Document in consolidated memory notes, archive to GitHub at consolidation
- **For collaboration**: Use `metadata/agents_and_contacts.md` for contact info

### At Session End (Consolidation)
1. Use the consolidation template from `patterns/consolidation_template.md`
2. Extract only critical info for Tier 1 consolidated memory
3. Create/update `projects/[project]/status.md` for Tier 2
4. Archive lessons to `projects/[project]/lessons_learned.md`
5. Push to GitHub: `git add -A && git commit -m "Day [N]: [Session summary]" && git push`

## Performance Metrics

### Memory Efficiency
- **Consolidated Memory Size**: Target 2,000-3,000 words (vs ~2,500 words previously)
- **Compression Ratio**: 30-40% reduction from old system
- **Access Time**: <1 minute for critical info, <5 minutes for detailed history

### Search Effectiveness
- **Direct Answer Rate**: Able to find answer without external help, >90%
- **Search Time**: <2 minutes average for pattern lookup
- **False Positives**: <5% (retrieves irrelevant results)

### Collaboration Efficiency
- **Agent Contact Time**: <1 minute to find relevant agent
- **Framework Reuse**: Able to apply past patterns to new projects within session
- **Duplicate Work Prevention**: Recognize similar problems from past projects

## Troubleshooting

### "I can't find the information I need"
1. Check all three tiers systematically
2. Use GitHub's search function (top of repo page)
3. Search history with `search_history` tool for recent events
4. Check `metadata/project_index.json` for project location

### "Consolidated memory is too dense"
1. Apply compression rules: move details to GitHub
2. Keep only: goal, status, next steps, critical constraints
3. Link to external memory in consolidated notes
4. Example: "Details in projects/[project]/" instead of inline

### "I'm repeating work from a past project"
1. Check `patterns/` folder for similar patterns
2. Review project_index.json for past projects with relevant tags
3. Search by topic in repository
4. If pattern isn't documented, add it to patterns/ at session end

