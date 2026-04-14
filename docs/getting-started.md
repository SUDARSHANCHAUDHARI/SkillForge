# Getting Started with SkillForge

This guide walks you through installing SkillForge and running your first audit in under 5 minutes.

---

## Requirements

- Python 3.11 or higher
- pip
- Git

Check your Python version:

```bash
python3 --version
```

---

## Step 1 — Clone the repo

```bash
git clone https://github.com/SUDARSHANCHAUDHARI/SkillForge.git
cd SkillForge
```

---

## Step 2 — Create a virtual environment

```bash
python3.11 -m venv .venv
```

Activate it:

```bash
# macOS / Linux
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

You should see `(.venv)` in your terminal prompt.

---

## Step 3 — Install dependencies

```bash
pip install -r requirements.txt
```

This installs: `typer`, `rich`, `watchdog`, `scikit-learn`.

---

## Step 4 — Initialise your skills directory

```bash
python -m cli.main init ./skills
```

This creates:
- `skills/` — your skill files go here
- `skills/example-skill.md` — a template to start from
- `.skillforgerc` — your local config file

---

## Step 5 — Run your first audit

```bash
python -m cli.main audit ./skills
```

Example output:

```
Total: 1
Duplicates: 0
Files with issues: 1

  ⚠ example-skill.md: Too short (under 50 chars)
```

---

## Step 6 — Try other commands

```bash
# See all your skill files
python -m cli.main list ./skills

# Quality score for a single file
python -m cli.main score ./skills/example-skill.md

# Bulk quality table
python -m cli.main lint ./skills

# Check which skills you actually use
python -m cli.main usage ./skills
```

---

## Using the entry point shorthand

Instead of `python -m cli.main`, you can use:

```bash
python skillforge.py audit ./skills
```

---

## Next steps

- [Full command reference](commands.md)
- [Config file reference](config.md)
- [VS Code + Chrome extension setup](extensions.md)
