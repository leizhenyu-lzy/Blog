# Matplotlib

# Portals

[【莫烦Python】Matplotlib Python 画图教程](https://www.bilibili.com/video/BV1Jx411L7LU)

## 基本用法
```python
import numpy as np
from matplotlib import pyplot as plt
x = np.linspace(-1,1,50)
y = 2*x+1
plt.plot(x, y)
plt.show()
```

## figure图像

figure用于将图像显示在不同窗口。show将多个窗口一并显示。
figure有一个num参数，可以给数字也可以给字符串。还有一个figsize，可以传递一个tuple

```python
x = np.linspace(-1,1,50)
y1 = 2*x+1
y2 = x**2

plt.figure(num="a11", figsize=(7,8))
plt.plot(x, y1)

plt.figure(num=3)
plt.plot(x, y2, color="red", linewidth=1.0, linestyle="--")

plt.show()
```

## 设置坐标轴标签
xlim 和 ylim：xy两个轴的显示范围，(a,b)。a和b的大小没有限制，a可以大于b相当于把图片进行翻转
xlabel 和 ylabel：设置xy轴的标签名称
xticks 和 yticks：设置xy坐标轴上标签（原标签会被覆盖（不存在了））

```python
x = np.linspace(-5, 5, 50)
y1 = 2 * x + 1
y2 = x ** 2

plt.figure(num="a11", figsize=(7, 8))
plt.plot(x, y1)
plt.plot(x, y2, color="red", linewidth=1.0, linestyle="--")

plt.xlim((5, -5))
plt.ylim((-5, 5))
plt.xlabel("i am x")
plt.ylabel("i am y")

new_ticks = np.linspace(-1, 2, 5)
plt.xticks(new_ticks)
plt.yticks([-2, 3, 4],
           ["a", "b" , "c"])

plt.show()
```

颜色
```
'b'          蓝色
'g'          绿色
'r'          红色
'c'          青色
'm'          品红
'y'          黄色
'k'          黑色
'w'          白色
```

标记点形状
```
‘.’：点(point marker)
‘,’：像素点(pixel marker)
‘o’：圆形(circle marker)
‘v’：朝下三角形(triangle_down marker)
‘^’：朝上三角形(triangle_up marker)
‘<‘：朝左三角形(triangle_left marker)
‘>’：朝右三角形(triangle_right marker)
‘1’：(tri_down marker)
‘2’：(tri_up marker)
‘3’：(tri_left marker)
‘4’：(tri_right marker)
‘s’：正方形(square marker)
‘p’：五边星(pentagon marker)
‘*’：星型(star marker)
‘h’：1号六角形(hexagon1 marker)
‘H’：2号六角形(hexagon2 marker)
‘+’：+号标记(plus marker)
‘x’：x号标记(x marker)
‘D’：菱形(diamond marker)
‘d’：小型菱形(thin_diamond marker)
‘|’：垂直线形(vline marker)
‘_’：水平线形(hline marker)
```

线形
```
‘-‘：实线(solid line style)
‘–‘：虚线(dashed line style)
‘-.’：点划线(dash-dot line style)
‘:’：点线(dotted line style)
```


## 设置坐标轴位置

gca : get current axis
spines : 脊梁。 []选择具体哪个轴

set_position : 要绑定的轴在另一个轴上的位置

```python
x = np.linspace(-5, 5, 50)
y1 = 2 * x + 1
y2 = x ** 2

plt.figure(num="a11", figsize=(7, 8))
plt.plot(x, y1)
plt.plot(x, y2, color="red", linewidth=1.0, linestyle="--")

new_ticks = np.linspace(-1, 2, 5)
plt.xticks(new_ticks)
plt.yticks([-2, 3, 4],
           ["a", "b" , "c"])

# plt.xticks(())  # 隐藏标签
# plt.yticks(())  # 隐藏标签


ax = plt.gca()
ax.spines['right'].set_color('none')  # 让顶部脊梁（边框）消失
ax.spines['top'].set_color('none')  # 让顶部脊梁（边框）消失

ax.xaxis.set_ticks_position('bottom')  # 将bottom设置为xaxis
ax.yaxis.set_ticks_position('left')  # 将left设置为yaxis

ax.spines['bottom'].set_position(('data', -1))  # 将xaxis绑定在y轴值等于-1的位置
ax.spines['left'].set_position(('data', 2))  # 将yaxis绑定在x轴值等于2的位置

plt.show()
```

## Legend图例
```python
x = np.linspace(-5, 5, 50)
y1 = 2 * x + 1
y2 = x ** 2

plt.figure(num="a11", figsize=(7, 8))
plt.plot(x, y1, label="xy1")
plt.plot(x, y2, color="red", linewidth=1.0, linestyle="--", label="xy2")
plt.legend()
plt.show()
```

## Annotation

懒得看


## tick能见度

## Scatter散点图

```python
n = 1024
X = np.random.normal(0,1,n)
X = np.random.normal(0,1,n)
T = np.arctan2(Y, X)

plt.scatter(X, Y, s=75, c=T, alpha=0.5) # s点的大小  alpha透明度

plt.show()
```

## Bar柱状图

## Contours等高线图

## Image图片

```python
a = np.array([0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1]).reshape(3,3)

plt.imshow(a, interpolation="nearest", cmap='bone', origin='upper')
# origin控制输出的方向，upper就是和ndarry对应，lower是相反
plt.colorbar()

plt.show()

```


## 3D数据

## Subplot多合一显示

## Subplot分格显示

## 图中图

## 次坐标轴

## Animation动画
