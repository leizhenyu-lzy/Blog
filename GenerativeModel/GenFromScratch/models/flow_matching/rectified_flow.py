"""
Rectified Flow / Linear Conditional Flow Matching.

与 DDPM 的 GaussianDiffusion 类似, 这里把训练目标和采样 ODE 从 backbone
里解耦出来。backbone 只需要满足:
    model(x_t, t_model) -> velocity

其中:
    x_t = (1 - t) * noise + t * x_data,  t in [0, 1]
    target velocity = x_data - noise
"""

import torch
import torch.nn as nn
import torch.nn.functional as F


class RectifiedFlow(nn.Module):
    """
    Linear CFM / Rectified Flow 训练与采样逻辑

    负责训练目标和采样过程，但不关心 backbone 是 UNet 还是 DiT

    Args:
        time_scale: 把连续时间 t in [0, 1] 映射到现有 DDPM backbone 的时间嵌入尺度。
                    现有 UNet / DiT 的 SinusoidalTimeEmbedding 原本吃 0~999,
                    因此默认使用 1000.0
                    外部无感
    """

    def __init__(self, time_scale: float = 1000.0):
        super().__init__()
        assert time_scale > 0.0, f"time_scale must be positive, got {time_scale}"
        self.time_scale = float(time_scale)
        self.register_buffer("_device_ref", torch.empty(0), persistent=False)  # empty tensor for device anchor

    def _scale_time(self, t: torch.Tensor) -> torch.Tensor:
        """
        t in [0, 1] -> t_model in [0, time_scale].
        reuse current UNet / DiT 's time embedding
        外部无感
        """
        return t * self.time_scale

    @staticmethod
    def _expand_time_dim(t: torch.Tensor, x: torch.Tensor) -> torch.Tensor:
        """(B,) -> (B, 1, 1, 1, ...) for broadcasting over x."""
        return t.view(t.shape[0], *([1] * (x.ndim - 1)))  # (B,) -> (B, 1, 1, 1) align with (B, C, H, W)

    def sample_training_tuple(
        self,
        x_data: torch.Tensor,
    ) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
        """
        采样一组训练用的 (x_t, t_model, target_velocity, noise).

        x_t = (1 - t) * noise + t * x_data
        v   = x_data - noise
        """
        b = x_data.shape[0]
        t = torch.rand(b, device=x_data.device, dtype=x_data.dtype)  # [0, 1)
        noise = torch.randn_like(x_data)  # noise 尺寸 和 图像一致
        t_view = self._expand_time_dim(t, x_data)
        x_t = (1.0 - t_view) * noise + t_view * x_data  # position linear interpolation
        target_velocity = x_data - noise  # fixed for current flow, does not depend on t

        return x_t, self._scale_time(t), target_velocity, noise

    def compute_loss(
        self,
        model: nn.Module,
        x_data: torch.Tensor,
    ) -> torch.Tensor:
        """
        L = E[ || v_theta(x_t, t) - (x_data - noise) ||^2 ].
        """
        x_t, t_model, target_velocity, _ = self.sample_training_tuple(x_data)
        velocity_pred = model(x_t, t_model)
        return F.mse_loss(velocity_pred, target_velocity)

    @torch.no_grad()
    def sample_loop(
        self,
        model: nn.Module,
        shape: tuple,
        num_steps: int = 50,
    ) -> torch.Tensor:
        """
        Euler ODE 采样: 从 Gaussian noise 在 t=0 积分到 t=1.

        x_{t+dt} = x_t + dt * v_theta(x_t, t)
        """
        assert num_steps > 0, f"num_steps must be positive, got {num_steps}"

        device = self._device_ref.device
        b = shape[0]
        x_t = torch.randn(shape, device=device)
        dt = 1.0 / num_steps

        for i in range(num_steps):
            t = torch.full(
                (b,),
                i / num_steps,
                device=device,
                dtype=x_t.dtype,
            )
            velocity = model(x_t, self._scale_time(t))
            x_t = x_t + dt * velocity

        return x_t
