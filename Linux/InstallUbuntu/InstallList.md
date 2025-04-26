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


---


apt
1. git
   1. beautify - https://github.com/leizhenyu-lzy/Blog/blob/main/ComputerScience/Git/GitInShell.md
   2. git config --global user.email lzy20190501@gmail.com
   3. sudo sh cuda_12.4.0_550.54.14_linux.run
2. pavucontrol
3. nodejs
4. dotnet8
5. curl
6. gthumb
7. python3-pip
8. python3-venv
9.  gcc
10. g++
11. meshlab
12. flameshot
13. synaptic : sudo apt install -y synaptic
14. tree
15. gnome-sound-recorder
16. clang
17. cmake
18. net-tools
19. ubuntu-restricted-extras(基本的媒体编解码器)
20. neofetch
21. openjdk-11-jdk
    1. java -version
    2. javac -version
22. gpustat
23. remmina & filezilla
24. cheese
25. kazam
26. ffmpeg
27. gnome-clocks
28. gnome-tweaks
    1. sudo apt install chrome-gnome-shell
    2. sudo apt install gnome-shell-extensions
    3. install position : /home/lzy/.local/share/gnome-shell/extensions
    4. gnome-shell --version (GNOME Shell 42.9)
    5. extension : https://chrome.google.com/webstore/detail/gnome-shell-integration/gphhapmejobijbbhgpjhcjognlahblep
    6. Clipboard Indicator
    7. Net Speed
    8. Sound Input & Output Device Chooser
    9. Network Stats
    10. gTile
    11. Extension List
    12. Vitals
    13. Panel World Clock (Lite)
    14. Weather O'Clock
29. p7zip p7zip-full p7zip
30. mysql-server
    1. mysql -V
    2. sudo mysql
    3. ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password by 'your new password';  # 输入自己新设置的密码
31. gnome-todo
32. npm
33. build-essential
34. gnome-weather
35. vlc
36. ntfs-3g
37. exfat-fuse
38. sudo apt install ca-certificates apt-transport-https software-properties-common lsb-release -y
39. sudo apt install blueman bluez*  (蓝牙自启动)



冻结 & 解冻
1. sudo apt-mark hold/unhold package_name



---



Web
1. edge
   1. 历史版本 - https://packages.microsoft.com/repos/edge/pool/main/m/microsoft-edge-stable/ - 如果无法输入中文，可以尝试安装之前版本
   2. github
   3. whatsapp
   4. bilibili - https://github.com/the1812/Bilibili-Evolved
2. vscode
3. qq
4. ros
5. wechat
6. wps
7. 向日葵
   1. https://d.oray.com/sunlogin/doc/%E8%B4%9D%E9%94%90%E5%90%91%E6%97%A5%E8%91%B5IT%E8%BF%90%E7%BB%B4%E8%A7%A3%E5%86%B3%E6%96%B9%E6%A1%88%E5%AE%89%E5%85%A8%E7%99%BD%E7%9A%AE%E4%B9%A6.pdf
8. sogou
   1. sudo apt install fcitx
   2. sudo apt install fcitx-bin
   3. sudo apt install fcitx-table
   4. sudo apt install libqt5qml5 libqt5quick5 libqt5quickwidgets5 qml-module-qtquick2
   5. sudo apt install libgsettings-qt1
   6. sudo cp /usr/share/applications/fcitx.desktop /etc/xdg/autostart/
   7. sudo apt purge ibus
   8. sudo apt -f install
   9. Fcitx Configuration 中 手动 添加 sogoupinyin，注意 不要 勾选 Only Show Current Language
9.  eudic & ting_en
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
17. whatsapp 网页栏 添加 到桌面
18. youtube music 网页栏 添加 到桌面
19. cursor : https://www.cursor.com/cn
    ```txt
      [Desktop Entry]
      Name=Cursor
      Comment=Cursor
      Type=Application
      Icon=/usr/share/pixmaps/cursor.png
      Exec=/home/lzy/Tools/Cursor/Cursor.AppImage
      Terminal=false
      StartupNotify=true
      Categories=Application;Development;
    ```

---


Ubuntu Software / Snap
1. slack
2. discord
3. dbeaver-ce
4. zoom-client
5. shotcut
6. blender --classic
7. freecad
8. drawio
9. pomatez 计时器
10. htop (cpu monitor)
11. steam
12. xmind

---


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
2. BIOS select **Discrete Graphics**
3. nvidia-detector 查看 driver 选择 后续对应版本
4. Driver : https://www.nvidia.cn/geforce/drivers/  (Production Branch)
   1. chmod +x NVIDIA-Linux-x86_64-xxx.xxx.run
   2. sudo bash NVIDIA-Linux-x86_64-xxx.xxx.run
   3. uninstall : sudo ./NVIDIA*.run --uninstall
5. CUDA : https://developer.nvidia.com/cuda-toolkit-archive runfile(local)
   1. wget https://developer.download.nvidia.com/xxx/cuda_xxx_linux.run
   2. sudo sh cuda_xxx_linux.run (如果上一步正确，不要选 driver)
   3. add to PATH (~/.bashrc) (如果正确，会有添加环境变量的提示)
      1. export PATH=/usr/local/cuda/bin:${PATH}
      2. export LD_LIBRARY_PATH=/usr/local/cuda/lib64:${LD_LIBRARY_PATH}
      3. P.S. : ls /usr/local -l : cuda -> /usr/local/cuda-12.4/ (soft link)
   4. uninstall : 使用 /usr/local/cuda-<version>/bin 中的 cuda-uninstaller
6. cuDNN : https://developer.nvidia.com/rdp/cudnn-archive
   1. sudo apt install ./cudnn-xxx.deb
   2. 根据提示可能需要类似操作 : sudo cp /var/cudnn-local-repo-ubuntu2204-8.9.7.29/cudnn-local-08A7D361-keyring.gpg /usr/share/keyrings/
   3. 可能位置 /home/lzy/.local/lib/python3.10/site-packages/nvidia/cudnn/include/cudnn_version.h
   4. cat cudnn_version.h_path | grep CUDNN_MAJOR -A 2

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


lsmod | grep nvidia
systemctl status gdm / systemctl status display-manager
sudo update-initramfs -u




fonts
1. 将字体解压缩到 **`/usr/share/fonts`** (或`~/.local/share/fonts`)，以在系统范围内安装字体
2. `fc-cache -f -v`


desktop
```
[Desktop Entry]
Type=Application
Name=ICQ
Icon=/path/to/icon.png
Exec=/path/to/executable
Terminal=false
```





Other
1. beyond compare 4
2. Matlab - TODO
3. Clash - TODO




`/etc/apt/sources.list.d` 用于存放附加的软件源列表文件，每个文件里都可以列出一组 APT 仓库地址，格式和 `/etc/apt/sources.list` 一样
1. 很多 `.deb` 包在安装时会往这里添加自己的源
2. 可以单独启用/禁用某些软件源，而不用改 `/etc/apt/sources.list`




