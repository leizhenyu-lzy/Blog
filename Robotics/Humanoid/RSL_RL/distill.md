# Distillation 蒸馏 (RSL_RL)


`rsl_rl/algorithms/distillation.py` : 蒸馏算法本体
1. class `Distillation`
   1. `__init__()`
      1. loss_fn_dict : mse & huber
   2. `act()` : `on_policy_runner.py` 在 `learn()` 的时候调用
      1. rollout
         1. 给 obs(`TensorDict`)，student & teacher `forward()` 的时候 会在 `get_latent()` 时候自动选择 需要的 obs 拼接
         2. student 出 动作(action)，teacher 出 监督标签(**privileged_actions**)
      2. action & privileged_actions，都放入 rollout storage 的 transition 中
   3. `process_env_step()`
      1. `on_policy_runner.py` 在 `learn()` 中 调用 `step()`，得到 obs, rewards, dones
      2. `student.update_normalization()` : 只 update student 的
         1. 仅在 启用 `obs_normalization` 后有作用，使用 `EmpiricalNormalization`，`forward()` 时会作用在输入，训练过程中还会持续更新统计量
      3. 相关内容 (reward, dones) 存入 transition，加入 storage，清空 transition
      4. teacher & student 进行 reset (for RNN hidden state)
   4. `update()` **==☆==** : 真正 学习 的地方，rollout 的 数据拿出来，反复训练 student
      1. 每个 epoch(使用 相同的 rollout 数据) 先 对 teacher & student 进行 reset(恢复 hidden state，for RNN)
      2. 通过 storage.generator 生成 batch
         1. 通过 student 得到 action
         2. 和 privileged_actions(teacher 在 rollout(`act`) 的时候 对应的 action) 进行 behavior cloning loss 计算
         3. loss 累计 若干 batch 的 loss 一起 backward，可以有 对于 grad_norm 的 clip，然后 清零 loss
         4. mean_behavior_loss 统计日志数值 不参与反向传播
      3. 清空 storage
   5. `compute_returns()` : distill 不需要
   6. `construct_algorithm()`
      1. 根据 obs(`TensorDict`) & env(`VecEnv`) & 训练配置 cfg，把整个 `Distillation` 算法对象组装出来
      2. cfg 中 会配置 obs_groups，指定 需要的 observation sets (default 是 teacher & student)
      3. `resolve_obs_groups()` : 检查配置里写的 group 是否合法
      4. initialize teacher/student policy
         1. `init` 初始化 teacher & student model 时候，传入 `cfg["obs_groups"]` & `teacher/student`
         2. `get_latent()` 中 进行 **实际拼接**



`rsl_rl/runners/distillation_runner.py` : 蒸馏训练 runner
1. class `DistillationRunner`，继承 `OnPolicyRunner`
   1. 只是规定了 alg 类型是 `Distillation`
   2. 另外 `learn()` 会先 检查是否已经 load teacher
      1. `init_at_random_ep_len` : 在开始训练前，把每个并行环境当前的 episode 长度随机初始化一下，等价于让不同 env 看起来像是已经处在 episode 的不同阶段



`rsl_rl/storage/rollout_storage.py` : 蒸馏模式下保存 privileged_actions



`rsl_rl/env/vec_env.py` : 环境接口里明确支持 student / teacher 观测组
1. PPO
   1. actor
   2. critic
2. Distill
   1. teacher (teacher 通常 是 PPO 的 actor_state_dict 加载)
   2. student






RND : Random Network Distillation，只在 PPO 里面用，distill 不用


不兼容 RND & Symmetry(`ppo.py`)


