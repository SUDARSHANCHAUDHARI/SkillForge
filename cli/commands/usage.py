
import os
import json
import glob
from collections import defaultdict
from datetime import datetime
from rich.console import Console
from rich.table import Table
from cli.core.scanner import scan_skills

console = Console()

HISTORY_ROOT = os.path.expanduser("~/.claude/projects/")


def _parse_history(history_root: str) -> dict:
    """Return {skill_name: {"count": int, "last_used": str}}"""
    usage = defaultdict(lambda: {"count": 0, "last_used": None})

    pattern = os.path.join(history_root, "**", "*.jsonl")
    for filepath in glob.glob(pattern, recursive=True):
        try:
            with open(filepath, encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        obj = json.loads(line)
                    except json.JSONDecodeError:
                        continue

                    timestamp = obj.get("timestamp", "")
                    msg = obj.get("message", {})
                    if not isinstance(msg, dict):
                        continue

                    for block in msg.get("content", []):
                        if not isinstance(block, dict):
                            continue
                        if block.get("type") == "tool_use" and block.get("name") == "Skill":
                            skill = block.get("input", {}).get("skill", "").strip()
                            if skill:
                                usage[skill]["count"] += 1
                                if timestamp:
                                    prev = usage[skill]["last_used"]
                                    if prev is None or timestamp > prev:
                                        usage[skill]["last_used"] = timestamp
        except OSError:
            continue

    return dict(usage)


def usage_cmd(path: str, history: str = HISTORY_ROOT):
    try:
        skills = scan_skills(path)
    except (FileNotFoundError, NotADirectoryError) as e:
        console.print(f"[red]Error:[/red] {e}")
        return

    if not skills:
        console.print("[yellow]No skill files found.[/yellow]")
        return

    if not os.path.isdir(history):
        console.print(f"[yellow]History not found at:[/yellow] {history}")
        return

    usage_data = _parse_history(history)

    local_names = {os.path.splitext(s["name"])[0] for s in skills}

    table = Table(title="Skill Usage")
    table.add_column("Skill", style="cyan")
    table.add_column("Invocations", style="bold", justify="right")
    table.add_column("Last Used", style="dim")
    table.add_column("Status")

    used = []
    unused = []

    for s in skills:
        stem = os.path.splitext(s["name"])[0]
        data = usage_data.get(stem) or usage_data.get(s["name"])
        if data and data["count"] > 0:
            used.append((s["name"], data["count"], data["last_used"]))
        else:
            unused.append(s["name"])

    used.sort(key=lambda x: x[1], reverse=True)

    for name, count, last_used in used:
        last = last_used[:10] if last_used else "—"
        table.add_row(name, str(count), last, "[green]active[/green]")

    for name in unused:
        table.add_row(name, "0", "—", "[red]never used[/red]")

    console.print(table)
    console.print(f"\n[bold]Active:[/bold] {len(used)}  [bold]Unused:[/bold] {len(unused)}")

    if unused:
        console.print(f"\n[yellow]Tip:[/yellow] Run [cyan]skillforge cleanup {path}[/cyan] to remove unused files.")
