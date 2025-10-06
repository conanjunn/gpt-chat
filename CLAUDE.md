# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

这是一个基于 OpenAI Responses API 的网页聊天应用，支持多轮对话、历史记录和 Markdown 渲染。

## 开发环境设置

```bash
# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 运行服务

```bash
source venv/bin/activate && python server.py
```

服务将在 `http://0.0.0.0:5000` 启动。

## 配置说明

**重要**: `config.py` 包含 API 密钥和 URL，已加入 `.gitignore`，不应提交到 git。

`config.py` 必须包含以下变量：
- `API_URL`: OpenAI Responses API 端点
- `API_KEY`: API 认证密钥
- `MODEL`: 使用的模型名称
- `INSTRUCTIONS`: 系统指令

## 架构说明

### 后端 (server.py)

- **Flask 应用**: 提供 HTTP 服务和静态文件
- **会话管理**:
  - 使用内存字典 `conversations` 存储聊天记录
  - 使用 `last_access` 跟踪会话活跃时间
  - 自动清理超过 1 小时未使用的会话，防止内存泄漏
  - 每个会话最多保留 20 条消息
- **API 集成**:
  - 调用 OpenAI Responses API (`/v1/responses`)
  - 使用 Server-Sent Events (SSE) 流式返回响应
  - 解析 `response.output_text.delta` 事件获取文本增量
  - 启用 `web_search` 工具，由 LLM 自主决定是否使用

### 前端 (index.html)

- **会话持久化**: 使用 `localStorage` 保存 `conversationId`，刷新页面保持会话
- **历史记录加载**: 页面加载时从服务端获取历史记录并显示
- **Markdown 渲染**: 使用本地 `marked.min.js` 解析并渲染 Markdown 格式的回复
- **流式显示**: 使用 Fetch API + ReadableStream 实时显示响应

### OpenAI Responses API 关键点

- **请求格式**:
  - `input`: 消息数组，格式为 `[{"type": "message", "role": "user/assistant", "content": [...]}]`
  - `instructions`: 系统级指令
  - `tools`: 可用工具列表，如 `[{"type": "web_search"}]`
  - `stream`: 启用流式响应
  - `store`: 保存会话状态
- **响应格式**: SSE 流，每行格式为 `event: <type>` 和 `data: <json>`
- **文本增量**: 监听 `response.output_text.delta` 事件，`delta` 字段包含文本片段

## 注意事项

- 项目不使用外部 CDN（避免 HTTP 页面加载 HTTPS 资源的混合内容问题）
- `marked.min.js` 已下载到本地
- 服务器需要处理 `/marked.min.js` 路由返回静态文件
