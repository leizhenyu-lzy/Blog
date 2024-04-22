# RAG

---

## Table of Content
- [RAG](#rag)
  - [Table of Content](#table-of-content)
- [Retrieval-Augmented Generation for Large Language Models: A Survey](#retrieval-augmented-generation-for-large-language-models-a-survey)
- [12 RAG Pain Points and Proposed Solutions-Solving the core challenges of Retrieval-Augmented Generation](#12-rag-pain-points-and-proposed-solutions-solving-the-core-challenges-of-retrieval-augmented-generation)

---

# Retrieval-Augmented Generation for Large Language Models: A Survey

[Retrieval-Augmented Generation for Large Language Models: A Survey](https://arxiv.org/abs/2312.10997)





---

# 12 RAG Pain Points and Proposed Solutions-Solving the core challenges of Retrieval-Augmented Generation

[12 RAG Pain Points and Proposed Solutions](https://towardsdatascience.com/12-rag-pain-points-and-proposed-solutions-43709939a28c)

[12 个 RAG 痛点和建议的解决方案 (中文翻译)](https://zhuanlan.zhihu.com/p/681351068)

![](Pics/rag001.webp)

Pain Point
1. **Missing Content (内容缺失)**
   1. provides a **plausible but incorrect answer** when **the actual answer is not in the knowledge base**, rather than stating it doesn’t know
   2. users receive misleading information, leading to frustration
   3. **SOLUTION**
      1. **Clean your data** - Garbage in, garbage out, such as containing conflicting information. Clean data is the prerequisite for any RAG pipeline
      2. **Better prompting** - By instructing the system with prompts : "Tell me you don’t know if you are not sure of the answer", encourage the model to acknowledge its limitations and communicate uncertainty
2. **Missed the Top Ranked Documents (错过排名靠前的文档)**
   1. essential documents may not appear in the top results returned by the system’s retrieval component
   2. correct answer is overlooked, causing the system to fail to deliver accurate responses
   3. question is in the document but did not rank highly enough to be returned to the user
   4. **SOLUTION**
      1. **Hyperparameter tuning** for **chunk_size**(分块大小) and **similarity_top_k**(相似度最高的K个) - manage the efficiency and effectiveness of the data retrieval process, impact the **trade-off** between **computational efficiency** and the **quality of retrieved information**
      2. **Reranking retrieval results** - evaluate and enhance retriever performance using various **embeddings and rerankers** & finetune **a custom reranker**
3. **Not in Context - Consolidation Strategy Limitations (不在上下文中-整合策略的局限性)**
   1. Documents with the answer were retrieved from the database but **did not make it into the context for generating an answer**, a consolidation process takes place to retrieve the answer
   2. **SOLUTION**
      1. Tweak retrieval strategies
      2. Finetune embeddings
4. **Not Extracted (未提取)**
   1. system struggles to extract the correct answer from the provided context, especially when overloaded with information
   2. Key details are missed, compromising the quality of responses
   3. occurs when there is too much noise or contradicting information in the context
   4. **SOLUTION**
      1. Clean your data
      2. Prompt Compression
      3. LongContextReorder - the best performance typically arises when crucial data is positioned at the start or conclusion of the input context
5. **Wrong Format (格式错误)**
   1. an instruction to extract information in a specific format(table & list) is overlooked 
   2. **SOLUTION**
      1. Better prompting - Clarify the instructions、Simplify the request and use keywords、Give examples、Iterative prompting and asking follow-up questions
      2. Output parsing - to provide “parsing” for LLM outputs、provide formatting instructions
      3. Pydantic programs - serves as a versatile framework that converts an input string into a structured Pydantic object
      4. OpenAI JSON mode - enable JSON mode for the response
6. **Incorrect Specificity (特征不明显)**
   1. responses may lack the necessary detail or specificity, often requiring follow-up queries for clarification
   2. answers may be too vague or general, failing to meet the user’s needs
   3. **SOLUTION**
      1. Advanced retrieval strategies
         1. small-to-big retrieval - 先从较小、较精确的数据集开始搜索，如果在这些数据集中找不到足够的信息，就逐渐扩展到更大的数据集
         2. sentence window retrieval - 基于文本窗口的检索策略，特别适用于需要从大量文本中提取具体句子或短文本片段的场景，检索系统会根据查询的上下文或关键词，确定相关句子周围的“窗口”范围，并从这些窗口中提取信息
         3. recursive retrieval - 迭代的检索方法，它在初次检索后使用检索到的信息来精细化和改进后续的搜索查询
7. **Incomplete (不完整)**
   1. partial responses aren’t wrong; however, don’t provide all the details, despite the information being present and accessible within the context
   2. **SOLUTION**
      1. Query transformations - add a query understanding layer before actually querying the vector store
8. **Data Ingestion Scalability (数据摄取可扩展性)**
   1. the system struggles to efficiently manage and process large volumes of data
   2. lead to performance bottlenecks and potential system failure
   3. cause prolonged ingestion time, system overload, data quality issues, and limited availability
   4. **SOLUTION**
      1. Parallelizing ingestion pipeline - ingestion pipeline parallel processing
9. **Structured Data QA (结构化数据 QA)**
   1. accurately interpreting user queries to retrieve relevant structured data
   2. especially with complex or ambiguous queries, inflexible text-to-SQL
   3. **SOLUTION** of LlamaIndex
      1. Chain-of-table Pack
      2. Mix-Self-Consistency Pack
10. **Data Extraction from Complex PDFs (复杂 PDF 中的数据提取)**
    1. extract data from complex PDF documents(embedded tables)
    2. **SOLUTION**
       1. Embedded table retrieval - use [Unstructured.io](Unstructured.io) to parse out the embedded tables from an HTML document(use **pdf2htmlEX** to convert the PDF to HTML), build a node graph, use recursive retrieval to index/retrieve tables based on the user question
11. **Fallback Model(s) (后备模型)**
    1. rate limit errors with OpenAI’s models
    2. a fallback model(s) as the backup in case your **primary model malfunctions**
    3. **SOLUTION**
       1. Neutrino router - a collection of LLMs to which you can route queries
       2. OpenRouter - a unified API to access any LLM, finds the lowest price for any model and offers fallbacks in case the primary host is down
12. **LLM Security (LLM安全性)**
    1. combat **prompt injection**, handle **insecure outputs**, prevent **sensitive information disclosure**
    2. **SOLUTION**
       1. Guard - classify content for LLMs by examining both the inputs (through **prompt classification**) and the outputs (via **response classification**), produce text outcomes that determine whether a specific prompt or response is considered safe or unsafe

