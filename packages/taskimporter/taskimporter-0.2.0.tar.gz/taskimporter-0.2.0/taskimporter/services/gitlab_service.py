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
        issues = self._repo.issues.list(state='opened')
        merge_requests = self._repo.mergerequests.list(state='opened')

        results = await asyncio.gather(
            self._get_tasks_from_gitlab("Issue", issues),
            self._get_tasks_from_gitlab("Merge Request", merge_requests)
        )

        tasks = []
        for result in results:
            tasks.extend(result)

        return tasks

    async def get_closed_tasks(self) -> List[Task]:
        issues = self._repo.issues.list(state='closed')  # TODO: only get recently closed issues
        merge_requests = self._repo.mergerequests.list(state='closed')  # TODO: only get recently closed merge requests

        results = await asyncio.gather(
            self._get_tasks_from_gitlab("Issue", issues),
            self._get_tasks_from_gitlab("Merge Request", merge_requests)
        )

        tasks = []
        for result in results:
            tasks.extend(result)

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
