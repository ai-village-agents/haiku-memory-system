#!/usr/bin/env python3
"""Scan AI Village agent inventories via raw GitHub fetches."""

import argparse
import json
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from typing import Iterable, List, Optional
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

try:
    import yaml  # type: ignore
except ImportError:  # pragma: no cover - simple runtime guard
    yaml = None

AGENT_REPOS: List[str] = [
    "ai-village-agents/haiku-memory-system", "ai-village-agents/claude-opus-memory",
    "ai-village-agents/opus-46-memory", "ai-village-agents/gemini-3.1-pro-memory",
    "ai-village-agents/gpt-5-4-memory-kit", "ai-village-agents/gpt-5-2-memory-improvement",
    "ai-village-agents/deepseek-r1-memory", "ai-village-agents/gemini-flash-memory",
    "ai-village-agents/sonnet-3.5-memory", "ai-village-agents/gpt-4o-mini-memory",
    "ai-village-agents/llama-3-memory", "ai-village-agents/mistral-large-memory",
    "ai-village-agents/mixtral-8x7b-memory", "ai-village-agents/qwen-2.5-memory",
    "ai-village-agents/claude-3.7-memory", "ai-village-agents/o1-preview-memory",
]

RAW_PATHS = ("main", "master")
USER_AGENT = "ai-village-inventory-scanner/0.1"
CORE_FIELDS = ("id", "status", "kind", "summary", "source", "last_verified", "retrieval_cue")
@dataclass
class InventoryItem:
    agent: str
    id: str
    status: str
    kind: str
    summary: str
    source: str
    last_verified: str
    retrieval_cue: str

def fetch_inventory_yaml(repo: str) -> Optional[str]:
    """Fetch inventory.yaml content from GitHub raw; return None on failure."""
    for branch in RAW_PATHS:
        url = f"https://raw.githubusercontent.com/{repo}/{branch}/inventory.yaml"
        try:
            req = Request(url, headers={"User-Agent": USER_AGENT})
            with urlopen(req, timeout=10) as resp:
                return resp.read().decode("utf-8")
        except HTTPError as exc:
            # Try next branch if 404; otherwise propagate as warning upstream
            if exc.code != 404:
                raise
        except URLError:
            raise
    return None


def parse_inventory(agent: str, raw_yaml: str) -> List[InventoryItem]:
    """Parse inventory YAML and normalize fields."""
    if yaml is None:
        raise RuntimeError("pyyaml is not installed; run `pip install pyyaml`.")

    loaded = yaml.safe_load(raw_yaml)
    if not isinstance(loaded, list):
        raise ValueError("inventory.yaml must be a list of items.")

    items: List[InventoryItem] = []
    for entry in loaded:
        if not isinstance(entry, dict):
            continue
        normalized = {f: "" if entry.get(f) is None else str(entry.get(f)).strip() for f in CORE_FIELDS}
        items.append(
            InventoryItem(
                agent=agent,
                id=normalized["id"],
                status=normalized["status"],
                kind=normalized["kind"],
                summary=normalized["summary"],
                source=normalized["source"],
                last_verified=normalized["last_verified"],
                retrieval_cue=normalized["retrieval_cue"],
            )
        )
    return items


def summarize_status(items: Iterable[InventoryItem]) -> str:
    counts = Counter(item.status or "unknown" for item in items)
    return ", ".join(f"{s}:{c}" for s, c in counts.most_common()) or "n/a"


def summarize_kinds(items: Iterable[InventoryItem], limit: int = 3) -> str:
    counts = Counter(item.kind or "unspecified" for item in items)
    return ", ".join(kind for kind, _ in counts.most_common(limit)) or "n/a"


def print_table(rows: List[dict]) -> None:
    agent_width = max(len(row["agent"]) for row in rows + [{"agent": "Agent"}])
    header = f"{'Agent'.ljust(agent_width)} | Items | Status Summary               | Sample Kinds"
    divider = "-" * len(header)
    print(divider)
    print(header)
    print(divider)
    for row in rows:
        print(
            f"{row['agent'].ljust(agent_width)} | "
            f"{str(row['count']).rjust(5)} | "
            f"{row['status'][:30].ljust(30)} | "
            f"{row['kinds']}"
        )
    print(divider)


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Scan agent inventories via raw GitHub.")
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show individual inventory items for each agent.",
    )
    parser.add_argument(
        "--save",
        metavar="PATH",
        default=None,
        help="Optional JSON file to write aggregated inventories (inventories.json).",
    )
    args = parser.parse_args(argv)

    aggregated: List[InventoryItem] = []; warnings: List[str] = []
    per_agent = defaultdict(list)
    for repo in AGENT_REPOS:
        agent = repo.split("/")[-1].replace("-memory", "")
        try:
            raw_yaml = fetch_inventory_yaml(repo)
        except HTTPError as exc:
            warnings.append(f"{repo}: HTTP error {exc.code} while fetching inventory.yaml")
            continue
        except URLError as exc:
            warnings.append(f"{repo}: network error {exc.reason}")
            continue

        if raw_yaml is None:
            warnings.append(f"{repo}: inventory.yaml not found on main/master")
            continue

        try:
            items = parse_inventory(agent, raw_yaml)
        except Exception as exc:
            warnings.append(f"{repo}: invalid inventory.yaml ({exc})")
            continue

        aggregated.extend(items)
        per_agent[agent].extend(items)

    if aggregated:
        rows = [
            {
                "agent": agent,
                "count": len(items),
                "status": summarize_status(items),
                "kinds": summarize_kinds(items),
            }
            for agent, items in sorted(per_agent.items())
        ]
        print_table(rows)
    else:
        print("No inventories found.")

    if warnings:
        print("\nWarnings:")
        for note in warnings:
            print(f"  - {note}")

    if args.verbose and aggregated:
        print("\nVerbose items:")
        for item in aggregated:
            print(
                f"[{item.agent}] {item.id or '<no-id>'} | "
                f"status={item.status or 'n/a'} | kind={item.kind or 'n/a'} | "
                f"{item.summary or 'no summary'}"
            )

    if args.save and aggregated:
        payload = [item.__dict__ for item in aggregated]
        try:
            with open(args.save, "w", encoding="utf-8") as f:
                json.dump(payload, f, indent=2)
            print(f"\nSaved aggregated inventories to {args.save}")
        except OSError as exc:
            print(f"\nUnable to save inventories: {exc}", file=sys.stderr)
            return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
