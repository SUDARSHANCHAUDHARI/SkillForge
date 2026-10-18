
import os
import shutil
from rich.console import Console
from cli.core.scanner import scan_skills
from cli.core.similarity import find_duplicates
from cli.core.analyzer import analyze_text

console = Console()


def _fixes_for(name: str, content: str) -> list:
    """Return list of (description, fixed_content) tuples."""
    fixes = []
    fixed = content

    # Fix 1: Strip leading/trailing whitespace
    stripped = content.strip()
    if stripped != content:
        fixes.append(("Strip leading/trailing whitespace", stripped))
        fixed = stripped

    # Fix 2: Add missing title
    lines = fixed.splitlines()
    has_title = any(line.startswith("# ") for line in lines)
    if not has_title:
        title = "# " + os.path.splitext(name)[0].replace("-", " ").replace("_", " ").title()
        fixed_with_title = title + "\n\n" + fixed
        fixes.append(("Add missing title", fixed_with_title))
        fixed = fixed_with_title

    return fixes


def fix_cmd(path: str, apply: bool = False):
    try:
        skills = scan_skills(path)
    except (FileNotFoundError, NotADirectoryError) as e:
        console.print(f"[red]Error:[/red] {e}")
        return

    if not skills:
        console.print("[yellow]No skill files found.[/yellow]")
        return

    dups = find_duplicates(skills)
    fixable = [(s, _fixes_for(s["name"], s["content"])) for s in skills]
    fixable = [(s, fixes) for s, fixes in fixable if fixes]

    if not dups and not fixable:
        console.print("[green]✔ Nothing to fix.[/green]")
        return

    if dups:
        console.print(f"[yellow]Duplicates ({len(dups)}) — manual review required:[/yellow]")
        for d in dups:
            console.print(f"  [cyan]{d['a']}[/cyan]  ↔  [cyan]{d['b']}[/cyan]  (score: {d['score']:.2f})")
        console.print()

    if fixable:
        console.print(f"[yellow]Auto-fixable ({len(fixable)} file(s)):[/yellow]\n")
        for s, fixes in fixable:
            console.print(f"  [cyan]{s['name']}[/cyan]")
            for desc, _ in fixes:
                console.print(f"    [dim]→ {desc}[/dim]")

        if not apply:
            console.print(f"\n[dim]Dry run — no files changed. Use --apply to fix.[/dim]")
            return

        console.print()
        fixed_count = 0
        for s, fixes in fixable:
            # Apply all fixes in sequence
            content = s["content"]
            for _, new_content in fixes:
                content = new_content
            if content == s["content"]:
                continue
            try:
                # Byte-exact copy of the original; fails (and skips the write) if unreadable.
                shutil.copyfile(s["path"], s["path"] + ".bak")
                with open(s["path"], "w", encoding="utf-8") as f:
                    f.write(content)
                console.print(f"[green]Fixed:[/green] {s['name']}")
                fixed_count += 1
            except OSError as e:
                console.print(f"[red]Error fixing {s['name']}:[/red] {e}")

        console.print(f"\n[bold]Fixed {fixed_count} file(s).[/bold]")
