![](Pics/langchain000.png)

---

# 目录
- [目录](#目录)
- [LangChain](#langchain)
  - [Introduction](#introduction)
  - [QuickStart](#quickstart)
  - [Components](#components)
  - [LangChain \& ZhipuAI(ChatGLM)](#langchain--zhipuaichatglm)
    - [Getting started](#getting-started)
    - [ChatGLM + LangChain 实践培训 (实现基于本地知识的问答)](#chatglm--langchain-实践培训-实现基于本地知识的问答)
- [九天玩转 Langchain](#九天玩转-langchain)
  - [第 01 讲 - 简介](#第-01-讲---简介)
  - [第 02 讲 - HelloWorld](#第-02-讲---helloworld)
  - [第 03 讲 -](#第-03-讲--)
  - [第 04 讲 -](#第-04-讲--)
  - [第 05 讲 -](#第-05-讲--)
  - [第 06 讲 -](#第-06-讲--)
  - [第 07 讲 -](#第-07-讲--)
  - [第 08 讲 -](#第-08-讲--)
  - [第 09 讲 -](#第-09-讲--)
  - [第 10 讲 -](#第-10-讲--)
- [Functions, Tools and Agents with LangChain](#functions-tools-and-agents-with-langchain)
- [LangChain for LLM Application Development](#langchain-for-llm-application-development)
- [Additional Reading](#additional-reading)
  - [RESTful API](#restful-api)


---

# LangChain

[LangChain - 官网](https://www.langchain.com/)

[LangChain Docs - 官网](https://python.langchain.com/docs/get_started/introduction/)



## Introduction

LangChain is a framework for developing applications powered by large language models

Simplifies every stage of the LLM application lifecycle
1. Development开发 - using LangChain's open-source building **blocks** and [components](https://python.langchain.com/docs/modules/)
2. Productionization生产 - **LangSmith** to inspect, monitor and evaluate your chains
3. Deployment部署 - Turn any chain into an API with **LangServe**

![](Pics/langchain001.svg)

framework consists of the following open-source libraries
1. langchain-core : 基础抽象和LangChain表达式语言
2. langchain-community : 第三方集成，如langchain-openai、langchain-anthropic等
3. langchain : Chains, agents, and retrieval strategies
4. langgraph : Build robust and stateful multi-actor applications with LLMs by modeling steps
5. langserve : deploy chains as REST APIs
6. LangSmith : developer platform (debug, test, evaluate, and monitor LLM applications)

## QuickStart



## Components

[Components](https://python.langchain.com/docs/modules/)

**Main Components**
1. [Model I/O](https://python.langchain.com/docs/modules/model_io/)
   ![](Pics/langchain003.png)
   1. **Prompts**
   2. **Chat Models**
      1. tuned for **conversations**
      2. take a list of chat messages(not single string) as input and they return an AI message as output
      3. 受 上下文窗口 限制 - 对话管理策略 : 信息压缩和摘要、关键信息标记
   3. **LLMs**
      1. in LangChain == **pure text completion models**
      2. take **a string prompt as input** and **output a string completion**
   4. **Output Parsers**
   5. What's More
      1. Different models have different prompting strategies that work best for them
      2. **Anthropic**'s models work best with **XML** (P.S. Anthropic 是一家人工智能研究和安全公司，由前OpenAI员工创建，Claude)
      3. **OpenAI**'s models work best with **JSON**
2. Retrieval
   1. Document Loaders
   2. Text Splitters
   3. Embedding Models
   4. Vectorestores
   5. Retrievers
3. Composition
   1. Tools
   2. Agents
   3. Chains
4. Additional
   1. Memory
   2. Callbacks



## LangChain & ZhipuAI(ChatGLM)

[LangChain & ZhipuAI - LangChain官网](https://python.langchain.com/docs/integrations/chat/zhipuai/)

[资源包管理 - 智谱AI开放平台](https://open.bigmodel.cn/usercenter/resourcepack)

[GLM-4 接口文档 - 智谱AI](https://open.bigmodel.cn/dev/api#glm-4)

### Getting started

**Installation**

```python
%pip install --quiet httpx[socks]==0.24.1 httpx-sse PyJWT
```

**Importing the Required Modules**

```python
from langchain_community.chat_models import ChatZhipuAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

zhipuai_api_key = "your_api_key"
```

### ChatGLM + LangChain 实践培训 (实现基于本地知识的问答)

[ChatGLM + LangChain 实践培训](https://www.bilibili.com/video/BV13M4y1e7cN/)

[ LangChain-Chatchat (原 Langchain-ChatGLM) 配套代码](https://github.com/chatchat-space/Langchain-Chatchat)

ChatGLM 具备的能力
1. 自我认知
2. 提纲写作
3. 文案写作
4. 信息抽取

LangChain 应用场景
1. 文档问答
2. 个人助理
3. 查询表格数据
4. API 交互
5. 信息提取
6. 文档总结

基于 **单一文档问答** 的实现原理
1. 加载本地文档 - 读取本地文档加载为文本
2. 文本拆分 - 将文本按照 字符、长度或语义 进行拆分 - 输入有长度限制
   1. chunking - 分块 - 指的是将长文本分割成的较小的、可管理的段落或部分
   2. 内存管理、并行处理
3. 根据提问匹配文本 - 根据用户提问对文本进行 字符匹配 或 **语义检索(向量化 & 向量空间检索)**
4. 构建prompt - 将匹配文本、用户提问加入Prompt模板
5. LLM生成回答 - 将Prompt发送给LLM获得基于文档内容的回答

基于 **本地知识库问答** 的实现原理 (VectorStore 向量数据库)
![](Pics/rag001.png)


AIMessage
SystemMessage
HumanMessage














---

# 九天玩转 Langchain

[九天玩转Langchain](https://space.bilibili.com/1235535223/channel/collectiondetail?sid=1794575)

## 第 01 讲 - 简介

LLM - 补全

Prompt 提示词

主流 LLM
1. GPT
2. LLaMA(Large Language Model Meta AI)
3. ChatGLM - 中文语料

GPT API
1. model - 模型选择
2. prompt
3. temperature - 模型发散能力

几个问题
1. 如何 格式化 输出 json/csv
2. 提示词长度 / 长文本
3. 多次进行 API 调用，连续的问题
4. 调用外部的服务
5. 标准化的开发
6. 快速切换模型

LangChain 类似与工具箱，协助 LLM 应用开发

设计思路 - 交互流程 模块化、抽象化

Mixture of Experts - 专家混合模型
1. 将大型网络分解为多个较小的子网络
2. 每个专家负责学习输入数据的一部分
3. 进行预测时，MoE模型会根据输入选择最相关的专家进行处理
4. 一个 **门控机制** gating mechanism，决定哪个专家对于给定的输入最为合适，从而只激活一个或少数几个专家进行计算
5. 提高模型的效率和扩展性
6. MoE特别适用于处理非常大的数据集和模型，因为它允许模型动态地只激活相关的部分


## 第 02 讲 - HelloWorld



LLM 模型
1. 本地
2. API
   1. 百度 ERNIE
   2. 阿里 Qwen
   3. Replicate
   4. OpenAI

predict 根据输入的文本生成新的文本




## 第 03 讲 -

## 第 04 讲 -

## 第 05 讲 -

## 第 06 讲 -

## 第 07 讲 -

## 第 08 讲 -

## 第 09 讲 -

## 第 10 讲 -



# Functions, Tools and Agents with LangChain

[Functions, Tools and Agents with LangChain](https://learn.deeplearning.ai/courses/functions-tools-agents-langchain/lesson/1/introduction)





---

# LangChain for LLM Application Development

[LangChain for LLM Application Development](https://learn.deeplearning.ai/courses/langchain/lesson/1/introduction)




---


# Additional Reading

## RESTful API

[RESTful 个人笔记](../../Software/restful.md)
