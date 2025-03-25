# XAdmin 前端项目文档

## 项目概述

XAdmin是一个基于Vue 3的后台管理系统，主要功能包括用户认证、系统管理、数据源管理、数据查询和报表管理等。项目使用了Element Plus作为UI组件库，Pinia进行状态管理，Vue Router进行路由管理，以及Monaco Editor作为代码编辑器。

## 目录结构及功能说明

### 根目录

- `index.html`: 项目的HTML入口文件
- `vite.config.js`: Vite构建工具的配置文件
- `package.json`: 项目依赖和脚本配置文件

### src目录

#### 主要文件

- `main.js`: 应用程序的入口文件，负责初始化Vue应用、注册Element Plus组件和图标、配置路由和状态管理
- `App.vue`: 应用程序的根组件
- `style.css`: 全局样式文件

#### assets目录

- `vue.svg`: Vue框架的SVG图标

#### components目录

- `MonacoEditor.vue`: Monaco编辑器组件，用于SQL查询等代码编辑场景，支持语法高亮、代码补全等功能
- `QueryResult.vue`: 查询结果展示组件，用于展示SQL查询的结果，支持分页、排序和格式化等功能

#### layout目录

- `index.vue`: 布局主组件，定义了应用的整体布局结构
- `components/AppMain.vue`: 主内容区域组件
- `components/Sidebar.vue`: 侧边栏组件，用于导航菜单展示
- `components/SidebarItem.vue`: 侧边栏菜单项组件
- `components/TagView.vue`: 标签视图组件，用于多页签导航

#### router目录

- `index.js`: 路由配置文件，定义了应用的路由结构，包括登录/注册、仪表盘、系统管理、数据源管理、数据开发和报表信息等模块

#### utils目录

- `config.js`: 配置文件，包含API配置、用户存储键名、HTTP状态码和错误消息等常量
- `request.js`: 网络请求封装，基于axios实现，包含请求拦截器和响应拦截器，用于处理认证和错误情况

#### views目录

##### 主要视图

- `Login.vue`: 登录页面，包含用户名和密码输入框，以及登录功能
- `Register.vue`: 注册页面，用于新用户注册
- `Dashboard.vue`: 仪表盘页面，系统首页
- `DataSources.vue`: 数据源管理页面，用于管理数据库连接

##### dataquery目录

- `index.vue`: 数据查询页面，包含数据源选择、SQL编辑器和查询结果展示等功能
- `QueryLog.vue`: 查询日志页面，用于查看历史查询记录

##### reportinfo目录

- `index.vue`: 报表信息主页面
- `PlatformManage.vue`: 平台管理页面，用于管理报表平台
- `ModuleManage.vue`: 模块管理页面，用于管理报表模块
- `ReportManage.vue`: 报表设计页面，用于创建和编辑报表
- `InterfaceManage.vue`: 接口管理页面，用于管理报表接口
- `InterfaceFields.vue`: 接口字段管理页面，用于配置接口字段

##### system目录

- `Config.vue`: 系统配置页面，用于管理系统参数
- `Log.vue`: 系统日志页面，用于查看系统日志
- `Menu.vue`: 菜单管理页面，用于管理系统菜单
- `Roles.vue`: 角色管理页面，用于管理用户角色和权限
- `Users.vue`: 用户管理页面，用于管理系统用户

## 功能模块说明

### 用户认证

用户认证模块包括登录和注册功能，通过`Login.vue`和`Register.vue`实现。用户登录成功后，会将token和用户信息存储在localStorage中，并通过请求拦截器添加到后续请求的头部。

### 系统管理

系统管理模块包括用户管理、角色管理、菜单管理、系统配置和系统日志等功能，通过`system`目录下的组件实现。

### 数据源管理

数据源管理模块用于管理数据库连接，通过`DataSources.vue`实现。用户可以添加、编辑和删除数据源，并测试连接。

### 数据查询

数据查询模块是系统的核心功能之一，通过`dataquery/index.vue`实现。它包含以下功能：

- 数据源选择：用户可以选择要查询的数据源
- SQL编辑器：基于Monaco Editor实现的SQL编辑器，支持语法高亮和代码补全
- 查询执行：执行SQL查询并展示结果
- 结果展示：以表格形式展示查询结果，支持分页和排序
- 多标签页：支持多个查询结果的标签页管理

### 报表管理

报表管理模块是系统的另一个核心功能，通过`reportinfo`目录下的组件实现。它包含以下功能：

- 平台管理：管理报表平台
- 模块管理：管理报表模块
- 报表设计：创建和编辑报表
- 接口管理：管理报表接口，包括接口的基本信息、数据库配置等
- 接口字段管理：配置接口字段，包括字段名称、类型、描述等

## 技术栈

- **前端框架**：Vue 3
- **UI组件库**：Element Plus
- **状态管理**：Pinia
- **路由管理**：Vue Router
- **HTTP客户端**：Axios
- **代码编辑器**：Monaco Editor
- **构建工具**：Vite

## 开发和构建

### 开发环境

```bash
npm run dev
```

### 生产构建

```bash
npm run build
```

### 预览构建结果

```bash
npm run preview
```
