# Yolo

[toc]

# Yolo V8

## Portals

[Yolo V8 Github 官网说明](https://github.com/ultralytics/ultralytics)

[Yolo V8 官方文档](https://docs.ultralytics.com/)

## Install

```bash
# Pip 安装包含所有 requirements 的 ultralytics 包，环境要求 Python>=3.7，且 PyTorch>=1.7 
pip install ultralytics

# YOLOv8 可以直接在命令行界面（CLI）中使用 yolo 命令运行  似乎会下载 一个bus图片 和 一个yolov8n.pt
yolo predict model=yolov8n.pt source='https://ultralytics.com/images/bus.jpg'

# yolo可以用于各种任务和模式，并接受额外的参数，例如 imgsz=640
python3 setup.py install

pip3 install -r requirements.txt
```

## Use

主要 使用 cfg 文件 进行 配置 

对于一个项目，可以创建多个 .cfg 文件，分别用于 train val predict 等等

```bash
yolo cfg=xxx.yaml
```

对于不同任务，model和data需要相应调整。以segmentation为例，model 和 data 需要使用 xxx-seg.yaml

## Mode

可选模式
1. Train: For training a YOLOv8 model on a custom dataset.  # 用自己的数据集训练模型
2. Val: For validating a YOLOv8 model after it has been trained.  # 用于验证训练好的模型
3. Predict: For making predictions using a trained YOLOv8 model on new images or videos.  # 用训练的模型进行预测
4. Export: For exporting a YOLOv8 model to a format that can be used for deployment.  # 导出方便部署的模型
5. Track: For tracking objects in real-time using a YOLOv8 model.  # 将模型用于实时追踪物体
6. Benchmark: For benchmarking YOLOv8 exports (ONNX, TensorRT, etc.) speed and accuracy.  # 

## Position

[dataset].yaml : ultralytics/datasets/coco128-seg.yaml

[network].yaml : ultralytics/models/v8/yolov8-seg.yaml

[cfg].yaml : ultralytics/yolo/cfg/testSeg.yaml

[datasetPos] : datasets/coco128-seg  当然可以自己设定

[network].pt : [project]/[name]/weights/last.pt


# Yolo V5

项目位置 /home/lzy/Project/yolov5

# 其他


**教程**

[yolov5 github 官方页面](https://github.com/ultralytics/yolov5)

[目标检测 YOLOv5 开源代码项目调试与讲解实战【土堆 x 布尔艺数】](https://www.bilibili.com/video/BV1tf4y1t7ru)

[《YOLOv5全面解析教程》九，train.py 逐代码解析](https://zhuanlan.zhihu.com/p/587808267)

[Train Custom Data yolov5 官网说明](https://docs.ultralytics.com/yolov5/train_custom_data/)

[Train Custom Data yolov8 官网说明](https://docs.ultralytics.com/modes/train/)


**工具**

[https://zhuanlan.zhihu.com/p/402114635](图像标注用的工具有哪些)

LabelImg，支持PASCAL VOC 格式和 YOLO 格式，在本机 conda 环境 label 中

Labelme，支持对象检测、图像语义分割数据标注。支持矩形、圆形、线段和点标注;支持视频标注;支持导出 VOC 与 COCO 格式数据实验分割



[cvat官网](https://www.cvat.ai/)

[cvat github 首页](https://github.com/opencv/cvat)