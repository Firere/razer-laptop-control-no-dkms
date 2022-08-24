#!/bin/bash

cargo build --release

systemctl --user stop razerdaemon.service
mkdir -p ~/.local/share/razercontrol
sudo /bin/bash << EOF
mkdir -p /usr/share/razercontrol
systemctl stop razerdaemon.service
cp target/release/razer-cli /usr/bin/
cp target/release/daemon /usr/share/razercontrol/
cp data/devices/laptops.json /usr/share/razercontrol/
cp data/udev/99-hidraw-permissions.rules /etc/udev/rules.d/
cp razerdaemon.service /usr/lib/systemd/user/
udevadm control --reload-rules
cp src/gui.py /usr/bin/razercontrol-gui
chmod +x /usr/bin/razercontrol-gui
mv razercontrol.desktop /usr/share/applications/razercontrol.desktop
mv assets/logo1.png /usr/share/razercontrol/logo1.png
mv assets/logo2.png /usr/share/razercontrol/logo2.png
mv assets/logo3.ong /usr/share/razercontrol/logo3.png
EOF
systemctl --user enable razerdaemon.service
systemctl --user start razerdaemon.service
echo "Install complete!"
