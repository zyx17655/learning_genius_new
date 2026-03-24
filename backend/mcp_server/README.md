# Smart Question MCP Server

基于MCP (Model Context Protocol) 协议的智能出题服务。

## 功能特性

- **标准MCP协议**：完全遵循MCP协议，支持stdio和HTTP双模式
- **多模型支持**：预留Kimi、OpenAI、Qwen等模型适配器接口
- **智能出题**：根据知识素材自动生成高质量考试题目
- **题目验证**：自动验证题目质量，确保符合标准
- **即插即用**：可被Claude Desktop、Cursor等AI应用直接调用

## 安装

```bash
pip install -r requirements.txt
```

## 配置

设置环境变量：

```bash
export KIMI_API_KEY="your-kimi-api-key"
```

## 运行模式

### Stdio模式（MCP协议）

用于AI应用连接（Claude Desktop、Cursor等）：

```bash
python run_stdio.py
```

### HTTP模式（REST API）

用于HTTP客户端调用：

```bash
python run_http.py
```

### 双模式

同时支持stdio和HTTP：

```bash
python run.py --mode dual
```

## MCP工具

### generate_questions

根据知识素材生成考试题目。

**参数**：
- `knowledge_input`: 知识素材内容
- `question_types`: 题目类型列表
- `type_counts`: 各题型数量
- `difficulty`: 难度（简单/中等/困难）

### verify_question

验证单个题目的质量。

### get_question_templates

获取题目模板。

### list_rules

获取可用规则列表。

## 在Claude Desktop中使用

编辑 `~/.config/claude-desktop/claude_desktop_config.json`：

```json
{
  "mcpServers": {
    "question-generator": {
      "command": "python",
      "args": ["/path/to/run_stdio.py"]
    }
  }
}
```

## API端点

- `GET /` - 服务信息
- `GET /health` - 健康检查
- `POST /generate/questions` - 生成题目
- `POST /verify/question` - 验证题目
- `GET /templates` - 获取模板
- `GET /rules` - 获取规则
- `GET /stats` - 统计信息

## License

MIT
