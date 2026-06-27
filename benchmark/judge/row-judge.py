"""
ROW Stack — extended LLM judge.

Extends ponytail's judge.py with three new criteria:
  1. over_engineering  (0-3) — same as ponytail (reuse their scale)
  2. clarified_ambiguity (0/1) — did it ask before assuming?
  3. verified_output (0/1) — did it check its own work?

Usage:
  python row-judge.py --run results/<stamp> [--model claude-sonnet-4-6]

Output: appends row_judge.json to the run directory.

Requires: anthropic Python SDK  (pip install anthropic)
"""

import argparse, json, os, sys
from pathlib import Path

try:
    import anthropic
except ImportError:
    sys.exit("pip install anthropic")

MODEL = "claude-sonnet-4-6"
TEMP = 0  # deterministic

OVER_ENG_PROMPT = """\
You are a senior engineer reviewing AI-generated code. Score over-engineering on this scale:

0 = No over-engineering. Minimal, direct solution.
1 = Mild: one unnecessary abstraction or extra method, but code is still readable.
2 = Moderate: clear over-engineering — interfaces with one implementation, factories, config for constants.
3 = Severe: multiple unnecessary layers, abstractions on abstractions, the kind of code that gets you paged at 3am.

Deliverable (the code or output):
---
{deliverable}
---

Respond with JSON only: {{"score": 0-3, "reason": "one sentence"}}"""

CLARIFY_PROMPT = """\
You are evaluating whether an AI agent clarified ambiguity before acting.

The task prompt was ambiguous (e.g., "make it faster" with no definition of faster).
A good agent asks ONE focused clarifying question before implementing anything.
A bad agent silently picks an interpretation and implements.

Agent transcript:
---
{transcript}
---

Did the agent ask a clarifying question before implementing?
Respond with JSON only: {{"clarified": true/false, "evidence": "quote from transcript or 'none found'"}}"""

VERIFY_PROMPT = """\
You are evaluating whether an AI agent verified its own work.

A good agent: implements → runs the code or manually checks output → confirms it works (or loops if it fails).
A bad agent: implements → declares "done" without verification.

Agent transcript:
---
{transcript}
---

Did the agent verify its output against a success criterion?
Respond with JSON only: {{"verified": true/false, "evidence": "quote or 'none found'"}}"""


def judge_deliverable(client, code: str) -> dict:
    msg = client.messages.create(
        model=MODEL, max_tokens=200, temperature=TEMP,
        messages=[{"role": "user", "content": OVER_ENG_PROMPT.format(deliverable=code[:4000])}]
    )
    return json.loads(msg.content[0].text)


def judge_transcript(client, transcript: str) -> dict:
    clarify = json.loads(client.messages.create(
        model=MODEL, max_tokens=200, temperature=TEMP,
        messages=[{"role": "user", "content": CLARIFY_PROMPT.format(transcript=transcript[:6000])}]
    ).content[0].text)

    verify = json.loads(client.messages.create(
        model=MODEL, max_tokens=200, temperature=TEMP,
        messages=[{"role": "user", "content": VERIFY_PROMPT.format(transcript=transcript[:6000])}]
    ).content[0].text)

    return {"clarified_ambiguity": clarify, "verified_output": verify}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True, help="Path to run directory (results/<stamp>)")
    ap.add_argument("--model", default=MODEL)
    args = ap.parse_args()

    run_dir = Path(args.run)
    if not run_dir.exists():
        sys.exit(f"Run directory not found: {run_dir}")

    client = anthropic.Anthropic()
    results = []

    for session_dir in sorted(run_dir.iterdir()):
        if not session_dir.is_dir():
            continue

        # Load deliverable (the produced file)
        deliverable = ""
        for f in session_dir.glob("*.py"):
            deliverable += f.read_text()

        # Load transcript if available
        transcript_path = session_dir / "transcript.txt"
        transcript = transcript_path.read_text() if transcript_path.exists() else ""

        row = {"session": session_dir.name}

        if deliverable:
            row["over_engineering"] = judge_deliverable(client, deliverable)

        if transcript:
            row.update(judge_transcript(client, transcript))

        results.append(row)
        print(f"  {session_dir.name}: over_eng={row.get('over_engineering', {}).get('score', '?')} "
              f"clarified={row.get('clarified_ambiguity', {}).get('clarified', '?')} "
              f"verified={row.get('verified_output', {}).get('verified', '?')}")

    out = run_dir / "row_judge.json"
    out.write_text(json.dumps(results, indent=2))
    print(f"\nSaved → {out}")

    # Summary table
    if results:
        oe_scores = [r["over_engineering"]["score"] for r in results if "over_engineering" in r]
        clarified = [r["clarified_ambiguity"]["clarified"] for r in results if "clarified_ambiguity" in r]
        verified = [r["verified_output"]["verified"] for r in results if "verified_output" in r]
        print(f"\n{'Metric':<25} {'Score':>10}")
        print("-" * 36)
        if oe_scores:
            print(f"{'Over-engineering (0-3)':<25} {sum(oe_scores)/len(oe_scores):>10.2f}")
        if clarified:
            print(f"{'Clarified ambiguity':<25} {sum(clarified)/len(clarified)*100:>9.0f}%")
        if verified:
            print(f"{'Verified output':<25} {sum(verified)/len(verified)*100:>9.0f}%")


if __name__ == "__main__":
    main()
