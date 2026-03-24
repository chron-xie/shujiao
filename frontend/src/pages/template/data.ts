export const TEMPLATE_CATEGORIES = [
  { value: '参数表模板', label: '参数表模板' },
  { value: '店铺架构模板', label: '店铺架构模板' },
  { value: '实拍SOP模板', label: '实拍 SOP 模板' },
  { value: 'FAQ话术模板', label: 'FAQ 话术模板' },
] as const

export type TemplateCategory = (typeof TEMPLATE_CATEGORIES)[number]['value']

export const FILTER_OPTIONS = [
  { value: 'all', label: '全部' },
  { value: 'free', label: '免费' },
  { value: 'paid', label: '付费' },
] as const

export type FilterType = (typeof FILTER_OPTIONS)[number]['value']

export type TemplateItem = {
  id: number
  template_name: string
  template_category: TemplateCategory
  cover_image_url: string
  description: string
  price: number
  is_free: boolean
}

export const SAMPLE_TEMPLATES: Record<TemplateCategory, TemplateItem[]> = {
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
