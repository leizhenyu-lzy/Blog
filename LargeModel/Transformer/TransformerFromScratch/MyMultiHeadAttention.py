"""
My Multi-Head Attention Implementation
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import math

class MultiHeadAttention(nn.Module):
    def __init__(self, d_model, n_head, dropout=0.1):
        super().__init__()
        
        assert d_model % n_head == 0, "d_model must be divisible by n_heads"
        
        self.d_model = d_model
        self.n_head = n_head
        self.d_head = d_model // n_head

        self.q_linear = nn.Linear(d_model, d_model)
        self.k_linear = nn.Linear(d_model, d_model)
        self.v_linear = nn.Linear(d_model, d_model)
        
        self.dropout = nn.Dropout(dropout)
        self.out_linear = nn.Linear(d_model, d_model)

    def forward(self, q, k, v, mask=None):
        """
        q & k & v : (batch_size, seq_len, d_model)
        mask      : (batch_size, seq_len, seq_len)
        return    : (batch_size, seq_len, d_model)
        
        Self-Attention  : q=k=v=x，padding mask
        Cross-Attention : q=x，k=encoder_output，v=encoder_output，look-ahead/causal mask
        """
        batch_size = q.size(0)
        
        # 线性变换
        q_embed = self.q_linear(q)
        k_embed = self.k_linear(k)
        v_embed = self.v_linear(v)
        
        # 分头 + 转置(方便后续矩阵乘法)
        # (batch_size, seq_len, d_model) -> (batch_size, seq_len, n_head, d_head) -> (batch_size, n_head, seq_len, d_head)
        # -1 自动推断 剩余的维度，cross-attention 时，q 的 seq_len 和 k & v 的 seq_len 可能不同，所以不能固定
        q_embed = q_embed.view(batch_size, -1, self.n_head, self.d_head).transpose(1, 2)
        k_embed = k_embed.view(batch_size, -1, self.n_head, self.d_head).transpose(1, 2)
        v_embed = v_embed.view(batch_size, -1, self.n_head, self.d_head).transpose(1, 2)
        # x.transpose(a, b) == x.transpose(b, a) -> 交换 a 和 b 维度
        # .transpose() 不要求输入是 contiguous，任何张量都能 transpose
        # .transpose() 返回的张量 通常是 non-contiguous 的
        # non-contiguous 的张量用在 matmul、+、* 这些算子上完全没问题
        
        # 计算注意力分数
        attention_scores = q_embed @ k_embed.transpose(-2, -1) / math.sqrt(self.d_head)  # (batch_size, n_head, q_seq_len, k_seq_len)
        
        if mask is not None:  # mask 加在 softmax 之前
            attention_scores = attention_scores.masked_fill(mask == 0, -1e9)  # (batch_size, n_head, q_seq_len, k_seq_len)
        
        attention_weights = F.softmax(attention_scores, dim=-1)  # (batch_size, n_head, seq_len, seq_len)  # dim=-1 -> 沿着 每个 head 的 行 做 softmax
        attention_weights = self.dropout(attention_weights)  # Transformer 论文中，Dropout 加在 Softmax 之后，乘以 V 之前
        
        context = attention_weights @ v_embed  # (batch_size, n_head, seq_len, d_head)
        
        # 合头
        # (batch_size, n_head, seq_len, d_head) -> (batch_size, seq_len, n_head, d_head) -> (batch_size, seq_len, d_model)
        context = context.transpose(1, 2).contiguous().view(batch_size, -1, self.d_model)  # token 融合了全局信息的 上下文表示
        # view 通常要在 contiguous 张量上用，transpose 不要求输入是 contiguous，但会导致张量变 non-contiguous，后面再 view 时才需要配合 .contiguous()
        
        output = self.out_linear(context)
        return output
