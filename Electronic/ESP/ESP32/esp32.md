# ESP32

[toc]


## Portals

[孤独的二进制 - ESP32上的FREERTOS](https://www.bilibili.com/video/BV1q54y1Z7ca/)

[wokwi在线仿真网址](https://wokwi.com/)

# 孤独的二进制 - ESP32上的FREERTOS

## 什么是RTOS

FreeRTOS中, Task = Thread

开源

ESP32双核


## 多任务点灯

```cpp
void task1(void* pt)
{
  pinMode(23, OUTPUT);
  while(1)
  {
    digitalWrite(23,!digitalRead(23));
    vTaskDelay(1000);  // delay换为支持多任务的delay  // 函数内部填多少ticks
    // 对于esp32正好一个tick是1ms
  }
}

void task2(void* pt)
{
  pinMode(21, OUTPUT);
  while(1)
  {
    digitalWrite(21,!digitalRead(21));
    vTaskDelay(3000);
  }
}

void setup() 
{
  // 函数名，定义名称，分配内存大小（字节），参数，优先级，状态Handle
  xTaskCreate(task1,"blink23",1024,nullptr,1,nullptr);
  xTaskCreate(task2,"blink21",1024,nullptr,1,nullptr);
}

void loop() 
{

}

```

## 给任务传递参数

### 传递单个参数

### 传递多个参数



## STM32 FreeRTOS
