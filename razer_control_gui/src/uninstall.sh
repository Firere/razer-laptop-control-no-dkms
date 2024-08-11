#!/usr/bin/bash

# If a user's home directory was specified in the first argument, then remove their settings too
if ! [[ -z "$1" ]]; then
	rm -rf "$1/.local/share/razercontrol"
fi

sudo /usr/bin/bash << EOF
rm -rf /usr/share/razercontrol
rm /usr/bin/razer-cli
rm /usr/bin/razercontrol-gui
EOF
