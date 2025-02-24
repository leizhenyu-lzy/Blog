# Isaac Gym

[Isaac Gym - Tensor API](file:///home/lzy/Projects/isaacgym/docs/programming/tensors.html?highlight=wrap_tensor)

- [Isaac Gym](#isaac-gym)
  - [Simulation Setup](#simulation-setup)
  - [Assets](#assets)
  - [Tensor API](#tensor-api)
    - [Physics State](#physics-state)
    - [Contact Tensors](#contact-tensors)
    - [Force Tensors](#force-tensors)
    - [Control Tensors](#control-tensors)
  - [API Reference](#api-reference)
    - [Python API](#python-api)


## Simulation Setup

`from isaacgym import gymapi`  core API defined in `gymapi` module

`gym = gymapi.acquire_gym()`


## Assets



## Tensor API

tensor API is currently only supported for the **PhysX backend**




**global tensors** : tensors that hold the values for all actors in the simulation

Gym Tensor API 直接与 GPU 交互，但返回的数据不是标准的 PyTorch Tensor，而是低级别的 GPU 缓冲区，必须使用 `gymtorch.wrap_tensor()` 转换，才能在 PyTorch 中操作

Gym tensor API uses simple tensor desciptor, which specify the **device, memory address, data type, and shape of a tensor**




### Physics State

Actor Root State Tensor

Degrees-of-Freedom


### Contact Tensors

```python
_net_cf = gym.acquire_net_contact_force_tensor(sim)
net_cf = gymtorch.wrap_tensor(_net_cf)
```

### Force Tensors


### Control Tensors

**DOF Control**

set_dof_actuation_force_tensor

**Body Forces**






## API Reference

### Python API

class `isaacgym.gymapi.Gym`
1. `acquire_actor_root_state_tensor` : Retrieves buffer for Actor root states
   1. shape : (num_actors, 13)
      1. position([0:3])
      2. rotation([3:7])
      3. linear velocity([7:10])
      4. angular velocity([10:13])


torch_utils
1. `quat_rotate` & `quat_rotate_inverse`
   1. input
      1. q : 四元数 $(q_x, q_y, q_z, q_w)$
      2. v : 待旋转的向量 $x, y, z$

```python
@torch.jit.script
def quat_rotate(q, v):
    shape = q.shape
    q_w = q[:, -1]
    q_vec = q[:, :3]
    a = v * (2.0 * q_w ** 2 - 1.0).unsqueeze(-1)
    b = torch.cross(q_vec, v, dim=-1) * q_w.unsqueeze(-1) * 2.0
    c = q_vec * \
        torch.bmm(q_vec.view(shape[0], 1, 3), v.view(
            shape[0], 3, 1)).squeeze(-1) * 2.0
    return a + b + c


@torch.jit.script
def quat_rotate_inverse(q, v):
    shape = q.shape
    q_w = q[:, -1]
    q_vec = q[:, :3]
    a = v * (2.0 * q_w ** 2 - 1.0).unsqueeze(-1)
    b = torch.cross(q_vec, v, dim=-1) * q_w.unsqueeze(-1) * 2.0
    c = q_vec * \
        torch.bmm(q_vec.view(shape[0], 1, 3), v.view(
            shape[0], 3, 1)).squeeze(-1) * 2.0
    return a - b + c
```

