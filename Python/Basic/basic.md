# 基础知识

[toc]

# 语法糖 Syntactic Sugar

[Python中常用的九种语法糖](https://www.bilibili.com/video/BV1Nf4y1k7Pu/)

常用的9种
1. 交换两个变量的值 a,b=b,a
2. 判断变量是否在某个范围内 if a<=b<=c:
3. 格式化输出字符 print("#"*10)
4. 列表拼接 a=[1,2,3] b=[4,5,6] a+b
5. 列表切片 a=[1,2,3,4,5,6] b=a[1:-2] c=a[:3] d=a[-3:]
6. 打包&解包 a=(1,2,3) x,y,z=a
7. with语句 with open("xxx","xx") as file: data=f.read() 会自动关闭文件以及处理异常
8. 列表推导式 a=[1,2,3,4] b=[i+233 for i in a]
9. 数字分隔符 a=1_0000_0000



# 路径 虚拟环境

[路径 虚拟环境 poetry依赖管理](https://www.bilibili.com/video/BV1cX4y1Z7kv/)

查看版本 python3 --version

```
lzy@legion:~$ python3 --version
Python 3.10.6
```

```
lzy@legion:~$ which python3
/usr/bin/python3
```

对于linux自带的python
1. 解释器 位置 : /usr/bin
   ```bash
    lzy@legion:~$ ls /usr/bin/ | grep python
    activate-global-python-argcomplete3
    dh_python3-ply
    pvtkpython
    pybabel-python3
    python3
    python3.10
    python3.10-config
    python3.10-coverage
    python3-config
    python3-coverage
    python3-futurize
    python3-pasteurize
    python-argcomplete-check-easy-install-script3
    python-argcomplete-tcsh3
    register-python-argcomplete3
    vtkpython-9.0
    x86_64-linux-gnu-python3.10-config
    x86_64-linux-gnu-python3-config
   ```
2. 使用 pip3 安装第三方库的默认路径 位置 : /home/lzy/.local/lib/python[版本号]/site-packages
   ```bash
    lzy@legion:~/Project/Blog$ python3
    Python 3.10.6 (main, Nov 14 2022, 16:10:14) [GCC 11.3.0] on linux
    Type "help", "copyright", "credits" or "license" for more information.
    >>> import sys
    >>> sys.path
    ['', '/opt/ros/humble/lib/python3.10/site-packages', '/opt/ros/humble/local/lib/python3.10/dist-packages', '/usr/lib/python310.zip', '/usr/lib/python3.10', '/usr/lib/python3.10/lib-dynload', '/home/lzy/.local/lib/python3.10/site-packages', '/usr/local/lib/python3.10/dist-packages', '/usr/lib/python3/dist-packages']
   ```

使用conda激活虚拟环境，相应的python版本也随之改变

```bash
(opencv3.4.2) lzy@legion:/usr/lib/python3.10$ python3 --version
Python 3.6.13 :: Anaconda, Inc.
```


```python
import sys

print("path_prefix                  :", sys.prefix)  # python解释器路径前缀
print("path of current interpreter  :", sys.executable)  # 当前解释器的路径
print("search packages from         :", sys.path)  # 寻找依赖的路径
```

```bash
(opencv3.4.2) lzy@legion:~/Project/Blog$ conda deactivate
lzy@legion:~/Project/Blog$ python3 ./Python/Basic/basic.py 
path_prefix                  : /usr
path of current interpreter  : /usr/bin/python3
search packages from         : ['/home/lzy/Project/Blog/Python/Basic', '/opt/ros/humble/lib/python3.10/site-packages', '/opt/ros/humble/local/lib/python3.10/dist-packages', '/usr/lib/python310.zip', '/usr/lib/python3.10', '/usr/lib/python3.10/lib-dynload', '/home/lzy/.local/lib/python3.10/site-packages', '/usr/local/lib/python3.10/dist-packages', '/usr/lib/python3/dist-packages']
lzy@legion:~/Project/Blog$ conda activate opencv3.4.2
(opencv3.4.2) lzy@legion:~/Project/Blog$ python3 ./Python/Basic/basic.py 
path_prefix                  : /home/lzy/miniconda3/envs/opencv3.4.2
path of current interpreter  : /home/lzy/miniconda3/envs/opencv3.4.2/bin/python3
search packages from         : ['/home/lzy/Project/Blog/Python/Basic', '/opt/ros/humble/lib/python3.10/site-packages', '/opt/ros/humble/local/lib/python3.10/dist-packages', '/home/lzy/miniconda3/envs/opencv3.4.2/lib/python36.zip', '/home/lzy/miniconda3/envs/opencv3.4.2/lib/python3.6', '/home/lzy/miniconda3/envs/opencv3.4.2/lib/python3.6/lib-dynload', '/home/lzy/miniconda3/envs/opencv3.4.2/lib/python3.6/site-packages']
(opencv3.4.2) lzy@legion:~/Project/Blog$ 
```

