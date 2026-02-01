import { useState, useEffect } from 'react'
import { View, Text, ScrollView, Image } from '@tarojs/components'
import Taro from '@tarojs/taro'
import { userAPI } from '../../services/api'
import './index.scss'

interface UserInfo {
  id: number
  nickname: string
  avatar_url: string | null
}

export default function Profile() {
  const [userInfo, setUserInfo] = useState<UserInfo | null>(null)
  const [isLoggedIn, setIsLoggedIn] = useState(false)

  useEffect(() => {
    checkLoginStatus()
  }, [])

  const checkLoginStatus = async () => {
    try {
      // TODO: 检查登录状态，从本地存储获取token
      // 模拟登录状态
      const data: any = await userAPI.getMe()
      setUserInfo(data)
      setIsLoggedIn(true)
    } catch (error) {
      console.log('未登录')
      setIsLoggedIn(false)
    }
  }

  const handleLogin = () => {
    // TODO: 集成微信登录
    Taro.showModal({
      title: '提示',
      content: '即将调用微信登录授权',
      success: (res) => {
        if (res.confirm) {
          // 模拟登录成功
          setUserInfo({
            id: 1,
            nickname: '微信用户',
            avatar_url: null,
          })
          setIsLoggedIn(true)
          Taro.showToast({ title: '登录成功', icon: 'success' })
        }
      },
    })
  }

  const handleNavigate = (page: string) => {
    const pages: Record<string, string> = {
      favorites: '/pages/profile/favorites/index',
      orders: '/pages/profile/orders/index',
      downloads: '/pages/profile/downloads/index',
      feedback: '/pages/profile/feedback/index',
      contact: '/pages/profile/contact/index',
      help: '/pages/profile/help/index',
    }

    if (pages[page]) {
      Taro.navigateTo({ url: pages[page] })
    }
  }

  return (
    <ScrollView scrollY className='profile-page'>
      {/* 用户信息区 */}
      <View className='user-section'>
        <View className='user-info'>
          <View className='avatar'>
            {userInfo?.avatar_url ? (
              <Image className='avatar-image' src={userInfo.avatar_url} />
            ) : (
              <Text className='avatar-placeholder'>👤</Text>
            )}
          </View>
          <View className='user-details'>
            <Text className='nickname'>
              {isLoggedIn ? userInfo?.nickname || '微信用户' : '未登录'}
            </Text>
          </View>
          {!isLoggedIn && (
            <View className='login-btn' onClick={handleLogin}>
              <Text>微信快捷登录</Text>
            </View>
          )}
        </View>
      </View>

      {/* 我的服务区 */}
      <View className='section-block'>
        <Text className='section-title'>我的服务</Text>
        <View className='menu-list'>
          <View className='menu-item' onClick={() => handleNavigate('favorites')}>
            <View className='menu-left'>
              <Text className='menu-icon'>⭐</Text>
              <Text className='menu-text'>我的收藏</Text>
            </View>
            <Text className='menu-arrow'>→</Text>
          </View>
          <View className='menu-item' onClick={() => handleNavigate('orders')}>
            <View className='menu-left'>
              <Text className='menu-icon'>📋</Text>
              <Text className='menu-text'>我的订单</Text>
            </View>
            <Text className='menu-arrow'>→</Text>
          </View>
          <View className='menu-item' onClick={() => handleNavigate('downloads')}>
            <View className='menu-left'>
              <Text className='menu-icon'>⬇️</Text>
              <Text className='menu-text'>下载记录</Text>
            </View>
            <Text className='menu-arrow'>→</Text>
          </View>
        </View>
      </View>

      {/* 常用工具区 */}
      <View className='section-block'>
        <Text className='section-title'>常用工具</Text>
        <View className='menu-list'>
          <View className='menu-item' onClick={() => handleNavigate('feedback')}>
            <View className='menu-left'>
              <Text className='menu-icon'>💬</Text>
              <Text className='menu-text'>意见反馈</Text>
            </View>
            <Text className='menu-arrow'>→</Text>
          </View>
          <View className='menu-item' onClick={() => handleNavigate('contact')}>
            <View className='menu-left'>
              <Text className='menu-icon'>📞</Text>
              <Text className='menu-text'>联系我们</Text>
            </View>
            <Text className='menu-arrow'>→</Text>
          </View>
          <View className='menu-item' onClick={() => handleNavigate('help')}>
            <View className='menu-left'>
              <Text className='menu-icon'>❓</Text>
              <Text className='menu-text'>使用帮助</Text>
            </View>
            <Text className='menu-arrow'>→</Text>
          </View>
        </View>
      </View>

      {/* 底部信息 */}
      <View className='footer-info'>
        <Text className='version'>版本号：V1.0</Text>
        <Text className='disclaimer'>
          免责声明：数据仅供参考，实际以国标/厂商检测报告为准
        </Text>
      </View>
    </ScrollView>
  )
}
