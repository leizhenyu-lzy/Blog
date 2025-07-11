# OpenCV VLM Bootcamp

## Table of Contents

- [OpenCV VLM Bootcamp](#opencv-vlm-bootcamp)
  - [Table of Contents](#table-of-contents)
- [Setup](#setup)
- [CLIP](#clip)


# Setup

HuggingFace 的 transformers 库，内置了大量预训练模型，NLP、CV、多模态

`pip install transformers`

# CLIP

[CLIP - Slide](./Slides/CLIP_Internals_and_Architecture.pdf)

Contrastive Language Image Pretraining - CLIP

`from transformers import CLIPTokenizer, CLIPProcessor, CLIPModel`

**multimodal** : vision + language

**internet scale** : image-caption pair, WIT(Web ImageText) Dataset, not public, 400M

或许可以用 [Wikipedia-based Image Text Dataset - Github](https://github.com/google-research-datasets/wit?tab=readme-ov-file#wit--wikipedia-based-image-text-dataset) 代替

**zero-shot capabilities**

Contrastive Learning
1. encode image/text as same sized vector (represent semantic meaning)
   1. vision encoder
   2. text encoder
2. **shared embedding space**
3. 余弦相似度 **cosine similarity** $(a, b) = \frac{a b}{|a| |b|}$
   1. 训练时，CLIP 会在视觉/文本编码器 输出后做 L2-norm
      1. 模型仍在 完整空间 里 输出向量，仅仅是在训练时进行归一化
   2. 向量的模长全部固定为 1，点积就正好等价于余弦值
   3. 模型无法 靠增大模长 来作弊，只能通过改变方向来表达语义差异，从而使学习过程更稳定




