import gi

from .utils import Gtk


class Prompt(Gtk.Dialog):
    def __init__(self, message):
        super().__init__()
        self.set_decorated(False)
        box = self.get_content_area()
        self.entry = Gtk.Entry()
        self.entry.set_text(message)

        self.entry.connect("destroy", Gtk.main_quit)

        self.entry.grab_focus()
        box.add(self.entry)


class NewTaskPrompt(Prompt):
    def __init__(self):
        super().__init__("New Task")
        self.entry.connect("activate", self.create_task)

    def create_task(self, *args):
        task = self.entry.get_text()
        self.create_new_task(task)
        self.destroy()

    def create_new_task(self, task):
        raise NotImplementedError("You have to implement 'create_new_task'.")
