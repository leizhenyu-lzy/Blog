#  Hardware

[toc]


# 拓展坞 - Dcoking Station




# 内存

内存品牌只代表售后服务，决定品质的是内存颗粒(黑色)

大多数内存品牌没有生产制造内存颗粒的能力，从上游厂商购买

各个厂商都有高中低档产品
1. 三星
2. 海力士
3. 镁光
4. 长鑫

高频率内存一定使用好颗粒

使用场景
1. 游戏 - 对内存频率敏感的游戏并不多 - 当显卡不行，内存频率影响不大，内存成为瓶颈 - 内存数据频繁更换
2. 工作 - 更用不上高频 - 像剪视频、建模等都是初始一次性导入很多数据，后续长时间对该数据简单调整

内存超频存在一定风险，可能导致不能稳定运行，甚至无法进入系统

不要轻易动内存电压，可能造成硬件损坏

内存频率越高，时钟周期越短 (内存频率越高越好，时序越低越好)

内存通达 - 内存控制器和内存之间数据交换通道数 - 受CPU中内存控制器限制
1. 双通道 - 大多数平台 - 基本上足够了
2. 四通道 - 大吞吐量 - 线程撕裂者、X299才会支持

## DDR4 & DDR5

![](Pics/hardware026.png)

同频率的 DDR4 读写性能约等于 DDR5

相同频率，时序越低，延迟越低

DDR4 延迟相对较低

![](Pics/hardware027.png)


# 硬盘

三大种类
1. 固态硬盘 - SSD - solid state drive
2. 混合硬盘 - HHD - hybrid hard drive
3. 传统硬盘 - HDD - hard disk drive


## 固态硬盘 SSD

[M.2、SATA、PCI-E、NVMe都是啥？看看这个就知道了 - 啃芝士](https://www.bilibili.com/video/BV1cx411X7xA/)

[【硬核科普】硬盘的SATA M.2 NGFF NVME是什么意思，详解硬盘的总线、协议与接口 - 硬件茶谈](https://www.bilibili.com/video/BV1Qv411t7ZL/)

[【拯点攻略】2021拯救者全系笔记本内存更换&硬盘加装教程](https://www.bilibili.com/video/BV1RL4y1E7t8/)

[三款性价比PCIe 4.0 SSD对比测试：三星980 PRO、WD_BLACK SN770、致态TiPlus7100](https://zhuanlan.zhihu.com/p/596718372)

![](Pics/hardware008.png)

总线、协议、接口 需要匹配

读取、写入 设备速率要匹配

耐用问题 - 闪存颗粒 - 概率问题 - 大品牌售后好(三星、西数、闪迪、铠侠、金士顿、英睿达)

按接口
1. SATA - Serial Advanced Technology Attachment - 接口 & 通道
   1. 与目前市面上的机械硬盘在接口方面没有区别，一个供电接口一个数据接口
   2. 最常见的接口类型之一，使用串行ATA技术
   3. 兼容传统硬盘接口，易于升级
   4. 速度受限于SATA标准，最高理论传输速率为6 Gb/s (SATA III)
2. mSATA - Mini-SATA
   1. 尺寸比传统SATA SSD更小，但使用的是SATA协议，因此速度相似
   2. 已被更小型且支持更高速度的M.2接口取代
3. M.2 - 物理接口
   1. 直接插到主板接口上并用螺丝固定
   2. 一种小型化的接口规格，可以跑**SATA和PCIe通道**，M.2插槽可以支持基于SATA和基于PCIe的设备，这意味着一个M.2插槽可能兼容多种类型的SSD
   3. M.2 SSDs可通过**PCIe通道**提供更高的速度，特别是当配合**NVMe协议**时
   4. 适合笔记本和紧凑型设备，具有不同长度和宽度的规格
   5. 插槽两种类型 - B型 & M型 - 有些固态硬盘两种插槽都支持（两个缺口） - M型支持更高的总线标准(拿到一个m key的ssd，就可以直接判定它是支持nvme的，拿到一个b&m key的ssd则无法判定，我只能说绝大多数b&m key都是不支持nvme协议的)
      ![](Pics/hardware003.png)
      ![](Pics/hardware009.png)
      ![](Pics/hardware010.png)
   6. 长度多种规格 - eg : 2280 = 22mm×88mm
      ![](Pics/hardware004.png)
4. PCIe - Peripheral Component Interconnect Express - 接口 & 通道
   1. 桌面级SSD的顶级产品
   2. 既是一种接口标准，也涉及到协议的概念
   3. 高速接口，直接连接到主板的PCIe插槽
   4. 提供比SATA更高的数据传输速率，特别是在使用NVMe协议时
   5. 用于高端和性能要求高的应用场景

按颗粒类型
1. SLC - Single-Level Cell
   1. 每个存储单元存储1位数据 - 每个单元只需要区分两种状态（0或1），使得电子擦写和重写的过程对存储介质的损耗最小
   2. 优点：最快的读写速度、最高的耐用性、最长的使用寿命
   3. 缺点：成本最高，每GB存储空间的价格最贵
   4. 用途：高端企业级应用，需要极高的性能和可靠性
2. MLC - Multi-Level Cell
   1. 每个存储单元存储2位数据 - 需要区分四种状态（00、01、10、11），这增加了读写错误的概率，并通过更频繁的擦写周期加速了介质的磨损
   2. 优点：较好的速度和耐用性，成本低于SLC
   3. 缺点：速度和耐用性低于SLC，寿命较短
   4. 用途：企业级和高端消费级市场
3. TLC - Triple-Level Cell
   1. 每个存储单元存储3位数据 - 区分八种状态，比MLC更复杂，因此在相同的物理空间内可以存储更多数据，成本更低。但这也导致每个单元的耐用性进一步降低，因为需要更精细的电压控制和更频繁的擦写周期
   2. 优点：存储密度高，制造成本低
   3. 缺点：相较于SLC和MLC，读写速度慢，耐用性和寿命较低
   4. 用途：主流消费级市场，平衡性能和成本

按传输协议
1. AHCI - Advanced Host Controller Interface - 协议
   1. 主要用于SATA接口的一种旧协议，虽然主要与HDDs相关联，但也适用于SSD
2. NVMe - Non-Volatile Memory Express - 协议
   1. 一种优化的协议，**专为SSD通过PCIe接口设计**，提高速度和效率
   2. 提供极低的延迟和高IOPS（输入/输出操作每秒）

协议 protocol : 电脑内部的规矩，规定两设备通讯时：

设备间协议一致或者相容(compatibility)才能通讯

![](Pics/hardware011.png)

![](Pics/hardware012.png)


对普通用户购买建议是优先购买大厂**M.2接口**支持**NVMe协议**走PCIe总线的TLC颗粒产品

![](Pics/hardware001.png)

SATA & NVMe 对比
1. 走SATA协议的M.2 SSD会被连接到南桥的SATA port上，在其上走传统的AHCI协议栈（SCSI的一个子集），漫长而延迟很高。AHCI只有1个命令队列，队列深度32，如果发生大量小文件操作，就会发生拥堵。
2. 走NVMe的SSD，直接走PCIe通道，协议栈很浅。而NVMe可以有65535个队列，每个队列都可以深达65536个命令。NVMe也充分使用了MSI的2048个中断向量优势，延迟大大减小，尤其大量小文件时速度更是飞快。

![](Pics/hardware002.png)

AHCI还是基于传统的块传输。而NVMe使用了一种叫做“Doorbell”的机制来充分利用了极长的队列，大大减小了延迟。


## [【硬核科普】硬盘的SATA M.2 NGFF NVME是什么意思，详解硬盘的总线、协议与接口 - 硬件茶谈](https://www.bilibili.com/video/BV1Qv411t7ZL/)

### 协议-总线-接口 总图

![](Pics/hardware008.png)

**常用接口**
1. 民用：SATA、mSATA、SATA Express、M.2(B-Key & M-Key)、PCIe
2. 企业：U.2、 SAS

其中，**PCIe 总线的硬盘之间的接口大部分可以相互转换**

![](Pics/hardware025.png)


SATA 3.0 普及较广

![](Pics/hardware017.png)

$6Gbps × 8/10 = 6/8 GB/s × 8/10 = 0.6 GB/s = 600 MB/s$

PCIe 3.0 4.0 普及较广 (PCIe 带宽和长度有关)

![](Pics/hardware018.png)

SAS 3.0 普及较广

![](Pics/hardware019.png)

$12Gbps × 8/10 = 12/8 GB/s × 8/10 = 1.2 GB/s$



### SATA 接口

使用 SATA 总线，AHCI 协议

![](Pics/hardware014.png)

民用 2.5寸机械硬盘、3.5寸机械硬盘、2.5寸固态硬盘 使用的都是该接口

![](Pics/hardware015.png)

SATA 接口 分为两部分
1. 供电 - 接驳在电脑电源上
2. 数据 - SATA数据线接驳在主板上

速度上限 600 MB/s

### mSATA 接口

使用 SATA 总线，AHCI 协议

诞生目的 - 给SATA接口的固态缩小体积

![](Pics/hardware016.png)

速率没有提升，没有前瞻性的提供高带宽，只是单纯的减少体积，因此在 M.2 接口普及后就消失了

### SATA Express 接口

PCIe × 2 总线，可以走 AHCI协议 或 NVMe协议

![](Pics/hardware020.png)

不够前瞻性，接口体积过于庞大，后被tao'tai

### M.2 接口 (别名 NGFF)

![](Pics/hardware021.png)

走 SATA 总线 AHCI 协议，则和普通的 SATA 硬盘没有区别，速率限制在 500 MB/S

可以走 PCIe 总线， AHCI 协议 或 NVMe 协议，速率上限由 PCIe 版本 和 长度 决定

最常见的组合是 PCIe + NVMe

M.2 接口
1. B-Key(Socket2，豁口在左)，支持 SATA 总线 和 PCIe * 2
2. M-Key(Socket3，豁口在右)，支持 SATA 总线 和 PCIe * 4

无法通过外形判断支持什么协议

### PCIe 接口

PCIe 可以作为总线、传输通道，也可也以接口形式存在

![](Pics/hardware022.png)

目前直接以 PCIe 为接口的固态硬盘常见于超高性能等级以及企业级固态硬盘上，民用级固态硬盘还是以 M.2 为主

### SAS 接口

SAS 总线、SCSI协议，服务器上用的较多，可以理解为强化版 SATA 接口

SAS 总线可以 一分多，以满足服务器硬盘柜多硬盘要求

![](Pics/hardware023.png)

由于直接在 SATA 接口上改款而来，**SAS 接口** 可以向下兼容 SATA 硬盘，走 AHCI

而 SAS 硬盘本身是 SAS 总线，SCSI 协议

### U.2 接口

在 SAS 接口上继续改款

![](Pics/hardware023.png)

兼容 SAS、SATA

额外提供 PCIe × 4 总线 支持






# 主板

主板 和 CPU 需要匹配，与机箱

尺寸
1. ATX - 大板 - 7条PCIe
2. MATX - 4条PCIe
3. ITX - 1条PCIe

价格区别
1. 供电 - 主板CPU供电
   1. 供电相数越多，每一相承载的电流越少，发热量低，供电稳定
   2. 供电原件质量
2. 扩展性
   1. 内存条插槽数量
   2. PCIe插槽数量
   3. PCIe插槽速度
   4. M.2接口数量
   5. SATA接口数量
   6. 背板接口数量
      1. 视频输出 - HDMI、DP (显示器应该连在独显上，而非主板上)
      2. USB、Type-C、电口
      3. 网口
      4. 音频
      5. WiFi
      6. 蓝牙
   7. 风扇供电接口数量
   8. RGB接口数量
3. BIOS - Basic Input Output System
   1. 对于普通用户没啥用




# 南桥 & 北桥

通过高速总线(如 DMI、HyperTransport)连接起来，形成了整个系统的芯片组架构

两个主要芯片
1. 北桥 - NorthBridge
   1. 负责处理与 CPU 直接通信的高速组件，比如内存控制器、PCI Express 总线、显卡接口等。
   2. 随着技术的发展，现代处理器已经集成了内存控制器和 PCIe 控制器，因此北桥的作用逐渐减弱。
2. 南桥 - SorthBridge
   1. 负责处理与 CPU 间接通信的低速组件，如硬盘接口（SATA、IDE）、USB、网卡、音频接口等。
   2. 通常也包含了一些辅助功能，如电源管理、时钟、GPIO（通用输入输出）等。