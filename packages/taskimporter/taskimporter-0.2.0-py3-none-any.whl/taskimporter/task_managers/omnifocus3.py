# SPDX-FileCopyrightText: 2022 Joshua Mulliken <joshua@mulliken.net>
#
# SPDX-License-Identifier: GPL-3.0-or-later
import asyncio
from subprocess import Popen, PIPE

from taskimporter import Task
from taskimporter.const import JINJA_TEMPLATE_ENV
from taskimporter.task_managers import BaseTaskManager

# look for an existing project with the same name and if one doesn't exist,
# create it
OMNIFOCUS_PROJECT = "Default Project"
OMNIFOCUS_TEMPLATE = JINJA_TEMPLATE_ENV.get_template("omnifocus3_add_todo.applescript")


class Omnifocus3(BaseTaskManager):
    name = "omnifocus3"

    @staticmethod
    async def add_task(task: Task, project: str = OMNIFOCUS_PROJECT) -> None:
        omnifocus_script = OMNIFOCUS_TEMPLATE.render(
            todo_name=task.name.replace('"', ''),
            todo_url=task.url,
            things_project=project,
            todo_due_date=task.due_date)

        proc = await asyncio.subprocess.create_subprocess_shell('osascript -', stdin=PIPE)
        proc.stdin.write(omnifocus_script.encode('utf-8'))
        proc.stdin.close()
        await proc.wait()

    @staticmethod
    async def mark_done(task: Task, project: str) -> None:
        raise NotImplementedError("Omnifocus3 does not currently support marking tasks done. Contributions welcome!")
