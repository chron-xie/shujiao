import { useState } from 'react'
import { View, Text, Input, Textarea, ScrollView, Picker } from '@tarojs/components'
import Taro from '@tarojs/taro'
import { consultationAPI } from '../../services/api'
import './index.scss'

const CONSULT_TYPES = ['参数', '店铺', '实拍', '其他']

interface FormData {
  name: string
  company: string
  consult_type: string
  problem: string
  contact: string
  agree: boolean
}

export default function Consultation() {
  const [formData, setFormData] = useState<FormData>({
    name: '',
    company: '',
    consult_type: '',
    problem: '',
    contact: '',
    agree: false,
  })

  const [typeIndex, setTypeIndex] = useState(0)
  const [submitting, setSubmitting] = useState(false)

  const handleNameChange = (e: any) => {
    setFormData({ ...formData, name: e.detail.value })
  }

  const handleCompanyChange = (e: any) => {
    setFormData({ ...formData, company: e.detail.value })
  }

  const handleTypeChange = (e: any) => {
    const index = e.detail.value
    setTypeIndex(index)
    setFormData({ ...formData, consult_type: CONSULT_TYPES[index] })
  }

  const handleProblemChange = (e: any) => {
    setFormData({ ...formData, problem: e.detail.value })
  }

  const handleContactChange = (e: any) => {
    setFormData({ ...formData, contact: e.detail.value })
  }

  const handleAgreeChange = () => {
    setFormData({ ...formData, agree: !formData.agree })
  }

  const validateForm = (): boolean => {
    if (!formData.name.trim()) {
      Taro.showToast({ title: '请填写姓名', icon: 'none' })
      return false
    }

    if (!formData.consult_type) {
      Taro.showToast({ title: '请选择咨询类型', icon: 'none' })
      return false
    }

    if (!formData.problem.trim()) {
      Taro.showToast({ title: '请描述您的问题', icon: 'none' })
      return false
    }

    if (!formData.contact.trim()) {
      Taro.showToast({ title: '请填写联系方式', icon: 'none' })
      return false
    }

    if (!formData.agree) {
      Taro.showToast({ title: '请阅读并同意咨询须知', icon: 'none' })
      return false
    }

    return true
  }

  const handleSubmit = async () => {
    if (!validateForm()) {
      return
    }

    setSubmitting(true)
    try {
      await consultationAPI.create({
        name: formData.name,
        company: formData.company || undefined,
        consult_type: formData.consult_type,
        problem: formData.problem,
        contact: formData.contact,
      })

      // 显示预约成功弹窗
      Taro.showModal({
        title: '预约成功！',
        content: '请添加微信 shujiao2026 沟通后续事宜',
        confirmText: '复制微信',
        cancelText: '确定',
        success: (res) => {
          if (res.confirm) {
            Taro.setClipboardData({
              data: 'shujiao2026',
              success: () => {
                Taro.showToast({ title: '微信号已复制', icon: 'success' })
                // 返回首页
                setTimeout(() => {
                  Taro.switchTab({ url: '/pages/home/index' })
                }, 1500)
              },
            })
          } else {
            Taro.switchTab({ url: '/pages/home/index' })
          }
        },
      })
    } catch (error) {
      console.error('提交预约失败:', error)
      Taro.showToast({ title: '提交失败，请重试', icon: 'none' })
    } finally {
      setSubmitting(false)
    }
  }

  const handleBack = () => {
    Taro.navigateBack()
  }

  return (
    <View className='consultation-page'>
      {/* 顶部导航 */}
      <View className='header'>
        <View className='back-btn' onClick={handleBack}>
          <Text>←</Text>
        </View>
        <Text className='title'>15分钟轻咨询</Text>
      </View>

      <ScrollView scrollY className='consultation-content'>
        {/* 咨询介绍 */}
        <View className='intro-section'>
          <Text className='intro-title'>专业轻咨询，解决3类核心问题</Text>
          <View className='intro-list'>
            <View className='intro-item'>
              <Text className='item-icon'>✓</Text>
              <Text className='item-text'>产品参数梳理与合规标注</Text>
            </View>
            <View className='intro-item'>
              <Text className='item-icon'>✓</Text>
              <Text className='item-text'>1688/淘宝店铺信息架构优化</Text>
            </View>
            <View className='intro-item'>
              <Text className='item-icon'>✓</Text>
              <Text className='item-text'>工厂实拍素材规范指导</Text>
            </View>
          </View>
        </View>

        {/* 预约表单 */}
        <View className='form-section'>
          <View className='form-item'>
            <Text className='form-label'>姓名/称呼 *</Text>
            <Input
              className='form-input'
              placeholder='请输入姓名/称呼'
              value={formData.name}
              onInput={handleNameChange}
            />
          </View>

          <View className='form-item'>
            <Text className='form-label'>咨询类型 *</Text>
            <Picker mode='selector' range={CONSULT_TYPES} onChange={handleTypeChange}>
              <View className='form-picker'>
                <Text className={formData.consult_type ? 'selected' : 'placeholder'}>
                  {formData.consult_type || '请选择咨询类型'}
                </Text>
                <Text className='arrow'>▼</Text>
              </View>
            </Picker>
          </View>

          <View className='form-item'>
            <Text className='form-label'>问题描述 *</Text>
            <Textarea
              className='form-textarea'
              placeholder='请简要描述你的核心问题'
              value={formData.problem}
              onInput={handleProblemChange}
              maxlength={500}
            />
          </View>

          <View className='form-item'>
            <Text className='form-label'>微信/电话 *</Text>
            <Input
              className='form-input'
              placeholder='请输入微信或电话，便于沟通'
              value={formData.contact}
              onInput={handleContactChange}
            />
          </View>

          <View className='form-item'>
            <Text className='form-label'>公司/店铺名称</Text>
            <Input
              className='form-input'
              placeholder='可选，便于精准对接'
              value={formData.company}
              onInput={handleCompanyChange}
            />
          </View>

          {/* 同意条款 */}
          <View className='form-item agree-item'>
            <View
              className={`checkbox ${formData.agree ? 'checked' : ''}`}
              onClick={handleAgreeChange}
            >
              {formData.agree && <Text className='check-icon'>✓</Text>}
            </View>
            <Text className='agree-text'>已阅读咨询须知</Text>
          </View>
        </View>

        {/* 价格与说明 */}
        <View className='price-section'>
          <Text className='price-text'>99元/15分钟</Text>
          <View className='notes-list'>
            <Text className='note-item'>• 预约后微信沟通确认</Text>
            <Text className='note-item'>• 提供1个核心问题+3个可执行动作</Text>
            <Text className='note-item'>• 交付文字版总结</Text>
          </View>
        </View>
      </ScrollView>

      {/* 提交按钮 */}
      <View className='footer-buttons'>
        <View
          className={`btn submit-btn ${submitting ? 'disabled' : ''}`}
          onClick={submitting ? undefined : handleSubmit}
        >
          <Text>{submitting ? '提交中...' : '提交预约'}</Text>
        </View>
      </View>
    </View>
  )
}
