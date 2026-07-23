#!/usr/bin/env python3
"""Build all reference sites into public/sites with zero external dependencies."""
from __future__ import annotations

import importlib.util
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GENERATOR = ROOT / "core" / "generator" / "generate_site.py"
PUBLIC = ROOT / "public"


def load_generator():
    spec = importlib.util.spec_from_file_location("evesite_generator", GENERATOR)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load generator: {GENERATOR}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    module = load_generator()
    site_root = PUBLIC / "sites"
    if site_root.exists():
        shutil.rmtree(site_root)
    site_root.mkdir(parents=True)

    for example in sorted((ROOT / "examples").glob("*/theory.json")):
        data = json.loads(example.read_text(encoding="utf-8"))
        output = site_root / example.parent.name
        module.generate(data, example.parent, output)
        print(f"Built {example.parent.name} -> {output.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
