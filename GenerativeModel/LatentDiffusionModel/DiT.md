# DiT : Scalable Diffusion Models with Transformers

https://zhuanlan.zhihu.com/p/599887666

https://zhuanlan.zhihu.com/p/590840909

https://cs.uwaterloo.ca/~ppoupart/teaching/cs480-winter23/slides/

https://cvpr2022-tutorial-diffusion-models.github.io/
1. https://drive.google.com/file/d/1DYHDbt1tSl9oqm3O333biRYzSCOtdtmn/view?usp=sharing
2. https://www.youtube.com/watch?v=cS6JQpEY9cs

---

用 DiT 替代 LDM(latent diffusion model) 中的 U-Net 结构



无条件生成 (Unconditional Generation) : 从纯噪声开始，逐步去噪生成图像，可能会生成符合数据分布的任意图像

类别条件生成 (Class-Conditional Generation) : 定向命题，在生成过程中，模型接收类别作为条件输入，使得生成的图像属于指定类别



FID(Frechet Inception Distance) : 衡量生成图像与真实图像分布之间的距离，数值越小表示生成图像质量越高


