#!/bin/bash

cargo build --release

systemctl --user stop razerdaemon.service
mkdir -p ~/.local/share/razercontrol
sudo /bin/bash << EOF
mkdir -p /usr/share/razercontrol/bin
git clone https://github.com/phush0/razer-laptop-control-no-dkms.git /usr/share/razercontrol/repo
echo -e "#!/usr/bin/bash\n\ncd /usr/share/razercontrol/repo/razer_control_gui/src\npython3 gui.py" > /usr/bin/razercontrol-gui
cp src/update.sh /usr/share/razercontrol/bin/update
chmod +x /usr/share/razercontrol/bin/update
cp src/uninstall.sh /usr/share/razercontrol/bin/uninstall
chmod +x /usr/share/razercontrol/bin/uninstall
systemctl stop razerdaemon.service
cp target/release/razer-cli /usr/bin/
cp target/release/daemon /usr/share/razercontrol/
cp data/devices/laptops.json /usr/share/razercontrol/
cp data/udev/99-hidraw-permissions.rules /etc/udev/rules.d/
cp razerdaemon.service /usr/lib/systemd/user/
udevadm control --reload-rules
cp razercontrol.desktop /usr/share/applications/
cp assets/logo1.png /usr/share/razercontrol/
cp assets/logo2.png /usr/share/razercontrol/
cp assets/logo3.png /usr/share/razercontrol/
EOF
systemctl --user enable razerdaemon.service
systemctl --user start razerdaemon.service
echo "Install complete!"
