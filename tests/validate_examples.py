#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = {"project", "thesis", "evidence", "sections", "documents", "status"}
ALLOWED_LEVELS = {f"L{i}" for i in range(7)}
ALLOWED_INTERACTIVE = {"none", "weighted-risk", "maturity-ladder"}


def validate(path: Path) -> list[str]:
    errors: list[str] = []
    data = json.loads(path.read_text(encoding="utf-8"))
    missing = REQUIRED - set(data)
    if missing:
        errors.append(f"missing top-level keys: {sorted(missing)}")
    level = data.get("evidence", {}).get("level")
    if level not in ALLOWED_LEVELS:
        errors.append(f"invalid evidence level: {level!r}")
    interactive = data.get("interactive", {}).get("type", "none")
    if interactive not in ALLOWED_INTERACTIVE:
        errors.append(f"invalid interactive type: {interactive!r}")
    for document in data.get("documents", []):
        relative = document.get("path")
        if not relative:
            errors.append("document entry missing path")
        elif not (path.parent / relative).exists():
            errors.append(f"missing document file: {relative}")
    return errors


def main() -> int:
    failed = False
    for path in sorted((ROOT / "examples").glob("*/theory.json")):
        errors = validate(path)
        if errors:
            failed = True
            print(f"FAIL {path.relative_to(ROOT)}")
            for error in errors:
                print(f"  - {error}")
        else:
            print(f"PASS {path.relative_to(ROOT)}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
