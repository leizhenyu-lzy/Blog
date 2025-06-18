# 量化

[模型量化 - B站合集](https://space.bilibili.com/18235884/lists/2887562?type=season)

# 量化基础

Llama 13B = 13,000,000,000
1. FP32 : 52GB
2. FP16 : 26GB
3. Int8 : 13GB
4. Int4 : 6.5GB



优势
1. 减少模型存储大小
2. 减小推理时占用的显存大小，提升模型推理速度
   1. 计算过程中，TensorCore 和 显存之间 频繁的数据 交换，减少数据交换大小，从而提升模型推理速度
   2. 显存带宽固定，制约推理速度

TFLOPS(Tera Floating-point Operations Per Second)

TOPS(Tera Operations Per Second)

对称量化

非对称量化


极大值量化

零点量化


