# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

绝缘材料参数工具 - 特种塑胶/绝缘材料行业工具小程序，提供参数标准查询、行业模板下载、轻量咨询预约服务。

**核心定位**: 工业材料从业者的随身工具 - 查参数、套模板、懂规范

**技术栈**:
- Frontend: Taro (React) + TypeScript - 微信小程序
- Backend: FastAPI + Python 3.12
- Database: MySQL (47.116.114.44)
- Environment: Conda (Python), npm (Node.js)

## Development Commands

### Frontend (Taro Mini-Program)

```bash
cd frontend

# Install dependencies
npm install

# Development (WeChat Mini-Program)
npm run dev:weapp

# Development (H5 for browser testing)
npm run dev:h5

# Build for production
npm run build:weapp:prod

# Linting
npm run lint
npm run lint:fix
```

### Backend (FastAPI)

```bash
cd backend

# Create and activate conda environment
conda env create -f environment.yml
conda activate shujiao

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Development only

# Start development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# API Documentation
# http://localhost:8000/docs (Swagger UI)
# http://localhost:8000/redoc (ReDoc)

# Code formatting
black .
isort .

# Linting
flake8
pylint app/
mypy app/

# Testing
pytest
pytest --cov  # With coverage
```

## Project Architecture

### Frontend Structure

```
frontend/src/
├── pages/              # 4 main tab pages
│   ├── home/          # 首页 - Core feature entry, hot tools, recent updates
│   ├── parameter/     # 参数查询 - Material classification, parameter list/detail
│   ├── template/      # 模板库 - Template categories, paid/free templates, WeChat payment
│   └── profile/       # 我的 - User center, favorites, orders, feedback
├── components/        # Reusable components
├── services/         # API service layer (backend communication)
├── utils/            # Utility functions
├── types/            # TypeScript type definitions
└── assets/           # Static resources (icons, images)
```

**Key Frontend Patterns**:
- 底部 Tab 导航 (4 tabs: 首页, 参数查询, 模板库, 我的)
- 所有页面支持返回操作，核心功能操作 ≤3 步
- 工业风极简设计，无复杂装饰、无渐变、无阴影

### Backend Structure

```
backend/app/
├── api/v1/            # API routes (versioned)
│   └── endpoints/     # Endpoint modules
│       ├── parameters.py      # 参数查询相关
│       ├── templates.py       # 模板库相关
│       ├── consultations.py   # 轻咨询预约
│       └── users.py          # 用户管理
├── core/              # Core configuration (settings, security)
├── models/            # SQLAlchemy ORM models
├── schemas/           # Pydantic schemas (request/response)
├── services/          # Business logic layer
└── db/                # Database session, utilities
```

**Key Backend Patterns**:
- API versioning: `/api/v1/*`
- Async/await for all database operations (aiomysql)
- Pydantic for request/response validation
- Environment-based configuration (.env)

## Core Features & Business Logic

### 1. 参数标准查询 (Parameter Query)
- 3 material categories: 玻纤板 (FR-4/G11), PI板, 特种塑胶通用 (PEEK/PPS/PEI/电木)
- Excel 数据库批量导入: id, material_category, param_name, param_definition, test_standard, standard_unit, user_focus, marking_spec, remark
- 搜索功能: 关键词模糊匹配，实时联想提示
- 参数详情: 定义、测试标准、标准单位、客户关注点、标注规范
- 收藏功能: 本地缓存 + 云端同步

### 2. 模板库 (Template Library)
- 4 template categories: 参数表模板, 店铺架构模板, 实拍SOP模板, FAQ话术模板
- Free/Paid filtering
- WeChat Payment integration: 9.9元、19.9元、29.9元 (single template), 199元 (全库会员)
- Download: 阿里云盘/腾讯微云永久链接
- Excel 导入字段: template_id, template_category, template_name, cover_image_url, description, price, download_url, is_free

### 3. 轻咨询预约 (Consultation Booking)
- Form validation: 姓名, 咨询类型 (参数/店铺/实拍/其他), 问题描述, 微信/电话
- Pricing: 99元/15分钟
- Service: 1个核心问题 + 3个可执行动作 + 文字版总结
- 预约状态: 待沟通/已完成/已取消

### 4. 用户中心 (User Profile)
- WeChat快捷登录
- 我的收藏: 参数收藏、模板收藏
- 我的订单: 模板购买记录、咨询预约记录
- 下载记录: 已购买模板的下载链接
- 意见反馈

## Design System

### Color Palette
```scss
--primary-color: #1A5F7A      // 主色 (标题、核心按钮、选中状态)
--bg-color: #F5F7FA           // 辅助色 (页面/模块背景)
--text-color: #333333         // 辅助色 (正文/标题文字)
--highlight-color: #FF7D00    // 强调色 (付费按钮、收藏状态、核心提示)
--disabled-color: #CCCCCC     // 禁用色 (禁用按钮、次要文字、边框)
```

### Typography
- Font: 微软雅黑 / System sans-serif
- Sizes: 标题 16-18px, 正文 14-15px, 辅助文字 12px, 按钮文字 14px

### Layout Principles
- Spacing: 12px, 16px, 24px (统一间距)
- Border radius: 4px (所有模块)
- Page margins: 16px
- Module spacing: 24px
- **极简工业风**: 无渐变、无阴影、无复杂装饰，信息优先、视觉服务功能

## Database Configuration

**Production Database**:
- Host: 47.116.114.44
- User: root
- Password: A123456z
- Port: 3306
- Database: shujiao

**IMPORTANT**:
- Use environment variables (.env) for credentials, never commit to git
- Backend uses aiomysql for async MySQL operations
- SQLAlchemy ORM for models
- Alembic for database migrations

## WeChat Mini-Program Configuration

**App Info**:
- Name: 绝缘材料参数工具
- Slogan: 查参数、套模板、懂规范，工业材料从业者的随身工具
- Category: 工具-办公-查询工具
- Package size: ≤2MB
- Individual developer eligible for launch

**WeChat Integration**:
- WeChat login (微信快捷登录)
- WeChat payment (模板购买、咨询预约)
- Configure WECHAT_APP_ID, WECHAT_APP_SECRET in backend/.env

## Performance Requirements

- Page load time: ≤2 seconds
- Response time: ≤0.5 seconds (buttons, navigation, search)
- Concurrent users: ≥1000 (no data delay or functional issues)
- Compatibility: iOS/Android all versions, all screen resolutions

## Development Workflow

### Starting a New Feature

1. **Frontend**: Create page/component in `frontend/src/pages` or `frontend/src/components`
2. **Backend**: Add endpoint in `backend/app/api/v1/endpoints`, create schema in `schemas/`, model in `models/`
3. **Database**: If schema changes needed, create Alembic migration
4. **Testing**: Frontend manual testing in WeChat DevTools, Backend pytest

### Code Style Guidelines

**Frontend**:
- Use TypeScript strict mode
- Functional components with hooks (React)
- Service layer for all API calls (avoid direct fetch in components)
- Follow Taro component best practices

**Backend**:
- Use async/await for all I/O operations
- Pydantic schemas for all request/response
- Business logic in services/, not in endpoints
- Type hints for all functions
- Black + isort for formatting

## Important Notes

### Data Disclaimer
All pages must include: **"数据仅供参考，实际以国标/厂商检测报告为准"**
This is a legal requirement to avoid liability.

### Excel Data Import
- Backend must support Excel batch import for parameters and templates
- Use pandas or openpyxl for Excel processing
- Validate data format before import
- Backend provides update endpoints without requiring mini-program re-submission

### WeChat Payment Flow
1. User clicks "立即解锁" on paid template
2. Frontend calls backend payment API
3. Backend generates WeChat payment order
4. Frontend invokes WeChat payment
5. Payment callback updates order status
6. Display download link after successful payment

### Content Update Strategy
- Backend admin panel for content CRUD (parameters, templates)
- No mini-program re-submission needed for content updates
- Real-time data updates through API

## Common Issues & Solutions

### Frontend
- **Taro build fails**: Check node version (>= 16), clear `dist/` and `node_modules/`, reinstall
- **WeChat DevTools rendering issues**: Use real device testing for accurate results
- **Navigation issues**: Ensure all pages are registered in `app.config.ts`

### Backend
- **Database connection fails**: Check MySQL server status, verify credentials in .env
- **CORS errors**: Update ALLOWED_ORIGINS in backend/app/core/config.py
- **Import errors**: Ensure conda environment is activated, reinstall requirements.txt

### Integration
- **API calls fail**: Verify backend is running, check API_BASE_URL in frontend config
- **WeChat login fails**: Verify WECHAT_APP_ID and WECHAT_APP_SECRET
- **Payment fails**: Check WeChat merchant configuration (WECHAT_MCH_ID, WECHAT_MCH_KEY)

## Testing Strategy

### Frontend Testing
- Manual testing in WeChat DevTools
- Real device testing (iOS/Android)
- Test all navigation flows (no dead ends)
- Verify all forms validate correctly
- Test payment flow with sandbox environment

### Backend Testing
- Unit tests: pytest for services, models, utilities
- Integration tests: API endpoint testing with httpx
- Database tests: Use test database, rollback after tests
- Coverage target: >80%

## Deployment

### Frontend
- Build: `npm run build:weapp:prod`
- Submit to WeChat for review via WeChat DevTools
- Review category: 工具-办公-查询工具

### Backend
- Use uvicorn in production: `uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4`
- Consider using supervisord or systemd for process management
- Set up reverse proxy with Nginx
- Use production database credentials
- Enable HTTPS for API endpoints

## Documentation References

- PRD: `docs/《特种塑胶_绝缘材料工具小程序 PRD（V1.0）》.docx`
- Low-code platform guide: `docs/特种塑胶_绝缘材料行业工具小程序 低代码平台搭建完整提示语.docx`
- Taro docs: https://taro-docs.jd.com
- FastAPI docs: https://fastapi.tiangolo.com
- WeChat Mini-Program docs: https://developers.weixin.qq.com/miniprogram/dev/framework/
