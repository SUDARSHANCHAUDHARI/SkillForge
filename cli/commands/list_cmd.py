
from rich.console import Console
from cli.core.scanner import scan_skills

console = Console()


def list_cmd(path: str):
    try:
        skills = scan_skills(path)
    except (FileNotFoundError, NotADirectoryError) as e:
        console.print(f"[red]Error:[/red] {e}")
        return

    if not skills:
        console.print("[yellow]No skill files found.[/yellow]")
        return

    for s in skills:
        console.print(f"  [cyan]{s['name']}[/cyan]  [dim]{s['path']}[/dim]")

    console.print(f"\n[bold]Total:[/bold] {len(skills)}")
