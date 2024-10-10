# Path

在 Python 中，使用相对路径写文件时，路径
1. 是 **相对于你执行 Python 脚本时的当前工作目录**
2. 而 不是 **相对于 `.py` 文件本身的路径**
3. eg : 如果你在命令行的 `/home/user/project/` 目录中运行 Python 脚本，即使 .py 文件位于 `/home/user/project/scripts/` 中，相对路径仍然是基于你运行命令的 `/home/user/project/` 目录

检查当前工作目录

```python
import os
print(os.getcwd())  # 打印当前工作目录
```

如果你想使用 `.py` 文件所在的目录作为相对路径的基础

```python
import os
scriptDir = os.path.dirname(os.path.abspath(__file__))  # 获取 .py 文件所在目录的绝对路径
relativePath = os.path.join(script_dir, 'your_file.txt')  # 在 .py 文件所在目录下创建相对路径
```



