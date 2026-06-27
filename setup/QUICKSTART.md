# Quickstart — 5 steps

**Time: ~10 minutes. Works on Windows, Mac, Linux.**

---

### Step 1 — Install Claude Code

```bash
npm install -g @anthropic-ai/claude-code
```

> Already installed? Skip to step 2.

---

### Step 2 — Install Ponytail (lazy senior dev mode)

In any Claude Code session:

```
/plugin marketplace add forrestchang/andrej-karpathy-skills
```

Then install ponytail:

```bash
# Claude Code plugin
/plugin marketplace add dietrichgebert/ponytail
```

---

### Step 3 — Install Mempalace (cross-session memory)

```bash
npm install -g mempalace-mcp
```

Choose a folder for your memory palace — this is where Claude stores learnings between sessions:

```bash
# Mac/Linux
mkdir -p ~/claude-memory

# Windows (PowerShell)
mkdir "$HOME\claude-memory"
```

---

### Step 4 — Configure settings.json

Copy `settings.json.template` to your Claude settings:

```bash
# Mac/Linux
cp settings.json.template ~/.claude/settings.json

# Windows
copy settings.json.template %USERPROFILE%\.claude\settings.json
```

Edit the file and replace `<YOUR_PALACE_PATH>` with your actual path:
- Mac/Linux: `/home/yourname/claude-memory`
- Windows: `C:\Users\yourname\claude-memory`

---

### Step 5 — Add the workflow guidelines

Copy `CLAUDE.md` to your global Claude config:

```bash
# Mac/Linux — append to existing or create new
cat CLAUDE.md >> ~/.claude/CLAUDE.md

# Windows (PowerShell)
Get-Content CLAUDE.md | Add-Content "$HOME\.claude\CLAUDE.md"
```

---

### Done. Test it.

Start a new Claude Code session and ask:

> "What's our workflow for developing a product idea?"

Claude should describe the functionality-first loop pattern.

---

### Optional: Karpathy Skills as a plugin

The Karpathy guidelines are already included in `CLAUDE.md`. If you prefer the auto-updating plugin version:

```
/plugin marketplace add forrestchang/andrej-karpathy-skills
```

(You can then remove the karpathy sections from CLAUDE.md to avoid duplication.)
