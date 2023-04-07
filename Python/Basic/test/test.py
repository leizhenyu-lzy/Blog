import sys
print("sys.argv[0]                  ", sys.argv[0])

import os
print("os.path.dirname(__file__)    ", os.path.dirname(__file__))
print("os.path.abspath(sys.argv[0]) ", os.path.abspath(sys.argv[0]))
print("os.getcwd()                  ", os.getcwd())  #获取当前工作目录路径
print("os.path.abspath('.')         ", os.path.abspath('.'))  #获取当前文件目录路径
print("os.path.abspath('test.txt')  ", os.path.abspath('test.txt'))  #获取当前目录文件下的文件目录路径
print("os.path.abspath('..')        ", os.path.abspath('..'))  #获取当前文件目录的父目录 ！注意是父目录路径
print("os.path.abspath(os.curdir)   ", os.path.abspath(os.curdir)) #获取当前文件目录路径

filePath = os.path.abspath(sys.argv[0])  #  文件真实路径
print(os.path.exists(filePath))


# 当前文件位置 /home/lzy/Project/Blog/Python/Basic/test/test.py

# 在 ~/Project/Blog/Python/Basic 目录下运行 python3 test/test.py
# sys.argv[0]                   test/test.py
# os.path.dirname(__file__)     /home/lzy/Project/Blog/Python/Basic/test
# os.path.abspath(sys.argv[0])  /home/lzy/Project/Blog/Python/Basic/test/test.py
# os.getcwd()                   /home/lzy/Project/Blog/Python/Basic
# os.path.abspath('.')          /home/lzy/Project/Blog/Python/Basic
# os.path.abspath('test.txt')   /home/lzy/Project/Blog/Python/Basic/test.txt
# os.path.abspath('..')         /home/lzy/Project/Blog/Python
# os.path.abspath(os.curdir)    /home/lzy/Project/Blog/Python/Basic
# True

# 在 ~/Project/Blog/Python/Basic/test 目录下运行 python3 test.py
# sys.argv[0]                   test.py
# os.path.dirname(__file__)     /home/lzy/Project/Blog/Python/Basic/test
# os.path.abspath(sys.argv[0])  /home/lzy/Project/Blog/Python/Basic/test/test.py
# os.getcwd()                   /home/lzy/Project/Blog/Python/Basic/test
# os.path.abspath('.')          /home/lzy/Project/Blog/Python/Basic/test
# os.path.abspath('test.txt')   /home/lzy/Project/Blog/Python/Basic/test/test.txt
# os.path.abspath('..')         /home/lzy/Project/Blog/Python/Basic
# os.path.abspath(os.curdir)    /home/lzy/Project/Blog/Python/Basic/test
# True

