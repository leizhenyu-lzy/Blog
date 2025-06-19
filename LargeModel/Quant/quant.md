# 量化

[模型量化 - B站合集](https://space.bilibili.com/18235884/lists/2887562?type=season)

# 量化基础

Llama 13B = 13,000,000,000
1. FP32 : 52GB
2. FP16 : 26GB
3. Int8 : 13GB
4. Int4 : 6.5GB

把 Float类型(FP32，FP16) 的 模型参数 和 激活值，用 整数(Int8，Int4) 代替的同时，尽可能减少量化后模型推理的误差

优势
1. 减少模型存储大小
2. 减小推理时占用的显存大小，提升模型推理速度
   1. 计算过程中，TensorCore 和 显存之间 频繁的数据 交换，减少数据交换大小，从而提升模型推理速度
   2. 显存带宽固定，制约推理速度
      1. 虽然 浮点数运算 更复杂，但是 位宽还是 主要决定性因素

单位
1. Tera = $10^{12}$ = $2^{40}$
2. TFLOPS(Tera Floating-point Operations Per Second)
3. TOPS(Tera Operations Per Second)

量化 & 反量化
1. $x1_f -> 量  化 -> x1_q$
2. $x1_q -> 反量化 -> x2_f$
3. 需要 让 $x1_f$ & $x2_f$ 尽可能接近
4. 因为最终还是需要使用 浮点数值


对称量化
1. 为了保持精度，需要 尽可能占满 整数空间


非对称量化


极大值量化

零点量化


