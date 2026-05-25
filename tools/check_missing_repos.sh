#!/bin/bash
# Check for inventory.yaml files in known #best agent repos

AGENTS=(
    "claude-opus-4.7-memory"
    "gemini-3.5-flash-memory"
    "gpt-5.5-memory"
    "kimi-k2.6-memory"
)

echo "Checking for inventory.yaml in #best agent repos..."
echo ""

for agent in "${AGENTS[@]}"; do
    echo "Checking: ai-village-agents/$agent"
    
    # Try common paths
    for path in "" "metadata/" "memory/"; do
        url="https://raw.githubusercontent.com/ai-village-agents/$agent/main/${path}inventory.yaml"
        status=$(curl -s -o /dev/null -w "%{http_code}" "$url")
        if [ "$status" = "200" ]; then
            echo "  ✓ Found at: $path"
            break
        fi
    done
    
    # Try master branch if main doesn't have it
    if [ "$status" != "200" ]; then
        for path in "" "metadata/" "memory/"; do
            url="https://raw.githubusercontent.com/ai-village-agents/$agent/master/${path}inventory.yaml"
            status=$(curl -s -o /dev/null -w "%{http_code}" "$url")
            if [ "$status" = "200" ]; then
                echo "  ✓ Found at: $path (master branch)"
                break
            fi
        done
    fi
    
    if [ "$status" != "200" ]; then
        echo "  ✗ No inventory.yaml found"
    fi
    echo ""
done
