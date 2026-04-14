
from rich.console import Console
from rich.table import Table
from cli.core.scanner import scan_skills
from cli.core.similarity import find_duplicates

console = Console()


def stats_cmd(path: str):
    try:
        skills = scan_skills(path)
    except (FileNotFoundError, NotADirectoryError) as e:
        console.print(f"[red]Error:[/red] {e}")
        return

    if not skills:
        console.print("[yellow]No skill files found.[/yellow]")
        return

    dups = find_duplicates(skills)
    lengths = [len(s["content"]) for s in skills]
    avg_len = sum(lengths) // len(lengths) if lengths else 0
    total_words = sum(len(s["content"].split()) for s in skills)

    table = Table(title="SkillForge Stats")
    table.add_column("Metric", style="bold")
    table.add_column("Value", style="cyan")

    table.add_row("Total files", str(len(skills)))
    table.add_row("Duplicates", str(len(dups)))
    table.add_row("Avg file length (chars)", str(avg_len))
    table.add_row("Total words", str(total_words))

    console.print(table)
