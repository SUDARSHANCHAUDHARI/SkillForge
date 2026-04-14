
from rich.console import Console
from cli.core.scanner import scan_skills
from cli.core.similarity import find_duplicates

console = Console()


def fix_cmd(path: str):
    try:
        skills = scan_skills(path)
    except (FileNotFoundError, NotADirectoryError) as e:
        console.print(f"[red]Error:[/red] {e}")
        return

    dups = find_duplicates(skills)

    if not dups:
        console.print("[green]No duplicates found. Nothing to fix.[/green]")
        return

    console.print(f"[yellow]Found {len(dups)} duplicate pair(s):[/yellow]\n")
    for d in dups:
        console.print(f"  [cyan]{d['a']}[/cyan]  ↔  [cyan]{d['b']}[/cyan]  (score: {d['score']:.2f})")

    console.print("\n[bold]Manual cleanup recommended.[/bold] Auto-delete is not enabled.")
