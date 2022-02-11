import os.path

file = os.getcwd()+"/LearnOS.md"  # 注意要加上分隔符
print(os.path.getatime(file))  # 修改时间 1644554556.019328
print(os.path.getctime(file))  # 创建时间 1644552058.818725
print(os.path.getmtime(file))  # 创建时间 1644552058.8187253
print(os.path.getsize(file))