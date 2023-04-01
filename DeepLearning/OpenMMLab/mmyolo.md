# mmyolo

[MMYOLO github官网](https://github.com/open-mmlab/mmyolo)

[MMYOLO github官网文档](https://github.com/open-mmlab/mmyolo/blob/main/README_zh-CN.md)

[MMYOLO 中文说明文档](https://mmyolo.readthedocs.io/zh_CN/latest/get_started/overview.html)

[Roadmap of MMYOLO 开发计划](https://github.com/open-mmlab/mmyolo/issues/136)

[标注+训练+测试+部署全流程 官方文档](https://mmyolo.readthedocs.io/zh_CN/latest/recommended_topics/labeling_to_deployment_tutorials.html)

# 安装

[官方安装说明](https://mmyolo.readthedocs.io/zh_CN/latest/get_started/dependencies.html)

验证pytorch

```bash
python3 -c "import torch; print(torch.__version__); print(torch.cuda.is_available())"

1.13.1+cu117
True
```

```bash
pip install -U openmim
mim install "mmengine>=0.6.0"
mim install "mmcv>=2.0.0rc4,<2.1.0"
mim install "mmdet>=3.0.0rc6,<3.1.0"
```

有点怪，使用 mim install mmyolo 没有测试通过（没有输出结果），最后采用源码安装解决



# 【扫盲】MMYOLO部署&训练 B站

[【扫盲】MMYOLO部署&训练 B站](https://www.bilibili.com/video/BV1844y1R7QR/)

特征图可视化




# 玩转 MMYOLO 之基础篇 B站官方

## Portals

[玩转 MMYOLO 之基础篇（一）：配置文件全解读](https://www.bilibili.com/video/BV1214y157ck/)

## 玩转 MMYOLO 之基础篇（一）：配置文件全解读




