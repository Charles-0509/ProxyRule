# Upstream update report

Generated: `2026-11-09T11:28:02+00:00`

## Summary

- Changed sources: 28
- Failures: 0
- Warnings: 0

## Changes

| Source | Old SHA-256 | New SHA-256 | Old rules | New rules |
|---|---|---|---:|---:|
| `test` | `57a9b902ab3d` | `19c9272be350` | 61 | 62 |
| `openai` | `19d194277b7e` | `6aede2e962e4` | 22 | 24 |
| `github` | `e1c015908fae` | `d13336c90dca` | 64 | 66 |
| `x` | `e1b7735ec2af` | `7ad12e275c3b` | 27 | 28 |
| `facebook` | `f4bc4d117521` | `7bf95664c32f` | 396 | 397 |
| `amazon` | `019a5004d9d2` | `0d9d796059b2` | 246 | 247 |
| `apple` | `d59fa9ff98d7` | `9f8cf781c2c0` | 1792 | 1794 |
| `bing` | `76e566bc13d2` | `6b001003152c` | 40 | 41 |
| `microsoft` | `a085037143f2` | `d462cd85fce4` | 748 | 756 |
| `google-domain` | `f639665a2c02` | `4cc8758ad6da` | 1071 | 1078 |
| `google-ip` | `a0bbf374cbaa` | `cd2d3b360b38` | 8059 | 8426 |
| `tiktok` | `80ae73c96756` | `408348fbea47` | 36 | 40 |
| `netflix-domain` | `4cf3bf6f2b28` | `8df5a0903503` | 24 | 24 |
| `netflix-ip` | `4f8f67135cbb` | `409cee1a04e6` | 114 | 122 |
| `disney` | `8931d356f6fd` | `a116bc6b8b5d` | 224 | 224 |
| `spotify` | `f3e69f940cac` | `385c642d4b57` | 28 | 28 |
| `blizzard` | `a3abfb91bb72` | `0ccab4f1bb94` | 62 | 62 |
| `global` | `d82b216fde0b` | `6dbfdc192937` | 35028 | 35278 |
| `private-domain` | `10918636e35f` | `7f396a73bf5c` | 130 | 132 |
| `china-domain` | `6e658ba9a13e` | `f03c301bc6ef` | 111197 | 110177 |
| `china-ip` | `c00d29de109f` | `78c373bf4616` | 9651 | 9647 |
| `category-ads-all` | `d2490d5d7147` | `b03eb753f49c` | 910 | 908 |
| `connectivity-check` | `90d6616b58e9` | `f233a6decd94` | 27 | 28 |
| `dropbox` | `6e96f161ed76` | `0b79496b3fb1` | 16 | 25 |
| `paypal` | `3add0df2f1db` | `3b13b6dfcb94` | 245 | 245 |
| `cloudflare` | `adbbffbb8658` | `e9e9928f3b95` | 76 | 76 |
| `speedtest` | `53be15388001` | `f86908217750` | 13 | 20 |
| `category-scholar-!cn` | `37bbeece0e2d` | `6d68f84b1e71` | 476 | 466 |

## Review checklist

- Inspect every changed rule file; do not approve based only on counts.
- Confirm unexpected deletions, policy-like entries, and major size changes.
- CI must compile MRS files and validate all generated configurations before merge.
