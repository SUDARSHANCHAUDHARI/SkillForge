# SkillForge

> Audit, analyze, and manage your AI prompt skill files from the CLI.

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Platform](https://img.shields.io/badge/Platform-macOS%20%7C%20Linux%20%7C%20Windows-lightgrey)

SkillForge scans directories of `.md` skill/prompt files, detects duplicates using cosine similarity, flags quality issues, and gives you real-time watching — all from a single CLI. Comes with a VS Code extension and a Chrome extension.

---

## Features

- **Duplicate detection** — TF-IDF cosine similarity across all skill files
- **Quality analysis** — flags vague, too-short, or poorly structured prompts
- **Live watching** — auto-audit on file change using watchdog
- **Rich output** — clean tables and colored output via Rich
- **VS Code extension** — audit and duplicates commands in the editor
- **Chrome extension** — save prompts as `.md` files and analyze them inline

---

## Project Structure

```
SkillForge/
├── cli/
│   ├── core/
│   │   ├── scanner.py       # Recursive .md file scanner
│   │   ├── analyzer.py      # Quality checks
│   │   └── similarity.py    # TF-IDF duplicate detection
│   └── commands/
│       ├── audit.py         # audit command
│       ├── duplicates.py    # duplicates command
│       ├── analyze.py       # analyze command
│       ├── stats.py         # stats command
│       ├── watch.py         # watch command
│       ├── fix.py           # fix command
│       └── list_cmd.py      # list command
├── vscode-extension/        # VS Code extension
├── chrome-extension/        # Chrome extension
├── skills/                  # Your skill files go here
├── skillforge.py            # Entry point
└── requirements.txt
```

---

## Install

Requires Python 3.11+.

```bash
git clone https://github.com/SUDARSHANCHAUDHARI/SkillForge.git
cd SkillForge
python3.11 -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

---

## Usage

```bash
# Audit all skills — duplicates + quality issues
python -m cli.main audit ./skills

# List duplicate pairs
python -m cli.main duplicates ./skills

# Analyze a single file
python -m cli.main analyze ./skills/myprompt.md

# Stats — file count, avg length, word count
python -m cli.main stats ./skills

# List all skill files
python -m cli.main list ./skills

# Show duplicates for manual cleanup
python -m cli.main fix ./skills

# Watch directory and re-audit on change
python -m cli.main watch ./skills
```

Or use the shorthand entry point:

```bash
python skillforge.py audit ./skills
```

---

## Commands

| Command | Description |
|---|---|
| `audit [path]` | Scan for duplicates and quality issues. `--json-out` for JSON output. |
| `duplicates [path]` | List all duplicate skill pairs with similarity score |
| `analyze [file]` | Analyze a single `.md` file for quality issues |
| `stats [path]` | Show total files, duplicates, avg length, word count |
| `list [path]` | List all skill files with their paths |
| `fix [path]` | Show duplicates and guide manual cleanup |
| `watch [path]` | Watch directory and auto-audit on any `.md` change |

---

## VS Code Extension

Located in `vscode-extension/`.

**Commands available via Command Palette (`Cmd+Shift+P`):**
- `SkillForge: Audit` — runs audit on `./skills`
- `SkillForge: Duplicates` — runs duplicates check on `./skills`

To install locally: open VS Code → Extensions → `...` → Install from VSIX (after packaging).

---

## Chrome Extension

Located in `chrome-extension/`.

**Buttons:**
- **Save Prompt** — pastes your prompt and downloads it as `prompt-YYYY-MM-DD.md`
- **Analyze Prompt** — checks for quality issues inline (too short, vague summarization, etc.)

To install: Chrome → `chrome://extensions` → Enable Developer Mode → Load Unpacked → select `chrome-extension/`.

---

## Requirements

```
typer
rich
watchdog
scikit-learn
```

---

## Author

**SudarshanTechLabs** — [github.com/SUDARSHANCHAUDHARI](https://github.com/SUDARSHANCHAUDHARI)

## License

MIT
