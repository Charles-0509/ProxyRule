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
3. 把 `CHANGE_ME_TO_A_UNIQUE_LONG_RANDOM_SECRET` 换成每台路由器独有的长随机密码。
4. 不要把填入真实订阅和密码后的配置上传到 GitHub、网盘或聊天群。

之后在 OpenClash 中使用当前稳定 Mihomo 内核导入配置，选择 Rule 模式并
启动。首次加载时先下载机场节点，再刷新规则 provider；GitHub 规则下载会
自动走“规则更新”策略组，不依赖 `gh-proxy` 等第三方镜像。

## 默认流量行为

- 私网、银行、Apple Push、NTP、连接检测和中国大陆域名/IP：直连。
- ApplePush 在面板中有独立策略组，默认直连，也可以临时切换到任意故转组或节点。
- `Bing & Rewards`：Bing 搜索与 Microsoft Rewards 的独立策略组，默认直连；它只包含
  Bing、Rewards 页面及其登录所需域名，不改变 Windows、Office、OneDrive 等其他 Microsoft
  服务的既有分流。若 Rewards 的地区或登录页需要其他出口，可在 Zashboard 手动切换该组。
- `Steam社区`：Steam 商店、社区、好友、聊天、账户及连接管理流量，默认走“手动选择”。
  其中包括 `steampowered.com`、`steamcommunity.com`、`steam-chat.com` 和
  `steamserver.net` 等在中国大陆可能被阻断或污染的域名。
- `Steam下载`：游戏内容与中国大陆下载 CDN，默认直连，包括 `steamcontent.com`、
  `dl.steam.clngaa.com`、`st.dl.bscstorage.net` 等域名及单独维护的 CDN IPv4 网段。
  社区规则排在下载域名和下载 IP 规则之前，避免登录、好友连接被共享 Valve 网段误导向直连。
  社区侧没有加入宽泛静态 IP 段，因为 Steam CM 主机和下载 CDN 会共享或动态变更地址；
  在 Fake-IP、域名嗅探和规则优先级配合下，按域名分流更稳妥。
- `*.edu.cn` 和 `*.zfye.site`：无条件直连，优先级高于广告和代理规则。
- 广告规则：拒绝，可在“广告拦截”组临时切换为直连排查误杀。
- AI、GitHub、Telegram、社交、流媒体、游戏等：使用各自策略组。
- `学术期刊网站`：原“学术”统一更名，不拆分平台；Google Scholar、IEEE、ACM、
  Elsevier、Springer Nature 等保留在同一组，并优先于 Google/Gemini 通用规则。
  国内学术清单和补充规则优先进入“国内”，包括知网、万方、维普、超星、读秀、
  国家哲学社会科学学术期刊数据库和库客；同步使用直连 DoH 和真实 IP。
  按平台归属分类，不把所有 `.cn` 域名或“国内可访问”的国外平台都视作国内学术。
- `游戏平台`：原“游戏”更名，继续统一控制 NVIDIA、Epic、EA、Battle.net、Ubisoft、
  PlayStation 和 Nintendo；Steam社区、Steam下载的独立分流保留。
- `GitLab`、`Docker`：从“开发工具”拆出；`Notion`、`Slack`、`Zoom`：从“办公协作”拆出。
  原“流媒体”实际只挂载 `popcorn.plus`，现在更名为 `Popcorn`。加密货币保持统一分组。
- `Gemini`：从 AI 中独立，沿用仓库的 `gemini.list`，优先于 Google 通用规则。
  默认“手动选择”；如果该组当前的美国出口无法访问 Google，请在 Gemini 组中
  单独选择已验证可用的节点或地区，不必改变 OpenAI 等其他 AI 服务的出口。
  现有规则包含部分 Google 共享端点；通用 Google 登录等请求仍由 `Google` 组控制。
- `Apple Intelligence`：按用户提供的 19 条域名规则独立分流，默认“直连”，
  可在面板切换到 Azure、手动选择或地区故转组。规则优先于国内、Apple 和
  Cloudflare 通用规则；仅 `smoot.apple.com` 匹配所有子域，其余使用精确域名。
  这些域名同时涉及 Siri、iCloud 和位置服务等，分组并不意味着它们只服务于 AI。
  配置同时保留真实 IP 与直连 DoH，避免代理不可用时默认直连仍依赖代理 DNS。
  可读规则集中维护于 [`apple-intelligence.yaml`](rules/source/domain/apple-intelligence.yaml)，
  编译为 `rules/mrs/domain/apple-intelligence.mrs`，配置通过本仓库的 GitHub
  rule-provider 下载；分流、DNS 与 Fake-IP 例外均引用该规则集，无需手改三处域名清单。
- Telegram 在上游 GeoIP 之外保留经本地运行日志确认的窄范围 `/32` 补充规则，
  避免新端点落入最终兜底后在中国大陆直连超时。
- 未分类境外流量和最终兜底：默认使用“手动选择”。
- IPv6：默认关闭，避免节点或网络不完整时发生旁路和泄漏。

所有节点及每个地区都只提供手动、自动测速和故障转移组。所有代理业务默认
选择“手动选择”，它默认使用“美国-故转”，可在 Zashboard 中切换地区。
所选地区全部不可用时会优先交给“所有-自动”选择其他可用节点。
台湾过滤不包含中国大陆国旗，美国和
英国缩写使用单词边界，避免 `RUS`、品牌名称等常见误判。

Zashboard 文件夹属于浏览器本地设置。导入
[Zashboard 设置文件](config/zashboard-settings.json) 后，代理页会显示“策略组”、
“故障转移”和“节点组”三个标签，详见
[Zashboard 文件夹说明](docs/zashboard-folders.md)。

## DNS 与 TUN

Fake-IP 主配置使用 `198.18.0.1/16`、国内加密 DNS、节点域名专用 DNS、
规则感知 DNS、TCP/UDP 53 劫持和真实 IP 兼容清单。TUN 同时启用
`auto-route` 与 Linux 所需的 `auto-redirect`，并启用严格路由。

DNS 上游全部使用 HTTPS，未配置 `system`、明文 UDP/TCP 或失败后的明文回退：

- 启动解析与节点域名解析：阿里 DNS `223.5.5.5`、DNSPod `1.12.12.12`
  的 IP 地址形式 DoH，节点解析不依赖代理节点已连接，避免循环依赖。
- 国内、银行、Apple 中国服务、Bing/Rewards、Steam 下载等已列明的直连域名：
  国内 DoH 直连。实际 DIRECT 出口的域名也使用国内 DoH，且不跟随代理 DNS 策略。
- 其余域名：Cloudflare/Google 的 IP 地址形式 DoH，通过“手动选择”出口访问。
  DNS 提供商仍能看到查询；国内直连查询有意交给国内提供商，不以检测页面
  是否显示国内 DNS 作为唯一的泄漏判定。代理不可用时不自动改为本地明文解析。
- `respect-rules` 保持开启，明确指定 `#DIRECT`/`#手动选择` 的 DNS 连接按指定出口走。
  `prefer-h3` 关闭，不把 Loon 的 DoH3/DoQ 配置直接搬入核心。

OpenClash“增强”模式下，YAML 的 `tun.dns-hijack` 并不会单独建立系统防火墙规则。
应在 OpenClash 启用本地 DNS 劫持，让 dnsmasq 转发到 `127.0.0.1#7874`，
并确认 LAN 客户端的网关和 DNS 指向软路由；其他解析插件不应形成循环转发。
保持 LAN IPv6 分配与核心的 IPv6 设置一致，避免客户端经上级路由的 IPv6 绕过代理。

此方案控制经过 Mihomo 的 DNS；应用自带的 DoH/HTTPDNS（尤其 HTTPS 443）不能
仅凭 53 端口劫持完全接管。Loon 的 `Prevent_DNS_Leaks` 当前只将检测站点代理，
并非通用 DNS 防泄漏。它的 `Block_HTTPDNS` 含 URL/UA/MITM 与共享 IP 规则，
因此未整包移植或默认封锁所有 853/443 端口。浏览器安全 DNS、Android 私人 DNS、
其他 VPN/Tailscale 应单独检查；不要为让检测站点“全绿”而强制所有国内 DNS 出境。
首次启动应等待规则 provider 全部加载完成后再测 DNS；监听端口先就绪并不代表
规则集已经可用，过早查询可能得到尚未套用例外规则的 Fake-IP。

参考：[Mihomo DNS](https://wiki.metacubex.one/config/dns/)、
[Mihomo TUN DNS 劫持](https://wiki.metacubex.one/config/inbound/tun/)、
[Loon DNS 回退逻辑](https://nsloon.app/docs/DNS/)。

Cloudflare Tunnel 的 `argotunnel.com`、`cftunnel.com` 返回真实 IP，并优先
直连。OpenClash 的 `DIRECT` 仍经过核心转发；如需让 Tunnel 不受核心重启影响，
还需在路由器的目标 IP 绕过列表（`wan_ac_black_ips`）中加入
[Cloudflare 公布的 Tunnel 边缘地址](https://developers.cloudflare.com/cloudflare-one/networks/connectors/cloudflare-tunnel/configure-tunnels/tunnel-with-firewall/)，
随后重启 cloudflared，验证 DNS、实际套接字及防火墙绕过规则。

OpenWrt 至少应具备 TUN、完整 IP 工具和 nftables/firewall4 支持。不同固件
的软件包名称可能不同；启动失败时优先检查 OpenClash 日志中的缺失内核模块、
路由表和 nftables 错误。

IPv6 只有在运营商、WAN、LAN DNS、防火墙及所选代理节点全部通过测试后才
应启用。可参考 [IPv6 覆盖片段](examples/ipv6-overlay.yaml)，合并后还要验证：

- 国内和境外 IPv6 地址均按预期分流；
- `fc00::/7`、`fe80::/10` 和组播地址保持直连；
- 关闭代理后没有境外 IPv6 旁路。

## 安全设置

控制器默认绑定 `0.0.0.0:9090` 并允许私有网络跨域请求，便于 Zashboard 从
局域网连接 `路由器LAN地址:9090`。配置中的密码只是公开占位符，导入前必须
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
- **代理默认地区不对**：清理旧的策略组选择缓存；新配置的代理组第一项是“美国-故转”。
- **游戏或智能家居异常**：先切换 Redir-Host 兼容版，再把最小必要域名加入
  `rules/source/domain/compatibility.yaml`。
- **DNS 解析失败**：确认 53 端口劫持没有和 AdGuard Home、SmartDNS 等重复，
  并保证其监听链路只有一个明确入口。
- **GitHub 规则更新失败**：确认“规则更新”组有可用节点，并检查路由器时间；
  TLS 在系统时间错误时会失败。
- **配置更新后行为未变化**：刷新 rule provider、清空 Mihomo DNS/Fake-IP 缓存并重启核心。
- **节点实际可用但 Zashboard 测速全超时**：这通常是旧 Zashboard 与新版 Mihomo
  provider API 不兼容。按[修复 Zashboard 节点测速超时](docs/zashboard-mihomo-api-fix.md)
  更新前端，无需修改订阅或节点配置。
- **升级 3x-ui 后仅 VLESS Reality 失效**：如果 Xray-core `26.7.11` 配合
  Mihomo `1.19.28` 出现 `REALITY authentication failed`，参考
  [Reality 兼容性说明](docs/3x-ui-reality-mihomo-compatibility.md)。

## 许可证

自有脚本、配置生成器、测试和文档使用 MIT License。第三方规则分别使用
GPL-2.0、GPL-3.0 或许可证未知状态，详见 [NOTICE](NOTICE.md)、`LICENSES/`
和 `sources.json`。许可证未知不代表可自由再分发。
