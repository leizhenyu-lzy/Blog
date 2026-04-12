#

[OpenAI API - Docs](https://developers.openai.com/api/docs)

[MCP - Docs](https://modelcontextprotocol.io)



LLM & Agent 进化
1. **LLM** : 只能做 文字接龙(predict next token)
2. 角色区分(一问一答的 对话)，为了 增加记忆 再细分
   1. **Context** (背景材料) : 对话历史 / 检索到的资料 / 用户身份 / 任务环境 / 工具返回结果
      1. 把每次对话历史 都放入 context，伪装成多人对话，作为 **Memory**(可以用 LLM 对 memory 进行 总结 & 压缩)
   2. **Prompt** (对模型的指示)
      1. User Prompt
      2. System Prompt : 不是用户直接说出的功能(角色 / 性格 / 背景知识)
3. **Agent 智能体** : 辅助 LLM 的 额外功能，显得更加智能
   1. 减少 用户 & LLM 直接沟通次数
   2. 处理 LLM 无法直接 生成的内容
4. 增加 **Search**(检索) 能力
   1. **RAG** (Retrieval Augmented Generation) 检索增强生成 : 给 LLM 增加 检索本地 向量数据库 能力(通过语义匹配)，并加入 Context
   2. **Web Search** (联网搜索)
5. **Function/Tool Call** : 约定 LLM 用固定格式(eg : json)回复 工具调用，方便 Agent 程序解析
   1. 避免 LLM 用自然语言 描述 辅助功能 调用，导致 Agent 解析困难
   2. Model 接收 Tool Definition & Message，不会自己真正执行 Tools，只 判断是否需要 Tools，选择 Tools，生成 结构化 调用请求，得到结果 组织成自然语言回复
   3. 外部程序 读取模型返回的 调用请求，执行函数/API，再把结果喂回模型
6. **MCP**(Model Context Protocol)
   1. 将 额外的辅助功能 从 Agent 拆分/解耦，单独写成服务，形成一套规范 让 Agent 程序能 发现/调用
   2. $\text{LLM} \xleftrightarrow{\text{Function Call}} \text{Agent} \xleftrightarrow{\text{MCP}} \text{Tools/MCP Server}$
   3. Agent 职责变为
      1. 发现和接入工具(MCP / 本地函数 / HTTP API / 数据库)
      2. 把 工具描述 暴露给 LLM(Tool Schema / Function Definition)
      3. 接收模型返回的 Tool Call，并调用工具执行，执行结果转发给模型，最终结果给用户
      4. 管理任务流程(多轮调用、错误处理、重试、记忆、权限控制、日志)
   4. MCP Server : 运行 Tool 的 服务
   5. MCP Client : 调用 MCP 的 Agent
7. 交互方式(Agent & User)
   1. CLI (命令行窗口) : Claude Code / iFlow / CodeX
   2. IDE (编程工具) : Cursor / Antigravity / Trae
   3. 桌面助手 : OpenClaw
8. **Workflow**(工作流) : 任务 拆成 预定义步骤，由 编排系统 按固定流程执行
   1. 某些步骤是 脚本/API，某些步骤调用 LLM
   2. 不一定需要 Agent 式的自主规划
9. **Skills** : 写给 agent 的可复用任务说明，告诉 agent 在 特定任务场景下 如何使用 仓库的 知识/工具/流程
   1. `skill.md`(入口，**required**)，告诉 agent : skills 使用场景，流程规范，补充资料/脚本
   2. 可以配合 reference / examples / scripts
   3. 提前约定 指定路径，在 Agent 中写死 路径，去读取对应位置的 markdown，省去每次都要告诉 agent skills 位置
10. **SubAgent** : Context 隔离
    1. 复杂任务，主 Agent 上下文很大
    2. 独立的 子任务 可以在 子Agent 内完成，上下文隔离(子 Agent 的上下文，不保留在 主Agent 中)










数据更新

早期的 LLM(如 GPT-3 刚发布时) 确实就像一个 **断网** 的图书馆

闭卷考试变开卷考试
1. RAG 检索增强生成 (Retrieval-Augmented Generation)
   1. 搜索引擎抓取相关的最新网页
   2. 抓到的网页内容和你的问题一起塞进 Context
   3. 准确度高，且通常会附带 来源链接 Citation
2. 工具调用与插件 (Tool Use / Function Calling)
   1. 实时 API 连接
   2. 识别出这是一个需要 工具 的任务，然后自动调用 天气预报/金融市场的 API 接口

