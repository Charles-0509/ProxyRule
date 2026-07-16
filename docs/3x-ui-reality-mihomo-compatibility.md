# 3x-ui 更新后 VLESS Reality 无法连接

## 已知兼容性问题

3x-ui `3.5.0` 搭载的 Xray-core `26.7.11` 与 Mihomo `1.19.28` 的
VLESS + Reality + Vision 存在已知兼容性问题。典型表现是：

- 同一台服务器上的 Hysteria2 正常；
- VLESS Reality 端口正常监听，防火墙也已放行；
- UUID、公钥、Short ID 和 SNI 均正确；
- Mihomo 日志出现 `REALITY authentication failed`。

对应上游报告：
[XTLS/Xray-core #6477](https://github.com/XTLS/Xray-core/issues/6477)。

## 临时处理方法

在 3x-ui 中编辑 VLESS Reality 入站，将 `minClientVer` 设置为：

```text
1.0.0
```

保存并重启 Xray 后重新测速。这个设置会放宽服务端接受的客户端版本范围，
建议只作为兼容性措施；当 Mihomo 已升级并确认支持新版 Reality 行为后，应
移除该覆盖并重新测试。

另一个经过上游用户验证的办法是只把服务端 Xray-core 回退到 `26.6.27`，
保留 3x-ui、数据库、UUID 和 Reality 密钥不变。回退核心前必须备份原二进制，
并只从 XTLS/Xray-core 官方 Release 下载及核验文件。

## 排查顺序

1. 确认 VLESS TCP 端口正在监听并被防火墙允许。
2. 对比订阅中的 UUID、Reality 公钥、Short ID、SNI 与服务端入站。
3. 确认 3x-ui 数据库和实际运行的 Xray 配置一致；必要时备份后重启 x-ui。
4. 用 Mihomo 调试日志确认是否为 `REALITY authentication failed`。
5. 最后再应用 `minClientVer` 兼容设置或回退 Xray 核心。

不要为了排障重新生成 UUID、Reality 密钥或订阅路径；这会同时让所有已有
客户端失效，并掩盖真正的版本兼容问题。
