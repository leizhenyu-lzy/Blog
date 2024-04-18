# import pandas as pd
# import numpy as np
# import os.path
#
# root_dir = r"D:\Project\DataSet\WFLW\WFLW_annotations\list_98pt_rect_attr_train_test\list_98pt_rect_attr_test.txt"
# # print(os.path.exists(root_dir))  # True
#
# datas = pd.read_csv(filepath_or_buffer=root_dir, sep=" ", encoding="utf-8", header=None, index_col=206)  # utf8似乎也可以
# # print(datas.shape)  # (2499, 207)
# # print(datas)
# # print(datas.to_string())
# # print(datas.head().to_string())
# # print(datas.iloc[0, 0])
# list = datas.iloc[0,:]
# print(list)

import pandas as pd
import numpy as np

df1 = pd.DataFrame(np.ones((3, 4)) * 1, columns=['a', 'b', 'c', 'd'])
df2 = pd.DataFrame(np.ones((3, 4)) * 2, columns=['a', 'b', 'c', 'd'])
df3 = pd.DataFrame(np.ones((3, 4)) * 3, columns=['a', 'b', 'c', 'd'])

df = pd.concat(objs=[df1, df2, df3], axis=0, ignore_index=True)
# axis=0是竖着叠在一起，axis=1是横着拼在一起
# ignore_index是否忽略index重新从0赋值

print(df)

"""
     a    b    c    d
0  1.0  1.0  1.0  1.0
1  1.0  1.0  1.0  1.0
2  1.0  1.0  1.0  1.0
3  2.0  2.0  2.0  2.0
4  2.0  2.0  2.0  2.0
5  2.0  2.0  2.0  2.0
6  3.0  3.0  3.0  3.0
7  3.0  3.0  3.0  3.0
8  3.0  3.0  3.0  3.0
"""

# join功能
# outer,inner（默认outer）
# outer,两者进行拼接，数据缺失部分用NaN填充，不会重合
# join_axes = [df.index]
