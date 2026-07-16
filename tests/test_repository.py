#!/usr/bin/env python3

from __future__ import annotations

import importlib.util
import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_generator():
    spec = importlib.util.spec_from_file_location("generate_configs", ROOT / "scripts/generate_configs.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(module)
    return module


GENERATOR = load_generator()


class RepositoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads((ROOT / "sources.json").read_text(encoding="utf-8"))
        cls.stable = (ROOT / "config/openclash-stable.yaml").read_text(encoding="utf-8")
        cls.redir = (ROOT / "config/openclash-redir-host.yaml").read_text(encoding="utf-8")

    def test_manifest_ids_and_paths_are_unique(self):
        sources = self.manifest["sources"]
        self.assertEqual(71, len(sources))
        for key in ["id", "source_path", "runtime_path"]:
            values = [item[key] for item in sources]
            if key == "runtime_path":
                # Text providers intentionally use their source as the runtime file.
                values = [f"{item['id']}:{item[key]}" for item in sources]
            self.assertEqual(len(values), len(set(values)), key)
        self.assertGreaterEqual(sum(item["runtime_format"] == "mrs" for item in sources), 35)

    def test_manifest_files_and_hashes_exist(self):
        for item in self.manifest["sources"]:
            self.assertRegex(item["sha256"], r"^[0-9a-f]{64}$", item["id"])
            self.assertGreater(item["line_count"], 0, item["id"])
            self.assertTrue((ROOT / item["source_path"]).is_file(), item["source_path"])
            self.assertTrue((ROOT / item["runtime_path"]).is_file(), item["runtime_path"])

    def test_runtime_configs_only_use_owned_rule_urls(self):
        for config in [self.stable, self.redir]:
            self.assertNotIn("gh-proxy.com", config)
            self.assertNotIn("gh-proxy.org", config)
            urls = re.findall(r"^\s*url:\s*['\"]?([^'\"\s]+)", config, flags=re.MULTILINE)
            rule_urls = [url for url in urls if "/rules/" in url]
            self.assertTrue(rule_urls)
            self.assertTrue(all(url.startswith("https://raw.githubusercontent.com/Charles-0509/ProxyRule/main/") for url in rule_urls))

    def test_safe_controller_and_dns_defaults(self):
        self.assertIn("external-controller: 0.0.0.0:9090", self.stable)
        self.assertIn("allow-private-network: true", self.stable)
        self.assertIn("secret: 'CHANGE_ME_TO_A_UNIQUE_LONG_RANDOM_SECRET'", self.stable)
        self.assertIn("fake-ip-range: 198.18.0.1/16", self.stable)
        self.assertIn("enhanced-mode: redir-host", self.redir)
        self.assertNotIn("fake-ip-range:", self.redir)
        self.assertIn("auto-route: true", self.stable)
        self.assertIn("auto-redirect: true", self.stable)
        self.assertIn("strict-route: true", self.stable)
        self.assertIn("endpoint-independent-nat: false", self.stable)
        self.assertNotIn("global-client-fingerprint", self.stable)

    def test_rule_order_and_representative_routes(self):
        expected = [
            "DOMAIN-SUFFIX,edu.cn,国内",
            "DOMAIN-SUFFIX,zfye.site,国内",
            "IP-CIDR,192.168.0.0/16,国内,no-resolve",
            "RULE-SET,bank,国内",
            "RULE-SET,category-ads-all,广告拦截",
            "RULE-SET,apple-push,ApplePush",
            "RULE-SET,openai,AI",
            "RULE-SET,github,GitHub",
            "RULE-SET,gitlab,开发工具",
            "RULE-SET,telegram-ip,Telegram,no-resolve",
            "RULE-SET,notion,办公协作",
            "RULE-SET,category-scholar-!cn,学术",
            "RULE-SET,bilibili,国内",
            "RULE-SET,china-domain,国内",
            "RULE-SET,proxy,国外",
            "MATCH,其他",
        ]
        positions = [self.stable.index(item) for item in expected]
        self.assertEqual(positions, sorted(positions))
        checks = {
            "rules/source/domain/openai.yaml": ("openai.com", "chatgpt.com"),
            "rules/source/domain/github.yaml": ("github.com",),
            "rules/source/domain/telegram-domain.yaml": ("telegram.org",),
            "rules/source/domain/bilibili.yaml": ("bilibili.com",),
            "rules/source/domain/apple-push.yaml": ("push.apple.com",),
        }
        for path, needles in checks.items():
            content = (ROOT / path).read_text(encoding="utf-8")
            self.assertTrue(any(needle in content for needle in needles), path)

    def test_region_filters_do_not_misclassify_common_samples(self):
        samples = {
            "香港": ["香港 01", "HK Premium", "Hong Kong IPLC"],
            "台湾": ["台湾 01", "TW Premium", "Taiwan Hinet"],
            "美国": ["美国 01", "US Premium", "United States LA"],
            "英国": ["英国 01", "UK London", "United Kingdom"],
        }
        compiled = {name: re.compile(pattern) for name, pattern in GENERATOR.REGIONS}
        for region, names in samples.items():
            for name in names:
                self.assertRegex(name, compiled[region])
        self.assertIsNone(compiled["台湾"].search("🇨🇳 中国大陆"))
        self.assertIsNone(compiled["英国"].search("英伟达 美国节点"))
        self.assertIsNone(compiled["美国"].search("RUS Russia"))

    def test_fallback_groups_and_proxy_defaults(self):
        self.assertIn("- name: 所有-故转", self.stable)
        for region, _ in GENERATOR.REGIONS:
            self.assertIn(f"- name: {region}-自动", self.stable)
            self.assertIn(f"- name: {region}-故转", self.stable)
            self.assertNotIn(f"- name: {region}-首选", self.stable)
        self.assertIn("- name: 其他地区-故转", self.stable)
        self.assertNotIn("- name: 所有-首选", self.stable)
        manual_failover = self.stable.split("  - name: 手动选择\n", 1)[1].split("  - name:", 1)[0]
        self.assertRegex(manual_failover, r"proxies:\n\s+- 美国-故转")
        us_fallback = self.stable.split("  - name: 美国-故转\n", 1)[1].split("  - name:", 1)[0]
        self.assertRegex(us_fallback, r"proxies:\n\s+- 美国-手动\n\s+- 美国-自动\n\s+- 所有-自动")
        ai_block = self.stable.split("  - name: AI\n", 1)[1].split("  - name:", 1)[0]
        self.assertRegex(ai_block, r"proxies:\n\s+- 手动选择")
        apple_push_block = self.stable.split("  - name: ApplePush\n", 1)[1].split("  - name:", 1)[0]
        self.assertRegex(apple_push_block, r"proxies:\n\s+- 直连")

    def test_zashboard_folder_profile(self):
        settings = json.loads((ROOT / "config/zashboard-settings.json").read_text(encoding="utf-8"))
        self.assertEqual("on", settings["config/proxy-folder-mode-setting"])
        self.assertEqual("core", settings["config/speedtest-mode"])
        folders = json.loads(settings["config/proxy-folders"])["folders"]
        self.assertEqual(["策略组", "故障转移", "节点组"], [item["name"] for item in folders])
        self.assertEqual("手动选择", folders[0]["manualIncludes"][0])
        self.assertNotIn("节点选择", folders[0]["manualIncludes"])
        self.assertTrue(folders[1]["rules"][0]["pattern"].endswith("-故转$"))

    def test_update_report_has_no_unresolved_alerts(self):
        report = (ROOT / "UPSTREAM_UPDATE_REPORT.md").read_text(encoding="utf-8")
        self.assertIn("- Failures: 0", report)
        self.assertIn("- Warnings: 0", report)

    def test_subscription_secrets_are_not_committed(self):
        for config in [self.stable, self.redir]:
            self.assertEqual(1, config.count("replace-with-provider-1-subscription"))
            self.assertEqual(1, config.count("replace-with-provider-2-subscription"))
            self.assertEqual(1, config.count("CHANGE_ME_TO_A_UNIQUE_LONG_RANDOM_SECRET"))
            self.assertNotRegex(config, r"(?i)(github_pat_|ghp_|bearer\s+[a-z0-9])")


if __name__ == "__main__":
    unittest.main()
