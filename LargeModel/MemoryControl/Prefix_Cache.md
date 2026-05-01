# Prefix Cache

实际业务中，很多不同的用户请求往往拥有完全相同的开头(Prefix)

真实世界的 Prompt 中包含了海量的冗余重复内容
1. System Prompt
2. RAG 的 Context



实现方式
1. 基数树(Radix Tree / 前缀树) : 系统会在内存里动态维护一棵树，每一个节点代表一段 Token 生成的 KV Cache 数据块
2. 哈希匹配 : 当新请求进来时，系统会按顺序对它的 Prompt 进行 Hash 计算，去树里寻找 匹配的 最长公共前缀路径
3. 指针共享 : PagedAttention 把显存切成了固定大小的 Block，把对应 Block 的显存指针给新请求用即可

好处
1. 命中缓存后，Prefill 阶段瞬间变成 0 秒，首字响应速度快
   1. Prefill : 大模型都要先阅读输入文本
   2. 如果不复用，会导致 **首字延迟(TTFT, Time To First Token)** 很高
2. 用户共享同一个 System Prompt，在显存里只会占用 1 份 KV Cache




vLLM 实现 Prefix Cache
1. **==写时复制==(Copy-on-Write)** + **==引用计数==(Reference Counting)**
2. 公共前缀计算 + 引用计数
3. 发生分支时(追加新 Token)
   1. **铁律** : 只有 引用计数 = 1 的 Block 才能被直接修改/写入
   2. 如果老 Block 已满 : 分支各自申请新 Block 写入，老 Block 引用计数不变
   3. 如果老 Block 没满 : **触发 写时复制(CoW)**，当前分支申请新 Block，复制旧数据，写入新数据，随后该分支与老 Block 解绑，老 Block 引用计数减 1
   4. 彻底分道扬镳 : 一旦分支有了自己独立的 Block(无论是满了追加的，还是 CoW 复制的)，后续的生成 就在 各自独立的 Block 中进行，互不干涉
4. <img src="Pics/prefix001.png" width=600>

