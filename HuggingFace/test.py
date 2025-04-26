import os
from huggingface_hub import snapshot_download

snapshot_download(
    repo_id="openvla/openvla-7b-finetuned-libero-spatial",
    # repo_type="model",
    local_dir=os.path.join(r"/home/lzy/Projects/OpenVLA", r"openvla-7b-finetuned-libero-spatial")
)

