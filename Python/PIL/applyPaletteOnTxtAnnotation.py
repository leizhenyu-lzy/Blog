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