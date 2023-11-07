# Git Credential Manager

[toc]

[Git 工具 - 凭证存储 --- Git官网](https://git-scm.com/book/zh/v2/Git-%E5%B7%A5%E5%85%B7-%E5%87%AD%E8%AF%81%E5%AD%98%E5%82%A8)


# git credential helper 让你的 https 不再需要输入用户名密码

[git credential helper 让你的 https 不再需要输入用户名密码](https://blog.csdn.net/ustccw/article/details/84591578)

在使用版本管理 git 时, 如果使用 https 连接, 通常要求你输入 username & password

那么如何可以不用每次都输入 username & password 呢?
1. 采用 SSH 连接方式，前提当然你得有权限将自己主机 id_rsa.pub 加入到 git 账户的 SSH Keys 中
2. 采用 HTTPS 连接方式，只要你有仓库访问权限即可, 使用本文即将介绍的 credential 来配置一下即可




# 必知必会之Git Windows credential.helper

[必知必会之Git Windows credential.helper](https://zhuanlan.zhihu.com/p/157751660)

[必知必会之Git-Windows凭据管理器](https://zhuanlan.zhihu.com/p/157607438)

查询当前凭证存储模式

```bash
git config credential.helper
```

可以设置 Git 的配置来选择上述的一种方式

```bash
git config --global credential.helper xxxx
```

```bash
git config --unset credential.helper
```


![](Pics/credential001.png)

可选凭证存储模式
1. **wincred 模式**
2. **cache 模式**
   1. 会将凭证存放在内存中一段时间
   2. 密码永远不会被存储在磁盘中，并且在15分钟后从内存中清除
3. **store 模式**
   1. 会将凭证用明文的形式存放在磁盘中，并且永不过期
   2. 这意味着除非你修改了你在 Git 服务器上的密码，否则你永远不需要再次输入你的凭证信息
   3. 缺点是你的密码是用明文的方式存放在你的 home 目录下 
   4. 保存至home目录下的.git-credentials文件，内容 :
      ```
      https://userName:pwd@github.com
      ```
4. **osxkeychain 模式**
   1. 如果你使用的是 Mac，Git 还有一种 osxkeychain 模式
   2. 会将凭证缓存到你系统用户的钥匙串中
   3. 这种方式将凭证存放在磁盘中，并且永不过期，但是是被加密的，这种加密方式与存放 HTTPS 凭证以及 Safari 的自动填写是相同的
5. **manager 模式**
   1. 若安装Git时安装了GitGUI，自动会在system级别中设置credential.helper为manager
   2. 如果你使用的是 Windows，可以安装一个叫做 Git Credential Manager for Windows 的辅助工具
   3. 这和上面说的 osxkeychain 十分类似，但是是使用 Windows Credential Store 来控制敏感信息


在这里对比 "wincred" 和 "manager"的区别
1. 相同点 : 都会将用户信息存储到Windows凭据管理器中
2. 不同点 : Windows凭据管理器中用户信息是否加密
   1. "wincred" 模式下的用户信息展示如下
    ```
    Internet 地址或网络地址：git:https://用户名@github.com； 
    用户名：真实用户名 
    ```
   2. "manager" 模式下的用户信息展示如下
    ```
    Internet 地址或网络地址：git:https://github.com； 
    用户名：PersonalAccessToken 
    ```
3. 很明显，在用户信息暴露的情况下，其他人很容易通过 https://用户名@http://github.com 访问到路径对应的项目，为了避免这种风险的存在，我们可以安装 “Git Credential Manager for Windows” 的辅助工具。

[Git Credential Manager for Windows 下载网址 --- Github](https://github.com/microsoft/Git-Credential-Manager-for-Windows/releases)

![](Pics/credential003.png)

![](Pics/credential004.png)

安装完后，再次通过指令查询，可以知道凭证存储模式已经由默认的"wincred"修改为"manager"

修改了凭证存储模式后，原先存储的用户信息依旧是"wincred"模式下的，需要删除后重新输入

可以前往Windows凭据管理器中进行删除

