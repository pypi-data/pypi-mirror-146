# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gcal_cmd_tool', 'gcal_cmd_tool.libs']

package_data = \
{'': ['*']}

install_requires = \
['google-api-python-client>=2.42.0,<3.0.0',
 'google-auth-httplib2>=0.1.0,<0.2.0',
 'google-auth-oauthlib>=0.5.1,<0.6.0',
 'typer[all]>=0.4.1,<0.5.0']

entry_points = \
{'console_scripts': ['gcal-cmd-tool = gcal_cmd_tool.main:app']}

setup_kwargs = {
    'name': 'gcal-cmd-tool',
    'version': '0.1.0',
    'description': 'A command line tool to manage Google Calendars',
    'long_description': '# gcal-cmd-tool\nA command line tool to manage Google Calendars\n\n## Authentication\nAuthentication to Google Calendar API is done using a service account. Instructions can be read on Google\'s [Authenticating as a service account ](https://cloud.google.com/docs/authentication/production).\n\nTo set the environment variable `GOOGLE_APPLICATION_CREDENTIALS` on Linux run the following command:\n```bash\nexport GOOGLE_APPLICATION_CREDENTIALS="KEY_PATH"\n```\nReplace KEY_PATH with the path of the JSON file that contains your service account key.\n\nFor example:\n```bash\nexport GOOGLE_APPLICATION_CREDENTIALS="/home/user/Downloads/service-account-file.json"\n```\n\n## Resource types\n\n### Acl\n#### list\nReturns the rules in the access control list for the calendar.\n```bash\n$ python3 main.py acl list [OPTIONS] CALENDAR\n```\n#### insert\nCreates an access control rule.\n#### delete\nDeletes an access control rule. \n\n### Calendars\n#### get\nReturns metadata for a calendar. \n#### delete\nDeletes a secondary calendar.',
    'author': 'Alexandre Santos',
    'author_email': 'ajvsms@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
