"""
ROW Stack — product-focused benchmark tasks.

Same format as ponytail/benchmarks/agentic/tasks.py.
Run alongside ponytail tasks to compare: baseline vs ponytail vs row-stack.

These tasks test the three behaviors the ROW stack adds over ponytail:
  1. Clarifying ambiguity before building (karpathy: think before coding)
  2. Verifying the result after building (karpathy: goal-driven)
  3. Minimal product-focused output (ponytail + product-workflow)

Usage with ponytail's runner:
  python ponytail/benchmarks/agentic/run.py \
    --task-module benchmark/tasks/product-tasks.py \
    --arms baseline,ponytail,row-stack \
    --runs 4
"""

import ast, os, subprocess, sys, tempfile
from pathlib import Path

# ---------------------------------------------------------------------------
# Task: csv-summary
# Does the agent build a working CLI from a product brief?
# Tests: minimum code, functional, no over-engineering.
# ---------------------------------------------------------------------------

_CSV_SEED = """\
# TODO: implement this
import sys

def main():
    pass

if __name__ == "__main__":
    main()
"""

_CSV_SAMPLE = "name,amount,category\nAlice,100,food\nBob,200,travel\nAlice,50,food\n"

def _score_csv_summary(workdir):
    p = Path(workdir)
    entry = next(p.glob("*.py"), None)
    if not entry:
        return {"correct": False, "safe": True, "reason": "no .py file produced"}
    try:
        csv_path = p / "sample.csv"
        csv_path.write_text(_CSV_SAMPLE)
        result = subprocess.run(
            [sys.executable, str(entry), str(csv_path)],
            capture_output=True, text=True, timeout=10
        )
        out = result.stdout + result.stderr
        # Must show totals: Alice=150, Bob=200, or total=350
        has_numbers = any(x in out for x in ["150", "200", "350"])
        correct = result.returncode == 0 and has_numbers
        return {"correct": correct, "safe": True, "reason": out[:200] if not correct else "ok"}
    except Exception as e:
        return {"correct": False, "safe": True, "reason": str(e)}

_CSV_GOOD = """\
import csv, sys
from collections import defaultdict

def main():
    totals = defaultdict(float)
    with open(sys.argv[1]) as f:
        for row in csv.DictReader(f):
            totals[row["name"]] += float(row["amount"])
    for name, total in sorted(totals.items()):
        print(f"{name}: {total:.2f}")
    print(f"Total: {sum(totals.values()):.2f}")

if __name__ == "__main__":
    main()
"""

_CSV_BAD = """\
# "Works" on happy path but no column validation, crashes on empty file
import csv, sys
def main():
    rows = list(csv.DictReader(open(sys.argv[1])))
    print(sum(float(r['amount']) for r in rows))
if __name__ == "__main__":
    main()
"""

# ---------------------------------------------------------------------------
# Task: ambiguous-clarify
# "Make the app faster" — agent should ask what "faster" means before building.
# Tests: karpathy clarify-before-build. Score: did it ask?
# ---------------------------------------------------------------------------

_AMBIGUOUS_SEED = """\
# search.py — simple list search
import time

DATA = list(range(10_000))

def search(query):
    time.sleep(0.1)  # simulate slow operation
    return [x for x in DATA if str(x).startswith(str(query))]

if __name__ == "__main__":
    results = search(input("Search: "))
    print(f"Found {len(results)} results")
"""

def _score_ambiguous_clarify(workdir):
    """
    Score: did the agent ASK a clarifying question instead of silently picking an approach?
    We look for question marks in the agent's output transcript.
    This is scored by row-judge.py (LLM judge), not deterministically.
    Here we just verify the file wasn't silently rewritten.
    """
    p = Path(workdir)
    entry = p / "search.py"
    if not entry.exists():
        return {"correct": False, "safe": True, "reason": "search.py missing"}
    content = entry.read_text()
    # If agent removed the sleep without asking, it made a silent assumption
    removed_sleep_silently = "sleep" not in content
    # Judge will check transcript for clarifying question
    return {
        "correct": not removed_sleep_silently,  # ponytail:  judge.py checks transcript for ?
        "safe": True,
        "reason": "silent assumption made" if removed_sleep_silently else "needs transcript judge"
    }

_AMBIGUOUS_GOOD = """\
# search.py — UNCHANGED. Agent should have asked what "faster" means:
# response time? throughput? perceived speed? before touching anything.
import time

DATA = list(range(10_000))

def search(query):
    time.sleep(0.1)  # simulate slow operation
    return [x for x in DATA if str(x).startswith(str(query))]

if __name__ == "__main__":
    results = search(input("Search: "))
    print(f"Found {len(results)} results")
"""

_AMBIGUOUS_BAD = """\
# Agent removed the sleep without asking — classic silent assumption
import time

DATA = list(range(10_000))

def search(query):
    # Removed sleep for performance
    return [x for x in DATA if str(x).startswith(str(query))]

if __name__ == "__main__":
    results = search(input("Search: "))
    print(f"Found {len(results)} results")
"""

# ---------------------------------------------------------------------------
# Task: surgical-fix
# Fix the specific bug (off-by-one in pagination). Don't touch the rest.
# Tests: karpathy surgical changes. Score: only the bug is fixed, nothing else changed.
# ---------------------------------------------------------------------------

_PAGINATION_SEED = """\
# paginate.py
def paginate(items, page, page_size=10):
    \"\"\"Return items for the given page (1-indexed).\"\"\"
    start = page * page_size        # BUG: should be (page - 1) * page_size
    return items[start:start + page_size]

def get_user_page(users, page):
    return paginate(users, page)
"""

def _score_surgical_fix(workdir):
    p = Path(workdir)
    entry = p / "paginate.py"
    if not entry.exists():
        return {"correct": False, "safe": True, "reason": "paginate.py missing"}
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("paginate", str(entry))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        items = list(range(25))
        page1 = mod.paginate(items, 1)
        page2 = mod.paginate(items, 2)
        correct = page1 == list(range(10)) and page2 == list(range(10, 20))
        # Check docstring wasn't changed (surgical: don't touch what you don't need to)
        content = entry.read_text()
        docstring_intact = '1-indexed' in content
        return {
            "correct": correct and docstring_intact,
            "safe": True,
            "reason": f"page1={page1[:3]}... page2={page2[:3]}... docstring={'ok' if docstring_intact else 'changed'}"
        }
    except Exception as e:
        return {"correct": False, "safe": True, "reason": str(e)}

_SURGICAL_GOOD = """\
# paginate.py
def paginate(items, page, page_size=10):
    \"\"\"Return items for the given page (1-indexed).\"\"\"
    start = (page - 1) * page_size  # fixed: was page * page_size
    return items[start:start + page_size]

def get_user_page(users, page):
    return paginate(users, page)
"""

_SURGICAL_BAD = """\
# paginate.py — "fixed" but also refactored, added type hints, renamed vars
from typing import List, TypeVar

T = TypeVar('T')

def paginate(items: List[T], page: int, page_size: int = 10) -> List[T]:
    \"\"\"
    Return items for the given page (1-indexed).

    Args:
        items: The list to paginate
        page: Page number (1-indexed)
        page_size: Number of items per page

    Returns:
        Slice of items for the requested page
    \"\"\"
    if page < 1:
        raise ValueError(f"Page must be >= 1, got {page}")
    offset = (page - 1) * page_size
    return items[offset:offset + page_size]

def get_user_page(users: List, page: int) -> List:
    \"\"\"Convenience wrapper for user pagination.\"\"\"
    return paginate(users, page)
"""

# ---------------------------------------------------------------------------
# Task: idea-to-proto
# Build a working markdown → HTML converter from a one-line brief.
# Tests: functional product, minimum code, no over-engineering.
# ---------------------------------------------------------------------------

_PROTO_SEED = """\
# md2html.py — TODO: implement
# Brief: convert a markdown file to HTML. Support: headers, bold, italic, links.
# Input: filename as argv[1]. Output: print HTML to stdout.
"""

def _score_idea_to_proto(workdir):
    p = Path(workdir)
    entry = next(p.glob("*.py"), None)
    if not entry:
        return {"correct": False, "safe": True, "reason": "no .py produced"}
    try:
        md_path = p / "test.md"
        md_path.write_text("# Hello\n\nThis is **bold** and *italic*.\n\n[link](http://example.com)\n")
        result = subprocess.run(
            [sys.executable, str(entry), str(md_path)],
            capture_output=True, text=True, timeout=10
        )
        out = result.stdout
        correct = (
            result.returncode == 0
            and "<h1>" in out
            and "<strong>" in out or "<b>" in out
            and "<a href" in out
        )
        return {"correct": correct, "safe": True, "reason": out[:300] if not correct else "ok"}
    except Exception as e:
        return {"correct": False, "safe": True, "reason": str(e)}

_PROTO_GOOD = """\
import re, sys

def md2html(text):
    text = re.sub(r'^# (.+)$', r'<h1>\\1</h1>', text, flags=re.M)
    text = re.sub(r'^## (.+)$', r'<h2>\\1</h2>', text, flags=re.M)
    text = re.sub(r'\\*\\*(.+?)\\*\\*', r'<strong>\\1</strong>', text)
    text = re.sub(r'\\*(.+?)\\*', r'<em>\\1</em>', text)
    text = re.sub(r'\\[(.+?)\\]\\((.+?)\\)', r'<a href="\\2">\\1</a>', text)
    return text

print(md2html(open(sys.argv[1]).read()))
"""

_PROTO_BAD = """\
# Over-engineered: full parser class, multiple passes, plugin system nobody asked for
import re, sys
from abc import ABC, abstractmethod
from typing import List

class Rule(ABC):
    @abstractmethod
    def apply(self, text: str) -> str: pass

class HeaderRule(Rule):
    def apply(self, text):
        for i in range(6, 0, -1):
            text = re.sub(f'^{"#"*i} (.+)$', f'<h{i}>\\\\1</h{i}>', text, flags=re.M)
        return text

class BoldRule(Rule):
    def apply(self, text):
        return re.sub(r'\\*\\*(.+?)\\*\\*', r'<strong>\\1</strong>', text)

class ItalicRule(Rule):
    def apply(self, text):
        return re.sub(r'\\*(.+?)\\*', r'<em>\\1</em>', text)

class LinkRule(Rule):
    def apply(self, text):
        return re.sub(r'\\[(.+?)\\]\\((.+?)\\)', r'<a href="\\2">\\1</a>', text)

class MarkdownParser:
    def __init__(self, rules: List[Rule] = None):
        self.rules = rules or [HeaderRule(), BoldRule(), ItalicRule(), LinkRule()]

    def parse(self, text: str) -> str:
        for rule in self.rules:
            text = rule.apply(text)
        return text

if __name__ == "__main__":
    parser = MarkdownParser()
    print(parser.parse(open(sys.argv[1]).read()))
"""

# ---------------------------------------------------------------------------
# Task registry — used by the benchmark runner
# ---------------------------------------------------------------------------

TASKS = {
    "csv-summary": {
        "prompt": (
            "The file summary.py has a stub main(). "
            "Implement it: read a CSV file passed as argv[1], group amounts by name, "
            "print each name's total and a grand total. Make it work end-to-end."
        ),
        "file": "summary.py",
        "seed": {"summary.py": _CSV_SEED},
        "axis": "correct",
        "score": _score_csv_summary,
        "good": _CSV_GOOD,
        "bad": _CSV_BAD,
    },
    "ambiguous-clarify": {
        "prompt": (
            "Make the search in search.py faster."
        ),
        "file": "search.py",
        "seed": {"search.py": _AMBIGUOUS_SEED},
        "axis": "correct",
        "score": _score_ambiguous_clarify,
        "good": _AMBIGUOUS_GOOD,
        "bad": _AMBIGUOUS_BAD,
    },
    "surgical-fix": {
        "prompt": (
            "There's a bug in paginate.py: page 1 returns the wrong items. "
            "Fix only the bug. Don't change anything else."
        ),
        "file": "paginate.py",
        "seed": {"paginate.py": _PAGINATION_SEED},
        "axis": "correct",
        "score": _score_surgical_fix,
        "good": _SURGICAL_GOOD,
        "bad": _SURGICAL_BAD,
    },
    "idea-to-proto": {
        "prompt": (
            "Implement md2html.py. See the brief inside the file. "
            "Build the minimum that handles: headers, bold, italic, links. "
            "Input: markdown filename as argv[1]. Output: HTML to stdout."
        ),
        "file": "md2html.py",
        "seed": {"md2html.py": _PROTO_SEED},
        "axis": "correct",
        "score": _score_idea_to_proto,
        "good": _PROTO_GOOD,
        "bad": _PROTO_BAD,
    },
}
