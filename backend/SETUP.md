# 后端环境设置指南

## 1. 创建 Conda 环境

```bash
# 在backend目录下执行
conda env create -f environment.yml
```

这将创建名为 `shujiao` 的 conda 环境，Python版本为 3.12

## 2. 激活环境

```bash
conda activate shujiao
```

## 3. 安装依赖

```bash
pip install -r requirements.txt
```

## 4. 配置环境变量

```bash
cp .env.example .env
```

编辑 `.env` 文件，确认数据库配置正确：
- DATABASE_HOST=47.116.114.44
- DATABASE_USER=root
- DATABASE_PASSWORD=A123456z
- DATABASE_NAME=shujiao

## 5. 初始化数据库

```bash
python scripts/init_db.py
```

这将创建所有数据库表。

## 6. 启动开发服务器

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 7. 访问 API 文档

打开浏览器访问：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 常见问题

### 问题1: ModuleNotFoundError

确保已激活 conda 环境：
```bash
conda activate shujiao
```

### 问题2: 数据库连接失败

检查 `.env` 文件中的数据库配置是否正确，确保数据库服务器可访问。

### 问题3: 端口被占用

更换端口启动：
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```
