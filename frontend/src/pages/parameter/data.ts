export const MATERIAL_CATEGORIES = [
  { value: '玻纤板(FR-4/G11)', label: '玻纤板(FR-4/G11)' },
  { value: 'PI板', label: 'PI板' },
  { value: '特种塑胶通用', label: '特种塑胶通用' },
]

export const SAMPLE_DATA = {
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

export function getCategoryIndex(value) {
  return MATERIAL_CATEGORIES.findIndex(category => category.value === value)
}

export function getFilteredParameters(categoryIndex, searchText) {
  const category = MATERIAL_CATEGORIES[categoryIndex] || MATERIAL_CATEGORIES[0]
  const source = SAMPLE_DATA[category.value] || []
  const normalizedQuery = searchText.trim().toLowerCase()

  if (!normalizedQuery) {
    return source
  }

  return source.filter(parameter => parameter.param_name.toLowerCase().includes(normalizedQuery))
}
