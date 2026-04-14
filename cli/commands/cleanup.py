
import os
import typer
from rich.console import Console
from cli.core.scanner import scan_skills

console = Console()


def _is_broken(content: str) -> str | None:
    """Return reason string if file should be cleaned up, else None."""
    if not content.strip():
        return "empty"
    if len(content.strip()) < 10:
        return "too short (under 10 chars)"
    if len(content.split()) < 2:
        return "single word"
    return None


def cleanup_cmd(path: str, apply: bool = False):
    try:
        skills = scan_skills(path)
    except (FileNotFoundError, NotADirectoryError) as e:
        console.print(f"[red]Error:[/red] {e}")
        return

    if not skills:
        console.print("[yellow]No skill files found.[/yellow]")
        return

    broken = [(s, _is_broken(s["content"])) for s in skills]
    broken = [(s, reason) for s, reason in broken if reason]

    if not broken:
        console.print(f"[green]✔ All {len(skills)} files are healthy.[/green]")
        return

    console.print(f"[yellow]Found {len(broken)} file(s) to clean up:[/yellow]\n")
    for s, reason in broken:
        console.print(f"  [red]✗[/red] [cyan]{s['name']}[/cyan]  — {reason}")
        console.print(f"     [dim]{s['path']}[/dim]")

    if not apply:
        console.print(f"\n[dim]Dry run — no files deleted. Use --apply to delete.[/dim]")
        return

    console.print()
    confirmed = typer.confirm(f"Delete {len(broken)} file(s)?")
    if not confirmed:
        console.print("[yellow]Cancelled.[/yellow]")
        return

    deleted = 0
    for s, reason in broken:
        try:
            os.remove(s["path"])
            console.print(f"[red]Deleted:[/red] {s['name']}")
            deleted += 1
        except OSError as e:
            console.print(f"[red]Error deleting {s['name']}:[/red] {e}")

    console.print(f"\n[bold]Deleted {deleted} file(s).[/bold]")
