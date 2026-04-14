
from rich.console import Console
from rich.table import Table
from cli.core.scanner import scan_skills
from cli.core.similarity import find_duplicates

console = Console()


def duplicates_cmd(path: str):
    try:
        skills = scan_skills(path)
    except (FileNotFoundError, NotADirectoryError) as e:
        console.print(f"[red]Error:[/red] {e}")
        return

    dups = find_duplicates(skills)

    if not dups:
        console.print("[green]No duplicates found.[/green]")
        return

    table = Table(title="Duplicate Skills")
    table.add_column("File A", style="cyan")
    table.add_column("File B", style="cyan")
    table.add_column("Score", style="yellow")

    for d in dups:
        table.add_row(d["a"], d["b"], f"{d['score']:.2f}")

    console.print(table)
