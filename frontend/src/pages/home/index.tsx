import { View, Text, ScrollView } from '@tarojs/components'
import Taro from '@tarojs/taro'
import Icon from '../../components/Icon'
import './index.scss'

const MATERIAL_SHORTCUTS = [
  { label: 'FR-4 / G11', value: '玻纤板(FR-4/G11)', note: '玻纤板' },
  { label: 'PI', value: 'PI板', note: '高温材料' },
  { label: 'PEEK', value: '特种塑胶通用', note: '特种塑胶' },
  { label: 'PPS', value: '特种塑胶通用', note: '特种塑胶' },
  { label: 'PEI', value: '特种塑胶通用', note: '特种塑胶' },
]

const HOME_UPDATES = [
  { date: '2026-02-01', title: '新增 PEEK 参数表模板' },
  { date: '2026-01-28', title: '更新 FR-4 标准参数库' },
  { date: '2026-01-25', title: '优化参数对比工具' },
  { date: '2026-01-20', title: '新增 PTFE 材料检测标准' },
]

const secondaryActions = [
  {
    key: 'template',
    title: '模板库',
    description: '查找可直接复用的资料和话术。',
    icon: 'folder',
  },
  {
    key: 'consultation',
    title: '轻咨询',
    description: '对接参数梳理、店铺结构与拍摄规范。',
    icon: 'chat',
  },
]

function openParameterTab() {
  Taro.switchTab({ url: '/pages/parameter/index' })
}

function openTemplateTab() {
  Taro.switchTab({ url: '/pages/template/index' })
}

function openConsultation() {
  Taro.navigateTo({ url: '/pages/consultation/index' })
}

function openMaterialCategory(value) {
  Taro.setStorageSync('parameterCategory', value)
  Taro.switchTab({ url: '/pages/parameter/index' })
}

function openSopResource() {
  Taro.showToast({
    title: 'SOP 正在整理中',
    icon: 'none',
  })
}

function handlePrimaryAction(actionKey) {
  if (actionKey === 'parameter') {
    openParameterTab()
    return
  }

  if (actionKey === 'template') {
    openTemplateTab()
    return
  }

  if (actionKey === 'consultation') {
    openConsultation()
  }
}

export default function Home() {
  const updates = HOME_UPDATES.slice().sort((left, right) => right.date.localeCompare(left.date))

  return (
    <View className="home-page">
      <View className="home-content">
        <View className="brand-panel">
          <View className="brand-topline">
            <Text className="brand-kicker">工业工作台</Text>
            <View className="brand-chip">
              <Text className="brand-chip-text">参数 / 模板 / 咨询</Text>
            </View>
          </View>

          <Text className="brand-title">绝缘材料参数工具</Text>
          <Text className="brand-subtitle">查参数、找模板、发咨询，一屏完成入口判断。</Text>

          <View className="brand-search" onClick={openParameterTab}>
            <Icon type="search" size={30} color="#F7FAFC" />
            <Text className="brand-search-text">搜索参数、材料名称或关键词</Text>
            <Text className="brand-search-action">进入</Text>
          </View>
        </View>

        <View className="section-block">
          <View className="section-head">
            <Text className="section-title">主操作</Text>
            <Text className="section-caption">高频入口</Text>
          </View>

          <View className="primary-launcher">
            <View className="primary-launch-main" onClick={() => handlePrimaryAction('parameter')}>
              <View className="launch-topline">
                <View className="launch-icon launch-icon-emphasis">
                  <Icon type="book" size={42} color="#FFFFFF" />
                </View>
                <Text className="launch-badge">最强入口</Text>
              </View>
              <Text className="launch-title">参数速查</Text>
              <Text className="launch-copy">快速定位材料分类、重点参数和基础数值。</Text>
            </View>

            <View className="primary-launch-grid">
              {secondaryActions.map(action => (
                <View
                  key={action.key}
                  className="primary-launch-secondary"
                  onClick={() => handlePrimaryAction(action.key)}
                >
                  <View className="launch-icon">
                    <Icon type={action.icon} size={34} color="#1F4D66" />
                  </View>
                  <Text className="launch-title">{action.title}</Text>
                  <Text className="launch-copy">{action.description}</Text>
                </View>
              ))}
            </View>
          </View>
        </View>

        <View className="section-block">
          <View className="section-head">
            <Text className="section-title">热门材料</Text>
            <Text className="section-caption">一键切换分类</Text>
          </View>

          <ScrollView scrollX className="shortcut-scroll">
            <View className="shortcut-list">
              {MATERIAL_SHORTCUTS.map(item => (
                <View key={`${item.label}-${item.value}`} className="shortcut-chip" onClick={() => openMaterialCategory(item.value)}>
                  <Text className="shortcut-chip-label">{item.label}</Text>
                  <Text className="shortcut-chip-note">{item.note}</Text>
                </View>
              ))}
            </View>
          </ScrollView>
        </View>

        <View className="section-block">
          <View className="section-head">
            <Text className="section-title">常用资源</Text>
            <Text className="section-caption">次级入口</Text>
          </View>

          <View className="resource-list">
            <View className="resource-row" onClick={openSopResource}>
              <View className="resource-icon">
                <Icon type="camera" size={34} color="#1F4D66" />
              </View>
              <View className="resource-body">
                <Text className="resource-title">实拍规范 SOP</Text>
                <Text className="resource-desc">暂无独立页面，保留当前开发中反馈。</Text>
              </View>
              <Text className="resource-tag">开发中</Text>
            </View>
          </View>
        </View>

        {updates.length > 0 && (
          <View className="section-block">
            <View className="section-head">
              <Text className="section-title">最近更新</Text>
              <Text className="section-caption">新到旧</Text>
            </View>

            <View className="updates-list">
              {updates.map(item => (
                <View key={`${item.date}-${item.title}`} className="update-row">
                  <Text className="update-date">{item.date}</Text>
                  <Text className="update-title">{item.title}</Text>
                </View>
              ))}
            </View>
          </View>
        )}

        <View className="consultation-block">
          <View className="consultation-copy">
            <Text className="consultation-kicker">轻咨询</Text>
            <Text className="consultation-title">15 分钟解决一个核心问题</Text>
            <Text className="consultation-desc">适合参数梳理、店铺结构和实拍素材规范。</Text>
          </View>

          <View className="consultation-actions">
            <View className="consultation-button" onClick={openConsultation}>
              <Text className="consultation-button-text">去咨询</Text>
            </View>
          </View>
        </View>

        <View className="disclaimer-block">
          <Text className="disclaimer-text">数据仅供参考，实际以国标/厂商检测报告为准。</Text>
        </View>
      </View>
    </View>
  )
}
