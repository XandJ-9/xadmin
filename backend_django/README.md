# XAdmin 后端项目 (Django)

## 项目概述

XAdmin 后端项目是一个基于 Django 和 Django REST Framework 构建的管理系统后端，提供了用户管理、权限控制、数据源管理、报表管理等功能的 RESTful API 接口。

## 项目结构

```
backend_django/
├── app_init/            # 应用初始化模块
├── datasource/          # 数据源管理模块
├── report/              # 报表管理模块
├── system/              # 系统管理模块
├── utils/               # 工具类模块
├── xadmin/              # 项目配置模块
├── .env_template        # 环境变量模板
├── manage.py            # Django 管理脚本
└── requirements.txt     # 项目依赖
```

## 应用说明

### 1. system - 系统管理模块

系统管理模块负责用户、角色、权限、部门等基础数据的管理。

**主要功能：**
- 用户管理：用户的增删改查、密码修改、状态管理等
- 角色管理：角色的增删改查、权限分配等
- 部门管理：部门的增删改查、部门树结构管理等
- 岗位管理：岗位的增删改查等
- 字典管理：系统字典的增删改查等
- 菜单管理：系统菜单的增删改查、权限配置等
- 操作日志：记录用户操作日志

### 2. datasource - 数据源管理模块

数据源管理模块负责管理各种数据库连接和数据查询。

**主要功能：**
- 数据源管理：支持 MySQL、PostgreSQL 等数据库的连接配置
- 数据查询：执行 SQL 查询并返回结果
- 查询日志：记录查询操作日志

### 3. report - 报表管理模块

报表管理模块负责管理报表和数据接口。

**主要功能：**
- 平台管理：管理报表平台信息
- 模块管理：管理报表模块信息
- 报表管理：管理报表信息
- 接口管理：管理数据接口信息

### 4. app_init - 应用初始化模块

应用初始化模块负责系统初始化数据的导入。

**主要功能：**
- 初始化系统数据：包括默认角色、管理员用户、示例数据源等

## 关键文件功能说明

### 1. 系统模块 (system)

#### models.py
- `BaseModel`: 所有模型的基类，包含创建者、更新者、创建时间、更新时间等通用字段
- `Role`: 角色模型，定义系统角色及其权限
- `Dept`: 部门模型，定义组织架构
- `User`: 用户模型，继承自 Django 的 AbstractUser
- `Menu`: 菜单模型，定义系统菜单结构
- `Dict`: 字典模型，定义系统字典数据

#### permissions.py
- `IsAdminUser`: 检查用户是否为管理员
- `IsSuperUser`: 检查用户是否为超级管理员
- `IsOwnerOrAdmin`: 检查用户是否为对象的创建者或管理员
- `HasRolePermission`: 检查用户是否拥有指定角色权限

#### middleware.py
- `UserOperationMiddleware`: 记录用户操作日志的中间件

#### serializers.py
- 各种模型的序列化器，用于 API 数据的序列化和反序列化

### 2. 数据源模块 (datasource)

#### models.py
- `DataSource`: 数据源模型，存储数据库连接信息
- `QueryLog`: 查询日志模型，记录 SQL 查询操作

#### middleware.py
- `QueryLogMiddleware`: 记录数据查询日志的中间件

#### executors/
- 各种数据库连接和查询的执行器

### 3. 报表模块 (report)

#### models.py
- `PlatformInfo`: 平台信息模型
- `ModuleInfo`: 模块信息模型
- `ReportInfo`: 报表信息模型
- `InterfaceInfo`: 接口信息模型

### 4. 工具模块 (utils)

#### models.py
- `CoreModel`: 核心模型基类
- `BizBaseModel`: 业务模型基类

#### exception.py
- `CustomExceptionHandler`: 全局异常处理器

#### pagination.py
- `CustomPagination`: 自定义分页类

#### serializer.py
- 序列化器工具类和混合类

#### viewset.py
- `CustomModelViewSet`: 自定义视图集基类

#### util_response.py
- `SuccessResponse`: 成功响应类
- `DetailResponse`: 详情响应类
- `ErrorResponse`: 错误响应类

#### util_datasource.py
- 数据源连接和查询工具类

#### util_spark.py
- Spark 连接和操作工具类

#### util_kafka.py
- Kafka 消息队列工具类

#### excel_response.py
- Excel 导出工具类

#### import_export_mixin.py
- 数据导入导出混合类

### 5. 项目配置 (xadmin)

#### settings.py
- Django 项目配置文件

#### urls.py
- 项目 URL 配置

#### db_router.py
- 数据库路由配置

## 安装部署说明

### 1. 环境要求

- Python 3.8+
- PostgreSQL 12+
- Redis (可选，用于缓存)

### 2. 安装步骤

1. 克隆项目代码

```bash
git clone <repository-url>
cd backend_django
```

2. 创建并激活虚拟环境

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate    # Windows
```

3. 安装依赖包

```bash
pip install -r requirements.txt
```

4. 配置环境变量

```bash
cp .env_template .env
# 编辑 .env 文件，设置数据库连接信息和其他配置
```

5. 创建数据库

```bash
# 在 PostgreSQL 中创建数据库
createdb xadmin
```

6. 执行数据库迁移

```bash
python manage.py migrate
```

7. 初始化系统数据

```bash
python manage.py data_init
```

### 3. 运行项目

```bash
python manage.py runserver 0.0.0.0:8000
```

### 4. 生产环境部署

对于生产环境，建议使用 Gunicorn 或 uWSGI 作为 WSGI 服务器，并配合 Nginx 作为反向代理。

```bash
# 使用 Gunicorn 启动
gunicorn xadmin.wsgi:application --bind 0.0.0.0:8000 --workers 4
```

## API 文档

API 文档可通过以下方式访问：

```
http://localhost:8000/api/docs/
```

## 开发指南

### 1. 添加新应用

```bash
python manage.py startapp new_app
```

然后在 `settings.py` 的 `INSTALLED_APPS` 中添加新应用。

### 2. 创建新模型

在新应用的 `models.py` 中定义模型，继承 `utils.models.BizBaseModel`。

### 3. 创建序列化器

在新应用的 `serializers.py` 中创建序列化器。

### 4. 创建视图集

在新应用的 `views.py` 中创建视图集，继承 `utils.viewset.CustomModelViewSet`。

### 5. 配置 URL

在新应用的 `urls.py` 中配置 URL，然后在项目的 `urls.py` 中包含这些 URL。

## 许可证

[MIT License](LICENSE)