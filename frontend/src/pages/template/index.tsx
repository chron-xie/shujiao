import { useState, useEffect } from 'react'
import { View, Text, ScrollView, Image } from '@tarojs/components'
import Taro from '@tarojs/taro'
import { templateAPI } from '../../services/api'
import './index.scss'

const TEMPLATE_CATEGORIES = [
  { value: '参数表模板', label: '参数表' },
  { value: '店铺架构模板', label: '店铺架构' },
  { value: '实拍SOP模板', label: '实拍SOP' },
  { value: 'FAQ话术模板', label: 'FAQ话术' },
]

interface Template {
  id: number
  template_category: string
  template_name: string
  cover_image_url: string | null
  price: number
  is_free: boolean
}

export default function Template() {
  const [activeTab, setActiveTab] = useState(0)
  const [filterType, setFilterType] = useState<'all' | 'free' | 'paid'>('all')
  const [templates, setTemplates] = useState<Template[]>([])
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    loadTemplates()
  }, [activeTab, filterType])

  const loadTemplates = async () => {
    setLoading(true)
    try {
      const category = TEMPLATE_CATEGORIES[activeTab].value
      const params: any = {
        template_category: category,
      }
      if (filterType !== 'all') {
        params.is_free = filterType === 'free'
      }
      const data: any = await templateAPI.getList(params)
      setTemplates(data)
    } catch (error) {
      console.error('加载模板失败:', error)
      Taro.showToast({ title: '加载失败', icon: 'none' })
    } finally {
      setLoading(false)
    }
  }

  const handleFilter = () => {
    Taro.showActionSheet({
      itemList: ['全部', '免费', '付费'],
      success: (res) => {
        const types: ('all' | 'free' | 'paid')[] = ['all', 'free', 'paid']
        setFilterType(types[res.tapIndex])
      },
    })
  }

  const handleTemplateClick = (id: number) => {
    Taro.navigateTo({ url: `/pages/template/detail?id=${id}` })
  }

  return (
    <View className='template-page'>
      {/* 顶部导航栏 */}
      <View className='header'>
        <Text className='title'>行业模板库</Text>
        <View className='filter-btn' onClick={handleFilter}>
          <Text>筛选</Text>
        </View>
      </View>

      {/* Tab切换 */}
      <View className='tab-bar'>
        {TEMPLATE_CATEGORIES.map((cat, index) => (
          <View
            key={cat.value}
            className={`tab-item ${activeTab === index ? 'active' : ''}`}
            onClick={() => setActiveTab(index)}
          >
            <Text className='tab-text'>{cat.label}</Text>
          </View>
        ))}
      </View>

      {/* 模板列表 */}
      <ScrollView scrollY className='template-list'>
        {loading ? (
          <View className='loading'>
            <Text>加载中...</Text>
          </View>
        ) : templates.length === 0 ? (
          <View className='empty'>
            <Text>暂无对应模板，可反馈定制</Text>
          </View>
        ) : (
          templates.map((template) => (
            <View
              key={template.id}
              className='template-card'
              onClick={() => handleTemplateClick(template.id)}
            >
              {/* 模板封面 */}
              <View className='template-cover'>
                {template.cover_image_url ? (
                  <Image
                    className='cover-image'
                    src={template.cover_image_url}
                    mode='aspectFill'
                  />
                ) : (
                  <View className='cover-placeholder'>
                    <Text>📄</Text>
                  </View>
                )}
              </View>

              {/* 模板信息 */}
              <View className='template-info'>
                <Text className='template-name'>{template.template_name}</Text>
                <View className='template-price'>
                  {template.is_free ? (
                    <Text className='price-tag free'>免费</Text>
                  ) : (
                    <Text className='price-tag paid'>¥{template.price}</Text>
                  )}
                </View>
              </View>

              {/* 操作按钮 */}
              <View className='template-action'>
                <Text className='action-btn'>
                  {template.is_free ? '立即查看' : '立即解锁'}
                </Text>
              </View>
            </View>
          ))
        )}
      </ScrollView>
    </View>
  )
}
