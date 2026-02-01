import { useState, useEffect } from 'react'
import { View, Text, ScrollView } from '@tarojs/components'
import Taro, { useRouter } from '@tarojs/taro'
import { parameterAPI, userAPI } from '../../../services/api'
import './index.scss'

interface ParameterDetail {
  id: number
  material_category: string
  param_name: string
  param_definition: string | null
  test_standard: string | null
  standard_unit: string | null
  user_focus: string | null
  marking_spec: string | null
  remark: string | null
}

export default function ParameterDetail() {
  const router = useRouter()
  const { id } = router.params
  const [parameter, setParameter] = useState<ParameterDetail | null>(null)
  const [isFavorited, setIsFavorited] = useState(false)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (id) {
      loadParameter()
      checkFavorite()
    }
  }, [id])

  const loadParameter = async () => {
    setLoading(true)
    try {
      const data: any = await parameterAPI.getDetail(Number(id))
      setParameter(data)
    } catch (error) {
      console.error('加载参数详情失败:', error)
      Taro.showToast({ title: '加载失败', icon: 'none' })
    } finally {
      setLoading(false)
    }
  }

  const checkFavorite = async () => {
    try {
      const data: any = await userAPI.getFavorites('parameter')
      setIsFavorited(data.favorite_ids.includes(Number(id)))
    } catch (error) {
      console.error('检查收藏状态失败:', error)
    }
  }

  const handleFavorite = async () => {
    try {
      if (isFavorited) {
        await userAPI.removeFavorite('parameter', Number(id))
        setIsFavorited(false)
        Taro.showToast({ title: '取消收藏', icon: 'success' })
      } else {
        await userAPI.addFavorite('parameter', Number(id))
        setIsFavorited(true)
        Taro.showToast({ title: '收藏成功', icon: 'success' })
      }
    } catch (error) {
      console.error('收藏操作失败:', error)
      Taro.showToast({ title: '操作失败', icon: 'none' })
    }
  }

  const handleBack = () => {
    Taro.navigateBack()
  }

  if (loading) {
    return (
      <View className='parameter-detail-page'>
        <View className='loading'>
          <Text>加载中...</Text>
        </View>
      </View>
    )
  }

  if (!parameter) {
    return (
      <View className='parameter-detail-page'>
        <View className='error'>
          <Text>参数不存在</Text>
        </View>
      </View>
    )
  }

  return (
    <View className='parameter-detail-page'>
      {/* 顶部标题 */}
      <View className='header'>
        <View className='back-btn' onClick={handleBack}>
          <Text>←</Text>
        </View>
        <Text className='title'>{parameter.param_name}</Text>
      </View>

      {/* 参数详情 */}
      <ScrollView scrollY className='detail-content'>
        <View className='detail-section'>
          <Text className='section-label'>参数定义</Text>
          <Text className='section-value'>{parameter.param_definition || '暂无'}</Text>
        </View>

        <View className='detail-section'>
          <Text className='section-label'>测试标准</Text>
          <Text className='section-value'>{parameter.test_standard || '暂无'}</Text>
        </View>

        <View className='detail-section'>
          <Text className='section-label'>标准单位</Text>
          <Text className='section-value'>{parameter.standard_unit || '暂无'}</Text>
        </View>

        <View className='detail-section'>
          <Text className='section-label'>客户关注点</Text>
          <Text className='section-value'>{parameter.user_focus || '暂无'}</Text>
        </View>

        <View className='detail-section'>
          <Text className='section-label'>标注规范</Text>
          <Text className='section-value'>{parameter.marking_spec || '暂无'}</Text>
        </View>

        {parameter.remark && (
          <View className='detail-section'>
            <Text className='section-label'>备注</Text>
            <Text className='section-value'>{parameter.remark}</Text>
          </View>
        )}
      </ScrollView>

      {/* 底部按钮 */}
      <View className='footer-buttons'>
        <View
          className={`btn favorite-btn ${isFavorited ? 'favorited' : ''}`}
          onClick={handleFavorite}
        >
          <Text>{isFavorited ? '已收藏' : '加入收藏'}</Text>
        </View>
        <View className='btn back-btn-footer' onClick={handleBack}>
          <Text>返回列表</Text>
        </View>
      </View>
    </View>
  )
}
