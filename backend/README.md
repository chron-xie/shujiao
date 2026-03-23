# 绝缘材料参数工具 - 后端服务

基于 FastAPI 的后端服务，提供参数查询、模板管理、轻咨询预约等功能。

## 环境要求

- Python 3.12
- Conda 环境管理
- MySQL 数据库
    - DATABASE_HOST=47.116.114.44
    - DATABASE_USER=root
    - DATABASE_PASSWORD=A123456z
    - DATABASE_NAME=shujiao

## 快速开始

### 1. 创建 Conda 环境

```bash
conda env create -f environment.yml
conda activate shujiao
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
# 开发环境
pip install -r requirements-dev.txt
```

### 3. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 文件，填入实际配置
```

### 4. 启动开发服务器

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API 文档访问地址：http://localhost:8000/docs

## 项目结构

```
backend/
├── app/
│   ├── api/v1/          # API 路由
│   ├── core/            # 核心配置
│   ├── models/          # 数据库模型
│   ├── schemas/         # Pydantic schemas
│   ├── services/        # 业务逻辑层
│   └── db/              # 数据库相关
├── tests/               # 测试文件
└── scripts/             # 脚本工具
```


