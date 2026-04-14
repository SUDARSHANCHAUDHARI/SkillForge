# SkillForge

> Audit, analyze, and manage your AI prompt skill files from the CLI.

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Platform](https://img.shields.io/badge/Platform-macOS%20%7C%20Linux%20%7C%20Windows-lightgrey)

SkillForge scans directories of `.md` skill/prompt files, detects duplicates using cosine similarity, flags quality issues, scores files 0–100, and gives you real-time watching — all from a single CLI. Comes with a VS Code extension and a Chrome extension.

---

## Features

- **Duplicate detection** — TF-IDF cosine similarity across all skill files
- **Quality analysis** — flags vague, too-short, or poorly structured prompts
- **Scoring** — 0–100 quality score per file
- **Lint** — bulk quality check across all files in a table
- **Search** — find skill files by keyword
- **Compare** — directly compare two files for similarity
- **Export** — save full audit report as JSON or Markdown
- **Live watching** — auto-audit on file change
- **Config file** — `.skillforgerc` for default path and threshold
- **VS Code extension** — audit output in dedicated Output Channel
- **Chrome extension** — save prompts as `.md` and analyze inline

---

## Project Structure

```
SkillForge/
├── cli/
│   ├── core/
│   │   ├── scanner.py       # Recursive .md file scanner
│   │   ├── analyzer.py      # Quality checks + scoring
│   │   ├── similarity.py    # TF-IDF duplicate detection
│   │   └── config.py        # .skillforgerc loader
│   └── commands/
│       ├── audit.py         # audit command
│       ├── duplicates.py    # duplicates command
│       ├── analyze.py       # analyze command
│       ├── stats.py         # stats command
│       ├── watch.py         # watch command
│       ├── fix.py           # fix command
│       ├── list_cmd.py      # list command
│       ├── search.py        # search command
│       ├── export.py        # export command
│       ├── score.py         # score command
│       ├── compare.py       # compare command
│       ├── init_cmd.py      # init command
│       └── lint.py          # lint command
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

## Quick Start

```bash
# Scaffold a skills directory + example file + .skillforgerc
python -m cli.main init ./skills

# Run a full audit
python -m cli.main audit ./skills
```

---

## Commands

| Command | Description |
|---|---|
| `init [path]` | Scaffold skills directory, example file, and `.skillforgerc` |
| `audit [path]` | Duplicates + quality issues. Flags: `--threshold`, `--verbose`, `--quiet`, `--json-out` |
| `lint [path]` | Bulk quality check — all files in a table with scores |
| `duplicates [path]` | List duplicate pairs. Flag: `--threshold` |
| `analyze [file]` | Analyze a single `.md` file |
| `score [file]` | Show 0–100 quality score for a file |
| `compare [file_a] [file_b]` | Compare two files — similarity score + common words |
| `search [path] [keyword]` | Find skill files containing a keyword |
| `export [path]` | Save audit report. Flag: `--format json\|md` |
| `stats [path]` | Total files, duplicates, avg length, word count |
| `list [path]` | List all skill files with paths |
| `fix [path]` | Show duplicates and guide manual cleanup |
| `watch [path]` | Watch directory and auto-audit on `.md` change |

### Examples

```bash
python -m cli.main audit ./skills --verbose
python -m cli.main audit ./skills --threshold 0.7
python -m cli.main duplicates ./skills --threshold 0.6
python -m cli.main score ./skills/myprompt.md
python -m cli.main compare ./skills/a.md ./skills/b.md
python -m cli.main search ./skills summarize
python -m cli.main export ./skills --format md
python -m cli.main lint ./skills
```

---

## Config File

Create `.skillforgerc` in your project root (or run `init`):

```json
{
  "path": "./skills",
  "threshold": 0.8,
  "ignore": []
}
```

---

## VS Code Extension

Located in `vscode-extension/`.

**Commands (Command Palette `Cmd+Shift+P`):**
- `SkillForge: Audit` — full audit with per-file scores in Output Channel
- `SkillForge: Duplicates` — duplicate check in Output Channel

To install locally: VS Code → Extensions → `...` → Install from VSIX.

---

## Chrome Extension

Located in `chrome-extension/`.

- **Save Prompt** — downloads prompt as `prompt-YYYY-MM-DD.md`
- **Analyze Prompt** — inline quality check (too short, vague, etc.)

To install: Chrome → `chrome://extensions` → Developer Mode → Load Unpacked → `chrome-extension/`.

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
