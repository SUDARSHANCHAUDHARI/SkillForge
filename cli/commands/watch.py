
import time
from rich.console import Console
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from cli.commands.audit import audit_cmd

console = Console()


class SkillHandler(FileSystemEventHandler):
    def __init__(self, path: str):
        self.path = path

    def on_modified(self, event):
        if event.src_path.endswith(".md"):
            console.print(f"[cyan]Change detected:[/cyan] {event.src_path}")
            audit_cmd(self.path)


def watch_cmd(path: str):
    try:
        obs = Observer()
        obs.schedule(SkillHandler(path), path, recursive=True)
        obs.start()
        console.print(f"[green]Watching:[/green] {path}  (Ctrl+C to stop)")
        while True:
            time.sleep(2)
    except KeyboardInterrupt:
        obs.stop()
        console.print("[yellow]Stopped.[/yellow]")
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
    finally:
        obs.join()
