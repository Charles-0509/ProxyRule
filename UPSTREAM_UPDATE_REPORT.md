# Upstream update report

Generated: `2026-11-02T11:00:57+00:00`

## Summary

- Changed sources: 27
- Failures: 0
- Warnings: 0

## Changes

| Source | Old SHA-256 | New SHA-256 | Old rules | New rules |
|---|---|---|---:|---:|
| `test` | `57a9b902ab3d` | `19c9272be350` | 61 | 62 |
| `openai` | `19d194277b7e` | `6aede2e962e4` | 22 | 24 |
| `github` | `e1c015908fae` | `1c6b5790a087` | 64 | 65 |
| `facebook` | `f4bc4d117521` | `7bf95664c32f` | 396 | 397 |
| `amazon` | `019a5004d9d2` | `0d9d796059b2` | 246 | 247 |
| `apple` | `d59fa9ff98d7` | `a86d969aaeb1` | 1792 | 1793 |
| `bing` | `76e566bc13d2` | `6b001003152c` | 40 | 41 |
| `microsoft` | `a085037143f2` | `4d4b8a1d0957` | 748 | 755 |
| `google-domain` | `f639665a2c02` | `a87ffd5d32df` | 1071 | 1078 |
| `google-ip` | `a0bbf374cbaa` | `a76acd5d076b` | 8059 | 8559 |
| `tiktok` | `80ae73c96756` | `408348fbea47` | 36 | 40 |
| `netflix-domain` | `4cf3bf6f2b28` | `8df5a0903503` | 24 | 24 |
| `netflix-ip` | `4f8f67135cbb` | `409cee1a04e6` | 114 | 122 |
| `disney` | `8931d356f6fd` | `21fee1a588ef` | 224 | 224 |
| `spotify` | `f3e69f940cac` | `385c642d4b57` | 28 | 28 |
| `blizzard` | `a3abfb91bb72` | `0ccab4f1bb94` | 62 | 62 |
| `global` | `d82b216fde0b` | `6dbfdc192937` | 35028 | 35278 |
| `private-domain` | `10918636e35f` | `7f396a73bf5c` | 130 | 132 |
| `china-domain` | `6e658ba9a13e` | `f03c301bc6ef` | 111197 | 110177 |
| `china-ip` | `c00d29de109f` | `1e38f21f823f` | 9651 | 10012 |
| `category-ads-all` | `d2490d5d7147` | `e73d0b7051a3` | 910 | 904 |
| `connectivity-check` | `90d6616b58e9` | `f233a6decd94` | 27 | 28 |
| `dropbox` | `6e96f161ed76` | `0b79496b3fb1` | 16 | 25 |
| `paypal` | `3add0df2f1db` | `3b13b6dfcb94` | 245 | 245 |
| `cloudflare` | `adbbffbb8658` | `e9e9928f3b95` | 76 | 76 |
| `speedtest` | `53be15388001` | `f86908217750` | 13 | 20 |
| `category-scholar-!cn` | `37bbeece0e2d` | `f8b46c3ecc5a` | 476 | 466 |

## Review checklist

- Inspect every changed rule file; do not approve based only on counts.
- Confirm unexpected deletions, policy-like entries, and major size changes.
- CI must compile MRS files and validate all generated configurations before merge.
