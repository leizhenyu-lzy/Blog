
# [PyTorch 的 Autograd](https://zhuanlan.zhihu.com/p/69294347)
# [AUTOGRAD MECHANICS](https://pytorch.org/docs/stable/notes/autograd.html#requires-grad)

import math
import torch
import numpy

choice = 22

# [pytorch自动求导机制](https://blog.csdn.net/qq_52852138/article/details/122659658)

# 计算图是由节点和边组成的，其中的一些节点是数据，一些是数据之间的运算
# 计算图实际上就是变量之间的关系
# tensor 和 function 互相连接生成的一个有向无环图（Directed Acyclic Graph）。简称DAG 图

# 我们使用 loss.backward() 来计算梯度
# 使用 .grad 来检索梯度值
# 仅能获得计算图叶子节点的 grad 属性，并且需要这些节点设置 requires_grad = True

# 由于性能原因，在给定的计算图中，我们仅能使用 backward() 计算梯度一次（每次backward之后，计算图会被释放，但叶子节点的梯度不会被释放。
# 叶子节点就是参数，不包括一些运算产生的中间变量
# 如果需要多次计算，我们需要设置 backward 的 retain_graph = True，这样的话求得的最终梯度是几次梯度之和

# 有时，我们只想对数据应用模型(forward过程)，而不考虑模型的更新，这时我们可以不使用梯度跟踪
# 将计算代码包围在 torch.no_grad() 块中
# fine-tune一个预训练的模型时，我们需要冻结模型的一些参数
# 当进行前向传播时，加速计算。对不追踪梯度的tensor进行计算会更高效

# autograd 在由 Function 对象组成的有向无环图(DAG)中保存数据(张量)和所有执行的操作(以及产生的新张量)的记录
# 在DAG中，叶子是 input tensors，根是 output tensors
# 通过从根到叶跟踪这个图，可以使用链式法则自动计算梯度
# 在前向传播中，autograd同时做两件事
# 1. 运行请求的操作来计算结果张量
# 2. 在DAG中保持操作的梯度函数
# 反向传播过程开始，当 .backward() 在 DAG 根上被使用时
# 1. 从每个 .grad_fn 中计算梯度
# 2. 将它们累加到各个 tensor 的 .grad 属性中
# 3. 利用链式法则，一直传播到叶子 tensor
# ...... 没看完



# 卷积之后,如果要接BN操作,最好是不设置偏置,因为不起作用,而且占显卡内存。 pytorch默认有Bias

# [浅谈 PyTorch 中的 tensor 及使用](https://zhuanlan.zhihu.com/p/67184419)

# requires_grad
# 创建一个张量 (tensor) 的时候，如果没有特殊指定的话，那么这个张量是默认是不需要求导的
# 我们可以通过 tensor.requires_grad 来检查一个张量是否需要求导

# 只有当所有输入都不需要求导的时候，输出才会不需要
# 训练一个网络的时候，我们从 DataLoader 中读取出来的一个 mini-batch 的数据，这些输入默认是不需要求导的
# 其次，网络的输出我们没有特意指明需要求导吧，Ground Truth 我们也没有特意设置需要求导
# 虽然输入的训练数据是默认不求导的，但是，我们的 model 中的所有参数，它默认是求导的
# 其中只要有一个需要求导，那么输出的网络结果必定也会需要求的

# 不要把网络的输入和 Ground Truth 的 requires_grad 设置为 True
# 虽然这样设置不会影响反向传播，但是需要额外计算网络的输入和 Ground Truth 的导数，增大了计算量和内存
# net = nn.Sequential()  
# for param in net.named_parameters(): 
#     print(param[0], param[1].requires_grad)
# 在训练的过程中冻结部分网络，让这些层的参数不再更新，这在迁移学习中很有用处

# torch.no_grad()
# 做 evaluating 的时候（不需要计算导数），我们可以将推断（inference）的代码包裹在 with torch.no_grad():中
# 以达到 暂时 不追踪网络参数中的导数的目的，总之是为了减少可能存在的计算和内存消耗。

# 反向传播及网络的更新
# 有了网络输出之后，根据这个结果来更新我们的网络参数
# ...... 没看完




# CPU and GPU
# 关于 tensor.cuda() 和 tensor.to(device) ，当 device 是 GPU 的时候，这两者并没有区别
# 直接在代码最前面加一句话指定 device ，后面的代码直接用to(device) 就可以了
# device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
# a = torch.rand([3,3]).to(device)
# 使用 GPU 还有一个点，在我们想把 GPU tensor 转换成 Numpy 变量的时候，需要先将 tensor 转换到 CPU 中去
# 因为 Numpy 是 CPU-only 的
# 如果 tensor 需要求导的话，还需要加一步 detach，再转成 Numpy 
# x  = torch.rand([3,3], device='cuda')
# x_ = x.cpu().numpy()
# y  = torch.rand([3,3], requires_grad=True, device='cuda').
# y_ = y.cpu().detach().numpy()

# tensor.item()
# 我们在提取 loss 的纯数值的时候，常常会用到 loss.item()，其返回值是一个 Python 数值 (python number)
# 不像从 tensor 转到 numpy (需要考虑 tensor 是在 cpu，还是 gpu，需不需要求导)
# 无论什么情况，都直接使用 item() 就完事了，如果需要从 gpu 转到 cpu 的话，PyTorch 会自动帮你处理。
# 注意 item() 只适用于 tensor 只包含一个元素的时候。因为大多数情况下我们的 loss 就只有一个元素，所以就经常会用到
# 如果想把含多个元素的 tensor 转换成 Python list 的话，要使用 tensor.tolist()



# [为什么要使用optimizer.zero_grad()](https://blog.csdn.net/scut_salmon/article/details/82414730)

# optimizer.zero_grad()意思是把梯度置零，也就是把loss关于weight的导数变成0
# 对于每个batch大都执行了这样的操作
# optimizer.zero_grad()  # 梯度初始化为零
# # forward + backward + optimize
# outputs = net(inputs)  # 前向传播求出预测的值
# loss = criterion(outputs, labels)  # 求loss
# loss.backward()  # 反向传播求梯度
# optimizer.step()  # 更新所有参数

if choice == 11:
    a = torch.tensor(1,dtype=torch.float32,requires_grad=True)  # 创建tensor时设置 requires_grad = True 来支持梯度计算

    b = math.exp(a)
    print("b", b)  # b 2.718281828459045

    c = a.exp()
    print("c", c)  # c tensor(2.7183, grad_fn=<ExpBackward0>)
    print(c.requires_grad)  # True
    print(c.grad_fn)  # <ExpBackward0 object at 0x7f1983585c40>
    
    p = torch.tensor(3, dtype=torch.float64, requires_grad=False)
    print(p.requires_grad)  # False
    p.requires_grad_(True)  # 使用 x.requires_grad_(True) 来设置
    print(p.requires_grad)  # True
    
    
elif choice == 12:
    input = torch.ones([2, 2], requires_grad=False)
    w1 = torch.tensor(2.0, requires_grad=True)
    w2 = torch.tensor(3.0, requires_grad=True)
    w3 = torch.tensor(4.0, requires_grad=True)
    l1 = input * w1
    l2 = l1 + w2
    l3 = l1 * w3
    l4 = l2 * l3
    loss = l4.mean()
    loss.backward()
    print(l4.grad_fn)  # <MulBackward0 object at 0x7fab9bc57c40>
    print(loss.grad_fn)  # <MeanBackward0 object at 0x7fbeb60e6c40>
    print(w1.grad)  # tensor(28.)  # 我们仅能获得计算图叶子节点的 grad 属性，并且需要这些节点设置 requires_grad = True

elif choice == 13:
    input = torch.ones([2, 2], requires_grad=False)
    w1 = torch.tensor(2.0, requires_grad=True)
    w2 = torch.tensor(3.0, requires_grad=True)
    w3 = torch.tensor(4.0, requires_grad=True)
    l1 = input * w1
    l2 = l1 + w2
    l3 = l1 * w3
    l4 = l2 * l3
    l4.retain_grad()
    loss = l4.mean()
    loss.backward(retain_graph=True)
    loss.backward()  # #如果上面没有设置 retain_graph = True，这里会报错
    print(l4.grad_fn)  # <MulBackward0 object at 0x7fab9bc57c40>
    print(loss.grad_fn)  # <MeanBackward0 object at 0x7fbeb60e6c40>
    print(w1.grad)  # tensor(28.)  # 我们仅能获得计算图叶子节点的 grad 属性，并且需要这些节点设置 requires_grad = True

elif choice == 14:
    input = torch.ones([2, 2], requires_grad=False)
    w1 = torch.tensor(2.0, requires_grad=True)
    w2 = torch.tensor(3.0, requires_grad=True)
    w3 = torch.tensor(4.0, requires_grad=True)
    l1 = input * w1
    l2 = l1 + w2
    l3 = l1 * w3
    l4 = l2 * l3
    print(l4.requires_grad)  # True
    print(w1.requires_grad)  # True
    
    l4 = l4.detach()
    w1 = w1.detach()
    print(l4.requires_grad)  # False
    print(w1.requires_grad)  # False
    
    with torch.no_grad():
        input = torch.ones([2, 2], requires_grad=False)
        w1 = torch.tensor(2.0, requires_grad=True)
        w2 = torch.tensor(3.0, requires_grad=True)
        w3 = torch.tensor(4.0, requires_grad=True)
        l1 = input * w1
        l2 = l1 + w2
        l3 = l1 * w3
        l4 = l2 * l3
        print(l4.requires_grad)  # False
        print(w1.requires_grad)  # True

elif choice == 21:
    input = torch.tensor([1.0], requires_grad=False)
    coeff = torch.tensor([2.0], requires_grad=False)
    output = torch.matmul(input,coeff)
    print(output.requires_grad)  # False(默认)
    output.requires_grad_()
    print(output.requires_grad)  # True
    
    input = torch.tensor([1.0], requires_grad=True)
    coeff = torch.tensor([2.0], requires_grad=False)
    output = torch.matmul(input,coeff)
    print(output.requires_grad)  # True(默认)
    
elif choice == 22:
    device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
    print(device)  # cuda
    x1 = torch.rand([3,3], device='cuda')
    x1_ = x1.cpu()
    x1__ = x1.cpu().numpy()
    print(type(x1),type(x1_),type(x1__))  # <class 'torch.Tensor'> <class 'torch.Tensor'> <class 'numpy.ndarray'>
    print(x1.device, x1_.device)  # cuda:0 cpu
    
    x2 = torch.rand([3,3]).to(device)
    print(x2.device)  # cuda:0
    
    x3 = torch.rand([3,3], requires_grad = True, device='cuda')
    x3_ = x3.detach().cpu()  # 可以不用detach
    x3__ = x3.detach().cpu().numpy()  # 需要加detach()否则 Can't call numpy() on Tensor that requires grad
    print(type(x3),type(x3_),type(x3__))  # <class 'torch.Tensor'> <class 'torch.Tensor'> <class 'numpy.ndarray'>
    print(x3.device, x3_.device)  # cuda:0 cpu
    print(x3.requires_grad, x3_.requires_grad)  # True False
    
    x4 = torch.rand([3,3], requires_grad = True).to(device)
    x4_ = x4.cpu()  # 可以不用detach
    x4__ = x4.detach().cpu().numpy()  # 需要加detach()否则 Can't call numpy() on Tensor that requires grad
    print(type(x4),type(x4_),type(x4__))  # <class 'torch.Tensor'> <class 'torch.Tensor'> <class 'numpy.ndarray'>
    print(x4.device, x4_.device)  # cuda:0 cpu
    print(x4.requires_grad, x4_.requires_grad)  # True False
