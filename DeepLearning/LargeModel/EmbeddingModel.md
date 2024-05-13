# Embedding Model

---

## Table of Contents

- [Embedding Model](#embedding-model)
  - [Table of Contents](#table-of-contents)
- [Embedding 排行榜](#embedding-排行榜)
- [FlagEmbedding(BAAI)](#flagembeddingbaai)
- [word2vec](#word2vec)

---


embedding是一种将数据（如文本）转化为高维向量的表示方法，这种表示方法使得在某些特定方面相似的数据在向量空间中彼此接近，而与之不相关的数据则相距较远，能够捕捉词语和句子之间的语义关系，数据能够有效用于聚类、分类、信息搜索、知识库检索等应用场景。

# Embedding 排行榜

[HuggingFace - MTEB(Massive Text Embedding Benchmark)](https://huggingface.co/spaces/mteb/leaderboard)





# FlagEmbedding(BAAI)

RAG 开发时 会涉及到向量数据库，需要使用 Embedding 模型对文本进行 向量化 处理

大模型如 OpenAI,Gemini 的模型都提供可供调用的 Embedding 模型，但是根据 token 数量来收费

[FlagOpen - BAAI(北京智源人工智能研究院)](https://flagopen.baai.ac.cn/#/home)

[FlagEmbedding(BAAI) - Github](https://github.com/FlagOpen/FlagEmbedding)，中国人自己开发的，同时支持中文和英文


# word2vec


