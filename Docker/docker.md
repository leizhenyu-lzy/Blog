# Docker

[toc]


# [【GeekHour】30分钟Docker入门教程](https://www.bilibili.com/video/BV14s4y1i7Vf) 

## Docker 简介

用于 构建build、运行run、传送ship 应用程序的平台 

![](Pics/docker007.png)

## Docker 和 虚拟机 的区别

虚拟机

![](Pics/docker008.png)

使用虚拟化(Hypervisor)技术实现

![](Pics/docker009.png)

缺点
1. 占用资源多
2. 启动速度慢

大部分时候不需要整个操作系统的所有功能

![](Pics/docker010.png)

容器

容器 ≠ Docker

Docker 只是容器化的解决方案&平台

![](Pics/docker011.png)

容器使用宿主机的操作系统

优点
1. 启动速度快
2. 减少资源的浪费（服务器上开更多的容器）

## 基本原理和概念

![](Pics/docker012.png)

镜像 image
1. 只读的模板
2. 可以用来创建容器

容器 container
1. 运行实例
2. 提供独立可移植的环境

**镜像&容器 ≈ 类&对象（实例）**

仓库 registry
1. 存储 docker 镜像
2. 最流行的 - docker hub - 公共的，可上传和下载 镜像

docker 使用 client-server 架构模式
1. docker client 和 docker daemon(服务端的守护进程) 之间通过 socket 或 restful api 通信
2. docker client 向 docker daemon 发送请求，docker daemon 接收到请求后进行处理，结果返回给 docker client


## Docker 安装

Windows 中需要开启 Hyper-V 功能

查看版本信息（只看到client说明没有启动docker）

```bash
lzy@Razer:/media/lzy/4D01-C671/Blog (main)$ docker version
Client: Docker Engine - Community
 Cloud integration: v1.0.35+desktop.11
 Version:           25.0.3
 API version:       1.44
 Go version:        go1.21.6
 Git commit:        4debf41
 Built:             Tue Feb  6 21:13:09 2024
 OS/Arch:           linux/amd64
 Context:           desktop-linux

Server: Docker Desktop 4.28.0 (139021)
 Engine:
  Version:          25.0.3
  API version:      1.44 (minimum version 1.24)
  Go version:       go1.21.6
  Git commit:       f417435
  Built:            Tue Feb  6 21:14:25 2024
  OS/Arch:          linux/amd64
  Experimental:     false
 containerd:
  Version:          1.6.28
  GitCommit:        ae07eda36dd25f8a1b98dfbf587313b99c0190bb
 runc:
  Version:          1.1.12
  GitCommit:        v1.1.12-0-g51d5e94
 docker-init:
  Version:          0.19.0
  GitCommit:        de40ad0
```

## 容器化 和 Dockerfile

containerization

容器化三个步骤
![](Pics/docker013.png)

Dockerfile - 文本文件 - 包含指令，告诉 docker 构建应用程序镜像所需要的步骤和配置

包含
1. 精简版操作系统
2. 应用程序的运行环境
3. 应用程序
4. 第三方依赖
5. 配置文件
6. 环境变量


## 实践环节

Dockerfile (D大写，无后缀)

```docker
FROM baseImage
<!-- 指定基础镜像 -->

COPY source dest
<!-- 复制文件 源路径（相对Dockerfile） 目标路径（相对镜像） -->

CMD 
<!--  -->
```

```bash
docker build -t [name] .
# .表示当前目录
```

查看镜像位置
```bash
docker image ls
# 或
docker images
```

```bash
lzy@Razer:/media/lzy/4D01-C671/Blog/Docker/HelloDocker (main)$ docker image ls
REPOSITORY        TAG       IMAGE ID       CREATED          SIZE
hello-my-docker   latest    6d2dd257ed27   15 minutes ago   119MB
```
TAG - 版本(不指定默认为latest)


```bash
docker run [name]
```

如果想在另一环境运行，仅需复制镜像，再run

也可以将镜像上传仓库，使用docker pull

[Play with Docker 网站](https://labs.play-with-docker.com/#)

可以使用命令行运行

## Docker Desktop

volumes - 逻辑卷

docker容器中的数据不会持久化，容器停止后，所有数据会丢失

如果想要持久化，则使用逻辑卷，可以将容器中的目录或指定路径映射到宿主机，保存在宿主机的磁盘中

Dev Environments 用于配置开发环境

## Docker Compose

![](Pics/docker014.png)

![](Pics/docker015.png)



# [Docker 1小时快速上手教程，无废话纯干货](https://www.bilibili.com/video/BV11L411g7U1/)

[Docker 快速入门](https://docker.easydoc.net)

## Docker 简介

可以理解为一个轻量的虚拟机，它只虚拟你软件需要的运行环境，多余的一点都不要，而普通虚拟机则是一个完整而庞大的系统，包含各种不管你要不要的软件。

|特性|普通虚拟机|Docker|
|----|--------|------|
|跨平台|通常只能在桌面级系统运行，例如 Windows/Mac，无法在不带图形界面的服务器上运行|支持的系统非常多，各类 windows 和 Linux 都支持|
|性能|性能损耗大，内存占用高，因为是把整个完整系统都虚拟出来了|性能好，只虚拟软件所需运行环境，最大化减少没用的配置|
|自动化|需要手动安装所有东西|一个命令就可以自动部署好所需环境|
|稳定性|稳定性不高，不同系统差异大|稳定性好，不同系统都一样部署方式|

**打包、分发、部署**
1. **打包**：就是把你软件运行所需的依赖、第三方库、软件打包到一起，变成一个安装包
2. **分发**：你可以把你打包好的“安装包”上传到一个镜像仓库，其他人可以非常方便的获取和安装
3. **部署**：拿着“安装包”就可以一个命令运行起来你的应用，自动模拟出一摸一样的运行环境，不管是在 Windows/Mac/Linux。

**Docker 通常用来做什么**
1. 应用分发、部署，方便传播给他人安装。特别是开源软件和提供私有部署的应用
2. 快速安装测试/学习软件，用完就丢（类似小程序），不把时间浪费在安装软件上。例如 Redis / MongoDB / ElasticSearch / ELK
3. 多个版本软件共存，不污染系统，例如 Python2、Python3，Redis4.0，Redis5.0
4. Windows 上体验/学习各种 Linux 系统

**镜像**：可以理解为软件安装包，可以方便的进行传播和安装。
**容器**：软件安装后的状态，每个软件运行环境都是独立的、隔离的，称之为容器。

## 镜像加速源

![](Pics/docker016.png)

加速地址
1. Docker 中国官方镜像	https://registry.docker-cn.com
2. 科大镜像站	https://docker.mirrors.ustc.edu.cn
3. 腾讯云	https://mirror.ccs.tencentyun.com

## 用 Docker 快速安装软件

[Docker Hub](https://hub.docker.com/)

[docker container run 官方文档（docker docs）](https://docs.docker.com/reference/cli/docker/container/run/)

```bash
docker ps                        查看当前运行中的容器
docker images                    查看镜像列表
docker rm container-id           删除指定 id 的容器
docker stop/start container-id   停止/启动指定 id 的容器
docker rmi image-id              删除指定 id 的镜像
docker volume ls                 查看 volume 列表
docker network ls                查看网络列表
```



# 安装 Docker & Docker Desktop

## 官方安装教程

[Install Docker Desktop on Ubuntu - Docker官方](https://docs.docker.com/desktop/install/ubuntu/)
1. Set up Docker's package repository. See step one of Install using the apt repository.[Install Docker Engine on Ubuntu - Docker官方](https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository)
   1. Set up Docker's apt repository.
      ```bash
      # Add Docker's official GPG key:
      sudo apt-get update
      sudo apt-get install ca-certificates curl
      sudo install -m 0755 -d /etc/apt/keyrings
      sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
      sudo chmod a+r /etc/apt/keyrings/docker.asc

      # Add the repository to Apt sources:
      echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
      $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
      sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
      sudo apt-get update
      ```
   2. Install the Docker packages.
      ```bash
      sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
      ```
   3. Verify that the Docker Engine installation is successful by running the hello-world image.
      ```bash
      sudo docker run hello-world
      ```
2. Download latest DEB package.
3. Install the package with apt as follows:
   ```bash
   sudo apt-get update
   sudo apt-get install ./docker-desktop-<version>-<arch>.deb
   ```
4. config the proxy via docker-desktop which is same as the proxy of ubuntu (if using clash)
5. [Sign in to Docker Desktop](https://docs.docker.com/desktop/get-started/#credentials-management-for-linux-users)  -- "Unable to log in You must initialize pass"
   ```bash
   gpg --generate-key
   pass init xxxxxxx(between pub and uid)
   ```


## 测试与 Docker Hub 的连通性

方法1

```bash
curl -I https://hub.docker.com/

lzy@Razer:~ $ curl -I https://hub.docker.com/
HTTP/1.1 200 Connection established

HTTP/1.1 200 OK
date: Fri, 01 Mar 2024 06:45:05 GMT
content-type: text/html; charset=utf-8
x-xss-protection: 1; mode=block
x-docker-correlation-id: 72d388f1-4298-4511-8c0b-ceac191df541
x-docker-app-version: v3801.0.0
accept-ch: Sec-CH-Prefers-Color-Scheme
vary: Sec-CH-Prefers-Color-Scheme, Accept-Encoding
link: <https://hub.docker.com/>; rel="canonical"
server: nginx
x-frame-options: deny
x-content-type-options: nosniff
strict-transport-security: max-age=31536000
```

## 其他安装教程

```bash
sudo apt update                              # 升级 apt
sudo apt install docker.io docker-compose    # 安装docker
sudo usermod -aG docker ${USER}              # 将当前用户加入 docker组

# 测试
docker ps -a
docker run hello-world
```

## 常见问题

### docker run 命令需要 sudo，导致 vscode 中无法正常使用

```text
permission denied while trying to connect to the Docker daemon socket at unix:///var/run/docker.sock: Get "http://%2Fvar%2Frun%2Fdocker.sock/v1.24/containers/json?all=1": dial unix /var/run/docker.sock: connect: permission denied
```

解决方法

```bash
sudo chmod 666 /var/run/docker.sock
```

### vscode没有运行docker的permission

```bash
sudo groupadd docker             # 创建docker组，如果提示groupadd: group 'docker' already exists，表示这个组之前已经创建
sudo usermod -aG docker $USER    # 添加你的用户到docker组中
newgrp docker                    # 在终端中输入下面的命令更新组
```

### docker-desktop : Depends: docker-ce-cli but it is not installable

[Install using the apt repository - Docker官方](https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository)

```bash
sudo apt install -y ca-certificates curl gnupg lsb-release
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
```

### 无法登录 docker desktop

如果 ubuntu 系统配置了 network proxy，则 docker-desktop 也需要配置

![](Pics/docker006.png)

**注意 ！！！ 不要手贱把第二行的 http 改成 https**



# NVIDIA Container Toolkit 安装 - nvidia-docker

[NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/)

[Docker Hub nvidia/cuda Images](https://hub.docker.com/r/nvidia/cuda)

![](Pics/docker017.png)

The NVIDIA Container Toolkit enables users to build and run GPU-accelerated containers. The toolkit includes a container runtime library and utilities to automatically configure containers to leverage NVIDIA GPUs.

NVIDIA 容器工具包使用户能够构建和运行 GPU 加速的容器。该工具包包括一个容器运行时库和自动配置容器以利用 NVIDIA GPU 的实用程序。

## Installing the NVIDIA Container Toolkit

Installing with Apt
1. Configure the production repository
   ```bash
   curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
   && curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
   sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
   sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
   ```
2. Update the packages list from the repository && Install the NVIDIA Container Toolkit packages
   ```bash
   sudo apt update
   sudo apt install -y nvidia-container-toolkit
   ```

## Configuration

Configure the container runtime by using the nvidia-ctk command
```bash
sudo nvidia-ctk runtime configure --runtime=docker
```

Restart the Docker daemon:
```bash
sudo systemctl restart docker
```


## Docker Hub nvidia/cuda Images

[Docker Hub - nvidia/cuda Images](https://hub.docker.com/r/nvidia/cuda)

```bash
docker pull nvidia/cuda:12.3.2-base-ubuntu22.04

# --rm               Automatically remove the container when it exits
# --runtime string   Runtime to use for this container
# --gpus gpu-request GPU devices to add to the container ('all' to pass all GPUs)

lzy@Razer:/media/lzy/(main)$ sudo docker run --rm --runtime=nvidia --gpus all ubuntu nvidia-smi

Sun Mar  3 13:33:13 2024       
+---------------------------------------------------------------------------------------+
| NVIDIA-SMI 545.23.06              Driver Version: 545.23.06    CUDA Version: 12.3     |
|-----------------------------------------+----------------------+----------------------+
| GPU  Name                 Persistence-M | Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |         Memory-Usage | GPU-Util  Compute M. |
|                                         |                      |               MIG M. |
|=========================================+======================+======================|
|   0  NVIDIA GeForce GTX 1060 ...    On  | 00000000:01:00.0 Off |                  N/A |
| N/A   46C    P8               3W /  70W |      6MiB /  6144MiB |      0%      Default |
|                                         |                      |                  N/A |
+-----------------------------------------+----------------------+----------------------+
                                                                                         
+---------------------------------------------------------------------------------------+
| Processes:                                                                            |
|  GPU   GI   CI        PID   Type   Process name                            GPU Memory |
|        ID   ID                                                             Usage      |
|=======================================================================================|
+---------------------------------------------------------------------------------------+
```


## Running a Sample Workload

```bash
sudo docker run --rm --runtime=nvidia --gpus all ubuntu nvidia-smi
```




# Docker 三大版本

[docker的版本，你真的搞清楚了吗](https://zhuanlan.zhihu.com/p/305572519)

三大版本发展历史
1. docker.io
   1. 在 Docker 技术出现之前，Linux中已经有一个叫 docker 的工具，这个 docker 是一个窗口停靠栏程序
   2. Docker技术出来以后，由于在Linux系统中软件名不能与 docker 重名，而且那个时候 Docker 的官网是 http://docker.io，所以，就在软件名称上加了 io 的后缀
   3. 在 Ubuntu 中就是docker.io，在 CentOS 中就是docker-io
   4. 随着docker的发展，docker的名称虽然发生了三番五次的变化，但Ubuntu上的http://docker.io却一直在维护，它的版本也在不停地更新
2. docker-engine
   1. 后来随着 Docker 的发展，软件包名改成了 docker-engine，名称达到了统一
3. docker
   1. 再后来，随着 Docker 技术的火爆，Docker 容器技术的软件包名才正式成了 docker 这个名称，Docker软件包的名称又得到了一次统一
   2. docker-ce 社区版，免费
   3. docker-ee 商业版，收费

[Docker 三大版本区别](https://kms.app/archives/324/)

三个版本
1. docker.io
   1. debian/ubuntu 官方基于docker社区源码封装的版本,有时候比docker-ce版本还要新
   2. 特点是将docker的依赖直接转接到主系统上
2. docker-ce
   1. docker.com 放出来的社区版,仅维护源码
   2. 特点是使用golang将依赖封装在一个包中
3. docker-ee
   1. docker.com 维护的商业版,主要有以下三个级别:
      1. 基本:用于认证基础架构的Docker平台,得到Docker Inc.的支持以及来自Docker Store的认证容器和插件
      2. 标准:添加了高级映像和容器管理,LDAP / AD用户集成以及基于角色的访问控制.这些功能共同构成了Docker企业版
      3. 高级:添加Docker安全扫描和连续漏洞监控

docker-ce有一个致命缺陷-依赖: docker本身依赖成百上千个第三方依赖，理论上只要有一个依赖出问题就需要完全重新编译docker,否则会被各种hack:joy:反观 docker.io 将依赖托管给系统,只需要更新docker主程序即可

docker-ce不应该被用于任何期望稳定运行的产品中
推荐使用 docker.io 或者 docker-ee
在产品中使用docker-ce是极度不负责的行为
