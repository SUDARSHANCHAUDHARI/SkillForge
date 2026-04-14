
import json
from rich.console import Console
from cli.core.scanner import scan_skills
from cli.core.similarity import find_duplicates
from cli.core.analyzer import analyze_text

console = Console()


def audit_cmd(path: str, json_out: bool = False):
    try:
        skills = scan_skills(path)
    except (FileNotFoundError, NotADirectoryError) as e:
        console.print(f"[red]Error:[/red] {e}")
        return

    if not skills:
        console.print("[yellow]No skill files found.[/yellow]")
        return

    dups = find_duplicates(skills)

    issues_map = {}
    for s in skills:
        issues = analyze_text(s["content"])
        if issues:
            issues_map[s["name"]] = issues

    result = {
        "total": len(skills),
        "duplicates": len(dups),
        "issues": issues_map,
    }

    if json_out:
        print(json.dumps(result, indent=2))
        return

    console.print(f"[bold]Total:[/bold] {len(skills)}")
    console.print(f"[bold]Duplicates:[/bold] {len(dups)}")
    console.print(f"[bold]Files with issues:[/bold] {len(issues_map)}")

    if issues_map:
        console.print()
        for name, issues in issues_map.items():
            for issue in issues:
                console.print(f"  [yellow]⚠[/yellow] {name}: {issue}")
