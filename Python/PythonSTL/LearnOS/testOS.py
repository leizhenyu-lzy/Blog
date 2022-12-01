import os
# file = os.getcwd()+"\\LearnOS.md"  # 注意要加上分隔符
# print(file)
# print(os.path.isfile(file))
# print(os.path.split(file))  # 进行切分('D:\\Project\\Blog\\Python', 'LearnOS.md')

# tempPath = os.getcwd()
# print(os.path.isfile(os.path.join(tempPath,"testOS.py")))

for roots,dirs,files in os.walk("."):
    print(roots,dirs,files)

