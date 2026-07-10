# ProxyRule：可审计的中国大陆 OpenClash 配置

这套配置面向运行 OpenClash/Mihomo 的 OpenWrt 软路由。目标不是盲目追随
第三方规则，而是把规则源码、构建过程、审核记录和发布版本全部放在自己
可控的 GitHub 仓库中。

## 直接使用

推荐下载 [Fake-IP 稳定版](config/openclash-stable.yaml)。遇到智能家居、
老旧游戏、DDNS 或特殊应用兼容问题时，可以改用
[Redir-Host 兼容版](config/openclash-redir-host.yaml)。

使用前必须编辑配置顶部：

1. 把 `provider1` 的 `replace-with-provider-1-subscription` 换成自己的机场订阅。
2. 有第二个机场时替换 `provider2`；没有时删除整个 `provider2` 段，避免无效请求日志。
3. 不要把填入真实订阅后的配置上传到 GitHub、网盘或聊天群。

之后在 OpenClash 中使用当前稳定 Mihomo 内核导入配置，选择 Rule 模式并
启动。首次加载时先下载机场节点，再刷新规则 provider；GitHub 规则下载会
自动走“规则更新”策略组，不依赖 `gh-proxy` 等第三方镜像。

## 默认流量行为

- 私网、银行、Apple Push、NTP、连接检测和中国大陆域名/IP：直连。
- 广告规则：拒绝，可在“广告拦截”组临时切换为直连排查误杀。
- AI、GitHub、Telegram、社交、流媒体、游戏等：使用各自策略组。
- 未分类境外流量和最终兜底：默认使用“节点选择”。
- IPv6：默认关闭，避免节点或网络不完整时发生旁路和泄漏。

每个地区同时有手动组和自动测速组。台湾过滤不包含中国大陆国旗，美国和
英国缩写使用单词边界，避免 `RUS`、品牌名称等常见误判。

## DNS 与 TUN

Fake-IP 主配置使用 `198.18.0.1/16`、国内加密 DNS、节点域名专用 DNS、
规则感知 DNS、TCP/UDP 53 劫持和真实 IP 兼容清单。TUN 同时启用
`auto-route` 与 Linux 所需的 `auto-redirect`，并启用严格路由。

OpenWrt 至少应具备 TUN、完整 IP 工具和 nftables/firewall4 支持。不同固件
的软件包名称可能不同；启动失败时优先检查 OpenClash 日志中的缺失内核模块、
路由表和 nftables 错误。

IPv6 只有在运营商、WAN、LAN DNS、防火墙及所选代理节点全部通过测试后才
应启用。可参考 [IPv6 覆盖片段](examples/ipv6-overlay.yaml)，合并后还要验证：

- 国内和境外 IPv6 地址均按预期分流；
- `fc00::/7`、`fe80::/10` 和组播地址保持直连；
- 关闭代理后没有境外 IPv6 旁路。

## 安全设置

控制器默认绑定 `127.0.0.1:9090`，共享模板不包含公共默认密码。如需从 LAN
直接访问 API，参考 [LAN 面板覆盖片段](examples/lan-dashboard-overlay.yaml)，
为每台设备生成不同的长随机密码，并确认 WAN 防火墙没有开放以下端口：

- 7890：Mixed 代理
- 7892：Redirect
- 7895：TProxy
- 7874：Mihomo DNS
- 9090：控制器 API

## 稳定版、锁定版和离线包

- `main` 稳定版只跟随人工审核后合并的规则，适合自动更新。
- GitHub Release 中的 pinned 配置把所有 URL 固定到版本标签，适合最高可控性。
- Release 同时提供 ZIP、tar.gz 和 `SHA256SUMS`，可用于无 GitHub 初始网络的
  离线部署和完整回滚。

离线复制时，配置中的 provider 缓存路径位于 Mihomo HomeDir 下的
`rule_provider/proxyrule/`。OpenClash 通常使用 `/etc/openclash` 作为 HomeDir，
但应以本机启动日志为准。

## 规则维护流程

`sources.json` 是规则供应链清单，记录来源、固定分支、格式、行为、许可证、
大小上限、规则数量和 SHA-256。

```bash
make sync       # 抓取候选更新并生成审计报告
make validate   # 只验证已提交源码和哈希
make build      # 从 YAML 编译 MRS
make generate   # 重新生成公开配置
make test       # 运行测试并调用固定版本 Mihomo 校验
```

每周自动任务只更新 `automation/upstream-sync` 分支并创建 PR。必须检查
`UPSTREAM_UPDATE_REPORT.md` 和每一处规则差异，CI 通过后再人工合并。它不会
自动合并，也不会自动发布 Release。

发布锁定版本需在 GitHub Actions 手动运行“Publish an immutable reviewed
release”，输入例如 `v2026.07.10`。本地也可以执行：

```bash
make package TAG=v2026.07.10
```

## 常见故障

- **首次没有规则**：确认机场 provider 已成功下载节点，然后手动刷新规则；
  必要时使用 Release 离线包。
- **国内网站走代理**：检查“国内”是否仍以“直连”为第一项，并清理旧的策略组选择缓存。
- **游戏或智能家居异常**：先切换 Redir-Host 兼容版，再把最小必要域名加入
  `rules/source/domain/compatibility.yaml`。
- **DNS 解析失败**：确认 53 端口劫持没有和 AdGuard Home、SmartDNS 等重复，
  并保证其监听链路只有一个明确入口。
- **GitHub 规则更新失败**：确认“规则更新”组有可用节点，并检查路由器时间；
  TLS 在系统时间错误时会失败。
- **配置更新后行为未变化**：刷新 rule provider、清空 Mihomo DNS/Fake-IP 缓存并重启核心。

## 许可证

自有脚本、配置生成器、测试和文档使用 MIT License。第三方规则分别使用
GPL-2.0、GPL-3.0 或许可证未知状态，详见 [NOTICE](NOTICE.md)、`LICENSES/`
和 `sources.json`。许可证未知不代表可自由再分发。
