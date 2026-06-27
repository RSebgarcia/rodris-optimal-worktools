# Claude Product Stack — Workflow Guidelines

Behavioral guidelines for building products with Claude Code.
**Philosophy:** Working > Functional > Practical > Beautiful.

---

## 1. Think Before Coding (Karpathy)

**Don't assume. Surface ambiguity. Ask before building.**

Before implementing anything non-trivial:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them — don't pick silently.
- If a simpler approach exists, say so before starting.

## 2. Surgical Changes (Karpathy)

**Touch only what the request requires.**

- Don't "improve" adjacent code that isn't broken.
- Don't delete pre-existing code you don't understand — mention it, don't touch it.
- Every changed line should trace directly to the user's request.

## 3. Goal-Driven Execution + Loops (Karpathy)

**Define verifiable success criteria. Loop until verified.**

Transform tasks into verifiable goals before starting:
- "Fix the bug" → "write a test that reproduces it, then make it pass"
- "Add feature X" → "X works when [concrete condition]"

For multi-step tasks:
```
1. [step] → verify: [concrete check]
2. [step] → verify: [concrete check]
```
Use `/loop` to iterate until all checks pass.

## 4. Product Development Workflow

**Priority: Works > Practical > Beautiful**

- Ideas go directly to functional prototypes. No specs or mockups first.
- Beautiful design is a bonus, not a requirement. Functional design is non-negotiable.
- Ship what works, polish later.
- For iterative builds: use `/loop` with a defined success criterion.

When the user says "let's develop this idea":
1. Identify the core function (what does it need to *do*?)
2. Build the minimum that works end-to-end
3. Loop until it works
4. Aesthetics after, if needed

## 5. Mempalace — Cross-session Memory

**RECALL before solving. CAPTURE after solving.**

Before tackling any non-trivial problem, search mempalace:
```
mempalace_search("keywords describing the problem")
```

After solving, capture the solution:
```
mempalace_add_drawer(wing="project-name", room="problem-type", content="verbatim problem + solution")
```

- `wing` = project or domain (e.g. `my-app`, `general`)
- `room` = problem type (e.g. `auth-bugs`, `api-gotchas`, `deploy`)
- Store the **symptom + solution**, not just the fix — so future searches by symptom find it.

---

*Stack: [ponytail](https://github.com/DietrichGebert/ponytail) + [mempalace](https://github.com/multica-ai/mempalace) + [karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills)*
