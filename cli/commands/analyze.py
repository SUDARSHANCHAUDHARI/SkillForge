
import os
from rich.console import Console
from cli.core.analyzer import analyze_text

console = Console()


def analyze_cmd(file: str):
    if not os.path.isfile(file):
        console.print(f"[red]Error:[/red] File not found: {file}")
        return

    try:
        text = open(file, encoding="utf-8").read()
    except OSError as e:
        console.print(f"[red]Error:[/red] Could not read file: {e}")
        return

    issues = analyze_text(text)

    if not issues:
        console.print("[green]✔ Clean[/green]")
    else:
        for issue in issues:
            console.print(f"[yellow]⚠[/yellow] {issue}")
