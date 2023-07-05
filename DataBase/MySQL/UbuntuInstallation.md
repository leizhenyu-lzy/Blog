# ubuntu 安装 mysql

[Ubuntu下安装MySQL数据库](https://www.bilibili.com/video/BV12q4y1U7sZ/)

## 安装

```bash
sudo apt update

sudo apt install mysql-server
```

## 设置 root 密码

**安全设置 mysql_secure_installation 前先设置 root 密码**

[mysql_secure_installation 报错解决方案 : MySQL root password setup error](https://askubuntu.com/questions/1406395/mysql-root-password-setup-error/1406673#1406673)

```bash
sudo mysql

ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password by 'your new password';  # 输入自己新设置的密码
```

如下所示

```bash
lzy@legion:~$ sudo mysql
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 18
Server version: 8.0.33-0ubuntu0.22.04.2 (Ubuntu)

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password by 'xxxxxx';
Query OK, 0 rows affected (0.03 sec)

mysql> exit
Bye
```

## root 登录方式

```bash
sudo mysql -u root -p  # 以后使用该命令登录并输入密码
```

```bash
mysql> show schemas;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
| sys                |
+--------------------+
4 rows in set (0.01 sec)
```

## sudo mysql_secure_installation 设置


```bash
sudo mysql_secure_installation
```

无需更改为 root 用户设置的密码，删除匿名用户，不禁用root远程链接，移除测试数据库，重载privilege tables让设置立刻生效

## 查看 mysql server 是否正在运行

```bash
lzy@legion:~$ systemctl status mysql.service

```


# ubuntu 安装 dbeaver

```bash
sudo snap install dbeaver-ce
```

安装位置

```bash
/snap/dbeaver-ce
```