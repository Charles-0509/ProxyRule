#!/usr/bin/env python3
"""Synchronize and validate rule sources without executing upstream content."""

from __future__ import annotations

import argparse
import hashlib
import ipaddress
import json
import re
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "sources.json"
REPORT = ROOT / "UPSTREAM_UPDATE_REPORT.md"
USER_AGENT = "Charles-0509/ProxyRule rule auditor"
FORBIDDEN_CLASSICAL = {"MATCH", "RULE-SET", "SCRIPT", "SUB-RULE"}


class ValidationError(RuntimeError):
    pass


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_manifest() -> dict:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def write_manifest(manifest: dict) -> None:
    manifest["generated_at"] = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    MANIFEST.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def meaningful_lines(text: str) -> list[str]:
    return [
        line.strip()
        for line in text.splitlines()
        if line.strip() and not line.lstrip().startswith(("#", "//"))
    ]


def yaml_payload(text: str) -> list[str]:
    lines = meaningful_lines(text)
    if not lines or lines[0] != "payload:":
        raise ValidationError("YAML ruleset must start with payload:")
    payload: list[str] = []
    for line in lines[1:]:
        match = re.match(r"^-\s+(.+?)\s*$", line)
        if not match:
            raise ValidationError(f"invalid YAML payload line: {line[:120]}")
        item = match.group(1)
        if len(item) >= 2 and item[0] == item[-1] and item[0] in {"'", '"'}:
            item = item[1:-1]
        payload.append(item)
    if not payload:
        raise ValidationError("ruleset payload is empty")
    return payload


def validate_classical(lines: list[str]) -> list[str]:
    warnings: list[str] = []
    if not lines:
        raise ValidationError("classical ruleset is empty")
    for number, line in enumerate(lines, 1):
        token = line.split(",", 1)[0].strip().upper()
        if not re.fullmatch(r"[A-Z][A-Z0-9-]*", token):
            raise ValidationError(f"line {number}: invalid rule token {token!r}")
        if token in FORBIDDEN_CLASSICAL:
            warnings.append(f"line {number}: forbidden control rule {token}")
        fields = [field.strip().upper() for field in line.split(",")]
        if len(fields) >= 3 and fields[-1] in {"DIRECT", "REJECT", "PROXY"}:
            warnings.append(f"line {number}: appears to contain an embedded policy")
    return warnings


def normalize_and_validate(entry: dict, raw: bytes) -> tuple[bytes, int, list[str]]:
    if b"\x00" in raw:
        raise ValidationError("NUL byte detected")
    try:
        text = raw.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise ValidationError(f"not valid UTF-8: {exc}") from exc
    sample = text.lstrip()[:256].lower()
    if sample.startswith(("<!doctype html", "<html", "<head", "<body")):
        raise ValidationError("received HTML instead of a ruleset")
    text = text.replace("\r\n", "\n").replace("\r", "\n").rstrip() + "\n"
    warnings: list[str] = []
    if entry["source_format"] == "yaml":
        items = yaml_payload(text)
        if entry["behavior"] == "ipcidr":
            for item in items:
                try:
                    ipaddress.ip_network(item, strict=False)
                except ValueError as exc:
                    raise ValidationError(f"invalid CIDR {item!r}") from exc
        count = len(items)
    elif entry["source_format"] == "text":
        lines = meaningful_lines(text)
        warnings.extend(validate_classical(lines))
        count = len(lines)
    else:
        raise ValidationError(f"unsupported source format {entry['source_format']!r}")
    return text.encode("utf-8"), count, warnings


def download(entry: dict) -> bytes:
    request = urllib.request.Request(entry["source_url"], headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=30) as response:
        content_type = response.headers.get("Content-Type", "")
        raw = response.read(entry["max_size"] + 1)
        if len(raw) > entry["max_size"]:
            raise ValidationError(f"response exceeds {entry['max_size']} bytes")
        if "text/html" in content_type.lower():
            raise ValidationError(f"unexpected content type {content_type}")
        return raw


def validate_entry_file(entry: dict) -> tuple[bytes, int, list[str]]:
    path = ROOT / entry["source_path"]
    if not path.is_file():
        raise ValidationError(f"missing local source {entry['source_path']}")
    return normalize_and_validate(entry, path.read_bytes())


def render_report(changes: list[dict], failures: list[str], warnings: list[str]) -> str:
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    lines = ["# Upstream update report", "", f"Generated: `{now}`", ""]
    lines += ["## Summary", "", f"- Changed sources: {len(changes)}", f"- Failures: {len(failures)}", f"- Warnings: {len(warnings)}", ""]
    if changes:
        lines += ["## Changes", "", "| Source | Old SHA-256 | New SHA-256 | Old rules | New rules |", "|---|---|---|---:|---:|"]
        for item in changes:
            lines.append(
                f"| `{item['id']}` | `{item['old_sha'][:12] or '-'}` | `{item['new_sha'][:12]}` | {item['old_count']} | {item['new_count']} |"
            )
        lines.append("")
    if warnings:
        lines += ["## Warnings requiring review", ""] + [f"- {item}" for item in warnings] + [""]
    if failures:
        lines += ["## Failures", ""] + [f"- {item}" for item in failures] + [""]
    lines += [
        "## Review checklist",
        "",
        "- Inspect every changed rule file; do not approve based only on counts.",
        "- Confirm unexpected deletions, policy-like entries, and major size changes.",
        "- CI must compile MRS files and validate all generated configurations before merge.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--update", action="store_true", help="download remote sources and update the manifest")
    parser.add_argument("--validate-local", action="store_true", help="validate committed files and hashes")
    parser.add_argument("--allow-large-change", action="store_true")
    args = parser.parse_args()
    if args.update == args.validate_local:
        parser.error("choose exactly one of --update or --validate-local")

    manifest = load_manifest()
    changes: list[dict] = []
    failures: list[str] = []
    warnings: list[str] = []
    downloaded: dict[str, bytes] = {}
    download_failures: dict[str, Exception] = {}

    if args.update:
        remote_entries = [entry for entry in manifest["sources"] if not entry.get("local", False)]
        with ThreadPoolExecutor(max_workers=8) as executor:
            futures = {executor.submit(download, entry): entry for entry in remote_entries}
            for future in as_completed(futures):
                entry = futures[future]
                try:
                    downloaded[entry["id"]] = future.result()
                except Exception as exc:  # Network and validation errors are rendered into the audit report.
                    download_failures[entry["id"]] = exc

    for entry in manifest["sources"]:
        try:
            if args.update:
                if entry.get("local", False):
                    normalized, count, entry_warnings = validate_entry_file(entry)
                else:
                    if entry["id"] in download_failures:
                        raise download_failures[entry["id"]]
                    normalized, count, entry_warnings = normalize_and_validate(entry, downloaded[entry["id"]])
                old_count = int(entry.get("line_count", 0))
                old_sha = entry.get("sha256", "")
                new_sha = sha256(normalized)
                if old_count >= 50 and count < old_count * 0.6 and not args.allow_large_change:
                    entry_warnings.append(f"rule count shrank from {old_count} to {count}")
                if new_sha != old_sha:
                    path = ROOT / entry["source_path"]
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_bytes(normalized)
                    changes.append({
                        "id": entry["id"], "old_sha": old_sha, "new_sha": new_sha,
                        "old_count": old_count, "new_count": count,
                    })
                entry["sha256"] = new_sha
                entry["line_count"] = count
            else:
                normalized, count, entry_warnings = validate_entry_file(entry)
                actual_sha = sha256(normalized)
                if actual_sha != entry.get("sha256"):
                    raise ValidationError(
                        f"SHA mismatch for {entry['source_path']}: manifest={entry.get('sha256')} actual={actual_sha}"
                    )
                if count != entry.get("line_count"):
                    raise ValidationError(
                        f"rule count mismatch for {entry['source_path']}: manifest={entry.get('line_count')} actual={count}"
                    )
            warnings.extend(f"`{entry['id']}`: {item}" for item in entry_warnings)
        except (ValidationError, urllib.error.URLError, TimeoutError, ValueError) as exc:
            failures.append(f"`{entry['id']}`: {exc}")

    if args.update:
        if changes or failures or warnings:
            write_manifest(manifest)
            REPORT.write_text(render_report(changes, failures, warnings), encoding="utf-8")
        else:
            print("no upstream changes detected")
    if failures or warnings:
        for item in failures + warnings:
            print(item, file=sys.stderr)
        return 2
    print(f"validated {len(manifest['sources'])} rule sources")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
