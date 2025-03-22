# Shell

---

## Table of Contents

- [Shell](#shell)
  - [Table of Contents](#table-of-contents)
- [配置 SHELL](#配置-shell)
  - [查看 SHELL](#查看-shell)
  - [终端补全忽略大小写](#终端补全忽略大小写)
  - [Git 高亮显示](#git-高亮显示)

---

# 配置 SHELL

## 查看 SHELL

查看当前 SHELL

```bash
lzy@legion:~ $ echo $SHELL
/bin/bash
```

查看系统支持的 SHELL

```bash
lzy@legion:~ $ cat /etc/shells
# /etc/shells: valid login shells
/bin/sh
/bin/bash
/usr/bin/bash
/bin/rbash
/usr/bin/rbash
/usr/bin/sh
/bin/dash
/usr/bin/dash
```

```bash
sudo apt install wget git curl vim -y
```

## 终端补全忽略大小写


```bash
# 在/etc/inputrc中添加使全局所有用户生效
echo 'set completion-ignore-case on' >> /etc/inputrc

# 对于个别用户，则可以在用户home目录下添加
echo 'set completion-ignore-case on' >> ~/.inputrc
```

## Git 高亮显示

[如何在 shell 下显示 git分支](../ComputerScience/Git/GitInShell.md)





