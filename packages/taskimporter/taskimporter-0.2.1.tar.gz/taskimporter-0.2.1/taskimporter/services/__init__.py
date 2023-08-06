# SPDX-FileCopyrightText: 2022 Joshua Mulliken <joshua@mulliken.net>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import pkgutil
from abc import ABC, abstractmethod
from importlib import import_module
from inspect import isclass
from pathlib import Path
from typing import List

from taskimporter import Task


class BaseService(ABC):
    service_type: str
    name: str
    project_key: str

    @property
    @abstractmethod
    def service_type(self) -> str:
        pass

    @property
    @abstractmethod
    def config_keys(self) -> List[str]:
        pass

    @abstractmethod
    async def get_open_tasks(self) -> List[Task]:
        pass

    @abstractmethod
    async def get_closed_tasks(self) -> List[Task]:
        pass


services = {}

package_dir = Path(__file__).resolve().parent
for (_, module_name, _) in pkgutil.iter_modules([str(package_dir)]):
    module = import_module(f"{__name__}.{module_name}")

    for attribute_name in dir(module):
        attribute = getattr(module, attribute_name)

        if isclass(attribute) and issubclass(attribute, BaseService) and attribute is not BaseService:
            services[attribute.service_type] = attribute
