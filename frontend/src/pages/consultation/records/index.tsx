import { View, Text, ScrollView, Checkbox } from '@tarojs/components'
import { useState, useEffect } from 'react'
import Taro from '@tarojs/taro'
import { consultationAPI } from '../../../services/api'
import './index.scss'

interface Consultation {
  id: number
  name: string
  company?: string
  consult_type: string
  problem: string
  contact: string
  status: string
  user_id: number
  order_id?: number
  created_at: string
  updated_at: string
}

export default function ConsultationRecords() {
  const [consultations, setConsultations] = useState<Consultation[]>([])
  const [selectedIds, setSelectedIds] = useState<number[]>([])
  const [currentStatus, setCurrentStatus] = useState<string>('')
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    loadConsultations(currentStatus)
  }, [currentStatus])

  const loadConsultations = async (status: string) => {
    setLoading(true)
    try {
      const params = status ? { status } : {}
      const data = await consultationAPI.getAdminList(params)
      setConsultations(data as Consultation[])
      setSelectedIds([]) // 清空选择
    } catch (error) {
      console.error('加载咨询记录失败:', error)
      Taro.showToast({ title: '加载失败', icon: 'none' })
    } finally {
      setLoading(false)
    }
  }

  const handleCheckboxChange = (id: number) => {
    setSelectedIds(prev => {
      if (prev.includes(id)) {
        return prev.filter(selectedId => selectedId !== id)
      } else {
        return [...prev, id]
      }
    })
  }

  const handleSelectAll = () => {
    if (selectedIds.length === consultations.length) {
      // 全部已选中，取消全选
      setSelectedIds([])
    } else {
      // 选中全部
      setSelectedIds(consultations.map(c => c.id))
    }
  }

  const handleProcess = () => {
    if (selectedIds.length === 0) {
      Taro.showToast({ title: '请先选择记录', icon: 'none' })
      return
    }

    Taro.showActionSheet({
      itemList: ['标记为已完成', '标记为已取消'],
      success: (res) => {
        if (res.tapIndex === 0) {
          handleBatchUpdate('已完成')
        } else if (res.tapIndex === 1) {
          handleBatchUpdate('已取消')
        }
      }
    })
  }

  const handleBatchUpdate = async (newStatus: string) => {
    try {
      Taro.showLoading({ title: '处理中...' })
      await consultationAPI.batchUpdate({
        consultation_ids: selectedIds,
        status: newStatus
      })
      Taro.hideLoading()
      Taro.showToast({ title: '更新成功', icon: 'success' })
      // 刷新列表
      loadConsultations(currentStatus)
    } catch (error) {
      Taro.hideLoading()
      console.error('批量更新失败:', error)
      Taro.showToast({ title: '更新失败', icon: 'none' })
    }
  }

  const handleTabChange = (status: string) => {
    setCurrentStatus(status)
  }

  const truncateText = (text: string, maxLength: number = 50) => {
    if (text.length <= maxLength) return text
    return text.substring(0, maxLength) + '...'
  }

  const formatDateTime = (dateStr: string) => {
    const date = new Date(dateStr)
    const year = date.getFullYear()
    const month = String(date.getMonth() + 1).padStart(2, '0')
    const day = String(date.getDate()).padStart(2, '0')
    const hours = String(date.getHours()).padStart(2, '0')
    const minutes = String(date.getMinutes()).padStart(2, '0')
    return `${year}-${month}-${day} ${hours}:${minutes}`
  }

  const getStatusBadgeClass = (status: string) => {
    switch (status) {
      case '待沟通':
        return 'status-badge pending'
      case '已完成':
        return 'status-badge completed'
      case '已取消':
        return 'status-badge cancelled'
      default:
        return 'status-badge'
    }
  }

  const isAllSelected = consultations.length > 0 && selectedIds.length === consultations.length

  return (
    <View className='records-container'>
      {/* 状态筛选 */}
      <View className='filter-tabs'>
        <View
          className={currentStatus === '' ? 'tab active' : 'tab'}
          onClick={() => handleTabChange('')}
        >
          全部
        </View>
        <View
          className={currentStatus === '待沟通' ? 'tab active' : 'tab'}
          onClick={() => handleTabChange('待沟通')}
        >
          待沟通
        </View>
        <View
          className={currentStatus === '已完成' ? 'tab active' : 'tab'}
          onClick={() => handleTabChange('已完成')}
        >
          已完成
        </View>
        <View
          className={currentStatus === '已取消' ? 'tab active' : 'tab'}
          onClick={() => handleTabChange('已取消')}
        >
          已取消
        </View>
      </View>

      {/* 全选栏 */}
      {consultations.length > 0 && (
        <View className='select-all-bar'>
          <Checkbox
            checked={isAllSelected}
            onClick={handleSelectAll}
            className='select-all-checkbox'
          />
          <Text className='select-all-text' onClick={handleSelectAll}>
            全选
          </Text>
        </View>
      )}

      {/* 记录列表 */}
      <ScrollView className='records-list' scrollY>
        {loading ? (
          <View className='empty-state'>加载中...</View>
        ) : consultations.length === 0 ? (
          <View className='empty-state'>暂无咨询记录</View>
        ) : (
          consultations.map(consultation => (
            <View key={consultation.id} className='record-item'>
              <View className='checkbox-wrapper'>
                <Checkbox
                  checked={selectedIds.includes(consultation.id)}
                  onClick={() => handleCheckboxChange(consultation.id)}
                />
              </View>
              <View className='record-content'>
                <View className='record-header'>
                  <Text className='record-id'>#{consultation.id}</Text>
                  <View className={getStatusBadgeClass(consultation.status)}>
                    {consultation.status}
                  </View>
                </View>
                <View className='record-info'>
                  <Text className='info-label'>姓名：</Text>
                  <Text className='info-value'>{consultation.name}</Text>
                </View>
                <View className='record-info'>
                  <Text className='info-label'>类型：</Text>
                  <Text className='info-value'>{consultation.consult_type}</Text>
                </View>
                <View className='record-info'>
                  <Text className='info-label'>联系：</Text>
                  <Text className='info-value'>{consultation.contact}</Text>
                </View>
                <View className='record-info'>
                  <Text className='info-label'>问题：</Text>
                  <Text className='info-value problem'>
                    {truncateText(consultation.problem)}
                  </Text>
                </View>
                <View className='record-time'>
                  {formatDateTime(consultation.created_at)}
                </View>
              </View>
            </View>
          ))
        )}
      </ScrollView>

      {/* 底部操作按钮 */}
      {consultations.length > 0 && (
        <View className='bottom-action'>
          <View
            className={selectedIds.length > 0 ? 'action-button active' : 'action-button disabled'}
            onClick={handleProcess}
          >
            处理选中项 ({selectedIds.length})
          </View>
        </View>
      )}
    </View>
  )
}
