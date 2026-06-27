---
name: build-loop
description: Intelligent build loop integrating ponytail + karpathy + mempalace. Clarify → implement minimum → verify → loop until done → capture to memory. Use when the user says "/build", "let's build X", "develop this idea", or "make X work".
trigger: /build
---

You are in BUILD LOOP mode.

This skill integrates three layers: **ponytail** (minimum code), **karpathy** (think before coding, verify after), and **mempalace** (capture learnings). It loops until the goal is verifiably met.

---

## Phase 1 — CLARIFY

Before writing a single line of code:

1. State your assumptions about the goal explicitly. Example:
   > "I'm assuming: (a) input is a CSV file, (b) output goes to stdout, (c) no UI needed"

2. If any part is ambiguous, **ask one focused question**. Don't ask multiple questions — pick the one that unblocks the most.

3. Define **one verifiable success criterion**:
   > "This works when: [concrete, testable condition]"

Do not proceed to Phase 2 until the criterion is clear.

---

## Phase 2 — IMPLEMENT (ponytail rules)

Build the **minimum** that satisfies the criterion from Phase 1.

Climb the ladder — stop at the first rung that works:
1. Does this need to exist at all? (YAGNI)
2. Already in this codebase?
3. Stdlib does it?
4. Native platform feature covers it?
5. Already-installed dependency solves it?
6. Can it be one line?
7. Only then: minimum custom code

Touch **only** what the goal requires. No adjacent cleanup. No speculative features.

---

## Phase 3 — VERIFY

Test against the success criterion defined in Phase 1.

Run the code / check the output / verify the behavior. Report clearly:
- **PASS**: criterion met → go to Phase 4
- **FAIL**: state exactly what failed and why → loop back to Phase 2

Max 3 iterations before surfacing to the user: "Stuck after 3 attempts. Here's what I tried and where it fails: [summary]"

---

## Phase 4 — DONE

On PASS:

1. **Capture to mempalace**:
   ```
   mempalace_add_drawer(
     wing="[current project slug]",
     room="[feature type, e.g. 'cli-tools', 'data-pipeline']",
     content="[verbatim: what was built, the criterion, any gotchas discovered]"
   )
   ```

2. **Report concisely**: what was built, what was skipped, when to add it.

Pattern: `[code/feature] → skipped: [X], add when [Y].`

---

## Loop tracking

Keep a running count visible to the user:

```
BUILD LOOP — iteration 1/3
[Phase] ...
```

This makes the loop state transparent, not hidden.
