# XAdmin 项目

## 项目概述
XAdmin 是一个基于Ruoyi-Vue3开发的前后端分离管理系统，由Django后端和Vue 3前端组成。该系统提供了用户认证、系统管理、数据源管理、数据查询和报表管理等核心功能，旨在提供一个简单、易用且功能强大的管理界面。

## 项目结构

```
├── backend_django/         # Django后端项目
│   ├── .venv/              # Python虚拟环境
│   ├── app_init/           # 应用初始化模块
│   ├── datasource/         # 数据源管理模块
│   ├── report/             # 报表管理模块
│   ├── system/             # 系统管理模块
│   ├── utils/              # 工具类
│   ├── xadmin/             # 项目配置
│   ├── manage.py           # Django管理脚本
│   └── requirements.txt    # 依赖包列表
├── frontend/               # Vue 3前端项目
│   ├── public/             # 静态资源
│   ├── src/                # 源代码
│   │   ├── assets/         # 资源文件
│   │   ├── components/     # 组件
│   │   ├── layout/         # 布局组件
│   │   ├── router/         # 路由配置
│   │   ├── store/          # 状态管理
│   │   ├── utils/          # 工具函数
│   │   ├── views/          # 视图组件
│   │   ├── App.vue         # 根组件
│   │   └── main.js         # 入口文件
│   ├── index.html          # HTML入口
│   ├── package.json        # 依赖配置
│   └── vite.config.js      # Vite配置
└── backend/                # 其他后端项目(Java)
```

## 技术栈

### 后端
- Python 3.6+
- Django 5.0.3
- Django REST Framework 3.15.2
- PostgreSQL 数据库
- JWT认证
- PySpark (用于数据处理)

### 前端
- Vue 3
- Vite
- Element Plus
- Pinia (状态管理)
- Vue Router
- Monaco Editor (代码编辑器)
- Axios (HTTP客户端)

## 功能模块

### 系统管理
- 用户管理：用户的增删改查、登录注册
- 角色管理：角色的增删改查、权限分配
- 菜单管理：系统菜单的配置
- 系统配置：系统参数的配置
- 系统日志：记录用户操作日志

### 数据源管理
- 数据源配置：支持多种数据库连接(MySQL, PostgreSQL等)
- 连接测试：测试数据源连接是否正常
- 数据查询：执行SQL查询并展示结果
- 查询日志：记录查询历史

### 报表管理
- 平台管理：报表平台的管理
- 模块管理：报表模块的管理
- 报表设计：创建和编辑报表
- 接口管理：管理报表接口
- 接口字段：配置接口字段

## 安装指南

### 后端安装

1. **克隆项目**
   ```bash
   git clone https://github.com/your-repo/xadmin.git
   cd xadmin
   ```

2. **使用虚拟环境**
   ```bash
   # 进入后端目录
   cd backend_django
   
   # 激活已创建的虚拟环境
   source .venv/bin/activate  # Linux/Mac
   # 或
   .venv\Scripts\activate  # Windows
   ```

3. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

4. **配置环境变量**
   创建`.env`文件在`backend_django`目录下，添加以下内容：
   ```
   DB_NAME=your_db_name
   DB_USER=your_db_user
   DB_PASSWORD=your_db_password
   DB_HOST=localhost
   DB_PORT=5432
   ```

5. **数据库迁移**
   ```bash
   python manage.py migrate
   ```

6. **创建超级用户**
   ```bash
   python manage.py createsuperuser
   ```

7. **启动开发服务器**
   ```bash
   python manage.py runserver
   ```

### 前端安装

1. **进入前端目录**
   ```bash
   cd frontend
   ```

2. **安装依赖**
   ```bash
   npm install
   ```

3. **启动开发服务器**
   ```bash
   npm run dev
   ```

## 使用说明

1. **访问后台管理系统**
   - 前端: http://localhost:5173 (默认Vite端口)
   - 后端API: http://localhost:8000

2. **登录系统**
   - 使用创建的超级用户账号登录
   - 或使用注册功能创建新账号

3. **系统配置**
   - 首先配置角色和权限
   - 然后添加数据源
   - 最后可以进行数据查询和报表设计

## 开发指南

### 后端开发
- 遵循Django REST Framework的开发规范
- 新功能开发请在对应的应用目录下进行
- 使用Django的ORM进行数据库操作
- 使用JWT进行身份验证

### 前端开发
- 遵循Vue 3的组件化开发方式
- 使用Element Plus组件库进行UI开发
- 使用Pinia进行状态管理
- 使用Vue Router进行路由管理

## 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建Pull Request