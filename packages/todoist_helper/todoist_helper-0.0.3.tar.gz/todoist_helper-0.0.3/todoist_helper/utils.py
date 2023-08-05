import gi

gi.require_version("Gtk", "3.0")

from gi.repository import Gtk


def show_prompt(prompt):
    prompt.show_all()
    Gtk.main()
