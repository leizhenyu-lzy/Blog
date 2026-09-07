# Harness

**==Harness==** : 包在 Model / Agent / Tools / Prompt / Runtime / Eval 外层的 **运行与控制框架**

1. Model 是 大脑，Harness 是 身体 + 车间 + 质检
2. 目标 : 让 Agent 能 **稳定 / 可控 / 可验证** 地完成 **长任务**
3. 同义词 : Agent Scaffold / Agent Runtime / Agent Loop / 脚手架

> 词义歧义(看语境区分)
> 1. **Agent Harness** : 跑 Agent 的运行框架 (Claude Code / OpenHands / SWE-agent)
> 2. **Eval Harness** (Test Harness) : 跑评测的执行框架 (SWE-bench 官方 harness : 建镜像 → 打 patch → 跑测试 → 判分)
>
> 二者会耦合 : 评测分数 = **Model × Harness** 的联合结果，同一模型换 harness 分数可差十几个点
> $\Rightarrow$ **Harness 本身也是被评测的一部分**

---

# 概念

## 层次区分

| 概念        | 是什么                                                 |
| ----------- | ------------------------------------------------------ |
| **Model**   | 只做 next token prediction，**无状态**                 |
| **Agent**   | Model + Tools + Memory，能自主决定下一步               |
| **Harness** | 承载 Agent 的运行时 : 循环 / 上下文 / 沙箱 / 验证 / 恢复 |
| **Workflow**| 预定义步骤 的编排，流程固定，不依赖自主规划            |

## Agent Loop (最小内核)

```
LLM 输出 → 解析 Tool Call → 执行工具 → 结果回灌 Context → 再调 LLM → ... → 停止条件
```

Harness = 围绕这个 loop 补的 **所有工程**
1. 什么时候停 ?
2. Context 满了怎么办 ?
3. 工具报错怎么办 ?
4. 模型说 "做完了" 要不要信 ?

## 要解决的 3 个典型失败

1. **卡死**   : 推进停滞 / 上下文混乱 / 长时间不收敛
2. **断头**   : 做到一半停下，没有交付 / 收尾 / 状态传递
3. **假完成** : 口头宣称完成，实际没执行成功 或 没通过验证

---

# 核心模块

<!-- TODO : 逐节展开 -->

1. **Loop & 预算控制** : 最大轮数 / 停止条件 / token & 时间 & 成本 budget / 中断 & 续跑
2. **Context 管理** : system prompt 分层 / 历史裁剪 / compaction 压缩 / 检索注入 / 文件系统当外部记忆
3. **Tool 层** : tool schema 设计 / 结果截断 / 错误回传格式 / MCP 接入
4. **状态 & 记忆** : TODO 计划文件 / checkpoint / handoff 交接文档
5. **子代理编排** : SubAgent 做 Context 隔离，主 Agent 只收结论
6. **环境 Sandbox** : 容器 / git worktree / 快照回滚
7. **验证层** : 跑测试 / lint / critic / verifier / self-check
8. **权限 & 安全** : permission mode / 人在环 HITL / prompt injection 防护 / 审计日志
9. **可观测性** : trace / 日志 / replay / token 计量

---

# 指标 Metrics

## A. 效果 (Effectiveness)

1. `pass@1` / `pass@k` : 一次 / k 次内解决
2. `resolve rate` : 任务解决率 (SWE-bench 式)
3. `avg@k` + **方差** : **稳定性**，同一题跑 k 次有几次成
4. rubric score / LLM-as-Judge : 非二元任务的 部分完成度

## B. 效率 & 成本 (Efficiency)

1. steps / turns 数，tool call 次数
2. token 消耗 (input / output / **cached**)，cache hit rate
3. **$ per solved task** : 比单纯准确率 更能反映 harness 好坏
4. wall-clock 时间

## C. 可靠性 (Reliability)

1. 卡死率 / 超时率
2. **循环重复率** : 反复做同一动作
3. **假完成率** : 声称完成但没过验证 $\Rightarrow$ Harness 最该管的指标
4. tool call 错误率 / schema 违规率
5. **recovery rate** : 报错后能自行恢复的比例

## D. 上下文 (Context)

1. context 利用率，compaction 触发次数
2. **长程衰减 (context rot)** : 第 1 轮 vs 第 50 轮 正确率差

## E. 自主性 & 安全

1. human intervention rate (每任务打断次数) / autonomy ratio
2. 危险操作拦截率，prompt injection 抵抗率

## 综合

单点分数没意义，看 **score-vs-budget 帕累托曲线** : 给多少 token / 多少 $，能到多少分

---

# Benchmark

<!-- TODO : 逐个补充 任务形态 / 评测方式 / harness 影响 -->

1. **SWE-bench** (Verified / Pro) : 真实 GitHub issue 修复
2. **Terminal-Bench** : 终端环境任务
3. **τ-bench** (tau-bench) : tool + agent + user 多轮交互
4. **OSWorld** : 桌面 GUI 操作
5. **WebArena** / **BrowseComp** : 网页任务
6. **GAIA** : 通用助手任务
7. **MLE-bench** : 机器学习工程任务

---

# 设计原则

1. **简单 loop + 强模型 > 复杂手工 workflow** (bitter lesson)
2. 工具 **少而正交**，描述写清楚
3. 让模型 **看得见反馈** (测试输出 / 报错原文)
4. 一切 **可恢复** : checkpoint > 长上下文
5. **不信模型的自述，信验证器**

---

# DeepSeek Harness

Links
1. [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness)
2. [dsh-plugin](https://github.com/topics/dsh-plugin)

# Codex Harness

