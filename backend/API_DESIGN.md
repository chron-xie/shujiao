# API接口设计文档

## 概述

本文档描述绝缘材料参数工具小程序的后端API接口设计，采用RESTful风格，支持微信小程序前端调用。

**基础信息**:
- Base URL: `http://localhost:8000` (开发) / `https://api.example.com` (生产)
- API版本: `/api/v1`
- 数据格式: JSON
- 字符编码: UTF-8

## 通用规范

### 1. 请求格式

**Header**:
```http
Content-Type: application/json
Authorization: Bearer {access_token}  # 需要认证的接口
```

**请求参数位置**:
- GET: Query参数
- POST/PUT/PATCH: Request Body (JSON)
- DELETE: URL Path参数

### 2. 响应格式

**成功响应** (200 OK):
```json
{
  "code": 0,
  "message": "success",
  "data": { /* 响应数据 */ }
}
```

**分页响应**:
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "items": [ /* 数据列表 */ ],
    "total": 100,
    "page": 1,
    "page_size": 20,
    "total_pages": 5
  }
}
```

**错误响应** (4xx/5xx):
```json
{
  "code": 40001,
  "message": "参数验证失败",
  "detail": "姓名不能为空"
}
```

### 3. 错误码规范

| 错误码 | 说明 |
|-------|------|
| 0 | 成功 |
| 40001 | 参数错误 |
| 40100 | 未登录 |
| 40101 | 登录过期 |
| 40300 | 无权限 |
| 40400 | 资源不存在 |
| 40900 | 重复操作 |
| 50000 | 服务器错误 |
| 50001 | 数据库错误 |
| 50002 | 第三方服务错误（微信支付） |

### 4. 认证方式

使用JWT Token认证：
1. 用户通过微信登录获取 `access_token`
2. 需要认证的接口在Header中携带 `Authorization: Bearer {access_token}`
3. Token有效期：7天（可刷新）

## API端点列表

### 用户模块 (User)

| 方法 | 端点 | 说明 | 认证 |
|------|------|------|------|
| POST | `/api/v1/users/login` | 微信登录 | 否 |
| GET | `/api/v1/users/me` | 获取当前用户信息 | 是 |
| PUT | `/api/v1/users/me` | 更新用户信息 | 是 |
| GET | `/api/v1/users/favorites` | 获取收藏列表 | 是 |
| POST | `/api/v1/users/favorites` | 添加收藏 | 是 |
| DELETE | `/api/v1/users/favorites/{id}` | 取消收藏 | 是 |
| GET | `/api/v1/users/orders` | 获取订单列表 | 是 |
| GET | `/api/v1/users/downloads` | 获取下载记录 | 是 |

### 参数查询模块 (Parameter)

| 方法 | 端点 | 说明 | 认证 |
|------|------|------|------|
| GET | `/api/v1/parameters/` | 获取参数列表 | 否 |
| GET | `/api/v1/parameters/{id}` | 获取参数详情 | 否 |
| GET | `/api/v1/parameters/search` | 搜索参数 | 否 |
| GET | `/api/v1/parameters/categories` | 获取材料分类 | 否 |
| GET | `/api/v1/parameters/hot` | 获取热门参数 | 否 |

### 模板库模块 (Template)

| 方法 | 端点 | 说明 | 认证 |
|------|------|------|------|
| GET | `/api/v1/templates/` | 获取模板列表 | 否 |
| GET | `/api/v1/templates/{id}` | 获取模板详情 | 否 |
| GET | `/api/v1/templates/categories` | 获取模板分类 | 否 |
| POST | `/api/v1/templates/{id}/download` | 下载模板 | 是 |

### 咨询预约模块 (Consultation)

| 方法 | 端点 | 说明 | 认证 |
|------|------|------|------|
| POST | `/api/v1/consultations/` | 创建咨询预约 | 是 |
| GET | `/api/v1/consultations/{id}` | 获取咨询详情 | 是 |
| GET | `/api/v1/consultations/` | 获取咨询列表 | 是 |

### 订单模块 (Order)

| 方法 | 端点 | 说明 | 认证 |
|------|------|------|------|
| POST | `/api/v1/orders/` | 创建订单 | 是 |
| GET | `/api/v1/orders/{order_no}` | 获取订单详情 | 是 |
| POST | `/api/v1/orders/{order_no}/pay` | 发起支付 | 是 |
| POST | `/api/v1/orders/wechat-callback` | 微信支付回调 | 否 |

### 反馈模块 (Feedback)

| 方法 | 端点 | 说明 | 认证 |
|------|------|------|------|
| POST | `/api/v1/feedbacks/` | 提交反馈 | 否 |
| GET | `/api/v1/feedbacks/{id}` | 获取反馈详情 | 是 |

---

## 详细接口设计

## 1. 用户模块

### 1.1 微信登录

**POST** `/api/v1/users/login`

**请求参数**:
```json
{
  "code": "081xZXXX"  // 微信小程序 wx.login() 返回的code
}
```

**响应**:
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "Bearer",
    "expires_in": 604800,  // 7天（秒）
    "user": {
      "id": 1,
      "nickname": "微信用户",
      "avatar_url": "https://example.com/avatar.jpg",
      "is_vip": false,
      "vip_expire_at": null
    }
  }
}
```

**业务逻辑**:
1. 使用 `code` 调用微信API获取 `openid`
2. 查询数据库是否存在该用户（根据 `openid`）
3. 不存在则创建新用户
4. 生成JWT Token并返回
5. 更新 `last_login_at`

### 1.2 获取当前用户信息

**GET** `/api/v1/users/me`

**认证**: 必需

**响应**:
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "id": 1,
    "nickname": "张三",
    "avatar_url": "https://example.com/avatar.jpg",
    "phone": "138****5678",
    "is_vip": true,
    "vip_expire_at": "2027-02-01T12:00:00Z",
    "created_at": "2026-01-01T10:00:00Z"
  }
}
```

### 1.3 更新用户信息

**PUT** `/api/v1/users/me`

**认证**: 必需

**请求参数**:
```json
{
  "nickname": "李四",
  "phone": "13800138000"
}
```

**响应**:
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "id": 1,
    "nickname": "李四",
    "phone": "13800138000",
    "updated_at": "2026-02-01T15:30:00Z"
  }
}
```

### 1.4 获取收藏列表

**GET** `/api/v1/users/favorites`

**认证**: 必需

**Query参数**:
- `favorite_type`: 收藏类型（`parameter` | `template` | 不传则全部）
- `page`: 页码（默认1）
- `page_size`: 每页数量（默认20）

**请求示例**:
```
GET /api/v1/users/favorites?favorite_type=parameter&page=1&page_size=20
```

**响应**:
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "items": [
      {
        "id": 1,
        "favorite_type": "parameter",
        "item_id": 5,
        "created_at": "2026-02-01T10:00:00Z",
        "detail": {
          "param_name": "玻璃化温度Tg",
          "material_category": "玻纤板(FR-4/G11)",
          "standard_unit": "℃"
        }
      },
      {
        "id": 2,
        "favorite_type": "template",
        "item_id": 3,
        "created_at": "2026-02-01T11:00:00Z",
        "detail": {
          "template_name": "FR-4玻纤板参数表标准模板",
          "template_category": "参数表模板",
          "price": 0.00,
          "cover_image_url": "https://example.com/cover.jpg"
        }
      }
    ],
    "total": 12,
    "page": 1,
    "page_size": 20,
    "total_pages": 1
  }
}
```

### 1.5 添加收藏

**POST** `/api/v1/users/favorites`

**认证**: 必需

**请求参数**:
```json
{
  "favorite_type": "parameter",  // parameter | template
  "item_id": 5
}
```

**响应**:
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "id": 15,
    "favorite_type": "parameter",
    "item_id": 5,
    "created_at": "2026-02-01T15:30:00Z"
  }
}
```

**错误响应** (重复收藏):
```json
{
  "code": 40900,
  "message": "已收藏该项目"
}
```

### 1.6 取消收藏

**DELETE** `/api/v1/users/favorites/{id}`

**认证**: 必需

**响应**:
```json
{
  "code": 0,
  "message": "success"
}
```

### 1.7 获取订单列表

**GET** `/api/v1/users/orders`

**认证**: 必需

**Query参数**:
- `order_type`: 订单类型（`template` | `consultation` | `vip_membership` | 不传则全部）
- `status`: 订单状态（`pending` | `paid` | `cancelled` | `refunded` | 不传则全部）
- `page`: 页码（默认1）
- `page_size`: 每页数量（默认20）

**响应**:
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "items": [
      {
        "id": 10,
        "order_no": "20260201153045123456",
        "order_type": "template",
        "item_id": 3,
        "item_name": "PEEK特种塑胶全参数表模板",
        "amount": 19.90,
        "status": "paid",
        "paid_at": "2026-02-01T15:31:00Z",
        "created_at": "2026-02-01T15:30:00Z"
      }
    ],
    "total": 5,
    "page": 1,
    "page_size": 20,
    "total_pages": 1
  }
}
```

### 1.8 获取下载记录

**GET** `/api/v1/users/downloads`

**认证**: 必需

**Query参数**:
- `page`: 页码（默认1）
- `page_size`: 每页数量（默认20）

**响应**:
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "items": [
      {
        "id": 25,
        "template_id": 3,
        "template_name": "PEEK特种塑胶全参数表模板",
        "cover_image_url": "https://example.com/cover.jpg",
        "download_url": "https://aliyundrive.com/s/xxx",
        "created_at": "2026-02-01T15:32:00Z"
      }
    ],
    "total": 8,
    "page": 1,
    "page_size": 20,
    "total_pages": 1
  }
}
```

---

## 2. 参数查询模块

### 2.1 获取参数列表

**GET** `/api/v1/parameters/`

**Query参数**:
- `material_category`: 材料分类（`玻纤板(FR-4/G11)` | `PI板` | `特种塑胶通用(PEEK/PPS/PEI/电木)`）
- `search`: 搜索关键词（模糊匹配 `param_name` 和 `param_definition`）
- `is_core`: 是否核心参数（`true` | `false`）
- `page`: 页码（默认1）
- `page_size`: 每页数量（默认20）

**请求示例**:
```
GET /api/v1/parameters/?material_category=玻纤板(FR-4/G11)&page=1&page_size=20
```

**响应**:
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "items": [
      {
        "id": 1,
        "material_category": "玻纤板(FR-4/G11)",
        "param_name": "玻璃化温度Tg",
        "param_definition": "材料从玻璃态到高弹态的转变温度",
        "test_standard": "IPC-TM-650 2.4.25",
        "standard_unit": "℃",
        "is_core": true,
        "view_count": 1250,
        "favorite_count": 85
      },
      {
        "id": 2,
        "material_category": "玻纤板(FR-4/G11)",
        "param_name": "击穿电压",
        "param_definition": "材料被击穿时的电压强度",
        "test_standard": "IPC-TM-650 2.5.6",
        "standard_unit": "kV/mm",
        "is_core": true,
        "view_count": 1100,
        "favorite_count": 72
      }
    ],
    "total": 45,
    "page": 1,
    "page_size": 20,
    "total_pages": 3
  }
}
```

### 2.2 获取参数详情

**GET** `/api/v1/parameters/{id}`

**响应**:
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "id": 1,
    "material_category": "玻纤板(FR-4/G11)",
    "param_name": "玻璃化温度Tg",
    "param_definition": "材料从玻璃态到高弹态的转变温度，是衡量材料耐热性的重要指标",
    "test_standard": "IPC-TM-650 2.4.25 (DSC法)",
    "standard_unit": "℃",
    "user_focus": "影响焊接耐热性、尺寸稳定性和可靠性，高Tg板材适用于多层板和高可靠性产品",
    "marking_spec": "标注格式：Tg ≥ 170℃（高Tg）或 Tg ≥ 150℃（中Tg）",
    "remark": "FR-4标准Tg为130-140℃，高Tg板材≥170℃",
    "is_core": true,
    "standard_value": "130-170℃",
    "view_count": 1251,
    "favorite_count": 85,
    "created_at": "2026-01-01T10:00:00Z",
    "updated_at": "2026-02-01T16:00:00Z"
  }
}
```

**业务逻辑**:
- 每次访问详情页，`view_count++`（异步更新，避免阻塞）

### 2.3 搜索参数

**GET** `/api/v1/parameters/search`

**Query参数**:
- `q`: 搜索关键词（必需）
- `page`: 页码（默认1）
- `page_size`: 每页数量（默认20）

**请求示例**:
```
GET /api/v1/parameters/search?q=玻璃化温度&page=1
```

**响应**:
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "items": [
      {
        "id": 1,
        "param_name": "玻璃化温度Tg",
        "material_category": "玻纤板(FR-4/G11)",
        "param_definition": "材料从玻璃态到高弹态的转变温度",
        "highlight": "<em>玻璃化温度</em>Tg"  // 搜索关键词高亮
      }
    ],
    "total": 3,
    "page": 1,
    "page_size": 20,
    "total_pages": 1
  }
}
```

### 2.4 获取材料分类

**GET** `/api/v1/parameters/categories`

**响应**:
```json
{
  "code": 0,
  "message": "success",
  "data": [
    {
      "value": "玻纤板(FR-4/G11)",
      "label": "玻纤板(FR-4/G11)",
      "count": 45
    },
    {
      "value": "PI板",
      "label": "PI板",
      "count": 32
    },
    {
      "value": "特种塑胶通用(PEEK/PPS/PEI/电木)",
      "label": "特种塑胶通用",
      "count": 58
    }
  ]
}
```

### 2.5 获取热门参数

**GET** `/api/v1/parameters/hot`

**Query参数**:
- `limit`: 返回数量（默认10）

**响应**:
```json
{
  "code": 0,
  "message": "success",
  "data": [
    {
      "id": 1,
      "param_name": "玻璃化温度Tg",
      "material_category": "玻纤板(FR-4/G11)",
      "view_count": 1251
    },
    {
      "id": 2,
      "param_name": "击穿电压",
      "material_category": "玻纤板(FR-4/G11)",
      "view_count": 1100
    }
  ]
}
```

**业务逻辑**: 按 `view_count` 或 `favorite_count` 降序排序

---

## 3. 模板库模块

### 3.1 获取模板列表

**GET** `/api/v1/templates/`

**Query参数**:
- `template_category`: 模板分类（`参数表模板` | `店铺架构模板` | `实拍SOP模板` | `FAQ话术模板`）
- `is_free`: 是否免费（`true` | `false` | 不传则全部）
- `page`: 页码（默认1）
- `page_size`: 每页数量（默认20）

**请求示例**:
```
GET /api/v1/templates/?template_category=参数表模板&is_free=false&page=1
```

**响应**:
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "items": [
      {
        "id": 2,
        "template_category": "参数表模板",
        "template_name": "PEEK特种塑胶全参数表模板",
        "cover_image_url": "https://example.com/covers/peek-template.jpg",
        "description": "PEEK材料完整参数表，含热性能、力学性能、电性能",
        "price": 19.90,
        "is_free": false,
        "download_count": 156,
        "view_count": 890
      }
    ],
    "total": 12,
    "page": 1,
    "page_size": 20,
    "total_pages": 1
  }
}
```

### 3.2 获取模板详情

**GET** `/api/v1/templates/{id}`

**响应**:
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "id": 2,
    "template_category": "参数表模板",
    "template_name": "PEEK特种塑胶全参数表模板",
    "cover_image_url": "https://example.com/covers/peek-template.jpg",
    "description": "PEEK材料完整参数表，含热性能、力学性能、电性能。包含国标参数定义、测试标准、标注规范，适用于1688/淘宝店铺及客户询盘",
    "price": 19.90,
    "is_free": false,
    "download_count": 156,
    "purchase_count": 89,
    "view_count": 891,
    "created_at": "2026-01-15T10:00:00Z",
    "can_download": false  // 当前用户是否可下载（已购买或VIP会员）
  }
}
```

**业务逻辑**:
- 每次访问详情页，`view_count++`
- 判断用户是否可下载：
  - 免费模板：直接可下载
  - 付费模板：已购买（orders表有记录且paid）或VIP会员

### 3.3 获取模板分类

**GET** `/api/v1/templates/categories`

**响应**:
```json
{
  "code": 0,
  "message": "success",
  "data": [
    {
      "value": "参数表模板",
      "label": "参数表模板",
      "count": 25
    },
    {
      "value": "店铺架构模板",
      "label": "店铺架构模板",
      "count": 18
    },
    {
      "value": "实拍SOP模板",
      "label": "实拍SOP模板",
      "count": 12
    },
    {
      "value": "FAQ话术模板",
      "label": "FAQ话术模板",
      "count": 15
    }
  ]
}
```

### 3.4 下载模板

**POST** `/api/v1/templates/{id}/download`

**认证**: 必需

**业务逻辑**:
1. 验证用户权限：
   - 免费模板：直接允许
   - 付费模板：检查是否已购买或VIP会员
2. 如果有权限：创建下载记录，返回下载链接
3. 如果无权限：返回错误，提示需要购买

**响应（有权限）**:
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "download_url": "https://aliyundrive.com/s/xxx",
    "template_name": "PEEK特种塑胶全参数表模板",
    "download_id": 25
  }
}
```

**响应（无权限）**:
```json
{
  "code": 40300,
  "message": "需要购买后才能下载",
  "detail": "该模板为付费模板，请先购买"
}
```

---

## 4. 咨询预约模块

### 4.1 创建咨询预约

**POST** `/api/v1/consultations/`

**认证**: 必需

**请求参数**:
```json
{
  "name": "张三",
  "company": "深圳市某某科技有限公司",  // 可选
  "consult_type": "产品参数梳理与合规标注",
  "problem": "我司生产PEEK注塑件，需要梳理产品参数并符合1688平台标注规范，目前参数表较混乱，客户经常询问参数定义...",  // 至少50字
  "contact": "13800138000"
}
```

**响应**:
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "id": 15,
    "name": "张三",
    "company": "深圳市某某科技有限公司",
    "consult_type": "产品参数梳理与合规标注",
    "problem": "我司生产PEEK注塑件...",
    "contact": "13800138000",
    "status": "待沟通",
    "price": 99.00,
    "created_at": "2026-02-01T16:30:00Z"
  }
}
```

**错误响应** (验证失败):
```json
{
  "code": 40001,
  "message": "参数验证失败",
  "detail": {
    "problem": "问题描述至少50字"
  }
}
```

### 4.2 获取咨询详情

**GET** `/api/v1/consultations/{id}`

**认证**: 必需

**响应**:
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "id": 15,
    "name": "张三",
    "company": "深圳市某某科技有限公司",
    "consult_type": "产品参数梳理与合规标注",
    "problem": "我司生产PEEK注塑件...",
    "contact": "13800138000",
    "status": "已完成",
    "price": 99.00,
    "consultation_time": "2026-02-02T10:00:00Z",
    "summary": "针对贵司PEEK注塑件产品，梳理了核心参数体系，建议补充以下内容...",
    "actions": [
      "补充热变形温度HDT参数及测试标准",
      "完善拉伸强度、弯曲强度标注格式",
      "增加阻燃等级UL94标注"
    ],
    "created_at": "2026-02-01T16:30:00Z",
    "updated_at": "2026-02-02T11:00:00Z"
  }
}
```

### 4.3 获取咨询列表

**GET** `/api/v1/consultations/`

**认证**: 必需

**Query参数**:
- `status`: 状态（`待沟通` | `已完成` | `已取消` | 不传则全部）
- `page`: 页码（默认1）
- `page_size`: 每页数量（默认20）

**响应**:
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "items": [
      {
        "id": 15,
        "consult_type": "产品参数梳理与合规标注",
        "status": "已完成",
        "created_at": "2026-02-01T16:30:00Z"
      }
    ],
    "total": 3,
    "page": 1,
    "page_size": 20,
    "total_pages": 1
  }
}
```

---

## 5. 订单模块

### 5.1 创建订单

**POST** `/api/v1/orders/`

**认证**: 必需

**请求参数**:
```json
{
  "order_type": "template",  // template | consultation | vip_membership
  "item_id": 2,  // 模板ID或咨询ID（VIP会员无需item_id）
  "item_name": "PEEK特种塑胶全参数表模板"  // 可选，后端会自动填充
}
```

**响应**:
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "id": 20,
    "order_no": "20260201163045123456",
    "order_type": "template",
    "item_id": 2,
    "item_name": "PEEK特种塑胶全参数表模板",
    "amount": 19.90,
    "status": "pending",
    "created_at": "2026-02-01T16:30:45Z"
  }
}
```

**业务逻辑**:
- 订单号生成：`yyyyMMddHHmmss + 随机6位数字`
- 根据 `order_type` 和 `item_id` 查询价格
- 创建订单，状态=pending

### 5.2 获取订单详情

**GET** `/api/v1/orders/{order_no}`

**认证**: 必需

**响应**:
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "id": 20,
    "order_no": "20260201163045123456",
    "order_type": "template",
    "item_id": 2,
    "item_name": "PEEK特种塑胶全参数表模板",
    "amount": 19.90,
    "status": "paid",
    "payment_method": "wechat",
    "transaction_id": "4200001234567890",
    "paid_at": "2026-02-01T16:31:20Z",
    "created_at": "2026-02-01T16:30:45Z"
  }
}
```

### 5.3 发起支付

**POST** `/api/v1/orders/{order_no}/pay`

**认证**: 必需

**请求参数**:
```json
{
  "payment_method": "wechat"
}
```

**响应**:
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "payment_params": {
      "timeStamp": "1643702400",
      "nonceStr": "5K8264ILTKCH16CQ2502SI8ZNMTM67VS",
      "package": "prepay_id=wx01164559252577f19a7e6d861234567890",
      "signType": "RSA",
      "paySign": "oR9d8PuhnIc+YZ8cBHFOH05Z..."
    }
  }
}
```

**业务逻辑**:
1. 验证订单状态（必须是pending）
2. 调用微信统一下单API
3. 返回支付参数给前端
4. 前端调用 `wx.requestPayment()` 发起支付

### 5.4 微信支付回调

**POST** `/api/v1/orders/wechat-callback`

**认证**: 否（微信服务器回调，使用签名验证）

**请求参数**: 微信支付回调参数（XML格式）

**业务逻辑**:
1. 验证签名
2. 更新订单状态=paid
3. 记录 `transaction_id` 和 `paid_at`
4. 如果是VIP订单，更新用户VIP状态
5. 返回成功响应给微信

**响应** (XML格式):
```xml
<xml>
  <return_code><![CDATA[SUCCESS]]></return_code>
  <return_msg><![CDATA[OK]]></return_msg>
</xml>
```

---

## 6. 反馈模块

### 6.1 提交反馈

**POST** `/api/v1/feedbacks/`

**认证**: 否（支持匿名反馈）

**请求参数**:
```json
{
  "feedback_type": "问题反馈",
  "content": "参数查询页面加载较慢，希望能优化性能",
  "contact": "13800138000",  // 可选
  "images": [  // 可选
    "https://example.com/feedback1.jpg",
    "https://example.com/feedback2.jpg"
  ]
}
```

**响应**:
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "id": 8,
    "feedback_type": "问题反馈",
    "content": "参数查询页面加载较慢...",
    "status": "pending",
    "created_at": "2026-02-01T17:00:00Z"
  }
}
```

### 6.2 获取反馈详情

**GET** `/api/v1/feedbacks/{id}`

**认证**: 必需

**响应**:
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "id": 8,
    "feedback_type": "问题反馈",
    "content": "参数查询页面加载较慢...",
    "contact": "13800138000",
    "images": [
      "https://example.com/feedback1.jpg"
    ],
    "status": "resolved",
    "admin_reply": "感谢反馈，我们已优化了参数查询接口的性能，加载速度提升50%",
    "created_at": "2026-02-01T17:00:00Z",
    "updated_at": "2026-02-03T10:00:00Z"
  }
}
```

---

## 认证和授权

### JWT Token格式

**Token Payload**:
```json
{
  "user_id": 1,
  "openid": "oXXXXXXXXXXXXXXXXX",
  "is_vip": false,
  "exp": 1643789200  // 过期时间（Unix时间戳）
}
```

### 权限验证

**需要登录的接口**:
- 用户个人信息相关（`/users/me`, `/users/favorites`, `/users/orders`, `/users/downloads`）
- 收藏操作（添加/取消收藏）
- 模板下载
- 咨询预约
- 订单相关

**公开接口**:
- 参数查询（列表、详情、搜索）
- 模板查询（列表、详情、分类）
- 反馈提交（支持匿名）

### Token刷新机制

如果Token即将过期（距离到期时间<24小时），后端在响应Header中返回新Token：

```http
X-New-Token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

前端应该更新本地存储的Token。

---

## 性能优化

### 1. 缓存策略

- **参数分类、模板分类**: Redis缓存1小时
- **热门参数**: Redis缓存30分钟
- **模板列表（首页）**: Redis缓存10分钟

### 2. 数据库优化

- 统计字段（`view_count`, `favorite_count`）使用异步更新，避免阻塞请求
- 搜索接口使用全文索引
- 列表查询使用复合索引

### 3. 分页

所有列表接口都支持分页，默认 `page_size=20`，最大100。

---

## 安全性

### 1. SQL注入防护

使用SQLAlchemy ORM或参数化查询，严禁拼接SQL。

### 2. XSS防护

前端输入的内容（如反馈内容）需要转义HTML标签。

### 3. 限流

- 登录接口：单IP每分钟最多10次
- 搜索接口：单用户每秒最多5次
- 支付接口：单用户每分钟最多3次

### 4. 敏感信息

- 手机号脱敏显示：`138****5678`
- 微信OpenID不暴露给前端
- 数据库密码使用环境变量

---

## 测试用例

### 用户登录测试

```bash
# 1. 微信登录
curl -X POST http://localhost:8000/api/v1/users/login \
  -H "Content-Type: application/json" \
  -d '{"code": "081xZXXX"}'

# 响应示例
{
  "code": 0,
  "message": "success",
  "data": {
    "access_token": "eyJhbGc...",
    "user": {
      "id": 1,
      "nickname": "微信用户"
    }
  }
}
```

### 参数查询测试

```bash
# 2. 获取参数列表
curl http://localhost:8000/api/v1/parameters/?material_category=玻纤板(FR-4/G11)&page=1&page_size=10

# 3. 获取参数详情
curl http://localhost:8000/api/v1/parameters/1

# 4. 搜索参数
curl http://localhost:8000/api/v1/parameters/search?q=玻璃化温度
```

### 模板购买流程测试

```bash
# 5. 获取模板详情
curl http://localhost:8000/api/v1/templates/2

# 6. 创建订单
curl -X POST http://localhost:8000/api/v1/orders/ \
  -H "Authorization: Bearer {access_token}" \
  -H "Content-Type: application/json" \
  -d '{"order_type": "template", "item_id": 2}'

# 7. 发起支付
curl -X POST http://localhost:8000/api/v1/orders/20260201163045123456/pay \
  -H "Authorization: Bearer {access_token}" \
  -H "Content-Type: application/json" \
  -d '{"payment_method": "wechat"}'

# 8. 下载模板（支付成功后）
curl -X POST http://localhost:8000/api/v1/templates/2/download \
  -H "Authorization: Bearer {access_token}"
```

---

## 后续优化方向

1. **WebSocket支持**: 实时通知（订单状态、咨询回复）
2. **GraphQL**: 减少请求次数，按需查询
3. **API网关**: 统一限流、认证、日志
4. **服务拆分**: 用户服务、订单服务、内容服务独立部署
5. **消息队列**: 异步处理（统计更新、消息通知）

---

## 附录

### HTTP状态码使用规范

- **200 OK**: 请求成功
- **201 Created**: 创建成功
- **400 Bad Request**: 参数错误
- **401 Unauthorized**: 未登录
- **403 Forbidden**: 无权限
- **404 Not Found**: 资源不存在
- **409 Conflict**: 资源冲突（如重复收藏）
- **500 Internal Server Error**: 服务器错误

### 日期时间格式

所有日期时间使用ISO 8601格式：`2026-02-01T16:30:45Z`（UTC时区）

### 数据仅供参考免责声明

所有返回参数数据的接口响应中，建议在前端显示时添加：
> 数据仅供参考，实际以国标/厂商检测报告为准
