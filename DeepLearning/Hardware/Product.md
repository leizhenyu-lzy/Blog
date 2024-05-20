# 产品调研

---

## Table of Contents

- [产品调研](#产品调研)
  - [Table of Contents](#table-of-contents)
- [Nvidia](#nvidia)
- [Huawei](#huawei)



---

# Nvidia

L40S

---

# Huawei

[昇腾 Ascend ![](Pics/huawei001.svg)](https://www.hiascend.com/)

**昇腾全栈 AI 软硬件平台**

![](Pics/huawei002.png)

[昇腾软硬件全栈简介](https://zhuanlan.zhihu.com/p/571485917)

[大模型国产化适配 - 华为昇腾AI全栈软硬件平台总结](https://zhuanlan.zhihu.com/p/637918406)

昇腾芯片
1. **昇腾910** for **训练**
2. **昇腾310** for **推理**

达芬奇架构，对标 Nvidia

**Atlas系列**产品(NPU) - 基于 `昇腾910` 和 `昇腾310` 打造出来的
1. Atlas 800 (型号：9000)
   1. **训练服务器**
   2. 包含8个训练卡(Atlas 300 T - **昇腾910**)
2. Atlas 800 (型号：3000)
   1. **推理服务器**
   2. 包含8个推理卡(Atlas 300 I - **昇腾310**)
3. Atlas 900
   1. **训练集群**
   2. 128台Atlas 800(型号：9000)构成
   3. 由一批训练服务器组合而成

**异构计算架构 CANN**
1. 对标英伟达的 CUDA + CuDNN 的核心软件层
2. 引擎、编译器、执行器、算子库
   ![](Pics/huawei003.png)


**AI框架**
1. 自研框架 - MindSpore昇思
2. 第三方框架 - PyTorch、TensorFlow等

**应用使能**
1. ModelZoo - 存放模型的仓库，包括普通模型 和 昇思大模型
2. MindX SDK - 帮助用户快速开发并部署人工智能应用
3. MindX DL - 昇腾深度学习组件。提供昇腾 AI 处理器资源管理和监控、昇腾 AI 处理器优化调度、分布式训练集合通信配置生成等
4. MindX Edge - 昇腾智能边缘组件



ARM+910B

X86+910B







