# Cryptology

Cryptology(密码学) = Cryptography(编码学) + Cryptanalysis(破译学)

---

## Table of Contents

- [Cryptology](#cryptology)
  - [Table of Contents](#table-of-contents)
- [Asymmetric/Symmetric Encryption](#asymmetricsymmetric-encryption)
- [加密算法](#加密算法)
  - [AES 对称加密](#aes-对称加密)
  - [RSA 非对称加密](#rsa-非对称加密)
  - [Diffie-Hellman (DH) 密钥交换算法](#diffie-hellman-dh-密钥交换算法)




---





# Asymmetric/Symmetric Encryption

**对称加密** (Symmetric Encryption)
1. 特点 : 只有一把钥匙
2. 原理 : 加密 & 解密 使用 同一个密钥
3. Pros : 速度极快，计算量小，适合传输大量数据 (eg : 文件、视频流)
4. Cons : 密钥分发困难，密钥分发时候被中间人截获，加密就失效
5. 生活类比 : 你买了一把锁和两把一样的钥匙，你把一把钥匙快递寄给朋友(如果快递被偷，锁就废了)
6. 常用算法
   1. AES


**非对称加密** (Asymmetric Encryption)
1. 特点 : 有一对钥匙，公钥 & 私钥
2. 原理
   1. 公钥 (Public Key) : 公开 给所有人，用来加密
   2. 私钥 (Private Key) : 自己严密保存，用来解密
3. ==规则==
   1. **公钥 加密的，只有 私钥 能解密**
   2. **私钥 签名的，公钥 能验证**
4. Pros : 安全，不需要传输私钥，解决了密钥分发问题
5. Cons : 速度极慢(比对称加密慢 100-1000 倍)，计算消耗大
6. 生活类比 : 带锁的 空箱子 寄送出去，大家都能放东西 & 上锁(公钥加密)，但钥匙自己保留，才能打开信箱取信(私钥解密)
7. 常用算法
   1. RSA



---

# 加密算法

## AES 对称加密



## RSA 非对称加密

基于 **大数质因数分解**




## Diffie-Hellman (DH) 密钥交换算法

基于 **离散对数问题**

初始化 (Negotiation)
1. 服务器 & 客户端 协商好两个大质数 : 底数$G$ 和 模数$P$，明文传输的

生成私钥 (Private Generation)
1. 本机 (Client) : 生成 随机大整数 $a$，只有自己知道
2. 服务器 (Server) : 生成 随机大整数 $b$，只有自己知道

计算并交换公钥 (Public Exchange)
1. Client 算 $A = G^a \pmod P$，把 $A$ 发给 Server
2. Server 算 $B = G^b \pmod P$，把 $B$ 发给 Client
3. 窃听者截获了 $P, G, A, B$，但是根据 **离散对数难题**，已知 $A, G, P$ 很难反推 $a$

计算会话密钥 (Secret Calculation)
1. Client 计算 $K = B^a \pmod P = (G^b)^a \pmod P $
2. Server 计算 $K = A^b \pmod P = (G^a)^b \pmod P $
3. $(x^m)^n = x^{m \times n}$，因此 $(G^b)^a \pmod P = (G^a)^b \pmod P$
4. 双方算出的 $K$ 是完全一样的！这个 $K$ 就是接下来的 会话密钥 (Session Key)

