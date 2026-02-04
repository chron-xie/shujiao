export default {
  pages: [
    'pages/home/index',
    'pages/parameter/index',
    'pages/parameter/detail/index',
    'pages/template/index',
    'pages/template/detail/index',
    'pages/profile/index',
    'pages/consultation/index',
    'pages/consultation/records/index'
  ],
  window: {
    backgroundTextStyle: 'light',
    navigationBarBackgroundColor: '#1A5F7A',
    navigationBarTitleText: '绝缘材料参数工具',
    navigationBarTextStyle: 'white'
  },
  tabBar: {
    color: '#333333',
    selectedColor: '#1A5F7A',
    backgroundColor: '#ffffff',
    borderStyle: 'black',
    list: [
      {
        pagePath: 'pages/home/index',
        text: '首页',
        iconPath: 'assets/icons/home.png',
        selectedIconPath: 'assets/icons/home-active.png'
      },
      {
        pagePath: 'pages/parameter/index',
        text: '参数查询',
        iconPath: 'assets/icons/search.png',
        selectedIconPath: 'assets/icons/search-active.png'
      },
      {
        pagePath: 'pages/template/index',
        text: '模板库',
        iconPath: 'assets/icons/template.png',
        selectedIconPath: 'assets/icons/template-active.png'
      },
      {
        pagePath: 'pages/profile/index',
        text: '我的',
        iconPath: 'assets/icons/profile.png',
        selectedIconPath: 'assets/icons/profile-active.png'
      }
    ]
  }
}
