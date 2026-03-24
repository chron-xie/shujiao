import { useState } from 'react'
import { View, Text, Input, ScrollView } from '@tarojs/components'
import Taro, { useDidShow } from '@tarojs/taro'
import Icon from '../../components/Icon'
import { MATERIAL_CATEGORIES, getCategoryIndex, getFilteredParameters } from './data'
import './index.scss'

export default function Parameter() {
  const [activeTab, setActiveTab] = useState(0)
  const [searchText, setSearchText] = useState('')

  useDidShow(() => {
    const storedCategory = Taro.getStorageSync('parameterCategory')

    if (storedCategory) {
      const nextTab = getCategoryIndex(storedCategory)
      if (nextTab >= 0) {
        setActiveTab(nextTab)
      }
    }

    Taro.removeStorageSync('parameterCategory')
  })

  const parameters = getFilteredParameters(activeTab, searchText)

  function handleSearch(e: { detail: { value: string } }) {
    setSearchText(e.detail.value)
  }

  function handleParameterClick(id: number) {
    Taro.navigateTo({ url: `/pages/parameter/detail/index?id=${id}` })
  }

  return (
    <View className='parameter-page'>
      <View className='parameter-header'>
        <View className='parameter-title-group'>
          <Text className='parameter-kicker'>参数查询</Text>
          <Text className='parameter-title'>参数标准查询</Text>
          <Text className='parameter-subtitle'>按分类浏览重点参数与基础数值。</Text>
        </View>

        <View className='parameter-search'>
          <Input
            className='parameter-search-input'
            placeholder='搜索参数'
            placeholderClass='parameter-search-placeholder'
            value={searchText}
            onInput={handleSearch}
            confirmType='search'
          />
          <View className='parameter-search-icon'>
            <Icon type='search' size={24} color='#8A97A3' />
          </View>
        </View>
      </View>

      <View className='parameter-category-tabs'>
        {MATERIAL_CATEGORIES.map((cat, index) => (
          <View
            key={cat.value}
            className={`parameter-category-tab ${activeTab === index ? 'parameter-category-tab--active' : ''}`}
            onClick={() => setActiveTab(index)}
          >
            <Text className='parameter-category-tab-text'>{cat.label}</Text>
          </View>
        ))}
      </View>

      <ScrollView scrollY className='parameter-scroll'>
        <View className='parameter-list'>
          {parameters.length === 0 ? (
            <View className='parameter-empty'>
              <View className='parameter-empty-icon'>
                <Icon type='document' size={34} color='#8A97A3' />
              </View>
              <Text className='parameter-empty-text'>暂无参数数据</Text>
            </View>
          ) : (
            parameters.map((param) => (
              <View
                key={param.id}
                className={`parameter-item ${param.is_highlight ? 'parameter-item--highlight' : ''}`}
                onClick={() => handleParameterClick(param.id)}
              >
                <View className='param-main'>
                  <View className='param-name-row'>
                    <Text className='param-name'>{param.param_name}</Text>
                    {param.is_highlight && <Text className='param-badge'>重点</Text>}
                  </View>
                </View>

                <View className='param-reading'>
                  <Text className='param-value'>{param.value}</Text>
                  <View className='param-unit-row'>
                    <Text className='param-unit'>{param.unit}</Text>
                    <Text className='param-arrow'>›</Text>
                  </View>
                </View>
              </View>
            ))
          )}
        </View>
      </ScrollView>
    </View>
  )
}
