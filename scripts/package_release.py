#!/usr/bin/env python3
"""Create immutable configs and a checksumed offline release bundle."""

from __future__ import annotations

import argparse
import hashlib
import shutil
import subprocess
import tarfile
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("tag", help="immutable Git tag, for example v2026.07.10")
    args = parser.parse_args()
    if not args.tag.startswith("v"):
        parser.error("tag must start with v")
    dist = ROOT / "dist"
    shutil.rmtree(dist, ignore_errors=True)
    bundle = dist / f"ProxyRule-{args.tag}"
    bundle.mkdir(parents=True)
    subprocess.run([
        "python3", str(ROOT / "scripts/generate_configs.py"), "--ref", args.tag,
        "--output-dir", str(bundle / "config"), "--prefix", "openclash-pinned",
    ], check=True)
    shutil.copytree(ROOT / "rules", bundle / "rules")
    for name in ["README.md", "NOTICE.md", "sources.json"]:
        shutil.copy2(ROOT / name, bundle / name)
    tar_path = dist / f"ProxyRule-{args.tag}.tar.gz"
    zip_path = dist / f"ProxyRule-{args.tag}.zip"
    with tarfile.open(tar_path, "w:gz") as archive:
        archive.add(bundle, arcname=bundle.name)
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(bundle.rglob("*")):
            if path.is_file():
                archive.write(path, path.relative_to(dist))
    checksum_files = sorted([tar_path, zip_path, *list((bundle / "config").glob("*.yaml"))])
    (dist / "SHA256SUMS").write_text(
        "".join(f"{digest(path)}  {path.relative_to(dist)}\n" for path in checksum_files),
        encoding="utf-8",
    )
    print(f"created release bundle for {args.tag}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
