# Install PyTorch

## Anaconda

常用命令：

conda activate pytorch  激活环境

conda deactivate   回到base

pip list   列出功能包

## CUDA

先查看自己GPU版本，在命令行中输入nvidia-smi

![](toolkit000.png)

[NVIDIA CUDA TOOLKIT DOCUMENTATION](https://docs.nvidia.com/cuda/cuda-toolkit-release-notes/index.html)

对照下表查看可以安装的CUDA Toolkit

![](toolkit001.png)

不行就更新

![](toolkit002.png)

[一篇博客：about_cuda_install](http://allophane.com/index.php/2021/05/04/about_cuda_install/)

## PyTorch

[PyTorch官网](https://pytorch.org/)

![](pytorch000.png)

![](pytorch001.png)

在命令行中输入指令

```python
import torch
torch.cuda.is_available()
```

pip list如下

![](pytorch002.png)