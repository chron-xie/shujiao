# 绝缘材料参数工具

> 查参数、套模板、懂规范 - 工业材料从业者的随身工具

特种塑胶/绝缘材料行业工具小程序，提供参数标准查询、行业模板下载、轻量咨询预约服务。

## 项目简介

**核心定位**: 为特种塑胶/绝缘材料行业从业者（工厂技术员、电商运营、采购工程师、产品选型人员）提供：
- 📊 **参数标准查询** - CTI、Tg、击穿电压等专业参数速查
- 📋 **行业模板库** - 参数表、店铺架构、实拍SOP、FAQ话术模板
- 💬 **轻量咨询** - 15分钟专业咨询服务

**用户价值**:
- 专业: 整合行业核心参数、国标/测试标准、标注规范
- 高效: 可直接编辑的标准化模板，降低工厂店铺搭建时间成本
- 便捷: 轻量化、高性价比的行业咨询服务

## 技术栈

### 前端 (Frontend)
- **框架**: Taro 4.x (React + TypeScript)
- **平台**: 微信小程序
- **UI**: 工业风极简设计
- **状态管理**: React Hooks

### 后端 (Backend)
- **框架**: FastAPI (Python 3.12)
- **ORM**: SQLAlchemy (async)
- **数据库**: MySQL
- **认证**: WeChat OAuth
- **支付**: WeChat Pay

### 开发工具
- **前端**: Node.js 16+, npm
- **后端**: Conda (Python 3.12)
- **版本控制**: Git

## 快速开始

### 环境准备

**前端环境**:
```bash
# 确保安装 Node.js 16+ 和 npm
node --version  # v16.0.0+
npm --version   # 8.0.0+
```

**后端环境**:
```bash
# 确保安装 Conda
conda --version

# 创建并激活环境
conda env create -f backend/environment.yml
conda activate shujiao
```

### 前端开发

```bash
cd frontend

# 安装依赖
npm install

# 启动微信小程序开发模式
npm run dev:weapp

# 在微信开发者工具中打开 frontend/dist 目录
```

### 后端开发

```bash
cd backend

# 激活环境
conda activate shujiao

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件

# 启动开发服务器
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 访问 API 文档
# http://localhost:8000/docs
```

## 项目结构

```
shujiao/
├── frontend/              # Taro 微信小程序
│   ├── src/
│   │   ├── pages/        # 页面 (home, parameter, template, profile)
│   │   ├── components/   # 组件
│   │   ├── services/     # API 服务
│   │   ├── utils/        # 工具函数
│   │   └── assets/       # 静态资源
│   └── config/           # 配置文件
│
├── backend/              # FastAPI 后端
│   ├── app/
│   │   ├── api/v1/       # API 路由
│   │   ├── core/         # 核心配置
│   │   ├── models/       # 数据库模型
│   │   ├── schemas/      # Pydantic schemas
│   │   ├── services/     # 业务逻辑
│   │   └── db/           # 数据库
│   └── tests/            # 测试
│
├── docs/                 # 项目文档
│   ├── PRD V1.0.docx     # 产品需求文档
│   └── 低代码搭建指南.docx
│
└── CLAUDE.md             # Claude Code 开发指南
```

## 核心功能

### 1️⃣ 首页
- 核心功能入口 (2×2网格)
- 热门工具推荐 (横向滚动)
- 最近更新列表

### 2️⃣ 参数查询
- 材料分类 Tab (玻纤板/PI板/特种塑胶)
- 参数列表 + 搜索
- 参数详情 (定义/标准/单位/关注点/规范)
- 收藏功能

### 3️⃣ 模板库
- 模板分类 Tab (参数表/店铺架构/实拍SOP/FAQ话术)
- 免费/付费筛选
- 微信支付 (9.9元/19.9元/29.9元/199元会员)
- 云盘下载 (阿里云盘/腾讯微云)

### 4️⃣ 轻咨询预约
- 预约表单 (姓名/类型/问题/联系方式)
- 99元/15分钟
- 微信预约沟通

### 5️⃣ 我的
- 用户信息 (微信登录)
- 我的收藏/订单/下载记录
- 意见反馈/联系我们/使用帮助

## 设计规范

### 色彩系统
- 主色: `#1A5F7A` (深蓝 - 工业专业感)
- 辅助色: `#F5F7FA` (浅灰), `#333333` (深灰)
- 强调色: `#FF7D00` (橙色 - 付费/收藏)
- 禁用色: `#CCCCCC`

### 视觉风格
- 工业风极简设计
- 无渐变、无阴影、无复杂装饰
- 圆角 4px，间距 12/16/24px
- 信息优先，视觉服务功能

## 数据库配置

**生产环境**:
- Host: 47.116.114.44
- User: root
- Password: A123456z
- Database: shujiao

**重要**: 使用环境变量管理敏感信息，不要提交到 Git

## 开发文档

详细开发指南请参考 [CLAUDE.md](./CLAUDE.md)，包含：
- 完整命令参考
- 项目架构详解
- 核心功能业务逻辑
- 设计系统规范
- 常见问题解决
- 测试与部署指南

## 版本规划

### MVP V1.0 (当前)
- 核心功能: 参数查询、模板库、轻咨询、用户中心
- 开发周期: 3天
- 目标: 验证用户需求与付费意愿

### V2.0 (计划)
- 参数对比工具
- 合规检测
- 素材规范查询
- 会员体系

### V3.0 (规划)
- 行业供需对接
- 企业定制版
- 行业资讯
- 付费课程

## License

Copyright © 2026 绝缘材料参数工具团队

---

**免责声明**: 数据仅供参考，实际以国标/厂商检测报告为准
