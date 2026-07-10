#!/usr/bin/env python3
"""Download the pinned Mihomo binary and verify its release digest."""

from __future__ import annotations

import gzip
import hashlib
import json
import os
import platform
import shutil
import stat
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = json.loads((ROOT / "tools/mihomo.json").read_text(encoding="utf-8"))


def main() -> int:
    override = os.environ.get("MIHOMO_BIN")
    if override:
        print(override)
        return 0
    os_name = {"Darwin": "darwin", "Linux": "linux"}.get(platform.system())
    arch = {"arm64": "arm64", "aarch64": "arm64", "x86_64": "amd64", "AMD64": "amd64"}.get(platform.machine())
    key = f"{os_name}-{arch}"
    if key not in SPEC["assets"]:
        raise SystemExit(f"unsupported build host {key}")
    asset = SPEC["assets"][key]
    cache = ROOT / ".cache" / "mihomo" / SPEC["version"]
    binary = cache / "mihomo"
    if binary.is_file():
        print(binary)
        return 0
    cache.mkdir(parents=True, exist_ok=True)
    archive = cache / asset["name"]
    request = urllib.request.Request(asset["url"], headers={"User-Agent": "ProxyRule builder"})
    with urllib.request.urlopen(request, timeout=120) as response, archive.open("wb") as output:
        shutil.copyfileobj(response, output)
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    if digest != asset["sha256"]:
        archive.unlink(missing_ok=True)
        raise SystemExit(f"Mihomo digest mismatch: expected {asset['sha256']}, got {digest}")
    with gzip.open(archive, "rb") as source, binary.open("wb") as output:
        shutil.copyfileobj(source, output)
    binary.chmod(binary.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    print(binary)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
