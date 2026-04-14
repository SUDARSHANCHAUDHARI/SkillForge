# Changelog

All notable changes to SkillForge are documented here.

---

## [0.3.0] — 2026-04-14

### Added
- `usage` command — parses `~/.claude/projects/` conversation history to show skill invocation counts and last-used dates
- `cleanup` command — finds empty, whitespace-only, or broken skill files; deletes with `--apply` and confirmation prompt
- `fix` command rewritten — now auto-fixes whitespace and missing titles with dry-run by default; `--apply` to write changes

---

## [0.2.0] — 2026-04-14

### Added
- `search` command — find skill files by keyword
- `export` command — save full audit report as JSON or Markdown (`--format json|md`)
- `score` command — 0–100 quality score per file, color coded
- `compare` command — similarity score + common words between two files
- `init` command — scaffold skills directory, example template, and `.skillforgerc`
- `lint` command — bulk quality table across all files with scores
- `--threshold` flag on `audit` and `duplicates`
- `--verbose` flag on `audit` — per-file score breakdown
- `--quiet` flag on `audit` and `lint`
- `.skillforgerc` config file support (`cli/core/config.py`)
- `score_text()` function in `cli/core/analyzer.py`
- VS Code extension now uses OutputChannel for full scrollable output

---

## [0.1.0] — 2026-04-14

### Added
- Initial release
- `audit` — duplicate detection + quality issues, `--json-out` flag
- `duplicates` — list duplicate pairs with rich table
- `analyze` — single file quality check
- `stats` — file count, avg length, word count
- `watch` — watchdog file watcher, re-audits on `.md` change
- `fix` — list duplicates for manual review
- `list` — list all skill files
- `cli/core/scanner.py` — recursive `.md` scanner with safe error handling
- `cli/core/analyzer.py` — rule-based quality checks
- `cli/core/similarity.py` — TF-IDF cosine similarity duplicate detection
- `skillforge.py` entry point
- VS Code extension — `SkillForge: Audit` and `SkillForge: Duplicates` commands
- Chrome extension — Save Prompt + Analyze Prompt with timestamp
- `.gitignore`, `README.md`, `LICENSE`
