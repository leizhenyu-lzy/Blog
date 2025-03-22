#

[Download Isaac Sim - Nvidia](https://docs.isaacsim.omniverse.nvidia.com/4.5.0/installation/download.html)




# Installation


```bash
# 检查 ICD 冲突 (只保留一个位置包含 nvidia_icd.json 文件，另一个重命名加一个 '.bak')

ls /etc/vulkan/icd.d/*nvidia*
ls /usr/share/vulkan/icd.d/*nvidia*

```






[NVIDIA Isaac Sim](https://developer.nvidia.com/isaac/sim)
1. 点击 `Download Omniverse` 进入 [Installation](https://docs.omniverse.nvidia.com/isaacsim/latest/installation/index.html)
2. 选择 `Workstation Installation`, Direct Link: `Linux`, 下载 `omniverse-launcher-linux.AppImage`

打开 `Omniverse Launcher`，进入 `EXCHANGE`，搜索 `ISAAC SIM` 并安装，同时 安装 `CACHE`

