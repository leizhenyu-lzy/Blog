# Benchmark

Benchmark = **测试任务 + 测试环境 / 规则 + 评分方法**，用来衡量模型某方面的能力

宏观上可以分为
1. **答题能力** : 知识、数学、推理
2. **做事能力** : 写代码、操作电脑、完成专业工作
   1. 测的是 **模型 + Agent 框架 + 工具** 的整体表现

本文按截图类别整理，版本号沿用截图；整理日期：2026-09-07。分类会交叉，不代表统一的行业标准；这里只记“测什么”，不记录易变化的模型排名。

## 3rdParty Website

| 名称 | 解释 |
| --- | --- |
| [Artificial Analysis](https://artificialanalysis.ai/) | 第三方 AI 评测平台，比较模型能力、速度、延迟、成本及 API 服务商，也发布综合指数。 |
| Benchmark | 一套具体测试，相当于一张试卷。 |
| Index | 多项评测汇总的综合分数，组成和权重可能随版本变化。 |
| Leaderboard | 根据某项指标排列的榜单。 |

## ARC-AGI-3：交互推理与泛化

[ARC-AGI-3](https://arcprize.org/arc-agi/3)

测的是：**面对没见过的环境，能不能通过探索学会规则、发现目标，并规划行动完成任务。**

可以想成一个没有完整说明书的陌生小游戏：观察画面 → 尝试动作 → 看反馈 → 推断规则 → 调整策略。除了能否完成，也关注相对人类基线的行动效率。

ARC-AGI-1 / 2 主要是根据示例推断静态网格变换；ARC-AGI-3 转向需要持续交互的环境。它关注新任务中的学习与适应能力，分数本身不等于“是否实现 AGI”。[官方介绍](https://arcprize.org/blog/arc-agi-3-launch)

## Academic：学术知识与推理

| Benchmark | 宏观上测什么 |
| --- | --- |
| [Terminal-Bench Science 0.1](https://openai.com/index/gpt-6-astra/) | 用代码和终端完成科学研究流程，例如数据分析、运行模拟、拟合模型。 |
| [FrontierMath Tier 4 (v2)](https://epoch.ai/frontiermath/tiers-1-4/about) | 专家编写的高难度数学题；Tier 4 偏研究级数学推理。 |
| [GPQA Diamond](https://arxiv.org/abs/2311.12022) | 物理、化学、生物等研究生级科学问答；Diamond 是精选的高难度子集。 |
| [Humanity's Last Exam（HLE，w/ tools）](https://lastexam.ai/) | 跨学科专家级难题，测广泛知识与复杂推理；截图采用允许使用工具的设置。 |

## Coding：编程与软件工程

| Benchmark / Index | 宏观上测什么 |
| --- | --- |
| [Terminal-Bench 4.0](https://www.tbench.ai/) | 在终端环境中完成多步骤任务，例如改代码、调试、配置环境；既测编程，也测命令行操作。截图版本为 4.0。 |
| [DeepSWE v1.1](https://arxiv.org/abs/2607.07946) | 需要长时间、多步骤推进的软件工程任务，关注 Agent 能否完成完整实现并通过验证。 |
| [FrontierCode 1.1 Extended（score）](https://cognition.com/frontiercode) | 真实代码仓库中的工程任务，重点看代码是否达到可合并标准，包括正确性、测试质量、风格和修改范围。 |
| [FrontierCode 1.1 Main（score）](https://cognition.com/blog/frontier-code-1.1) | 同一评测的 Main 子集；与 Extended 是不同题目范围，比较时应保持子集一致。 |
| Internal Database Migration Tasks | 数据库迁移类内部工程测试；公开细节有限，不将名称推测扩展为具体题目或评分规则。 |
| [Artificial Analysis Coding Agent Index v1.4](https://artificialanalysis.ai/) | 编程 Agent 的综合指数，汇总多项工程评测；不是单独一套编程题。 |

内部项目名称及截图版本见[原始评测表](https://openai.com/index/gpt-6-astra/)。

## Science & Health：生命科学与医疗

| Benchmark | 宏观上测什么 |
| --- | --- |
| [GeneBench Pro](https://jeremyhli.org/writing/genebench-pro/) | 基因组学、定量生物学等多阶段分析，关注从数据、统计结果走到科学判断的能力。 |
| [MedChemBench（Internal）](https://openai.com/index/introducing-new-capabilities-to-gpt-rosalind/) | 药物化学推理，例如理解分子结构、判断药物性质、优化候选分子；属于内部评测。 |
| [LifeSciBench](https://openai.com/index/introducing-life-sci-bench/) | 真实生命科学研究任务，例如解读证据、设计实验、分析矛盾结果、决定下一步研究方向。 |
| [HealthBench Professional（length-adjusted）](https://arxiv.org/abs/2604.27470) | 医疗专业人员实际工作中的问答与辅助任务；按专家标准评分，并校正回答长度带来的影响。 |

## Computer Use：电脑操作

| Benchmark | 宏观上测什么 |
| --- | --- |
| [Agents' Last Exam（ALE）](https://arxiv.org/abs/2606.05405) | 跨行业、长流程的真实专业任务，测 Agent 能否使用电脑和工具交付可验证的工作成果。 |
| [OSWorld 2.0](https://os-world.github.io/) | 在桌面操作系统和应用中完成任务，测完整操作流程；截图限定为 `v2026.08.08, offline set, partial score`，不能与其他版本或全任务成功率直接混用。 |
| [ScreenSpot-Pro（no tools）](https://github.com/likaixin2000/ScreenSpot-Pro-GUI-Grounding) | 根据指令在高分辨率软件截图中定位目标控件，侧重“应该点哪里”；不是完整的多步任务执行。 |

可以这样区分：**ScreenSpot-Pro 看定位，OSWorld 看操作流程，ALE 看较长专业任务的最终交付。**

## Professional：专业工作

| Benchmark / Index | 宏观上测什么 |
| --- | --- |
| [AutomationBench](https://github.com/zapier/AutomationBench) | 通过工具 / API 协调多个业务应用，完成销售、财务、HR 等工作流，并检查最终业务状态。 |
| [BenchCAD](https://benchcad.com/) | 理解和生成参数化 CAD：从机械零件图像恢复建模代码、回答几何问题或修改设计，测空间推理与工程建模。 |
| [BrowseComp](https://openai.com/index/browsecomp/) | 通过网页搜索和多处信息核对，找到难以检索的答案，测深度检索能力。 |
| OpenScore String Quartets（1 − OMR-NED） | 基于弦乐四重奏乐谱的光学乐谱识别评测：把乐谱图像转为结构化音乐表示；`1 − OMR-NED` 是把归一化编辑距离转成越高越好的指标。 |
| Internal Design Tasks | 设计类内部任务，关注设计成果；具体任务范围及评分细节需看发布方说明。 |
| Internal Data Science Tasks | 数据科学类内部任务，关注分析工作成果；公开信息有限。 |
| [Artificial Analysis Intelligence Index v4.1.1](https://artificialanalysis.ai/) | 多方面模型能力的综合指数；截图放在 Professional 下，但它不只衡量专业办公能力。 |

OpenScore 指标和内部任务名称见[原始评测表及脚注](https://openai.com/index/gpt-6-astra/)；乐谱识别方法背景见 [LEGATO](https://arxiv.org/abs/2506.19065)。

## Cybersecurity：网络与软件安全

| Benchmark | 宏观上测什么 |
| --- | --- |
| [ExploitBench](https://exploitbench.ai/exploitbench.pdf) | 从软件漏洞走到可验证利用的能力，关注实际安全任务而非安全知识问答。 |
| [Exploit Gym / ExploitGym](https://openai.com/index/gpt-6-astra/) | 同样关注把已知软件漏洞转化为有效利用的能力，在可执行环境中验证结果。 |
| [ExploitBench（June–Aug 2026）](https://openai.com/index/gpt-6-astra/) | 发布方针对该时间段漏洞构建的内部评测，减少历史漏洞可能已被模型见过的影响；不等同于原始 ExploitBench。 |
| [SRE-Bench](https://openai.com/index/gpt-6-astra/) | 软件逆向工程：没有源代码时，理解二进制程序的核心逻辑。这里的 SRE 不是网站可靠性工程。 |
| [SEC-Bench Pro](https://sec-bench.github.io/) | 在复杂真实软件中进行长流程漏洞挖掘与验证，关注 Agent 的实际安全分析能力。 |

## 看分数时记住

- **先看测什么**：数学高分、写代码强、会操作电脑，是不同能力。
- **对齐设置再比较**：版本、题目子集、工具权限、Agent 框架、思考预算、尝试次数都会影响成绩。
- **看清指标**：`score` 不一定是任务成功率；`partial score` 允许部分得分；`w/ tools` / `no tools` 指是否允许工具；`length-adjusted` 指做了回答长度校正。
- **区分来源**：第三方复测、厂商自报和内部评测的信息透明度不同；综合指数也要看版本及组成。真实选型仍需用自己的任务验证。
