import { useState, useEffect } from 'react'
import { View, Text, Input, ScrollView } from '@tarojs/components'
import Taro from '@tarojs/taro'
import { parameterAPI } from '../../services/api'
import './index.scss'

const MATERIAL_CATEGORIES = [
  { value: '玻纤板(FR-4/G11)', label: '玻纤板(FR-4/G11)' },
  { value: 'PI板', label: 'PI板' },
  { value: '特种塑胶通用', label: '特种塑胶通用' },
]

// 示例数据（当API未返回数据时使用）
const SAMPLE_DATA = {
  '玻纤板(FR-4/G11)': [
    { id: 1, param_name: 'CTI值', value: '≥600', unit: 'V', is_highlight: true },
    { id: 2, param_name: '玻璃化转变温度Tg', value: '130-180', unit: '°C', is_highlight: true },
    { id: 3, param_name: '热膨胀系数', value: '12-16', unit: 'ppm/°C', is_highlight: false },
    { id: 4, param_name: '介电常数', value: '4.3-4.8', unit: '1MHz', is_highlight: true },
    { id: 5, param_name: '吸水率', value: '≤0.1', unit: '%', is_highlight: false },
    { id: 6, param_name: '抗弯强度', value: '≥400', unit: 'MPa', is_highlight: true },
    { id: 7, param_name: '热导率', value: '0.3-0.4', unit: 'W/m·K', is_highlight: false },
  ],
  'PI板': [
    { id: 11, param_name: '玻璃化转变温度Tg', value: '360-410', unit: '°C', is_highlight: true },
    { id: 12, param_name: '热膨胀系数', value: '3-5', unit: 'ppm/°C', is_highlight: false },
    { id: 13, param_name: '介电常数', value: '3.2-3.5', unit: '1MHz', is_highlight: true },
    { id: 14, param_name: '吸水率', value: '≤0.3', unit: '%', is_highlight: false },
  ],
  '特种塑胶通用': [
    { id: 21, param_name: 'PEEK熔点', value: '343', unit: '°C', is_highlight: true },
    { id: 22, param_name: 'PPS热变形温度', value: '≥260', unit: '°C', is_highlight: true },
    { id: 23, param_name: 'PEI玻璃化转变温度', value: '217', unit: '°C', is_highlight: false },
    { id: 24, param_name: '吸水率', value: '0.1-0.5', unit: '%', is_highlight: false },
  ],
}

export default function Parameter() {
  const [activeTab, setActiveTab] = useState(0)
  const [searchText, setSearchText] = useState('')
  const [parameters, setParameters] = useState([])
  const [loading, setLoading] = useState(false)

  // 安全的返回处理
  function handleBack() {
    const pages = Taro.getCurrentPages()
    if (pages.length > 1) {
      Taro.navigateBack()
    } else {
      Taro.switchTab({ url: '/pages/home/index' })
    }
  }

  useEffect(() => {
    loadParameters()
  }, [activeTab, searchText])

  function loadParameters() {
    setLoading(true)
    const category = MATERIAL_CATEGORIES[activeTab].value

    // 使用示例数据
    const sampleData = SAMPLE_DATA[category] || []

    // 如果有搜索文本，进行过滤
    const filteredData = searchText
      ? sampleData.filter(param =>
          param.param_name.toLowerCase().includes(searchText.toLowerCase())
        )
      : sampleData

    setParameters(filteredData)
    setLoading(false)

    // TODO: 后续接入真实API
    /*
    const params = {
      material_category: category,
      search: searchText || undefined,
    }
    parameterAPI.getList(params)
      .then(data => {
        setParameters(data || [])
      })
      .catch(error => {
        console.error('加载参数失败:', error)
        // 失败时使用示例数据
        setParameters(SAMPLE_DATA[category] || [])
      })
      .finally(() => {
        setLoading(false)
      })
    */
  }

  function handleSearch(e) {
    setSearchText(e.detail.value)
  }

  function handleParameterClick(id) {
    Taro.navigateTo({ url: `/pages/parameter/detail/index?id=${id}` })
  }

  function toggleSearch() {
    setShowSearch(!showSearch)
    if (showSearch) {
      setSearchText('')
    }
  }

  return (
    <View className='parameter-page'>
      {/* 顶部导航 */}
      <View className='page-header'>
        <View className='header-left'>
          <View className='back-button' onClick={handleBack}>
            <Text className='back-icon'>‹</Text>
          </View>
          <Text className='page-title'>参数标准查询</Text>
        </View>
        <View className='search-box'>
          <Input
            className='search-input'
            placeholder='搜索参数'
            value={searchText}
            onInput={handleSearch}
          />
          <Text className='search-icon'>🔍</Text>
        </View>
      </View>

      {/* Tab切换 */}
      <View className='tabs'>
        {MATERIAL_CATEGORIES.map((cat, index) => (
          <View
            key={cat.value}
            className={`tab-item ${activeTab === index ? 'active' : ''}`}
            onClick={() => setActiveTab(index)}
          >
            <Text className='tab-text'>{cat.label}</Text>
          </View>
        ))}
      </View>

      {/* 参数列表 */}
      <ScrollView scrollY className='parameter-list'>
        {loading ? (
          <View className='loading'>
            <Text>加载中...</Text>
          </View>
        ) : parameters.length === 0 ? (
          <View className='empty-state'>
            <View className='empty-icon'>📋</View>
            <Text className='empty-text'>暂无参数数据</Text>
          </View>
        ) : (
          parameters.map((param) => (
            <View
              key={param.id}
              className={`parameter-item ${param.is_highlight ? 'highlight-param' : ''}`}
              onClick={() => handleParameterClick(param.id)}
            >
              <View className='param-left'>
                <Text className={`param-name ${param.is_highlight ? 'highlight-name' : ''}`}>
                  {param.param_name}
                </Text>
              </View>
              <View className='param-right'>
                <View className='param-value-box'>
                  <Text className='param-unit'>{param.unit}</Text>
                  <Text className='param-value'>{param.value}</Text>
                </View>
                <Text className='param-arrow'>›</Text>
              </View>
            </View>
          ))
        )}
      </ScrollView>
    </View>
  )
}
