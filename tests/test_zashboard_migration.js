const assert = require('node:assert/strict')
const fs = require('node:fs')
const vm = require('node:vm')
const path = require('node:path')
const code = fs.readFileSync(path.join(__dirname, '../config/zashboard-folder-bootstrap.js'), 'utf8')

for (const version of ['2026-11-11-v7', '2026-11-14-v8']) {
  const original = {
    folders: [
      { id: 'custom', name: '策略组', manualIncludes: ['手动选择', '规则更新', '学术', '游戏', '开发工具', '办公协作', '流媒体', '加密货币', 'GitHub'], custom: true },
      { id: 'nodes', manualIncludes: ['Azure', 'Gemini'], rules: [{ type: 'auto', value: 'nodeOnly' }] },
    ],
    activeId: 'nodes', custom: 'keep',
  }
  const store = new Map([
    ['proxyrule/folder-layout-version', version],
    ['config/proxy-folders', JSON.stringify(original)],
    ['config/speedtest-timeout', '19000'],
  ])
  const context = { localStorage: { getItem: (key) => store.get(key) ?? null, setItem: (key, value) => store.set(key, value) } }
  vm.runInNewContext(code, context)
  const migrated = JSON.parse(store.get('config/proxy-folders'))
  for (const name of ['学术期刊网站', '游戏平台', 'GitLab', 'Docker', 'Notion', 'Slack', 'Zoom', 'Popcorn', 'Gemini', '加密货币']) {
    assert(migrated.folders[0].manualIncludes.includes(name), name)
  }
  for (const name of ['学术', '游戏', '开发工具', '办公协作', '流媒体']) assert(!migrated.folders[0].manualIncludes.includes(name), name)
  assert.deepEqual(migrated.folders[1].manualIncludes, ['Azure'])
  assert.deepEqual(migrated.folders[1].rules, original.folders[1].rules)
  assert.equal(migrated.activeId, 'nodes')
  assert.equal(migrated.custom, 'keep')
  assert.equal(migrated.folders[0].custom, true)
  assert.equal(store.get('config/speedtest-timeout'), '19000')
  const once = store.get('config/proxy-folders')
  vm.runInNewContext(code, context)
  assert.equal(store.get('config/proxy-folders'), once)
}
console.log('Browser folder migration passed: renames, splits, Gemini membership, preference preservation, idempotence')
