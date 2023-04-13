# mmcv

[MMCV github 官網](https://github.com/open-mmlab/mmcv)

[MMCV 教程](https://mmcv.readthedocs.io/)

[手撸OpenMMlab系列教程(mmcv，mmsegmentation)](https://www.bilibili.com/video/BV1ub4y187DP)

# 深入理解 MMCV-1.7.1

[MMCV 核心组件分析（一）：整体概述 --- 官方知乎博客](https://zhuanlan.zhihu.com/p/336081587)

## mmcv & mmcv-full

![](Pics/mmcv001.png)

## [Config 配置](https://mmcv.readthedocs.io/zh_CN/v1.7.1/understand_mmcv/config.html)

[MMCV 核心组件分析(四): Config --- 官方知乎博客](https://zhuanlan.zhihu.com/p/346203167)


## [Registry 注册器](https://mmcv.readthedocs.io/zh_CN/v1.7.1/understand_mmcv/registry.html)

[MMCV 核心组件分析(五): Registry --- 官方知乎博客](https://zhuanlan.zhihu.com/p/355271993)

MMCV 使用 注册器 来管理具有相似功能的不同模块

在MMCV中，注册器可以看作类或函数到字符串的映射。 一个注册器中的类或函数通常有相似的接口，但是可以实现不同的算法或支持不同的数据集。 借助注册器，用户可以通过使用相应的字符串查找类或函数，并根据他们的需要实例化对应模块或调用函数获取结果。




