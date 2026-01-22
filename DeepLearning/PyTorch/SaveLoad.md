# Save & Load

[Saving and Loading Models - Pytorch Tutorials](https://docs.pytorch.org/tutorials/beginner/saving_loading_models.html)


---

parameters & state_dict & register_buffer
1. ==下面的 方法返回的 Tensor 都是引用 (Reference)==，需要按需使用 `copy.deepcopy()`，如果直接序列化保存了则不需要
2. `model.state_dict()` : 返回 **字典 dict**，包含 需要 back-propagation 的 & register_buffer
3. `model.parameters()` : 返回 **迭代器 iterator**，仅 Parameter (权重)，只包含 Tensor 对象本身
4. `model.named_parameters()` : 返回 **迭代器 iterator**，仅 Parameter (权重) + 名字，(name, tensor) 元组
5. `model.named_buffers()` : 返回 **迭代器 iterator**，仅 register_buffer (非梯度状态) + 名字，(name, tensor) 元组

---

`torch.save`
1. 保存 serialized object，使用 python 的 pickle 进行 序列化
2. 形式
   ```python
   torch.save(
      obj,
      f,
      pickle_module=pickle,
      pickle_protocol=2,
      _use_new_zipfile_serialization=True  # 如果希望使用旧格式文件，需要传递的关键字
   )
   ```


`torch.load`
1. 使用 pickle 的反序列化功能，将 pickle 对象文件反序列化到内存中，可设置 将数据加载到的 device
2. `load`后，反序列化为 state_dict 后，才能 进一步 `load_state_dict`
3. 形式
   ```python
   torch.load(
      f,
      map_location=None,  # 跨设备保存需要，张量底层的存储空间会使用 map_location 参数动态地重新映射到其他设备
      pickle_module=pickle, *,
      weights_only=True,
      mmap=None,
      **pickle_load_args
   )
   ```




保存 & 加载 **==state_dict==**
1. **state_dict**
   1. `model.state_dict()` 返回的是 Python OrderedDict(有序字典，`collections.OrderedDict`)，属于 python 标准类型
   2. 只包含 Python 和 PyTorch 的 通用标准数据类型
   3. 只有 具有可学习参数的层(weight & bias) & ==register_buffer==(eg : running_mean) 才会出现在 state_dict 中
      1. register_buffer 是 `nn.Module` 自带的方法
      2. 不是模型参数(Parameter)，不需要梯度更新，是 state_dict 的一部分
   4. optimizer 会接收 `model.parameters()`，并且也有 state_dict
      1. `state`(内部状态，开始训练后才有)
      2. `param_groups`(参数组，`lr` / `momentum` / `dampening` / `weight_decay` / `params`(对应 传入时候的 `model.parameters()`))
2. `model.load_state_dict()` **加载时 必须 实例化 相同结构** (模型对象的 参数 键值对 Key-Value)
   1. 会 return 一个 NamedTuple 对象，通常被称为 IncompatibleKeys，包含两个列表(missing_keys, unexpected_keys)
      1. 如果加上 `strict=True`，有任何不匹配，都会抛出 Error
      2. 迁移学习等 需要加载 其他预训练的 参数 可能就需要 `strict=False`
   2. In-place Copy(原位拷贝) 操作，替换原始随机初始化的数值，Python 对象引用不变
   3. `load_state_dict` 会自动处理搬运
      1. Target (Model Parameters)，看 `model.parameters()` 当前在哪个设备上
      2. Source (State Dict)，看 ckpt["model"] 里的 Tensor 在哪个设备上 (可以通过 map_location 调整)
      3. **自动搬运** : 如果 源 和 目标 设备不一致，会自动把 源 Tensor copy 到 目标 Tensor 所在的设备上
   4. **==推荐顺序==** : 先 将 初始化的 model `.to(device)`，建立 optimizer 与 model.parameters 关系，最后再 load
      1. 优化器 没有 `.to()`，必须通过正确的初始化顺序来保证它在正确的设备上
3. 代码
   ```python
   # save
   torch.save(model.state_dict(), "xxx.pth")
   # load
   model = MyModel()  # 实例化模型
   state = torch.load('data.pth')  # 纯字典
   model.load_state_dict(state, strict=True)  # 填入数值
   ```
4. 一个文件保存多个模型，通常使用 `.tar` 作为 文件扩展名
   ```python
   # save
   torch.save({
      'modelA_state_dict': modelA.state_dict(),
      'modelB_state_dict': modelB.state_dict(),
      'optimizerA_state_dict': optimizerA.state_dict(),
      'optimizerB_state_dict': optimizerB.state_dict(),
      ...
   }, PATH)

   # load
   modelA = TheModelAClass(*args, **kwargs)
   modelB = TheModelBClass(*args, **kwargs)
   optimizerA = TheOptimizerAClass(*args, **kwargs)
   optimizerB = TheOptimizerBClass(*args, **kwargs)

   checkpoint = torch.load(PATH, weights_only=True)
   modelA.load_state_dict(checkpoint['modelA_state_dict'])
   modelB.load_state_dict(checkpoint['modelB_state_dict'])
   optimizerA.load_state_dict(checkpoint['optimizerA_state_dict'])
   optimizerB.load_state_dict(checkpoint['optimizerB_state_dict'])
   ```
5. **完整恢复训练** : 只有权重是不够的，一定要把 `optimizer` / `scheduler` 之类一并存起来，否则 动量、学习率 进度 都会丢
   ```python
   # save
   ckpt = {
       "epoch":      epoch,
       "model":      model.state_dict(),
       "optimizer":  optimizer.state_dict(),
       "scheduler":  scheduler.state_dict() if scheduler else None,
       "scaler":     scaler.state_dict()    if scaler    else None,  # AMP 可选，自动混合精度 (Automatic Mixed Precision)
   }
   torch.save(ckpt, "checkpoint.pth")

   # load
   ckpt = torch.load("checkpoint.pth", map_location="cuda:0")
   model.load_state_dict(ckpt["model"])
   optimizer.load_state_dict(ckpt["optimizer"])
   if scheduler and ckpt["scheduler"]:
       scheduler.load_state_dict(ckpt["scheduler"])
   if scaler and ckpt["scaler"]:
       scaler.load_state_dict(ckpt["scaler"])
   start_epoch = ckpt["epoch"] + 1
   ```
6. 跨设备 save & load
   1. **GPU (Save)** -> **GPU (Load)**
      1. 不需要 `map_location` (默认行为就是保持原来的设备，tensor 的 metadata 包含了 dtype & device)
      2. 需要 `model.to(device)`，实例化 model 时，模型默认是在 CPU 上的，加载了 state_dict 后，还是得显式地把整个模型搬到 GPU 上去
   2. **GPU (Save)** -> **CPU (Load)**
      1. 需要 `map_location='cpu'`，必须告诉 `torch.load` 加载到 CPU 内存里，如果不加，它会尝试找 GPU，如果这台机器没 GPU 就会报错
      2. 不需要 `model.to(device)` : **模型初始化默认就在 CPU**，加载进来的参数也已经在 CPU
   3. **CPU (Save)** -> **GPU (Load)**
      1. 需要 `map_location="cuda:0"`，在 `torch.load` 时直接把 Tensor 加载到显存里
         1. P.S. 其实可选(Optional)，可以先加载到 CPU 再通过 `model.to(device)` 搬运
      2. 需要 `model.to(device)`，最关键的，**强制性的、覆盖性的操作**，不管 `load` 加载到了哪里， PyTorch 遍历 model 下 所有的子模块、所有的 Parameter 和 Buffer，统统强制搬运到
7. 保存 DataParallel 模型
   1. `torch.nn.DataParallel` 是一个模型包装器，可实现并行 GPU 利用
   2. 保存方式 : `torch.save(model.module.state_dict(), PATH)`
   3. 如果忘记写 `module.`，导致所有 Key 多了 `module` 前缀，可以手动修改 Key


保存 & 加载 **==full_model==** (Pickle 整个模型)
1. pickle 在序列化 对象时，不会把这个对象的 类定义代码(Class Definition) 打包 进文件
2. 实际上保存
   1. 数据 : 模型中 具体的 参数值 (weight & bias 等)
   2. 引用 : 保存 模块名(Module Name) & 类名(Class Name)，形式是 Python 的 导入路径(Import Path)，eg : `models.resnet.MyResNet`
3. 目录结构(directory structure)敏感 & 需要特定类 : 加载模型时，pickle 会尝试 **根据引用 去 重新导入类**，如果 重构代码 或者 在另一个项目加载，就会 加载失败
4. 强依赖 PyTorch 版本 / pickle 协议，跨版本、跨框架不可靠，在生产并不推荐
5. 代码
   ```python
   # save
   torch.save(model, 'full_model.pth')
   # load
   loaded_model = torch.load('full_model.pth', weights_only=False)
   # 这里不需要先实例化 model = MyModel()，直接返回一个 nn.Module 对象
   ```











---

`torch.export` 通过一种叫 Tracing (追踪) 的技术，完整地记录下模型在运行一次时的所有计算步骤


`.pth` & `.onnx`




`TorchScript` (结构 + 参数) : 更多是 PyTorch 自己能跑的 黑箱模型
1. 两种路径
   1. script(对控制流友好) : 控制流保留，梯度正常，但加载后要重新创建优化器
   2. trace(对纯前向图最快) : 静态图，若网络里有数据依赖分支就不适合再训
2. 场景
   1. 加载后可直接推理，无需原始 Python 代码
   2. 可在 C++/LibTorch 端部署
3. code
   1. `torch.jit.script`
      ```py
      # save
      scripted = torch.jit.script(model)
      scripted.save("xxx.pt")

      # load
      model_ts = torch.jit.load("xxx.pt", map_location="cpu")
      ```
   2. `torch.jit.trace`
      ```py
      # save
      traced = torch.jit.trace(model, dummy_input)
      traced.save("xxx.pt")

      # load
      model_tr = torch.jit.load("xxx.pt")
      ```
4. 注意
   1. `trace` 只记录给定样例的前向图，含数据依赖分支/动态形状时优先 `script` 或混合 `script_module.forward = torch.jit.trace(...)`
   2. 导出前 `model.eval()`，去除 Dropout/BN 的训练行为；若需训练式 TorchScript，需要确保脚本化路径兼容
   3. 可用 `torch.jit.freeze` 冻结脚本模块以收敛属性并减少运行时开销
      ```python
      model.eval()
      scripted = torch.jit.script(model)
      scripted = torch.jit.freeze(scripted)
      scripted.save("xxx.pt")
      ```






ONNX + ONNX Runtime 推理
1. 一般 只推理
2. 跨框架可执行的 静态图 + 权重
3. 可丢给 ORT / TensorRT / OpenVINO 等后端
4. 导出（PyTorch → ONNX）
   ```python
   model.eval()
   dummy = torch.randn(1, C, H, W)
   torch.onnx.export(
       model, dummy, "model.onnx",
       input_names=["input"], output_names=["output"],
       opset_version=13,
       dynamic_axes={"input": {0: "batch"}, "output": {0: "batch"}},
   )
   ```
5. ONNX Runtime 推理
   ```python
   import onnxruntime as ort
   import numpy as np

   sess = ort.InferenceSession(
       "model.onnx",
       providers=["CUDAExecutionProvider", "CPUExecutionProvider"],
   )
   x = np.random.randn(4, C, H, W).astype(np.float32)
   y, = sess.run([sess.get_outputs()[0].name], {"input": x})
   ```
6. 常见注意事项
   1. 动态形状需设置 `dynamic_axes`；否则可能固定为导出样例形状
   2. 不支持的算子需替换/重写，或使用更高 `opset_version`；必要时用 `onnx-simplifier` 简化图
   3. 进一步加速可转 TensorRT（`trtexec --onnx=model.onnx`），注意精度（FP16/INT8）与算子支持





