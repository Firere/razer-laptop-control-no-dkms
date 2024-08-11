import gi

gi.require_versions({ "Gtk": "4.0", "Adw": "1"})
from gi.repository import Adw, Gtk
from ui.const import args, pg_bottom

# TODO: save state
# TODO: standard effects
# TODO: effects

class effects(Gtk.Box):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.standard_effects_pg = Adw.PreferencesGroup(title="Standard Effects", margin_bottom=pg_bottom)

		self.effects_pg = Adw.PreferencesGroup(title="Effects", margin_bottom=pg_bottom)

		self.append(self.standard_effects_pg)
		self.append(self.effects_pg)


box = effects(**args)
