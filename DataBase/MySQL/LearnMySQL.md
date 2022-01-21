![](Pics/icon.png)

# MySQL

[toc]

## Portals

[尚硅谷 MySQL数据库](https://www.bilibili.com/video/BV1iq4y1u7vj)

current

## 数据库概述与MySQL

### 数据库简介

**为什么使用数据库**
1. 持久化 persistence 将数据存储到硬盘加以“固化”
2. 持久化的主要作用是将内存中的数据存储在关系型数据库中
3. 存储在数据库中而不存储在文件中，因为数据库的结构可以更复杂，支持的类型多种多样（大文本、图片、字符串），同时可以存储的数据量更大。（条目数、丰富度）

**数据库相关概念**
1. 数据库：DB Database：存储数据的仓库，文件系统
2. 数据库管理系统 DBMS Database Management System：操纵管理数据库的软件
3. 结构化查询语言 SQL Structured Query Language：与数据库通信的语言

![](Pics/Fundamental/fund_sql001.png)

**常见数据库管理系统**
1. Oracle（商用 Relational RDBMS 关系型 不开源）
2. MySQL
   1. 开源的关系型数据库管理系统
   2. 支持大学数据库
   3. 支持多种编程语言
3. MongoDB
4. Microsoft SQL Server
5. Redis
6. PostgreSQL


**RDBMS和非RDBMS**

Relational,Document,Key-Value,Search Engine

RDBMS（主流）
1. 将复杂的数据结构归结为二维表格形式
2. 按照行row和列column的形式存储数据，一系列行和列称为表，一组表组成一个库database
3. 表与表之间的数据记录有关系。现实世界中的各种实体之间的各种联系均用**关系模型**来表示。
4. 便于复杂查询、事务支持（多线程安全性）

非RDBMS
1. RDBMS的阉割版本（“舍得”）
2. 基于键值对存储数据，不需要经过SQL层的解析
3. 减少不常用功能，进一步提高性能
4. 种类
   1. 键值型 Redis
   2. 文档型 MongoDB 可以存放获取文档，可以是XML、JSON格式
   3. 搜索引擎 Solr 核心：“倒排索引”
   4. 列式存储、行式存储 HBase 降低系统I/O
   5. 图形型 存储图形关系的数据库

### 关系型数据库设计规则
1. 典型数据结构：**数据表**（结构化的）
2. 将数据放在表中，表放在库中
3. 数据库中有多个表，表有自己的名字用于标识
4. 表具有特性，定义了数据在表中如何存储（**类**）

**表、记录、字段**

E-R模型 entity-relationship：实体集、属性、联系集

ORM思想（Object Relational Mapping）：数据库中的一个表table对应于一个实体集（类class），表中的一条数据（一行row）对应类的对象（实体instance、记录record），表中的一列column对应类中的属性attribute（字段field）。

![](Pics/Fundamental/fund_sql002.png)

**表的关联关系**

四种：一对一、一对多、多对多（包括多对一）、自我引用

1. 一对一关系：实际应用不多，因为可以创建成一张表，但是为了节省I/O和内存占用，从设计上应该分拆为常用和不常用。
2. 一对多关系：客户订单表、分类商品表、部门员工表。主表、从表。
3. 多对多关系：必须创建第三个表（**联结表**），将多对多关系划分为两个一对多关系。多对多体现在联结表中。通过联结表关联。
   ![](Pics/Fundamental/fund_sql003.png)
4. 自我引用（Self Reference）：员工的主管也是公司员工，也有自己的主管

### MySQL环境搭建

四个MySQL位置
1. 软件安装位置
2. 数据库位置
3. 服务
4. 环境变量

**MySQL的卸载**
1. 停止MySQL服务
2. 卸载软件，通过windows控制面板或其他软件或使用自身的Installer卸载
3. 数据文件不会随着软件的卸载而被删除，自行决定删除或保留
4. 删除环境变量
5. 可能需要删除服务和注册表（8.0版本不需要手动删除注册表，其他版本可能需要regedit）
6. 重启电脑

**MySQL的下载、安装、配置**

官方提供MySQL Workbench图形界面管理工具

[MySQL官网下载](https://dev.mysql.com/downloads/mysql/)

![](Pics/Fundamental/fund_sql004.png)

推荐下载.msi文件而不是.zip，这样可以省去安装后的配置步骤。

如果需要历史版本，点击Archives即可

安装时双击.msi文件，选择custom

![](Pics/Fundamental/fund_sql005.png)

选择需要添加的组件，选中右侧方框中的组件，并点击Advanced Options进行软件安装位置和文件存储位置的配置。（路径中不要有中文）

![](Pics/Fundamental/fund_sql006.png)

选择Config Type为Development Computer。端口号尽量不要修改，但是如果安装多个版本，则需要手动修改。

![](Pics/Fundamental/fund_sql007.png)

之后，设置Root用户密码

一路继续

最后还需要配置环境变量，将安装软件位置中bin的文件夹位置添加进环境变量即可。

```
查看version

mysql --version

登录数据库

mysql -u[root] -p[Password]

password可以不直接在中括号中写

退出数据库
quit
```
```
如果想要访问不同版本的数据库，可以通过端口号

mysql -u[root] -P[Port] -p
```

```
想要访问其他ip下的数据库

mysql -u[root] -P[Port] -hlocalhost -p

mysql -u[root] -P[Port] -h127.0.0.1 -p

mysql -u[root] -P[Port] -h[要访问的数据库ip] -p
```

**MySQL的登录**
1. 服务的启动与停止
   1. 使用图形化界面，在服务中启动与停止
   2. 用管理员运行cmd，然后net start/stop mysql80
2. 自带客户端的登录与推出
   1. MySQL自带的命令行工具
   2. Windows的命令行工具

**MySQL的常见操作**

![](Pics/Fundamental/fund_sql008.png)

```
show databases;
查看databases
```

四个自带的数据库服务器
1. information_schema 保持数据库服务器的系统信息、名称、存储权限
2. mysql 运行时的系统信息、字符集
3. performance_schema 监控性能指标
4. sys 存储性能指标

![](Pics/Fundamental/fund_sql009.png)

```
create database [dbname];
创建名为[dbname]的数据库
```

![](Pics/Fundamental/fund_sql010.png)
```
use [dbname];
使用名为[dbname]的数据库
show tables;
查看正在使用中的数据库中的所有表格
```

![](Pics/Fundamental/fund_sql011.png)
```
create table [tablename(...)]
创建table，并指定其参数类型
```

![](Pics/Fundamental/fund_sql012.png)
```
select * from [tablename];
查看所有数据
```

![](Pics/Fundamental/fund_sql014.png)
```
insert into [tablename] values(...);
插入一条数据（可重复）
8.0版本values中可以出现中文，而5.7等版本不行，因为字符集问题
```

![](Pics/Fundamental/fund_sql013.png)

![](Pics/Fundamental/fund_sql015.png)

![](Pics/Fundamental/fund_sql016.png)

![](Pics/Fundamental/fund_sql017.png)
```
show create table [tablename];
show create database [dbname];
show variables like 'character_%';
show variables like 'collation_%';
可以查看字符集
```

![](Pics/Fundamental/fund_sql018.png)

若要修改字符集，在my.ini中修改[mysql]和[mysqld]中的default即可。my.ini在数据库数据位置。再重启服务

![](Pics/Fundamental/fund_sql019.png)
```
drop databases [dbname]
删除数据库
```
### 图形化管理工具

1. Workbench
2. Navicat
3. SQLyog
4. DBeaver

使用MySQL8.0版本在设置时，由于使用高级加密方式导致使用GUI工具连接不上，如下图所示

![](Pics/Fundamental/fund_sql020.png)

解决方案：

```
use mysql;

ALTER USER 'root'@'locolhost' IDENTIFIED WITH mysql_native_password BY '[yourpassword]';

FLUSH PRIVILEGES;
```



## SQL之select使用



## DDL、DML、DCL使用

## 其他数据库对象

## MySQL8.0其他新特性

## MySQL

## 索引及调优 

##

