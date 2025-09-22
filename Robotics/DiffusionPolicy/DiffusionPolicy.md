# Diffusion Policy

[Diffusion Policy: LeRobot Research Presentation #2 by Cheng Chi](https://www.youtube.com/watch?v=M03sZFfW-qU)

[Diffusion Policy 基于扩散模型的机器人动作生成策略 - 知乎](https://zhuanlan.zhihu.com/p/670555655)

[Diffusion Policy - Project](https://diffusion-policy.cs.columbia.edu/#paper)

[Diffusion Policy - Github](https://github.com/real-stanford/diffusion_policy)


##

Diffusion Policy 一种新型机器人行为生成方法(Robot Action Generation)

将机器人的视觉动作策略(Visuomotor Policy) 表示为 条件去噪扩散过程(Conditional Denoising Diffusion Process)


Action : sequence of 2D end-effector positions



##





Learning Paradigms
1. imitation learning
2. meta learning
3. self-supervised learning
4. reinforcement learning

End Product
1. Observation -> **Visuomotor Policy(视觉-运动策略)** -> Action

<img src="Pics/dp001.png" width=650>

Diffusion Model
1. Input  ： Text
2. Output ： Image

Diffusion Policy
1. Input  : Image
2. Output : Sequence of Actions

<img src="Pics/dp002.png" width=650>

Action Multi-Modality







