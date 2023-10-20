# 如何在 Linux 的 Shell 下显示当前 Git 分支

[toc]

[如何在Linux下显示当前git分支](https://zhuanlan.zhihu.com/p/133291342)


修改 "~/.bashrc" 文件

考虑到有的目录下可能并不存在git项目，所以需要做是否为空的判断，也要注意处理标准错误。因此将获取git分支信息的部分写成一个shell函数

在 "~/.bashrc" 文件 最后添加

```bash
git_branch()
{
   branch=`git rev-parse --abbrev-ref HEAD 2>/dev/null`
   if [ "${branch}" != "" ]
   then
       if [ "${branch}" = "(no branch)" ]
       then
           branch="(`git rev-parse --short HEAD`...)"
       fi
       echo "($branch)"
   fi
}
```

然后修改 "~/.bashrc" 文件中的 PS1 部分 (# 注释的是原始的样式)

```bash
if [ "$color_prompt" = yes ]; then
    # PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '
    PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w \[\033[35m\]$(git_branch)\[\033[00m\]\$ '
else
    # PS1='${debian_chroot:+($debian_chroot)}\u@\h:\w\$ '
    PS1='${debian_chroot:+($debian_chroot)}\u@\h:\w$(git_branch)\$ '
fi
```

我为此添加了紫红色 用于区分

```bash
\[\033[35m\]$(git_branch)
```

也可以替换其他颜色

```text
前景色 背景色  
30      40      黑色
31      41      红色
32      42      绿色
33      43      黄色
34      44      蓝色
35      45      紫红色
36      46      青蓝色
37      47      白色
```

vscode terminal 的最终效果

![](Pics/shell01.png)

