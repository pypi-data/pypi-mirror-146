# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fail2ban_importer', 'fail2ban_importer.downloaders']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.21.37,<2.0.0',
 'click>=8.1.2,<9.0.0',
 'pydantic>=1.9.0,<2.0.0',
 'requests>=2.27.1,<3.0.0',
 'schedule>=1.1.0,<2.0.0']

entry_points = \
{'console_scripts': ['fail2ban-importer = fail2ban_importer.__main__:cli']}

setup_kwargs = {
    'name': 'fail2ban-importer',
    'version': '0.0.9',
    'description': 'Takes banlists and uses fail2ban to block them',
    'long_description': '# fail2ban-from-s3\n\nGrabs a JSON-encoded list of things to ban and bans them using [fail2ban](https://www.fail2ban.org).\n\n# Installation\n\n`python -m pip install --upgrade fail2ban-importer`\n\n# Usage\n\n`fail2ban-importer [--oneshot|--dryrun]`\n\n# Configuration\n\nThe following paths will be tested (in order) and the first one loaded:\n\n - `./fail2ban-importer.json`\n - `/etc/fail2ban-importer.json`\n - `~/.config/fail2ban-importer.json`\n\n## Fields \n\nNote the `fail2ban_jail` field. If you\'re going to pick up your logs from fail2ban, and use them for the source of automation, make sure to filter out the actions by this system - otherwise you\'ll end up in a loop!\n\n| Field Name        | Value Type | Default Value     | Required | Description |\n| ---               |     ---    |     ---           |  ---     |    ---   |\n| `download_module` | `str`      | `http`            | No       | The download module to use (either `http` or `s3`)  |\n| `fail2ban_jail`   | `str`      | unset             | **Yes**  | The jail to use for banning - DO NOT REUSE AN EXISTING JAIL |\n| `source`          | `str`      | `blank`           | **Yes**  | Where to pull the file from, can be a `http(s)://` or `s3://` URL. |\n| `fail2ban_client` | `str`      | `fail2ban_client` | No       |  The path to the `fail2ban-client` executable, in case it\'s not in the user\'s `$PATH` |\n| `schedule_mins`   | `int`      | 15                | No       | How often to run the action. |\n| `s3_endpoint`     | `str`      |                   | No       | The endpoint URL if you need to force it for s3, eg if you\'re using minio or another S3-compatible store. |\n| `s3_v4`           | `bool`     | `false`           | No       | Whether to force `s3_v4` requests (useful for minio) |\n| `s3_minio`        | `bool`     | `false`           | No       | Enable minio mode, force `s3_v4` requests |\n\n## HTTP(S) Source\n\n```json fail2ban-importer.json\nx\n{\n    "source": "https://example.com/fail2ban.json",\n    "fail2ban_client": "/usr/bin/fail2ban-client",\n    "fail2ban_jail" : "automated",\n    "schedule_mins" : 15\n}\n```\n\n## S3-compatible Source\n\nYou can use the usual [boto3 AWS configuration](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html#configuration), or put the options in the config file.\n\n```json fail2ban-importer.json\n{\n    "source": "s3://my-magic-fail2ban-bucket/fail2ban.json",\n    "AWS_ACCESS_KEY_ID" : "exampleuser",\n    "AWS_SECRET_ACCESS_KEY" : "hunter2",\n    "schedule_mins" : 1\n}\n```\n\nIf you\'re using minio as your backend, you should add the following additional options to the config file:\n\n```json\n{\n    "s3_v4" : true,\n    "s3_endpoint" : "https://example.com",\n}\n```\n\n# Example source data file\n\n```json data.json\n[\n  {\n    "jail": "sshd",\n    "ip": "196.30.15.254"\n  },\n  {\n    "jail": "sshd",\n    "ip": "119.13.89.28"\n  }\n]\n```\n\n# Thanks\n\n - [fail2ban](https://www.fail2ban.org)\n - [boto3](https://boto3.amazonaws.com)\n - [requests](https://docs.python-requests.org/en/master/index.html)\n - [schedule](https://schedule.readthedocs.io/en/stable/)',
    'author': 'James Hodgkinson',
    'author_email': 'james@terminaloutcomes.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
