

[廖雪峰 - Git 教程](https://liaoxuefeng.com/books/git/introduction/index.html)


Installation & Configuration
```bash
sudo apt install git

git --version

# --global 表示这台机器上所有的Git仓库都会使用这个配置
git config --global user.name "Your Name"
git config --global user.email "email@example.com"
git config --list
```

Git 是 分布式版本控制系统，所以 每个机器 都必须自报家门

创建版本库
```bash
cd <local_repository>
git init  # 把这个目录变成Git可以管理的仓库
# 新增 .git 目录(默认隐藏) Git来跟踪管理版本库的
```

所有的版本控制系统(包括 Git)，其实只能跟踪 文本文件的 改动，比如 TXT文件、网页、程序代码 等

而图片、视频这些二进制文件，虽然也能由版本控制系统管理，但没法跟踪文件的变化

如果要真正使用版本控制系统，就要以纯文本方式编写文件

强烈建议使用标准的`UTF-8`编码，所有语言使用同一种编码，既没有冲突，又被所有平台所支持

千万不要使用 Windows 自带的 记事本 编辑任何文本文件

Git命令必须**在Git仓库目录内执行**


```bash
git add <filePath>  # 可以多次add不同的文件
git commit -m "comment"  # commit可以一次提交很多文件
```

```bash
git status  # 掌握仓库当前的状态
git diff <filePath>
```

`git diff`
1. 不支持直接比较未跟踪文件 (untracked files)
2. 只比较以下几种情况
   1. 工作区(working directory) 与 暂存区(staging area) 之间的差异
   2. 暂存区(staging area) 与 最后一次提交(HEAD) 之间的差异
   3. 工作区或暂存区 与 指定提交(如 HEAD) 的差异



