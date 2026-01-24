import h5py
import numpy as np


# 1. 创建/写入 HDF5 文件
with h5py.File('my_data.h5', 'w') as f:
    # 创建一个组
    train_group = f.create_group("train")

    # 生成一些随机数据 (假设是 1000张 256x256 的图片)
    data = np.random.random((1000, 256, 256))

    # 存入数据集，并开启压缩
    dateset = train_group.create_dataset("images", data=data, compression="gzip")

    # 添加元数据
    dateset.attrs['description'] = "Synthetic training images"
    dateset.attrs['version'] = 1.0

# 2. 读取 HDF5 文件
with h5py.File('my_data.h5', 'r') as f:
    # 像查字典一样访问
    print(list(f.keys()))  # 输出: ['train']

    # 此时并没有把数据加载到内存，只获取了指针
    dataset = f['train']['images']

    # 只读取第 10 张图片的数据 (非常快)
    image_10 = dataset[10]
    print(image_10.shape)



# 3. 遍历 HDF5 文件，查看 Structure (结构)、Metadata (元数据)、Data Objects (数据对象信息)
def print_structure(name, obj):
    # 1. 查看 Structure (结构)
    # 这里的 name 就是层级路径，比如 "train/images"
    print(f"Name: {name}")

    # 2. 查看 Metadata (元数据)
    # obj.attrs 存储了所有的元数据
    if len(obj.attrs) > 0:
        print("  Metadata (Attributes):")
        for key, val in obj.attrs.items():
            print(f"    - {key}: {val}")

    # 3. 查看 Data Objects (数据对象信息)
    # 如果是 Dataset (类似文件)，打印它的形状和类型
    if isinstance(obj, h5py.Dataset):
        print(f"  Data Object: Shape={obj.shape}, Dtype={obj.dtype}")

    print("-" * 20)

# 打开文件并遍历
with h5py.File('my_data.h5', 'r') as f:
    print("-" * 20)
    print("-" * 20)
    print(f"File: {f.filename}\n")
    # visititems 会递归遍历文件中的每一个节点，并调用上面的函数
    f.visititems(print_structure)