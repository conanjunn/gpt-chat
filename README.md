# AI Chat Web 应用

一个基于 OpenAI Responses API 的简洁网页聊天应用，支持多轮对话、历史记录和 Markdown 渲染。

## 功能特性

- ✨ 流式响应 - 实时显示 AI 回复
- 💬 多轮对话 - 支持上下文连续对话
- 📝 Markdown 渲染 - 自动渲染代码块、列表等格式
- 💾 会话持久化 - 刷新页面保持聊天记录
- 🔍 Web Search - AI 可自主决定是否联网搜索
- 📱 移动端适配 - 支持手机浏览器访问

## 快速开始

### 1. 环境准备

```bash
# Python 3.7+
python3 --version
```

### 2. 安装依赖

```bash
# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows

# 安装依赖包
pip install -r requirements.txt
```

### 3. 配置

复制配置示例文件并修改：

```bash
cp config.py.example config.py
```

编辑 `config.py`，填入你的 API 配置：

```python
API_URL = "https://api.openai.com/v1/responses"
API_KEY = "your-api-key-here"
MODEL = "gpt-4"
INSTRUCTIONS = "你是一个有帮助的助手"
```

### 4. 运行

```bash
source venv/bin/activate
python server.py
```

服务将在 `http://0.0.0.0:5000` 启动，浏览器访问即可使用。

## 项目结构

```
.
├── server.py           # Flask 后端服务
├── index.html          # 前端页面
├── marked.min.js       # Markdown 解析库
├── config.py           # 配置文件（需自行创建）
├── requirements.txt    # Python 依赖
└── CLAUDE.md          # 开发指南
```

## 技术栈

- **后端**: Flask + Requests
- **前端**: 原生 JavaScript + Marked.js
- **API**: OpenAI Responses API

## 架构说明

### 会话管理

- 使用内存存储聊天记录
- 每个会话最多保留 20 条消息
- 自动清理超过 1 小时未使用的会话

### OpenAI Responses API

本项目使用 OpenAI 的 Responses API，这是一个有状态的 API，特点：

- 支持流式响应
- 内置工具调用（如 web_search）
- 自动管理对话上下文

API 请求格式：

```python
{
    "model": "gpt-4",
    "instructions": "系统指令",
    "input": [
        {"type": "message", "role": "user", "content": [...]}
    ],
    "stream": True,
    "tools": [{"type": "web_search"}]
}
```

响应为 Server-Sent Events (SSE) 流，监听 `response.output_text.delta` 事件获取文本增量。

## 配置说明

### config.py 参数

- `API_URL`: API 端点地址
- `API_KEY`: API 认证密钥
- `MODEL`: 使用的模型名称（如 `gpt-4`、`gpt-5-codex` 等）
- `INSTRUCTIONS`: 系统级指令，定义 AI 的角色和行为

### 注意事项

- `config.py` 包含敏感信息，已加入 `.gitignore`，不要提交到版本控制
- 如使用 HTTP 访问，需注意混合内容问题（已使用本地 marked.js 解决）

## 开发

查看 [CLAUDE.md](CLAUDE.md) 了解详细的开发指南和架构说明。

## License

MIT License
