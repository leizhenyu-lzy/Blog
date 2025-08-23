[torch.utils.data.Sampler - PyTorch Docs](https://docs.pytorch.org/docs/stable/data.html#torch.utils.data.Sampler)



`torch.utils.data.Sampler`
1.
2. 所有的 采样器 继承自 `Sampler` 这个类
3. ```py
    __all__ = [

    ]
    ```
4. `__init__` : 初始化
5. `__iter__` : 产生迭代索引值的，也就是指定每个 step 需要读取哪些数据
6. `__len__`  : 返回每次迭代器的长度






`SequentialSampler` : 按顺序对数据集采样

`RandomSampler` : `replacement = True`，可以重复采样(可能导致有的样本采样不到)

`SubsetRandomSampler`

`WeightedRandomSampler`

`BatchSampler` : 对批量的数据进行训练



"Sampler",
"SequentialSampler",
"RandomSampler",
"SubsetRandomSampler",
"WeightedRandomSampler",
"BatchSampler",
"DistributedSampler",