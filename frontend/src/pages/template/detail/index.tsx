import { useState, useEffect } from 'react'
import { View, Text, ScrollView, Image } from '@tarojs/components'
import Taro, { useRouter } from '@tarojs/taro'
import { templateAPI } from '../../../services/api'
import './index.scss'

interface TemplateDetail {
  id: number
  template_category: string
  template_name: string
  description: string | null
  cover_image_url: string | null
  price: number
  is_free: boolean
  download_url: string | null
  download_count: number
}

export default function TemplateDetail() {
  const router = useRouter()
  const { id } = router.params
  const [template, setTemplate] = useState<TemplateDetail | null>(null)
  const [loading, setLoading] = useState(true)
  const [isPaid, setIsPaid] = useState(false) // TODO: 从订单系统获取

  useEffect(() => {
    if (id) {
      loadTemplate()
    }
  }, [id])

  const loadTemplate = async () => {
    setLoading(true)
    try {
      const data: any = await templateAPI.getDetail(Number(id))
      setTemplate(data)
    } catch (error) {
      console.error('加载模板详情失败:', error)
      Taro.showToast({ title: '加载失败', icon: 'none' })
    } finally {
      setLoading(false)
    }
  }

  const handlePayment = async () => {
    // TODO: 集成微信支付
    Taro.showModal({
      title: '支付提示',
      content: `确认支付 ¥${template?.price} 购买此模板？`,
      success: (res) => {
        if (res.confirm) {
          // 模拟支付成功
          Taro.showToast({ title: '支付成功', icon: 'success' })
          setIsPaid(true)
        }
      },
    })
  }

  const handleDownload = async () => {
    if (!template?.download_url) {
      Taro.showToast({ title: '下载链接不可用', icon: 'none' })
      return
    }

    // 记录下载次数
    try {
      await templateAPI.recordDownload(Number(id))
    } catch (error) {
      console.error('记录下载失败:', error)
    }

    // 复制下载链接
    Taro.setClipboardData({
      data: template.download_url,
      success: () => {
        Taro.showToast({ title: '链接已复制，请在浏览器打开', icon: 'success' })
      },
    })
  }

  const handleBack = () => {
    Taro.navigateBack()
  }

  if (loading) {
    return (
      <View className='template-detail-page'>
        <View className='loading'>
          <Text>加载中...</Text>
        </View>
      </View>
    )
  }

  if (!template) {
    return (
      <View className='template-detail-page'>
        <View className='error'>
          <Text>模板不存在</Text>
        </View>
      </View>
    )
  }

  const canDownload = template.is_free || isPaid

  return (
    <View className='template-detail-page'>
      {/* 顶部导航 */}
      <View className='header'>
        <View className='back-btn' onClick={handleBack}>
          <Text>←</Text>
        </View>
        <Text className='title'>{template.template_name}</Text>
        <View className='price-tag'>
          {template.is_free ? (
            <Text className='free'>免费</Text>
          ) : (
            <Text className='paid'>¥{template.price}</Text>
          )}
        </View>
      </View>

      {/* 模板详情 */}
      <ScrollView scrollY className='detail-content'>
        {/* 封面图 */}
        {template.cover_image_url && (
          <View className='cover-section'>
            <Image
              className='cover-image'
              src={template.cover_image_url}
              mode='aspectFill'
            />
          </View>
        )}

        {/* 适用场景说明 */}
        <View className='detail-section'>
          <Text className='section-label'>适用场景</Text>
          <Text className='section-value'>
            {template.description || '专业模板，开箱即用'}
          </Text>
        </View>

        {/* 包含内容 */}
        <View className='detail-section'>
          <Text className='section-label'>包含内容</Text>
          <Text className='section-value'>
            • 完整模板文件{'\n'}
            • 使用说明文档{'\n'}
            • 示例参考{'\n'}
            • 后续免费更新
          </Text>
        </View>

        {/* 下载统计 */}
        <View className='detail-section'>
          <Text className='section-label'>下载次数</Text>
          <Text className='section-value'>{template.download_count} 次</Text>
        </View>

        {/* 下载链接（仅支付后显示） */}
        {canDownload && template.download_url && (
          <View className='detail-section download-section'>
            <Text className='section-label'>下载链接</Text>
            <View className='download-link' onClick={handleDownload}>
              <Text className='link-text'>{template.download_url}</Text>
              <Text className='copy-btn'>复制</Text>
            </View>
          </View>
        )}
      </ScrollView>

      {/* 底部操作按钮 */}
      <View className='footer-buttons'>
        {template.is_free ? (
          <View className='btn download-btn-footer' onClick={handleDownload}>
            <Text>下载</Text>
          </View>
        ) : canDownload ? (
          <View className='btn download-btn-footer' onClick={handleDownload}>
            <Text>下载</Text>
          </View>
        ) : (
          <View className='btn pay-btn' onClick={handlePayment}>
            <Text>立即支付 ¥{template.price}</Text>
          </View>
        )}
      </View>
    </View>
  )
}
