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
   5. `compute_returns()` : distill 不需要，直接 跳过
      1. PPO : `rollout -> reward -> value -> returns/advantages -> policy/value loss -> update`
      2. Distillation : `rollout -> teacher action labels -> behavior loss -> update`
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


distill 不兼容 RND & Symmetry(`ppo.py`)



`on_policy_runner.py` & `distill.py / ppo.py`(统称为 `alg.py`)
1. runner 中的 `learn()`
   1. 先 收集 第一次 初始 obs
   2. 循环 num_learning_iterations 个 iters，每个 iteration
      1. rollout 循环 num_steps_per_env 个 steps
         1. 传入 obs，调用 `alg.act()` 得到 actions
         2. 传入 actions，给环境 调用 `env.step()` 得到 obs & rewards & dones & extras
         3. 传入 obs & rewards & dones & extras，调用 `alg.process_env_step()` 进行收尾，transition -> storage
      2. rollout 后传入 obs(最新的)，调用 `alg.compute_returns()`
   3. 调用 `alg.update()`
   4. 记录 log & 保存 model
2. alg 中的 `act()` : 记录关键信息 到 transition 中
   1. actions : actor 网络 结果 + `stochastic_output=True`
   2. values : critic 网络 结果
   3. actions_log_prob : 当前 采样出来的动作，在 旧策略分布 下的对数概率，后续用于 **重要性采样**
   4. distribution_params : 当前 actor 输出的动作分布参数 (`mean` & `std / log_std`)，不直接输出 action，而是先输出 动作分布的参数，再从分布采样 action
3. alg 中的 `compute_returns()`
   1. 在 rollout 结束后，计算 returns & advantage(GAE)，根据
      1. storage 中的 rewards & dones & values
      2. 最后一个时刻的 **value bootstrap** (最新 obs 送入 critic 网络)
   2. GAE 会根据 dones 自动截断
4. alg 中的 `update()`
   1. epoch & batch : 通过 num_learning_epochs & num_mini_batches 控制，给 **generator** (就没有 epoch / batch 的概念了)
   2. P.S. 第一个 batch 算的 actions_log_prob 和之前 transition->storage 的 old_actions_log_prob 一样，没有 `optimizer.step()` 过
