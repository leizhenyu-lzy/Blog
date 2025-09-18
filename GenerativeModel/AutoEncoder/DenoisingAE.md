# Denoising AutoEncoders

[Denoising Autoencoders - YouTube(Deepia)](https://www.youtube.com/watch?v=0V96wE7lY4w&t=191s)

---

图像噪声 : 像素值的随机变化，会破坏原始信号

噪声的强度 : 指的是噪声的方差(Variance)

常见的噪声建模方法
1. Gaussian Noise (高斯噪声)
   1. 遵循 **正态分布 Normal Distribution** 的随机噪声，高斯分布 就是 正态分布
   2. **高斯噪声的强度(方差) 与 信号的强度 无关**，无论信号是强是弱 噪声的方差都是恒定的，来自系统自身的特性
   3. 有很好的性质
   4. $x_{\text{noisy}} = x_{\text{clean}} + \epsilon \ \text{with} \ \epsilon \sim \mathcal{N}(0, \sigma)$
      1. 无论图像内容，只需要直接添加到像素值中
      2. 随机变化 遵循 正态分布
      3. 多数 集中在 0，少数 极端 异常值
2. Poisson Noise  (泊松噪声)
   1. Shot Noise (散粒噪声) / Photon Noise (光子噪声)
   2. **离散型噪声**，描述 在固定时间间隔内 随机事件发生的次数
   3. **泊松噪声的强度 与 信号的强度 相关**，其噪声的方差 等于 信号的平均值，信号越强，噪声越大


