# Trainer 类 / Trainer 抽象

不是 PyTorch 原生组件

封装
1. `__init__`
    1. model : `torch.nn.Module`
    2. train : `DataLoader`
    3. optimizer : `torch.optim.Optimizer`
    4. gpu_id : `int`
    5. save_freq : `int`
2. **run_epoch** & **run_batch** : run_epoch 内 调用 run_batch
3. **train** : 调用 run_batch & save_checkpoint
4. forward_propagation
5. loss_compute
6. backward_propagation
7. optimizer_step
8. zero_gradient
9. save_checkpoint


helper functions
1. load_train_objs : 返回 dataset & model & optimizer
2. prepare_dataloader





