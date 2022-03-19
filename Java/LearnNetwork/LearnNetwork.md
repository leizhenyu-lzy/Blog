# Java Web

## Portals

[狂神说 网络编程](https://www.bilibili.com/video/BV1LJ411z7vY)

[菜鸟教程 网络编程](https://www.runoob.com/java/java-networking.html)

# 狂神说 网络编程

TCP:打电话
UDP:发短信

网络编程：tcp/ip  C/S
网页编程：javaweb B/S

## 网络通信要素

通信双方地址
1. ip
2. 端口号

网络通信协议
1. http
2. ftp
3. smtp
4. tcp
5. udp

## IP地址

127.0.0.1 localhost

ipv4:$2^{4*8}$
ipv6:$2^{128}$：格式为X:X:X:X:X:X:X:X，其中每个X表示地址中的16位，以十六进制表示（每个X四个十六进制数）

公网--互联网
私网--局域网

域名：免去记忆ip

## 端口Port

不同的进程有不同端口号

查看所有端口，命令行：**netstat -ano**

TCP和UDP可以同时使用同一个端口进行通信

## 通信协议

TCP：连接、稳定

UDP：不连接、不稳定（DDOS）

## TCP

客户端

服务器

## Tomcat

Tomcat服务器

## UDP

## URL


# 菜鸟教程 网络编程

## InetAddress 类的方法

**没有构造器，不能new**

这个类表示互联网协议(IP)地址。

常用方法
1. static InetAddress getByAddress(byte[] addr)
   在给定原始 IP 地址的情况下，返回 InetAddress 对象
2. static InetAddress getByAddress(String host, byte[] addr)
   根据提供的主机名和 IP 地址创建 InetAddress
3. static InetAddress getByName(String host)
   在给定主机名的情况下确定主机的 IP 地址
4. String getHostAddress() 
   返回 IP 地址字符串（以文本表现形式）
5. String getHostName() 
   获取此 IP 地址的主机名/域名
6. static InetAddress getLocalHost()
   返回本地主机。
7. String toString()
   将此 IP 地址转换为 String。

需要使用try catch

```java
try
{
    InetAddress name = InetAddress.getByName("www.google.com");
    System.out.println(name.getCanonicalHostName());//108.160.163.102
    System.out.println(name.getAddress());//[B@7a0ac6e3
    System.out.println(name.getHostAddress());//108.160.163.102
    System.out.println(name.getLocalHost());//DESKTOP-D4K3O6R/192.168.154.1
}
catch (UnknownHostException e)
{
    e.printStackTrace();
}
```

## ServerSocket 类的方法

服务器应用程序通过使用 java.net.ServerSocket 类以获取一个端口,并且侦听客户端请求。

**构造方法**
1.	public ServerSocket(int port) throws IOException
    创建绑定到特定端口的服务器套接字。
2.	public ServerSocket(int port, int backlog) throws IOException
    利用指定的 backlog 创建服务器套接字并将其绑定到指定的本地端口号。
3.	public ServerSocket(int port, int backlog, InetAddress address) throws IOException
    使用指定的端口、侦听 backlog 和要绑定到的本地 IP 地址创建服务器。
4.	public ServerSocket() throws IOException
    创建非绑定服务器套接字。

创建非绑定服务器套接字。 如果 ServerSocket 构造方法没有抛出异常，就意味着你的应用程序已经成功绑定到指定的端口，并且侦听客户端请求。

**常用方法**
1.	public int getLocalPort()
    返回此套接字在其上侦听的端口。
2.	public Socket accept() throws IOException
    侦听并接受到此套接字的连接。
3.	public void setSoTimeout(int timeout)
    通过指定超时值启用/禁用 SO_TIMEOUT，以毫秒为单位。
4.	public void bind(SocketAddress host, int backlog)
    将 ServerSocket 绑定到特定地址（IP 地址和端口号）。

## Socket 类的方法

java.net.Socket 类代表客户端和服务器都用来互相沟通的套接字。客户端要获取一个 Socket 对象通过实例化 ，而 服务器获得一个 Socket 对象则通过 accept() 方法的返回值。


**构造方法**
1.  public Socket(String host, int port) throws UnknownHostException, IOException.
    创建一个流套接字并将其连接到指定主机上的指定端口号。
2.  public Socket(InetAddress host, int port) throws IOException
    创建一个流套接字并将其连接到指定 IP 地址的指定端口号。
3.	public Socket(String host, int port, InetAddress localAddress, int localPort) throws IOException.
    创建一个套接字并将其连接到指定远程主机上的指定远程端口。
4.	public Socket(InetAddress host, int port, InetAddress localAddress, int localPort) throws IOException.
    创建一个套接字并将其连接到指定远程地址上的指定远程端口。
5.	public Socket()
    通过系统默认类型的 SocketImpl 创建未连接套接字

当 Socket 构造方法返回，并没有简单的实例化了一个 Socket 对象，它实际上会尝试连接到指定的服务器和端口。

客户端和服务器端都有一个 Socket 对象，所以无论客户端还是服务端都能够调用这些方法。


**常用方法**
1.  public void connect(SocketAddress host, int timeout) throws IOException
    将此套接字连接到服务器，并指定一个超时值。
2.	public InetAddress getInetAddress()
    返回套接字连接的地址。
3.	public int getPort()
    返回此套接字连接到的远程端口。
4.	public int getLocalPort()
    返回此套接字绑定到的本地端口。
5.	public SocketAddress getRemoteSocketAddress()
    返回此套接字连接的端点的地址，如果未连接则返回 null。
6.	public InputStream getInputStream() throws IOException
    返回此套接字的输入流。
7.	public OutputStream getOutputStream() throws IOException
    返回此套接字的输出流。
8.	public void close() throws IOException
    关闭此套接字。

```java
public static void main(String[] args)
{
    InetSocketAddress inetsocket1 = new InetSocketAddress("127.0.0.1",8080);
    System.out.println(inetsocket1.getAddress());///127.0.0.1
    System.out.println(inetsocket1.getHostName());//127.0.0.1
    System.out.println(inetsocket1.getPort());//8080
    InetSocketAddress inetsocket2 = new InetSocketAddress("localhost",8080);
    System.out.println(inetsocket2.getAddress());//localhost/127.0.0.1
    System.out.println(inetsocket2.getHostName());//localhost
    System.out.println(inetsocket2.getPort());//8080
}
```