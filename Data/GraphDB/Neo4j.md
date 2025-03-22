![](Pics/graph000.svg)

# Neo4j


[Neo4j - Official Website](https://neo4j.com/)

[Neo4j - Github](https://github.com/neo4j/neo4j)

**[Neo4j Docs](https://neo4j.com/docs/)**

[Neo4j Sandbox](https://sandbox.neo4j.com/)

---

## Table of Contents

- [Neo4j](#neo4j)
  - [Table of Contents](#table-of-contents)
- [Overview](#overview)
- [Neo4j DBMS](#neo4j-dbms)
  - [Welcome](#welcome)
  - [Get Started](#get-started)
  - [Model Data for Neo4j](#model-data-for-neo4j)
  - [Import Data into Neo4j](#import-data-into-neo4j)
  - [Query Neo4j Database](#query-neo4j-database)
  - [Connect to Neo4j](#connect-to-neo4j)
  - [Data Science with Neo4j](#data-science-with-neo4j)
  - [Visualize Data with Neo4j](#visualize-data-with-neo4j)
- [Neo4j Desktop](#neo4j-desktop)
  - [Install](#install)
  - [Visual Tour](#visual-tour)
- [Neo4j Desktop 操作](#neo4j-desktop-操作)
  - [Neo4j Desktop](#neo4j-desktop-1)
  - [本地 Neo4j-Browser (对应 单个 DBMS)](#本地-neo4j-browser-对应-单个-dbms)
  - [网页 Neo4j-Browser (对应 单个 DBMS)](#网页-neo4j-browser-对应-单个-dbms)
- [Neo4j x Python](#neo4j-x-python)
- [Cypher](#cypher)
- [Generative AI](#generative-ai)
- [Neo4j Operations Manual v5](#neo4j-operations-manual-v5)
  - [Installation](#installation)
  - [Remote Connection](#remote-connection)
  - [Docker \& Kubernetes](#docker--kubernetes)
  - [Configuration](#configuration)
- [Install](#install-1)
  - [Neo4j](#neo4j-1)
  - [Neo4j Desktop](#neo4j-desktop-2)
  - [Neo4j AuraDB](#neo4j-auradb)
- [Problem Shooting](#problem-shooting)
  - [01 Unsupported Java Version](#01-unsupported-java-version)
  - [02 Neo4j Start Failure](#02-neo4j-start-failure)


---

# Overview

[Neo4j in 100 Seconds](https://www.youtube.com/watch?v=T6L9EoBy8Zk)

CRUD - **Create Read Update Delete**

**Acid compliant** (描述数据库事务正确性的术语)
1. **A**tomicity 原子性 - 所有操作要么全部成功，要么全部失败。如果事务中的某个操作失败，整个事务将被回滚
2. **C**onsistency 一致性 - 事务必须将数据库从一个有效状态转换到另一个有效状态。事务完成后，所有数据规则都必须应用于数据库数据，确保数据的正确性和完整性
3. **I**solation 隔离性 - 发执行的事务之间必须是隔离的，事务的执行不应互相干扰，每个事务都应该独立于其他事务运行
4. **D**urability 持久性 - 一旦事务被提交，对数据库的修改就是永久性的，即使系统发生故障也不会丢失

RelationalDB -> **Tabular Model**(表格模型)

GraphDB -> **Property Graph Model**(属性图模型)
1. node -> **entity**
2. edge -> **relationship**
3. property -> **Key-Value Pair**

创始人 - **Emil Eifrem**

Neo4j 核心数据库引擎 用 **Java** 编写

查询 & 编程 语言 - **Cypher**(声明式图形查询语言)

![](Pics/neo4j004.png)

**项目结构**(三个层次 - Project、DBMS、Database)

```text
Project: My Project
├── DBMS Instance: DBMS1
│   ├── Database: DatabaseA
│   ├── Database: DatabaseB
│   └── Database: DatabaseC
└── DBMS Instance: DBMS2
    ├── Database: DatabaseX
    ├── Database: DatabaseY
    └── Database: DatabaseZ
```
![](Pics/neo4j012.png) ![](Pics/neo4j013.png)

可以安装插件(第一个不知道咋用)

![](Pics/neo4j005.png)

`Ctrl` + `Shift` + `p` & neo4j

---


# Neo4j DBMS

[Neo4j DBMS](https://neo4j.com/docs/getting-started) - Learn about graph database concepts, introduce yourself to Cypher, and find useful resources.

## Welcome

![](Pics/neo4j006.png)

节点保存 direct pointer 无需 index

graph database takes a **property graph** approach

beneficial for both **traversal performance**(遍历性能) and **operations runtime**(运行时)

dedicated **memory management** and **memory-efficient operations**

**Neo4j Graph Database** is the core product
1. Community Edition (**CE**)
2. Enterprise Edition (**EE**)

**Neo4j AuraDB** is a graph database as a service

## Get Started

## Model Data for Neo4j

## Import Data into Neo4j

## Query Neo4j Database

## Connect to Neo4j




## Data Science with Neo4j

## Visualize Data with Neo4j

---

# Neo4j Desktop

[Neo4j Desktop - Neo4j Docs](https://neo4j.com/docs/desktop-manual/current/)

## Install

[Install Neo4j Desktop](#neo4j-desktop-1)

Software requirement - **Ubuntu 22.04**

Proxy Setup

![](Pics/neo4j007.png)


## Visual Tour

[Visual Tour](https://neo4j.com/docs/desktop-manual/current/visual-tour/)

![](Pics/neo4j008.png)

# Neo4j Desktop 操作

## Neo4j Desktop

![](Pics/neo4j016.png)



## 本地 Neo4j-Browser (对应 单个 DBMS)

通过 Desktop -> Project -> DBMS -> Open -> Neo4j Browser 进入

![](Pics/neo4j015.png)

功能 和 网页端 一样

![](Pics/neo4j017.png)


## 网页 Neo4j-Browser (对应 单个 DBMS)

网页端打开 DBMS 管理平台

> [127.0.0.1:7474](http://127.0.0.1:7474/browser/) - 不是 driver 要用的 URI (本地打开了那个 DBMS 就显示 哪个 DBMS 的内容)

![](Pics/neo4j014.png)

功能 和 本地端 一样





---

# Neo4j x Python

[Using Neo4j from Python](https://neo4j.com/docs/getting-started/languages-guides/neo4j-python/)

[Build applications with Neo4j and Python](https://neo4j.com/docs/python-manual/current/)

[Building Neo4j Applications with Python](https://graphacademy.neo4j.com/courses/app-python/)


```bash
pip3 install neo4j
```

> The **Driver** object is immutable, **thread-safe**, **application-wide** & **fairly expensive to create**

> The **Driver** API is **topology independent**, can run the same code against a **Neo4j cluster** or a **single DBMS**.

**Driver 对应 DBMS实例**，database 的选择在 session 中控制

Neo4j Driver 支持语言
1. Python
2. Java
3. JavaScript
4. DotNet
5. Go

```python
with self.driver.session(database=database) as session:
    result = session.run(query, parameters)
```

![](Pics/neo4j012.png)


```python
from neo4j import GraphDatabase

# URI examples: "neo4j://localhost", "neo4j+s://xxx.databases.neo4j.io"
URI = "<URI for Neo4j database>"
AUTH = ("<Username>", "<Password>")

with GraphDatabase.driver(URI, auth=AUTH) as driver:
    driver.verify_connectivity()
```

可以采用更安全的 URI、USER、PASSWORD 方式，需要 `.env` 文件


```python
import os
from dotenv import load_dotenv
load_dotenv()

NEO4J_URI=os.getenv('NEO4J_URI')
NEO4J_USERNAME=os.getenv('NEO4J_USERNAME')
NEO4J_PASSWORD=os.getenv('NEO4J_PASSWORD')

with GraphDatabase.driver(uri=NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD)) as driver:
    driver.verify_connectivity()  # 检查链接
```

如果没有使用 **with** 代码块，则需要 手动 **driver.close()**

**scheme**
1. neo4j, neo4j+s, neo4j+ssc
2. bolt,  bolt+s,  bolt+ssc

![](Pics/neo4j011.png)

**Connection String** 结构

![](Pics/neo4j010.png)

**Session**
1. Session 是 **与数据库交互的会话**，提供了一种上下文，用于执行查询、事务和管理连接的生命周期
2. **每个 Session 是独立的**，提供了一种隔离机制，确保不同的会话之间互不影响
3. 功能
   1. 执行查询 - 执行 Cypher 查询，读取或写入数据
   2. 管理事务 - 显式事务的支持，可以在一个事务中执行多个查询，并在事务结束时提交或回滚
   3. 链接管理 - 管理与数据库的连接，确保连接的生命周期与会话一致

**`driver.execute_query`** 方法实际上是一个高层次的辅助方法，它会在内部自动创建一个 **会话 session**，执行查询并处理结果，简化在单次操作中使用会话和事务的过程

**`driver.execute_query`** 中 configuration parameters are suffixed(后缀) with _
1. Database selection - `database_="neo4j"`
2. Request routing(cluster environment) - `routing_="r"`
3. Transform query result - `result_transformer_`
   1. Result as a list
   2. Transform to pandas DataFrame
   3. Transform to graph



```python
with GraphDatabase.driver(uri=NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD)) as driver:
    # DB Property
    records, summary, keys = driver.execute_query(
        database_="neo4j",
        query_="CALL db.propertyKeys()")
    for record in records:
        print(record.data())
    # SET Label
    labels = "Teacher"
    records, summary, keys = driver.execute_query(
        database_="neo4j",
        # Neo4j 不允许在 SET 子句中使用参数来设置标签
        query_=f"MATCH (p:Person{{name:$name}}) \
            SET p:{labels} \
            RETURN p", name="Alice")
    for record in records:
        print(record.data())
        print(record)
    # ADD Relationship
    records, summary, keys = driver.execute_query(
        database_="neo4j",
        query_="MERGE (p1:Person{name:$name1})\
            MERGE (p2:Person{name:$name2})\
            MERGE (p1)-[:Knows]->(p2)\
            RETURN p1, p2", name1="lzy", name2="Alice")
    for record in records:
        print(record.data())
        print(record)
    # DELETE
    records, summary, keys = driver.execute_query(
        database_="neo4j",
        query_="MATCH (p:Person)\
            WHERE p.name=$name\
            DETACH DELETE p",
        name="alice")
    for record in records:
        print(record.data())
```

**Query Parameters** - Do not hardcode or concatenate parameters directly into queries, use placeholders and specify the Cypher parameters
1. **performance** benefits
2. protect against **Cypher injection注入**
   ```cypher
   CREATE (s:Student)
   SET s.name = 'Robby'
   // 用于将查询的上下文(变量&结果)传递给后续的查询部分
   WITH true as ignored  // 并没有传递有用的数据
   MATCH (s:Student) DETACH DELETE s;
   //'; // 注释掉任何后续的代码，确保注入的删除操作能顺利执行
   ```

[parameterized querying - 参数化查询](https://neo4j.com/docs/cypher-manual/current/syntax/parameters/)
1. 字面量 和 表达式
2. 节点和关系的 ID

**Neo4j 不允许在 SET 子句中使用参数来设置标签**

**参数不能用于**
1. **property keys**
   ```cypher
   MATCH (n) WHERE n.$param = 'something'
   ```
2. **relationship types**
   ```cypher
   MATCH (n)-[:$param]→(m)
   ```
3. **labels**
   ```cypher
   MATCH (n:$param)
   ```

```cypher
// String literal
{
  "name": "John"
}
MATCH (n:Person)
WHERE n.name = $name
RETURN n

MATCH (n:Person {name: $name})
RETURN n

// Regular expression
{
  "regex": ".*h.*"
}
MATCH (n:Person)
WHERE n.name =~ $regex
RETURN n.name

// Create node with properties
{
  "props": {
    "name": "Andy",
    "position": "Developer"
  }
}
CREATE ($props)

// Create multiple nodes with properties
{
  "props": [ {
    "awesome": true,
    "name": "Andy",
    "position": "Developer"
  }, {
    "children": 3,
    "name": "Michael",
    "position": "Developer"
  } ]
}

UNWIND $props AS properties
CREATE (n:Person)
SET n = properties
RETURN n

// Setting all properties on a node
{
  "props": {
    "name": "Andy",
    "position": "Developer"
  }
}
MATCH (n:Person)
WHERE n.name = 'Mike'
SET n = $props

// Multiple node ids
{
  "ids" : [ "4:1fd57deb-355d-47bb-a80a-d39ac2d2bcdb:0", "4:1fd57deb-355d-47bb-a80a-d39ac2d2bcdb:1" ]
}
MATCH (n)
WHERE elementId(n) IN $ids
RETURN n.name
```

**`class neo4j.EagerResult(records, summary, keys)`**
1. **records** - list of records returned by the query (list of Record objects)
2. **summary** - summary of the query execution (ResultSummary object)
3. **keys** - list of keys returned by the query (see AsyncResult.keys and Result.keys)







**Sandbox Credentials**
```bash
Browser URL
https://070ba802c8a8d909e1ecb0aafed466fd.neo4jsandbox.com/browser/
--------------------
Bolt URI
bolt://44.204.38.141:7687
--------------------
Websocket Bolt URI
bolt+s://070ba802c8a8d909e1ecb0aafed466fd.neo4jsandbox.com:7687
--------------------
Username
neo4j
--------------------
Password
pails-opinions-fluids
```

[clone the repository](https://github.com/neo4j-graphacademy/app-python)













---


# Cypher

[Cypher](https://neo4j.com/docs/cypher-manual) - Learn about Cypher; the graph query language for Neo4j and AuraDB.

[Cypher Cheat Sheet](https://neo4j.com/docs/cypher-cheat-sheet)

[Cypher Personal Note - 个人笔记](./Cypher.md)


---

# Generative AI

[Generative AI](https://neo4j.com/docs/genai/) - Learn how to integrate Neo4j with Generative AI models.


---



# Neo4j Operations Manual v5

```bash
lzy@legion:~ $ neo4j --version
5.19.0
```

## Installation

[Installation - Neo4j](https://neo4j.com/docs/operations-manual/current/installation/)

[Installation - Local Note(Ubuntu22.04)](#install)


## Remote Connection

Procedure
1. the remote instance needs to be started
2. configuration setting
    ```bash
    server.default_listen_address=0.0.0.0=true
    ```
3. the firewall on your remote instance allows inbound connections to the defined bolt port (by default: 7687)


## Docker & Kubernetes

[Docker - Neo4j](https://neo4j.com/docs/operations-manual/current/docker/)

[Kubernetes - Neo4j](https://neo4j.com/docs/operations-manual/current/kubernetes/)

## Configuration


---



# Install

## Neo4j

[Deployment Center - Neo4j](https://neo4j.com/deployment-center/#community)

[Linux installation - Neo4j Official Operations Manual](https://neo4j.com/docs/operations-manual/current/installation/linux/)

[Download and install - Neo4j Official](https://neo4j.com/docs/desktop-manual/current/installation/download-installation/)

[Debian-based distributions (.deb) - Neo4j Official](https://neo4j.com/docs/operations-manual/current/installation/linux/debian/)

```bash
# Neo4j是基于Java的图形数据库，因此必须安装JAVA的JDK
# add the official OpenJDK package repository to apt
sudo add-apt-repository -y ppa:openjdk-r/ppa
sudo apt-get update
sudo apt install openjdk-21-jdk

# Dealing with multiple installed Java versions
# must configure your default Java version to point to Java 17, or Neo4j 5.19.0 will be unable to start
update-java-alternatives --list

# add the repository
# Debian package is available from https://debian.neo4j.com
wget -O - https://debian.neo4j.com/neotechnology.gpg.key | sudo apt-key add -
echo 'deb https://debian.neo4j.com stable latest' | sudo tee -a /etc/apt/sources.list.d/neo4j.list
sudo apt-get update

sudo add-apt-repository universe

sudo apt install maven
sudo apt install neo4j  # community
```

## Neo4j Desktop

Neo4j 一个图形用户界面应用程序

[Download Neo4j Desktop - Neo4j Official](https://neo4j.com/download/)

![](Pics/neo4j001.png)

填个人信息后，浏览器自动下载 .AppImage 并 提供 **Neo4j Desktop Activation Key**

```bash
sudo chmod +x ~/Tools/Neo4j/neo4j-desktop-1.5.9-x86_64.AppImage
```

双击即可打开

创建快捷方式

```bash
sudo gedit /usr/share/applications/neo4j-desktop.desktop
```

[Website Icon - 不太清晰](https://neo4j.com/favicon.ico)

![](Pics/neo4j-icon.png) ![](Pics/neo4j-icon-old.png)


```bash
sudo cp ~/Projects/Blog/Data/GraphDB/Pics/neo4j-icon.png /usr/share/pixmaps/neo4j-icon.png

sudo cp ~/Projects/Blog/Data/GraphDB/Pics/neo4j-icon-old.png /usr/share/pixmaps/neo4j-icon-old.png
```

```bash
[Desktop Entry]
Encoding=UTF-8
Type=Application
Name=Neo4j-Desktop
#添加neo4j-desktop-1.4.1-x86_64.AppImage在本地的位置
Exec=/home/lzy/Tools/Neo4j-Desktop/neo4j-desktop-1.5.9-x86_64.AppImage
#读者可自行在互联网上搜索*.png格式图片然后重命名neo4j-desktop.png放置/neo4j目录
Icon=/usr/share/pixmaps/neo4j-icon.png
# Icon=/usr/share/pixmaps/neo4j-icon-old.png
Terminal=false
StartupNotify=true
Categories=Application;Development;
```



## Neo4j AuraDB

```bash
username : neo4j

password : lvq1WFfG0b-yYbf14J1PXG9YtvsmqeTYtL2JKLfvNF8
```

# Problem Shooting

## 01 Unsupported Java Version

**Java LTS** - Java 8 ，Java 11， Java 17，Java 21

```bash
lzy@legion:~ $ neo4j
Unsupported Java 11.0.22 detected. Please use Java(TM) 17 or Java(TM) 21 to run Neo4j Server.

# Dealing with multiple installed Java versions
update-java-alternatives --list
sudo update-alternatives --config java

# 修改 $JAVA_HOME
# JAVA_HOME="/usr/lib/jvm/java-11-openjdk-amd64"JAVA_HOME="/usr/lib/jvm/java-11-openjdk-amd64"

echo '# JAVA_HOME by lzy' >> ~/.bashrc
echo 'JAVA_HOME=/usr/lib/jvm/java-1.21.0-openjdk-amd64' >> ~/.bashrc
echo 'export PATH=$JAVA_HOME/bin:$PATH' >> ~/.bashrc
source ~/.bashrc

# cd $JAVA_HOME/bin/
```

## 02 Neo4j Start Failure

neo4j start 失败，报错

```bash
lzy@legion:~ $ neo4j start
Validating Neo4j configuration: /etc/neo4j/neo4j.conf
No issues found.

Validating user Log4j configuration: /etc/neo4j/user-logs.xml
5 issues found.
Error: Cannot access RandomAccessFile java.io.FileNotFoundException: /var/log/neo4j/neo4j.log (Permission denied)

...

Warning: Null object returned for RollingRandomAccessFile in Appenders.
Warning: Null object returned for RollingRandomAccessFile in Appenders.
Warning: Null object returned for RollingRandomAccessFile in Appenders.
Warning: Null object returned for RollingRandomAccessFile in Appenders.
Warning: Unable to locate appender "DebugLog" for logger config "root"
Warning: Unable to locate appender "HttpLog" for logger config "HttpLogger"
Warning: Unable to locate appender "QueryLog" for logger config "QueryLogger"
Warning: Unable to locate appender "SecurityLog" for logger config "SecurityLogger"

Configuration file validation failed.
Configuration contains errors. This validation can be performed again using 'neo4j-admin server validate-config'.
```


需要 sudo

```bash
lzy@legion:~ $ sudo neo4j start
[sudo] password for lzy:
Directories in use:
home:         /var/lib/neo4j
config:       /etc/neo4j
logs:         /var/log/neo4j
plugins:      /var/lib/neo4j/plugins
import:       /var/lib/neo4j/import
data:         /var/lib/neo4j/data
certificates: /var/lib/neo4j/certificates
licenses:     /var/lib/neo4j/licenses
run:          /var/lib/neo4j/run
Starting Neo4j.
Started neo4j (pid:678744). It is available at http://localhost:7474
There may be a short delay until the server is ready.
```

在浏览器中输入网址，可以看到相应界面

![](Pics/neo4j003.png)

初始的 用户名 和 密码 都是 **neo4j**

后面会让修改 密码

You are connected as user **neo4j** - to **neo4j://localhost:7687**

```bash
lzy@legion:~ $ sudo neo4j stop
Stopping Neo4j....... stopped.
```
