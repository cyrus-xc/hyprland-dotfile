 #!/bin/bash

# Check if Hyde is installed
if ! command -v Hyde &> /dev/null; then
    echo "Hyde for hyprland is not installed. Please refer to readme at https://github.com/cyrus-xc/hyprland-dotfile"
    exit 1
fi

# Check if yay is installed
if ! command -v yay &> /dev/null; then
    echo "yay is not your default AUR package manager, please install yay before continuing."
    exit 1
fi

# Install packages using yay
yay -S visual-studio-code-bin google-chrome input-remapper-git stress-ng typora wechat-universal zoom font-manager fzf zoxide fcitx5-im fcitx5-pinyin-zhwiki

# Get the monitor scaling factor
scale=$(hyprctl monitors all | grep -Po '(?<=scale: )[0-9.]+')

# Prompt the scale variable
echo "Monitor scaling factor: $scale"

# Copy and modify the WeChat desktop file
cp /usr/share/applications/wechat-universal.desktop $HOME/.local/share/applications/wechat-universal.desktop
sed -i 's/^Exec=.*/Exec=env QT_SCALE_FACTOR='"$scale"' XCURSOR_SIZE=16 QT_IM_MODULE=fcitx wechat-universal %u/' $HOME/.local/share/applications/wechat-universal.desktop

# Append the zoxide initialization line to ~/.zshrc
echo '# zoxide' >> $HOME/.zshrc
echo 'eval "$(zoxide init --cmd cd zsh)"' >> $HOME/.zshrc

# Create and append to the electron-flags.conf file
echo "--enable-features=UseOzonePlatform" > $HOME/.config/electron-flags.conf
echo "--enable-features=WaylandWindowDecorations" >> $HOME/.config/electron-flags.conf
echo "--enable-features=WebRTCPipeWireCapturer" >> $HOME/.config/electron-flags.conf
echo "--ozone-platform-hint=auto" >> $HOME/.config/electron-flags.conf
echo "--ozone-platform=wayland" >> $HOME/.config/electron-flags.conf
echo "--enable-wayland-ime" >> $HOME/.config/electron-flags.conf

# Copy .config folder from the same level as the script to $HOME directory
cp -r "$(dirname "$0")/.config" $HOME

# Run kbuildsycoca6
XDG_MENU_PREFIX=arch- kbuildsycoca6

# Copy arch-applications.menu to applications.menu
sudo cp /etc/xdg/menus/arch-applications.menu /etc/xdg/menus/applications.menu


echo "Finished"
