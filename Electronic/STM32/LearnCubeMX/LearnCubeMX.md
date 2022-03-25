# STM32CubeMX

[toc]

## Portals


# 软件试用

## GPIO

**CubeMX中的选项**

Input
1. GPIO mode
   1. Input mode
2. GPIO Pull-up/Pull-down
   1. No pull-up and no pull-down
   2. Pull-up
   3. Pull-down

Output
1. GPIO output level（默认输出的高低电平，程序初始化之后该Output口输出的电平信号是高还是低）
   1. Low
   2. High
2. GPIO mode（推挽输出、开漏输出）
   1. Output Push Pull
   2. Output Open Drain
3. GPIO Pull-up/Pull-down
   1. No pull-up and no pull-down
   2. Pull-up
   3. Pull-down（Open Drain时没有该选项）（开漏输出只有低电平和高阻态，高电平需要自己外接上拉电路）
4. Maximum output speed
   1. Low
   2. Medium
   3. High
5. User Label

**说明**

output level

pull-up/pull-down

