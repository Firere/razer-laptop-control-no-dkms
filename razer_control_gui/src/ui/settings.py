import os

import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk
from ui.const import args

# TODO: test update

class settings(Gtk.Box):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.update_button = Gtk.Button(label="Check for updates")
		self.update_button.connect("clicked", self.update_button_clicked)

		self.restart_button = Gtk.Button(label="Done! Restart to update")
		self.restart_button.hide()

		self.uninstall_window_keep = Gtk.Button(
			label="Uninstall, keep settings",
			margin_start=20,
			margin_top=20,
			margin_bottom=20,
			margin_end=20,
		)
		self.uninstall_window_remove = Gtk.Button(
			label="Uninstall, remove settings",
			margin_start=20,
			margin_top=20,
			margin_bottom=20,
			margin_end=20,
		)

		self.uninstall_window_button_box = Gtk.Box(
			halign=Gtk.Align.CENTER, orientation=Gtk.Orientation.HORIZONTAL
		)
		self.uninstall_window_button_box.append(self.uninstall_window_keep)
		self.uninstall_window_button_box.append(self.uninstall_window_remove)

		self.uninstall_window_label = Gtk.Label(
			justify=Gtk.Justification.CENTER,
			margin_start=20,
			margin_bottom=20,
			margin_end=20,
		)
		self.uninstall_window_label.set_markup(
			"<small><i>Settings are located in </i><span background='black' face='monospace' foreground='gray'>~/.local/share/razercontrol</span>.\n<i>To delete them, run </i><span background='black' face='monospace' foreground='gray'>rm -rf ~/.local/share/razercontrol</span><i> in the terminal.</i></small>"
		)

		self.uninstall_window_label_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		self.uninstall_window_label_box.append(self.uninstall_window_label)

		self.uninstall_window_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		self.uninstall_window_box.append(self.uninstall_window_button_box)
		self.uninstall_window_box.append(self.uninstall_window_label_box)

		self.uninstall_window = Gtk.Window(
			resizable=False, title="Uninstall Razer Laptop Control"
		)
		self.uninstall_window.set_child(self.uninstall_window_box)

		self.uninstall_button = Gtk.Button(label="Uninstall")

		self.uninstall_button.connect("clicked", self.uninstall_button_clicked)

		self.append(self.update_button)
		self.append(self.uninstall_button)

	def update_button_clicked(self, _):
		self.update_button.set_label("Checking...")
		try:
			if (
				os.popen(
					"pkexec --user root echo 'cd /usr/share/razercontro/repo && git pull' | bash"
				).read()[0]
				!= "A"  # If it is up-to-date, it outputs "Already up to date."
			):
				self.update_button.set_label("Installing...")
				os.system("pkexec --user root /usr/share/razercontrol/repo/install.sh")
				self.update_button.hide()
				self.restart_button.show()
			else:
				self.update_button.set_label("Up to date")
		except:  # Presumably, the user cancelled the operation
			self.update_button.set_label("Check for updates")

	def uninstall_button_clicked(self, _):
		self.uninstall_window.present()


box = settings(**args)
