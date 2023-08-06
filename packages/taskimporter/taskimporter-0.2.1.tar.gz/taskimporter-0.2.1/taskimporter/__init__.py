# SPDX-FileCopyrightText: 2022 Joshua Mulliken <joshua@mulliken.net>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import argparse
import asyncio
import configparser
import os

from appdirs import user_data_dir

from taskimporter import const
from taskimporter.task import Task
from taskimporter.services import services, BaseService
from taskimporter.task_managers import task_managers, BaseTaskManager


def configure_services(config, user_services):
    s_list = []

    for service in user_services:
        service_name = config[service]['service']
        if service_name in services:
            service_cls = services[service_name]

            service_config = {}

            for key in service_cls.config_keys:
                if key in config[service]:
                    service_config[key] = config[service][key]

            service_config["project_key"] = config[service]['project']

            print(service_config)

            s_list.append(service_cls(**service_config))
        else:
            print("Invalid service: %s" % service_name)

    return s_list


async def add_task_worker(parent_name, a_task, task_manager, service):
    print("%s - Adding task: %s" % (parent_name, a_task.name))
    if task_manager in task_managers:
        await task_managers[task_manager].add_task(a_task, project=service.project_key)


async def mark_task_done_worker(parent_name, a_task, task_manager, service):
    print("%s - Marking task as done: %s" % (parent_name, a_task.name))
    if task_manager in task_managers:
        await task_managers[task_manager].mark_done(a_task, project=service.project_key)


async def pull_open_tasks(service):
    tasks = await service.get_open_tasks()
    return tasks


async def pull_closed_tasks(service):
    tasks = await service.get_closed_tasks()
    return tasks


async def async_main():
    parser = argparse.ArgumentParser(description='Import tasks from various services')
    parser.add_argument('-c', '--config', help='Path to configuration file')
    parser.add_argument('-w', '--write', help='Write default config', action='store_true')
    args = parser.parse_args()

    config_path = user_data_dir('taskimporter', 'Joshua Mulliken') + '/config.ini'

    if args.config:
        config_path = args.config

    os.makedirs(os.path.dirname(config_path), exist_ok=True)

    if args.write:
        with open(config_path, 'w') as f:
            f.write(const.DEFAULT_CONFIG)

            print('Default config written to \"{}\"'.format(config_path))
            print('Please edit the config file and run again')
            exit(0)

    config = configparser.ConfigParser()

    task_manager = ""
    user_services = []

    try:
        config.read(config_path)
        task_manager = config['DEFAULT']['task_manager']
        user_services = [section for section in config.sections() if section != 'DEFAULT']
    except KeyError:
        print('Invalid config file')
        print('Please run with --write to create a default config file')
        print('Config file path: \"{}\"'.format(config_path))
        exit(1)

    if len(user_services) == 0:
        print("No services configured. Please add a service to the config file and run again")
        print("Config location: \"{}\"".format(config_path))
        exit(0)

    service_workers = []
    count = 0
    for service in configure_services(config, user_services):
        print("Starting worker for service: %s" % service.name)
        service_workers.append(process_service_worker("Service Worker %s" % count, service, task_manager))
        count += 1

    await asyncio.gather(*service_workers)


async def process_open_tasks(name, service: BaseService, task_manager: str):
    print("%s - Pulling open tasks from %s" % (name, service.name))
    tasks = await service.get_open_tasks()
    await asyncio.gather(
        *[add_task_worker(name, tsk, task_manager, service) for tsk in tasks]
    )


async def process_closed_tasks(name, service: BaseService, task_manager: str):
    print("%s - Pulling closed tasks from %s" % (name, service.name))
    tasks = await service.get_closed_tasks()
    await asyncio.gather(
        *[mark_task_done_worker(name, tsk, task_manager, service) for tsk in tasks]
    )


async def process_service_worker(name, service: BaseService, task_manager: str):
    await asyncio.gather(
        process_open_tasks(name, service, task_manager),
        process_closed_tasks(name, service, task_manager)
    )


def main():
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
