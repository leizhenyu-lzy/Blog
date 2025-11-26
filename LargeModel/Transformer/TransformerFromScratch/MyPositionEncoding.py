"""
My Position Encoding Implementation
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import math


class PositionalEncoding(nn.Module):
    def __init__(self, d_model, max_seq_len):
        super().__init__()

        self.d_model = d_model
        self.max_seq_len = max_seq_len

        position_encoding = torch.zeros(max_seq_len, d_model)

        positions = torch.arange(0, max_seq_len).unsqueeze(1) # (max_seq_len,) -> (max_seq_len, 1)
        
        # 公式变换 : 1 / 10000^(2i/d_model) = exp((2i/d_model) * -log(10000))
        div_terms = torch.exp(torch.arange(0, d_model, 2).float() / d_model * -(math.log(10000.0)))  # (d_model // 2,)
        
        # Broadcast
        position_encoding[:, 0::2] = torch.sin(positions * div_terms)
        position_encoding[:, 1::2] = torch.cos(positions * div_terms)
        
        position_encoding = position_encoding.unsqueeze(0) # (max_seq_len, d_model) -> (1, max_seq_len, d_model)
        
        # register_buffer 是 nn.Module 自带的方法
        # 这不是模型参数(Parameter)，不需要梯度更新，但它是模型状态的一部分
        # 存成 buffer 后，model.cuda() 时它会自动跟着去 GPU，model.state_dict() 也会包含
        self.register_buffer('position_encoding', position_encoding)

    def forward(self, x):
        """
        x      : (batch_size, seq_len, d_model)
        return : (1, seq_len, d_model)，相加的时候 会 Broadcast
        """
        seq_len = x.size(1)
        return self.position_encoding[:, :seq_len, :]

