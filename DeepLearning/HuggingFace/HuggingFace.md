
# 下载 数据集

默认 下载位置 `/home/lzy/.cache/huggingface`

```python
import os
from huggingface_hub import snapshot_download

snapshot_download(
    repo_id="fleaven/Retargeted_AMASS_for_robotics",
    repo_type="dataset",
    local_dir=os.path.join(os.path.dirname(__file__), r"Retargeted_AMASS")
)
```


# 防止 429 限流 (HTTPError: 429 Client Error: Too Many Requests)

Terminal 登录 Hugging Face 账号 : `huggingface-cli login`

根据指导 在 [settings](https://huggingface.co/settings/tokens) 创建 token，并保存好，只会出现一次

输入 Ternimal

运行 下载 .py 文件

