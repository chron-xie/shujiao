import { View, Text, ScrollView, Image } from '@tarojs/components'
import Taro from '@tarojs/taro'
import './index.scss'

export default function Home() {
  const handleSearch = () => {
    Taro.switchTab({ url: '/pages/parameter/index' })
  }

  const handleNavigation = (page: string) => {
    if (page === 'parameter') {
      Taro.switchTab({ url: '/pages/parameter/index' })
    } else if (page === 'template') {
      Taro.switchTab({ url: '/pages/template/index' })
    } else if (page === 'consultation') {
      Taro.navigateTo({ url: '/pages/consultation/index' })
    }
  }

  const coreFeatures = [
    { id: 'parameter', name: '参数标准查询', primary: true },
    { id: 'template', name: '行业模板库', primary: false },
    { id: 'sop', name: '实拍规范SOP', primary: false },
    { id: 'consultation', name: '15分钟轻咨询', primary: false },
  ]

  const hotTools = [
    { id: 1, name: '玻纤板核心参数速查' },
    { id: 2, name: 'PI板参数对比' },
    { id: 3, name: '详情页五步法框架' },
    { id: 4, name: 'CTI/Tg标注规范' },
  ]

  const recentUpdates = [
    { id: 1, date: '2026-02-01', content: '新增PEEK参数表模板' },
    { id: 2, date: '2026-01-30', content: '更新玻纤板CTI参数标准' },
    { id: 3, date: '2026-01-28', content: '新增PI板参数对比工具' },
  ]

  return (
    <ScrollView scrollY className='home-page'>
      {/* 顶部Banner */}
      <View className='header-banner'>
        <Text className='title'>绝缘材料参数工具</Text>
        <View className='search-icon' onClick={handleSearch}>
          <Text className='icon'>🔍</Text>
        </View>
      </View>

      {/* 核心功能区 */}
      <View className='core-features'>
        {coreFeatures.map((feature) => (
          <View
            key={feature.id}
            className={`feature-btn ${feature.primary ? 'primary' : ''}`}
            onClick={() => handleNavigation(feature.id)}
          >
            <Text className='feature-text'>{feature.name}</Text>
          </View>
        ))}
      </View>

      {/* 热门工具推荐区 */}
      <View className='hot-tools'>
        <Text className='section-title'>热门工具</Text>
        <ScrollView scrollX className='tool-list'>
          {hotTools.map((tool) => (
            <View key={tool.id} className='tool-card'>
              <Text className='tool-name'>{tool.name}</Text>
            </View>
          ))}
        </ScrollView>
      </View>

      {/* 最近更新区 */}
      <View className='recent-updates'>
        <Text className='section-title'>最近更新</Text>
        <View className='update-list'>
          {recentUpdates.map((update) => (
            <View key={update.id} className='update-item'>
              <Text className='update-date'>{update.date}</Text>
              <Text className='update-content'>{update.content}</Text>
            </View>
          ))}
        </View>
      </View>

      {/* 底部说明栏 */}
      <View className='footer-note'>
        <Text className='note-text'>数据仅供参考，实际以国标/厂商检测报告为准</Text>
        <Text className='contact-btn' onClick={() => handleNavigation('consultation')}>
          联系咨询
        </Text>
      </View>
    </ScrollView>
  )
}
