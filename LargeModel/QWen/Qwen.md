# Qwen

[Qwen2.5-VL - Github](https://github.com/QwenLM/Qwen2.5-VL)

[Qwen/Qwen2.5-VL-3B-Instruct - HuggingFace](https://huggingface.co/Qwen/Qwen2.5-VL-3B-Instruct)




单纯的 Qwen (纯文本版) : Decoder-only
Qwen-VL (多模态版) : Vision Encoder(ViT) + Adapter + Decoder-only LLM(Backbone)






json 格式的 msgs 只是 对话脚本(原材料)，需要将 排版成 Qwen-VL 专属的提示词格式

Qwen-VL 只认 `<|im_start|>{role}\n{content}<|im_end|>` 这种包裹方式，并且最后还要 append  `<im_start>assistant` 才会生成回复 (assistant starts talking now)

```bash
<|im_start|>system
You are a helpful assistant.<|im_end|>
<|im_start|>user
<|vision_start|><|image_pad|><|vision_end|>Describe this image.<|im_end|>
<|im_start|>assistant
```

`|<image_pad>|` 只是一个 占位标记


合法 JSON 里，字符串内部不能出现裸换行，必须写成转义 `\\n`
Python 写正则时常用 原始字符串 `r'...'`，让反斜杠 `\` 不先被 Python 自己吃掉
1. `r'\n'` : 正则里真的是 `\` & `n` 两字符
2. `'\n'`  : 被 Python 变成换行符



auto
1. torch_dtype="auto" : 自动 挑最低安全精度
2. device_map="auto"  : 自动 把权重切片到可用设备



