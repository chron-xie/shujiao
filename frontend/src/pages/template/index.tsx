import { useState, useEffect } from 'react'
import { View, Text, ScrollView, Image } from '@tarojs/components'
import Taro from '@tarojs/taro'
import { templateAPI } from '../../services/api'
import './index.scss'

const TEMPLATE_CATEGORIES = [
  { value: '参数表模板', label: '参数表模板' },
  { value: '店铺架构模板', label: '店铺架构模板' },
  { value: '实拍SOP模板', label: '实拍 SOP 模板' },
  { value: 'FAQ话术模板', label: 'FAQ 话术模板' },
]

// 示例数据
const SAMPLE_TEMPLATES = {
  '参数表模板': [
    {
      id: 1,
      template_name: '玻纤板核心参数表（完整版）',
      template_category: '参数表模板',
      cover_image_url: '',
      description: '适用于 1688 / 淘宝详情页',
      price: 19.9,
      is_free: false,
    },
    {
      id: 2,
      template_name: '金属配件参数表（基础版）',
      template_category: '参数表模板',
      cover_image_url: '',
      description: '适用于 1688 / 淘宝详情页',
      price: 0,
      is_free: true,
    },
    {
      id: 3,
      template_name: 'PI板参数表（专业版）',
      template_category: '参数表模板',
      cover_image_url: '',
      description: '适用于 1688 / 淘宝详情页',
      price: 29.9,
      is_free: false,
    },
  ],
  '店铺架构模板': [
    {
      id: 11,
      template_name: '1688店铺首页架构',
      template_category: '店铺架构模板',
      cover_image_url: '',
      description: '适用于 1688 电商平台',
      price: 0,
      is_free: true,
    },
    {
      id: 12,
      template_name: '淘宝店铺架构（高级版）',
      template_category: '店铺架构模板',
      cover_image_url: '',
      description: '适用于淘宝 / 天猫店铺',
      price: 49.9,
      is_free: false,
    },
  ],
  '实拍SOP模板': [
    {
      id: 21,
      template_name: '产品实拍流程标准（完整版）',
      template_category: '实拍SOP模板',
      cover_image_url: '',
      description: '适用于工业材料产品拍摄',
      price: 39.9,
      is_free: false,
    },
    {
      id: 22,
      template_name: '简易实拍SOP（基础版）',
      template_category: '实拍SOP模板',
      cover_image_url: '',
      description: '适用于快速拍摄场景',
      price: 0,
      is_free: true,
    },
  ],
  'FAQ话术模板': [
    {
      id: 31,
      template_name: '客户常见问题话术库',
      template_category: 'FAQ话术模板',
      cover_image_url: '',
      description: '适用于客服接待场景',
      price: 0,
      is_free: true,
    },
    {
      id: 32,
      template_name: '技术咨询话术模板',
      template_category: 'FAQ话术模板',
      cover_image_url: '',
      description: '适用于技术咨询场景',
      price: 29.9,
      is_free: false,
    },
  ],
}

export default function Template() {
  const [activeTab, setActiveTab] = useState(0)
  const [filterType, setFilterType] = useState('all')
  const [templates, setTemplates] = useState([])
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
    loadTemplates()
  }, [activeTab, filterType])

  function loadTemplates() {
    setLoading(true)
    const category = TEMPLATE_CATEGORIES[activeTab].value

    // 使用示例数据
    let sampleData = SAMPLE_TEMPLATES[category] || []

    // 根据筛选类型过滤
    if (filterType === 'free') {
      sampleData = sampleData.filter(t => t.is_free)
    } else if (filterType === 'paid') {
      sampleData = sampleData.filter(t => !t.is_free)
    }

    setTemplates(sampleData)
    setLoading(false)

    // TODO: 后续接入真实API
    /*
    const params = {
      template_category: category,
    }
    if (filterType !== 'all') {
      params.is_free = filterType === 'free'
    }
    templateAPI.getList(params)
      .then(data => {
        setTemplates(data || [])
      })
      .catch(error => {
        console.error('加载模板失败:', error)
        setTemplates(SAMPLE_TEMPLATES[category] || [])
      })
      .finally(() => {
        setLoading(false)
      })
    */
  }

  function handleFilter() {
    Taro.showActionSheet({
      itemList: ['全部', '免费', '付费'],
      success: (res) => {
        const types = ['all', 'free', 'paid']
        setFilterType(types[res.tapIndex])
      },
    })
  }

  function handleTemplateClick(id) {
    Taro.navigateTo({ url: `/pages/template/detail/index?id=${id}` })
  }

  return (
    <View className='template-page'>
      {/* 顶部导航栏 */}
      <View className='page-header'>
        <View className='header-left'>
          <View className='back-button' onClick={handleBack}>
            <Text className='back-icon'>‹</Text>
          </View>
          <Text className='page-title'>行业模板库</Text>
        </View>
        <View className='filter-button' onClick={handleFilter}>
          <Text className='filter-text'>
            {filterType === 'all' ? '全部' : filterType === 'free' ? '免费' : '付费'}
          </Text>
        </View>
      </View>

      {/* Tab切换 */}
      <View className='tabs'>
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
          <View className='empty-state'>
            <View className='empty-icon'>📁</View>
            <Text className='empty-text'>暂无模板数据</Text>
          </View>
        ) : (
          templates.map((template) => (
            <View
              key={template.id}
              className='template-card card'
              onClick={() => handleTemplateClick(template.id)}
            >
              {/* 模板封面 */}
              {template.cover_image_url ? (
                <Image
                  className='template-cover'
                  src={template.cover_image_url}
                  mode='aspectFill'
                />
              ) : (
                <View className='template-cover placeholder'>
                  <Text className='placeholder-icon'>📄</Text>
                </View>
              )}

              {/* 模板信息 */}
              <View className='template-info'>
                <Text className='template-name'>{template.template_name}</Text>
                <Text className='template-subtitle'>{template.description}</Text>
              </View>

              {/* 底部操作区 */}
              <View className='template-footer'>
                <Text className={`template-price ${template.is_free ? 'free' : ''}`}>
                  {template.is_free ? '免费' : `¥${template.price}`}
                </Text>
                <View className={`action-button ${template.is_free ? 'outline' : 'primary'}`}>
                  <Text className='action-text'>
                    {template.is_free ? '立即查看' : '立即解锁'}
                  </Text>
                </View>
              </View>
            </View>
          ))
        )}
      </ScrollView>
    </View>
  )
}
