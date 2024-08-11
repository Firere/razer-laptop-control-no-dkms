import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

pg_bottom = 30
args = dict(
	baseline_position = Gtk.BaselinePosition.TOP,
	margin_bottom = 40,
	margin_end = 65,
	margin_start = 65,
	margin_top = 0,
	orientation = Gtk.Orientation.VERTICAL
)
