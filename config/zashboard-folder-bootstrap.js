(() => {
  const version = '2026-07-16-v2'
  const versionKey = 'proxyrule/folder-layout-version'
  if (localStorage.getItem(versionKey) === version) return

  const strategyGroups = [
    '手动选择', '规则更新', 'AI', 'GitHub', '开发工具', 'Cloudflare', 'Telegram',
    'Discord', 'WhatsApp', 'X', 'Facebook', 'Instagram', 'Reddit', 'TikTok',
    'YouTube', 'Netflix', 'Disney+', 'HBO', 'Amazon', 'Crunchyroll', '流媒体',
    'Spotify', '游戏', 'Apple', 'Microsoft', 'OneDrive', 'Google', '办公协作',
    '云盘', 'LinkedIn', 'PayPal', '学术', '测速', '加密货币', 'ApplePush',
    '国内', '广告拦截', '国外', '其他',
  ]
  const folderState = {
    folders: [
      {
        id: 'proxyrule-strategy',
        name: '策略组',
        order: 0,
        rules: [],
        manualIncludes: strategyGroups,
      },
      {
        id: 'proxyrule-failover',
        name: '故障转移',
        order: 1,
        rules: [
          {
            type: 'regex',
            pattern: '^(?:所有|香港|台湾|日本|新加坡|韩国|美国|英国|其他地区)-故转$',
          },
        ],
        manualIncludes: [],
      },
      {
        id: 'proxyrule-nodes',
        name: '节点组',
        order: 2,
        rules: [{ type: 'auto', value: 'nodeOnly' }],
        manualIncludes: [],
      },
    ],
    activeId: '__all__',
    seeded: true,
  }

  localStorage.setItem('config/proxy-folder-mode-setting', 'on')
  localStorage.setItem('config/speedtest-mode', 'core')
  localStorage.setItem('config/speedtest-timeout', '8000')
  localStorage.setItem('config/proxy-folders', JSON.stringify(folderState))
  localStorage.setItem(versionKey, version)
})()
