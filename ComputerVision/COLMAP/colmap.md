# COLMAP

# Installation

[COLMAP - Installation](https://colmap.github.io/install.html)

```bash
# Dependencies from the default Ubuntu repositories
sudo apt-get install \
    git \
    cmake \
    ninja-build \
    build-essential \
    libboost-program-options-dev \
    libboost-filesystem-dev \
    libboost-graph-dev \
    libboost-system-dev \
    libeigen3-dev \
    libflann-dev \
    libfreeimage-dev \
    libmetis-dev \
    libgoogle-glog-dev \
    libgtest-dev \
    libgmock-dev \
    libsqlite3-dev \
    libglew-dev \
    qtbase5-dev \
    libqt5opengl5-dev \
    libcgal-dev \
    libceres-dev

# To compile with CUDA support, also install Ubuntu’s default CUDA package
sudo apt-get install -y \
    nvidia-cuda-toolkit \
    nvidia-cuda-toolkit-gcc

# Configure and compile COLMAP
git clone https://github.com/colmap/colmap.git
cd colmap
mkdir build
cd build
cmake .. -GNinja
ninja
sudo ninja install
```


Run COLMAP
```bash
colmap -h  # help
colmap gui
```





[Snap 安装 COLMAP](https://snapcraft.io/install/colmap/ubuntu) - 未测试成功

