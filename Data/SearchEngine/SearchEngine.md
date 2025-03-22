# Search Engine

---

## Table of Contents

- [Search Engine](#search-engine)
  - [Table of Contents](#table-of-contents)
- [Indexing](#indexing)
  - [Forward Index - 正排索引](#forward-index---正排索引)
  - [Inverted Index - 倒排索引](#inverted-index---倒排索引)

---

# Indexing

正排索引是 **给出ID查Value**，倒排索引是 **给出Value查ID**

## Forward Index - 正排索引

每个文档有一个唯一的ID，索引将文档ID映射到文档的内容。通过文档的ID可以快速查找到对应的文档内容

## Inverted Index - 倒排索引

每个词汇都对应一个文档列表，列出包含该词汇的所有文档的ID。通过词汇可以快速查找到包含该词汇的所有文档ID

工作原理
1. 对所有文档进行分词处理，提取每个词汇
2. 为每个词汇建立一个列表，存储包含该词汇的文档ID
3. 用户提供一个词汇时，可以快速获取包含该词汇的所有文档ID

搜索引擎中最常用的索引类型，因为它使得根据关键词快速检索文档变得可能


