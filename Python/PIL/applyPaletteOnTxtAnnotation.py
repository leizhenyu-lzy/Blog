import os.path as osp
import numpy as np
from PIL import Image


if __name__ == "__main__":
    classes = ('sky', 'tree', 'road', 'grass', 'water', 'bldg', 'mntn', 'fg obj')
    palette = [[128, 128, 128], [129, 127, 38], [120, 69, 125], [53, 125, 34], 
            [0, 11, 123], [118, 20, 12], [122, 81, 25], [241, 134, 51]]
    
    annoPath = "/home/lzy/Project/mmsegmentation_old/demo/iccv09Data/labels/0000047.layers.txt"
    oriPicPath = "/home/lzy/Project/mmsegmentation_old/demo/iccv09Data/images/0000047.jpg"
    savePath = "/home/lzy/Project/Blog/Python/PIL/result.png"

    annoArray = np.loadtxt(annoPath).astype(np.uint8)
    annoImg = Image.fromarray(annoArray).convert('P')
    annoImg.putpalette(np.array(palette, dtype=np.uint8))
    annoImg.save(savePath)


# import os.path as osp
# import numpy as np
# from PIL import Image

# # convert dataset annotation to semantic segmentation map
# data_root = 'iccv09Data'
# img_dir = 'images'
# ann_dir = 'labels'

# # define class and plaette for better visualization 定义类别名和调色板
# classes = ('sky', 'tree', 'road', 'grass', 'water', 'bldg', 'mntn', 'fg obj')
# palette = [[128, 128, 128], [129, 127, 38], [120, 69, 125], [53, 125, 34], 
#            [0, 11, 123], [118, 20, 12], [122, 81, 25], [241, 134, 51]]

# # 将标注调整为mmseg支持的图片格式
# for file in mmcv.scandir(osp.join(data_root, ann_dir), suffix='.regions.txt'):
#   seg_map = np.loadtxt(osp.join(data_root, ann_dir, file)).astype(np.uint8)  # np.loadtxt是NumPy库中的一个函数，用于从文本文件中加载数据到NumPy数组中。它支持从各种文件类型（例如.csv、.txt等）中加载数据，并且可以根据需要指定分隔符、行数、列数等参数。使用np.loadtxt函数可以方便地将文本文件中的数据读取到NumPy数组中进行处理和分析。
#   seg_img = Image.fromarray(seg_map).convert('P')  # Image.fromarray是Python PIL库（Python Imaging Library）中的一个函数，用于将NumPy数组或Python列表中的数据转换为PIL图像对象。该函数接受一个NumPy数组或Python列表作为输入，然后根据数组中的数据创建一个相应的图像对象，并返回一个Image类型的对象。-----使用Image.fromarray函数时需要确保输入的数组具有正确的形状和数据类型，以便正确地创建相应的图像对象。否则可能会出现错误或不正确的图像。-----Image.convert('P')是Python PIL库（Python Imaging Library）中的一个方法，用于将图像对象转换为8位调色板模式（8-bit palette mode）。在调色板模式下，图像使用一个固定的颜色调色板来表示图像中的所有像素。这种模式通常用于处理具有有限颜色空间的图像，以减少内存使用和加速图像处理。
#   seg_img.putpalette(np.array(palette, dtype=np.uint8))  # Image.putpalette是Python PIL库（Python Imaging Library）中的一个方法，用于设置调色板（palette）的值。调色板是一个包含256个颜色的列表，用于在调色板模式下表示图像中的像素。在调色板模式下，每个像素的值都是一个指向调色板中颜色的索引。-----请注意，在调色板模式下，每个像素的值都是一个指向调色板中颜色的索引。因此，如果调色板中的颜色不合适，图像可能会出现颜色不正确的情况。使用putpalette方法时，应该仔细选择调色板的颜色，以确保图像的质量和正确性。
#   seg_img.save(osp.join(data_root, ann_dir, file.replace('.regions.txt', 'png')))