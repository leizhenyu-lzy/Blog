![](Pics/dify001.png)

# Dify

**[Dify - Github](https://github.com/langgenius/dify)**

**[Dify.ai - zh/cn](https://dify.ai/zh)**

**[Dify.ai - en/us](https://dify.ai/)**

**[Dify Docs](https://docs.dify.ai/v/zh-hans)**

**[Dify LLMs App Stack](https://assets.dify.ai/files/dify_llms_app_stack_cn.pdf)**

![](Pics/dify002.png)

---

## Table of Contents

- [Dify](#dify)
  - [Table of Contents](#table-of-contents)
- [Introduction](#introduction)
- [Deploy Community Edition](#deploy-community-edition)
  - [Docker Compose 部署](#docker-compose-部署)


---

# Introduction

Combine
1. **Backend-as-a-Service** : 后端即服务，不再编写或管理所有服务端组件，可以使用领域通用的远程组件(而不是进程内的库)来提供服务
2. **LLMOps**(Large Language Model Operations) - 涵盖了大型语言模型 **训练、开发、部署、监控、维护、优化、安全**
   1. 数据准备 - 数据收集、预处理工具，简化数据清洗和标注
   2. Prompt Engineering - Prompt 编辑和调试
   3. Embedding & LongContext - 自动处理长上下文的嵌入、存储和管理
   4. 应用监控 & 维护 - 监控性能 + 日志记录
   5. Fine Tuning - 提供一键微调功能
   6. DevOps - 支持多人协同、易用的界面

基础信息
1. 后端技术 - Python/Flask/PostgreSQL
2. 前端技术 - Next.js

Dify is an **open-source** LLM app development platform
1. Agent capabilities
2. AI workflow - Build and test powerful AI workflows on a visual canvas
   ![](Pics/dify003.png)
3. RAG pipeline
4. model management
5. observability features
6. knowledge base
7. go from prototype to production



enable developers to quickly build production-grade generative AI applications

# Deploy Community Edition

[Dify CE - Github](https://github.com/langgenius/dify)

## Docker Compose 部署

查看 **`docker`** & **`docker compose`** 版本

```bash
lzy@legion:~ $ docker --version
Docker version 26.1.2, build 211e74b

lzy@legion:~ $ docker compose version
Docker Compose version v2.24.6-desktop.1
```

**Clone**

```bash
git clone https://github.com/langgenius/dify.git
```

**Start**

```bash
cd dify/docker
sudo docker compose up -d
```

deployment procedure

![](Pics/dify004.png)

deployment result

![](Pics/dify005.png)

```bash
docker compose ps
```

![](Pics/dify006.png)

**Upgrade**

```bash
cd dify/docker
git pull origin main
docker compose down
docker compose pull
docker compose up -d
```

**Access**

访问 Dify 在浏览器中输入 [http://localhost](http://localhost)

```edge

```
