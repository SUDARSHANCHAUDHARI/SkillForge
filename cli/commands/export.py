
import json
import os
from datetime import date
from rich.console import Console
from cli.core.scanner import scan_skills
from cli.core.similarity import find_duplicates
from cli.core.analyzer import analyze_text, score_text

console = Console()


def export_cmd(path: str, format: str = "json"):
    try:
        skills = scan_skills(path)
    except (FileNotFoundError, NotADirectoryError) as e:
        console.print(f"[red]Error:[/red] {e}")
        return

    if not skills:
        console.print("[yellow]No skill files found.[/yellow]")
        return

    dups = find_duplicates(skills)
    today = date.today().isoformat()

    report = {
        "date": today,
        "total": len(skills),
        "duplicates": dups,
        "files": [
            {
                "name": s["name"],
                "path": s["path"],
                "score": score_text(s["content"]),
                "issues": analyze_text(s["content"]),
            }
            for s in skills
        ],
    }

    if format == "json":
        out_file = f"skillforge-report-{today}.json"
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)

    elif format == "md":
        out_file = f"skillforge-report-{today}.md"
        lines = [f"# SkillForge Report — {today}\n"]
        lines.append(f"**Total:** {report['total']}  ")
        lines.append(f"**Duplicates:** {len(dups)}\n")
        lines.append("## Files\n")
        for entry in report["files"]:
            lines.append(f"### {entry['name']}")
            lines.append(f"- Score: {entry['score']}/100")
            if entry["issues"]:
                for issue in entry["issues"]:
                    lines.append(f"- ⚠ {issue}")
            else:
                lines.append("- ✔ Clean")
            lines.append("")
        if dups:
            lines.append("## Duplicates\n")
            for d in dups:
                lines.append(f"- `{d['a']}` ↔ `{d['b']}` (score: {d['score']:.2f})")
        with open(out_file, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

    else:
        console.print(f"[red]Unknown format:[/red] {format}. Use 'json' or 'md'.")
        return

    console.print(f"[green]Report saved:[/green] {out_file}")
