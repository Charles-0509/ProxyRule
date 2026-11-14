(() => {
  const version = '2026-11-14-v10'
  const versionKey = 'proxyrule/folder-layout-version'
  // Repair existing browser layouts without resetting folders or preferences.
  try {
    const state = JSON.parse(localStorage.getItem('config/proxy-folders'))
    const strategy = state?.folders?.find(
      (folder) => folder.id === 'proxyrule-strategy' || folder.name === '策略组',
    )
    if (strategy && Array.isArray(strategy.manualIncludes)) {
      let changed = false
      const replacements = {
        学术: ['学术期刊网站'], 游戏: ['游戏平台'], 流媒体: ['Popcorn'],
        开发工具: ['GitLab', 'Docker'], 办公协作: ['Notion', 'Slack', 'Zoom'],
      }
      for (const folder of state.folders) {
        if (!Array.isArray(folder.manualIncludes)) continue
        const members = [...new Set(folder.manualIncludes.flatMap((name) => replacements[name] || [name]))]
        if (JSON.stringify(members) !== JSON.stringify(folder.manualIncludes)) {
          folder.manualIncludes = members
          changed = true
        }
      }
      for (const name of ['Gemini', 'GitLab', 'Docker', 'Notion', 'Slack', 'Zoom', 'Popcorn', '学术期刊网站', '游戏平台']) {
        if (!strategy.manualIncludes.includes(name)) {
          const index = name === 'Gemini' ? strategy.manualIncludes.indexOf('GitHub') : -1
          strategy.manualIncludes.splice(index < 0 ? strategy.manualIncludes.length : index, 0, name)
          changed = true
        }
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
    '学术期刊网站',
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
    'Discord',
    'Disney+',
    'Docker',
    'Dropbox',
    'Facebook',
    '游戏平台',
    'Gemini',
    'GitHub',
    'GitLab',
    '国外',
    'Google',
    'HBO',
    'Instagram',
    'LinkedIn',
    'Microsoft',
    'Netflix',
    'Notion',
    'OneDrive',
    '其他',
    'PayPal',
    'Popcorn',
    'Reddit',
    'Slack',
    '测速',
    'Spotify',
    'Steam社区',
    'Steam下载',
    'Telegram',
    'TikTok',
    'WhatsApp',
    'X',
    'YouTube',
    'Zoom',
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
