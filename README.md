# Hyprland 桌面

![image-20240511013659908](./assets/image-20240511013659908.png)

![1](./assets/1.png)

**[English](en.md)**

本仓库是基于[Hyde](https://github.com/kRHYME7/Hyde-cli)自定义的hyprland主题。

## 工具

列举一些我常用的工具

- 微信（AUR包还没支持wayland高分辨率缩放，我在安装脚本里实现了个简陋的fix。。）
- Spotify（免费听歌，要梯子，可pojie去广告）
- Steam（原神启动！）
- input-remapper（不错的键盘重映射工具，可以实现宏）
- Typora（最好用的markdown编辑器！）
- kitty（GPU加速的好看终端）
- fastfetch（好看就完了）
- zoxide（模糊匹配+动态权重的cd命令，已经替换cd）
- fzf（模糊搜索命令行工具）
- wlsunset（夜间模式，工具栏的🌙图标）
- fcitx5（中文输入法）

## 安装

最好用Arch Linux，或者其他使用AUR的Linux发行版应该也可，比如Manjaro

首先先安装[Hyde](https://github.com/kRHYME7/Hyde-cli), 包管理选**yay**，命令行选**zsh**

```
pacman -Sy git
git clone --depth 1 https://github.com/prasanthrangan/hyprdots ~/HyDE
cd ~/HyDE/Scripts
./install.sh
```

安装完先不要重启，然后运行

```
git clone https://github.com/cyrus-xc/hyprland-dotfile/tree/main ~/Download/hyprland-dotfile
cd ~/Download/hyprland-dotfile
./setup.sh
```

重启

## Nvidia

#### 我用N卡

安装nvidia-drm就行，依赖会自动装上

```
yay -Sy nvidia-drm
```

然后修改grub启动参数

```
sudo nano /etc/default/grub
```

找到GRUB_CMDLINE_LINUX这一行，在参数后面加上`nouveau.modeset=0 nvidia_drm.modeset=1 nvidia.NVreg_PreserveVideoMemoryAllocations=1`。然后重新生成grub.cfg文件

```
sudo grub-mkconfig -o /boot/grub/grub.cfg
sudo grub-install --target=x86_64-efi --efi-directory=/boot/efi --bootloader-id=GRUB
```

重启。

> 更多细节参考[wiki](https://wiki.hyprland.org/Nvidia/)



#### 我不用N卡

emm

听说Intel集显和AMD独显/集显都是可以用nouveau的，arch自带显示驱动，但是我没用过，只能给大致的方案：

1. 编辑`~/.config/hypr/nvidia.conf`，把所有的东西注释掉

2. 查找是否安装nvdia驱动，有的话就`yay -R`卸载。查找命令：`pacman -Qq | fzf --preview 'pacman -Qil {}' --layout=reverse --bind 'enter:execute(pacman -Qil {} | less)'`

3. 取消对 Nouveau 驱动程序的屏蔽。具体操作是在 `/etc/modprobe.d/nouveau_blacklist.conf` 或者 `/usr/lib/modprobe.d/nvidia-utils.conf` 文件中注释掉对 Nouveau 的屏蔽，修改成如下：

   ```
   #blacklist nouveau
   ```

