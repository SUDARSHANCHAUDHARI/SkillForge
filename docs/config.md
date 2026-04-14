# Config File Reference

SkillForge supports a `.skillforgerc` file in your project root for setting defaults so you don't have to pass flags on every command.

---

## Creating the config file

Run `init` to auto-generate it:

```bash
python -m cli.main init ./skills
```

Or create it manually in your project root:

```bash
touch .skillforgerc
```

---

## Format

The config file is JSON.

```json
{
  "path": "./skills",
  "threshold": 0.8,
  "ignore": []
}
```

---

## Fields

### `path`

**Type:** string
**Default:** `"./skills"`

The default directory to scan when no path is passed to a command.

```json
{
  "path": "./my-prompts"
}
```

### `threshold`

**Type:** float (0.0 – 1.0)
**Default:** `0.8`

The cosine similarity threshold for duplicate detection. Files with a similarity score at or above this value are flagged as duplicates.

- `1.0` — exact duplicates only
- `0.8` — highly similar (recommended)
- `0.5` — loosely similar

```json
{
  "threshold": 0.75
}
```

### `ignore`

**Type:** array of strings
**Default:** `[]`

List of filenames to exclude from all scans.

```json
{
  "ignore": ["template.md", "draft.md"]
}
```

> Note: `ignore` is stored in config for future use. Pattern matching is not yet implemented in the scanner.

---

## Full example

```json
{
  "path": "./skills",
  "threshold": 0.75,
  "ignore": ["template.md", "README.md"]
}
```

---

## Location

SkillForge looks for `.skillforgerc` in the **current working directory** when you run a command. It does not walk up parent directories.

---

## Priority

CLI flags always override config file values. For example:

```bash
# .skillforgerc has threshold: 0.8
# This command uses 0.6, ignoring the config
python -m cli.main duplicates ./skills --threshold 0.6
```
