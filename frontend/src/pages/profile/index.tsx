import { useState, useEffect } from 'react'
import { View, Text, ScrollView } from '@tarojs/components'
import Taro from '@tarojs/taro'
import { userAPI } from '../../services/api'
import './index.scss'

export default function Profile() {
  const [userInfo, setUserInfo] = useState(null)
  const [isLoggedIn, setIsLoggedIn] = useState(false)

  useEffect(() => {
    checkLoginStatus()
  }, [])

  function checkLoginStatus() {
    userAPI.getMe()
      .then(data => {
        setUserInfo(data)
        setIsLoggedIn(true)
      })
      .catch(() => {
        setIsLoggedIn(false)
      })
  }

  function handleLogin() {
    Taro.showModal({
      title: '提示',
      content: '即将调用微信登录授权',
      success: (res) => {
        if (res.confirm) {
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

  function handleNavigate(page) {
    Taro.showToast({ title: '功能开发中', icon: 'none' })
  }

  const menuItems = [
    { icon: '❤️', text: '我的收藏', page: 'favorites' },
    { icon: '📋', text: '我的订单', page: 'orders' },
    { icon: '⬇️', text: '下载记录', page: 'downloads' },
    { icon: '💬', text: '意见反馈', page: 'feedback' },
    { icon: '📞', text: '联系我们', page: 'contact' },
    { icon: '❓', text: '使用帮助', page: 'help' },
  ]

  return (
    <ScrollView scrollY className='profile-page'>
      {/* 用户信息区 */}
      <View className='user-section'>
        <View className='user-avatar'>
          <Text className='avatar-icon'>👤</Text>
        </View>
        <View className='user-info'>
          <Text className='user-name'>
            {isLoggedIn ? userInfo?.nickname || '微信用户' : '未登录'}
          </Text>
          {!isLoggedIn && (
            <View className='login-button' onClick={handleLogin}>
              <Text className='login-text'>微信快捷登录</Text>
            </View>
          )}
        </View>
      </View>

      {/* 菜单列表 */}
      <View className='menu-section'>
        {menuItems.map((item, index) => (
          <View
            key={index}
            className='menu-item list-item'
            onClick={() => handleNavigate(item.page)}
          >
            <View className='menu-left'>
              <Text className='menu-icon'>{item.icon}</Text>
              <Text className='menu-text'>{item.text}</Text>
            </View>
            <Text className='list-item-arrow'>›</Text>
          </View>
        ))}
      </View>

      {/* 底部信息 */}
      <View className='footer-section'>
        <Text className='footer-version'>版本号 1.0.0</Text>
        <Text className='footer-disclaimer'>
          数据仅供参考，实际以国标/厂商检测报告为准
        </Text>
      </View>
    </ScrollView>
  )
}
