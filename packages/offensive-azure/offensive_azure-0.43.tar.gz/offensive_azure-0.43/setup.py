# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['offensive_azure',
 'offensive_azure.Access_Tokens',
 'offensive_azure.Device_Code',
 'offensive_azure.Outsider_Recon',
 'offensive_azure.User_Enum']

package_data = \
{'': ['*']}

install_requires = \
['colorama>=0.4.4,<0.5.0',
 'dnspython>=2.2.1,<3.0.0',
 'requests>=2.27.1,<3.0.0',
 'uuid>=1.30,<2.0']

setup_kwargs = {
    'name': 'offensive-azure',
    'version': '0.43',
    'description': 'Collection of tools for attacking Microsoft Cloud products',
    'long_description': '<p align="center">\n  <img src="https://user-images.githubusercontent.com/28767257/160513484-cb70370c-9fce-48d1-84ec-8b9ea3cf8e5a.png">\n</p>\n\nCollection of offensive tools targeting Microsoft Azure written in Python to be platform agnostic. The current list of tools can be found below with a brief description of their functionality.\n\n- [`./Device_Code/device_code_easy_mode.py`](https://github.com/blacklanternsecurity/offensive-azure/tree/main/Device_Code)\n  - Generates a code to be entered by the target user\n  - Can be used for general token generation or during a phishing/social engineering campaign.\n- [`./Access_Tokens/token_juggle.py`](https://github.com/blacklanternsecurity/offensive-azure/tree/main/Access_Tokens)\n  - Takes in a refresh token in various ways and retrieves a new refresh token and an access token for the resource specified\n- [`./Outsider_Recon/outsider_recon.py`](https://github.com/blacklanternsecurity/offensive-azure/tree/main/Outsider_Recon)\n  - Takes in a domain and enumerates as much information as possible about the tenant without requiring authentication \n- [`./User_Enum/user_enum.py`](https://github.com/blacklanternsecurity/offensive-azure/tree/main/User_Enum)\n  - Takes in a username or list of usernames and attempts to enumerate valid accounts using one of three methods\n  - Can also be used to perform a password spray\n',
    'author': 'Cody Martin',
    'author_email': 'debifrank00@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/blacklanternsecurity.com/offensive-azure',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
