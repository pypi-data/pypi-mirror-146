# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['time_tracker_cli']
install_requires = \
['toml>=0.9,<0.10']

entry_points = \
{'console_scripts': ['time-tracker-cli = time_tracker_cli:main']}

setup_kwargs = {
    'name': 'time-tracker-cli',
    'version': '1.0.0',
    'description': 'time-tracker-cli is a Python script that allows you to track the time spent working in your projects or tasks.',
    'long_description': '\n<p align="center">\n  <img height=180 src="./readme_assets/logo.png">\n</p>\n\nIt\'s a Python script that allows you to track the time spent working in your projects or tasks.\nAt the moment, this script doesn\'t have external dependencies so it\'s ready to run.\n\n#### Installation: \n\n`$ pip install time-tracker-cli`\n\n#### How to use:\n\n**Help menu:**\n\n`$ time-tracker-cli -h`\n\n```\nusage: time-tracker-cli [-h] [-p PATH] [-r] project\n\npositional arguments:\n  project               project name\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -p PATH, --path PATH  Path to the JSON data file\n  -r, --report          Calculate and display a report of the time spent in the project\n```\n\n**Start/end working session**:\n\n`$ time-tracker-cli -p "~/Documents/my_project_time_tracker_data.json" "my_project"`\n\nThe file or project within the file will be created automatically if it doesn\'t exist.\n\n\n#### Behavior\n\nThe script saves "timestamps" for the working sessions in a JSON file with the following structure:\n\n```\n{\n   "projects": [\n       {\n           "project_name": "a_project_name",\n           "sessions": [\n              {\n                  "start": "dd/mm/yy - H:M:S" ,\n                  "end": "dd/mm/yy - H:M:S"\n              }\n           ]\n       }\n   ]\n}\n```\nUnfinished sessions will have a `null` value in the `end` field.\n\n#### Report\n\nTo calculate the time spent working in a project, run:\n\n```\n$ time-tracker-cli -r -p "~/Documents/my_project_time_tracker_data.json" "my_project" \n\nTime spent working on project: \'my_project\'\n1 day, 7:52:19\nOngoing sessions: True\nTime spent in ongoing session: 0:04:10.492647\n```\n\n#### TODO:\n\n- [x] Add more functions to estimate the time spent working in a project (total, mean per day).\n- [x] Add an argument to request a "report" of the time spent working in a project.\n- [x] Add more documentation.\n- [x] Add a simple GUI (optional). \n- [ ] Define behavior for unfinished sessions.\n\n#### GUI version\n\nCheck out [Time Tracker](https://github.com/pazitos10/time-tracker)\n',
    'author': 'pazitos10',
    'author_email': 'pazosbruno@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pazitos10/time-tracker-cli',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
