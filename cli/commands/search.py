
from rich.console import Console
from cli.core.scanner import scan_skills

console = Console()


def search_cmd(path: str, keyword: str):
    try:
        skills = scan_skills(path)
    except (FileNotFoundError, NotADirectoryError) as e:
        console.print(f"[red]Error:[/red] {e}")
        return

    matches = [s for s in skills if keyword.lower() in s["content"].lower()]

    if not matches:
        console.print(f"[yellow]No matches for '{keyword}'[/yellow]")
        return

    console.print(f"[bold]Found {len(matches)} match(es) for '[cyan]{keyword}[/cyan]':[/bold]\n")
    for s in matches:
        console.print(f"  [cyan]{s['name']}[/cyan]  [dim]{s['path']}[/dim]")
