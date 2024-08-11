import gi

gi.require_versions({ "Gtk": "4.0", "Adw": "1"})
from gi.repository import Adw, Gtk

from ui import func
from ui.const import args, pg_bottom

class lighting(Gtk.Box):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		# #### Sync
		self.sync_ar_prefix = Gtk.Label(
			label="Sync light effects between being plugged in and on battery"
		)

		self.sync_ar_suffix = Gtk.Switch(
			state=func.get_sync(), valign=Gtk.Align.CENTER
		)

		self.sync_ar = Adw.ActionRow()
		self.sync_ar.add_prefix(self.sync_ar_prefix)
		self.sync_ar.add_suffix(self.sync_ar_suffix)
		# /#### Sync

		# #### Brightness
		# ## Brightness (AC)
		self.brightness_ac_ar_prefix = Gtk.Label(label="Brightness (plugged in)")
		self.brightness_ac_ar_suffix = Gtk.Scale(
			digits=0, draw_value=True, width_request=350
		)
		self.brightness_ac_ar_suffix.set_range(0, 100)
		self.brightness_ac_ar_suffix.set_value(func.get_brightness_ac())
		self.brightness_ac_ar = Adw.ActionRow()
		self.brightness_ac_ar.add_prefix(self.brightness_ac_ar_prefix)
		self.brightness_ac_ar.add_suffix(self.brightness_ac_ar_suffix)
		# /## Brightness (AC)

		# ## Brightness (Battery)
		self.brightness_bat_ar_prefix = Gtk.Label(label="Brightness (on battery)")
		self.brightness_bat_ar_suffix = Gtk.Scale(
			digits=0, draw_value=True, width_request=350
		)
		self.brightness_bat_ar_suffix.set_range(0, 100)
		self.brightness_bat_ar_suffix.set_value(func.get_brightness_bat())
		self.brightness_bat_ar = Adw.ActionRow()
		self.brightness_bat_ar.add_prefix(self.brightness_bat_ar_prefix)
		self.brightness_bat_ar.add_suffix(self.brightness_bat_ar_suffix)
		# /## Brightness (Battery)
		# /#### Brightness

		# #### Logo
		# ## Logo (when sync is on)
		self.logo_ar_prefix = Gtk.Label(label="Logo lighting pattern")
		self.logo_ar_suffix_on = Gtk.CheckButton(label="On")
		self.logo_ar_suffix_breathing = Gtk.CheckButton(
			group=self.logo_ar_suffix_on, label="Breathing"
		)
		self.logo_ar_suffix_off = Gtk.CheckButton(
			group=self.logo_ar_suffix_on, label="Off"
		)

		if func.get_logo_manual() == 0:
			self.logo_ar_suffix_off.set_active(True)
		elif func.get_logo_manual() == 1:
			self.logo_ar_suffix_on.set_active(True)
		else:
			self.logo_ar_suffix_breathing.set_active(True)

		self.logo_ar = Adw.ActionRow()
		self.logo_ar.add_prefix(self.logo_ar_prefix)
		self.logo_ar.add_suffix(self.logo_ar_suffix_on)
		self.logo_ar.add_suffix(self.logo_ar_suffix_breathing)
		self.logo_ar.add_suffix(self.logo_ar_suffix_off)
		# /## Logo (when sync is on)

		# ## Logo (AC)
		self.logo_ac_ar_prefix = Gtk.Label(label="  Plugged in")
		self.logo_ac_ar_suffix_on = Gtk.CheckButton(label="On")
		self.logo_ac_ar_suffix_breathing = Gtk.CheckButton(
			group=self.logo_ac_ar_suffix_on, label="Breathing"
		)
		self.logo_ac_ar_suffix_off = Gtk.CheckButton(
			group=self.logo_ac_ar_suffix_on, label="Off"
		)

		if func.get_logo_ac_manual() == 0:
			self.logo_ac_ar_suffix_off.set_active(True)
		elif func.get_logo_ac_manual() == 1:
			self.logo_ac_ar_suffix_on.set_active(True)
		else:
			self.logo_ac_ar_suffix_breathing.set_active(True)

		self.logo_ac_ar = Adw.ActionRow()
		self.logo_ac_ar.add_prefix(self.logo_ac_ar_prefix)
		self.logo_ac_ar.add_suffix(self.logo_ac_ar_suffix_on)
		self.logo_ac_ar.add_suffix(self.logo_ac_ar_suffix_breathing)
		self.logo_ac_ar.add_suffix(self.logo_ac_ar_suffix_off)
		# /## Logo (AC)

		# ## Logo (Battery)
		self.logo_bat_ar_prefix = Gtk.Label(label="  On battery")
		self.logo_bat_ar_suffix_on = Gtk.CheckButton(label="On")
		self.logo_bat_ar_suffix_breathing = Gtk.CheckButton(
			group=self.logo_bat_ar_suffix_on, label="Breathing"
		)
		self.logo_bat_ar_suffix_off = Gtk.CheckButton(
			group=self.logo_bat_ar_suffix_on, label="Off"
		)

		if func.get_logo_bat_manual() == 0:
			self.logo_bat_ar_suffix_off.set_active(True)
		elif func.get_logo_bat_manual() == 1:
			self.logo_bat_ar_suffix_on.set_active(True)
		else:
			self.logo_bat_ar_suffix_breathing.set_active(True)

		self.logo_bat_ar = Adw.ActionRow()
		self.logo_bat_ar.add_prefix(self.logo_bat_ar_prefix)
		self.logo_bat_ar.add_suffix(self.logo_bat_ar_suffix_on)
		self.logo_bat_ar.add_suffix(self.logo_bat_ar_suffix_breathing)
		self.logo_bat_ar.add_suffix(self.logo_bat_ar_suffix_off)
		# /## Logo (Battery)
		# /#### Logo

		self.pg = Adw.PreferencesGroup(
			margin_bottom=pg_bottom, title="Lighting"
		)
		self.pg.add(self.sync_ar)
		self.pg.add(self.brightness_ac_ar)
		self.pg.add(self.brightness_bat_ar)
		self.pg.add(self.logo_ar)
		self.pg.add(self.logo_ac_ar)
		self.pg.add(self.logo_bat_ar)

		self.sync_ar_suffix.connect("state-set", self.sync_ar_suffix_state_set)

		self.brightness_ac_ar_suffix.connect(
			"value-changed", self.brightness_ac_ar_suffix_value_changed
		)
		self.brightness_bat_ar_suffix.connect(
			"value-changed", self.brightness_bat_ar_suffix_value_changed
		)

		self.logo_ac_ar_suffix_on.connect("toggled", self.logo_ac_ar_suffix_on_toggled)
		self.logo_ac_ar_suffix_breathing.connect(
			"toggled", self.logo_ac_ar_suffix_breathing_toggled
		)
		self.logo_ac_ar_suffix_off.connect(
			"toggled", self.logo_ac_ar_suffix_off_toggled
		)

		self.logo_bat_ar_suffix_on.connect(
			"toggled", self.logo_bat_ar_suffix_on_toggled
		)
		self.logo_bat_ar_suffix_breathing.connect(
			"toggled", self.logo_bat_ar_suffix_breathing_toggled
		)
		self.logo_bat_ar_suffix_off.connect(
			"toggled", self.logo_bat_ar_suffix_off_toggled
		)

		self.logo_ar_suffix_on.connect("toggled", self.logo_ar_suffix_on_toggled)
		self.logo_ar_suffix_breathing.connect(
			"toggled", self.logo_ar_suffix_breathing_toggled
		)
		self.logo_ar_suffix_off.connect("toggled", self.logo_ar_suffix_off_toggled)

		self.sync_ar_suffix_state_set("", func.get_sync())

		self.append(self.pg)

	def brightness_ac_ar_suffix_value_changed(self, _):
		func.set_brightness_ac(self.brightness_ac_ar_suffix.get_value())

	def brightness_bat_ar_suffix_value_changed(self, _):
		func.set_brightness_bat(self.brightness_bat_ar_suffix.get_value())

	def logo_ac_ar_suffix_on_toggled(self, _):
		if self.logo_ac_ar_suffix_on.get_value():
			func.set_logo_ac(1)

	def logo_ac_ar_suffix_breathing_toggled(self, _):
		if self.logo_ac_ar_suffix_breathing.get_value():
			func.set_logo_ac(2)

	def logo_ac_ar_suffix_off_toggled(self, _):
		if self.logo_ac_ar_suffix_off.get_value():
			func.set_logo_ac(0)

	def logo_bat_ar_suffix_on_toggled(self, _):
		if self.logo_bat_ar_suffix_on.get_value():
			func.set_logo_bat(1)

	def logo_bat_ar_suffix_breathing_toggled(self, _):
		if self.logo_bat_ar_suffix_breathing.get_value():
			func.set_logo_bat(2)

	def logo_bat_ar_suffix_off_toggled(self, _):
		if self.logo_bat_ar_suffix_off.get_value():
			func.set_logo_bat(0)

	def logo_ar_suffix_on_toggled(self, _):
		pass

	def logo_ar_suffix_breathing_toggled(self, _):
		pass

	def logo_ar_suffix_off_toggled(self, _):
		pass

	def sync_ar_suffix_state_set(self, _, state):
		func.set_sync(state)
		if state:
			self.logo_ar_suffix_on.show()
			self.logo_ar_suffix_breathing.show()
			self.logo_ar_suffix_off.show()
			self.logo_ac_ar.hide()
			self.logo_bat_ar.hide()
		else:
			self.logo_ar_suffix_on.hide()
			self.logo_ar_suffix_breathing.hide()
			self.logo_ar_suffix_off.hide()
			self.logo_ac_ar.show()
			self.logo_bat_ar.show()


box = lighting(**args)
