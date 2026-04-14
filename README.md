# SkillForge

A CLI tool for auditing, analyzing, and managing AI prompt skill files (`.md`).

## Features

- Detect duplicate skill files using cosine similarity
- Analyze skill quality (too short, vague, missing structure)
- Watch directory for changes and auto-audit
- VS Code extension for one-click audit
- Chrome extension to save and analyze prompts

## Install

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

```bash
python -m cli.main audit ./skills
python -m cli.main duplicates ./skills
python -m cli.main analyze ./skills/myprompt.md
python -m cli.main stats ./skills
python -m cli.main list ./skills
python -m cli.main fix ./skills
python -m cli.main watch ./skills
```

Or use the entry point:

```bash
python skillforge.py audit ./skills
```

## Commands

| Command | Description |
|---|---|
| `audit` | Scan for duplicates and quality issues |
| `duplicates` | List duplicate skill pairs |
| `analyze` | Analyze a single skill file |
| `stats` | Show file count, avg length, word count |
| `list` | List all skill files |
| `fix` | Show duplicates for manual cleanup |
| `watch` | Watch directory and re-audit on change |

## Extensions

- **VS Code** — `vscode-extension/` — commands: `SkillForge: Audit`, `SkillForge: Duplicates`
- **Chrome** — `chrome-extension/` — save and analyze prompts from the browser

## Author

[SudarshanTechLabs](https://github.com/SUDARSHANCHAUDHARI)

## License

MIT
