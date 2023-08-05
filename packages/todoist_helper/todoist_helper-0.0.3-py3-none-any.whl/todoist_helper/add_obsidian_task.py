from pathlib import Path

from .base import Prompt, NewTaskPrompt
from .utils import show_prompt


class ObsidianTaskPrompt(NewTaskPrompt):
    def __init__(self, inbox_path):
        super().__init__()
        self.inbox_path = inbox_path

    def create_new_task(self, task):
        add_inbox_entry(self.inbox_path, task)


def add_inbox_entry(inbox_path, task):
    with open(inbox_path, "r+") as inbox:
        content = inbox.readlines()
        index = 0
        for i, line in enumerate(content):
            if "------" in line:
                index = i
                break
        content.insert(index + 1, f"\n- [ ] {task}")
        inbox.seek(0)
        inbox.writelines(content)


def add_obsidian_task(inbox_path):
    show_prompt(ObsidianTaskPrompt(inbox_path))
