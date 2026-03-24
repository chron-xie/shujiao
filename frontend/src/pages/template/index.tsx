import { useMemo, useState } from 'react'
import { View, Text, ScrollView, Image } from '@tarojs/components'
import Taro from '@tarojs/taro'
import Icon from '../../components/Icon'
import { FILTER_OPTIONS, SAMPLE_TEMPLATES, TEMPLATE_CATEGORIES } from './data'
import './index.scss'

export default function Template() {
  const [activeTab, setActiveTab] = useState(0)
  const [filterType, setFilterType] = useState('all')

  const templates = useMemo(() => {
    const category = TEMPLATE_CATEGORIES[activeTab].value
    let currentTemplates = SAMPLE_TEMPLATES[category] || []

    if (filterType === 'free') {
      currentTemplates = currentTemplates.filter(template => template.is_free)
    } else if (filterType === 'paid') {
      currentTemplates = currentTemplates.filter(template => !template.is_free)
    }

    return currentTemplates
  }, [activeTab, filterType])

  function handleTemplateClick(id) {
    Taro.navigateTo({ url: `/pages/template/detail/index?id=${id}` })
  }

  return (
    <View className='template-page'>
      <View className='template-header'>
        <Text className='template-kicker'>资源目录</Text>
        <Text className='template-title'>行业模板库</Text>
        <Text className='template-header-subtitle'>按分类和价格状态快速筛选可复用资料。</Text>
      </View>

      <View className='template-category-tabs'>
        {TEMPLATE_CATEGORIES.map((cat, index) => (
          <View
            key={cat.value}
            className={`template-category-tab ${activeTab === index ? 'template-category-tab--active' : ''}`}
            onClick={() => setActiveTab(index)}
          >
            <Text className='template-category-tab-text'>{cat.label}</Text>
          </View>
        ))}
      </View>

      <View className='template-filter-row'>
        {FILTER_OPTIONS.map(option => (
          <View
            key={option.value}
            className={`template-filter-pill ${filterType === option.value ? 'template-filter-pill--active' : ''}`}
            onClick={() => setFilterType(option.value)}
          >
            <Text className='template-filter-pill-text'>{option.label}</Text>
          </View>
        ))}
      </View>

      <ScrollView scrollY className='template-scroll'>
        <View className='template-list'>
          {templates.length === 0 ? (
            <View className='template-empty'>
              <View className='template-empty-icon'>
                <Icon type='folder' size={34} color='#8A97A3' />
              </View>
              <Text className='template-empty-text'>暂无模板数据</Text>
            </View>
          ) : (
            templates.map((template) => (
              <View
                key={template.id}
                className='template-row'
                onClick={() => handleTemplateClick(template.id)}
              >
                {template.cover_image_url ? (
                  <Image
                    className='template-thumb'
                    src={template.cover_image_url}
                    mode='aspectFill'
                    lazyLoad
                  />
                ) : (
                  <View className='template-thumb template-thumb--placeholder'>
                    <Icon type='document' size={30} color='#5F6B76' />
                  </View>
                )}

                <View className='template-body'>
                  <Text className='template-name'>{template.template_name}</Text>
                  <Text className='template-description'>{template.description}</Text>
                </View>

                <View className='template-side'>
                  <Text className={`template-price ${template.is_free ? 'template-price--free' : ''}`}>
                    {template.is_free ? '免费' : `¥${template.price}`}
                  </Text>
                  <View className={`template-action ${template.is_free ? 'template-action--free' : ''}`}>
                    <Text className='template-action-text'>
                      {template.is_free ? '查看' : '解锁'}
                    </Text>
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
