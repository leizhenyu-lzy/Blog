# Linux 命令

**Table of Contents**
- [Linux 命令](#linux-命令)
- [内存 (`free`)](#内存-free)
- [存储 (`fdisk / gdisk / parted` \& `mkfs` \& `blkid`)](#存储-fdisk--gdisk--parted--mkfs--blkid)
- [挂载 (`lsblk` \& `mount` \& `umount`)](#挂载-lsblk--mount--umount)
- [权限修改 (`chmod` \& `chown`)](#权限修改-chmod--chown)



---

# 内存 (`free`)

`free` : 显示系统 物理内存(Physical Memory) & 交换空间(Swap Space) 的使用情况，默认单位 是 字节(Byte)
1. 栏目
   1. `Total`       : 系统安装的总物理内存或总交换空间大小
   2. `Used`        : 当前正在被进程使用的内存总量(不包括被 Buffer/Cache 占用的部分)
   3. `Free`        : 完全未被使用的内存总量
   4. `Shared`      : 被多个进程共享使用的内存
   5. `Buff/Cache`  : 被操作系统用作缓存和缓冲的内存总量，这部分内存随时可以被应用程序重新使用
   6. `Available`   : 真正可供应用程序立即使用的内存总量
2. `-h` : human-readable，Gi / Mi / Ki / B


# 存储 (`fdisk / gdisk / parted` & `mkfs` & `blkid`)

**==File System Type==**
1. **Linux 原生**      : Ext4 (最常用) / Ext3 / Ext2 / XFS (高性能/大容量) / Btrfs (新一代，带快照)
2. **Windows 原生**    : NTFS (Windows 主流)
3. **macOS 原生**      : APFS (新一代，苹果主流) / HFS+ (旧版)
4. **跨平台/通用**      : FAT32 / exFAT (U盘等通用交换格式，兼容 Windows, macOS, Linux)
5. **网络文件系统**     : NFS (Network File System) / SMB/CIFS (Samba，兼容 Windows 共享)
6. **只读压缩文件系统**  : Squashfs (用于 LiveCD、固件、AppImage，保证数据不可变性)
7. **虚拟/伪文件系统**  : procfs (/proc) / sysfs (/sys)，由内核动态维护，用于进程通信和系统配置
8. **内存文件系统**     : tmpfs，存储在内存和交换空间中，用于快速存取的临时数据


`blkid` (Block Device Attributes) : 查询块设备的属性，如 UUID / BLOCK_SIZE / FSTYPE
1. 建议加上 `sudo`，显示 系统内核识别到的 所有块设备的 完整 & 准确 属性信息


# 挂载 (`lsblk` & `mount` & `umount`)

`lsblk` (List Block Devices) : 树状结构列出 所有块设备 及其 分区
1. `-f` : 显示文件系统信息

`mount` : 将文件系统连接到目录树(挂载)
1. eg : `sudo mount /dev/sdb1 /mnt/data` (将 /dev/sdb1 挂载到 /mnt/data)

`umount` : 断开文件系统的连接(卸载)
1. eg : `sudo umount /mnt/data` 或 `sudo umount /dev/sdb1`


`df` (Disk Free) : 报告文件系统的磁盘空间使用情况
1. `-h` : human-readable

`du` (Disk Usage) : 报告文件或目录的磁盘空间占用大小
1. `-h` : human-readable

`/etc/fstab`


---

# 权限修改 (`chmod` & `chown`)

`whoami` : 查看 User/Owner

`id -gn` : 查看 Group


`chown` (Change Owner)
1. 解决 **你是谁？(身份)** 的问题
2. 将文件的 所有权从 root 转移到 自己
3. 作为 Owner，你获得了对该文件夹的完全控制权，可以运行 `chmod` 或在文件管理器中修改权限
4. `sudo chown -R <User/Owner>:<Group> Folder`

`chmod` (Change Mode)
1. 解决 **你能做什么？(权限)** 的问题
2. 设置 修改 文件的 读(r)、写(w)、执行(x) 权限
3. 只有文件或目录的 Owner(所有者) 或 root 用户 才能运行 `chmod` 来修改文件的权限
4. 2种模式
   1. **符号模式** (Symbolic Mode)
      1. `chmod +x filename` : 为所有用户(Owner, Group, Others) 添加执行 (x) 权限
   2. **数值模式** (Numeric Mode)  : r=4  | w=2 | x=1
      1. `chmod 777 filename` : 3位，分别对应 (Owner, Group, Others)，7=4+2+1，rwx 权限，授予所有用户 对文件或目录的 完全 读、写、执行 权限



