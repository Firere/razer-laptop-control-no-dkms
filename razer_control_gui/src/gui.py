#!/usr/bin/python3

import datetime
import gi
import json
import os

# import sys

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

laptops_raw = open("/usr/share/razercontrol/laptops.json")
laptops = json.loads(laptops_raw.read())
laptops_raw.close()


laptop_name = ""
has_creator_mode_support = False
has_boost_support = False
for entry in os.popen("lsusb"):
    vid = entry[23:27]
    pid = entry[28:32]
    for laptop in laptops:
        if vid == laptop["vid"] and pid == laptop["pid"]:
            laptop_name = laptop["name"]
            laptop_vid = laptop["vid"]
            laptop_pid = laptop["pid"]
            laptop_min_fan_speed = laptop["fan"][0]
            laptop_max_fan_speed = laptop["fan"][1]
            for feature in laptop["features"]:
                if feature == "creator_mode":
                    has_creator_mode_support = True
                if feature == "boost":
                    has_boost_support = True


def write(string):
    print("[" + str(datetime.datetime.now()) + "] " + string)


write("Starting")


# Don't know if it actually only supports Linux
# if sys.platform != "linux":
# 	exit("This only supports Linux")
# else:
# 	write("Passed platform check")


class Window(Gtk.Window):
    def __init__(self):
        super().__init__(title="Razer Laptop Control")
        write("Initialising window")

        # Header bar
        self.header_bar = Gtk.HeaderBar()
        self.header_bar.set_title("Razer Laptop Control")
        self.header_bar.set_show_close_button(True)
        self.about_dialog_button = Gtk.Button(label="About")
        self.about_dialog_button.connect("clicked", self.about_dialog_button_clicked)
        self.header_bar.add(self.about_dialog_button)
        self.set_titlebar(self.header_bar)

        # About dialog
        self.about_dialog = Gtk.AboutDialog()
        self.about_dialog.set_program_name("Razer Laptop Control")
        self.about_dialog.set_comments("This program is not in any way affiliated with Razer Inc. The trisnake logo is full property of Razer Inc.")
        self.about_dialog.set_website_label("GitHub repository")
        self.about_dialog.set_website("https://github.com/phush0/razer-laptop-control-no-dkms")
        self.about_dialog.set_license_type(Gtk.License.GPL_2_0)
        self.about_dialog.set_authors(["phusho (phush0) - project maintainer", "Firere - GUI"])
        self.about_dialog.set_artists(["Firere - Razer Laptop Control Logo"])
        self.about_dialog_header_bar = Gtk.HeaderBar()
        self.about_dialog_header_bar.set_title("About")
        self.about_dialog_header_bar.set_show_close_button(True)
        #self.about_dialog.set_titlebar(self.about_dialog_header_bar) # doesn't display for some reason

        # Assistant (navigation/sections)
        self.assistant = Gtk.Assistant()
        self.fans = Gtk.Frame()
        self.assistant.insert_page(self.fans, 0)
        #self.assistant.insert_page("Power", 1)
        #self.assistant.insert_page("Lighting", 2)
        self.assistant.set_current_page(0)
        self.add(self.assistant)

        write("Initialised window")

    def about_dialog_button_clicked(self, widget):
        self.about_dialog.run()
        write("Execute about_dialog_button_clicked")


window = Window()
window.connect("destroy", Gtk.main_quit)
window.show_all()
Gtk.main()
