# Upstream update report

Generated: `2026-10-26T08:52:16+00:00`

## Summary

- Changed sources: 21
- Failures: 0
- Warnings: 0

## Changes

| Source | Old SHA-256 | New SHA-256 | Old rules | New rules |
|---|---|---|---:|---:|
| `test` | `57a9b902ab3d` | `19c9272be350` | 61 | 62 |
| `openai` | `19d194277b7e` | `6aede2e962e4` | 22 | 24 |
| `github` | `e1c015908fae` | `a4cde29dee08` | 64 | 65 |
| `facebook` | `f4bc4d117521` | `7bf95664c32f` | 396 | 397 |
| `amazon` | `019a5004d9d2` | `d96a707d904a` | 246 | 247 |
| `apple` | `d59fa9ff98d7` | `0b3e3fb23070` | 1792 | 1791 |
| `microsoft` | `a085037143f2` | `341653e81a6a` | 748 | 746 |
| `google-domain` | `f639665a2c02` | `c2c33af88268` | 1071 | 1075 |
| `google-ip` | `a0bbf374cbaa` | `1dac43101fc4` | 8059 | 8562 |
| `tiktok` | `80ae73c96756` | `a5f9d0dd4e26` | 36 | 37 |
| `netflix-ip` | `4f8f67135cbb` | `409cee1a04e6` | 114 | 122 |
| `blizzard` | `a3abfb91bb72` | `0ccab4f1bb94` | 62 | 62 |
| `global` | `d82b216fde0b` | `bfa334c45396` | 35028 | 35267 |
| `private-domain` | `10918636e35f` | `7f396a73bf5c` | 130 | 132 |
| `china-domain` | `6e658ba9a13e` | `943ac70a3819` | 111197 | 110175 |
| `china-ip` | `c00d29de109f` | `255e5b0e25fb` | 9651 | 10011 |
| `category-ads-all` | `d2490d5d7147` | `9b8adb6c409f` | 910 | 904 |
| `connectivity-check` | `90d6616b58e9` | `f233a6decd94` | 27 | 28 |
| `dropbox` | `6e96f161ed76` | `0b79496b3fb1` | 16 | 25 |
| `speedtest` | `53be15388001` | `f86908217750` | 13 | 20 |
| `category-scholar-!cn` | `37bbeece0e2d` | `0efdb0ea9a31` | 476 | 466 |

## Review checklist

- Inspect every changed rule file; do not approve based only on counts.
- Confirm unexpected deletions, policy-like entries, and major size changes.
- CI must compile MRS files and validate all generated configurations before merge.
