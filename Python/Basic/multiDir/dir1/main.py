# 直接引用子文件夹中的文件，需要知道内部结构

# from subDir1.func import hello as hello1
# from subDir2.func import hello as hello2

# if __name__ == "__main__":
#     hello1()  # hello from subDir1
#     hello2()  # hello from subDir2


# ---------------------------------------------------


# 引用作为包的子文件夹，不需要知道内部结构，因为有 __init__.py
# 以下两个 __init__.py 均可
# ① from subDir1.func import *
# ② from .func import *

import subDir1
import subDir2

if __name__ == "__main__":
    subDir1.hello()  # hello from subDir1
    subDir2.hello()  # hello from subDir2


