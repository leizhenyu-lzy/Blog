bash
1. 终端补全忽略大小写
   1. echo 'set completion-ignore-case on' >> /etc/inputrc
   2. echo 'set completion-ignore-case on' >> ~/.inputrc
2. ros
   1. wget http://fishros.com/install -O fishros && . fishros
3. time
   1. sudo apt install ntpdate # 必须要sudo
   2. sudo ntpdate time.windows.com # 进行时间同步并检查
   3. sudo hwclock --localtime --systohc # 修改时间机制为localtime，并同步bios硬件时间


apt
1. git
2. pavucontrol
3. nodejs
4. dotnet8
5. gthumb
6. python3-pip
7. gcc
8. g++
9. meshlab
10. flameshot
11. synaptic : sudo apt install -y synaptic
12. tree
13. gnome-sound-recorder
14. clang
15. cmake
16. net-tools
17. ubuntu-restricted-extras(基本的媒体编解码器)
18. gnome-sound-recorder
19. neofetch
20. openjdk-11-jdk
    1. java -version
    2. javac -version
21. gpustat
22. remmina & filezilla
23. cheese
24. ffmpeg
25. gnome-clocks
26. gnome-tweaks
    1. chrome-gnome-shell
    2. gnome-shell --version (GNOME Shell 42.9)
    3. extension : https://chrome.google.com/webstore/detail/gnome-shell-integration/gphhapmejobijbbhgpjhcjognlahblep
    4. Clipboard Indicator
    5. Net Speed
    6. Sound Input & Output Device Chooser
    7. Network Stats
    8. gTile
    9. Extension List
    10. Vitals
    11. Panel World Clock (Lite)
    12. Weather O'Clock
27. p7zip p7zip-full p7zip
28. mysql-server
    1. mysql -V
    2. sudo mysql
    3. ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password by 'your new password';  # 输入自己新设置的密码
29. gnome-todo
30. npm
31. build-essential
32. gnome-weather
33. vlc
34. ntfs-3g
35. exfat-fuse









Web
1. edge
   1. github
   2. whatsapp
   3. bilibili - https://github.com/the1812/Bilibili-Evolved
2. vscode
3. qq
4. wechat
5. wps
6. 向日葵
   1. https://d.oray.com/sunlogin/doc/%E8%B4%9D%E9%94%90%E5%90%91%E6%97%A5%E8%91%B5IT%E8%BF%90%E7%BB%B4%E8%A7%A3%E5%86%B3%E6%96%B9%E6%A1%88%E5%AE%89%E5%85%A8%E7%99%BD%E7%9A%AE%E4%B9%A6.pdf
7. sogou
   1. sudo apt install fcitx
   2. sudo apt install fcitx-bin
   3. sudo apt install fcitx-table
   4. sudo apt install libqt5qml5 libqt5quick5 libqt5quickwidgets5 qml-module-qtquick2
   5. sudo apt install libgsettings-qt1
8. eudic & ting_en
9.
10. miniconda
    1. https://docs.anaconda.com/miniconda/install/
    2. conda config --set auto_activate_base false
11. Docker - TODO
12. BaiduNetdisk
13. foxglove : https://foxglove.dev/download
14. obs : https://obsproject.com/download
15. unity : https://docs.unity3d.com/hub/manual/InstallHub.html#install-hub-linux
16. docker : https://docs.docker.com/desktop/setup/install/linux/ubuntu/
    1. sign in desktop : https://docs.docker.com/desktop/setup/sign-in/#signing-in-with-docker-desktop-for-linux


Ubuntu Software / Snap
1. slack
2. discord
3. dbeaver-ce
4. zoom
5. shotcut
6. blender
7. FreeCAD
8. drawio
9. pomatez 计时器
10. htop (cpu monitor)
11. steam




pip3
1. torch torchvision torchaudio
   1. libtorch [Installing C++ Distributions of PyTorch](https://pytorch.org/cppdocs/installing.html)
   2. `python3 -c 'import torch;print(torch.utils.cmake_prefix_path)'` 检查 PyTorch 的 CMake 配置文件的路径
   3. `cmake -DCMAKE_PREFIX_PATH/home/lzy/Projects/libtorch-cxx11-abi-shared-with-deps-2.5.1+cu124/libtorch ..`
2. opencv-python
3. plyfile
4. tqdm
5. pandas
6. numpy
7. scipy
8. matplotlib
9.  scikit-learn
10. seaborn
11. beautifulsoup4
12. ipykernel





NVIDIA
1. Close Secure Boot
2. Driver : https://www.nvidia.cn/geforce/drivers/  (Production Branch)
   1. chmod +x NVIDIA-Linux-x86_64-xxx.xxx.run
   2. sudo bash NVIDIA-Linux-x86_64-xxx.xxx.run
3. CUDA : https://developer.nvidia.com/cuda-toolkit-archive runfile(local)
   1. wget https://developer.download.nvidia.com/xxx/cuda_xxx_linux.run
   2. sudo sh cuda_xxx_linux.run
   3. add to PATH (~/.bashrc)
      1. export PATH=/usr/local/cuda/bin:${PATH}
      2. export LD_LIBRARY_PATH=/usr/local/cuda/lib64:${LD_LIBRARY_PATH}
      3. P.S. : ls /usr/local -l : cuda -> /usr/local/cuda-12.4/ (soft link)
   4. uninstall : 使用 /usr/local/cuda-<version>/bin 中的 cuda-uninstaller
4. cuDNN : https://developer.nvidia.com/rdp/cudnn-archive
   1. sudo apt install ./cudnn-xxx.deb
   2. 可能位置 /home/lzy/.local/lib/python3.10/site-packages/nvidia/cudnn/include/cudnn_version.h
   3. cat cudnn_version.h_path | grep CUDNN_MAJOR -A 2

```python
>>> import torch
>>> print(torch.__version__)
2.5.1+cu124
>>> print(torch.version.cuda)
12.4
>>> print(torch.backends.cudnn.version())
90100
>>> print(torch.cuda.get_device_name(0))
```


Other
1. beyond compare 4
2. Matlab - TODO
3. Clash - TODO




