# Upstream update report

Generated: `2026-10-05T10:23:44+00:00`

## Summary

- Changed sources: 17
- Failures: 0
- Warnings: 0

## Changes

| Source | Old SHA-256 | New SHA-256 | Old rules | New rules |
|---|---|---|---:|---:|
| `test` | `57a9b902ab3d` | `19c9272be350` | 61 | 62 |
| `facebook` | `f4bc4d117521` | `7bf95664c32f` | 396 | 397 |
| `amazon` | `019a5004d9d2` | `7ce70391ff6b` | 246 | 246 |
| `apple` | `d59fa9ff98d7` | `d007c88e9fe4` | 1792 | 1792 |
| `microsoft` | `a085037143f2` | `a4a56ddb524e` | 748 | 748 |
| `google-domain` | `f639665a2c02` | `083506f0076a` | 1071 | 1075 |
| `google-ip` | `a0bbf374cbaa` | `163528e5e435` | 8059 | 8483 |
| `tiktok` | `80ae73c96756` | `a5f9d0dd4e26` | 36 | 37 |
| `netflix-ip` | `4f8f67135cbb` | `409cee1a04e6` | 114 | 122 |
| `disney` | `8931d356f6fd` | `10cceb54944b` | 224 | 224 |
| `blizzard` | `a3abfb91bb72` | `87acd09682cf` | 62 | 62 |
| `global` | `d82b216fde0b` | `d1f1effd3ef6` | 35028 | 35067 |
| `china-domain` | `6e658ba9a13e` | `421b7fb78ce3` | 111197 | 111224 |
| `china-ip` | `c00d29de109f` | `353bbbe9f956` | 9651 | 9648 |
| `category-ads-all` | `d2490d5d7147` | `10d224a50d48` | 910 | 910 |
| `connectivity-check` | `90d6616b58e9` | `f233a6decd94` | 27 | 28 |
| `category-scholar-!cn` | `37bbeece0e2d` | `d6b11ede6789` | 476 | 476 |

## Review checklist

- Inspect every changed rule file; do not approve based only on counts.
- Confirm unexpected deletions, policy-like entries, and major size changes.
- CI must compile MRS files and validate all generated configurations before merge.
