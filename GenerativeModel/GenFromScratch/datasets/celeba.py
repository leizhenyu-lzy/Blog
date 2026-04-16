import os
from pathlib import Path

from PIL import Image
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms


class CelebADataset(Dataset):
    """
    统一的 CelebA 数据集类，供 VAE / DDPM / Flow Matching 等所有模型共享。
    只加载图片，不加载属性标签（无条件生成）。
    """

    def __init__(self, data_root: str, image_size: int = 64):
        super().__init__()
        self.image_dir = self._resolve_image_dir(data_root)
        self.image_files = sorted([
            f for f in os.listdir(self.image_dir)
            if f.lower().endswith(('.jpg', '.jpeg', '.png'))
        ])
        if len(self.image_files) == 0:
            raise FileNotFoundError(
                f"No images found in {self.image_dir}. "
                f"Check your data_root: {data_root}"
            )

        self.transform = transforms.Compose([
            transforms.Resize(image_size),  # 短边缩放到 image_size，长边等比例缩放，保持宽高比不变
            transforms.CenterCrop(image_size),  # 统一为 image_size x image_size
            transforms.ToTensor(),            # [0, 1]
            transforms.Normalize([0.5] * 3, [0.5] * 3),  # (input - 0.5) / 0.5 -> [-1, 1]
        ])

    @staticmethod
    def _resolve_image_dir(data_root: str) -> str:
        """Kaggle CelebA 解压后是双层嵌套 : data_root/img_align_celeba/img_align_celeba/*.jpg"""
        image_dir = Path(data_root) / "img_align_celeba" / "img_align_celeba"
        if not image_dir.is_dir():
            raise FileNotFoundError(
                f"Expected CelebA images at {image_dir}, "
                f"check your data_root: {data_root}"
            )
        return str(image_dir)

    def __len__(self):
        return len(self.image_files)

    def __getitem__(self, idx):
        img_path = os.path.join(self.image_dir, self.image_files[idx])
        image = Image.open(img_path).convert("RGB")  # PIL Image (RGB, uint8, 0~255)，不同于 OpenCV (BGR, uint8, 0~255)
        return self.transform(image)


def get_dataloader(
    data_root: str,
    image_size: int = 64,
    batch_size: int = 64,
    num_workers: int = 4,
    shuffle: bool = True,
) -> DataLoader:
    """
    工厂函数：所有训练脚本统一调用这个接口获取 DataLoader

    用法:
        from datasets.celeba import get_dataloader
        loader = get_dataloader("/home/lzy/Datasets/CelebFacesAttributesDataset")
    """
    dataset = CelebADataset(data_root, image_size)
    return DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=shuffle,
        num_workers=num_workers,
        pin_memory=True,  # 将数据加载到 锁页内存(Pinned Memory) 区域，GPU 可以直接通过 DMA 读数据，分配过多可能导致系统资源紧张
        drop_last=True,
    )


def denormalize(tensor):
    """从 [-1, 1] 还原到 [0, 1]，用于可视化"""
    return tensor * 0.5 + 0.5
