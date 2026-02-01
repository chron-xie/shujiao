import { useState, useEffect } from 'react'
import { View, Text, Input, ScrollView } from '@tarojs/components'
import Taro from '@tarojs/taro'
import { parameterAPI } from '../../services/api'
import './index.scss'

const MATERIAL_CATEGORIES = [
  { value: '玻纤板(FR-4/G11)', label: '玻纤板' },
  { value: 'PI板', label: 'PI板' },
  { value: '特种塑胶通用', label: '特种塑胶' },
]

interface Parameter {
  id: number
  material_category: string
  param_name: string
  standard_unit: string | null
  is_core: number
}

export default function Parameter() {
  const [activeTab, setActiveTab] = useState(0)
  const [searchText, setSearchText] = useState('')
  const [parameters, setParameters] = useState<Parameter[]>([])
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    loadParameters()
  }, [activeTab, searchText])

  const loadParameters = async () => {
    setLoading(true)
    try {
      const category = MATERIAL_CATEGORIES[activeTab].value
      const params = {
        material_category: category,
        search: searchText || undefined,
      }
      const data: any = await parameterAPI.getList(params)
      setParameters(data)
    } catch (error) {
      console.error('加载参数失败:', error)
      Taro.showToast({ title: '加载失败', icon: 'none' })
    } finally {
      setLoading(false)
    }
  }

  const handleSearch = (e: any) => {
    setSearchText(e.detail.value)
  }

  const handleParameterClick = (id: number) => {
    Taro.navigateTo({ url: `/pages/parameter/detail?id=${id}` })
  }

  return (
    <View className='parameter-page'>
      {/* 搜索框 */}
      <View className='search-bar'>
        <Input
          className='search-input'
          placeholder='输入参数名称查询（如CTI、Tg）'
          value={searchText}
          onInput={handleSearch}
        />
      </View>

      {/* Tab切换 */}
      <View className='tab-bar'>
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
          <View className='empty'>
            <Text>暂无相关参数，可反馈新增</Text>
          </View>
        ) : (
          parameters.map((param) => (
            <View
              key={param.id}
              className='parameter-item'
              onClick={() => handleParameterClick(param.id)}
            >
              <Text className={`param-name ${param.is_core ? 'core' : ''}`}>
                {param.param_name}
              </Text>
              <View className='param-info'>
                <Text className='param-unit'>{param.standard_unit || '-'}</Text>
                <Text className='arrow'>→</Text>
              </View>
            </View>
          ))
        )}
      </ScrollView>
    </View>
  )
}
