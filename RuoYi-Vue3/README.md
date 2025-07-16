# RuoYi-Vue3 前端项目文档

## 项目介绍

RuoYi-Vue3是一个基于Vue3、Vite、Element Plus的前端解决方案，是若依管理系统的前端实现。该项目提供了丰富的功能模块和组件，可以快速搭建企业级中后台产品。

## 技术栈

### 核心框架
- Vue 3.4.x - 渐进式JavaScript框架
- Vue Router 4.4.x - Vue.js官方路由管理器
- Pinia 2.1.x - Vue.js的状态管理库
- Vite 5.3.x - 前端构建工具

### UI组件
- Element Plus 2.7.x - 基于Vue 3的组件库
- @element-plus/icons-vue 2.3.x - Element Plus的图标库

### 工具库
- Axios 0.28.x - 基于Promise的HTTP客户端
- ECharts 5.5.x - 数据可视化图表库
- js-cookie 3.0.x - 简单、轻量的处理cookies的js API
- jsencrypt 3.3.x - 用于执行OpenSSL RSA加密、解密和密钥生成的Javascript库
- vue-cropper 1.1.x - 图片裁剪插件
- @vueup/vue-quill 1.2.x - 富文本编辑器
- file-saver 2.0.x - 文件保存库
- fuse.js 6.6.x - 轻量级模糊搜索库

### 开发工具
- Sass 1.77.x - CSS预处理器
- unplugin-auto-import 0.17.x - 自动导入API
- vite-plugin-svg-icons 2.0.x - SVG图标插件
- vite-plugin-compression 0.5.x - 资源压缩插件

## 功能模块

### 系统管理
- 用户管理：用户是系统操作者，该功能主要完成系统用户配置。
- 部门管理：配置系统组织机构（公司、部门、小组），树结构展现支持数据权限。
- 岗位管理：配置系统用户所属担任职务。
- 菜单管理：配置系统菜单，操作权限，按钮权限标识等。
- 角色管理：角色菜单权限分配、设置角色按机构进行数据范围权限划分。
- 字典管理：对系统中经常使用的一些较为固定的数据进行维护。
- 参数管理：对系统动态配置常用参数。
- 通知公告：系统通知公告信息发布维护。

### 系统监控
- 在线用户：监视当前系统中活跃用户状态。
- 定时任务：在线（添加、修改、删除）任务调度包含执行结果日志。
- 数据监控：监视当前系统数据库连接池状态，可进行分析SQL找出系统性能瓶颈。
- 服务监控：监视当前系统CPU、内存、磁盘、堆栈等相关信息。
- 缓存监控：对系统的缓存信息查询，命令统计等。
- 日志监控：系统操作日志记录和查询；系统登录日志记录和查询。

### 数据资产管理
- 数据源管理：管理各种类型的数据源连接，包括MySQL、PostgreSQL、StarRocks等。
- 数据查询：提供数据查询功能，可以查询各种数据源的数据。
- 查询日志：记录用户的查询操作，方便追踪和审计。
- 报表管理：管理系统报表，提供报表展示和数据分析功能。
- 接口管理：管理系统接口，包括接口字段、接口数据查看等功能。
- 报表开发：提供报表开发功能，根据查询sql生成报表配置并同步到报表管理功能列表。(计划中...)
- 数据同步任务：提供数据同步功能，可以定时同步数据源的数据到数据库中。（计划中...）


### 系统工具
- 表单构建：拖拽表单元素生成相应的Vue代码。


## 安装部署

### 开发环境准备

1. 安装Node.js (推荐版本 16.x 或更高)
2. 安装包管理工具 npm 或 yarn

### 安装依赖

```bash
# 进入项目目录
cd RuoYi-Vue3

# 使用yarn安装依赖
yarn install

# 或使用npm安装依赖
npm install
```

### 开发模式运行

```bash
# 使用yarn
yarn dev

# 或使用npm
npm run dev

# 或使用批处理文件
bin/run-web.bat
```

启动成功后，浏览器访问 http://localhost:80

### 生产环境构建

```bash
# 使用yarn构建生产环境
yarn build:prod

# 或使用npm构建生产环境
npm run build:prod

# 或使用批处理文件
bin/build.bat
```

构建完成后，会在根目录生成 dist 文件夹，里面包含了所有静态资源文件。

### 环境配置

项目提供了多环境配置文件：

- `.env.development` - 开发环境配置
- `.env.production` - 生产环境配置
- `.env.staging` - 测试环境配置

可以根据需要修改这些配置文件中的参数。

## 项目结构

```
├── bin                      # 批处理脚本目录
├── public                   # 静态资源目录
├── src                      # 源代码目录
│   ├── api                  # 接口请求目录
│   ├── assets               # 主题、字体等静态资源
│   ├── components           # 全局公共组件
│   ├── directive            # 全局指令
│   ├── layout               # 布局组件
│   ├── plugins              # 插件配置
│   ├── router               # 路由配置
│   ├── store                # 全局状态管理
│   ├── utils                # 全局公用方法
│   ├── views                # 所有页面
│   ├── App.vue              # 入口页面
│   ├── main.js              # 入口文件
│   └── permission.js        # 权限管理
├── vite                     # vite配置
├── .env.development         # 开发环境配置
├── .env.production          # 生产环境配置
├── .env.staging             # 测试环境配置
├── vite.config.js           # vite配置文件
└── package.json             # 项目依赖
```

## 浏览器支持

支持现代浏览器和Internet Explorer 11+

| [<img src="https://raw.githubusercontent.com/alrra/browser-logos/master/src/edge/edge_48x48.png" alt="IE / Edge" width="24px" height="24px" />](http://godban.github.io/browsers-support-badges/)</br>IE / Edge | [<img src="https://raw.githubusercontent.com/alrra/browser-logos/master/src/firefox/firefox_48x48.png" alt="Firefox" width="24px" height="24px" />](http://godban.github.io/browsers-support-badges/)</br>Firefox | [<img src="https://raw.githubusercontent.com/alrra/browser-logos/master/src/chrome/chrome_48x48.png" alt="Chrome" width="24px" height="24px" />](http://godban.github.io/browsers-support-badges/)</br>Chrome | [<img src="https://raw.githubusercontent.com/alrra/browser-logos/master/src/safari/safari_48x48.png" alt="Safari" width="24px" height="24px" />](http://godban.github.io/browsers-support-badges/)</br>Safari |
| --------- | --------- | --------- | --------- |
| IE11, Edge | last 2 versions | last 2 versions | last 2 versions |

## 许可证

[MIT](https://opensource.org/licenses/MIT)

版权所有 © 2023 若依