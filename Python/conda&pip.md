# conda & pip

conda 环境是一个独立的环境，包含自己的 python 解释器和依赖


# 常用命令

conda info

conda env list / conda info --envs

conda create -n env_name python=x.x.x

conda remove --name env_name --all

conda activate env_name / deactivate

conda install/uninstall

conda upgrade



pip check  检查包冲突


# info

`conda info` 查看相关信息
1. virtual packages - 虚拟包
   1. 描述系统属性或环境特性的一种机制， 自动生成
   2. 帮助 conda 识别和适配当前环境，例如操作系统类型、CUDA 驱动版本、CPU 架构等
2. package cache - conda 缓存目录

conda 的环境隔离性也意味着 环境内的 pip 和 全局的 pip 是独立的

激活特定的 conda 环境时，pip 命令会绑定到这个环境的 Python 解释器上，使用 pip install 安装的包默认会安装到当前激活的 conda 环境 中，而不会共享到其他环境

激活 conda 环境后，可以通过 `which pip` 命令验证 pip 的工作路径 `/path_to_conda_envs/my_env/bin/pip`

conda 环境的隔离性保证了不同环境之间的包互不干扰

没有激活任何 conda 环境 (或者 conda deactivate 之后)，pip install 会安装到系统全局 python 环境中， `which pip` 结果 `/home/lzy/.local/bin/pip`

base环境(conda创建的默认环境) 和 未激活任何 conda 环境 是不同的情况


注意事项
1. conda 环境下优先使用 conda install
   1. 如果一个包同时可以通过 conda 和 pip 安装，优先使用 conda install，因为
      1. conda 会更好地管理包之间的依赖关系
      2. conda 下载的包通常是经过优化的二进制文件，安装速度更快，兼容性更高
2. pip 和 conda 的包管理可能冲突
   1. 如果使用 pip 安装的包覆盖了 conda 安装的包，可能会引起兼容性问题
   2. 建议先使用 conda install 安装大多数依赖，只在必要时用 pip install
3. 确认 pip 版本 `conda install pip`
4. 安装前查看环境中的已安装包 `conda list`(显示当前环境的所有包，包括 conda 和 pip 安装的包)


# site-packages

site-packages 位置 `~/miniconda3/envs/env_name/lib/pythonX.X/site-packages`



# list

conda list
1. 显示所有包
   1. conda install 安装的包
   2. pip install 安装的包(在 site-packages 中的)
2. 显示来源(标明包的来源渠道)
   1. defaults：来自 conda 的默认仓库
   2. conda-forge：来自 conda-forge 社区仓库
   3. pypi：通过 pip 安装的包

pip list
1. 仅显示 pip 安装的包
2. 无法区分来源(只显示包名和版本号)



# install

conda install
1. 如果你安装的包已经在 conda 的缓存中，conda 会 **硬链接 hard link** 该包到目标环境的 site-packages
2. 如果包不存在于缓存中，conda 会从网络下载包到缓存目录，然后再 硬链接 到目标环境的 site-packages

pip install
1. 包会安装到当前 conda 环境的 site-packages 中，不会存储在 conda 的 package cache 中
2. 这些包只对当前环境可见，其他 conda 环境不会共享这些通过 pip 安装的包

如果一个包通过 conda install 安装后，又通过 pip install 安装了不同版本，可能导致环境中的包冲突

onda 安装的包来源于 Conda 的包仓库(如 defaults 或 conda-forge)，这些包由 Conda 社区打包、优化和管理，确保兼容性(依赖链通常是稳定的，pip 安装的包可能升级或更改了关键依赖，破坏了 conda 环境的稳定性)

pip 安装的包来自 Python Package Index (PyPI)，这些包没有 Conda 的兼容性保证



# 缓存机制

conda 的缓存机制(自动开启)
1. 将下载的包先存储在共享缓存目录中(通常位于 `~/.conda/pkgs` or `/home/lzy/miniconda3/pkgs`)
2. 当其他环境安装相同的包时，conda 会直接从缓存目录中创建硬链接到目标环境，而无需重新下载或复制
3. `conda clean --all` 定期运行 清理未使用的包

pip 的缓存机制
1. pip 会将下载的包文件(如 .whl 或 .tar.gz 格式)存储在 ~/.cache/pip 目录下
2. 当你再次安装相同的包时，pip 会检查缓存，如果缓存中存在所需版本的包，它会直接从缓存中提取，而不是重新从网络下载，然后解压并将相关的文件安装(复制)到当前环境的 site-packages 目录中，不是通过 硬链接方式
3. pip 的缓存机制仅存储 .whl 或 .tar.gz 格式的包文件，而不是解压后的文件



Hard Link(硬链接) 是一种文件系统中的技术，用于创建一个文件的额外引用，使得多个文件名指向同一个数据块
1. 指向相同的数据块
2. 独立的文件名
3. 删除文件不影响数据
   1. 只有当所有硬链接都被删除时，文件的实际数据才会从磁盘中移除
   2. 删除其中一个硬链接，不会影响其他硬链接或原始文件

符号链接/软链接





