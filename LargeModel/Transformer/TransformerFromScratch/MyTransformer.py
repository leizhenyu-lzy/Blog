"""
My Transformer Scratch Implementation
"""


import torch
import torch.nn as nn
import torch.nn.functional as F
import copy

from MyAttentionEncoderDecoder import AttentionEncoderLayer, AttentionDecoderLayer
from MyPositionEncoding import PositionalEncoding
from MyTokenEmbedding import TokenEmbedding


def clone_layers(layer, N):
    return nn.ModuleList([copy.deepcopy(layer) for idx in range(N)])

class EncoderLayers(nn.Module):
    def __init__(self, layer, N):
        super().__init__()
        self.layers = clone_layers(layer, N)
        self.layer_norm = nn.LayerNorm(layer.d_model)
    
    def forward(self, x, src_mask : torch.bool = None):
        for layer in self.layers:
            x = layer(x, src_mask)
        return self.layer_norm(x)

class DecoderLayers(nn.Module):
    def __init__(self, layer, N):
        super().__init__()
        self.layers = clone_layers(layer, N)
        self.layer_norm = nn.LayerNorm(layer.d_model)

    def forward(self, x, encoder_output, src_mask : torch.bool = None, tgt_mask : torch.bool = None):
        for layer in self.layers:
            x = layer(x, encoder_output, src_mask, tgt_mask)
        return self.layer_norm(x)

class Transformer(nn.Module):
    def __init__(
            self, src_vocab_size, tgt_vocab_size, 
            d_model, n_head, d_ffn, 
            n_encoder_layers, n_decoder_layers, max_seq_len, dropout
        ):
        super().__init__()
        
        self.src_embed = nn.Sequential(
            TokenEmbedding(src_vocab_size, d_model),
            PositionalEncoding(d_model, max_seq_len),
        )
        self.tgt_embed = nn.Sequential(
            TokenEmbedding(tgt_vocab_size, d_model),
            PositionalEncoding(d_model, max_seq_len),
        )
        
        encoder_layer = AttentionEncoderLayer(d_model, n_head, d_ffn, dropout)
        decoder_layer = AttentionDecoderLayer(d_model, n_head, d_ffn, dropout)
        
        self.encoder = EncoderLayers(encoder_layer, n_encoder_layers)
        self.decoder = DecoderLayers(decoder_layer, n_decoder_layers)
        
        self.interpret_linear = nn.Linear(d_model, tgt_vocab_size)
        
        self.reset_parameters()
        
    def reset_parameters(self):
        for p in self.parameters():
            if p.dim() > 1:
                nn.init.xavier_uniform_(p)  # Xavier 均匀分布初始化
    
    def encode(self, src, src_mask : torch.bool = None):
        return self.encoder(self.src_embed(src), src_mask)
    
    def decode(self, tgt, encoder_output, src_mask : torch.bool = None, tgt_mask : torch.bool = None):
        return self.decoder(self.tgt_embed(tgt), encoder_output, src_mask, tgt_mask)
    
    def forward(self, src, tgt, src_mask : torch.bool = None, tgt_mask : torch.bool = None):
        # encode
        src_embed = self.src_embed(src)
        encoder_output = self.encoder(src_embed, src_mask)
        
        # decode
        tgt_embed = self.tgt_embed(tgt)
        decoder_output = self.decoder(tgt_embed, encoder_output, src_mask, tgt_mask)
        
        # interpret
        return self.interpret_linear(decoder_output)


def make_src_mask(src, pad_idx):
    """
    只 处理 source 的 padding mask
    pad_idx : padding token 在 vocabulary 中的 index
    src: (batch, seq_len) -> return: (batch, 1, 1, seq_len)
    
    利用 PyTorch 的 广播机制 (Broadcasting)
    让 Mask 能够自动适配 Multi-Head Attention 中的 4 维注意力分数矩阵，形状 (batch_size, n_head, q_seq_len, k_seq_len)
    """
    return (src != pad_idx).unsqueeze(1).unsqueeze(2)

def make_tgt_mask(tgt, pad_idx):
    """
    处理 target 的 padding mask 和 casual mask
    pad_idx : padding token 在 vocabulary 中的 index
    tgt: (batch, tgt_len) -> return: (batch, 1, tgt_len, tgt_len)
    
    利用 PyTorch 的 广播机制 (Broadcasting)，让 Mask 能够自动适配 Multi-Head Attention 中的 4 维分数矩阵
    """
    tgt_pad_mask = (tgt != pad_idx).unsqueeze(1).unsqueeze(2)
    tgt_len = tgt.size(1)
    tgt_causal_mask = torch.tril(torch.ones(tgt_len, tgt_len))
    return tgt_pad_mask & tgt_causal_mask

https://gemini.google.com/app/ba2f65a24ad1b39b