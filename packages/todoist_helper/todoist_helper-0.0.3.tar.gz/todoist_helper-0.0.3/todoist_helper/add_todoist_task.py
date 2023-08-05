from os import path

import todoist
from .base import Prompt, NewTaskPrompt
from .utils import show_prompt, Gtk

CONFIG = path.expanduser("~/.config/todoist")


class APITokenPrompt(Prompt):
    def __init__(self, reason=""):
        super().__init__("API Token")
        self.entry.connect("activate", self.save_api)

        label = Gtk.Label()
        if reason != "":
            reason += ". "

        label.set_markup(
            "{}<a href='https://todoist.com/prefs/integrations'>Get your API token here</a>".format(
                reason
            )
        )
        box = self.get_content_area()
        box.add(label)

    def save_api(self, *args):
        with open(CONFIG, "w") as stream:
            stream.write(self.entry.get_text())
        self.destroy()


class TodoistTaskPrompt(NewTaskPrompt):
    def __init__(self, project_id):
        super().__init__()
        self.project_id = project_id

    def create_new_task(self, task):
        with open(CONFIG) as stream:
            api = todoist.TodoistAPI(stream.read())
            if self.project_id:
                res = api.add_item(task, project_id=self.project_id)
            else:
                res = api.add_item(task)

            if res.get("error_tag") == "AUTH_INVALID_TOKEN":
                show_prompt(APITokenPrompt("Invalid token"))


def add_todoist_task(project_id):
    if not path.exists(CONFIG):
        show_prompt(APITokenPrompt("Missing token"))
    show_prompt(TodoistTaskPrompt(project_id))
