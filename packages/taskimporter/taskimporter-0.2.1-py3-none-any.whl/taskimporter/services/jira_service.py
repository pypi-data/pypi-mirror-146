# SPDX-FileCopyrightText: 2022 Joshua Mulliken <joshua@mulliken.net>
#
# SPDX-License-Identifier: GPL-3.0-or-later
import asyncio
from datetime import date
from typing import List

from jira import JIRA
from jira.resources import Issue as JiraIssue

from taskimporter import Task
from taskimporter.services import BaseService


class JiraService(BaseService):
    service_type = "jira"
    config_keys = ["server", "api_token"]

    def __init__(self, server, api_token, project_key):
        """
        JiraService constructor. Reads the config from the keys defined in config_keys.
        Any other implementations of BaseService should include the project_key as the last argument.

        :param server:
        :param api_token:
        :param project_key:
        """

        self._server = server
        self._jira = JIRA(server=self._server, token_auth=api_token)
        self.name = "Jira: %s" % self._server
        self.project_key = project_key

    async def get_open_tasks(self):
        loop = asyncio.get_running_loop()
        issues = await loop.run_in_executor(None, self._jira.search_issues, 'assignee = currentUser() AND resolution = Unresolved')

        return await self._get_tasks_from_issues(issues)

    async def get_closed_tasks(self):
        loop = asyncio.get_running_loop()
        issues = await loop.run_in_executor(None, self._jira.search_issues, 'assignee = currentUser() AND resolution != Unresolved ORDER BY "Resolved Date" ASC')

        return await self._get_tasks_from_issues(issues)

    async def _get_task_from_issue(self, issue: JiraIssue):
        task = Task()
        task.name = ("[%s] %s" % (issue.key, issue.fields.summary)).replace("\"", "'")
        task.url = "%s/browse/%s" % (self._server, issue.key)

        if issue.fields.duedate:
            task.due_date = date.fromisoformat(issue.fields.duedate)
            print("We got a due date and it is %s" % task.due_date)

        return task

    async def _get_tasks_from_issues(self, issues: List[JiraIssue]):
        results = await asyncio.gather(*[self._get_task_from_issue(issue) for issue in issues])

        tasks = []
        issue: JiraIssue
        for task in results:
            tasks.append(task)

        return tasks
