#!/usr/bin/env python3
"""Generate stable, compatibility, pinned, and fully local test configs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO_RAW = "https://raw.githubusercontent.com/Charles-0509/ProxyRule"
TEST_URL = "https://www.gstatic.com/generate_204"

# Telegram Desktop was observed using this endpoint on 2026-07-16.  It is not
# present in MetaCubeX's Telegram GeoIP data, so keep the narrow /32 override
# ahead of the upstream rule-set instead of broadening the catch-all policy.
TELEGRAM_OBSERVED_IPS = ["194.221.250.50/32"]

REGIONS = [
    ("香港", r"(?i)(香港|Hong\s*Kong|\bHK\b|🇭🇰)"),
    ("台湾", r"(?i)(台湾|台灣|Tai\s*Wan|Taiwan|\bTW\b|🇹🇼)"),
    ("日本", r"(?i)(日本|东京|東京|大阪|Japan|\bJP\b|🇯🇵)"),
    ("新加坡", r"(?i)(新加坡|狮城|獅城|Singapore|\bSG\b|🇸🇬)"),
    ("韩国", r"(?i)(韩国|韓國|首尔|首爾|Korea|\bKR\b|🇰🇷)"),
    ("美国", r"(?i)(美国|美國|洛杉矶|洛杉磯|圣何塞|聖何塞|西雅图|西雅圖|纽约|紐約|United\s*States|\bUSA?\b|🇺🇸)"),
    ("英国", r"(?i)(英国|英國|伦敦|倫敦|United\s*Kingdom|\bUK\b|🇬🇧)"),
]

OTHER_FILTER = (
    r"(?i)^(?!.*(?:香港|Hong\s*Kong|\bHK\b|🇭🇰|台湾|台灣|Tai\s*Wan|Taiwan|\bTW\b|🇹🇼|"
    r"日本|东京|東京|大阪|Japan|\bJP\b|🇯🇵|新加坡|狮城|獅城|Singapore|\bSG\b|🇸🇬|"
    r"韩国|韓國|首尔|首爾|Korea|\bKR\b|🇰🇷|美国|美國|洛杉矶|洛杉磯|圣何塞|聖何塞|"
    r"西雅图|西雅圖|纽约|紐約|United\s*States|\bUSA?\b|🇺🇸|英国|英國|伦敦|倫敦|"
    r"United\s*Kingdom|\bUK\b|🇬🇧)).*$"
)


def q(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


def provider_block(manifest: dict, ref: str, local_rules: bool) -> str:
    lines = ["rule-providers:"]
    for entry in manifest["sources"]:
        lines.append(f"  {entry['id']}:")
        if local_rules:
            lines += [
                "    type: file",
                f"    behavior: {entry['behavior']}",
                f"    format: {entry['runtime_format']}",
                f"    path: {q(str(ROOT / entry['runtime_path']))}",
            ]
        else:
            runtime_path = entry["runtime_path"]
            suffix = Path(runtime_path).suffix
            lines += [
                "    type: http",
                f"    behavior: {entry['behavior']}",
                f"    format: {entry['runtime_format']}",
                f"    path: {q('./rule_provider/proxyrule/' + entry['id'] + suffix)}",
                f"    url: {q(f'{REPO_RAW}/{ref}/{runtime_path}')}",
                "    interval: 86400",
                "    proxy: 规则更新",
                f"    size-limit: {entry['max_size']}",
            ]
    return "\n".join(lines)


def subscription_block(test_mode: bool) -> str:
    if test_mode:
        nodes = [
            "香港测试", "台湾测试", "日本测试", "新加坡测试", "韩国测试", "美国测试", "英国测试", "法国测试"
        ]
        proxy_lines = ["proxy-providers: {}", "", "proxies:", "  - { name: 直连, type: direct, udp: true }", "  - { name: 拒绝, type: reject }"]
        proxy_lines += [
            f"  - {{ name: {name}, type: socks5, server: 127.0.0.1, port: 9, udp: true }}" for name in nodes
        ]
        return "\n".join(proxy_lines)
    return f"""proxy-providers:
  provider1:
    type: http
    url: 'https://example.invalid/replace-with-provider-1-subscription'
    path: ./proxy_provider/provider1.yaml
    interval: 86400
    proxy: 直连
    filter: '(?i)^(?!.*(?:官网|套餐|流量|剩余|到期|过期|客服|网址|通知|更新|客户端|倍率说明)).*$'
    health-check:
      enable: true
      lazy: true
      url: {TEST_URL}
      interval: 300
      expected-status: 204
    override:
      additional-prefix: '[P1] '
  provider2:
    type: http
    url: 'https://example.invalid/replace-with-provider-2-subscription'
    path: ./proxy_provider/provider2.yaml
    interval: 86400
    proxy: 直连
    filter: '(?i)^(?!.*(?:官网|套餐|流量|剩余|到期|过期|客服|网址|通知|更新|客户端|倍率说明)).*$'
    health-check:
      enable: true
      lazy: true
      url: {TEST_URL}
      interval: 300
      expected-status: 204
    override:
      additional-prefix: '[P2] '

proxies:
  - {{ name: 直连, type: direct, udp: true }}
  - {{ name: 拒绝, type: reject }}"""


def group_mapping(name: str, proxies: list[str]) -> list[str]:
    unique_proxies = list(dict.fromkeys(proxies))
    return [f"  - name: {name}", "    type: select", "    proxies:"] + [f"      - {item}" for item in unique_proxies]


def groups_block() -> str:
    lines = ["proxy-groups:"]
    all_filter = r"(?i)^(?!(?:直连|拒绝)$).+"
    lines += [
        "  - name: 所有-手动", "    type: select", "    include-all: true", f"    filter: {q(all_filter)}",
        "  - name: 所有-自动", "    type: url-test", "    include-all: true", f"    filter: {q(all_filter)}",
        f"    url: {TEST_URL}", "    interval: 300", "    tolerance: 50", "    lazy: true",
    ]
    for name, regex in REGIONS:
        lines += [
            f"  - name: {name}-手动", "    type: select", "    include-all: true", f"    filter: {q(regex)}",
            f"  - name: {name}-自动", "    type: url-test", "    include-all: true", f"    filter: {q(regex)}",
            f"    url: {TEST_URL}", "    interval: 300", "    tolerance: 50", "    lazy: true",
        ]
    lines += [
        "  - name: 其他地区-手动", "    type: select", "    include-all: true", f"    filter: {q(OTHER_FILTER)}",
        "  - name: 其他地区-自动", "    type: url-test", "    include-all: true", f"    filter: {q(OTHER_FILTER)}",
        f"    url: {TEST_URL}", "    interval: 300", "    tolerance: 50", "    lazy: true",
    ]
    region_names = [name for name, _ in REGIONS] + ["其他地区"]
    lines += ["  - name: 所有-故转", "    type: fallback", "    proxies:", "      - 所有-手动", "      - 所有-自动"]
    lines += [f"    url: {TEST_URL}", "    interval: 300", "    lazy: true"]
    for name in region_names:
        lines += [
            f"  - name: {name}-故转", "    type: fallback", "    proxies:",
            f"      - {name}-手动", f"      - {name}-自动", "      - 所有-自动",
        ]
        lines += [f"    url: {TEST_URL}", "    interval: 300", "    lazy: true"]
    fallbacks = [f"{name}-故转" for name in region_names]
    lines += group_mapping("手动选择", ["美国-故转", "香港-故转", "台湾-故转", "日本-故转", "新加坡-故转", "韩国-故转", "英国-故转", "其他地区-故转", "所有-故转"])
    lines += group_mapping("规则更新", ["手动选择", "所有-故转", "所有-自动", "直连"])
    service_choices = ["手动选择", "所有-故转"] + fallbacks + ["所有-手动", "所有-自动", "直连", "拒绝"]
    service_groups = [
        "AI", "GitHub", "开发工具", "Cloudflare", "Telegram", "Discord", "WhatsApp", "X",
        "Facebook", "Instagram", "Reddit", "TikTok", "YouTube", "Netflix", "Disney+", "HBO",
        "Amazon", "Crunchyroll", "流媒体", "Spotify", "游戏", "Apple", "Bing & Rewards", "Microsoft", "OneDrive",
        "Google", "办公协作", "Dropbox", "LinkedIn", "PayPal", "学术", "测速", "加密货币", "国外", "其他",
    ]
    for name in service_groups:
        choices = ["直连"] + service_choices if name == "Bing & Rewards" else service_choices
        lines += group_mapping(name, choices)
    lines += group_mapping("ApplePush", ["直连", "手动选择", "所有-故转"] + fallbacks + ["所有-手动", "所有-自动", "拒绝"])
    lines += group_mapping("国内", ["直连", "手动选择", "所有-自动"])
    lines += group_mapping("广告拦截", ["拒绝", "直连", "手动选择"])
    return "\n".join(lines)


def dns_block(enhanced_mode: str) -> str:
    fake = ""
    if enhanced_mode == "fake-ip":
        fake = """
  fake-ip-range: 198.18.0.1/16
  fake-ip-filter-mode: rule
  fake-ip-filter:
    - RULE-SET,private-domain,real-ip
    - RULE-SET,china-domain,real-ip
    - RULE-SET,connectivity-check,real-ip
    - RULE-SET,category-ntp,real-ip
    - RULE-SET,apple-push,real-ip
    - RULE-SET,compatibility,real-ip
    - MATCH,fake-ip"""
    policy_ids = ["private-domain", "china-domain", "connectivity-check", "category-ntp", "apple-push", "compatibility"]
    policy_lines: list[str] = []
    for ident in policy_ids:
        policy_lines += [
            f"    'rule-set:{ident}':",
            "      - https://dns.alidns.com/dns-query",
            "      - https://doh.pub/dns-query",
        ]
    return f"""dns:
  enable: true
  listen: 0.0.0.0:7874
  ipv6: false
  cache-algorithm: arc
  enhanced-mode: {enhanced_mode}{fake}
  default-nameserver:
    - 223.5.5.5
    - 119.29.29.29
  nameserver:
    - https://dns.alidns.com/dns-query
    - https://doh.pub/dns-query
  proxy-server-nameserver:
    - https://dns.alidns.com/dns-query
    - https://doh.pub/dns-query
  direct-nameserver:
    - https://dns.alidns.com/dns-query
    - https://doh.pub/dns-query
  direct-nameserver-follow-policy: true
  respect-rules: true
  nameserver-policy:
{chr(10).join(policy_lines)}"""


def rules_block() -> str:
    rules = [
        "DOMAIN-SUFFIX,lan,国内", "DOMAIN-SUFFIX,local,国内", "DOMAIN-SUFFIX,home.arpa,国内",
        "DOMAIN-SUFFIX,edu.cn,国内", "DOMAIN-SUFFIX,zfye.site,国内",
        "IP-CIDR,127.0.0.0/8,国内,no-resolve", "IP-CIDR,10.0.0.0/8,国内,no-resolve",
        "IP-CIDR,100.64.0.0/10,国内,no-resolve", "IP-CIDR,169.254.0.0/16,国内,no-resolve",
        "IP-CIDR,172.16.0.0/12,国内,no-resolve", "IP-CIDR,192.168.0.0/16,国内,no-resolve",
        "IP-CIDR,224.0.0.0/4,国内,no-resolve",
        "IP-CIDR6,::1/128,国内,no-resolve", "IP-CIDR6,fc00::/7,国内,no-resolve",
        "IP-CIDR6,fe80::/10,国内,no-resolve", "IP-CIDR6,ff00::/8,国内,no-resolve",
        "RULE-SET,bank,国内", "RULE-SET,compatibility,国内", "RULE-SET,private-domain,国内",
        "RULE-SET,category-ads-all,广告拦截", "RULE-SET,block,广告拦截",
        "RULE-SET,apple-push,ApplePush", "RULE-SET,connectivity-check,国内", "RULE-SET,category-ntp,国内",
        "RULE-SET,test,测速", "RULE-SET,speedtest,测速",
        "RULE-SET,openai,AI", "RULE-SET,claude,AI", "RULE-SET,meta-ai,AI", "RULE-SET,perplexity,AI",
        "RULE-SET,copilot,AI", "RULE-SET,gemini,AI", "RULE-SET,groq,AI", "RULE-SET,grok,AI",
        "RULE-SET,github,GitHub",
        "RULE-SET,gitlab,开发工具", "RULE-SET,bing,Bing & Rewards", "RULE-SET,microsoft-rewards,Bing & Rewards",
        "RULE-SET,docker,开发工具", "RULE-SET,cloudflare,Cloudflare",
        "RULE-SET,telegram-domain,Telegram",
        *(f"IP-CIDR,{cidr},Telegram,no-resolve" for cidr in TELEGRAM_OBSERVED_IPS),
        "RULE-SET,telegram-ip,Telegram,no-resolve",
        "RULE-SET,discord,Discord", "RULE-SET,whatsapp,WhatsApp", "RULE-SET,x,X",
        "RULE-SET,facebook,Facebook", "RULE-SET,instagram,Instagram", "RULE-SET,reddit,Reddit",
        "RULE-SET,apple-cn,国内", "RULE-SET,apple,Apple", "RULE-SET,apple-custom,Apple",
        "RULE-SET,microsoft,Microsoft", "RULE-SET,onedrive,OneDrive", "RULE-SET,dropbox,Dropbox",
        "RULE-SET,google-domain,Google", "RULE-SET,google-ip,Google,no-resolve",
        "RULE-SET,notion,办公协作", "RULE-SET,slack,办公协作", "RULE-SET,zoom,办公协作",
        "RULE-SET,linkedin,LinkedIn", "RULE-SET,paypal,PayPal", "RULE-SET,category-scholar-!cn,学术",
        "RULE-SET,okx,加密货币", "RULE-SET,bybit,加密货币", "RULE-SET,binance,加密货币",
        "RULE-SET,bilibili,国内", "RULE-SET,youtube,YouTube", "RULE-SET,tiktok,TikTok",
        "RULE-SET,netflix-domain,Netflix", "RULE-SET,netflix-ip,Netflix,no-resolve", "RULE-SET,disney,Disney+",
        "RULE-SET,amazon,Amazon", "RULE-SET,crunchyroll,Crunchyroll", "RULE-SET,popcorn,流媒体", "RULE-SET,hbo,HBO",
        "RULE-SET,spotify,Spotify",
        "RULE-SET,nvidia,游戏", "RULE-SET,steam,游戏", "RULE-SET,epic,游戏", "RULE-SET,ea,游戏",
        "RULE-SET,blizzard,游戏", "RULE-SET,ubi,游戏", "RULE-SET,playstation,游戏", "RULE-SET,nintendo,游戏",
        "RULE-SET,direct,国内", "RULE-SET,china-domain,国内", "RULE-SET,china-ip,国内,no-resolve",
        "RULE-SET,proxy,国外", "RULE-SET,global,国外", "MATCH,其他",
    ]
    return "rules:\n" + "\n".join(f"  - {rule}" for rule in rules)


def render(manifest: dict, enhanced_mode: str, ref: str, test_mode: bool) -> str:
    store_fake = "true" if enhanced_mode == "fake-ip" else "false"
    header = f"""# Generated by scripts/generate_configs.py. Edit the generator, not this file.
# Replace the provider subscription placeholder URLs before use.

{subscription_block(test_mode)}

mixed-port: 7890
redir-port: 7892
tproxy-port: 7895
allow-lan: true
mode: rule
log-level: info
ipv6: false
unified-delay: true
tcp-concurrent: true
external-controller: 0.0.0.0:9090
external-controller-cors:
  allow-origins:
    - '*'
  allow-private-network: true
secret: 'CHANGE_ME_TO_A_UNIQUE_LONG_RANDOM_SECRET'

profile:
  store-selected: true
  store-fake-ip: {store_fake}

sniffer:
  enable: true
  force-dns-mapping: true
  parse-pure-ip: true
  override-destination: true
  sniff:
    HTTP:
      ports: [80, 8080-8880]
      override-destination: true
    TLS:
      ports: [443, 8443]
    QUIC:
      ports: [443, 8443]
  skip-domain:
    - Mijia Cloud
    - '+.push.apple.com'
    - '+.lan'
    - '+.local'

tun:
  enable: true
  stack: mixed
  device: utun
  dns-hijack:
    - any:53
    - tcp://any:53
  auto-route: true
  auto-redirect: true
  auto-detect-interface: true
  strict-route: true
  endpoint-independent-nat: false

{dns_block(enhanced_mode)}

{groups_block()}

{rules_block()}

{provider_block(manifest, ref, test_mode)}
"""
    return header


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ref", default="main")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "config")
    parser.add_argument("--test-mode", action="store_true")
    parser.add_argument("--prefix", default="openclash")
    args = parser.parse_args()
    manifest = json.loads((ROOT / "sources.json").read_text(encoding="utf-8"))
    args.output_dir.mkdir(parents=True, exist_ok=True)
    if args.test_mode:
        path = args.output_dir / "openclash-test.yaml"
        path.write_text(render(manifest, "fake-ip", args.ref, True), encoding="utf-8")
        print(path)
        return 0
    outputs = [
        (args.output_dir / f"{args.prefix}-stable.yaml", "fake-ip"),
        (args.output_dir / f"{args.prefix}-redir-host.yaml", "redir-host"),
    ]
    for path, mode in outputs:
        path.write_text(render(manifest, mode, args.ref, False), encoding="utf-8")
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
