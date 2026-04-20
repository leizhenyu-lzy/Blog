"""
Exponential Moving Average (EMA) of model parameters.

DDPM / diffusion 类模型采样时几乎必用 EMA 权重, 因为原始优化器权重在 SGD 噪声下
采样质量不稳定, EMA 相当于对最近几万步的权重取"惯性平均", 明显更平滑、更稳。

设计选择:
    - 只追踪 `named_parameters()` (可学习参数), 不追踪 buffer.
      理由: EMA 的数学定义就是对可学习参数的平均; buffer 常常本身已经是 moving
      average (e.g. BN running_mean), 再做 EMA 没有意义. OpenAI DDPM /
      diffusers 官方实现也是如此.
    - decay=0.9999 对应有效窗口 ≈ 1/(1-decay) = 1 万步 (CelebA 上约 1.5 epoch).

用法:
    ema = EMA(model, decay=0.9999)
    for x in loader:
        loss = diffusion.compute_loss(model, x)
        loss.backward()
        optimizer.step()
        ema.update(model)             # 每个 optimizer.step() 后调一次

    # 采样前用 EMA 权重造一份独立模型:
    sampling_model = ema.clone_model(model)
    samples = diffusion.p_sample_loop(sampling_model, shape)

保存 / 加载:
    torch.save({"ema": ema.state_dict(), ...}, ckpt_path)
    ema.load_state_dict(ckpt["ema"])
"""

from __future__ import annotations

import copy
from typing import Dict

import torch
import torch.nn as nn


class EMA:
    """参数级 EMA: shadow[k] = decay * shadow[k] + (1 - decay) * model[k]"""

    def __init__(self, model: nn.Module, decay: float = 0.9999):
        assert 0.0 <= decay <= 1.0, f"decay must be in [0, 1], got {decay}"
        self.decay = decay
        self.shadow: Dict[str, torch.Tensor] = self._clone_param_dict(
            dict(model.named_parameters())
        )

    @staticmethod
    def _clone_param_dict(
        params: Dict[str, torch.Tensor],
    ) -> Dict[str, torch.Tensor]:
        """对参数字典做 detach + clone, 保证独立存储、不参与 autograd"""
        return {k: v.detach().clone() for k, v in params.items()}

    @torch.no_grad()
    def update(self, model: nn.Module) -> None:
        """在 optimizer.step() 之后调一次, 更新 shadow 权重

        inplace 实现 (mul_/add_) 避免每步分配新张量. alpha 参数直接把
        (1-decay)*v 的缩放融进 add, 省一个临时张量.
        """
        for k, v in model.named_parameters():
            # shadow = decay * shadow + (1 - decay) * current
            self.shadow[k].mul_(self.decay).add_(v.detach(), alpha=1.0 - self.decay)

    @torch.no_grad()
    def copy_params_to(self, model: nn.Module) -> None:
        """把当前 shadow 权重装到 `model` 对应参数上 (常用于采样前)"""
        for k, v in model.named_parameters():
            v.data.copy_(self.shadow[k])

    def clone_model(self, model: nn.Module) -> nn.Module:
        """
        复制一份 `model` 的结构, 装上 EMA 权重, 用于采样时的模型.
        不影响原 model 的训练权重.
        """
        ema_model = copy.deepcopy(model)
        self.copy_params_to(ema_model)
        ema_model.eval()
        return ema_model

    def state_dict(self) -> Dict[str, torch.Tensor]:
        return self.shadow

    def load_state_dict(self, state_dict: Dict[str, torch.Tensor]) -> None:
        self.shadow = self._clone_param_dict(state_dict)

    def to(self, device: torch.device) -> "EMA":
        """跟随 model 做 device 迁移 (一般不需要手动调)"""
        self.shadow = {k: v.to(device) for k, v in self.shadow.items()}
        return self
