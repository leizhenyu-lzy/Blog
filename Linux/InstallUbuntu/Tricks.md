系统设置(settings)消失

```bash
sudo apt-get install unity-control-center
sudo apt-get install gnome-control-center
# 没有立即生效尝试注销用户或重启
```

桌面不显示文件
```bash
gedit ~/.config/user-dirs.dirs  # XDG_DESKTOP_DIR 一项改成"$HOME/Desktop"
sudo apt install gnome-shell-extension-desktop-icons-ng
sudo apt install gnome-shell-extension-prefs
```

Desktop Icon
1. `/usr/share/applications`
2. `~/.local/share/applications`
3. `~/.local/share/applications/wine/Programs`



