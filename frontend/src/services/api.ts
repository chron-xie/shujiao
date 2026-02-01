import Taro from '@tarojs/taro'

const BASE_URL = 'http://localhost:8000/api/v1'

interface RequestOptions {
  method?: 'GET' | 'POST' | 'PUT' | 'DELETE'
  data?: any
  header?: any
}

export async function request<T>(url: string, options: RequestOptions = {}): Promise<T> {
  const { method = 'GET', data, header = {} } = options

  try {
    const response = await Taro.request({
      url: `${BASE_URL}${url}`,
      method,
      data,
      header: {
        'Content-Type': 'application/json',
        ...header,
      },
    })

    if (response.statusCode >= 200 && response.statusCode < 300) {
      return response.data as T
    } else {
      throw new Error(`Request failed with status ${response.statusCode}`)
    }
  } catch (error) {
    console.error('API request error:', error)
    throw error
  }
}

// 参数相关API
export const parameterAPI = {
  getList: (params?: { material_category?: string; search?: string }) =>
    request('/parameters/', { data: params }),

  getDetail: (id: number) => request(`/parameters/${id}`),
}

// 模板相关API
export const templateAPI = {
  getList: (params?: { template_category?: string; is_free?: boolean }) =>
    request('/templates/', { data: params }),

  getDetail: (id: number) => request(`/templates/${id}`),

  recordDownload: (id: number) =>
    request(`/templates/${id}/download`, { method: 'POST' }),
}

// 咨询相关API
export const consultationAPI = {
  create: (data: any) =>
    request('/consultations/', { method: 'POST', data }),

  getMyList: () => request('/consultations/my'),
}

// 用户相关API
export const userAPI = {
  create: (data: any) => request('/users/', { method: 'POST', data }),

  getMe: () => request('/users/me'),

  updateMe: (data: any) => request('/users/me', { method: 'PUT', data }),

  addFavorite: (favorite_type: string, favorite_id: number) =>
    request('/users/favorites', {
      method: 'POST',
      data: { favorite_type, favorite_id },
    }),

  removeFavorite: (favorite_type: string, favorite_id: number) =>
    request('/users/favorites', {
      method: 'DELETE',
      data: { favorite_type, favorite_id },
    }),

  getFavorites: (favorite_type: string) =>
    request(`/users/favorites/${favorite_type}`),
}
