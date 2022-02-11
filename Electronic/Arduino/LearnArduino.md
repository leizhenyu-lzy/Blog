# Learn Arduino

[toc]

# Arduino编程从零开始

## Arduino介绍

## 启程

## C语言基础

digitalWrite(引脚,高/低电平); HIGH LOW
digitalRead(引脚);
analogWrite(引脚,value); 0-255的整形
analogread();

delay(time);

“样本”代码：setup loop 必须始终存在于项目中

pinMode(num,MODE);

MODE可以选择INPUT_PULLUP(内部上拉电阻)

**项目开始时，setup将只运行一次**

可以在setup和loop之前定义变量，并在函数内使用

Serial.begin(9600);
Serial.println(1234);
Serial.available();
Serial.read();
Serial.parseFloat();从字符串提取一个浮点数

尽量不要在loop里面再嵌套循环，否则loop函数的执行效率会较低。如果

软件消抖
1. 加延时
2. 使用Bounce2.h库
   1. #include <Bounce2.h>
   2. 在全局区Bounce bouncer = Bounce();
   3. 在setup中bouncer.attach(PIN);
   4. 在loop中bouncer.update();
   5. 在loop中bouncer.read();


## 函数

## 数组和字符串

## 输入和输出

## Arduino标准类库

## 数据存储

## 显示器

## Arduino物联网程序设计

## C++和库