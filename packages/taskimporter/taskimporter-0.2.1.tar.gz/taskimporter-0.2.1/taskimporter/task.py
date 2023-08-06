# SPDX-FileCopyrightText: 2022 Joshua Mulliken <joshua@mulliken.net>
#
# SPDX-License-Identifier: GPL-3.0-or-later
from datetime import date
from typing import Optional


class Task:
    name: str
    url: str
    due_date: Optional[date] = None
