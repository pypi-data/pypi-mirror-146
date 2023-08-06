# SPDX-FileCopyrightText: 2022 Joshua Mulliken <joshua@mulliken.net>
#
# SPDX-License-Identifier: GPL-3.0-or-later
import asyncio
from typing import List

from gitlab import Gitlab

from taskimporter import Task
from taskimporter.services import BaseService


class GitlabService(BaseService):
    service_type = "gitlab"
    config_keys = ["gitlab_instance", "repo", "api_token"]

    def __init__(self, gitlab_instance, repo, api_token, project_key):
        """
        GitlabService constructor. Reads the config from the keys defined in config_keys.
        Any other implementations of BaseService should include the project_key as the last argument.

        :param gitlab_instance: The gitlab instance to use.
        :param repo:
        :param api_token:
        :param project_key:
        """

        self._gitlab = Gitlab(gitlab_instance, private_token=api_token)
        self._gitlab.auth()
        self._repo_name = repo
        self._repo = self._gitlab.projects.get(repo)

        self.name = "GitLab: %s" % repo
        self.project_key = project_key

    async def get_open_tasks(self) -> List[Task]:
        loop = asyncio.get_running_loop()

        results = await asyncio.gather(
            loop.run_in_executor(None, self._get_issues_from_gitlab, "opened"),
            loop.run_in_executor(None, self._get_merge_requests_from_gitlab, "opened")
        )

        all_tasks = await asyncio.gather(
            self._get_tasks_from_gitlab("Issue", results[0]),
            self._get_tasks_from_gitlab("Merge Request", results[1])
        )

        tasks = []
        for task_list in all_tasks:
            tasks.extend(task_list)

        return tasks

    def _get_issues_from_gitlab(self, state):
        return self._repo.issues.list(state=state)  # TODO: only get recently closed issues

    def _get_merge_requests_from_gitlab(self, state):
        return self._repo.mergerequests.list(state=state)  # TODO: only get recently closed issues

    async def get_closed_tasks(self) -> List[Task]:
        loop = asyncio.get_running_loop()

        results = await asyncio.gather(
            loop.run_in_executor(None, self._get_issues_from_gitlab, "closed"),
            loop.run_in_executor(None, self._get_merge_requests_from_gitlab, "closed")
        )

        all_tasks = await asyncio.gather(
            self._get_tasks_from_gitlab("Issue", results[0]),
            self._get_tasks_from_gitlab("Merge Request", results[1])
        )

        tasks = []
        for task_list in all_tasks:
            tasks.extend(task_list)

        return tasks

    @staticmethod
    async def _get_task_from_gitlab(issue_type, issue) -> Task:
        task = Task()
        task.name = ("[%s] %s" % (issue_type, issue.title)).replace("\"", "'")
        task.url = issue.web_url

        return task

    @staticmethod
    async def _get_tasks_from_gitlab(issue_type, issues) -> List[Task]:
        results = await asyncio.gather(*[GitlabService._get_task_from_gitlab(issue_type, issue) for issue in issues])

        tasks = []
        for task in results:
            tasks.append(task)

        return tasks
