# Claude Product Stack

> A Claude Code workflow for people who build things. Functionality first, always.

---

## What this is

A layered set of guidelines and tools that make Claude Code behave like a senior developer focused on **shipping working products** — not writing perfect code or beautiful mockups that never ship.

**Philosophy:** `Works > Practical > Beautiful`

## The Stack

| Layer | Tool | What it does |
|-------|------|-------------|
| Write less code | [ponytail](https://github.com/DietrichGebert/ponytail) | Enforces the laziest solution that works. YAGNI, stdlib first, one line over fifty. |
| Think before coding | [karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills) | Surface assumptions before building. Surgical changes only. Define verifiable success criteria. |
| Remember between sessions | [mempalace](https://github.com/multica-ai/mempalace) | Cross-session memory. RECALL before solving, CAPTURE after. Never solve the same problem twice. |
| Iterate until it works | `/loop` (built-in) | Claude Code's built-in loop skill. Implement → verify → repeat until criterion passes. |
| Product mindset | `CLAUDE.md` (this repo) | Ideas → working prototypes directly. No specs, no mockups first. |

## Why this combination

Each layer answers a different question:

- **ponytail** → *How much* code to write? (minimum)
- **karpathy** → *How* to think before writing?
- **mempalace** → *What* to remember between sessions?
- **loops** → *How* to iterate until it works?
- **product workflow** → *Why* are we building this? (functionality, not aesthetics)

## The loop pattern for product development

```
"Let's build X"
  ↓
Karpathy: What does it need to DO? Surface assumptions.
  ↓
Ponytail: Minimum that works end-to-end.
  ↓
/loop: implement → verify → fix → repeat until criterion passes
  ↓
Mempalace: capture learnings for next session
  ↓
Ship. Polish later if needed.
```

## Using `/bloop`

`/bloop [goal]` is the core command — it activates the intelligent build loop.

| Environment | How to invoke |
|-------------|--------------|
| **Desktop app** | Type `bloop [goal]` (no slash — desktop app doesn't support custom slash commands) |
| **CLI terminal** | `/bloop [goal]` after installing the plugin (see below) |

Both work identically. The slash is a UI affordance, not a behavior change.

**CLI install:**
```
/plugin marketplace add RSebgarcia/rodris-optimal-worktools
```

## Install

See [setup/QUICKSTART.md](setup/QUICKSTART.md) — ~10 minutes, works on Windows, Mac, Linux.

## Files

| File | What it is |
|------|-----------|
| `CLAUDE.md` | Guidelines template — copy to `~/.claude/CLAUDE.md` |
| `settings.json.template` | Settings template with mempalace config |
| `setup/QUICKSTART.md` | 5-step install guide |
| `setup/windows.md` | Windows-specific notes |
| `setup/mac-linux.md` | Mac/Linux-specific notes |

## What this is NOT

- A replacement for tests or validation
- An excuse to skip error handling at system boundaries
- A "design is unimportant" manifesto — functional design matters; decorative design is optional

---

*Built on: [Claude Code](https://claude.ai/code) · [ponytail](https://github.com/DietrichGebert/ponytail) · [mempalace](https://github.com/multica-ai/mempalace) · [karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills)*
