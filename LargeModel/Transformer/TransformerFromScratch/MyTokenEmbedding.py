"""
My Token Embedding Implementation
"""

import torch
import torch.nn as nn
import torch.nn.functional as F

class TokenEmbedding(nn.Module):
    def __init__(self, vocab_size, d_model):
        super().__init__()
        self.d_model = d_model
        self.vocab_size = vocab_size

        # nn.Parameter 变成可训练的参数，并自动注册到模型中
        # 被 优化器看见，自动更新，自动保存
        # 受到 .train() & .eval() 影响
        self.weight = nn.Parameter(torch.randn(vocab_size, d_model))

    def forward(self, idx_seq):
        """
        PyTorch 高级索引
        用一个张量(Tensor) 去索引另一个张量时，输出的形状 自动保留索引张量的形状
        """
        return self.weight[idx_seq]



