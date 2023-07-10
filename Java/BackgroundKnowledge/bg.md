# Background Knowledge

**目录**
[toc]

# OpenJDK & OracleJDK

```bash
lzy@legion:~$ java -version 
openjdk version "11.0.19" 2023-04-18
OpenJDK Runtime Environment (build 11.0.19+7-post-Ubuntu-0ubuntu122.04.1)
OpenJDK 64-Bit Server VM (build 11.0.19+7-post-Ubuntu-0ubuntu122.04.1, mixed mode, sharing)

lzy@legion:~$ javac -version
javac 11.0.19
```

# JAVA_HOME directory in Linux

## 获取 JDK 可执行文件（Java 编译器）的位置

```bash
lzy@legion:~$ $(dirname $(dirname $(readlink -f $(which javac))))
bash: /usr/lib/jvm/java-11-openjdk-amd64: Is a directory

lzy@legion:~$ echo $(dirname $(dirname $(readlink -f $(which javac))))
/usr/lib/jvm/java-11-openjdk-amd64

lzy@legion:~$ which javac  # 在这里的问题是，它给出的位置实际上是一个 符号链接
/usr/bin/javac

lzy@legion:~$ readlink -f `which java`
/usr/lib/jvm/java-11-openjdk-amd64/bin/java
lzy@legion:~$ readlink -f `which javac`
/usr/lib/jvm/java-11-openjdk-amd64/bin/javac

# readlink 命令会跟随一个符号链接。我在 which java 的外侧使用 readlink 将会使用 which java 的输出来替换要检查的符号链接，这被称之为命令替换
```

## 设置 JAVA_HOME 变量

[在 Ubuntu Linux 中正确地设置 JAVA_HOME 变量 --- 知乎](https://zhuanlan.zhihu.com/p/429757891)

设置 JAVA_HOME 变量，将其写在 **~/.bashrc** 文件中

```bash
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64/bin/java
```

```bash
lzy@legion:~/Project/Blog$ echo $JAVA_HOME
/usr/lib/jvm/java-11-openjdk-amd64/bin/java
```

现在，即使你退出会话或重新启动系统，JAVA_HOME 环境变量都仍将设置为你所具体指定的值

## 不知道有没有用的命令

```bash
lzy@legion:~$ sudo update-alternatives --config java
[sudo] password for lzy: 
There is only one alternative in link group java (providing /usr/bin/java): /usr/lib/jvm/java-11-openjdk-amd64/bin/java
Nothing to configure.
```


# java vscode

[【教程】VScode中配置Java运行环境](https://www.bilibili.com/video/BV1eB4y127Cy/)




# 其他相关知识

## 常用DOS命令

常用DOS命令
1. dir
2. md
3. rd
4. cd
5. cd..
6. cd\
7. del
8. exit