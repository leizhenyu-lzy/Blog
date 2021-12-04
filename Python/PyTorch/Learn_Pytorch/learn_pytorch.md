# PyTorch官方教程

## 什么是PyTorch？

### Tensor 张量

Tensors 类似于 NumPy 的 ndarrays ，同时 Tensors 可以使用 GPU 进行计算。

构造矩阵

```python
x = torch.empty(a,b)  #构造一个a×b矩阵，不初始化

x = torch.rand(a,b)  #构造一个a×b矩阵，随机初始化

x = torch.zeros(a,b，dtype=torch.long)  #构造一个a×b矩阵，全0，数据类型为long

x = torch.tensor([m,n])  #构造一个张量，直接使用数据

x = torch.randn_like(x, dtype=torch.float)  #创建一个 tensor 基于已经存在的 tensor

```

获取信息
```python
print(x.size())
```

操作

任何使张量会发生变化的操作都有一个前缀 ‘’。例如：x.copy(y), x.t_(), 将会改变 x

```python
#加法
x + y
torch.add(x, y)
torch.add(x, y, out=result)  #提供一个输出 tensor 作为参数
y.add_(x)  #in-place

#索引
x[:, 1]  #使用标准的 NumPy 类似的索引操作

#改变大小：如果你想改变一个 tensor 的大小或者形状，你可以使用 torch.view
z = x.view(-1, 8) # the size -1 is inferred from other dimensions

#获取值：使用 .item() 来获得这个 value
x.item()
```