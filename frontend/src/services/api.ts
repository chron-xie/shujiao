import Taro from '@tarojs/taro'

const BASE_URL = 'http://localhost:8000/api/v1'

// interface RequestOptions {
//   method?: 'GET' | 'POST' | 'PUT' | 'DELETE'
//   data?: any
//   header?: any
// }

export async function request(url, options = {}) {
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
      return response.data
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
  getList: (params) =>
    request('/parameters/', { data: params }),

  getDetail: (id) => request(`/parameters/${id}`),
}

// 模板相关API
export const templateAPI = {
  getList: (params) =>
    request('/templates/', { data: params }),

  getDetail: (id) => request(`/templates/${id}`),

  recordDownload: (id) =>
    request(`/templates/${id}/download`, { method: 'POST' }),
}

// 咨询相关API
export const consultationAPI = {
  create: ( data) =>
    request('/consultations/', { method: 'POST', data }),

  getMyList: () => request('/consultations/my'),
}

// 用户相关API
export const userAPI = {
  create: ( data) => request('/users/', { method: 'POST', data }),

  getMe: () => request('/users/me'),

  updateMe: ( data) => request('/users/me', { method: 'PUT', data }),

  addFavorite: (favorite_type, favorite_id) =>
    request('/users/favorites', {
      method: 'POST',
      data: { favorite_type, favorite_id },
    }),

  removeFavorite: (favorite_type, favorite_id) =>
    request('/users/favorites', {
      method: 'DELETE',
      data: { favorite_type, favorite_id },
    }),

  getFavorites: (favorite_type) =>
    request(`/users/favorites/${favorite_type}`),
}
