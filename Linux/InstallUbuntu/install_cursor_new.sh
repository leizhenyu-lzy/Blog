#!/bin/bash
# Ubuntu安装Cursor脚本
# 版本：1.2.1
# 作者：DIC_lijx19
# 更新：2025-04-23
set -euo pipefail

# 错误处理函数
trap 'echo -e "\n${RED}安装被中断！退出代码 $?"${NC}; exit 130' INT
trap 'echo -e "\n${RED}发生错误！在行号 $LINENO"${NC}; exit 1' ERR

# 初始化颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

# 1.定义部署参数
APP_NAME="Cursor"
INSTALL_DIR="/opt"

# APP_IMAGE="${INSTALL_DIR}/cursor.appimage"
# ICON_PATH="${INSTALL_DIR}/cursor.png"

APP_IMAGE="/usr/share/applications/cursor.AppImage"
ICON_PATH="/usr/share/pixmaps/cursor.png"

DESKTOP_ENTRY="/usr/share/applications/cursor.desktop"
APP_URL="https://downloads.cursor.com/production/ec408037b24566b11e6132c58bbe6ad27046eb91/linux/x64/Cursor-0.49.4-x86_64.AppImage"
ICON_URL="https://registry.npmmirror.com/@lobehub/icons-static-png/latest/files/dark/cursor.png"


# 2.检查是否已安装
if [ -f "$APP_IMAGE" ]; then
    echo "$APP_NAME 已安装，位置：$APP_IMAGE"
    exit 0
fi

# 3.安装必要依赖
install_dependencies() {
    echo "检查系统依赖..."

    # 识别发行版
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        OS=$ID
        VER=$VERSION_ID
    else
        echo -e "${RED}无法识别Linux发行版${NC}"
        exit 1
    fi

    # 安装libfuse2（Ubuntu/Debian）
    if ! dpkg -l libfuse2 | grep -q '^ii'; then
        echo "安装libfuse2..."

        case $OS in
            ubuntu|debian)
                sudo apt-get update -qq
                sudo apt-get install -y -qq libfuse2
                ;;
            *)
                echo -e "${RED}不支持的系统：$OS${NC}"
                exit 1
                ;;
        esac

        # 验证安装
        if ! ldconfig -p | grep -q libfuse.so.2; then
            echo -e "${RED}libfuse2安装失败！${NC}"
            exit 1
        fi
    fi

    # 安装wget（如果不存在）
    if ! command -v wget &> /dev/null; then
        echo "安装wget..."
        sudo apt-get install -y -qq wget
    fi
}

install_dependencies

# 4.下载文件（使用sudo保证安装到系统目录）
echo "下载Cursor AppImage..."
sudo wget --tries=3 --timeout=30 -O "$APP_IMAGE" "$APP_URL"
sudo chmod +x "$APP_IMAGE"

echo "下载图标..."
sudo wget --tries=3 --timeout=15 -O "$ICON_PATH" "$ICON_URL"

# 5.创建桌面菜单项
echo "创建桌面入口..."
sudo tee "$DESKTOP_ENTRY" > /dev/null <<EOF
[Desktop Entry]
Type=Application
Name=$APP_NAME
Exec=$APP_IMAGE --no-sandbox %U
Icon=$ICON_PATH
Categories=Development;
Terminal=false
StartupWMClass=cursor
EOF

# 6.更新菜单缓存
sudo update-desktop-database


# 7.设置权限
sudo chmod +x "$APP_IMAGE"
sleep 5

echo "安装完成！请通过应用程序菜单启动Cursor"