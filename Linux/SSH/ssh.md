# SSH


# 保持 SSH 连接不断开

要保持 SSH 连接不断开，可以使用 SSH 的 KeepAlive 机制。KeepAlive 机制可以在 SSH 连接保持空闲状态时发送保活消息，防止连接因为长时间没有活动而被服务器断开。

## 命令行选项：使用 -o 选项设置 SSH KeepAlive 参数

```bash
ssh -o ServerAliveInterval=60 user@host

# 这将在 SSH 连接空闲 60 秒时发送保活消息
```


## SSH 配置文件：在 ~/etc/ssh/ssh_config 文件中添加

```bash
Host *  #这表示要让所有的ssh连接自动加上此属性，文件本身已经已经存在该字段
ServerAliveInterval 60  # 该配置将对所有 SSH 主机生效，当 SSH 连接空闲 60 秒时发送保活消息
```



# SSH 教程 (没看完)

[SSH 教程](https://www.cainiaojc.com/ssh/ssh-index.html)

## SSH 是什么

SSH 是 Linux 系统的登录工具，现在广泛用于服务器登录和各种加密通信。

SSH（Secure Shell 的缩写）是一种网络协议，用于加密两台计算机之间的通信，并且支持各种身份验证机制。

它主要用于保证远程登录和远程通信的安全，任何网络服务都可以用这个协议来加密。

历史上，网络主机之间的通信是不加密的，属于明文通信。这使得通信很不安全，一个典型的例子就是服务器登录。登录远程服务器的时候，需要将用户输入的密码传给服务器，如果这个过程是明文通信，就意味着传递过程中，线路经过的中间计算机都能看到密码，这是很可怕的。

SSH 就是为了解决这个问题而诞生的，它能够加密计算机之间的通信，保证不被窃听或篡改。它还能对操作者进行认证（authentication）和授权（authorization）。明文的网络协议可以套用在它里面，从而实现加密。

### SSH 架构

SSH 的软件架构是服务器-客户端模式（Server - Client）。在这个架构中，SSH 软件分成两个部分：向服务器发出请求的部分，称为客户端（client），OpenSSH 的实现为 ssh；接收客户端发出的请求的部分，称为服务器（server），OpenSSH 的实现为 sshd

```bash
lzy@legion:/etc/ssh$ ls
ssh_config  ssh_config.d

```

## SSH 客户端

### 简介

OpenSSH 的客户端是二进制程序 ssh。它在 Linux/Unix 系统的位置是 /usr/local/bin/ssh ，Windows 系统的位置是 \Program Files\OpenSSH\bin\ssh.exe

安装
```bash
sudo apt install openssh-client  # Ubuntu 和 Debian 
sudo dnf install openssh-clients  # CentOS 和 Fedora

ssh -V  # 查看版本  # OpenSSH_8.9p1 Ubuntu-3ubuntu0.1, OpenSSL 3.0.2 15 Mar 2022
```

### 基本用法

ssh 最常见的用途就是登录服务器，这要求服务器安装并正在运行 SSH 服务器软件

```bash
# ssh 登录服务器的命令
ssh hostname 
# hostname是主机名，它可以是域名，也可能是 IP 地址或局域网内部的主机名。不指定用户名的情况下，将使用客户端的当前用户名，作为远程服务器的登录用户名

# 如果要指定用户名，可以采用下面的语法，用户名和主机名写在一起了，之间使用@分隔
ssh user@hostname

# 用户名也可以使用ssh的-l参数指定，这样的话，用户名和主机名就不用写在一起了
ssh -l username host

# ssh 默认连接服务器的22端口，-p参数可以指定其他端口
ssh -p 8821 foo.com
```

### 连接流程

ssh 连接远程服务器后，首先有一个验证过程，验证远程服务器是否为陌生地址

如果是第一次连接某一台服务器，命令行会显示一段文字，表示不认识这台机器，提醒用户确认是否需要连接

```bash
lzy@legion:/etc/ssh$ ssh xxx@xx.xx.xx.xx
The authenticity of host 'xx.xx.xx.xx (xx.xx.xx.xx)' cant be established.
ED25519 key fingerprint is SHA256:Fb15i1NtPa+SG7fIKl3xG0+9gIEMn5TtN2vNLaKiSK4.
This key is not known by any other names
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes  

# 需要手动输入'yes'， 就可以将当前服务器的指纹也储存在本机~/.ssh/known_hosts文件中，并显示下面的提示。以后再连接的时候，就不会再出现警告了
Warning: Permanently added 'xx.xx.xx.xx' (ED25519) to the list of known hosts.
# 然后，客户端就会跟服务器建立连接。接着，ssh 就会要求用户输入所要登录账户的密码。用户输入并验证密码正确以后，就能登录远程服务器的 Shell 了。
```
上面这段文字告诉用户，这台服务器的指纹是陌生的，让用户选择是否要继续连接（输入 yes 或 no）

所谓“服务器指纹”，指的是 SSH 服务器公钥的哈希值。每台 SSH 服务器都有唯一一对密钥，用于跟客户端通信，其中公钥的哈希值就可以用来识别服务器

下面的命令可以查看某个公钥的指纹

```bash
ssh-keygen -l -f xxx.pub
```

ssh 会将本机连接过的所有服务器公钥的指纹，都储存在本机的~/.ssh/known_hosts文件中。每次连接服务器时，通过该文件判断是否为陌生主机（陌生公钥）


### 服务器密钥变更

服务器指纹可以防止有人恶意冒充远程主机。如果服务器的密钥发生变更（比如重装了 SSH 服务器），客户端再次连接时，就会发生公钥指纹不吻合的情况。这时，客户端就会中断连接，并显示一段警告信息

```bash
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@    WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!     @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
IT IS POSSIBLE THAT SOMEONE IS DOING SOMETHING NASTY!
Someone could be eavesdropping on you right now (man-in-the-middle attack)!
It is also possible that the RSA host key has just been changed.
The fingerprint for the RSA key sent by the remote host is
77:a5:69:81:9b:eb:40:76:7b:13:04:a9:6c:f4:9c:5d.
Please contact your system administrator.
Add correct host key in /home/me/.ssh/known_hosts to get rid of this message.
Offending key in /home/me/.ssh/known_hosts:36 
```

文字的意思是，该主机的公钥指纹跟~/.ssh/known_hosts文件储存的不一样，必须处理以后才能连接。这时，你需要确认是什么原因，使得公钥指纹发生变更，到底是恶意劫持，还是管理员变更了 SSH 服务器公钥。

如果新的公钥确认可以信任，需要继续执行连接，你可以执行下面的命令，将原来的公钥指纹从~/.ssh/known_hosts文件删除。

删除 公钥的指纹
```bash
ssh-keygen -R hostname  # hostname是发生公钥变更的主机名，除了使用上面的命令，你也可以手工修改known_hosts文件，将公钥指纹删除
# 删除了原来的公钥指纹以后，重新执行 ssh 命令连接远程服务器，将新的指纹加入known_hosts文件，就可以顺利连接了

lzy@legion:/etc/ssh$ ssh-keygen -f "/home/lzy/.ssh/known_hosts" -R "xx.xx.xx.xx"

# Host 10.184.12.37 found: line 4
# Host 10.184.12.37 found: line 5
/home/lzy/.ssh/known_hosts updated.
Original contents retained as /home/lzy/.ssh/known_hosts.old
```

### 执行远程命令

SSH 登录成功后，用户就进入了远程主机的命令行环境，所看到的提示符，就是远程主机的提示符。这时，你就可以输入想要在远程主机执行的命令。


