#!/usr/bin/env python3
"""Build all MRS rule providers from their committed, reviewable sources."""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def mihomo_binary() -> str:
    override = os.environ.get("MIHOMO_BIN")
    if override:
        return override
    result = subprocess.run(
        ["python3", str(ROOT / "scripts/ensure_mihomo.py")],
        check=True,
        text=True,
        capture_output=True,
    )
    return result.stdout.strip().splitlines()[-1]


def main() -> int:
    manifest = json.loads((ROOT / "sources.json").read_text(encoding="utf-8"))
    binary = mihomo_binary()
    built = 0
    for entry in manifest["sources"]:
        if entry.get("runtime_format") != "mrs":
            continue
        source = ROOT / entry["source_path"]
        output = ROOT / entry["runtime_path"]
        output.parent.mkdir(parents=True, exist_ok=True)
        temporary = output.with_suffix(output.suffix + ".tmp")
        temporary.unlink(missing_ok=True)
        subprocess.run(
            [binary, "convert-ruleset", entry["behavior"], entry["source_format"], str(source), str(temporary)],
            check=True,
        )
        temporary.replace(output)
        built += 1
    print(f"built {built} MRS files with {binary}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
