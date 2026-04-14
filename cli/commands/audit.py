
import json
from rich.console import Console
from cli.core.scanner import scan_skills
from cli.core.similarity import find_duplicates
from cli.core.analyzer import analyze_text, score_text

console = Console()


def audit_cmd(
    path: str,
    json_out: bool = False,
    threshold: float = 0.8,
    quiet: bool = False,
    verbose: bool = False,
):
    try:
        skills = scan_skills(path)
    except (FileNotFoundError, NotADirectoryError) as e:
        console.print(f"[red]Error:[/red] {e}")
        return

    if not skills:
        if not quiet:
            console.print("[yellow]No skill files found.[/yellow]")
        return

    dups = find_duplicates(skills, threshold=threshold)

    issues_map = {}
    scores_map = {}
    for s in skills:
        issues = analyze_text(s["content"])
        scores_map[s["name"]] = score_text(s["content"])
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

    if not quiet:
        console.print(f"[bold]Total:[/bold] {len(skills)}")
        console.print(f"[bold]Duplicates:[/bold] {len(dups)}")
        console.print(f"[bold]Files with issues:[/bold] {len(issues_map)}")

    if verbose:
        console.print()
        for s in skills:
            sc = scores_map[s["name"]]
            color = "green" if sc >= 80 else "yellow" if sc >= 50 else "red"
            issues = issues_map.get(s["name"], [])
            console.print(f"  [{color}]{sc:3}/100[/{color}]  [cyan]{s['name']}[/cyan]")
            for issue in issues:
                console.print(f"         [yellow]⚠[/yellow] {issue}")
    elif issues_map and not quiet:
        console.print()
        for name, issues in issues_map.items():
            for issue in issues:
                console.print(f"  [yellow]⚠[/yellow] {name}: {issue}")
