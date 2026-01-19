# PyTorch Autograd

[Automatic Differentiation Package `torch.autograd` - PyTorch Docs](https://docs.pytorch.org/docs/stable/autograd.html)

`torch.autograd.backward`
1. Compute the sum of gradients of given tensors with respect to graph leaves
   1. 对一个标量(通常是 Loss) 调用 `.backward()` 时，PyTorch 会自动从这个 Loss 开始，沿着计算图反向走一遍
   2. 寻找计算图中所有 `requires_grad=True` 的 叶子节点
   3. 计算出的梯度，不会返回，而是 直接 **累加** 到这些张量的 `.grad` 属性中
   4. 计算完成后，**默认** 释放计算图 以节省内存，除非 设置 `retain_graph=True`
2. 形式
   ```python
   torch.autograd.backward(
        tensors,
        grad_tensors=None,
        retain_graph=None,
        create_graph=False,
        grad_variables=None,
        inputs=None
   )
   ```


`torch.autograd.grad`
1. Compute and return the sum of gradients of outputs with respect to the inputs
   1. 不关心整个网络所有的参数，只计算 指定的 outputs 相对于 指定的 inputs 的梯度
   2. 不会修改张量的 `.grad` 属性，把计算出的梯度作为一个 tuple 直接返回
   3. 支持 `create_graph=True`，意味着 计算出来的 梯度 本身也是一个计算图的一部分，可以对这个 梯度 再次求导(二阶导数)
2. 形式
   ```python
   torch.autograd.grad(
        outputs,
        inputs,
        grad_outputs=None,
        retain_graph=None,
        create_graph=False,
        only_inputs=True,
        allow_unused=None,
        is_grads_batched=False,
        materialize_grads=False
   )
   ```





