"""
My Feed Forward Network & Residual Connection Implementation
"""

import torch
import torch.nn as nn
import torch.nn.functional as F

class FeedForwardNetwork(nn.Module):
    def __init__(self, d_model, d_ffn, dropout):
        super().__init__()

        self.linear_1 = nn.Linear(d_model, d_ffn)
        self.linear_2 = nn.Linear(d_ffn, d_model)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x):
        """
        x      : (batch_size, seq_len, d_model)
        return : (batch_size, seq_len, d_model)
        原文使用顺序 : Linear -> Activation -> Dropout -> Linear
        """
        return self.linear_2(self.dropout(F.relu(self.linear_1(x))))


class ResidualConnection(nn.Module):  # 对应 Transformer 论文中的 Add & Norm
    def __init__(self, d_model, dropout):
        super().__init__()
        self.layer_norm = nn.LayerNorm(d_model)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x, sub_layer, post_norm: bool = False):
        """
        x : (batch_size, seq_len, d_model)
        return : (batch_size, seq_len, d_model)
        
        Post-Norm : SubLayer -> Dropout -> Add -> Norm
        Transformer 论文中使用 Post-Norm
        
        Pre-Norm  : Norm -> SubLayer -> Dropout -> Add
        训练稳定性更高，梯度流动的顺畅性更好(input x 直接 和 output return 连接)
        现在主流使用 Pre-Norm
        """
        if post_norm:
            return self.layer_norm(x + self.dropout(sub_layer(x)))
        else:  # pre-norm
            return x + self.dropout(sub_layer(self.layer_norm(x)))

