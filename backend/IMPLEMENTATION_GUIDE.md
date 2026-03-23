# 后端实施指南

## 已完成的工作 ✅

### 1. 数据库设计
- ✅ **`database_schema.sql`** - 完整的8张表SQL建表脚本
- ✅ **`DATABASE_DESIGN.md`** - 详细的设计文档（表关系、索引、业务逻辑）

### 2. API接口设计
- ✅ **`API_DESIGN.md`** - 完整的31个API端点设计文档
  - 请求/响应格式
  - 认证授权规范
  - 错误码规范
  - 测试用例

### 3. Pydantic Schemas（请求/响应验证）
- ✅ **`app/schemas/common.py`** - 通用响应模型
- ✅ **`app/schemas/user.py`** - 用户模块schemas
- ✅ **`app/schemas/parameter.py`** - 参数模块schemas
- ✅ **`app/schemas/template.py`** - 模板模块schemas
- ✅ **`app/schemas/consultation.py`** - 咨询模块schemas
- ✅ **`app/schemas/order.py`** - 订单模块schemas
- ✅ **`app/schemas/feedback.py`** - 反馈模块schemas

### 4. SQLAlchemy Models（ORM模型）
- ✅ **`app/models/user.py`** - 用户表模型（含VIP、微信登录）
- ✅ **`app/models/parameter.py`** - 参数标准表模型（含统计字段）
- ✅ **`app/models/template.py`** - 模板库表模型（含统计字段）
- ✅ **`app/models/consultation.py`** - 咨询预约表模型（含总结和动作）
- ✅ **`app/models/favorite.py`** - 用户收藏表模型
- ✅ **`app/models/order.py`** - 订单表模型
- ✅ **`app/models/download.py`** - 下载记录表模型
- ✅ **`app/models/feedback.py`** - 反馈表模型

**特性**:
- 外键关系 + ORM relationships
- 索引优化（单列 + 复合索引）
- 唯一约束
- 时间戳混入

### 5. 认证系统
- ✅ **`app/core/auth.py`** - JWT Token认证
  - `create_access_token()` - 创建JWT token
  - `decode_access_token()` - 解码JWT token
  - `get_current_user()` - 依赖注入获取当前用户
  - `get_current_user_optional()` - 可选认证
- ✅ **`app/core/wechat.py`** - 微信API封装
  - `WeChatAPI.code2session()` - 微信登录
  - `WeChatAPI.get_access_token()` - 获取access_token
  - `WeChatPay.*` - 微信支付（待实现）

### 6. API Endpoints（部分完成）
- ✅ **`app/api/v1/endpoints/users.py`** - 用户模块（8个端点全部完成）
  - `POST /api/v1/users/login` - 微信登录
  - `GET /api/v1/users/me` - 获取当前用户信息
  - `PUT /api/v1/users/me` - 更新用户信息
  - `GET /api/v1/users/favorites` - 获取收藏列表
  - `POST /api/v1/users/favorites` - 添加收藏
  - `DELETE /api/v1/users/favorites/{id}` - 取消收藏
  - `GET /api/v1/users/orders` - 获取订单列表
  - `GET /api/v1/users/downloads` - 获取下载记录

---

## 待完成的工作 ⏭️

### 1. API Endpoints（剩余5个模块）

#### **参数查询模块** (5个端点)
文件: `app/api/v1/endpoints/parameters.py`

```python
@router.get("/", response_model=ResponseModel)
async def get_parameters(
    material_category: Optional[str] = None,
    search: Optional[str] = None,
    is_core: Optional[bool] = None,
    page: int = 1,
    page_size: int = 20,
    db: AsyncSession = Depends(get_db)
):
    """获取参数列表"""
    # 实现分页查询 + 筛选
    pass

@router.get("/{id}", response_model=ResponseModel)
async def get_parameter(id: int, db: AsyncSession = Depends(get_db)):
    """获取参数详情"""
    # 实现详情查询 + view_count++
    pass

@router.get("/search", response_model=ResponseModel)
async def search_parameters(
    q: str,
    page: int = 1,
    page_size: int = 20,
    db: AsyncSession = Depends(get_db)
):
    """搜索参数"""
    # 实现全文搜索（使用LIKE或FULLTEXT）
    pass

@router.get("/categories", response_model=ResponseModel)
async def get_categories(db: AsyncSession = Depends(get_db)):
    """获取材料分类"""
    # 实现分类统计
    pass

@router.get("/hot", response_model=ResponseModel)
async def get_hot_parameters(
    limit: int = 10,
    db: AsyncSession = Depends(get_db)
):
    """获取热门参数"""
    # 按view_count降序排序
    pass
```

#### **模板库模块** (4个端点)
文件: `app/api/v1/endpoints/templates.py`

```python
@router.get("/", response_model=ResponseModel)
async def get_templates(
    template_category: Optional[str] = None,
    is_free: Optional[bool] = None,
    page: int = 1,
    page_size: int = 20,
    db: AsyncSession = Depends(get_db)
):
    """获取模板列表"""
    pass

@router.get("/{id}", response_model=ResponseModel)
async def get_template(
    id: int,
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: AsyncSession = Depends(get_db)
):
    """获取模板详情"""
    # 判断can_download（免费/已购买/VIP会员）
    # view_count++
    pass

@router.get("/categories", response_model=ResponseModel)
async def get_template_categories(db: AsyncSession = Depends(get_db)):
    """获取模板分类"""
    pass

@router.post("/{id}/download", response_model=ResponseModel)
async def download_template(
    id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """下载模板"""
    # 权限验证：免费/已购买/VIP
    # 创建下载记录
    # 返回download_url
    pass
```

#### **咨询预约模块** (3个端点)
文件: `app/api/v1/endpoints/consultations.py`

```python
@router.post("/", response_model=ResponseModel)
async def create_consultation(
    consultation_data: ConsultationCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """创建咨询预约"""
    # 验证problem长度 >= 50字
    # 创建记录，状态=待沟通
    pass

@router.get("/{id}", response_model=ResponseModel)
async def get_consultation(
    id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取咨询详情"""
    # 验证user_id == current_user.id
    pass

@router.get("/", response_model=ResponseModel)
async def get_consultations(
    status: Optional[str] = None,
    page: int = 1,
    page_size: int = 20,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取咨询列表"""
    pass
```

#### **订单模块** (4个端点)
文件: `app/api/v1/endpoints/orders.py`

```python
@router.post("/", response_model=ResponseModel)
async def create_order(
    order_data: OrderCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """创建订单"""
    # 生成订单号: yyyyMMddHHmmss + 随机6位
    # 查询价格（根据order_type和item_id）
    # 创建订单，状态=pending
    pass

@router.get("/{order_no}", response_model=ResponseModel)
async def get_order(
    order_no: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取订单详情"""
    # 验证user_id == current_user.id
    pass

@router.post("/{order_no}/pay", response_model=ResponseModel)
async def pay_order(
    order_no: str,
    pay_request: OrderPayRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """发起支付"""
    # 验证订单状态=pending
    # 调用微信统一下单API
    # 生成支付参数
    pass

@router.post("/wechat-callback")
async def wechat_payment_callback(xml_data: str, db: AsyncSession = Depends(get_db)):
    """微信支付回调"""
    # 验证签名
    # 更新订单状态=paid
    # 如果是VIP订单，更新user.is_vip=True
    # 返回XML响应给微信
    pass
```

#### **反馈模块** (2个端点)
文件: `app/api/v1/endpoints/feedbacks.py`

```python
@router.post("/", response_model=ResponseModel)
async def create_feedback(
    feedback_data: FeedbackCreate,
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: AsyncSession = Depends(get_db)
):
    """提交反馈（支持匿名）"""
    # 创建反馈，status=pending
    # user_id可为空（匿名）
    pass

@router.get("/{id}", response_model=ResponseModel)
async def get_feedback(
    id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取反馈详情"""
    # 验证user_id == current_user.id
    pass
```

### 2. 路由注册

文件: `app/api/v1/__init__.py`

```python
from fastapi import APIRouter
from app.api.v1.endpoints import (
    users,
    parameters,
    templates,
    consultations,
    orders,
    feedbacks,
)

api_router = APIRouter()

api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(parameters.router, prefix="/parameters", tags=["parameters"])
api_router.include_router(templates.router, prefix="/templates", tags=["templates"])
api_router.include_router(consultations.router, prefix="/consultations", tags=["consultations"])
api_router.include_router(orders.router, prefix="/orders", tags=["orders"])
api_router.include_router(feedbacks.router, prefix="/feedbacks", tags=["feedbacks"])
```

### 3. 主应用配置

文件: `app/main.py`

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1 import api_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    return {"message": "绝缘材料参数工具 API"}
```

### 4. 数据库初始化

```bash
# 1. 登录MySQL
mysql -u root -p -h 47.116.114.44

# 2. 创建数据库
CREATE DATABASE IF NOT EXISTS shujiao DEFAULT CHARSET utf8mb4 COLLATE utf8mb4_general_ci;

# 3. 执行建表脚本
USE shujiao;
SOURCE /path/to/database_schema.sql;

# 4. 验证表创建
SHOW TABLES;
DESCRIBE users;
```

### 5. 环境配置

文件: `backend/.env`

```env
# Database
DATABASE_HOST=47.116.114.44
DATABASE_PORT=3306
DATABASE_USER=root
DATABASE_PASSWORD=A123456z
DATABASE_NAME=shujiao

# Security
SECRET_KEY=your-secret-key-change-in-production-random-string
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080

# WeChat Mini Program
WECHAT_APP_ID=your-wechat-app-id
WECHAT_APP_SECRET=your-wechat-app-secret

# WeChat Payment
WECHAT_MCH_ID=your-merchant-id
WECHAT_MCH_KEY=your-merchant-key
```

### 6. 依赖安装

文件: `backend/requirements.txt`（需要添加）

```txt
fastapi==0.110.0
uvicorn[standard]==0.27.1
sqlalchemy==2.0.27
aiomysql==0.2.0
pydantic==2.6.1
pydantic-settings==2.1.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.9
httpx==0.26.0
```

安装命令:
```bash
cd backend
pip install -r requirements.txt
```

### 7. 启动应用

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

访问API文档:
- Swagger UI: http://localhost:8000/api/v1/docs
- ReDoc: http://localhost:8000/api/v1/redoc

---

## 实施步骤

### 阶段1: 环境准备
1. ✅ 创建数据库表（执行`database_schema.sql`）
2. ✅ 配置`.env`文件
3. ✅ 安装Python依赖

### 阶段2: 核心功能实施
1. ✅ 完成用户模块（已完成）
2. ⏭️ 完成参数查询模块（5个端点）
3. ⏭️ 完成模板库模块（4个端点）
4. ⏭️ 完成咨询预约模块（3个端点）
5. ⏭️ 完成订单模块（4个端点）
6. ⏭️ 完成反馈模块（2个端点）

### 阶段3: 集成测试
1. ⏭️ 微信登录流程测试
2. ⏭️ 参数查询功能测试
3. ⏭️ 模板购买流程测试
4. ⏭️ 咨询预约流程测试
5. ⏭️ 支付流程测试（微信支付沙箱）

### 阶段4: 优化和部署
1. ⏭️ 性能优化（缓存、索引）
2. ⏭️ 日志系统（记录关键操作）
3. ⏭️ 监控和告警
4. ⏭️ 生产环境部署

---

## 关键业务逻辑

### 1. 微信登录流程
```
前端 wx.login() → code → 后端 /api/v1/users/login
→ WeChatAPI.code2session(code) → 获取openid
→ 查询用户（根据openid）
→ 不存在则创建新用户
→ 生成JWT Token
→ 返回 {access_token, user}
```

### 2. 模板下载权限判断
```python
def can_download(user, template):
    # 免费模板：直接允许
    if template.is_free:
        return True

    # VIP会员：所有模板免费
    if user.is_vip and user.vip_expire_at > datetime.now():
        return True

    # 付费模板：检查是否已购买
    order = db.query(Order).filter(
        Order.user_id == user.id,
        Order.order_type == "template",
        Order.item_id == template.id,
        Order.status == "paid"
    ).first()

    return order is not None
```

### 3. 订单号生成
```python
import time
import random

def generate_order_no():
    timestamp = time.strftime('%Y%m%d%H%M%S')
    random_num = random.randint(100000, 999999)
    return f"{timestamp}{random_num}"
    # 示例: 20260201163045123456
```

### 4. 异步统计更新
```python
# 参数详情页 view_count++ （异步）
async def increment_view_count(parameter_id: int, db: AsyncSession):
    await db.execute(
        update(Parameter)
        .where(Parameter.id == parameter_id)
        .values(view_count=Parameter.view_count + 1)
    )
    await db.commit()

# 在详情接口中调用（不等待结果）
import asyncio
asyncio.create_task(increment_view_count(parameter.id, db))
```

---

## 测试用例

### 1. 用户登录测试
```bash
curl -X POST http://localhost:8000/api/v1/users/login \
  -H "Content-Type: application/json" \
  -d '{"code": "081xZXXX"}'
```

### 2. 获取参数列表测试
```bash
curl http://localhost:8000/api/v1/parameters/?material_category=玻纤板(FR-4/G11)&page=1&page_size=10
```

### 3. 添加收藏测试
```bash
curl -X POST http://localhost:8000/api/v1/users/favorites \
  -H "Authorization: Bearer {access_token}" \
  -H "Content-Type: application/json" \
  -d '{"favorite_type": "parameter", "item_id": 1}'
```

---

## 注意事项

1. **数据库连接**: 确保生产数据库密码不要提交到git
2. **JWT Secret**: 生产环境必须使用强随机字符串
3. **微信配置**: 需要在微信公众平台配置AppID和AppSecret
4. **支付回调**: 需要配置公网可访问的回调URL
5. **CORS**: 生产环境配置具体的前端域名，不要使用`*`
6. **日志**: 记录所有关键操作（登录、支付、订单）
7. **错误处理**: 统一的错误响应格式
8. **性能优化**: 统计字段异步更新，避免阻塞请求

---

## 后续优化方向

1. **缓存**: Redis缓存热门参数、模板分类
2. **全文搜索**: Elasticsearch替代MySQL LIKE查询
3. **异步任务**: Celery处理邮件通知、统计更新
4. **文件上传**: OSS存储模板封面和用户头像
5. **消息队列**: RabbitMQ处理支付回调、库存扣减
6. **监控**: Prometheus + Grafana监控API性能
7. **限流**: Redis实现API限流
8. **日志分析**: ELK Stack分析用户行为

---

## 总结

✅ **已完成**:
- 数据库设计（8张表）
- API设计（31个端点）
- Pydantic Schemas（7个模块）
- SQLAlchemy Models（8个模型）
- 认证系统（JWT + 微信登录）
- 用户模块API（8个端点）

⏭️ **待完成**:
- 5个模块的API端点实现（23个端点）
- 路由注册和主应用配置
- 数据库初始化
- 环境配置和依赖安装
- 集成测试

**预计完成时间**: 4-6小时（实现剩余API端点 + 测试）
