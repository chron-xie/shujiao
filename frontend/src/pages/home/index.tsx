import { View, Text, ScrollView } from '@tarojs/components'
import { useState } from 'react'
import Taro from '@tarojs/taro'
import Icon from '../../components/Icon'
import './index.scss'

export default function Home() {
  // 默认选中"参数标准查询"
  const [selectedCard, setSelectedCard] = useState('parameter')

  function handleNavigation(page) {
    // 更新选中状态
    setSelectedCard(page)

    if (page === 'parameter') {
      Taro.switchTab({ url: '/pages/parameter/index' })
    } else if (page === 'template') {
      Taro.switchTab({ url: '/pages/template/index' })
    } else if (page === 'consultation') {
      Taro.navigateTo({ url: '/pages/consultation/index' })
    }
  }

  function handleSearch() {
    Taro.switchTab({ url: '/pages/parameter/index' })
  }

  const updates = [
    { date: '2026-02-01', title: '新增 PEEK 参数表模板' },
    { date: '2026-01-28', title: '更新 FR-4 标准参数库' },
    { date: '2026-01-25', title: '优化参数对比工具' },
    { date: '2026-01-20', title: '新增 PTFE 材料检测标准' }
  ]

  return (
    <ScrollView scrollY className="home-page">
      {/* 头部 */}
      <View className="home-header">
        <Text className="home-title">绝缘材料参数工具</Text>
        <View className="home-search-icon" onClick={handleSearch}>
          <Icon type="search" size={32} color="#666666" />
        </View>
      </View>

      {/* 四大功能卡片 */}
      <View className="function-grid">
        <View
          className={`function-card ${selectedCard === 'parameter' ? 'selected-card' : 'unselected-card'} card-hover`}
          onClick={() => handleNavigation('parameter')}
        >
          <View className="card-icon">
            <Icon type="book" size={64} color={selectedCard === 'parameter' ? '#FFFFFF' : '#666666'} />
          </View>
          <Text className="card-title">参数标准查询</Text>
        </View>

        <View
          className={`function-card ${selectedCard === 'template' ? 'selected-card' : 'unselected-card'} card-hover`}
          onClick={() => handleNavigation('template')}
        >
          <View className="card-icon">
            <Icon type="folder" size={64} color={selectedCard === 'template' ? '#FFFFFF' : '#666666'} />
          </View>
          <Text className="card-title">行业模板库</Text>
        </View>

        <View
          className={`function-card ${selectedCard === 'sop' ? 'selected-card' : 'unselected-card'} card-hover`}
          onClick={() => handleNavigation('sop')}
        >
          <View className="card-icon">
            <Icon type="camera" size={64} color={selectedCard === 'sop' ? '#FFFFFF' : '#666666'} />
          </View>
          <Text className="card-title">实拍规范 SOP</Text>
        </View>

        <View
          className={`function-card ${selectedCard === 'consultation' ? 'selected-card' : 'unselected-card'} card-hover`}
          onClick={() => handleNavigation('consultation')}
        >
          <View className="card-icon">
            <Icon type="chat" size={64} color={selectedCard === 'consultation' ? '#FFFFFF' : '#666666'} />
          </View>
          <Text className="card-title">15分钟轻咨询</Text>
        </View>
      </View>

      {/* 热门工具推荐 */}
      <View className="section">
        <Text className="section-title">热门工具推荐</Text>
        <ScrollView scrollX className="tool-list">
          <View className="tool-card card card-hover">
            <View className="tool-icon">
              <Icon type="document" size={40} color="#1A5F7A" />
            </View>
            <Text className="tool-name">玻纤板核心参数速查</Text>
          </View>

          <View className="tool-card card card-hover">
            <View className="tool-icon">
              <Icon type="scale" size={40} color="#1A5F7A" />
            </View>
            <Text className="tool-name">PI板参数对比</Text>
          </View>

          <View className="tool-card card card-hover">
            <View className="tool-icon">
              <Icon type="list" size={40} color="#1A5F7A" />
            </View>
            <Text className="tool-name">详情页五</Text>
          </View>
        </ScrollView>
      </View>

      {/* 最近更新 */}
      <View className="section">
        <Text className="section-title">最近更新</Text>
        <View className="updates-list">
          {updates.map((item, index) => (
            <View key={index} className="update-item card card-hover">
              <Text className="update-date">{item.date}</Text>
              <Text className="update-title">{item.title}</Text>
            </View>
          ))}
        </View>
      </View>

      {/* 底部联系 */}
      <View className="footer">
        <Text className="footer-note">数据仅供参考，实际以国标/厂商检测报告为准</Text>
        <Text className="footer-link" onClick={() => handleNavigation('consultation')}>联系咨询</Text>
      </View>
    </ScrollView>
  )
}
