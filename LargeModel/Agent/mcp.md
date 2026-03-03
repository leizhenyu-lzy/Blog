MCP (Model Context Protocol)

Anthropic 推出

解决 Tool Use 长期以来的痛点 : 大模型连接外部工具与数据的标准化问题

Tool Use 是 AI 的一种能力

MCP 是 工具的通用插座标准

没有 MCP 之前，开发者必须为每个工具编写一套特定的代码，换一个模型可能又要重写一遍

MCP 它提供了一个通用的协议，只要 数据源 实现了一个 MCP Server，任何支持 MCP 的模型都可以直接读取它

把压力从 模型端 转移到 服务端
1. 启动 MCP Client 时，它会问 Server 的能力
2. Server 回复 能力 & 描述
3. 模型理解，模型自动阅读这段描述，生成符合格式的指令


解耦 : 如果 Server API 变了，只需要 更新 MCP Server


MCP 的表现形式通常是一段 JSON 配置 或 轻量级的可执行程序

服务端 (MCP Server)
1. 并不关心是哪个 LLM 在调用它
2. 只负责 **暴露 Expose** 自己的能力
3. 简单的 Python 或 TypeScript 程序

客户端 (MCP Client)
1. 在 `config.json` 里加几行代码，指定 MCP Server 的路径

todo
