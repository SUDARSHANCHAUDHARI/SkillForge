# Extensions

SkillForge ships with two extensions — one for VS Code and one for Chrome.

---

## VS Code Extension

Located in `vscode-extension/`.

### Features

- **SkillForge: Audit** — runs a full verbose audit on `./skills` and shows output in a dedicated Output Channel
- **SkillForge: Duplicates** — runs duplicate detection and shows results in the Output Channel

Output appears in the **SkillForge** panel in VS Code's Output tab (not a truncated notification), so you can scroll through full results.

### Install (local / development)

VS Code does not auto-load extensions from a folder. To load it:

**Option 1 — Load unpacked (quickest):**

1. Open VS Code
2. Press `Cmd+Shift+P` (or `Ctrl+Shift+P` on Windows)
3. Run: `Developer: Install Extension from Location...`
4. Select the `vscode-extension/` folder

**Option 2 — Package as VSIX:**

Install `vsce` if you don't have it:

```bash
npm install -g @vscode/vsce
```

Package the extension:

```bash
cd vscode-extension
vsce package
```

This produces `skillforge-0.1.0.vsix`. Install it:

```bash
code --install-extension skillforge-0.1.0.vsix
```

### Usage

1. Open the repo folder in VS Code
2. Press `Cmd+Shift+P`
3. Type `SkillForge` — you'll see:
   - `SkillForge: Audit`
   - `SkillForge: Duplicates`
4. Select a command — output appears in the **Output** panel under the **SkillForge** channel

### Requirements

- Python must be available as `python` in your terminal PATH
- The CLI must be installed (dependencies from `requirements.txt`)
- Your workspace must have a `./skills` folder

### Customising the skills path

The extension currently runs against `./skills` by default. To change this, edit `vscode-extension/extension.js`:

```js
// Change './skills' to your path
runCommand(['audit', './my-prompts'], 'Audit');
```

---

## Chrome Extension

Located in `chrome-extension/`.

### Features

- **Save Prompt** — paste any text and download it as a timestamped `.md` file (`prompt-YYYY-MM-DD.md`)
- **Analyze Prompt** — paste text and get instant quality feedback inline (too short, vague, missing structure)

### Install

1. Open Chrome and go to `chrome://extensions`
2. Enable **Developer mode** (toggle in the top right)
3. Click **Load unpacked**
4. Select the `chrome-extension/` folder
5. The **SkillForge** extension icon appears in your toolbar

### Usage

**Save Prompt:**
1. Click the SkillForge icon in Chrome toolbar
2. Click **Save Prompt**
3. Paste your prompt in the dialog
4. File downloads automatically as `prompt-YYYY-MM-DD.md`

**Analyze Prompt:**
1. Click the SkillForge icon
2. Click **Analyze Prompt**
3. Paste your prompt in the dialog
4. Issues appear in the popup:
   - `✔ Clean` — no issues found
   - `⚠ Too short` / `⚠ Vague summarization` — issues listed

### Permissions used

| Permission | Why |
|---|---|
| `downloads` | Required to save `.md` files to your downloads folder |

No other permissions. The extension does not read your browser tabs, history, or any page content.
