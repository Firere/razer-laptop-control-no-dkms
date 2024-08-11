#!/usr/bin/python3

import gi

gi.require_versions({ "Gtk": "4.0", "Adw": "1"})
import os
import sys

from gi.repository import Adw, GdkPixbuf, Gtk

from ui import effects, fan, lighting, power, settings


class ApplicationWindow(Gtk.ApplicationWindow):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		os.system("systemctl --user restart razerdaemon")

		self.set_default_size(900, 800)
		# self.set_icon_from_file("/usr/share/razercontrol/logo2.png")
		# self.set_icon(
		#	 GdkPixbuf.Pixbuf.new_from_file("/usr/share/razercontrol/logo1.png")
		# )

		# Header bar
		self.header_bar = Gtk.HeaderBar()
		self.title = Gtk.Label()
		self.title.set_text("Razer Laptop Control")
		self.header_bar.set_title_widget(self.title)
		self.header_bar.set_show_title_buttons(True)
		self.about_dialog_button = Gtk.Button(label="About")
		self.header_bar.pack_start(self.about_dialog_button)
		self.set_titlebar(self.header_bar)

		# About dialog
		self.about_dialog = Gtk.AboutDialog()
		self.logo3 = Gtk.Image.new_from_file("/usr/share/razercontrol/logo3.png")
		self.about_dialog.set_logo(self.logo3.get_paintable())
		self.about_dialog.set_program_name("Razer Laptop Control")
		self.about_dialog.set_comments(
			"This program is not in any way affiliated with Razer Inc. The trisnake logo is full property of Razer Inc."
		)
		self.about_dialog.set_website_label("GitHub repository")
		self.about_dialog.set_website(
			"https://github.com/phush0/razer-laptop-control-no-dkms"
		)
		self.about_dialog.set_license_type(Gtk.License.GPL_2_0)
		self.about_dialog.set_authors(
			["phusho (GitHub: phush0) - project maintainer", "Firere - GUI"]
		)
		self.about_dialog.set_artists(["Firere - LC Logo"])
		self.about_dialog_header_bar = Gtk.HeaderBar()
		self.about_dialog_title = Gtk.Label()
		self.about_dialog_title.set_text("About")
		self.about_dialog_button.connect("clicked", self.about_dialog_button_clicked)

		settings.box.restart_button.connect("clicked", self.restart_button_clicked)
		settings.box.uninstall_window_keep.connect(
			"clicked", self.uninstall_window_keep_clicked
		)
		settings.box.uninstall_window_remove.connect(
			"clicked", self.uninstall_window_remove_clicked
		)

		self.stack = Gtk.Stack(
			transition_duration=200,
			transition_type=Gtk.StackTransitionType.SLIDE_LEFT_RIGHT,
		)
		self.stack.add_titled(fan.box, "fan", "Fans")
		self.stack.add_titled(power.box, "power", "Power")
		self.stack.add_titled(lighting.box, "lighting", "Lighting")
		self.stack.add_titled(effects.box, "effects", "Effects")
		self.stack.add_titled(settings.box, "settings", "Settings")

		self.stack_switcher = Gtk.StackSwitcher(
			margin_bottom=10,
			margin_end=10,
			margin_start=10,
			margin_top=10,
			stack=self.stack,
		)
		self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		self.box.append(self.stack_switcher)
		self.box.append(self.stack)
		self.set_child(self.box)  # Horizontal box to window

	def about_dialog_button_clicked(self, widget):
		self.about_dialog.show()

	def restart_button_clicked(self, _):
		self.destroy()

	def uninstall_window_keep_clicked(self, _):
		os.system("pkexec --user root /usr/share/razercontrol/bin/uninstall")
		self.destroy()

	def uninstall_window_remove_clicked(self, _):
		os.system(
			"pkexec --user root /usr/share/razercontrol/bin/uninstall "
			+ os.environ["HOME"]
		)
		self.destroy()


class Application(Adw.Application):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.connect("activate", self.activate)

	def activate(self, app):
		self.window = ApplicationWindow(application=app)
		self.window.present()


app = Application(application_id="com.github.phush0.razer-laptop-control-no-dkms")
app.run(sys.argv)
