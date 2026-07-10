# 修复 Zashboard 节点测速超时

## 适用现象

更新 OpenClash 或 Mihomo 内核后，节点本身能够正常联网，自动测速也可能有
延迟结果，但 Zashboard 点击顶部闪电图标进行测速时全部超时或失败。

常见原因是旧版 Zashboard 仍调用已不兼容的 `/proxies/{node}/delay` 接口；
新版 Mihomo 的机场 provider 节点应使用
`/providers/proxies/{provider}/{node}/healthcheck` 接口。

## 最简单的修复方法

1. SSH 登录软路由并进入 `root` shell。
2. 执行 OpenClash 自带的 Zashboard 更新脚本：

   ```sh
   /usr/share/openclash/openclash_download_dashboard.sh Zashboard Official
   ```

3. 命令返回后，确认已存在新的前端包：

   ```sh
   ls -l /usr/share/openclash/ui/zashboard/assets/index-*.js
   ```

4. 打开 `http://<router-lan-ip>:9090/ui/zashboard/`，使用 `Ctrl + Shift + R`
   强制刷新页面。若仍显示旧界面，用无痕窗口重新打开。
5. 再点击 Zashboard 右上角的闪电按钮测速。

该脚本会先下载并解压新面板，成功后才替换现有文件；下载或解压失败时会恢复
旧版本。通常不需要重启 OpenClash，也不需要重新导入订阅或修改节点配置。

## 验证与排查

- 更新前端后，测速请求应使用 `/providers/proxies/.../healthcheck`，而不是
  `/proxies/.../delay`。
- 如果脚本失败，先检查路由器能否访问 GitHub、系统时间是否正确，以及
  OpenClash 运行日志中的下载错误。
- 如果更新后仍超时，先强制刷新或清理浏览器站点缓存，避免 Service Worker
  继续提供旧的 Zashboard 前端文件。
