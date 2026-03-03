# 智能教学系统 - 题库管理模块

## 项目简介

本项目是一个智能教学系统中的题库管理模块，重点实现了AI出题功能，支持基于知识点自动生成高质量题目。

## 技术栈

- **前端**：Vue 2 + Element UI + ECharts
- **后端**：Python + Flask + SQLAlchemy
- **数据库**：MySQL 5.6.16
- **AI引擎**：OpenAI API

## 核心功能

### 1. 题库管理
- 题目CRUD操作
- 批量导入/导出
- 题目分类和标签管理
- 题目状态管理（草稿/已审核/已禁用）

### 2. AI智能生题
- 知识范围树形选择
- 题型、难度、数量配置
- 高级要求设置（干扰项基于常见误区、结合实际故障案例等）
- 实时生成进度显示
- 生成结果预览和可解释性分析
- 题目审核和入库流程

### 3. 题目分析
- 知识点覆盖分析
- 难度分布分析
- 题型分布分析
- 使用情况分析

## 项目结构

```
learning_genius/
├── backend/           # 后端代码
│   ├── app/           # 应用代码
│   │   ├── __init__.py
│   │   ├── models.py  # 数据库模型
│   │   └── routes.py  # API路由
│   ├── config/        # 配置文件
│   │   └── config.py
│   ├── requirements.txt  # 依赖管理
│   ├── init_db.py     # 数据库初始化
│   └── run.py         # 应用入口
├── frontend/          # 前端代码
│   ├── public/        # 静态资源
│   ├── src/           # 源代码
│   │   ├── api/       # API调用
│   │   ├── components/ # 组件
│   │   ├── views/     # 页面
│   │   ├── App.vue    # 根组件
│   │   └── main.js    # 入口文件
│   └── package.json   # 依赖管理
└── README.md          # 项目说明
```

## 运行说明

### 后端运行
1. 安装依赖：`pip install -r backend/requirements.txt`
2. 配置数据库连接（修改 `backend/config/config.py`）
3. 初始化数据库：`python backend/init_db.py`
4. 启动服务：`python backend/run.py`

### 前端运行
1. 安装依赖：`npm install`（在frontend目录下）
2. 启动开发服务器：`npm run serve`
3. 访问：`http://localhost:8080`

## 环境变量

需要设置以下环境变量：
- `OPENAI_API_KEY`：OpenAI API密钥
- `DATABASE_URL`：数据库连接字符串
- `SECRET_KEY`：Flask密钥

## 注意事项

1. 确保MySQL数据库已安装并运行
2. 确保OpenAI API密钥有效
3. 开发环境下，Flask默认运行在 `http://localhost:5000`
4. 前端默认运行在 `http://localhost:8080`

## 功能扩展

- 支持多语言题目生成
- 增加多媒体题目支持
- 实现题目版本控制
- 添加协作编辑功能
- 构建题目共享平台