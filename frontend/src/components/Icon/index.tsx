import { Text } from '@tarojs/components'
import './index.scss'

export default function Icon(props) {
  const { type, size = 48, color = 'currentColor' } = props

  // 使用 Unicode 字符和 emoji，兼容性更好
  const iconMap = {
    book: '📖',
    folder: '📁',
    camera: '📷',
    chat: '💬',
    search: '🔍',
    document: '📄',
    scale: '⚖️',
    list: '📑'
  }

  return (
    <Text
      className="icon-wrapper"
      style={{
        fontSize: `${size}rpx`,
        color: color,
        display: 'inline-block',
        lineHeight: 1,
        filter: color === '#FFFFFF' ? 'brightness(2) saturate(0)' : 'none'
      }}
    >
      {iconMap[type] || ''}
    </Text>
  )
}
