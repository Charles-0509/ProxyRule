# Third-party notices

本仓库自己的脚本、配置生成器、测试和文档使用根目录的 MIT License。
第三方规则仍受各自许可证和版权约束，具体文件归属可在 `sources.json`
中逐项审计。

| 上游 | 用途 | 许可证状态 |
|---|---|---|
| `MetaCubeX/meta-rules-dat` | 可读 YAML 规则源 | GPL-3.0-only |
| `blackmatrix7/ios_rule_script` | classical 文本规则 | GPL-2.0-only |
| `liandu2024/clash` | classical 文本规则 | NOASSERTION |
| `pathfinder-yu/ProxyRule` | 银行规则 | NOASSERTION |

GPL 全文保存在 `LICENSES/`。许可证未知文件的说明见
`LICENSES/NOASSERTION.md`。本仓库没有把许可证未知内容重新许可为 MIT。

同步过程保存规范化后的上游数据以及 SHA-256，并不执行上游文件。自动
更新 PR 仍需要维护者逐项审核，技术审计不能替代版权授权。
