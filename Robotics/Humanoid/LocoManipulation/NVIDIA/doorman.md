# DoorMan : Opening the Sim-to-Real Door for Humanoid Pixel-to-Action Policy Transfer

[Project](https://doorman-humanoid.github.io/) | [arXiv 2512.01061](https://arxiv.org/abs/2512.01061) | NVIDIA GEAR · 2025-12

作者:Haoru Xue, Tairan He, Jim Fan, Yuke Zhu 等（NVIDIA / UC Berkeley / CMU / CUHK）

同源同法:与 [ASAP](../../Locomotion) / H2O / OmniH2O 一脉,teacher-student sim-to-real 人形全身控制（WBC）。



## 0. TL;DR（一句话）

在 **纯仿真** 里训练一个 **只用 RGB** 的人形全身策略去开各种门（articulated loco-manipulation），零样本迁移到真机,成功率 83% ≈ 专家遥操(80%)、优于新手(60%),而且**比人快 23~32%**。号称第一个纯 RGB 感知做多样化 articulated loco-manipulation 的人形 sim-to-real policy。



## 1. 为什么"开门"是个硬骨头?

开篇金句:
> *humanoid kung fu and backflips are solved before they can open doors using only RGB vision.*
> （人形都能打拳翻跟头了,却还开不好一扇门 —— 因为后者是**接触密集 + 纯视觉**）

开门把多个难点**紧耦合**在一起,是 loco-manipulation 的极限压力测试:
1. 从**移动的第一视角相机**里找到把手的抓取位置（感知）
2. 旋转**弹簧回位**的门把手（接触力控制）
3. 跟随门板的**圆弧运动**（articulated 约束）
4. 在铰链反作用力下**保持全身平衡**（WBC）

> perception ↔ action ↔ contact ↔ whole-body balance,四者环环相扣,缺一不可。

**旧方案的局限**:靠深度相机 / 物体中心特征 / 硬编码运动基元(轮式底盘);或简化接触力学、依赖精确物体定位;DARPA 时代靠脚本 + 人工干预;近期遥操 pipeline 又很脆(brittle)。都不 scalable。



## 2. 两大挑战

| # | 挑战 | 对应解法 |
|---|------|----------|
| (i) | **算法**要简单、可扩展、对 partial observability 鲁棒,还要协调感知 + WBC | Teacher-Student-**Bootstrap** 三阶段(§3) |
| (ii) | **视觉 sim-to-real gap** 覆盖巨大的外观 + 物理变化空间,需要广而杂的数据而非精调场景 | IsaacLab 大规模程序化随机化(§4) |

> 关键理念:**不复刻**任何真实场景,而是把策略暴露在一个足够宽的 variability envelope 里 —— 所有真机评测场景训练时都没见过(unseen)。



## 3. 核心方法:Teacher-Student-Bootstrap 三阶段

全部在 IsaacLab 里交互式完成(Figure 2)。底座是一个**预训练好的 WBC**(Ben et al. 2025),省去从零学腿部 locomotion 的负担;策略以 **50 Hz** 输出 Unitree G1 的目标关节角(身体 + 灵巧手,动作维度很高)。

| 阶段 | 名称 | 算法 | 观测 | 一句话作用 |
|------|------|------|------|-----------|
| **Phase 1** | Teacher RL | **PPO** | **特权观测** (door pose / articulation…) | 用上帝视角学会开门 |
| **Phase 2** | Student Distillation | **DAgger** | **RGB 视觉** + 本体感知 | 把 teacher 蒸馏成纯 RGB 学生 |
| **Phase 3** | Student Bootstrapping | **GRPO** | RGB + 二值成功信号 | 学生自我提升,补 partial-obs 的坑 |

**每个阶段在化解一个矛盾:**
- ① 直接拿 RGB 学开门信号太稀疏 → **Phase 1** 先给上帝视角学「会开门」
- ② 上帝视角真机上没有 → **Phase 2** DAgger 蒸馏成只看 RGB 学「用眼睛开门」
- ③ 蒸馏有天花板(学生被自己身体挡住,teacher 从没这问题) → **Phase 3** 让学生自己试错学「看不全也能开门」

> 一句话:**Phase 1 学「会开门」,Phase 2 学「用眼睛开门」,Phase 3 学「在看不全的情况下也能开门」。**

### Teacher(特权观测,PPO)
特权信息 `o_T` 在真机上拿不到,只在仿真里有:
- robot-root → door 的变换 `ξ_RD`
- 左/右手 → 门把手的变换 `ξ_LD, ξ_RD`
- 18 个手部 body 的接触力旋量 `τ_H ∈ ℝ^{18×6}`
- root 线速度 `v_R ∈ ℝ³`

> 动机:**故意不用**硬编码估计器,把这些量全丢给特权 teacher,让最终的纯 RGB 学生自己从像素里长出来 → 泛化最大化。

### Student(RGB,DAgger 蒸馏)
- 非特权本体感知:关节角 `q`、关节速度 `q̇`、root 角速度 `ω̇`
- 网络:RGB → **视觉编码器(ResNet)** → latent ⊕ 本体特征 → **2 层 LSTM(512)** → **3 层 MLP(512/256/128)** → 目标关节角
- 视觉编码器与策略**联合微调**
- 用 **DAgger** 而非 BC:监督发生在**学生自己的输入分布**上,而不是只覆盖 teacher 分布

#### 代码实查:ResNet finetune / auxiliary loss

实查本地开源仓库 `/home/lzy/Projects/motion_rl/tmp/GR00T-VisualSim2Real`:

- DoorMan student config 指向 `type: ResNet`, `resnet_type: resnet18`, `pretrained: true`, `trainable: true` → **ImageNet 预训练 ResNet18,不冻结,端到端训练**。
- ResNet builder 用 `torchvision.models.resnet18(pretrained=pretrained)`,去掉 `avgpool/fc`,接 `AdaptiveAvgPool2d + Flatten + Linear` 投到 `vision_feature_dim=128`。
- student loss 主项是 **DAgger BC loss**:`policy_results["action_mean"]` 对 teacher `gt_actions` 做 L2/L1(默认 L2),`dagger_bc_loss_coef=1.0`。
- 代码里确实有一个 **object-position prediction auxiliary head**:`obj_pred_mlp` 预测 3D object position,trainer 会把 `obj_pred_loss` 加到总 loss;但 DoorMan student yaml 里 `obj_pred_loss_coef: 0.0` → **公开默认 recipe 中这个 auxiliary loss 权重为 0,不参与优化**。
- ⚠️ 证据边界:这只能说明**公开 repo / 默认 config 没启用** object prediction auxiliary loss,不能证明作者做过消融并发现它没用;也不能排除内部训练/其他实验曾开过。若要严格说,应表述为“released config disables it”,而不是“auxiliary loss is useless/unused in all experiments”。

> 结论:公开代码对应的 ResNet finetune 信号主要是 **Phase 2 的 teacher-action imitation loss**,不是 DINO-style 自监督/contrastive/seg/depth auxiliary;Phase 3 论文说再用 GRPO 任务回报微调,但当前 release 里未搜到 `GRPO` 命名实现。

### 关键辨析:DAgger 是 BC 还是 RL?

**都不是 —— DAgger 是"交互式模仿学习",本质仍是监督,但比纯 BC 强。** RL 只在 Phase 3 GRPO 才出现。

| 方法 | 数据来自谁的状态分布 | 监督信号 | reward |
|------|------|------|:---:|
| **BC** | teacher 走出来的状态 | 回归到 teacher 动作 | ❌ |
| **DAgger** | **student 自己**走出来的状态 | 回归到 teacher 动作(teacher 在这些状态打标) | ❌ |
| **GRPO** | student 自己 | **奖励**(二值成功 + 正则) | ✅ |

- BC 的病:数据全是 teacher 轨迹,部署时 student 一犯错就漂到没见过的状态 → 误差**滚雪球**(compounding error)。
- DAgger 的修法:让 student 自己 rollout,收集它**实际会遇到的状态**,再让 teacher 打标 → 监督发生在 **student 自己的输入分布**上。**但目标始终是"抄 teacher",没有 reward,不是 RL。**

### 为什么光蒸馏不够,还要 GRPO?

模仿有个**部分可观测**造成的天花板:teacher 全知,某些动作之所以最优是因为它"看得见"隐藏信息;而 student 只有晃动的第一视角相机,把手会被自己手挡住 / 晃出画面。

> 正确解法不是"把 teacher 抄得更像",而是做一件 **teacher 从不需要做的事** —— 主动挪身子调姿态,让把手留在画面里(active perception)。模仿**发明不出**这种行为。

证据(§3.3):teacher 80-90%,纯蒸馏 student 卡在 **50-70%** = **non-recoverable observability gap**;GRPO 后冲到 **80.8-85.8%**,曲线贴着 teacher 上界见顶。

### 纯 RGB 的 sim2real gap 分三层应对

| gap 类型 | 应对设计 | 在哪一步 |
|---------|---------|---------|
| **外观 gap** | 大规模**视觉随机化**:全表面随机 PBR 材质 + **5233 张 dome-light** + RTX 实时渲染 + motion blur/auto white balance + 相机内外参轻抖动;photorealistic 高保真渲染(Table 1 证明 > 老式纯色 DR) | §2.4 + Phase 2 蒸馏 |
| **动力学 gap** | **物理随机化**:门型/尺寸、铰链阻尼、闩锁 latch、把手阻力矩 | §2.4 |
| **可观测性 gap**(RGB 独有) | **GRPO** 学 active perception,把关键区域盯在画面里 | Phase 3 |
| 表征适配 | 视觉编码器(ResNet)与策略**联合微调**,不冻结 | Phase 2 |

> 一句话:**DAgger 把"会开门"搬到相机上,GRPO 补上"纯视觉可观测性"的坑 —— 解决的是不同问题,缺一不可。**

### 为什么 Phase 3 用 GRPO 而非 PPO?

先记住:**GRPO = "PPO 去掉 critic"**。论文原话 *"an actor-only variant of PPO that omits the value function and instead estimates baselines from grouped trajectory scores"*。两者 **clipped surrogate 目标(式 5)完全相同**,只差优势 `Â` 怎么算:

| | 优势 Â 来源 | 需要 critic |
|---|---|:---:|
| **PPO** | 学 `V(s)` + GAE | ✅ |
| **GRPO** | 同状态采 G 条 rollout,组内归一化 `Â_i=(R_i−mean R)/std R` | ❌(经验均值当 baseline) |

**Phase 3 不想要 critic 的三个理由(都踩在它的处境上):**
1. **Critic 死于部分可观测** —— student 只有部分 RGB,学 `V(o)` 本就有偏,PPO 还靠 `V(s')` 自举传播错误;而 Phase 3 存在的理由就是补可观测性坑,再塞个被同样问题毒害的 critic 是自找麻烦。GRPO 用组内蒙特卡洛均值当 baseline,不碰 value 自举 → 免疫。
2. **稀疏二值奖励 critic 没信号可学** —— 成功前几乎无监督,critic 极难拟合;GRPO 直接比"这次 vs 这批平均成功率"。
3. **轻量微调,不想再养第二个重网络** —— actor 已背 ResNet+LSTM,critic 为估准 V 又得处理 RGB;GRPO 省掉整个 critic,是 drop-in 的 "lightweight stable refinement"。

**那 Phase 1 为什么又用 PPO?条件正好反过来:**

| | Phase 1 Teacher | Phase 3 Student |
|---|---|---|
| 观测 | 特权全状态 | 部分 RGB |
| 奖励 | shaped 密集(Appendix A) | 稀疏二值成功 |
| value function | 近 Markov 全可观 → 好学准 | 部分可观 → 难学有偏 |
| 起点 | 从零学 | 已有非零成功率,只需精修 |
| → | **PPO**(critic 是助力) | **GRPO**(critic 是累赘) |

> 一句话:**全状态+密集奖励 → PPO;半盲+稀疏奖励+只需微调 → GRPO。** 算法选择被每阶段的"可观测性 + 奖励密度"逼出来。代价是 GRPO 每组采 G 条 rollout,但并行可 reset 的仿真里采样近乎免费。

### 追问:能不用 GRPO 吗?改造成本 & 效率(⚠️ 多为通用 RL 推理,论文无受控对比)

**能继续用 PPO** —— 经典解法 **asymmetric actor-critic**:仿真里 critic 吃**全状态特权信息**、actor 只吃 RGB,critic 训练时用完即弃,直接绕过"critic 死于部分可观测"。所以 GRPO 是**工程简洁 + 稀疏二值奖励**上的务实选择,非"PPO 做不到"。(但稀疏二值奖励下即便非对称 critic 也难估准逐步 value,GRPO 的 MC 组回报更干脆 —— 这是它在此 regime 的真实边际优势。)

**改造很简单,本质是减代码:**
```
GRPO = PPO − value网络 − value loss − GAE
           + 按相同初始状态采 G 条 rollout + 组内归一化 Â=(R−mean)/std
           (clipped loss 原封不动)
```
唯一 infra 要求:能按相同初始状态成组采样(可 reset 的并行仿真里 trivial);且 Phase 1 已有 PPO 实现可复用。代价:轨迹级标量优势广播到每步,丢了 GAE 的细粒度时序 credit assignment。

**效率四维拆解(GRPO 不是普遍更快):**

| 维度 | 谁赢 | 原因 |
|------|------|------|
| 单次更新 compute/显存 | ✅ GRPO | 没 critic(尤其省掉吃 RGB 的重 critic) |
| 样本效率(env steps) | ⚠️ 常 PPO 赢 | critic 给低方差逐步 baseline;GRPO MC 组基线高方差且 ×G 采样 |
| wall-clock | 看瓶颈 | 采样近免费时瓶颈在更新侧 → GRPO 更轻更快 |
| 稳定性/调参 | ✅ GRPO | 少 value loss 系数、GAE λ、A-C 学习率平衡等超参 |

> 关键看瓶颈:DoorMan 是**海量并行 + 采样近免费**,瓶颈在更新侧 → GRPO 占优且 ×G 被并行摊平;换真机/慢仿真(采样贵),×G 会疼、PPO 样本效率更重要。**GRPO 的优势是 regime-dependent,不是普适。**

> 🔜 待深入:§3.1 staged-reset 探索(Phase 1 的关键 trick)



## 4. 大规模仿真随机化(RGB sim2real 的看家本领)

### 哲学:撑宽分布,而非复刻场景
减小 sim2real gap 两条路:**A 数字孪生**(精确复刻真实场景,脆、不 scalable)vs **B 域随机化**(把训练分布撑宽,让真实世界只是分布里又一个采样)。DoorMan 走 **B + photorealism** —— 把宽分布的中心压在"真实感图像"附近。论文强调:*所有真机评测的门训练时一扇没见过(unseen)*。

> 机制:随机化把纹理/颜色/光照/相机抖动这些**任务无关 nuisance** 全打乱,逼视觉编码器学**任务因果结构**(把手/门缘/铰链),不能依赖表观 → 真实纹理光照只是新采样,编码器直接忽略。

### RGB 侧四个随机化旋钮(§2.4)

| 旋钮 | 做法 | 对付的真实变化 |
|------|------|------|
| ① 材质/纹理 | 全表面随机 **PBR 材质** | 门板/墙面颜色、花纹、反光 |
| ② 环境光照 | **5233 张 dome-light**(HDRI) | 不同地点/时段光照色温 |
| ③ 渲染器+后处理 | **RTX 实时(performance)** + **motion blur** + **auto white balance** | 真相机运动模糊、白平衡等 artifact |
| ④ 相机内外参 | 对齐后**轻微随机** | 相机装腿式机器人上,落地接触切换 → 视角剧烈抖动 |

- **④ 是本文特色**:人形第一视角是移动+落地冲击,视角本身剧烈晃,需专门随机化相机位姿 + motion blur。
- ①-④ 是**渲染层**随机化(物理正确 PBR + 真实光照);**注意还叠加了一层 2D 像素级增强**(见下"渲染实现细节 → 图像加噪"),两层并用,非二选一。
- ③ 用 performance 模式是工程折中:几千环境并行采样,渲染必须快。

### 渲染实现细节(⚠️ 论文仅一段带过,以下基于 Omniverse/IsaacLab 渲染栈通识)

- **Motion blur**:RTX 后处理,由仿真每帧的**真实运动向量**(相机+物体速度)驱动,沿 motion vector 在快门时间内涂抹。相机在弹跳机器人上 → 渲染出的模糊 = 真机第一视角运动模糊;附带阻止编码器依赖锐利纹理边缘。
- **Auto white balance**:相机 ISP 后处理。核心洞察:**真相机输出的是 AWB+tonemap 后的图,不是 raw radiance**。5233 张 dome light 各有色偏,开 AWB 让 sim 图经历和真相机一样的色彩归一化 → sim 颜色分布 ≈ 真相机输出。**match 的是传感器,不只是场景。** ①② 都是 Omniverse 内置后处理开关,贡献是"performance 模式下扛住并行 RL 还能开着"。
- **Dome light 为何是"5233 张贴图"而非随机光源**:dome light = **image-based lighting**,用球面 HDRI 把场景包起来,**图上每像素都是光源**,一次性带来真实的方向性/软阴影/彩色环境光/**镜面反射**。"5233" = HDRI 环境图库大小,每个并行环境随机抽一张。**金属把手是高镜面反射**,反射的是环境 → IBL 给出可信反射,3 个点光会假;策略要从 RGB 找把手,故这尤其重要(呼应 Table 1 光照是头号旋钮)。参数化光源随机化=较弱的 baseline;IBL 本质也是光照随机化,只是在图像层做。
- **PBR 材质怎么"加"**:PBR = 一组物理参数/贴图(albedo/roughness/metallic/normal…)。IsaacLab 自带材质库,建环境时给**每个表面随机绑一个 MDL 材质**(USD material binding)。Table 1 档位:`+10%/100% 纹理`=随机化覆盖比例;`纯色随机`=只随机均匀 albedo(退化 PBR,无纹理细节);`无随机化`=default gray(Figure 4 最后那张没材质的门)。物理基 → 材质与 dome-light IBL 物理正确叠加(渲染层);此外还在渲染后叠加 2D 像素级增强,见下。
- **图像加噪?论文没提,但代码里有(实查开源仓库确认)** —— 视觉随机化其实是**两层**:
  - **① 渲染层(物理正确,论文提了)**:PBR 材质、5233 HDRI、motion blur、AWB、相机内外参。
  - **② 2D 像素层(渲染后处理,只在代码里 `wsdpt_student.yaml`,`image_augmentation.enabled: True`)**:逐帧按概率对 RGB 图施加 torchvision `v2.functional` 增强:

  | 增强 | 概率 | 范围 |
  |------|:---:|------|
  | **gaussian_noise** | 0.25 | σ ∈ [0.0, 0.15] |
  | gaussian_blur | 0.25 | kernel [3,5], σ [0.1,1.5] |
  | brightness | 0.25 | [0.7, 2.0] |
  | contrast | 0.25 | [0.5, 1.5] |
  | hue | 0.5 | [-0.1, 0.1] |
  | saturation | 0.25 | [0.5, 2.0] |

  - ⚠️ **纠正**:先前笔记曾推断"他们用渲染层随机化替代像素层加噪" —— **错**,实际是**两层都上**,论文只写了①,②藏在 student config 里。
  - **teacher config(`wsdpt.yaml`)里 image_aug `enabled: False`** → 图像增强是 **student 专属**(teacher 吃特权状态无 RGB),印证 ② 是给纯 RGB 学生补 sim2real 的。
  - 输入分辨率 **108×192×3**(student 实验配置 `camera_resolutions:[108,192]`;代码注释里的 "60×60" 是过时值,勿信)。obs 同时喂 `rgb_image` + `rgb_image_delayed` 建模相机/推理延迟。另配了 depth_augmentation 但门策略纯 RGB,多半未启用。
- ⚠️ 论文未给具体参数(快门时长/AWB 算法/材质库大小/绑定策略),多在 Appendix/代码,本 9 页 PDF 无。

### 图像增强的实际实现(代码级)

> 源码:[`_image_augmentation` @ legged_robot_base.py:1990](https://github.com/NVlabs/GR00T-VisualSim2Real/blob/main/gr00t/rl/envs/legged_base_task/legged_robot_base.py#L1990) · 调用点 [`_get_obs_rgb_image` :1879](https://github.com/NVlabs/GR00T-VisualSim2Real/blob/main/gr00t/rl/envs/legged_base_task/legged_robot_base.py#L1879) · 参数 [`domain_rand/wsdpt_student.yaml:110`](https://github.com/NVlabs/GR00T-VisualSim2Real/blob/main/gr00t/rl/config/domain_rand/wsdpt_student.yaml#L110)

**流程(逐帧):**
```
rgb(来自 sim,已按 ImageNet 归一化,NHWC)
 ├─ 反归一化:rgb = rgb*std + mean        # 回到 [0,1] 像素空间
 ├─ permute NHWC → NCHW                   # torchvision 要 (N,C,H,W)
 ├─[掷骰 p] brightness     b∈[0.7,2.0]    随机采样
 ├─[掷骰 p] saturation     s∈[0.5,2.0]
 ├─[掷骰 p] hue            h∈[-0.1,0.1]
 ├─[掷骰 p] contrast       c∈[0.5,1.5]
 ├─[掷骰 p] gaussian_noise σ∈[0,0.15]     随机采样,加性,clip[0,1]
 ├─[掷骰 p] gaussian_blur  固定 3×5 核, σ=(0.1,1.5)  ← 不采样!
 ├─ permute NCHW → NHWC
 └─ 重归一化:rgb = (rgb-mean)/std         # 再喂 ResNet
```

**每个 op 数学上做了啥(torchvision `v2.functional`,均在 [0,1] RGB 上):**

| op | 公式(b/c/s/h/σ 为采样系数) | 直觉 |
|----|------|------|
| brightness | `clip(img·b, 0,1)`,b∈[0.7,2] | 整体调暗/调亮(向黑混合) |
| contrast | `clip(c·img+(1−c)·mean_luma, 0,1)`,c∈[0.5,1.5] | 向"全图灰度均值"混合,c<1 变平、>1 更硬 |
| saturation | `clip(s·img+(1−s)·gray(img), 0,1)`,s∈[0.5,2] | 向逐像素灰度混合,s=0 全灰、>1 更艳 |
| hue | RGB→HSV,H+=h(圈比例≈±36°),转回 | 平移色相(红↔橙…) |
| gaussian_noise | `clip(img+N(0,σ²), 0,1)`,σ∈[0,0.15] | 传感器/散粒噪声 |
| gaussian_blur | 固定 3×5 高斯核卷积,σ=(0.1纵,1.5横) | 失焦/残余模糊,横向更糊 |

**顺序有影响吗?** 数学上都不可交换(contrast 依赖当前图 mean_luma;hue/saturation 在不同色彩空间),但对"扩分布求不变性"的 DR 目的**问题不大** —— 不同顺序只把增强分布挪一挪,且每个 op 独立以 0.25~0.5 概率触发,多数帧只落一两个。唯一值得注意的耦合:**代码里 noise 在 blur 之前** → blur 低通会平滑掉刚加的高频噪声,使实际噪声被削弱、变空间相关(若 blur→noise 则噪声完整保留)。物理性注脚:真实相机是"传感器先出噪声、ISP 再做色彩",正确顺序应把 noise 放最前;他们是色彩→noise→blur,不符真实 ISP,但 DR 无所谓。

**3 个读代码才知道的 nuance:**
1. **归一化用 ImageNet 统计**(mean[0.485,0.456,0.406]/std[0.229,0.224,0.225])→ 坐实编码器是 **ImageNet 预训练 ResNet**。
2. **增强逐步 batch 共享,非 per-env** —— gate 与采样系数都是单标量,某一步几千 env 用同一个亮度/噪声/模糊;多样性靠时间维度堆,比 per-env 弱一档。
3. **gaussian_blur 没随机采样** —— 别的 aug 用 `torch_rand_float` 采系数,唯独 blur 把 config 的 range 端点当实参 `kernel=(3,5)/sigma=(0.1,1.5)` 直接传 functional → 触发时永远固定强度、横向偏强。疑似误用 API 的小 bug。

### 源码索引(NVlabs/GR00T-VisualSim2Real @ `main`)

| 内容 | 文件:行 |
|------|---------|
| 图像增强 `_image_augmentation` | `gr00t/rl/envs/legged_base_task/legged_robot_base.py:1990` |
| RGB 取图 + 调用增强 `_get_obs_rgb_image` | 同上 `:1879`(noise `:2065` / blur `:2082`) |
| 图像增强参数(student 全开) | `gr00t/rl/config/domain_rand/wsdpt_student.yaml:110` |
| 图像增强(teacher 全关) | `gr00t/rl/config/domain_rand/wsdpt.yaml:110` |
| 相机分辨率 [108,192] + rgb_delay | `gr00t/rl/config/exp/loco_manip/wsdpt_student_for_teacher_v8q8.002_resnet_rgb_delay.yaml:28` |
| ImageNet mean/std + 默认分辨率 | `gr00t/rl/config/simulator/isaacsim.yaml:47-49` |
| 观测噪声开关 / RFI 力矩噪声 | `gr00t/rl/simulator/isaacsim/isaaclab_cfg.py:336` / `:291` |
| 观测噪声 curriculum | `gr00t/rl/envs/base_task/loco_manip_base.py:955` |
| 域随机化分布(uniform/gaussian) | `gr00t/rl/simulator/isaacsim/events.py` |

### 资产/代码发布状态(实查项目页 + GitHub)

**渲染能力 vs 资产要分开:**
- **渲染能力**(motion blur / AWB / dome light / PBR / RTX)= **Omniverse/IsaacSim/IsaacLab 自带**,非他们发明;IsaacLab 提供域随机化框架去调用。
- **门程序化生成管线 + 随机化配置** = **他们自己的**(论文 "we design a procedural generation pipeline in IsaacLab")。
- **PBR 材质** 多半用 Omniverse 内置 **vMaterials** 库;**5233 张 dome-light HDRI** 很可能是他们自行聚合(来源未披露)。

**开源情况** —— 代码库 [NVlabs/GR00T-VisualSim2Real](https://github.com/NVlabs/GR00T-VisualSim2Real):
- ✅ **放了**:teacher PPO + DAgger + eval + ONNX 导出、IsaacLab 环境/任务定义、奖励函数、**域随机化参数配置**、G1 机器人配置(GRPO 或经 TRL 库,README 未明说)。
- ❌ **没放**:**dome light HDRI / PBR 材质 / 门网格等实际视觉资产**;只给引用它们的配置。需自装 `isaacsim==5.1.0.0` + IsaacLab,材质靠 vMaterials,HDRI 自备,精确渲染参数需邮件问作者。
- 定性:**partial research release** —— 给算法+随机化配方,不给整套视觉资产,无法开箱复现那 5233 张光照。

### Table 1 消融:哪个旋钮真管用(§3.2,120 扇 unseen 门,成功率 % = Push Lever/Pull Lever/Push Bar)

| # | 纹理随机化 | DL | Push Lever | Pull Lever | Push Bar |
|---|---|:---:|---|---|---|
| 1 | 无随机化 | ✗ | 10.8 | 5.0 | 20.0 |
| 2 | 纯色随机 | ✓ | 67.5 | 65.8 | 70.0 |
| 3 | +10% 纹理 | ✗ | 58.3 | 50.8 | 76.7 |
| 4 | +10% 纹理 | ✓ | 79.2 | 77.5 | 77.5 |
| 5 | +100% 纹理 | ✗ | 73.3 | 55.8 | 76.7 |
| **6** | **+100% 纹理** | **✓** | **85.8** | **80.8** | **85.0** |

1. **光照(DL)是头号旋钮**:5→6 Pull Lever 55.8→80.8(+25),3→4 是 50.8→77.5(+27);去 DL 整体掉 15-30%,最难的 Pull Lever 掉最多。
2. **纹理量很快饱和**:10%+DL(4) vs 100%+DL(6) 只差 4-8% → 纹理多样性不用拉满。
3. **完全不随机化=灾难**:row 1 仅 5-20%。
4. **photorealism > 老式纯色 DR**:纯色+DL(2,=Tobin 2017/OpenAI 那代)66-70% vs 全 photoreal(6)85% → 这 **15-18% 纯是高保真 PBR 渲染带来的**,是本文相对老 DR 的核心增量。

> RGB 配方一句话:**PBR 材质 + 海量真实光照 + 真相机 artifact + 抖动相机位姿;光照最关键、纹理易饱和、photorealistic 渲染本身值 ~15% 成功率。**



## 5. 实验结果（🔜 待聊）

- 超越人类遥操:83% vs 80%(专家) vs 60%(新手),快 23.8~31.7%
- 视觉随机化消融(Table 1)、GRPO 微调曲线(Fig 6a) —— 细节下轮补。



## TODO / 疑问

- [ ] staged-reset 的 staged reset law(α 权重 + occupancy measure 重加权)具体怎么推
- [ ] GRPO 为什么用 group-relative advantage 就能省掉 value function
- [x] ~~动作维度论文写 "33"~~ → GitHub 仓库确认 **G1 是 43-DOF**(29 身体 + 14 手),正文 "33" 是笔误
- [ ] 相机装在腿式机器人上"constant contact switching",内外参怎么对齐
