# 绝缘材料参数工具 - 小程序前端

基于 Taro 框架开发的微信小程序，提供参数查询、模板下载、轻咨询预约等功能。

## 环境要求

- Node.js >= 16
- npm >= 8

## 快速开始

### 1. 安装依赖

```bash
npm install
```

### 2. 开发调试

```bash
# 微信小程序
npm run dev:weapp

# H5 (用于浏览器调试)
npm run dev:h5
```

### 3. 构建生产版本

```bash
npm run build:weapp:prod
```

## 项目结构

```
frontend/
├── src/
│   ├── pages/           # 页面
│   │   ├── home/        # 首页
│   │   ├── parameter/   # 参数查询
│   │   ├── template/    # 模板库
│   │   └── profile/     # 我的
│   ├── components/      # 组件
│   ├── services/        # API 服务
│   ├── utils/           # 工具函数
│   ├── types/           # TypeScript 类型定义
│   └── assets/          # 静态资源
└── config/              # 配置文件
```

## 设计规范

- 主色: #1A5F7A
- 辅助色: #F5F7FA, #333333
- 强调色: #FF7D00
- 禁用色: #CCCCCC
