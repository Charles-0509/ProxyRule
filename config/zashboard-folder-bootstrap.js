(() => {
  const version = '2026-11-14-v8'
  const versionKey = 'proxyrule/folder-layout-version'
  // Repair existing browser layouts without resetting folders or preferences.
  try {
    const state = JSON.parse(localStorage.getItem('config/proxy-folders'))
    const strategy = state?.folders?.find(
      (folder) => folder.id === 'proxyrule-strategy' || folder.name === '策略组',
    )
    if (strategy && Array.isArray(strategy.manualIncludes)) {
      let changed = false
      if (!strategy.manualIncludes.includes('Gemini')) {
        const index = strategy.manualIncludes.indexOf('GitHub')
        strategy.manualIncludes.splice(index < 0 ? strategy.manualIncludes.length : index, 0, 'Gemini')
        changed = true
      }
      for (const folder of state.folders) {
        if (folder !== strategy && folder.manualIncludes?.includes('Gemini')) {
          folder.manualIncludes = folder.manualIncludes.filter((name) => name !== 'Gemini')
          changed = true
        }
      }
      if (changed) localStorage.setItem('config/proxy-folders', JSON.stringify(state))
      return
    }
  } catch {
    // Missing or invalid layout: initialize the default folders below.
  }

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
