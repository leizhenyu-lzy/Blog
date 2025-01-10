# Embodied AI - 具身智能

系统化方案 : 环境理解(CV) + 智能交互(语音) + 认知推理(LLM) + 规划执行


LLM as General Planner


将可以 调用的API 写在 Prompt 中，同时指定任务，由 LLM 具体规划代码生成



navigation

grasp - AnyGrasp



基础技术路线
1. 场景理解(成熟)
   1. 检测 & 分割
      1. vision foundation model (SAM, SAM3D, Open-Voc Detection 开放词汇目标检测)
   2. 多模态 Grounding(在具体模态中找到实体或目标) 2D -> 3D
      1. 多模态大模型 能够实现 像素级别，大模型 理解能力强，并且支持多样的 Prompt
2. 数据引导(数据量不够)
   1. 视频学习 : 引导，数据质量低，难以迁移到真机
   2. 硬件在环采集
      1. Light : 轻量级采集硬件数据(end-effector, 不是 full body)
      2. Heavy : VR 显示器 + 手套(硬件成本高)
   3. 生成式仿真 Generative Simulation
3. 动作执行
   1. 生成式模仿学习 Generative Imitation Learning
      1. Diffusion Policy
   2. Affordance 物体的不同部位可以被如何操作/交互
   3. 大模型问答 Q&A with LLM
   4. LLM Prompt Planning
   5. Language Corrections 矫正提示
4. 世界模型



Robotics & CV/NLP 区别 : 数据集

CLIP 对比学习


