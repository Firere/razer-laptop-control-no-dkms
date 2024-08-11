import gi

gi.require_versions({ "Gtk": "4.0", "Adw": "1"})
from gi.repository import Adw, Gtk

from ui import func
from ui.const import args, pg_bottom


class fan(Gtk.Box):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.ac_ar_automatic_prefix = Gtk.Label(label="Automatic")
		self.ac_ar_automatic_suffix = Gtk.Switch(valign=Gtk.Align.CENTER)
		self.ac_is_automatic = False
		# Check if it actually is automatic
		if func.get_fan_ac() == 0:
			self.ac_ar_automatic_suffix.set_state(True)
			self.ac_is_automatic = True
		# When using custom power settings, fans are permanently set to automatic and can't be changed

		# ## AC (automatic) - alternate
		self.ac_ar_automatic_alt_prefix = Gtk.Label(label="Automatic")
		self.ac_ar_automatic_alt_suffix = Gtk.Label()
		self.ac_ar_automatic_alt_suffix.set_markup(
			"<span color='gray'><small><i>Must be automatic when power mode is set to custom</i></small></span>"
		)
		self.ac_ar_automatic_alt = Adw.ActionRow()
		self.ac_ar_automatic_alt.add_prefix(self.ac_ar_automatic_alt_prefix)
		self.ac_ar_automatic_alt.add_suffix(self.ac_ar_automatic_alt_suffix)
		# /## AC (automatic) - alternate

		self.ac_ar_automatic = Adw.ActionRow()
		self.ac_ar_automatic.add_prefix(self.ac_ar_automatic_prefix)
		self.ac_ar_automatic.add_suffix(self.ac_ar_automatic_suffix)
		# /#### AC (automatic)

		# #### AC (manual)
		self.ac_ar_manual_prefix = Gtk.Label(label="Fan speed")
		self.ac_ar_manual_suffix = Gtk.Scale.new_with_range(
			Gtk.Orientation.HORIZONTAL,
			func.get_min_fan(),
			func.get_max_fan(),
			100,
		)
		self.ac_ar_manual_suffix.set_size_request(400, 0)
		self.ac_ar_manual_suffix.set_digits(0)
		self.ac_ar_manual_suffix.set_draw_value(True)
		self.ac_ar_manual_suffix.set_value(func.get_fan_ac_manual())

		self.ac_ar_manual = Adw.ActionRow()
		self.ac_ar_manual.add_prefix(self.ac_ar_manual_prefix)
		self.ac_ar_manual.add_suffix(self.ac_ar_manual_suffix)

		# If power mode is set to custom, show the alternate instead of the normal one
		if func.get_power_ac() == 4:
			self.ac_ar_manual.hide()
			self.ac_ar_automatic.hide()
		else:
			self.ac_ar_automatic_alt.hide()
		# /#### AC (manual)

		self.ac_pg = Adw.PreferencesGroup(
			margin_bottom=pg_bottom, title="Plugged in"
		)
		self.ac_pg.add(self.ac_ar_automatic_alt)
		self.ac_pg.add(self.ac_ar_automatic)
		self.ac_pg.add(self.ac_ar_manual)
		# /######## AC

		# ######## Battery
		# #### Battery (automatic)
		self.bat_ar_automatic_prefix = Gtk.Label(label="Automatic")

		self.bat_ar_automatic_suffix = Gtk.Switch(valign=Gtk.Align.CENTER)
		self.bat_is_automatic = False
		# Check if it actually is automatic
		if func.get_fan_bat() == 0:
			self.bat_ar_automatic_suffix.set_state(True)
			self.bat_is_automatic = True

		self.bat_ar_automatic = Adw.ActionRow()
		self.bat_ar_automatic.add_prefix(self.bat_ar_automatic_prefix)
		self.bat_ar_automatic.add_suffix(self.bat_ar_automatic_suffix)
		# /#### Battery (automatic)

		# #### Battery (manual)
		self.bat_ar_manual_prefix = Gtk.Label(label="Fan speed")
		self.bat_ar_manual_suffix = Gtk.Scale.new_with_range(
			Gtk.Orientation.HORIZONTAL,
			func.get_min_fan(),
			func.get_max_fan(),
			100,
		)
		self.bat_ar_manual_suffix.set_size_request(400, 0)
		self.bat_ar_manual_suffix.set_digits(0)
		self.bat_ar_manual_suffix.set_range(
			func.get_min_fan(), func.get_max_fan()
		)
		self.bat_ar_manual_suffix.set_draw_value(True)
		self.bat_ar_manual_suffix.set_value(func.get_fan_bat_manual())
		self.bat_ar_manual = Adw.ActionRow()
		self.bat_ar_manual.add_prefix(self.bat_ar_manual_prefix)
		self.bat_ar_manual.add_suffix(self.bat_ar_manual_suffix)
		if self.bat_is_automatic:
			self.bat_ar_manual.hide()

		self.bat_pg = Adw.PreferencesGroup(
			title="On battery", margin_bottom=pg_bottom
		)
		self.bat_pg.add(self.bat_ar_automatic)
		self.bat_pg.add(self.bat_ar_manual)
		# /#### Battery (manual)
		# /######## Battery

		self.ac_ar_automatic_suffix.connect(
			"state-set", self.ac_ar_automatic_switch_state_set
		)
		self.ac_ar_manual_suffix.connect(
			"value-changed", self.ac_ar_manual_suffix_value_changed
		)
		self.bat_ar_automatic_suffix.connect(
			"state-set", self.bat_ar_automatic_switch_state_set
		)
		self.bat_ar_manual_suffix.connect(
			"value-changed", self.bat_ar_manual_suffix_value_changed
		)

		self.append(self.ac_pg)
		self.append(self.bat_pg)

	def ac_ar_automatic_switch_state_set(self, _, state):
		if state:
			self.ac_ar_manual.hide()
			func.set_fan_ac(0)
		else:
			func.set_fan_ac(func.get_fan_ac_manual())
			self.ac_ar_manual.show()

	def ac_ar_manual_suffix_value_changed(self, _):
		self.ac_ar_manual_suffix.set_value(
			int(round(self.ac_ar_manual_suffix.get_value() / 100) * 100)
		)
		func.set_fan_ac(int(round(self.ac_ar_manual_suffix.get_value() / 100) * 100))

	def bat_ar_automatic_switch_state_set(self, _, state):
		if state:
			self.bat_ar_manual.hide()
			func.set_fan_bat(0)
		else:
			func.set_fan_bat(func.get_fan_bat_manual())
			self.bat_ar_manual.show()

	def bat_ar_manual_suffix_value_changed(self, _):
		self.bat_ar_manual_suffix.set_value(
			int(round(self.bat_ar_manual_suffix.get_value() / 100) * 100)
		)
		func.set_fan_bat(
			int(round(self.bat_ar_manual_suffix.get_value() / 100) * 100)
		)


box = fan(**args)
