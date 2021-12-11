# 字符串流 sstream

## 01.基本概念

以内存中的string类型变量为输入/输出对象

可以存放各种类型的数据

与标准输入输出流相同，进行文本和二进制只见的相互转换（可用于不同数据类型的转换）
1. 向string存数据 cout：二进制 to ASCII
2. 从string读数据 cin： ASCII to 二进制

不是文件，不需要打开关闭

## 02.相关流对象建立

**须加入头文件 #include <sstream>**

1. 字符串输出流对象：ostringstream 
2. 字符串输入流对象：istringstream
3. 字符串输入/输出流对象：stringstream


