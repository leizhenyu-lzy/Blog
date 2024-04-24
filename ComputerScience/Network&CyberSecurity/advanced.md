# Advanced Network

---

# Table of Contents


---

# Network & Storage (RoCE & FC & NVMe & NoF)

## FC (Fibre Channel)

高速网络技术，主要用于连接计算机数据存储

通常用于SAN (Storage Area Network)，即存储区域网络，它允许多台服务器访问共享的存储设备

## NVMe (Non-Volatile Memory Express)

**NVMe** 是一种针对高速非易失性存储媒介(如SSDs，固态硬盘)的传输协议，用来充分利用固态硬盘的高性能

通过减少延迟和增加输入/输出操作的速度，来提升数据传输效率

**NVMe** 是通过 **PCI Express (PCIe)** 接口在主机硬件和固态存储设备之间传输数据

## NoF (NVMe over Fabrics)

NVMe over Fabrics
1. NVMe over FC - 最大化继承传统 FC 网络，复用网络基础设施
2. NVMe over TCP - 可以基于 现有 IP网络，在网络设施不变的情况下实现 端到端 NVMe
3. NVMe over RDMA
   1. NVMe over RoCE - 性能较好，兼具TCP优势(**主流**)

扩展了传统NVMe技术，使其能够在更广阔的网络中使用

不仅限于直连到主机的PCIe设备，NVMe协议现在可以通过各种网络技术(如Fibre Channel、Ethernet等)，跨越更远的距离进行操作

## RoCE (RDMA over Converged Ethernet) 

RoCE 是一种网络技术，**允许远程直接内存访问 (RDMA) 的操作在以太网网络上进行**

RDMA(Remote Direct Memory Access)，允许一台计算机直接从另一台计算机的内存中读取或写入数据，而无需经过操作系统和CPU的处理，从而显著减少延迟并提高数据传输速率

RoCE 使得这种高效的数据传输方式能够在传统的以太网基础设施上实现，从而增加了网络的灵活性和数据处理能力