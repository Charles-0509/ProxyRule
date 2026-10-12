# Upstream update report

Generated: `2026-10-12T10:46:12+00:00`

## Summary

- Changed sources: 18
- Failures: 0
- Warnings: 0

## Changes

| Source | Old SHA-256 | New SHA-256 | Old rules | New rules |
|---|---|---|---:|---:|
| `test` | `57a9b902ab3d` | `19c9272be350` | 61 | 62 |
| `github` | `e1c015908fae` | `a4cde29dee08` | 64 | 65 |
| `facebook` | `f4bc4d117521` | `7bf95664c32f` | 396 | 397 |
| `amazon` | `019a5004d9d2` | `7ce70391ff6b` | 246 | 246 |
| `apple` | `d59fa9ff98d7` | `c76682fc9a3d` | 1792 | 1792 |
| `microsoft` | `a085037143f2` | `6f3b5096b02d` | 748 | 749 |
| `google-domain` | `f639665a2c02` | `024b2b86dd53` | 1071 | 1075 |
| `google-ip` | `a0bbf374cbaa` | `c137afaa53d1` | 8059 | 8495 |
| `tiktok` | `80ae73c96756` | `a5f9d0dd4e26` | 36 | 37 |
| `netflix-ip` | `4f8f67135cbb` | `409cee1a04e6` | 114 | 122 |
| `disney` | `8931d356f6fd` | `21fee1a588ef` | 224 | 224 |
| `blizzard` | `a3abfb91bb72` | `148f4ff869a4` | 62 | 62 |
| `global` | `d82b216fde0b` | `29bbe7ffad77` | 35028 | 35183 |
| `china-domain` | `6e658ba9a13e` | `fe50d8caf6e9` | 111197 | 111595 |
| `china-ip` | `c00d29de109f` | `f1141dede283` | 9651 | 9609 |
| `category-ads-all` | `d2490d5d7147` | `97d4f56f7e39` | 910 | 902 |
| `connectivity-check` | `90d6616b58e9` | `f233a6decd94` | 27 | 28 |
| `category-scholar-!cn` | `37bbeece0e2d` | `bdd84618c13a` | 476 | 476 |

## Review checklist

- Inspect every changed rule file; do not approve based only on counts.
- Confirm unexpected deletions, policy-like entries, and major size changes.
- CI must compile MRS files and validate all generated configurations before merge.
