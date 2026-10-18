# Command Reference

Full reference for all 15 SkillForge CLI commands.

**Base usage:**
```bash
python -m cli.main <command> [arguments] [options]
```

---

## init

Scaffold a new skills directory with an example file and config.

```bash
python -m cli.main init [PATH]
```

| Argument | Default | Description |
|---|---|---|
| `path` | `./skills` | Directory to create |

**What it creates:**
- `PATH/` — the skills directory
- `PATH/example-skill.md` — starter template
- `.skillforgerc` — config file in the current directory

**Example:**
```bash
python -m cli.main init ./my-skills
```

---

## audit

Full audit — duplicates + quality issues across all skill files.

```bash
python -m cli.main audit PATH [OPTIONS]
```

| Option | Default | Description |
|---|---|---|
| `--threshold` | `0.8` | Similarity threshold for duplicate detection (0.0–1.0) |
| `--verbose` | off | Show per-file score breakdown |
| `--quiet` | off | Suppress all output except errors |
| `--json-out` | off | Print results as JSON |

**Examples:**
```bash
python -m cli.main audit ./skills
python -m cli.main audit ./skills --verbose
python -m cli.main audit ./skills --threshold 0.7
python -m cli.main audit ./skills --json-out
python -m cli.main audit ./skills --quiet   # for CI/scripts
```

---

## lint

Bulk quality check — all files in a rich table with scores.

```bash
python -m cli.main lint PATH [OPTIONS]
```

| Option | Default | Description |
|---|---|---|
| `--quiet` | off | Only output if issues are found |

**Example:**
```bash
python -m cli.main lint ./skills
```

---

## analyze

Analyze a single skill file for quality issues.

```bash
python -m cli.main analyze FILE
```

**Example:**
```bash
python -m cli.main analyze ./skills/my-prompt.md
```

**Output:**
```
⚠ Too short (under 50 chars)
⚠ Vague summarization — no output format specified
```

Or if clean:
```
✔ Clean
```

---

## score

Show the 0–100 quality score for a single file.

```bash
python -m cli.main score FILE
```

Scores are color coded:
- **Green** — 80–100 (good)
- **Yellow** — 50–79 (needs improvement)
- **Red** — 0–49 (poor)

**Example:**
```bash
python -m cli.main score ./skills/my-prompt.md
# Score: 70/100
#   ⚠ Vague summarization — no output format specified
```

---

## duplicates

List all duplicate skill pairs above the similarity threshold.

```bash
python -m cli.main duplicates PATH [OPTIONS]
```

| Option | Default | Description |
|---|---|---|
| `--threshold` | `0.8` | Similarity threshold (0.0–1.0) |

**Example:**
```bash
python -m cli.main duplicates ./skills
python -m cli.main duplicates ./skills --threshold 0.6
```

---

## compare

Directly compare two skill files for similarity.

```bash
python -m cli.main compare FILE_A FILE_B
```

Shows:
- Cosine similarity score
- Word count of each file
- Common words (up to 10)
- Label: `Likely duplicate` / `Similar` / `Distinct`

**Example:**
```bash
python -m cli.main compare ./skills/a.md ./skills/b.md
```

---

## search

Find skill files containing a keyword.

```bash
python -m cli.main search PATH KEYWORD
```

**Example:**
```bash
python -m cli.main search ./skills summarize
python -m cli.main search ./skills "bullet points"
```

---

## fix

Auto-fix simple issues in skill files. Dry-run by default.

```bash
python -m cli.main fix PATH [OPTIONS]
```

| Option | Default | Description |
|---|---|---|
| `--apply` | off | Write fixes to disk (default is preview only). The original of each changed file is saved next to it as `<name>.md.bak` |

**What it fixes automatically:**
- Strips leading/trailing whitespace
- Adds a `# Title` if the file has no heading (uses filename)

**What it flags for manual review:**
- Duplicate files (never auto-deleted)

**Example:**
```bash
python -m cli.main fix ./skills           # preview only
python -m cli.main fix ./skills --apply   # write changes
```

---

## cleanup

Find and remove empty or broken skill files. Dry-run by default.

```bash
python -m cli.main cleanup PATH [OPTIONS]
```

| Option | Default | Description |
|---|---|---|
| `--apply` | off | Delete broken files after confirmation prompt |

**What counts as broken:**
- Empty file (0 bytes or whitespace only)
- Under 10 characters
- Single word

**Example:**
```bash
python -m cli.main cleanup ./skills           # preview only
python -m cli.main cleanup ./skills --apply   # delete with confirmation
```

---

## usage

Parse Claude Code conversation history to show which skills are invoked vs never used.

```bash
python -m cli.main usage PATH [OPTIONS]
```

| Option | Default | Description |
|---|---|---|
| `--history` | `~/.claude/projects/` | Path to Claude conversation history |

**Example:**
```bash
python -m cli.main usage ./skills
```

**Output:**
```
         Skill Usage
┌──────────┬─────────────┬───────────┬────────────┐
│ Skill    │ Invocations │ Last Used │ Status     │
├──────────┼─────────────┼───────────┼────────────┤
│ commit   │ 12          │ 2026-04-10│ active     │
│ review   │ 0           │ —         │ never used │
└──────────┴─────────────┴───────────┴────────────┘
Active: 1  Unused: 1
```

---

## export

Save a full audit report to a file.

```bash
python -m cli.main export PATH [OPTIONS]
```

| Option | Default | Description |
|---|---|---|
| `--format` | `json` | Output format: `json` or `md` |

**Output file:** `skillforge-report-YYYY-MM-DD.json` or `.md`

**Example:**
```bash
python -m cli.main export ./skills
python -m cli.main export ./skills --format md
```

---

## stats

Show summary statistics for the skills directory.

```bash
python -m cli.main stats PATH
```

Shows: total files, duplicates, average file length (chars), total word count.

---

## list

List all skill files with their full paths.

```bash
python -m cli.main list PATH
```

---

## watch

Watch the skills directory and re-run audit automatically on any `.md` file change.

```bash
python -m cli.main watch PATH
```

Stop with `Ctrl+C`.

**Example:**
```bash
python -m cli.main watch ./skills
# Watching: ./skills  (Ctrl+C to stop)
# Change detected: ./skills/my-prompt.md
# Total: 5 ...
```
