import { useState } from 'react'
import { View, Text, Input, Textarea, ScrollView, Picker } from '@tarojs/components'
import Taro from '@tarojs/taro'
import { consultationAPI } from '../../services/api'
import './index.scss'

const CONSULT_TYPES = ['产品参数梳理与合规标注', '1688/淘宝店铺信息架构优化', '工厂实拍素材规范指导']

export default function Consultation() {
  const [formData, setFormData] = useState({
    name: '',
    company: '',
    consult_type: '',
    problem: '',
    contact: '',
    agree: false,
  })

  const [typeIndex, setTypeIndex] = useState(-1)
  const [submitting, setSubmitting] = useState(false)

  // 安全的返回处理
  function handleBack() {
    const pages = Taro.getCurrentPages()
    if (pages.length > 1) {
      Taro.navigateBack()
    } else {
      Taro.switchTab({ url: '/pages/home/index' })
    }
  }

  function handleTypeChange(e) {
    const index = e.detail.value
    setTypeIndex(index)
    setFormData({ ...formData, consult_type: CONSULT_TYPES[index] })
  }

  function handleAgreeChange() {
    setFormData({ ...formData, agree: !formData.agree })
  }

  function validateForm() {
    if (!formData.name.trim()) {
      Taro.showToast({ title: '请填写姓名', icon: 'none' })
      return false
    }
    if (!formData.consult_type) {
      Taro.showToast({ title: '请选择咨询类型', icon: 'none' })
      return false
    }
    if (!formData.problem.trim() || formData.problem.length < 50) {
      Taro.showToast({ title: '问题描述至少50字', icon: 'none' })
      return false
    }
    if (!formData.contact.trim()) {
      Taro.showToast({ title: '请填写联系方式', icon: 'none' })
      return false
    }
    if (!formData.agree) {
      Taro.showToast({ title: '请阅读咨询须知', icon: 'none' })
      return false
    }
    return true
  }

  function handleSubmit() {
    if (!validateForm()) {
      return
    }

    setSubmitting(true)
    consultationAPI.create({
      name: formData.name,
      company: formData.company || undefined,
      consult_type: formData.consult_type,
      problem: formData.problem,
      contact: formData.contact,
    })
      .then(() => {
        Taro.showModal({
          title: '预约成功',
          content: '我们会尽快联系您',
          showCancel: false,
          success: () => {
            Taro.navigateBack()
          },
        })
      })
      .catch(error => {
        console.error('提交失败:', error)
        Taro.showToast({ title: '提交失败，请重试', icon: 'none' })
      })
      .finally(() => {
        setSubmitting(false)
      })
  }

  return (
    <View className='consultation-page'>
      {/* 顶部 */}
      <View className='page-header primary-header'>
        <View className='back-button' onClick={handleBack}>
          <Text className='back-icon'>‹</Text>
        </View>
        <Text className='page-title'>15 分钟轻咨询</Text>
      </View>

      <ScrollView scrollY className='consultation-content'>
        {/* 介绍区 */}
        <View className='intro-section'>
          <Text className='intro-title'>专业轻咨询，解决 3 类核心问题</Text>
          <View className='intro-list'>
            <View className='intro-item'>
              <Text className='item-bullet'>•</Text>
              <Text className='item-text'>产品参数梳理与合规标注</Text>
            </View>
            <View className='intro-item'>
              <Text className='item-bullet'>•</Text>
              <Text className='item-text'>1688/淘宝店铺信息架构优化</Text>
            </View>
            <View className='intro-item'>
              <Text className='item-bullet'>•</Text>
              <Text className='item-text'>工厂实拍素材规范指导</Text>
            </View>
          </View>
        </View>

        {/* 表单区 */}
        <View className='form-section'>
          <View className='form-item'>
            <Text className='form-label form-label-required'>姓名/称呼</Text>
            <Input
              className='form-input'
              placeholder='请输入您的姓名或称呼'
              value={formData.name}
              onInput={(e) => setFormData({ ...formData, name: e.detail.value })}
            />
          </View>

          <View className='form-item'>
            <Text className='form-label form-label-required'>咨询类型</Text>
            <Picker mode='selector' range={CONSULT_TYPES} value={typeIndex} onChange={handleTypeChange}>
              <View className='form-select'>
                <Text className={formData.consult_type ? '' : 'placeholder'}>
                  {formData.consult_type || '请选择咨询类型'}
                </Text>
                <Text className='select-arrow'>▼</Text>
              </View>
            </Picker>
          </View>

          <View className='form-item'>
            <Text className='form-label form-label-required'>问题描述</Text>
            <Textarea
              className='form-textarea'
              placeholder='请简要描述您的问题（至少50字）'
              value={formData.problem}
              onInput={(e) => setFormData({ ...formData, problem: e.detail.value })}
              maxlength={500}
            />
            <Text className='char-count'>{formData.problem.length}/500</Text>
          </View>

          <View className='form-item'>
            <Text className='form-label form-label-required'>微信/电话</Text>
            <Input
              className='form-input'
              placeholder='请输入您的联系方式'
              value={formData.contact}
              onInput={(e) => setFormData({ ...formData, contact: e.detail.value })}
            />
          </View>

          <View className='form-item'>
            <Text className='form-label'>公司/店铺名称</Text>
            <Input
              className='form-input'
              placeholder='选填'
              value={formData.company}
              onInput={(e) => setFormData({ ...formData, company: e.detail.value })}
            />
          </View>

          {/* 同意条款 */}
          <View className='agree-section'>
            <View className={`checkbox ${formData.agree ? 'checked' : ''}`} onClick={handleAgreeChange}>
              {formData.agree && <Text className='check-mark'>✓</Text>}
            </View>
            <Text className='agree-text'>已阅读咨询须知</Text>
          </View>
        </View>

        {/* 价格说明区 */}
        <View className='price-section'>
          <Text className='price-title'>99 元/15 分钟</Text>
          <View className='price-list'>
            <View className='price-item'>
              <Text className='price-bullet'>•</Text>
              <Text className='price-text'>预约后微信沟通确认</Text>
            </View>
            <View className='price-item'>
              <Text className='price-bullet'>•</Text>
              <Text className='price-text'>提供 1 个核心问题+3 个可执行动作</Text>
            </View>
            <View className='price-item'>
              <Text className='price-bullet'>•</Text>
              <Text className='price-text'>交付文字版总结</Text>
            </View>
          </View>
        </View>
      </ScrollView>

      {/* 底部提交按钮 */}
      <View className='submit-footer'>
        <View className={`submit-button ${submitting ? 'disabled' : ''}`} onClick={handleSubmit}>
          <Text className='submit-text'>{submitting ? '提交中...' : '提交预约'}</Text>
        </View>
      </View>
    </View>
  )
}
