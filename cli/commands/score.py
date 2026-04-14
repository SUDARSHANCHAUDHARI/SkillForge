
import os
from rich.console import Console
from cli.core.analyzer import score_text, analyze_text

console = Console()


def score_cmd(file: str):
    if not os.path.isfile(file):
        console.print(f"[red]Error:[/red] File not found: {file}")
        return

    try:
        text = open(file, encoding="utf-8").read()
    except OSError as e:
        console.print(f"[red]Error:[/red] Could not read file: {e}")
        return

    s = score_text(text)
    issues = analyze_text(text)

    color = "green" if s >= 80 else "yellow" if s >= 50 else "red"
    console.print(f"Score: [{color}]{s}/100[/{color}]")

    if issues:
        console.print()
        for issue in issues:
            console.print(f"  [yellow]⚠[/yellow] {issue}")
