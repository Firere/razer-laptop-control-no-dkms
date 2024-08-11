import gi

gi.require_versions({ "Gtk": "4.0", "Adw": "1"})
from gi.repository import Adw, Gtk

from ui import fan, func
from ui.const import args, pg_bottom


class power(Gtk.Box):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.ar_balanced_prefix = Gtk.Label(label="Balanced")
		self.ar_gaming_prefix = Gtk.Label(label="Gaming")
		self.ar_creator_prefix = Gtk.Label(label="Creator")
		self.ar_custom_prefix = Gtk.Label(label="Custom")

		self.ar_balanced_suffix = Gtk.CheckButton()
		self.ar_gaming_suffix = Gtk.CheckButton(group=self.ar_balanced_suffix)
		self.ar_creator_suffix = Gtk.CheckButton(group=self.ar_balanced_suffix)
		self.ar_custom_suffix = Gtk.CheckButton(group=self.ar_balanced_suffix)

		self.ar_balanced = Adw.ActionRow()
		self.ar_balanced.add_prefix(self.ar_balanced_prefix)
		self.ar_balanced.add_suffix(self.ar_balanced_suffix)
		self.ar_gaming = Adw.ActionRow()
		self.ar_gaming.add_prefix(self.ar_gaming_prefix)
		self.ar_gaming.add_suffix(self.ar_gaming_suffix)
		self.ar_creator = Adw.ActionRow()
		self.ar_creator.add_prefix(self.ar_creator_prefix)
		self.ar_creator.add_suffix(self.ar_creator_suffix)
		self.ar_custom = Adw.ActionRow()
		self.ar_custom.add_prefix(self.ar_custom_prefix)
		self.ar_custom.add_suffix(self.ar_custom_suffix)

		# #### Custom
		self.ar_custom_cpu_prefix = Gtk.Label(label="	CPU")
		self.ar_custom_gpu_prefix = Gtk.Label(label="	GPU")

		has_boost = 2
		if func.get_boost():
			has_boost = 3

		self.ar_custom_cpu_suffix = Gtk.Scale(
			digits=0, draw_value=True, width_request=250
		)
		self.ar_custom_cpu_suffix.set_range(0, has_boost)
		self.ar_custom_cpu_suffix.set_value(func.get_cpu_boost())
		for i in range(has_boost + 1):
			self.ar_custom_cpu_suffix.add_mark(i, Gtk.PositionType.LEFT)

		self.ar_custom_gpu_suffix = Gtk.Scale(
			digits=0, draw_value=True, width_request=250
		)
		self.ar_custom_gpu_suffix.set_range(0, 2)
		self.ar_custom_gpu_suffix.set_value(func.get_gpu_boost())
		for i in range(3):
			self.ar_custom_gpu_suffix.add_mark(i, Gtk.PositionType.LEFT)

		self.ar_custom_cpu = Adw.ActionRow()
		self.ar_custom_cpu.add_prefix(self.ar_custom_cpu_prefix)
		self.ar_custom_cpu.add_suffix(self.ar_custom_cpu_suffix)
		self.ar_custom_gpu = Adw.ActionRow()
		self.ar_custom_gpu.add_prefix(self.ar_custom_gpu_prefix)
		self.ar_custom_gpu.add_suffix(self.ar_custom_gpu_suffix)

		if func.get_power_ac() == 0:
			self.ar_balanced_suffix.set_active(True)
		elif func.get_power_ac() == 1:
			self.ar_gaming_suffix.set_active(True)
		elif func.get_power_ac() == 2:
			self.ar_creator_suffix.set_active(True)
		else:
			self.ar_custom_suffix.set_active(True)
			self.ar_custom_cpu.show()
			self.ar_custom_gpu.show()
		# /#### Custom

		self.pg = Adw.PreferencesGroup(title="Plugged in")
		self.pg.set_margin_bottom(pg_bottom)
		self.pg.add(self.ar_balanced)
		self.pg.add(self.ar_gaming)
		if func.get_creator_mode():
			self.pg.add(self.ar_creator)
		self.pg.add(self.ar_custom)
		self.pg.add(self.ar_custom_cpu)
		self.pg.add(self.ar_custom_gpu)
		if func.get_power_ac() != 4:
			self.ar_custom_cpu.hide()
			self.ar_custom_gpu.hide()

		self.ar_balanced_suffix.connect("toggled", self.ar_balanced_suffix_toggled)
		self.ar_gaming_suffix.connect("toggled", self.ar_gaming_suffix_toggled)
		self.ar_creator_suffix.connect("toggled", self.ar_creator_suffix_toggled)
		self.ar_custom_cpu_suffix.connect(
			"value-changed", self.ar_custom_component_suffix_value_changed
		)
		self.ar_custom_gpu_suffix.connect(
			"value-changed", self.ar_custom_component_suffix_value_changed
		)
		self.ar_custom_suffix.connect("toggled", self.ar_custom_suffix_toggled)
		self.append(self.pg)

	def ar_balanced_suffix_toggled(self, _):
		func.set_power_ac(0, _, _)
		self.ar_custom_cpu.hide()
		self.ar_custom_gpu.hide()
		self.match_fan_power()

	def ar_gaming_suffix_toggled(self, _):
		func.set_power_ac(1, _, _)
		self.ar_custom_cpu.hide()
		self.ar_custom_gpu.hide()
		self.match_fan_power()

	def ar_creator_suffix_toggled(self, _):
		func.set_power_ac(2, _, _)
		self.ar_custom_cpu.hide()
		self.ar_custom_gpu.hide()
		self.match_fan_power()

	def ar_custom_suffix_toggled(self, _):
		func.set_power_ac(
			4,
			int(self.ar_custom_cpu_suffix.get_value()),
			int(self.ar_custom_gpu_suffix.get_value()),
		)
		self.ar_custom_cpu.show()
		self.ar_custom_gpu.show()
		self.match_fan_power()

	def ar_custom_component_suffix_value_changed(self, _):
		func.set_power_ac(
			4,
			int(self.ar_custom_cpu_suffix.get_value()),
			int(self.ar_custom_gpu_suffix.get_value()),
		)
		self.match_fan_power()

	def match_fan_power(self):
		if func.get_power_ac() == 4:
			fan.box.ac_ar_automatic_alt.show()
			fan.box.ac_ar_automatic.hide()
			fan.box.ac_ar_manual.hide()
		else:
			fan.box.ac_ar_automatic_alt.hide()
			fan.box.ac_ar_automatic.show()
			fan.box.ac_ar_manual.show()

			if not fan.box.ac_ar_automatic_suffix.get_state():
				func.set_fan_ac(func.get_fan_ac_manual())


box = power(**args)
