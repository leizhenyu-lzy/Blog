"""
My Attention Encoder & Decoder Layer Implementation
"""

import torch
import torch.nn as nn
import torch.nn.functional as F

from MyMultiHeadAttention import MultiHeadAttention
from MyFeedForwardResidual import FeedForwardNetwork, ResidualConnection


class AttentionEncoderLayer(nn.Module):
    def __init__(self, d_model, n_head, d_ffn, dropout, post_norm=False):
        super().__init__()
        
        self.post_norm = post_norm
        
        self.self_attn = MultiHeadAttention(d_model, n_head, dropout)
        self.ffn = FeedForwardNetwork(d_model, d_ffn, dropout)
        
        self.residual_connect_attn = ResidualConnection(d_model, dropout)
        self.residual_connect_ffn = ResidualConnection(d_model, dropout)

    def forward(self, x, src_mask : torch.bool = None):
        # lambda function，作为一个 适配器
        # 本来 ResidualConnection 接受了 x & sub_layer 只会简单的 sub_layer(x)，但是 MHA 需要 q/k/v & mask
        self_attn_func = lambda src : self.self_attn(q=src, k=src, v=src, mask=src_mask)
        x = self.residual_connect_attn(x, self_attn_func, self.post_norm)
        
        x = self.residual_connect_ffn(x, self.ffn, self.post_norm)
        
        return x
        

class AttentionDecoderLayer(nn.Module):
    def __init__(self, d_model, n_head, d_ffn, dropout, post_norm=False):
        super().__init__()
        
        self.post_norm = post_norm
        
        self.self_attn = MultiHeadAttention(d_model, n_head, dropout)
        self.cross_attn = MultiHeadAttention(d_model, n_head, dropout)
        self.ffn = FeedForwardNetwork(d_model, d_ffn, dropout)
        
        self.residual_connect_attn = ResidualConnection(d_model, dropout)
        self.residual_connect_cross_attn = ResidualConnection(d_model, dropout)
        self.residual_connect_ffn = ResidualConnection(d_model, dropout)


    def forward(self, x, encoder_output, src_mask : torch.bool = None, tgt_mask : torch.bool = None):
        self_attn_func = lambda src : self.self_attn(q=src, k=src, v=src, mask=tgt_mask)
        x = self.residual_connect_attn(x, self_attn_func, self.post_norm)
        
        # 强制 Decoder 不要去关注 Encoder 输出中的 Padding 位置，Mask 永远遮挡 Key
        cross_attn_func = lambda src : self.cross_attn(q=src, k=encoder_output, v=encoder_output, mask=src_mask)
        x = self.residual_connect_cross_attn(x, cross_attn_func, self.post_norm)
        
        x = self.residual_connect_ffn(x, self.ffn, self.post_norm)
        
        return x
