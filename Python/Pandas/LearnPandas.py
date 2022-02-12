import pandas as pd
import numpy as np
import os.path

root_dir = r"D:\Project\DataSet\WFLW\WFLW_annotations\list_98pt_rect_attr_train_test\list_98pt_rect_attr_test.txt"
# print(os.path.exists(root_dir))  # True

datas = pd.read_csv(filepath_or_buffer=root_dir, sep=" ", encoding="utf-8", header=None)  # utf8似乎也可以
# print(datas.shape)  # (2499, 207)
# print(datas.to_string())

datas.to_csv("test_save.txt", sep=' ', header=None, index=False)

print(datas.head())
print(datas.tail())
print(datas.info())



