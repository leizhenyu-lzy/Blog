# Linux 命令

**Table of Contents**
- [Linux 命令](#linux-命令)
- [进程 Process (`ps` \& `top` \& `htop` \& `kill` \& `pkill` \& `pgrep`)](#进程-process-ps--top--htop--kill--pkill--pgrep)
- [内存 (`free`)](#内存-free)
- [存储 (`fdisk / gdisk / parted` \& `mkfs` \& `blkid`)](#存储-fdisk--gdisk--parted--mkfs--blkid)
- [挂载 (`lsblk` \& `mount` \& `umount`)](#挂载-lsblk--mount--umount)
- [权限修改 (`chmod` \& `chown`)](#权限修改-chmod--chown)

---

# 进程 Process (`ps` & `top` & `htop` & `kill` & `pkill` & `pgrep`)

**`ps`** (Process Status) : 查看进程状态，默认只显示当前终端的进程
1. **`ps aux`** : 最常用的进程查看命令
   1. `a` (all)             : 显示所有用户的进程
   2. `u` (user-oriented)   : 以用户为导向的格式显示详细信息
   3. `x`                   : 显示没有控制终端的进程（后台进程、守护进程）
2. **输出列说明**
   1. `USER`    : 进程所有者 用户名
   2. `PID`     : 进程ID (Process ID)，系统唯一标识
   3. `%CPU`    : CPU 使用率 百分比
   4. `%MEM`    : 物理内存 使用率 百分比
   5. `VSZ`     : **虚拟内存**   大小 (Virtual Memory Size)，单位 KB
   6. `RSS`     : **实际物理内存**大小 (Resident Set Size)，单位 KB
   7. `TTY`     : 关联的终端类型，`?` 表示无控制终端（守护进程）
   8. `STAT`    : 进程状态码（组合状态 = 主状态 + 附加属性）
      1. **主状态** (第一个字母)
         - `R` (Running)        : 正在运行或可运行(在运行队列中)
         - `S` (Sleeping)       : 可中断睡眠(等待事件完成，如 I/O、用户输入)
         - `D` (Disk Sleep)     : 不可中断睡眠(通常是等待磁盘 I/O，无法被信号中断)
         - `Z` (Zombie)         : 僵尸进程(已终止但未被父进程回收)
         - `T` (Stopped)        : 已停止(被信号暂停，如 Ctrl+Z)
         - `I` (Idle)           : 空闲的内核线程
      2. **附加属性** (后续字符)
         - `<`                  : 高优先级进程(nice 值 < 0)
         - `N`                  : 低优先级进程(nice 值 > 0)
         - `L`                  : 有页面锁在内存中(用于实时进程)
         - `s`                  : 会话领导者(session leader)，通常是 shell 或守护进程
         - `l`                  : 多线程进程(使用 POSIX 线程)
         - `+`                  : 前台进程组(与终端关联且在前台运行)
   9. `START`    : 进程启动时间
   10. `TIME`    : 进程累计占用 CPU 的时间
   11. `COMMAND` : 启动进程的 完整命令行
3. **常用组合**
   1. `ps aux | grep <进程名>` : 查找特定进程
   2. `ps aux --sort=-%cpu | head -n 10` : 按 CPU使用率 排序，显示前10个
   3. `ps aux --sort=-%mem | head -n 10` : 按 内存使用率 排序，显示前10个
   4. `ps -ef` : 另一种常用格式，显示 完整命令行 & 父进程ID(PPID)


**`top`** : 动态实时查看系统进程信息
1. **交互命令** (在 top 运行时按下)
   - `h` / `?` : 显示帮助信息
   - `q` : 退出 top
   - `k` : 杀死进程(输入 PID)
   - `r` : 重新设置进程优先级(renice)
   - `d` / `s` : 设置刷新间隔(秒)
   - `1` : 切换 显示 每个 CPU 核心的使用率 / 总体使用率
   - `c` : 切换 显示 命令名/完整命令行
2. **启动选项**
   - `top -u <username>` : 只显示指定用户的进程
   - `top -p <PID>` : 只监控指定 PID 的进程
   - `top -d <秒数>` : 设置刷新间隔
   - `top -n <次数>` : 刷新指定次数后退出

**`htop`** : 更强大、更友好的 `top` 替代品 (安装 `sudo apt install htop`)
1. 支持鼠标操作、彩色显示、树状视图
2. 安装 : `sudo apt install htop` (Ubuntu/Debian) 或 `sudo yum install htop` (CentOS/RHEL)


`pgrep` / `pkill`

**`pgrep`** (Process Grep) : 根据名称查找进程的PID
- `pgrep <进程名>` : 输出匹配进程的PID
- `pgrep -l <进程名>` : 同时显示PID和进程名
- `pgrep -u <username>` : 查找指定用户的进程

**`pkill`** (Process Kill) : 根据名称直接杀死进程
- `pkill <进程名>` : 杀死所有匹配的进程
- `pkill -9 <进程名>` : 强制杀死（相当于 `kill -9`）
- `pkill -u <username>` : 杀死指定用户的所有进程


**`kill` / `killall`**

**`kill`** : 向进程发送信号（通常用于终止进程）
1. `kill <PID>` : 发送默认信号 `SIGTERM`(15)，请求进程优雅退出
2. `kill -9 <PID>` : 发送 `SIGKILL`(9) 信号，强制立即终止进程（无法被捕获或忽略）
3. `kill -15 <PID>` : 等同于 `kill <PID>`，发送 `SIGTERM` 信号
4. `kill -l` : 列出所有可用的信号

**常用信号**
- `1 (SIGHUP)` : 重新加载配置文件（挂起）
- `2 (SIGINT)` : 中断（相当于 Ctrl+C）
- `9 (SIGKILL)` : 强制杀死，无法被捕获
- `15 (SIGTERM)` : 请求终止，可以被捕获和处理（优雅退出）
- `18 (SIGCONT)` : 继续执行已停止的进程
- `19 (SIGSTOP)` : 停止进程（无法被捕获）

**`killall`** : 根据进程名杀死所有匹配的进程
- `killall <进程名>` : 杀死所有同名进程
- `killall -9 <进程名>` : 强制杀死所有同名进程


`jobs` / `fg` / `bg` / `nohup` / `&`

**后台任务管理**

**`&`** : 在命令末尾添加，将进程放到后台运行
- `command &` : 启动后台进程
- 示例 : `python train.py &`

**`jobs`** : 列出当前终端的后台任务
- `jobs -l` : 显示任务的PID

**`fg`** (Foreground) : 将后台任务调到前台
- `fg` : 将最近的后台任务调到前台
- `fg %<job_id>` : 将指定任务号调到前台

**`bg`** (Background) : 将已停止的任务在后台继续运行
- `bg` : 继续运行最近停止的任务
- `bg %<job_id>` : 继续运行指定任务号

**`Ctrl+Z`** : 暂停前台进程（发送 `SIGTSTP` 信号）
- 然后可以用 `bg` 让它在后台继续运行，或用 `fg` 恢复到前台

**`nohup`** (No Hang Up) : 使命令在退出终端后继续运行
- `nohup command &` : 后台运行，且不受终端关闭影响
- 输出默认重定向到 `nohup.out` 文件
- 示例 : `nohup python train.py > output.log 2>&1 &`


`nice` / `renice`

调整进程优先级（-20 到 19，数值越小优先级越高）

**`nice`** : 启动进程时设置优先级
- `nice -n <优先级> command` : 以指定优先级运行命令
- 示例 : `nice -n 10 ./heavy_computation.sh` (降低优先级)

**`renice`** : 修改运行中进程的优先级
- `renice <优先级> -p <PID>` : 修改指定进程的优先级
- 示例 : `renice -5 -p 12345` (提高优先级，需要权限)


其他进程相关命令

**`pidof`** : 查找运行中程序的PID
- `pidof <程序名>` : 输出所有匹配的PID

**`lsof`** (List Open Files) : 列出打开的文件和网络连接
- `lsof -p <PID>` : 查看进程打开的所有文件
- `lsof -i :<端口号>` : 查看占用指定端口的进程
- 示例 : `lsof -i :8080` (查看占用8080端口的进程)

**`pstree`** : 以树状结构显示进程之间的父子关系
- `pstree -p` : 显示PID
- `pstree -u` : 显示用户名

**`watch`** : 周期性执行命令并显示输出
- `watch -n <秒数> <命令>` : 每隔指定秒数执行一次
- 示例 : `watch -n 2 'ps aux | grep python'` (每2秒刷新一次)






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


---

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


---

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



