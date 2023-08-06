# SPDX-FileCopyrightText: 2022 Joshua Mulliken <joshua@mulliken.net>
#
# SPDX-License-Identifier: GPL-3.0-or-later
import asyncio.subprocess
from subprocess import Popen, PIPE

from taskimporter import Task
from taskimporter.const import JINJA_TEMPLATE_ENV
from taskimporter.task_managers import BaseTaskManager

THINGS_PROJECT = "Default Project"
THINGS_TEMPLATE = JINJA_TEMPLATE_ENV.get_template("things3_add_todo.applescript")
THINGS_MARK_DONE = JINJA_TEMPLATE_ENV.get_template("things3_mark_todo_done.applescript")


class Things3(BaseTaskManager):
    name = "things3"

    @staticmethod
    async def add_task(task: Task, project=THINGS_PROJECT):
        things_script = THINGS_TEMPLATE.render(
            todo_name=task.name,
            todo_url=task.url,
            things_project=project,
            todo_due_date=task.due_date)

        await Things3.run_things_script(things_script)

    @staticmethod
    async def mark_done(task: Task, project: str) -> None:
        things_script = THINGS_MARK_DONE.render(
            todo_name=task.name,
            things_project=project)

        await Things3.run_things_script(things_script)

    @staticmethod
    async def run_things_script(script: str) -> None:
        proc = await asyncio.subprocess.create_subprocess_shell('osascript -', stdin=PIPE)
        proc.stdin.write(script.encode('utf-8'))
        proc.stdin.close()
        await proc.wait()