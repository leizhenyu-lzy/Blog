# OS

[toc]

# Portals

[Python基础之标准库os](https://www.bilibili.com/video/BV11A411e7oG/)

[]()


# Python基础之标准库os

## os标准库的主要功能
1. 系统相关变量和操作
2. 文件和目录相关操作
3. 执行命令和管理进程（执行exe等）

## 系统相关内容

```python
print(os.name)  # nt表示微软操作系统
print(os.environ)  # 环境变量（一堆）
print(os.sep)  # \ 分隔符
print(os.pathsep)  # ; path分隔符
print(os.linesep.__repr__())  # '\r\n'，使用__repr__()方法否则不方便查看

```


## 文件和目录相关

**文件操作**
```python
os.mkdir("testmkdir")  # 创建目录
os.rmdir("testmkdir")  # 删除目录
print(os.getcwd())  # 当前目录所在位置 D:\Project\Blog\Python\LearnOS

os.remove([filepath])  # 删除文件 
```

```python
# 绝对路径 __file__代表当前文件
dir1=os.path.dirname(__file__)  # d:\Project\Blog\Python\OS
print(dir1)
# 绝对路径
dir2=os.getcwd()  # d:\Project\Blog\Python\OS
print(dir2)

file1 = open('LearnOS.md', encoding='utf8')
content1 = file1.read()
print(content1)
file2 = open(r'D:\Project\Blog\Python\OS\LearnOS.md',encoding='utf8')
content2 = file2.read()
print(content2)
```

**子模块os.path**

**分离文件和路径**
```python
file = os.getcwd()+"/LearnOS.md"  # 注意要加上分隔符
print(os.path.split(file))  # 进行切分('D:\\Project\\Blog\\Python', 'LearnOS.md')

a, b = os.path.split(file)
print(a)  # D:\Project\Blog\Python\LearnOS
print(b)  # LearnOS.md
```

**对文件、文件夹进行基本判断**
```python
import os
import os.path

file1 = os.getcwd()+"/LearnOS.md"  # 注意要加上分隔符
file2 = os.getcwd()
file3 = "LearnOS.md"
file4 = "/LearnOS.md"
file5 = "./LearnOS.md"
# file3和file5在本次实验中结果完全一致

print("判断是否为绝对路径")
print(os.path.isabs(file1))  # True
print(os.path.isabs(file2))  # True
print(os.path.isabs(file3))  # False
print(os.path.isabs(file4))  # True
print(os.path.isabs(file5))  # False
# 有./和什么都没用都不会被认为是绝对路径

print("判断是否为文件")
print(os.path.isfile(file1))  # True
print(os.path.isfile(file2))  # False
print(os.path.isfile(file3))  # True
print(os.path.isfile(file4))  # False ？可能是被认为成了路径
print(os.path.isfile(file5))  # True

print("判断是否为文件夹")
print(os.path.isdir(file1))  # False
print(os.path.isdir(file2))  # True
print(os.path.isdir(file3))  # False
print(os.path.isdir(file4))  # False
print(os.path.isdir(file5))  # False
# 没有后缀

print("判断文件或文件夹是否存在")
print(os.path.exists(file1))  # True
print(os.path.exists(file2))  # True
print(os.path.exists(file3))  # True
print(os.path.exists(file4))  # False
print(os.path.exists(file5))  # True
# 相对和绝对都会检测
```

**得到文件的信息**

```python
file = os.getcwd()+"/LearnOS.md"  # 注意要加上分隔符
# 得到一个时间戳
print(os.path.getatime(file))  # 文件的最近访问时间
print(os.path.getctime(file))  # 文件属性最近修改的时间
print(os.path.getmtime(file))  # 文件的内容最近修改的时间

print(os.path.getsize(file))  # 得到文件大小
```

## 执行命令与管理进程

不推荐，有其他的标准库支持的更好

## os.walk

```python

for roots,dirs,files in os.walk("."):
    print(roots,dirs,files)
    


```