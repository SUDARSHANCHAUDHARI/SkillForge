
import os
from rich.console import Console

console = Console()

TEMPLATE = """# Skill Name

## Purpose
Describe what this skill does in one sentence.

## Instructions
Write clear, specific instructions here.
- Be explicit about the output format
- Include context and constraints
- Avoid vague language like "summarize this" without structure

## Example Output
Optional: show an example of the expected output.
"""


def init_cmd(path: str = "./skills"):
    if os.path.exists(path):
        console.print(f"[yellow]Directory already exists:[/yellow] {path}")
    else:
        os.makedirs(path)
        console.print(f"[green]Created:[/green] {path}")

    example_path = os.path.join(path, "example-skill.md")
    if os.path.exists(example_path):
        console.print(f"[yellow]Already exists:[/yellow] {example_path}")
    else:
        with open(example_path, "w", encoding="utf-8") as f:
            f.write(TEMPLATE)
        console.print(f"[green]Created:[/green] {example_path}")

    rc_path = os.path.join(os.getcwd(), ".skillforgerc")
    if not os.path.exists(rc_path):
        import json
        config = {"path": path, "threshold": 0.8, "ignore": []}
        with open(rc_path, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2)
        console.print(f"[green]Created:[/green] .skillforgerc")

    console.print(f"\n[bold]Ready.[/bold] Run: python -m cli.main audit {path}")
