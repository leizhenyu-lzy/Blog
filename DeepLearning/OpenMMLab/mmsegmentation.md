# mmsegmentation

[OpenMMLab github官网](https://github.com/open-mmlab)

[mmsegmentation --- github官网](https://github.com/open-mmlab/mmsegmentation)


## [【OpenMMLab 公开课】语义分割与 MMSegmentation](https://www.bilibili.com/video/BV1944y1b76p/)

### 全卷积网络

![](Pics/mmseg001.png)

![](Pics/mmseg002.png)

![](Pics/mmseg003.png)

![](Pics/mmseg004.png)

意思就是，原来是卷积核和每一个小划窗进行卷积，现在是直接与原图进行卷积

![](Pics/mmseg005.png)

分类任务中，输入大小固定

而分割任务中，输入大小不定，而希望输出和输入大小一致

![](Pics/mmseg006.png)

使用全连接层的卷积化，类别信息保存在通道中(图中为三分类)

![](Pics/mmseg007.png)

原来的分类问题使用的方法是先将特征图向量化，然后再通过矩阵乘法来模拟全连接

现在为了获取和原图相同大小的，使用卷积，不用将特征图化为向量的形式。当把全连接层替换成了卷积层后，就可以不限制输入图像的大小，一次性输入网络即可获得一张图片所有位置的检测目标概率，形成一幅 heatmap

![](Pics/mmseg008.png)

![](Pics/mmseg009.png)

双线性插值相对固定

![](Pics/mmseg010.png)

通过卷积化，加快计算速度

![](Pics/mmseg011.png)

转置卷积的卷积核可学习

![](Pics/mmseg012.png)

图中绿色为输出，蓝色为输入。转置卷积的操作可以理解为先散开然后卷积

![](Pics/mmseg013.png)

仅有形状上互逆

![](Pics/mmseg014.png)

![](Pics/mmseg015.png)

低层次和高层次特征图优势互补

![](Pics/mmseg016.png)

细节越来越多

![](Pics/mmseg017.png)

### 上下文信息

低层次小区域容易有歧义，通过上下文可以更加准确的进行判断

![](Pics/mmseg018.png)

建立特征图金字塔 pyramid pooling
1. 金字塔越顶端，看到的范围越大
2. 金字塔越底端，看到的范围越小

![](Pics/mmseg019.png)

### 空洞卷积与DeepLab系列算法

FCN UNet PSPNet

![](Pics/mmseg020.png)

**空洞卷积 解决下采样问题**

空洞卷积（atrous convolutions）又称扩张卷积（dilated convolutions）

![](Pics/mmseg021.png)

膨胀卷积核

![](Pics/mmseg022.png)

空洞卷积等价于下采样+卷积，两部合成一步

膨胀卷积核，不加入额外参数

![](Pics/mmseg023.png)

DeepLab核心

![](Pics/mmseg024.png)

使用交叉熵损失函数

**条件随机场 后处理**

![](Pics/mmseg025.png)

![](Pics/mmseg026.png)

能量函数包含两项，只跟自己有关的和与周围像素有关的

![](Pics/mmseg027.png)

条件随机场可以产生更加精细的边界

因为同时考虑了原图信息和网络输出的概率信息

**多尺度空洞卷积 ASPP 空间金字塔池化 捕捉上下文信息** Atrous Spatial Pyramid Pooling

![](Pics/mmseg028.png)

和PSPNet不同点在于，PSPNet是多尺度池化，而DeepLab使用的是不同膨胀率的空洞卷积

![](Pics/mmseg029.png)

![](Pics/mmseg030.png)

**总结**

![](Pics/mmseg031.png)

**评价体系**

利用交集和并集

![](Pics/mmseg032.png)

Accuracy : 像素级的 交集与面积的比值

IoU : 交集与并集的比值

Dicd : 两倍的交集除(真实面积+预测面积)

![](Pics/mmseg033.png)

### 语义分割工具包 MMSegmentation

![](Pics/mmseg034.png)

![](Pics/mmseg035.png)

![](Pics/mmseg036.png)

公平比较

![](Pics/mmseg037.png)

![](Pics/mmseg038.png)

**项目结构**

所有 openmmlab 工具包结构一致

![](Pics/mmseg039.png)

![](Pics/mmseg040.png)

模型
1. 主干网络  backbone eg. resnet
2. 颈部  neck  将主干网络产生的多层次特征进行融合  eg. FPN(feature pyramid network)
3. 解码头  decode head  根据特征生成分割图  eg. fcn转置卷积、PSPNet池化金字塔
4. 辅助解码头  auxiliary decode head  基于底层特征产生分割图的结构  eg. resnet
5. 级联解码头  cascade decode head  可能单个解码头效果不够好

![](Pics/mmseg041.png)

![](Pics/mmseg042.png)

resnetV1c 是 resnet 的变种

![](Pics/mmseg048.png)

语义分割一般采用C，7x7 卷积拆分为3个 3x3 的卷积，非线性映射能力更强



采用空洞卷积一般就不采用降采样了

多机多卡的环境下使用 SyncBN

![](Pics/mmseg043.png)

主解码头采用 PSPNet，包含池化金字塔

loss_weight是因为还有一个辅助解码头，控制主解码头的损失函数权重

![](Pics/mmseg044.png)

另一个解码头

鼓励主干网络学习出更好的低层次特征

同样的，也有一个loss_weight，一般辅助解码头的权重小一些

![](Pics/mmseg045.png)

数据集配置

指定一些 dataloader 的参数

数据处理流水线

数据集分为 train val test

![](Pics/mmseg046.png)

数据处理流水线

一开始只是字典

进行数据增强，亮度和对比度等一些操作不用在分割图上同时调整，其他的需要在原图和分割图上同时调整

![](Pics/mmseg047.png)

### 代码实操演示

[mmsegmentation 官方 model zoo](https://mmsegmentation.readthedocs.io/zh_CN/latest/modelzoo_statistics.html)


























## Install

### 源码安装

先安装mmcv

[BUILD MMCV FROM SOURCE 官方文档](https://mmcv.readthedocs.io/en/latest/get_started/build.html)

```bash
git clone https://github.com/open-mmlab/mmcv.git
cd mmcv

pip install -r requirements/optional.txt
# 不是直接 pip install -r requirements.txt

MMCV_WITH_OPS=1 pip install -e . -v

# 会出现结果 : Successfully installed addict-2.4.0 mmcv-full-1.7.1 yapf-0.32.0

python3 .dev_scripts/check_installation.py
# 结果如下
```

```
/home/lzy/Project/mmcv/mmcv/__init__.py:20: UserWarning: On January 1, 2023, MMCV will release v2.0.0, in which it will remove components related to the training process and add a data transformation module. In addition, it will rename the package names mmcv to mmcv-lite and mmcv-full to mmcv. See https://github.com/open-mmlab/mmcv/blob/master/docs/en/compatibility.md for more details.
  warnings.warn(
Start checking the installation of mmcv-full ...
CPU ops were compiled successfully.
CUDA ops were compiled successfully.
mmcv-full has been installed successfully.

Environment information:
------------------------------------------------------------
sys.platform: linux
Python: 3.8.16 (default, Mar  2 2023, 03:21:46) [GCC 11.2.0]
CUDA available: True
GPU 0: NVIDIA GeForce RTX 3050 Laptop GPU
CUDA_HOME: /usr/local/cuda-11.7
NVCC: Cuda compilation tools, release 11.7, V11.7.99
GCC: gcc (Ubuntu 11.3.0-1ubuntu1~22.04) 11.3.0
PyTorch: 2.0.0+cu117
PyTorch compiling details: PyTorch built with:
  - GCC 9.3
  - C++ Version: 201703
  - Intel(R) oneAPI Math Kernel Library Version 2022.2-Product Build 20220804 for Intel(R) 64 architecture applications
  - Intel(R) MKL-DNN v2.7.3 (Git Hash 6dbeffbae1f23cbbeae17adb7b5b13f1f37c080e)
  - OpenMP 201511 (a.k.a. OpenMP 4.5)
  - LAPACK is enabled (usually provided by MKL)
  - NNPACK is enabled
  - CPU capability usage: AVX2
  - CUDA Runtime 11.7
  - NVCC architecture flags: -gencode;arch=compute_37,code=sm_37;-gencode;arch=compute_50,code=sm_50;-gencode;arch=compute_60,code=sm_60;-gencode;arch=compute_70,code=sm_70;-gencode;arch=compute_75,code=sm_75;-gencode;arch=compute_80,code=sm_80;-gencode;arch=compute_86,code=sm_86
  - CuDNN 8.5
  - Magma 2.6.1
  - Build settings: BLAS_INFO=mkl, BUILD_TYPE=Release, CUDA_VERSION=11.7, CUDNN_VERSION=8.5.0, CXX_COMPILER=/opt/rh/devtoolset-9/root/usr/bin/c++, CXX_FLAGS= -D_GLIBCXX_USE_CXX11_ABI=0 -fabi-version=11 -Wno-deprecated -fvisibility-inlines-hidden -DUSE_PTHREADPOOL -DNDEBUG -DUSE_KINETO -DLIBKINETO_NOROCTRACER -DUSE_FBGEMM -DUSE_QNNPACK -DUSE_PYTORCH_QNNPACK -DUSE_XNNPACK -DSYMBOLICATE_MOBILE_DEBUG_HANDLE -O2 -fPIC -Wall -Wextra -Werror=return-type -Werror=non-virtual-dtor -Werror=bool-operation -Wnarrowing -Wno-missing-field-initializers -Wno-type-limits -Wno-array-bounds -Wno-unknown-pragmas -Wunused-local-typedefs -Wno-unused-parameter -Wno-unused-function -Wno-unused-result -Wno-strict-overflow -Wno-strict-aliasing -Wno-error=deprecated-declarations -Wno-stringop-overflow -Wno-psabi -Wno-error=pedantic -Wno-error=redundant-decls -Wno-error=old-style-cast -fdiagnostics-color=always -faligned-new -Wno-unused-but-set-variable -Wno-maybe-uninitialized -fno-math-errno -fno-trapping-math -Werror=format -Werror=cast-function-type -Wno-stringop-overflow, LAPACK_INFO=mkl, PERF_WITH_AVX=1, PERF_WITH_AVX2=1, PERF_WITH_AVX512=1, TORCH_DISABLE_GPU_ASSERTS=ON, TORCH_VERSION=2.0.0, USE_CUDA=ON, USE_CUDNN=ON, USE_EXCEPTION_PTR=1, USE_GFLAGS=OFF, USE_GLOG=OFF, USE_MKL=ON, USE_MKLDNN=ON, USE_MPI=OFF, USE_NCCL=1, USE_NNPACK=ON, USE_OPENMP=ON, USE_ROCM=OFF, 

TorchVision: 0.15.1+cu117
OpenCV: 4.6.0
MMCV: 1.7.1
MMCV Compiler: GCC 11.3
MMCV CUDA Compiler: 11.7
------------------------------------------------------------
```

再源码安装mmsegmentation

```
git clone https://github.com/open-mmlab/mmsegmentation.git
cd mmsegmentation
pip install -v -e .
# "-v" means verbose, or more output
# "-e" means installing a project in editable mode,
# thus any local modifications made to the code will take effect without reinstallation.
```

### 简单安装

[安装指南链接](https://github.com/open-mmlab/mmsegmentation/blob/master/docs/en/get_started.md#installation)

MMSegmentation works on Linux, Windows and macOS. It requires Python 3.6+, CUDA 9.2+ and PyTorch 1.3+.

```bash
# download
pip install -U openmim
mim install mmcv-full
pip install mmsegmentationpip
```

```bash
# verity 会下载一个pth模型和一个py文件
mim download mmsegmentation --config pspnet_r50-d8_512x1024_40k_cityscapes --dest .

# 复制文档里的代码，自己找张图片试试看即可（记得python运行目录位置和图片位置）
# 我测试完就把他们删了
```

我是使用ApolloScape中的图片

![](Pics/test002.jpg)

结果如下

![](Pics/result.jpg)





## [手撸OpenMMlab系列教程(mmcv，mmsegmentation) --- B站视频](https://www.bilibili.com/video/BV1ub4y187DP/)

### 运行代码

[眼球血管数据集](https://staffnet.kingston.ac.uk/~ku15565/CHASE_DB1/assets/CHASEDB1.zip)

转换数据集格式

```bash
# python3 tools/convert_datasets/chase_db1.py /path/to/CHASEDB1.zip

# -o 指定结果保存位置

# 转换位置 : /mnt/sda1/Datasets/CHASEDB1forMMSeg
python3 tools/convert_datasets/chase_db1.py /mnt/sda1/Datasets/CHASEDB1.zip -o /mnt/sda1/Datasets/CHASEDB1forMMSeg

# 转换位置 : /home/lzy/Project/mmsegmentation/data/CHASE_DB1
python3 tools/convert_datasets/chase_db1.py /mnt/sda1/Datasets/CHASEDB1.zip

```

训练的配置在 configs 下

```bash
python3 tools/train.py tools/train.py configs/unet/unet_s5-d16_deeplabv3_4xb4-40k_chase-db1-128x128.py --work-dir userLogs/chaseDB_20230402_162030 --seed 0
```

可以在 /home/lzy/Project/mmsegmentation/configs/_base_/datasets/chase_db1.py 中修改数据集配置文件

```python
data_root = r"/mnt/sda1/Datasets/CHASEDB1forMMSeg"  # modified
```








