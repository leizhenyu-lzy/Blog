# import os

# print("conda 环境列表")
# os.system("conda env list")

# print("conda torch 版本")
# os.system("conda list | grep torch")

import os
os.system("conda env list & conda list | grep torch")
