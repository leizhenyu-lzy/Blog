#

[OpenAI API - Docs](https://developers.openai.com/api/docs)


LLM & Agent 进化
1. **LLM** 本身只能做 文字接龙(predict next token)
2. 角色区分(一问一答的 对话)，为了 增加记忆，再细分为
   1. **Context** (背景材料) : 对话历史 / 检索到的资料 / 用户身份 / 任务环境 / 工具返回结果
      1. 把每次对话历史 都放入 context，伪装成多人对话，作为 **Memory**(可以用 LLM 对 memory 进行 总结 & 压缩)
   2. **Prompt** (对模型的指示) : 角色设定 / 任务要求 / 输出格式 / 约束条件 / 最终指令
3. **Agent 智能体** : 辅助 LLM 的 额外功能，显得更加智能
   1. 减少 用户 & LLM 直接沟通次数
   2. 处理 LLM 无法直接 生成的内容
4. 增加 **Search**(检索) 能力
   1. **RAG** (Retrieval Augmented Generation) 检索增强生成 : 给 LLM 增加 检索本地 向量数据库 能力(通过语义匹配)，并加入 Context
   2. **Web Search** (联网搜索)
5. **Function Calling** : 避免 LLM 用自然语言 描述 tool 辅助功能的 调用，约定 用固定格式(eg : json)回复，方便 Agent 程序解析
   1. Model : 接收 Tool Definition & Message，不会自己真正执行 Tools，只 判断是否需要 Tools，选择 Tools，生成 结构化 调用请求，得到结果 组织成自然语言回复
   2. 外部程序 : 读取模型返回的 调用请求，执行函数/API，再把结果喂回模型
6. **MCP**











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

