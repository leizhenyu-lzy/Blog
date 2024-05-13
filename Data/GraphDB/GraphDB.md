# Graph Database

---

## Table of Contents
- [Graph Database](#graph-database)
  - [Table of Contents](#table-of-contents)
- [Overview 综述](#overview-综述)
  - [主流开源 GraphDB](#主流开源-graphdb)

---

# Overview 综述

[ISO/IEC 39075:2024 - (Information technology) Database languages GQL](https://www.iso.org/standard/76120.html)

GQL - Graph Query Language (a peer, complementary language to SQL)

**图数据库 ≠ 向量数据库**

**图数据库**
1. 存储和管理 **图结构的数据**
2. 由 节点(实体) 和 边(关系) 组成
3. 优化 遍历 节点和边 的操作，能够快速执行 **深度连接查询** 和 **递归查询**
4. 场景
   1. 社交网络
   2. 供应链
   3. 知识图谱
5. Neo4j、ArangoDB、JanusGraph

**向量数据库**
1. 存储和处理 **向量数据**
2. 可以快速执行向量之间的相似性搜索
3. 利用索引结构 (如 KD树、球树 等) 来优化向量空间的近邻搜索，从而快速找到与给定向量最相似的项
4. 场景
   1. 推荐系统
   2. 图像检索
   3. 自然语言处理
5. Milvus、Faiss、Elasticsearch


## 主流开源 GraphDB

[图数据库比较：Neo4j、OrientDB、ArangoDB等 - 百度开发者中心](https://developer.baidu.com/article/details/3047134)

主流开源图数据库
1. [Neo4j](https://neo4j.com/)
   ![](Pics/graph001.png)
2. [OrientDB](https://www.orientdb.org/)
   ![](Pics/graph002.png)
3. JanusGraph
4. HugeGraph
5. ArangoDB








