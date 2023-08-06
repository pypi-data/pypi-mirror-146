# SPDX-FileCopyrightText: 2022 Joshua Mulliken <joshua@mulliken.net>
#
# SPDX-License-Identifier: GPL-3.0-or-later
import asyncio
import datetime
from typing import List

from github import Github
from github.Issue import Issue
from github.PaginatedList import PaginatedList

from taskimporter import Task
from taskimporter.services import BaseService


class GithubService(BaseService):
    service_type = "github"
    config_keys = ["repo", "api_token"]

    def __init__(self, repo, api_token, project_key):
        """
        GithubService constructor. Reads the config from the keys defined in config_keys.
        Any other implementations of BaseService should include the project_key as the last argument.

        :param repo:
        :param api_token:
        :param project_key:
        """
        self._github = Github(api_token)
        self._repo_name = repo
        self._repo = self._github.get_repo(repo)

        self.name = "GitHub: %s" % repo
        self.project_key = project_key

    def get_issues(self, state: str, since: datetime.datetime) -> PaginatedList:
        if state == 'closed':
            return self._repo.get_issues(state='closed', since=since)

        return self._repo.get_issues(state=state)

    async def get_open_tasks(self) -> List[Task]:
        loop = asyncio.get_running_loop()
        issues = await loop.run_in_executor(None, self.get_issues, 'open', None)

        return await self._get_tasks_from_issues(issues)

    async def get_closed_tasks(self) -> List[Task]:
        loop = asyncio.get_running_loop()
        issues = await loop.run_in_executor(None, self.get_issues, 'closed', datetime.datetime.now() - datetime.timedelta(days=7))

        return await self._get_tasks_from_issues(issues)

    @staticmethod
    async def get_task_from_issue(issue: Issue) -> Task:
        task = Task()
        if issue.pull_request is None:
            task.name = ("[Issue] %s" % issue.title).replace("\"", "'")
        else:
            task.name = ("[Pull Request] %s" % issue.title).replace("\"", "'")
        task.url = issue.html_url

        return task

    @staticmethod
    async def _get_tasks_from_issues(issues: PaginatedList) -> List[Task]:
        tasks = []

        results = await asyncio.gather(*[GithubService.get_task_from_issue(issue) for issue in issues])

        for task in results:
            tasks.append(task)

        return tasks
