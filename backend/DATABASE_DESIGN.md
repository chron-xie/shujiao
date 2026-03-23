# 数据库设计文档

## 概述

本文档描述绝缘材料参数工具小程序的数据库表结构设计，包括8个核心表，覆盖用户管理、参数查询、模板库、咨询预约等全部功能。

**数据库信息**:
- 数据库名: `shujiao`
- 字符集: `utf8mb4`
- 引擎: `InnoDB`
- 生产服务器: `47.116.114.44:3306`

## 表结构总览

| 表名 | 说明 | 记录数量级 |
|-----|------|---------|
| `users` | 用户表 | 1万+ |
| `parameters` | 参数标准表 | 5000+ |
| `templates` | 模板库表 | 500+ |
| `consultations` | 轻咨询预约表 | 1000+ |
| `user_favorites` | 用户收藏表 | 5万+ |
| `orders` | 订单表 | 5万+ |
| `downloads` | 下载记录表 | 10万+ |
| `feedbacks` | 意见反馈表 | 5000+ |

## 表关系图

```
┌─────────────┐
│   users     │
└──────┬──────┘
       │
       ├─────────┐ 1:N
       │         │
       │    ┌────▼─────────────┐
       │    │  consultations   │
       │    └──────────────────┘
       │
       ├─────────┐ 1:N
       │         │
       │    ┌────▼──────────┐
       │    │  orders       │
       │    └───────────────┘
       │         │
       │         │ 1:N
       │    ┌────▼──────────┐
       │    │  downloads    │◄──────┐
       │    └───────────────┘       │
       │                            │ N:1
       ├─────────┐ 1:N         ┌────┴──────┐
       │         │             │ templates │
       │    ┌────▼─────────┐   └───────────┘
       │    │user_favorites│
       │    └──────────────┘
       │         │ N:1
       │    ┌────┴───────┐
       │    │parameters  │
       │    └────────────┘
       │
       └─────────┐ 1:N
                 │
            ┌────▼─────┐
            │feedbacks │
            └──────────┘
```

## 核心表详细设计

### 1. users (用户表)

**用途**: 存储用户基本信息和微信登录凭证

**关键字段**:
- `wechat_openid`: 微信OpenID，唯一标识用户
- `is_vip`: 是否全库会员（199元会员可下载所有模板）
- `vip_expire_at`: VIP到期时间

**业务逻辑**:
- 微信快捷登录时通过 `wechat_openid` 查找或创建用户
- VIP会员可免费下载所有付费模板
- 支持记录最后登录时间用于用户活跃度分析

**索引**:
- `idx_wechat_openid`: 用于登录查询
- `idx_created_at`: 用于用户增长分析

### 2. parameters (参数标准表)

**用途**: 存储材料参数标准信息，支持3大材料分类

**材料分类**:
1. 玻纤板(FR-4/G11)
2. PI板
3. 特种塑胶通用(PEEK/PPS/PEI/电木)

**关键字段**:
- `param_name`: 参数名称（如：玻璃化温度Tg）
- `test_standard`: 测试标准（如：IPC-TM-650 2.4.25）
- `is_core`: 是否核心参数（用于首页推荐）
- `view_count` / `favorite_count`: 统计字段

**业务逻辑**:
- 支持关键词全文搜索（FULLTEXT索引）
- 每次查看详情时 `view_count++`
- 每次收藏时 `favorite_count++`
- 核心参数显示在首页"热门工具推荐"

**索引**:
- `idx_material_category`: 分类筛选
- `ft_param_name_definition`: 全文搜索（中文支持需配置ngram）
- `idx_param_search`: 复合索引优化查询

**数据来源**: Excel批量导入（管理后台功能）

### 3. templates (模板库表)

**用途**: 存储行业模板信息，支持4大模板分类

**模板分类**:
1. 参数表模板
2. 店铺架构模板
3. 实拍SOP模板
4. FAQ话术模板

**关键字段**:
- `price`: 价格（0.00=免费，9.9/19.9/29.9=付费）
- `is_free`: 是否免费（快速筛选）
- `download_url`: 下载链接（阿里云盘/腾讯微云永久链接）
- `sort_order`: 排序权重（越大越靠前）

**业务逻辑**:
- 免费模板：直接下载，记录到 `downloads` 表
- 付费模板：购买后（`orders` 表记录）才能下载
- VIP会员：所有模板免费下载
- 支持上下架管理（`is_active`）

**索引**:
- `idx_template_category`: 分类筛选
- `idx_is_free`: 免费/付费筛选
- `idx_sort_order`: 排序展示
- `idx_template_filter`: 复合索引优化筛选

**数据来源**: Excel批量导入 + 管理后台手动添加

### 4. consultations (轻咨询预约表)

**用途**: 存储用户咨询预约记录

**咨询类型**:
1. 产品参数梳理与合规标注
2. 1688/淘宝店铺信息架构优化
3. 工厂实拍素材规范指导

**关键字段**:
- `problem`: 问题描述（至少50字，前端验证）
- `status`: 状态（待沟通|已完成|已取消）
- `price`: 咨询费用（默认99元/15分钟）
- `summary`: 咨询总结（完成后填写）
- `actions`: 可执行动作（JSON格式，如：`["动作1", "动作2", "动作3"]`）

**业务逻辑**:
- 用户提交表单 → 创建记录，状态=待沟通
- 管理员联系沟通 → 更新 `consultation_time`
- 沟通完成 → 填写 `summary` 和 `actions`，状态=已完成
- 用户可在"我的订单"中查看咨询记录

**索引**:
- `idx_user_id`: 用户订单查询
- `idx_status`: 管理后台筛选
- `idx_created_at`: 按时间排序

### 5. user_favorites (用户收藏表)

**用途**: 存储用户收藏的参数和模板

**收藏类型**:
- `parameter`: 参数收藏
- `template`: 模板收藏

**关键字段**:
- `favorite_type` + `item_id`: 标识收藏项目
- `uk_user_favorite`: 唯一约束防止重复收藏

**业务逻辑**:
- 收藏参数：`favorite_type='parameter'`, `item_id=参数ID`
- 收藏模板：`favorite_type='template'`, `item_id=模板ID`
- 取消收藏：删除对应记录
- "我的收藏"页面：根据 `user_id` + `favorite_type` 查询并关联原表获取详情

**索引**:
- `uk_user_favorite`: 唯一约束
- `idx_user_type`: 收藏列表查询

### 6. orders (订单表)

**用途**: 存储模板购买、咨询预约、VIP会员的订单

**订单类型**:
- `template`: 模板购买（单个模板）
- `consultation`: 咨询预约
- `vip_membership`: VIP会员（199元全库会员）

**关键字段**:
- `order_no`: 订单号（唯一，格式：`yyyyMMddHHmmss + 随机6位`）
- `status`: 订单状态（pending|paid|cancelled|refunded）
- `transaction_id`: 微信支付交易号
- `paid_at`: 支付成功时间

**业务逻辑**:
1. 用户点击购买 → 创建订单，状态=pending
2. 调用微信支付 → 获取 `transaction_id`
3. 支付成功回调 → 更新状态=paid，记录 `paid_at`
4. 如果是模板订单 → 允许下载，记录到 `downloads` 表
5. 如果是VIP订单 → 更新 `users.is_vip=TRUE`, `users.vip_expire_at`

**订单号生成**:
```python
import time
import random
order_no = f"{time.strftime('%Y%m%d%H%M%S')}{random.randint(100000, 999999)}"
# 示例: 20260201153045123456
```

**索引**:
- `idx_order_no`: 订单查询
- `idx_user_id`: 用户订单列表
- `idx_order_user_status`: 复合索引优化查询

### 7. downloads (下载记录表)

**用途**: 记录用户下载模板的历史

**关键字段**:
- `template_id`: 关联模板
- `order_id`: 关联订单（付费模板需要，免费模板为NULL）
- `download_url`: 下载链接（从 `templates` 表复制）

**业务逻辑**:
- 免费模板：直接创建下载记录，`order_id=NULL`
- 付费模板：验证订单已支付 → 创建下载记录，`order_id=订单ID`
- VIP会员：所有模板视为免费，`order_id=NULL`
- "下载记录"页面：查询 `downloads` 表并关联 `templates` 获取模板信息

**索引**:
- `idx_user_template`: 下载列表查询
- `idx_created_at`: 按时间排序

### 8. feedbacks (意见反馈表)

**用途**: 存储用户反馈

**反馈类型**:
- 功能建议
- 问题反馈
- 内容纠错
- 其他

**关键字段**:
- `user_id`: 用户ID（可为NULL，支持匿名反馈）
- `images`: 截图URL（JSON数组，如：`["https://example.com/img1.jpg"]`）
- `status`: 处理状态（pending|processing|resolved|closed）
- `admin_reply`: 管理员回复

**业务逻辑**:
- 用户提交反馈 → 创建记录，状态=pending
- 管理员处理 → 更新状态=processing
- 处理完成 → 填写 `admin_reply`，状态=resolved

**索引**:
- `idx_user_id`: 用户反馈查询
- `idx_status`: 管理后台筛选

## 数据迁移和初始化

### 1. 创建数据库

```bash
mysql -u root -p -h 47.116.114.44
```

```sql
CREATE DATABASE IF NOT EXISTS shujiao DEFAULT CHARSET utf8mb4 COLLATE utf8mb4_general_ci;
USE shujiao;
SOURCE /path/to/database_schema.sql;
```

### 2. Excel数据导入

**参数数据导入**:
```python
import pandas as pd
from sqlalchemy import create_engine

# 读取Excel
df = pd.read_excel('参数标准数据.xlsx')

# 连接数据库
engine = create_engine('mysql+aiomysql://root:A123456z@47.116.114.44:3306/shujiao')

# 导入数据
df.to_sql('parameters', con=engine, if_exists='append', index=False)
```

**模板数据导入**:
```python
df_templates = pd.read_excel('模板库数据.xlsx')
df_templates.to_sql('templates', con=engine, if_exists='append', index=False)
```

### 3. 测试数据

SQL文件中已包含3条示例参数数据和3条示例模板数据，用于开发测试。

## 性能优化策略

### 1. 索引优化

- **单列索引**: 常用筛选字段（如 `material_category`, `status`）
- **复合索引**: 常见查询组合（如 `user_id + status + created_at`）
- **全文索引**: 参数搜索（需配置 MySQL ngram分词器支持中文）

### 2. 查询优化

- 避免 `SELECT *`，只查询需要的字段
- 使用 `LIMIT` 分页查询
- 统计字段（`view_count`, `favorite_count`）异步更新，避免锁表

### 3. 数据归档

- `orders` 表：1年以上的已完成订单归档到历史表
- `downloads` 表：2年以上的下载记录归档
- `feedbacks` 表：已关闭的反馈定期归档

## 安全性考虑

### 1. SQL注入防护

- 使用 SQLAlchemy ORM 或参数化查询
- 严禁拼接SQL字符串

### 2. 敏感信息保护

- `users.phone` 加密存储（可选）
- `consultations.contact` 加密存储（可选）
- 数据库密码使用环境变量，不写入代码

### 3. 权限控制

- 生产数据库：只允许后端服务器IP访问
- 管理后台：单独的管理员权限系统
- 定期备份数据库

## 扩展性考虑

### 1. 预留字段

- 各表都有 `created_at` 和 `updated_at` 用于审计
- `remark` / `admin_notes` 用于备注

### 2. 状态枚举

- 使用 `VARCHAR` 而非 `ENUM`，方便扩展状态
- 前端和后端维护状态常量

### 3. JSON字段

- `consultations.actions`: 可执行动作列表
- `feedbacks.images`: 截图URL数组
- MySQL 5.7+ 支持 JSON 类型查询和索引

## 监控和维护

### 1. 慢查询日志

```sql
-- 开启慢查询日志
SET GLOBAL slow_query_log = 'ON';
SET GLOBAL long_query_time = 1; -- 1秒以上的查询记录
```

### 2. 表维护

```sql
-- 定期优化表
OPTIMIZE TABLE parameters;
OPTIMIZE TABLE templates;
OPTIMIZE TABLE orders;
```

### 3. 数据备份

```bash
# 每日自动备份
mysqldump -u root -p -h 47.116.114.44 shujiao > backup_$(date +%Y%m%d).sql
```

## 后续优化方向

1. **读写分离**: 主从复制，查询走从库
2. **缓存层**: Redis缓存热门参数和模板
3. **全文搜索**: Elasticsearch替代MySQL全文索引
4. **CDN加速**: 模板封面图和下载文件使用CDN
5. **分表策略**: 订单表、下载记录表按年分表

## 附录：表字段完整清单

参见 `database_schema.sql` 文件中的详细注释。
