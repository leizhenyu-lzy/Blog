# NVIDIA Container Toolkit




# Step 1 : 安装 NVIDIA Driver & CUDA Toolkit

[NVIDIA Drivers Installation - Ubuntu Docs](https://documentation.ubuntu.com/server/how-to/graphics/install-nvidia-drivers/index.html)

检测方法 :
1. `nvidia-smi`
2. `cat /proc/driver/nvidia/version`

`nvidia-smi`
1. Driver Version : NVIDIA 驱动程序 的版本号，CUDA Toolkit 的版本选择是基于这个驱动版本来决定的
2. CUDA   Version : GPU 驱动程序(Driver) 支持的最高 CUDA API 版本

CUDA Toolkit 版本 : 独立的软件开发包(SDK)，包含编译器、库和工具，根据 深度学习框架 (如 PyTorch、TensorFlow) 的要求 选择安装的版本

[CUDA Toolkit Downloads - NVIDIA](https://developer.nvidia.com/cuda-downloads)


修改 `~/.bashrc`，添加2行
1. `export PATH=/usr/local/cuda/bin:${PATH}`
2. `export LD_LIBRARY_PATH=/usr/local/cuda/lib64:${LD_LIBRARY_PATH}`

检测方法 : `nvcc -V`


---

# Step 2 : 安装 Docker

[Install Docker Engine on Ubuntu - Docker Docs](https://docs.docker.com/engine/install/ubuntu/)

[Linux post-installation steps for Docker Engine - Docker Docs](https://docs.docker.com/engine/install/linux-postinstall/)

可能需要 重启/注销 一下，使得 权限生效

检测方法 :
1. `docker --version`
2. `docker run hello-world` (不需要 `sudo` 就能运行)


---

# Step 3 : 安装 NVIDIA Container Toolkit

[Installing the NVIDIA Container Toolkit - NVIDIA Docs](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html)
1. Installation
2. Configuration

检测方法 :
1. `nvidia-ctk --version` & `cat /etc/docker/daemon.json`
   1. <img src="Pics/NvidiaContainer001.png" width=350>
2. `docker run --rm --gpus all nvidia/cuda:11.0.3-base-ubuntu20.04 nvidia-smi`
   1. 理论上看到的 和 `nvidia-smi` 的 结果应该一致


---





