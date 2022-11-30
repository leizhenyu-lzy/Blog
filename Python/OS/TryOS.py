import os

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


