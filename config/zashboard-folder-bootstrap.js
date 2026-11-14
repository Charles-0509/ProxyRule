(() => {
  const version = '2026-11-14-v8'
  const versionKey = 'proxyrule/folder-layout-version'
  if (localStorage.getItem(versionKey) === version) return

  const strategyGroups = [
    '手动选择',
    '规则更新',
    '学术',
    '广告拦截',
    'AI',
    'Amazon',
    'Apple',
    'Apple Intelligence',
    'ApplePush',
    'Bing & Rewards',
    '国内',
    'Cloudflare',
    'Crunchyroll',
    '加密货币',
    '开发工具',
    'Discord',
    'Disney+',
    'Dropbox',
    'Facebook',
    '游戏',
    'Gemini',
    'GitHub',
    '国外',
    'Google',
    'HBO',
    'Instagram',
    'LinkedIn',
    'Microsoft',
    'Netflix',
    '办公协作',
    'OneDrive',
    '其他',
    'PayPal',
    'Reddit',
    '测速',
    'Spotify',
    'Steam社区',
    'Steam下载',
    '流媒体',
    'Telegram',
    'TikTok',
    'WhatsApp',
    'X',
    'YouTube',
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
        manualIncludes: ['Azure'],
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
