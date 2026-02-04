module.exports = {
  presets: [
    ['@babel/preset-react', { runtime: 'automatic' }],
    ['taro', {
      framework: 'react',
      ts: false
    }]
  ]
}
