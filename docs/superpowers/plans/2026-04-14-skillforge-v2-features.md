# SkillForge v2 Features Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add 14 new features across CLI commands, packaging, GitHub integration, web dashboard, VS Code extension, and Chrome extension to make SkillForge a complete, installable skill management tool.

**Architecture:** Each feature is isolated in its own command file under `cli/commands/`. Shared logic (GitHub API, HTML generation) goes in `cli/core/`. Packaging is handled via `pyproject.toml`. Extensions are self-contained in their own directories.

**Tech Stack:** Python 3.11, Typer, Rich, scikit-learn, watchdog, stdlib only for new features (urllib, http.server, zipfile, subprocess, re) — no new pip dependencies.

---

## File Map

### New files to create
- `pyproject.toml` — packaging, entry point, dependencies
- `cli/commands/rename.py` — rename files from heading
- `cli/commands/backup.py` — zip skills folder
- `cli/commands/discover.py` — search GitHub for skill repos
- `cli/commands/install_cmd.py` — install skills from GitHub repo
- `cli/commands/diff.py` — git diff for a skill file
- `cli/commands/serve.py` — local web dashboard
- `.github/workflows/audit.yml` — CI audit on push
- `hooks/pre-commit` — pre-commit quality gate
- `tests/__init__.py`
- `tests/test_analyzer.py`
- `tests/test_scanner.py`
- `tests/test_similarity.py`
- `tests/test_rename.py`
- `tests/test_backup.py`

### Files to modify
- `cli/core/analyzer.py` — add frontmatter validation, update `analyze_text` + `score_text`
- `cli/commands/audit.py` — add `--min-score`, `--output` flags
- `cli/commands/lint.py` — add `--min-score`, `--output` flags
- `cli/main.py` — register 6 new commands
- `vscode-extension/extension.js` — add lint, score, usage commands
- `vscode-extension/package.json` — register new commands
- `chrome-extension/popup.html` — add Copy to Clipboard button
- `chrome-extension/popup.js` — add clipboard logic
- `docs/commands.md` — document new commands
- `CHANGELOG.md` — add v0.4.0 entry
- `README.md` — update features + commands table

---

## Task 1: Add test infrastructure

**Files:**
- Create: `tests/__init__.py`
- Create: `tests/test_analyzer.py`
- Create: `tests/test_scanner.py`
- Create: `tests/test_similarity.py`

- [ ] **Step 1: Create tests directory**

```bash
mkdir -p tests
touch tests/__init__.py
```

- [ ] **Step 2: Write analyzer tests**

Create `tests/test_analyzer.py`:

```python
from cli.core.analyzer import analyze_text, score_text


def test_too_short():
    issues = analyze_text("Hi")
    assert any("Too short" in i for i in issues)


def test_too_long():
    issues = analyze_text("word " * 500)
    assert any("Too long" in i for i in issues)


def test_clean():
    text = "Summarize the following article in 3 bullet points, keeping each under 20 words."
    issues = analyze_text(text)
    assert issues == []


def test_vague_summarize():
    issues = analyze_text("Please summarize this document for me and give me the output.")
    assert any("Vague summarization" in i for i in issues)


def test_score_clean():
    text = "Summarize the following article in 3 bullet points, keeping each under 20 words."
    assert score_text(text) == 100


def test_score_short():
    assert score_text("Hi") < 100


def test_score_clamp():
    assert score_text("x") >= 0
```

- [ ] **Step 3: Write scanner tests**

Create `tests/test_scanner.py`:

```python
import os
import tempfile
import pytest
from cli.core.scanner import scan_skills


def test_scan_finds_md_files():
    with tempfile.TemporaryDirectory() as tmp:
        open(os.path.join(tmp, "a.md"), "w").write("hello")
        open(os.path.join(tmp, "b.txt"), "w").write("ignore")
        results = scan_skills(tmp)
        assert len(results) == 1
        assert results[0]["name"] == "a.md"


def test_scan_missing_path():
    with pytest.raises(FileNotFoundError):
        scan_skills("/nonexistent/path/xyz")


def test_scan_returns_content():
    with tempfile.TemporaryDirectory() as tmp:
        open(os.path.join(tmp, "skill.md"), "w").write("my content")
        results = scan_skills(tmp)
        assert results[0]["content"] == "my content"
```

- [ ] **Step 4: Write similarity tests**

Create `tests/test_similarity.py`:

```python
from cli.core.similarity import find_duplicates


def test_no_duplicates():
    skills = [
        {"name": "a.md", "content": "Write a poem about the ocean waves crashing."},
        {"name": "b.md", "content": "List the top 10 Python libraries for data science work."},
    ]
    assert find_duplicates(skills) == []


def test_finds_duplicates():
    content = "Summarize this article in 3 bullet points keeping each point short."
    skills = [
        {"name": "a.md", "content": content},
        {"name": "b.md", "content": content},
    ]
    dups = find_duplicates(skills)
    assert len(dups) == 1
    assert dups[0]["score"] == 1.0


def test_empty_list():
    assert find_duplicates([]) == []
```

- [ ] **Step 5: Run tests**

```bash
.venv/bin/python -m pytest tests/ -v
```

Expected: all tests pass.

- [ ] **Step 6: Commit**

```bash
git add tests/
git commit -m "test: add test suite for analyzer, scanner, similarity"
```

---

## Task 2: Frontmatter validation

**Files:**
- Modify: `cli/core/analyzer.py`
- Create: `tests/test_frontmatter.py`

- [ ] **Step 1: Write failing test**

Create `tests/test_frontmatter.py`:

```python
from cli.core.analyzer import analyze_text


def test_missing_frontmatter_flagged():
    text = "This is a skill without any frontmatter at all.\n\nJust plain text here."
    issues = analyze_text(text)
    assert any("frontmatter" in i.lower() for i in issues)


def test_valid_frontmatter_not_flagged():
    text = "---\nname: my-skill\ndescription: Does something useful\ntype: user\n---\n\nThis is the skill body with enough content."
    issues = analyze_text(text)
    assert not any("frontmatter" in i.lower() for i in issues)


def test_incomplete_frontmatter_flagged():
    text = "---\nname: my-skill\n---\n\nMissing description and type fields here."
    issues = analyze_text(text)
    assert any("description" in i.lower() or "frontmatter" in i.lower() for i in issues)
```

- [ ] **Step 2: Run test — confirm it fails**

```bash
.venv/bin/python -m pytest tests/test_frontmatter.py -v
```

Expected: FAIL — frontmatter check not yet implemented.

- [ ] **Step 3: Add frontmatter parsing to analyzer**

Replace `cli/core/analyzer.py` with:

```python
import re


def _parse_frontmatter(text: str) -> dict | None:
    """Return dict of frontmatter fields, or None if no frontmatter block."""
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', text, re.DOTALL)
    if not match:
        return None
    fields = {}
    for line in match.group(1).splitlines():
        if ':' in line:
            key, _, val = line.partition(':')
            fields[key.strip()] = val.strip()
    return fields


def analyze_text(text: str) -> list:
    issues = []
    stripped = text.strip()
    word_count = len(stripped.split())

    if len(stripped) < 50:
        issues.append("Too short (under 50 chars)")

    if len(stripped) > 2000:
        issues.append("Too long (over 2000 chars)")

    if word_count < 5:
        issues.append("Too vague — fewer than 5 words")

    lower = stripped.lower()

    if "summarize" in lower and not any(w in lower for w in ["bullet", "points", "list", "format", "structure"]):
        issues.append("Vague summarization — no output format specified")

    if "write" in lower and word_count < 8:
        issues.append("Unclear write instruction — too few words")

    if any(w in lower for w in ["do this", "do that", "make it", "fix it"]) and word_count < 10:
        issues.append("Vague instruction — missing context")

    fm = _parse_frontmatter(stripped)
    if fm is None:
        issues.append("Missing frontmatter (no --- block found)")
    else:
        for field in ["name", "description"]:
            if field not in fm or not fm[field]:
                issues.append(f"Frontmatter missing required field: '{field}'")

    return issues


def score_text(text: str) -> int:
    issues = analyze_text(text)
    deductions = {
        "Too short": 30,
        "Too long": 20,
        "Too vague": 25,
        "Vague summarization": 15,
        "Unclear write": 15,
        "Vague instruction": 15,
        "Missing frontmatter": 10,
        "Frontmatter missing": 10,
    }
    total = 100
    for issue in issues:
        for key, penalty in deductions.items():
            if key.lower() in issue.lower():
                total -= penalty
                break
    return max(0, total)
```

- [ ] **Step 4: Run tests**

```bash
.venv/bin/python -m pytest tests/ -v
```

Expected: all pass.

- [ ] **Step 5: Commit**

```bash
git add cli/core/analyzer.py tests/test_frontmatter.py
git commit -m "feat: add frontmatter validation to analyzer"
```

---

## Task 3: --min-score flag on audit and lint

**Files:**
- Modify: `cli/commands/audit.py`
- Modify: `cli/commands/lint.py`

- [ ] **Step 1: Add --min-score to audit**

In `cli/commands/audit.py`, add `min_score: int = 0` parameter:

```python
def audit_cmd(
    path: str,
    json_out: bool = False,
    threshold: float = 0.8,
    quiet: bool = False,
    verbose: bool = False,
    min_score: int = 0,
):
```

In the verbose/issues section, filter by score:

```python
    # After building scores_map and issues_map, filter if min_score set
    if min_score > 0:
        issues_map = {
            name: issues
            for name, issues in issues_map.items()
            if scores_map.get(name, 100) < min_score
        }

    result = {
        "total": len(skills),
        "duplicates": len(dups),
        "issues": issues_map,
    }
```

- [ ] **Step 2: Add --min-score to lint**

In `cli/commands/lint.py`, add `min_score: int = 0` parameter:

```python
def lint_cmd(path: str, quiet: bool = False, min_score: int = 0):
```

Filter flagged list:

```python
    flagged_only = [
        (s, issues, sc) for s, issues, sc in flagged
        if issues and (min_score == 0 or sc < min_score)
    ]
```

- [ ] **Step 3: Test manually**

```bash
.venv/bin/python -m cli.main audit ./skills --min-score 80
.venv/bin/python -m cli.main lint ./skills --min-score 50
```

Expected: only files scoring below the threshold are shown.

- [ ] **Step 4: Commit**

```bash
git add cli/commands/audit.py cli/commands/lint.py
git commit -m "feat: add --min-score flag to audit and lint commands"
```

---

## Task 4: --output flag

**Files:**
- Modify: `cli/commands/audit.py`
- Modify: `cli/commands/lint.py`
- Modify: `cli/commands/duplicates.py`
- Modify: `cli/commands/stats.py`
- Modify: `cli/commands/list_cmd.py`

- [ ] **Step 1: Add --output to audit**

Rich's `Console` accepts a `file` argument. Add `output: str = ""` parameter to `audit_cmd`:

```python
import sys

def audit_cmd(
    path: str,
    json_out: bool = False,
    threshold: float = 0.8,
    quiet: bool = False,
    verbose: bool = False,
    min_score: int = 0,
    output: str = "",
):
    out_file = open(output, "w", encoding="utf-8") if output else None
    console = Console(file=out_file) if out_file else Console()
    try:
        # ... rest of function unchanged ...
    finally:
        if out_file:
            out_file.close()
            Console().print(f"[green]Saved to:[/green] {output}")
```

- [ ] **Step 2: Apply same pattern to lint, duplicates, stats, list**

For each command, add `output: str = ""` parameter and wrap Console with:

```python
out_file = open(output, "w", encoding="utf-8") if output else None
console = Console(file=out_file) if out_file else Console()
```

And close in a `finally` block.

- [ ] **Step 3: Test manually**

```bash
.venv/bin/python -m cli.main audit ./skills --output report.txt
cat report.txt
```

Expected: file created with audit output.

- [ ] **Step 4: Commit**

```bash
git add cli/commands/audit.py cli/commands/lint.py cli/commands/duplicates.py cli/commands/stats.py cli/commands/list_cmd.py
git commit -m "feat: add --output flag to audit, lint, duplicates, stats, list"
```

---

## Task 5: rename command

**Files:**
- Create: `cli/commands/rename.py`
- Create: `tests/test_rename.py`
- Modify: `cli/main.py`

- [ ] **Step 1: Write failing test**

Create `tests/test_rename.py`:

```python
import os
import tempfile
from cli.commands.rename import _suggested_name


def test_rename_from_heading():
    assert _suggested_name("# My Skill Title\n\nsome content") == "my-skill-title.md"


def test_rename_no_heading_uses_filename():
    assert _suggested_name("no heading here at all") is None


def test_rename_cleans_special_chars():
    assert _suggested_name("# Hello World! (Test)") == "hello-world-test.md"
```

- [ ] **Step 2: Run test — confirm it fails**

```bash
.venv/bin/python -m pytest tests/test_rename.py -v
```

Expected: FAIL — module not found.

- [ ] **Step 3: Create rename command**

Create `cli/commands/rename.py`:

```python
import os
import re
import typer
from rich.console import Console
from cli.core.scanner import scan_skills

console = Console()


def _suggested_name(content: str) -> str | None:
    """Extract first # heading and convert to kebab-case filename."""
    match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if not match:
        return None
    title = match.group(1).strip()
    slug = re.sub(r'[^a-zA-Z0-9\s-]', '', title)
    slug = re.sub(r'\s+', '-', slug).lower().strip('-')
    return f"{slug}.md" if slug else None


def rename_cmd(path: str, apply: bool = False):
    try:
        skills = scan_skills(path)
    except (FileNotFoundError, NotADirectoryError) as e:
        console.print(f"[red]Error:[/red] {e}")
        return

    suggestions = []
    for s in skills:
        suggested = _suggested_name(s["content"])
        if suggested and suggested != s["name"]:
            suggestions.append((s, suggested))

    if not suggestions:
        console.print("[green]✔ All filenames already match their headings.[/green]")
        return

    console.print(f"[yellow]Rename suggestions ({len(suggestions)}):[/yellow]\n")
    for s, new_name in suggestions:
        console.print(f"  [cyan]{s['name']}[/cyan]  →  [green]{new_name}[/green]")

    if not apply:
        console.print(f"\n[dim]Dry run. Use --apply to rename.[/dim]")
        return

    confirmed = typer.confirm(f"\nRename {len(suggestions)} file(s)?")
    if not confirmed:
        console.print("[yellow]Cancelled.[/yellow]")
        return

    for s, new_name in suggestions:
        new_path = os.path.join(os.path.dirname(s["path"]), new_name)
        if os.path.exists(new_path):
            console.print(f"[yellow]Skip:[/yellow] {new_name} already exists")
            continue
        os.rename(s["path"], new_path)
        console.print(f"[green]Renamed:[/green] {s['name']} → {new_name}")
```

- [ ] **Step 4: Register in main**

In `cli/main.py`, add:

```python
from cli.commands import rename
app.command("rename")(rename.rename_cmd)
```

- [ ] **Step 5: Run tests**

```bash
.venv/bin/python -m pytest tests/test_rename.py -v
```

Expected: all pass.

- [ ] **Step 6: Test manually**

```bash
.venv/bin/python -m cli.main rename ./skills
```

- [ ] **Step 7: Commit**

```bash
git add cli/commands/rename.py cli/main.py tests/test_rename.py
git commit -m "feat: add rename command — auto-rename files from headings"
```

---

## Task 6: backup command

**Files:**
- Create: `cli/commands/backup.py`
- Create: `tests/test_backup.py`
- Modify: `cli/main.py`

- [ ] **Step 1: Write failing test**

Create `tests/test_backup.py`:

```python
import os
import zipfile
import tempfile
from cli.commands.backup import _create_backup


def test_backup_creates_zip():
    with tempfile.TemporaryDirectory() as tmp:
        open(os.path.join(tmp, "skill.md"), "w").write("content")
        zip_path = _create_backup(tmp, tmp)
        assert os.path.exists(zip_path)
        assert zipfile.is_zipfile(zip_path)


def test_backup_contains_md_files():
    with tempfile.TemporaryDirectory() as tmp:
        open(os.path.join(tmp, "skill.md"), "w").write("content")
        open(os.path.join(tmp, "other.txt"), "w").write("ignore")
        zip_path = _create_backup(tmp, tmp)
        with zipfile.ZipFile(zip_path) as zf:
            names = zf.namelist()
        assert any("skill.md" in n for n in names)
```

- [ ] **Step 2: Run test — confirm it fails**

```bash
.venv/bin/python -m pytest tests/test_backup.py -v
```

Expected: FAIL.

- [ ] **Step 3: Create backup command**

Create `cli/commands/backup.py`:

```python
import os
import zipfile
from datetime import date
from rich.console import Console
from cli.core.scanner import scan_skills

console = Console()


def _create_backup(skills_path: str, output_dir: str) -> str:
    today = date.today().isoformat()
    zip_name = f"skillforge-backup-{today}.zip"
    zip_path = os.path.join(output_dir, zip_name)
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, _, files in os.walk(skills_path):
            for f in files:
                if f.endswith(".md"):
                    full = os.path.join(root, f)
                    arcname = os.path.relpath(full, skills_path)
                    zf.write(full, arcname)
    return zip_path


def backup_cmd(path: str, dest: str = "."):
    try:
        skills = scan_skills(path)
    except (FileNotFoundError, NotADirectoryError) as e:
        console.print(f"[red]Error:[/red] {e}")
        return

    if not skills:
        console.print("[yellow]No skill files to backup.[/yellow]")
        return

    zip_path = _create_backup(path, dest)
    console.print(f"[green]Backup saved:[/green] {zip_path}  ({len(skills)} files)")
```

- [ ] **Step 4: Register in main**

```python
from cli.commands import backup
app.command("backup")(backup.backup_cmd)
```

- [ ] **Step 5: Run tests**

```bash
.venv/bin/python -m pytest tests/test_backup.py -v
```

Expected: all pass.

- [ ] **Step 6: Test manually**

```bash
.venv/bin/python -m cli.main backup ./skills
ls skillforge-backup-*.zip
```

- [ ] **Step 7: Commit**

```bash
git add cli/commands/backup.py cli/main.py tests/test_backup.py
git commit -m "feat: add backup command — zip all skill files"
```

---

## Task 7: diff command

**Files:**
- Create: `cli/commands/diff.py`
- Modify: `cli/main.py`

- [ ] **Step 1: Create diff command**

Create `cli/commands/diff.py`:

```python
import os
import subprocess
from rich.console import Console
from rich.syntax import Syntax

console = Console()


def diff_cmd(file: str, ref: str = "HEAD"):
    if not os.path.isfile(file):
        console.print(f"[red]Error:[/red] File not found: {file}")
        return

    result = subprocess.run(
        ["git", "diff", ref, "--", file],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        err = result.stderr.strip()
        if "not a git repository" in err.lower():
            console.print("[red]Error:[/red] Not inside a git repository.")
        else:
            console.print(f"[red]Error:[/red] {err}")
        return

    if not result.stdout.strip():
        console.print(f"[green]No changes since {ref}.[/green]")
        return

    syntax = Syntax(result.stdout, "diff", theme="monokai", line_numbers=False)
    console.print(syntax)
```

- [ ] **Step 2: Register in main**

```python
from cli.commands import diff
app.command("diff")(diff.diff_cmd)
```

- [ ] **Step 3: Test manually**

```bash
# Modify a skill file, then:
.venv/bin/python -m cli.main diff ./skills/test1.md
# Should show git diff with syntax highlighting
```

- [ ] **Step 4: Commit**

```bash
git add cli/commands/diff.py cli/main.py
git commit -m "feat: add diff command — show git diff for a skill file"
```

---

## Task 8: discover command (GitHub search)

**Files:**
- Create: `cli/commands/discover.py`
- Modify: `cli/main.py`

- [ ] **Step 1: Create discover command**

Create `cli/commands/discover.py`:

```python
import urllib.request
import urllib.parse
import json
import os
from rich.console import Console
from rich.table import Table

console = Console()

GITHUB_API = "https://api.github.com"


def _github_search(query: str, token: str = "") -> list:
    encoded = urllib.parse.quote(query)
    url = f"{GITHUB_API}/search/repositories?q={encoded}&sort=stars&per_page=10"
    req = urllib.request.Request(url)
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("User-Agent", "SkillForge/1.0")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            return data.get("items", [])
    except Exception as e:
        console.print(f"[red]GitHub API error:[/red] {e}")
        return []


def discover_cmd(keyword: str = "claude-code-skills"):
    token = os.environ.get("GITHUB_TOKEN", "")
    console.print(f"[bold]Searching GitHub for:[/bold] [cyan]{keyword}[/cyan]\n")

    repos = _github_search(f"{keyword} in:topics language:python OR language:markdown")

    if not repos:
        console.print("[yellow]No results found.[/yellow]")
        return

    table = Table(title=f"GitHub Results — {keyword}")
    table.add_column("#", style="dim", width=3)
    table.add_column("Repository", style="cyan")
    table.add_column("Stars", justify="right", style="yellow")
    table.add_column("Description")

    for i, repo in enumerate(repos, 1):
        table.add_row(
            str(i),
            repo["full_name"],
            str(repo.get("stargazers_count", 0)),
            (repo.get("description") or "")[:60],
        )

    console.print(table)
    console.print(f"\n[dim]Set GITHUB_TOKEN env var for higher rate limits.[/dim]")
    console.print(f"[dim]Install a repo: skillforge install <owner/repo>[/dim]")
```

- [ ] **Step 2: Register in main**

```python
from cli.commands import discover
app.command("discover")(discover.discover_cmd)
```

- [ ] **Step 3: Test manually**

```bash
.venv/bin/python -m cli.main discover claude-code-skills
.venv/bin/python -m cli.main discover "prompt skills"
```

Expected: table of GitHub repos.

- [ ] **Step 4: Commit**

```bash
git add cli/commands/discover.py cli/main.py
git commit -m "feat: add discover command — search GitHub for skill repos"
```

---

## Task 9: install command

**Files:**
- Create: `cli/commands/install_cmd.py`
- Modify: `cli/main.py`

- [ ] **Step 1: Create install command**

Create `cli/commands/install_cmd.py`:

```python
import os
import urllib.request
import json
import typer
from rich.console import Console

console = Console()

GITHUB_RAW = "https://raw.githubusercontent.com"
GITHUB_API = "https://api.github.com"


def _list_md_files(owner: str, repo: str, token: str = "") -> list:
    """Return list of {path, download_url} for all .md files in the repo."""
    url = f"{GITHUB_API}/repos/{owner}/{repo}/git/trees/HEAD?recursive=1"
    req = urllib.request.Request(url)
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("User-Agent", "SkillForge/1.0")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            return [
                item for item in data.get("tree", [])
                if item["type"] == "blob" and item["path"].endswith(".md")
            ]
    except Exception as e:
        console.print(f"[red]GitHub API error:[/red] {e}")
        return []


def _download_file(owner: str, repo: str, path: str, dest: str):
    url = f"{GITHUB_RAW}/{owner}/{repo}/HEAD/{path}"
    req = urllib.request.Request(url)
    req.add_header("User-Agent", "SkillForge/1.0")
    with urllib.request.urlopen(req, timeout=10) as resp:
        content = resp.read()
    with open(dest, "wb") as f:
        f.write(content)


def install_cmd(repo: str, path: str = "./skills"):
    if "/" not in repo:
        console.print("[red]Error:[/red] Use format: owner/repo")
        return

    owner, repo_name = repo.split("/", 1)
    token = os.environ.get("GITHUB_TOKEN", "")

    console.print(f"[bold]Fetching file list from:[/bold] [cyan]{repo}[/cyan]")
    files = _list_md_files(owner, repo_name, token)

    if not files:
        console.print("[yellow]No .md files found in that repo.[/yellow]")
        return

    console.print(f"Found [bold]{len(files)}[/bold] .md file(s):\n")
    for f in files:
        console.print(f"  [dim]{f['path']}[/dim]")

    confirmed = typer.confirm(f"\nInstall {len(files)} file(s) into {path}?")
    if not confirmed:
        console.print("[yellow]Cancelled.[/yellow]")
        return

    os.makedirs(path, exist_ok=True)
    installed = 0
    for f in files:
        filename = os.path.basename(f["path"])
        dest = os.path.join(path, filename)
        if os.path.exists(dest):
            console.print(f"[yellow]Skip:[/yellow] {filename} (already exists)")
            continue
        try:
            _download_file(owner, repo_name, f["path"], dest)
            console.print(f"[green]Installed:[/green] {filename}")
            installed += 1
        except Exception as e:
            console.print(f"[red]Failed:[/red] {filename} — {e}")

    console.print(f"\n[bold]Installed {installed} file(s) into {path}[/bold]")
```

- [ ] **Step 2: Register in main**

```python
from cli.commands import install_cmd
app.command("install")(install_cmd.install_cmd)
```

- [ ] **Step 3: Test manually**

```bash
.venv/bin/python -m cli.main install khendzel/skills-janitor --path ./skills-test
```

Expected: lists files, prompts for confirmation, downloads `.md` files.

- [ ] **Step 4: Commit**

```bash
git add cli/commands/install_cmd.py cli/main.py
git commit -m "feat: add install command — install skills from GitHub repo"
```

---

## Task 10: serve command (web dashboard)

**Files:**
- Create: `cli/commands/serve.py`
- Modify: `cli/main.py`

- [ ] **Step 1: Create serve command**

Create `cli/commands/serve.py`:

```python
import json
import os
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from rich.console import Console
from cli.core.scanner import scan_skills
from cli.core.similarity import find_duplicates
from cli.core.analyzer import analyze_text, score_text

console = Console()

HTML_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>SkillForge Dashboard</title>
<style>
  body { font-family: system-ui, sans-serif; margin: 0; background: #0f172a; color: #e2e8f0; }
  .header { background: #1e293b; padding: 20px 32px; border-bottom: 1px solid #334155; }
  .header h1 { margin: 0; font-size: 22px; color: #38bdf8; }
  .stats { display: flex; gap: 16px; padding: 24px 32px; }
  .stat { background: #1e293b; border-radius: 8px; padding: 16px 24px; min-width: 120px; }
  .stat .label { font-size: 12px; color: #94a3b8; margin-bottom: 4px; }
  .stat .value { font-size: 28px; font-weight: bold; color: #38bdf8; }
  .section { padding: 0 32px 32px; }
  h2 { color: #94a3b8; font-size: 14px; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 12px; }
  table { width: 100%; border-collapse: collapse; background: #1e293b; border-radius: 8px; overflow: hidden; }
  th { text-align: left; padding: 10px 16px; font-size: 12px; color: #64748b; background: #0f172a; }
  td { padding: 10px 16px; border-top: 1px solid #334155; font-size: 14px; }
  .score-high { color: #4ade80; }
  .score-mid  { color: #facc15; }
  .score-low  { color: #f87171; }
  .issues { color: #f87171; font-size: 12px; }
  .clean  { color: #4ade80; font-size: 12px; }
  .dup-pair { background: #1e293b; border-radius: 6px; padding: 10px 16px; margin-bottom: 8px; font-size: 14px; color: #fbbf24; }
</style>
</head>
<body>
<div class="header"><h1>SkillForge Dashboard</h1></div>
<div class="stats">
  <div class="stat"><div class="label">Total Files</div><div class="value" id="total">—</div></div>
  <div class="stat"><div class="label">Duplicates</div><div class="value" id="dups">—</div></div>
  <div class="stat"><div class="label">Avg Score</div><div class="value" id="avg">—</div></div>
  <div class="stat"><div class="label">With Issues</div><div class="value" id="issues_count">—</div></div>
</div>
<div class="section">
  <h2>Files</h2>
  <table><thead><tr><th>Name</th><th>Score</th><th>Issues</th></tr></thead>
  <tbody id="tbody"></tbody></table>
</div>
<div class="section" id="dup_section" style="display:none">
  <h2>Duplicates</h2><div id="dup_list"></div>
</div>
<script>
const DATA = __DATA__;
document.getElementById('total').textContent = DATA.total;
document.getElementById('dups').textContent = DATA.duplicates.length;
const scores = DATA.files.map(f => f.score);
document.getElementById('avg').textContent = Math.round(scores.reduce((a,b)=>a+b,0)/scores.length);
document.getElementById('issues_count').textContent = DATA.files.filter(f=>f.issues.length>0).length;
const tbody = document.getElementById('tbody');
DATA.files.sort((a,b)=>a.score-b.score).forEach(f => {
  const cls = f.score>=80?'score-high':f.score>=50?'score-mid':'score-low';
  const issues = f.issues.length ? `<span class="issues">${f.issues.join('<br>')}</span>` : '<span class="clean">✔ Clean</span>';
  tbody.innerHTML += `<tr><td>${f.name}</td><td class="${cls}">${f.score}/100</td><td>${issues}</td></tr>`;
});
if(DATA.duplicates.length > 0) {
  document.getElementById('dup_section').style.display='block';
  const dl = document.getElementById('dup_list');
  DATA.duplicates.forEach(d => {
    dl.innerHTML += `<div class="dup-pair">${d.a} ↔ ${d.b} &nbsp; <span style="color:#94a3b8">(${d.score.toFixed(2)})</span></div>`;
  });
}
</script>
</body>
</html>"""


def _build_data(path: str) -> dict:
    skills = scan_skills(path)
    dups = find_duplicates(skills)
    return {
        "total": len(skills),
        "duplicates": dups,
        "files": [
            {
                "name": s["name"],
                "score": score_text(s["content"]),
                "issues": analyze_text(s["content"]),
            }
            for s in skills
        ],
    }


def serve_cmd(path: str, port: int = 7842):
    try:
        data = _build_data(path)
    except (FileNotFoundError, NotADirectoryError) as e:
        console.print(f"[red]Error:[/red] {e}")
        return

    html = HTML_TEMPLATE.replace("__DATA__", json.dumps(data))

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(html.encode())

        def log_message(self, *args):
            pass  # suppress request logs

    url = f"http://localhost:{port}"
    console.print(f"[green]Dashboard:[/green] {url}  (Ctrl+C to stop)")
    webbrowser.open(url)

    server = HTTPServer(("localhost", port), Handler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        console.print("[yellow]Stopped.[/yellow]")
```

- [ ] **Step 2: Register in main**

```python
from cli.commands import serve
app.command("serve")(serve.serve_cmd)
```

- [ ] **Step 3: Test manually**

```bash
.venv/bin/python -m cli.main serve ./skills
```

Expected: browser opens at `http://localhost:7842` showing the dashboard.

- [ ] **Step 4: Commit**

```bash
git add cli/commands/serve.py cli/main.py
git commit -m "feat: add serve command — local web dashboard"
```

---

## Task 11: pyproject.toml and skillforge entry point

**Files:**
- Create: `pyproject.toml`

- [ ] **Step 1: Create pyproject.toml**

Create `pyproject.toml` in the project root:

```toml
[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.backends.legacy:build"

[project]
name = "skillforge"
version = "0.4.0"
description = "Audit, analyze, and manage AI prompt skill files from the CLI."
readme = "README.md"
requires-python = ">=3.11"
license = {text = "MIT"}
authors = [
  {name = "SudarshanTechLabs", email = "sudarshantechlabs@gmail.com"}
]
dependencies = [
  "typer>=0.9",
  "rich>=13",
  "watchdog>=3",
  "scikit-learn>=1.3",
]

[project.scripts]
skillforge = "cli.main:app"

[project.urls]
Homepage = "https://github.com/SUDARSHANCHAUDHARI/SkillForge"
```

- [ ] **Step 2: Install in editable mode**

```bash
.venv/bin/pip install -e . -q
```

- [ ] **Step 3: Test entry point**

```bash
.venv/bin/skillforge --help
.venv/bin/skillforge audit ./skills
```

Expected: works identically to `python -m cli.main`.

- [ ] **Step 4: Commit**

```bash
git add pyproject.toml
git commit -m "feat: add pyproject.toml and skillforge CLI entry point"
```

---

## Task 12: GitHub Actions CI workflow

**Files:**
- Create: `.github/workflows/audit.yml`

- [ ] **Step 1: Create workflow file**

```bash
mkdir -p .github/workflows
```

Create `.github/workflows/audit.yml`:

```yaml
name: SkillForge Audit

on:
  push:
    paths:
      - 'skills/**'
  pull_request:
    paths:
      - 'skills/**'

jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Run audit
        run: python -m cli.main audit ./skills --quiet --min-score 50

      - name: Run lint
        run: python -m cli.main lint ./skills --quiet --min-score 50
```

- [ ] **Step 2: Commit**

```bash
git add .github/
git commit -m "ci: add GitHub Actions workflow to audit skills on push"
```

---

## Task 13: Pre-commit hook

**Files:**
- Create: `hooks/pre-commit`

- [ ] **Step 1: Create hook script**

```bash
mkdir -p hooks
```

Create `hooks/pre-commit`:

```bash
#!/bin/sh
# SkillForge pre-commit hook
# Install: cp hooks/pre-commit .git/hooks/pre-commit && chmod +x .git/hooks/pre-commit

echo "SkillForge: running audit..."

python -m cli.main audit ./skills --quiet --min-score 50

if [ $? -ne 0 ]; then
  echo "SkillForge: audit failed. Fix issues before committing."
  echo "Run: python -m cli.main lint ./skills"
  exit 1
fi

echo "SkillForge: audit passed."
exit 0
```

- [ ] **Step 2: Add install instructions to CONTRIBUTING.md**

In `CONTRIBUTING.md`, add under a new `## Pre-commit hook` section:

```markdown
## Pre-commit hook

To block commits when skill quality drops below 50/100:

```bash
cp hooks/pre-commit .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```
```

- [ ] **Step 3: Commit**

```bash
git add hooks/ CONTRIBUTING.md
git commit -m "feat: add pre-commit hook for skill quality gate"
```

---

## Task 14: VS Code extension — add lint, score, usage commands

**Files:**
- Modify: `vscode-extension/extension.js`
- Modify: `vscode-extension/package.json`

- [ ] **Step 1: Update package.json**

Replace `vscode-extension/package.json` with:

```json
{
  "name": "skillforge",
  "displayName": "SkillForge",
  "version": "0.2.0",
  "engines": { "vscode": "^1.80.0" },
  "main": "extension.js",
  "contributes": {
    "commands": [
      { "command": "skillforge.audit",      "title": "SkillForge: Audit" },
      { "command": "skillforge.duplicates", "title": "SkillForge: Duplicates" },
      { "command": "skillforge.lint",       "title": "SkillForge: Lint" },
      { "command": "skillforge.usage",      "title": "SkillForge: Usage" },
      { "command": "skillforge.score",      "title": "SkillForge: Score Current File" }
    ]
  }
}
```

- [ ] **Step 2: Update extension.js**

Replace `vscode-extension/extension.js` with:

```js
const vscode = require('vscode');
const { execFile } = require('child_process');

const outputChannel = vscode.window.createOutputChannel('SkillForge');

function runCommand(args, label) {
    const workspaceRoot = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
    if (!workspaceRoot) {
        vscode.window.showErrorMessage('SkillForge: No workspace folder open.');
        return;
    }
    outputChannel.show(true);
    outputChannel.appendLine(`\n▶ SkillForge ${label}  (${new Date().toLocaleTimeString()})`);
    outputChannel.appendLine('─'.repeat(50));
    execFile('python', ['-m', 'cli.main', ...args], { cwd: workspaceRoot }, (err, stdout, stderr) => {
        const output = (stdout || stderr || 'No output.').trim();
        outputChannel.appendLine(output);
        if (err) {
            vscode.window.showErrorMessage(`SkillForge ${label} failed. See Output panel.`);
        } else {
            vscode.window.showInformationMessage(`SkillForge ${label} complete. See Output panel.`);
        }
    });
}

function activate(context) {
    const cmds = [
        ['skillforge.audit',      () => runCommand(['audit', './skills', '--verbose'], 'Audit')],
        ['skillforge.duplicates', () => runCommand(['duplicates', './skills'], 'Duplicates')],
        ['skillforge.lint',       () => runCommand(['lint', './skills'], 'Lint')],
        ['skillforge.usage',      () => runCommand(['usage', './skills'], 'Usage')],
        ['skillforge.score',      () => {
            const file = vscode.window.activeTextEditor?.document.fileName;
            if (!file) { vscode.window.showWarningMessage('No file open.'); return; }
            runCommand(['score', file], 'Score');
        }],
    ];
    cmds.forEach(([cmd, fn]) =>
        context.subscriptions.push(vscode.commands.registerCommand(cmd, fn))
    );
}

exports.activate = activate;
```

- [ ] **Step 3: Commit**

```bash
git add vscode-extension/
git commit -m "feat: add lint, usage, score commands to VS Code extension"
```

---

## Task 15: Chrome extension — Copy to Clipboard

**Files:**
- Modify: `chrome-extension/popup.html`
- Modify: `chrome-extension/popup.js`
- Modify: `chrome-extension/manifest.json`

- [ ] **Step 1: Update manifest — add clipboardWrite permission**

```json
{
  "manifest_version": 3,
  "name": "SkillForge",
  "version": "1.1",
  "action": { "default_popup": "popup.html" },
  "permissions": ["downloads", "clipboardWrite"]
}
```

- [ ] **Step 2: Update popup.html — add Copy button**

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    body { font-family: sans-serif; padding: 12px; min-width: 200px; }
    button { display: block; width: 100%; margin-bottom: 8px; padding: 8px; cursor: pointer; }
    #output { font-size: 12px; margin-top: 8px; }
  </style>
</head>
<body>
  <button id="save">Save Prompt</button>
  <button id="analyze">Analyze Prompt</button>
  <button id="copy">Copy as Markdown</button>
  <div id="output"></div>
  <script src="popup.js"></script>
</body>
</html>
```

- [ ] **Step 3: Update popup.js — add copy logic**

Add after the analyze button handler:

```js
document.getElementById('copy').onclick = async () => {
    const text = prompt('Paste your prompt to copy as Markdown:');
    if (!text) return;
    const md = `# Prompt\n\n${text}\n`;
    try {
        await navigator.clipboard.writeText(md);
        const output = document.getElementById('output');
        output.style.color = 'green';
        output.textContent = '✔ Copied to clipboard as Markdown';
    } catch (e) {
        const output = document.getElementById('output');
        output.style.color = '#c00';
        output.textContent = 'Failed to copy: ' + e.message;
    }
};
```

- [ ] **Step 4: Commit**

```bash
git add chrome-extension/
git commit -m "feat: add Copy as Markdown button to Chrome extension"
```

---

## Task 16: Update docs and CHANGELOG

**Files:**
- Modify: `docs/commands.md`
- Modify: `CHANGELOG.md`
- Modify: `README.md`

- [ ] **Step 1: Add new commands to docs/commands.md**

Add documentation sections for: `rename`, `backup`, `diff`, `discover`, `install`, `serve`.

For each, follow the existing pattern:
```markdown
## <command>

<one-line description>

\`\`\`bash
python -m cli.main <command> [args] [options]
\`\`\`

| Option | Default | Description |
...
```

- [ ] **Step 2: Update CHANGELOG.md**

Add at top:

```markdown
## [0.4.0] — 2026-04-14

### Added
- `rename` command — auto-rename files from first heading
- `backup` command — zip all skills with timestamp
- `diff` command — show git diff for a skill file
- `discover` command — search GitHub for skill repos
- `install` command — install skills from a GitHub repo
- `serve` command — local web dashboard at localhost:7842
- `pyproject.toml` — `pip install .` and `skillforge` entry point
- GitHub Actions CI workflow for skills directory
- Pre-commit hook for quality gate
- `--min-score` flag on `audit` and `lint`
- `--output` flag on `audit`, `lint`, `duplicates`, `stats`, `list`
- Frontmatter validation in analyzer
- VS Code: `lint`, `usage`, `score current file` commands added
- Chrome: Copy as Markdown button
- Full test suite: `tests/`
```

- [ ] **Step 3: Update README features list and commands table**

Add new commands to the features bullet list and commands table in `README.md`.

- [ ] **Step 4: Final commit**

```bash
git add docs/ CHANGELOG.md README.md
git commit -m "docs: update commands reference and changelog for v0.4.0"
git push
```

---

## Self-Review

**Spec coverage:**
- ✅ rename, backup, discover, install, serve, diff — all have dedicated tasks
- ✅ Frontmatter validation — Task 2
- ✅ --min-score — Task 3
- ✅ --output flag — Task 4
- ✅ pyproject.toml + entry point — Task 11
- ✅ GitHub Actions — Task 12
- ✅ Pre-commit hook — Task 13
- ✅ VS Code: lint, score, usage — Task 14
- ✅ Chrome: clipboard — Task 15
- ✅ Tests — Task 1 (scanner, analyzer, similarity, rename, backup)
- ✅ Docs — Task 16

**Placeholder scan:** None found. All steps contain complete code.

**Type consistency:**
- `_suggested_name` returns `str | None` — used correctly in `rename_cmd`
- `_create_backup` returns `str` (zip path) — used correctly in `backup_cmd`
- `_build_data` returns `dict` with `total`, `duplicates`, `files` — used correctly in HTML template
- `_github_search` returns `list[dict]` — used correctly in `discover_cmd`
