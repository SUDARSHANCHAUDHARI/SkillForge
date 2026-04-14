# Contributing to SkillForge

Thanks for your interest. Contributions are welcome — bug fixes, new commands, or improvements to existing ones.

---

## Project structure

```
SkillForge/
├── cli/
│   ├── core/          # Scanner, analyzer, similarity, config
│   └── commands/      # One file per CLI command
├── vscode-extension/  # VS Code extension
├── chrome-extension/  # Chrome extension
├── docs/              # Documentation
└── skills/            # Test skill files
```

Each CLI command lives in its own file under `cli/commands/`. Adding a new command means:
1. Create `cli/commands/your_cmd.py`
2. Define `your_cmd(...)` function
3. Register it in `cli/main.py`

---

## Setup

```bash
git clone https://github.com/SUDARSHANCHAUDHARI/SkillForge.git
cd SkillForge
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## Running the CLI

```bash
python -m cli.main --help
python -m cli.main audit ./skills
```

---

## Code conventions

- Python 3.11+
- Use `rich.console.Console` for all output — no bare `print()` in commands
- All commands must handle `FileNotFoundError` and `NotADirectoryError` from the scanner
- Destructive operations (`--apply`, delete) must be dry-run by default
- Keep commands focused — one responsibility per command file
- No new dependencies without a strong reason — current stack is `typer`, `rich`, `watchdog`, `scikit-learn`

---

## Adding a new command

1. Create `cli/commands/your_cmd.py`:

```python
from rich.console import Console
from cli.core.scanner import scan_skills

console = Console()

def your_cmd(path: str):
    try:
        skills = scan_skills(path)
    except (FileNotFoundError, NotADirectoryError) as e:
        console.print(f"[red]Error:[/red] {e}")
        return
    # your logic here
```

2. Register in `cli/main.py`:

```python
from cli.commands import your_cmd
app.command("your-cmd")(your_cmd.your_cmd)
```

3. Add it to `docs/commands.md` with full flag documentation.

---

## Submitting changes

1. Fork the repo
2. Create a branch: `git checkout -b feature/your-feature`
3. Make your changes
4. Test manually: `python -m cli.main your-cmd ./skills`
5. Open a pull request with a clear description of what changed and why

---

## Reporting bugs

Open an issue at [github.com/SUDARSHANCHAUDHARI/SkillForge/issues](https://github.com/SUDARSHANCHAUDHARI/SkillForge/issues) with:
- Command you ran
- Expected output
- Actual output
- Python version (`python3 --version`)
