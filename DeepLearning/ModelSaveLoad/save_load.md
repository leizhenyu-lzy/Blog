`.pth` & `.onnx`


`state_dict` (仅权重参数)
1. 场景
   1. 保留模型代码，需要继续训练 / 微调 / 多实验对比
2. 最省空间、最灵活
3. 加载时必须实例化相同结构
4. code
   ```python
   # save
   torch.save(model.state_dict(), "xxx.pth")

   # load
   state = torch.load("cnn_state_dict.pth", map_location="cpu")
   model.load_state_dict(state, strict=True)  # model 是实例化的 Model 对象
   ```
5. `.ckpt` vs `.pt`
   1. 本质上一样，区别只在 习惯与内容约定
   2. `.pt` : 整模型 + 权重/参数
   3. `.ckpt` : 常见于 Lightning/自定义约定，通常是包含多项训练状态的字典
6. 只有权重是不够 完整恢复训练 的，一定要把 `optimizer` / `scheduler` 之类一并存起来，否则 动量、学习率 进度 都会丢
7. code
   ```python
   # save
   ckpt = {
       "epoch":      epoch,
       "model":      model.state_dict(),
       "optimizer":  optimizer.state_dict(),
       "scheduler":  scheduler.state_dict() if scheduler else None,
       "scaler":     scaler.state_dict()    if scaler   else None,  # AMP 可选
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

`torch.save(model)` (Pickle 整模型)
1. 加载回来就是普通 `nn.Module`
2. 强依赖 PyTorch 版本 / pickle 协议，跨版本、跨框架不可靠，在生产并不推荐
3. 安全风险：Pickle 反序列化可执行任意代码，仅加载可信来源；一般不建议在部署/分发中使用
4. 更推荐使用 `state_dict` 或 TorchScript/ONNX 等可移植格式
5. pickle 不会把类代码一起存进去，而是记录
   1. 对象的 模块名 : 比如 "autoencoder.height_encoder_nn"
   2. 对象的 类名 : 比如 "AutoencoderMLP3EN"
   3. 对象的参数(state_dict 等)




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





