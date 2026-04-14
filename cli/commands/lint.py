
from rich.console import Console
from rich.table import Table
from cli.core.scanner import scan_skills
from cli.core.analyzer import analyze_text, score_text

console = Console()


def lint_cmd(path: str, quiet: bool = False):
    try:
        skills = scan_skills(path)
    except (FileNotFoundError, NotADirectoryError) as e:
        console.print(f"[red]Error:[/red] {e}")
        return

    if not skills:
        console.print("[yellow]No skill files found.[/yellow]")
        return

    flagged = [(s, analyze_text(s["content"]), score_text(s["content"])) for s in skills]
    flagged_only = [(s, issues, sc) for s, issues, sc in flagged if issues]

    if not flagged_only:
        if not quiet:
            console.print(f"[green]✔ All {len(skills)} files passed.[/green]")
        return

    table = Table(title=f"Lint Results — {len(flagged_only)}/{len(skills)} files flagged")
    table.add_column("File", style="cyan")
    table.add_column("Score", style="bold")
    table.add_column("Issues")

    for s, issues, sc in flagged_only:
        color = "green" if sc >= 80 else "yellow" if sc >= 50 else "red"
        table.add_row(
            s["name"],
            f"[{color}]{sc}/100[/{color}]",
            "\n".join(f"⚠ {i}" for i in issues),
        )

    console.print(table)
