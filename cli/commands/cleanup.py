
import os
import subprocess
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


def _git_tracked(path: str) -> set:
    """Absolute paths of git-tracked files under path; empty if not a repo or git missing."""
    try:
        out = subprocess.run(["git", "-C", path, "ls-files", "-z"], capture_output=True, check=True).stdout
    except (OSError, subprocess.CalledProcessError):
        return set()
    return {os.path.realpath(os.path.join(path, f)) for f in out.decode("utf-8", "replace").split("\0") if f}


def _is_candidate(path: str, file_path: str, tracked: set) -> bool:
    """Only untracked files outside hidden dirs (.git, .claude, ...) may be deleted."""
    rel = os.path.relpath(file_path, path)
    if any(part.startswith(".") for part in rel.split(os.sep)[:-1]):
        return False
    return os.path.realpath(file_path) not in tracked


def cleanup_cmd(path: str, apply: bool = False):
    try:
        skills = scan_skills(path)
    except (FileNotFoundError, NotADirectoryError) as e:
        console.print(f"[red]Error:[/red] {e}")
        return

    if not skills:
        console.print("[yellow]No skill files found.[/yellow]")
        return

    tracked = _git_tracked(path)
    skills = [s for s in skills if _is_candidate(path, s["path"], tracked)]
    if not skills:
        console.print("[yellow]No untracked skill files to check (git-tracked and hidden-dir files are skipped).[/yellow]")
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
