// 全局类型定义文件

// 咨询表单数据
export type ConsultationFormData = {
  name: string
  company: string
  consult_type: string
  problem: string
  contact: string
  agree: boolean
}

// 参数数据类型
export type ParameterData = {
  id: number
  parameter_name: string
  material_category: string
  is_core: boolean
  definition?: string
  test_standard?: string
  standard_unit?: string
}

// 模板数据类型
export type TemplateData = {
  id: number
  template_name: string
  template_category: string
  price: number
  is_free: boolean
  cover_image?: string
  applicable_scenarios?: string
  download_count: number
}
