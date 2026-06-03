# Hiking in the Wild

`parkour_env_cfg.py`

depth 后处理
配置里的 noise pipeline 是：
`crop_and_resize()` -> `gaussian_blur_noise()` -> `depth_normalization()`

原图 36 x 64
CropAndResizeCfg(crop_region=(18, 0, 16, 16))
所以变成 18 x 32
blur: kernel_size=3, sigma=1
depth clip 到 [0.0, 2.5]，再 normalize 到 [0, 1]


ONNX 部署的时候 还是 拆分为 2个 model(perception & rl)



8 帧 depth 一起压到 128 维


Input depth:        (N, 8, 18, 32)

Conv2d:             in=8, out=4, kernel=3, stride=1, padding=1
ReLU

Feature map:        (N, 4, 18, 32)

Flatten:            4 * 18 * 32 = 2304

MLP head:
Linear 2304 -> 256
ReLU
Linear 256 -> 256
ReLU
Linear 256 -> 128

Output:             (N, 128)
