# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pypisd']

package_data = \
{'': ['*']}

install_requires = \
['bs4>=0.0.1,<0.0.2', 'requests>=2.27.1,<3.0.0', 'toml>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['pypisd = pypisd.main:cli']}

setup_kwargs = {
    'name': 'pypisd',
    'version': '0.1.3',
    'description': 'CLI tool to fetch source distribution url links from https://pypi.org for a given python package and its version.',
    'long_description': '# PyPiSD (PyPi Source Distribution)\n\nCLI tool to fetch source distribution url links from https://pypi.org for a given python package and its version.\n\n## Installing PyPiSD\n\nPypiSD is available on PyPi:\n\n```\n$ pip install pypisd\n```\n\n## How to use it\n\n### Fetching source distribution url\'s from environment\n\nRunning `pypisd` in your command line, the tool will fetch the packages installed in the environment where the command runs. In the background, it fetches this list by runing `pip list`.\n\n### Fetching source distribution url\'s from file\nYou can get the list of distribution links by providing a file that contains the list of libraries (like a requirements.txt file) or a file where in each line, library name and version are separated with a comma. You can see an example of what type of formats are allowed in `tests/test_input_file.txt`.\n\n```\n$ pypisd --input_file=tests/test_input_file.txt\n```\n\nYou can provide a toml file as an input too, and will get the source distribution links for the dependencies defined inside\n\n```\n$ pypisd --input_file=tests/pyproject_test.toml\n```\n\n### Output of the CLI task\n\nAfter running `pypisd` the output will be saved in a csv file. By default, the file name is "pypi_sd_links.csv".\nYou can providen the file name where the output should be saved by running:\n\n```\n$ pypisd --output_file="my_file_csv"\n```\n\n```\n$ pypisd --o="my_file_csv"\n```\n\n\nThe file has the following columns:\n\n- library_name: Name of the library.\n- version: version of the library. If none could be read from the environment/input file, "using latest version" will be used instead.\n- license: Defines the license that the library uses.\n- source_distribution_link: Link to download the source distribution for this given library&version. If not found, it will be replaced by "Can not find download link for My Library, version 0.0.1"\n\n\n| library_name      | version | license | source_distribution_link |\n| ----------- | ----------- | ----------- | ----------- |\n|bs4 | 0.0.1 | Not found| https://files.pythonhosted.org/packages/10/ed/7e8b97591f6f456174139ec089c769f89a94a1a4025fe967691de971f314/bs4-0.0.1.tar.gz |\n|beautifulsoup4|4.10.0|MIT License (MIT)|https://files.pythonhosted.org/packages/a1/69/daeee6d8f22c997e522cdbeb59641c4d31ab120aba0f2c799500f7456b7e/beautifulsoup4-4.10.0.tar.gz\nidna|3.3|BSD License (BSD-3-Clause)|https://files.pythonhosted.org/packages/62/08/e3fc7c8161090f742f504f40b1bccbfc544d4a4e09eb774bf40aafce5436/idna-3.3.tar.gz|\n|attrs|21.4.0|MIT License (MIT)|https://files.pythonhosted.org/packages/d7/77/ebb15fc26d0f815839ecd897b919ed6d85c050feeb83e100e020df9153d2/attrs-21.4.0.tar.gz|\n|certifi|2021.10.8|Mozilla Public License 2.0 (MPL 2.0) (MPL-2.0)|https://files.pythonhosted.org/packages/6c/ae/d26450834f0acc9e3d1f74508da6df1551ceab6c2ce0766a593362d6d57f/certifi-2021.10.8.tar.gz|\n|packaging|21.3|"Apache Software License BSD License (BSD-2-Clause or Apache-2.0)"|https://files.pythonhosted.org/packages/df/9e/d1a7217f69310c1db8fdf8ab396229f55a699ce34a203691794c5d1cad0c/packaging-21.3.tar.gz|\n|pluggy|0.13.1|MIT License (MIT license)|https://files.pythonhosted.org/packages/f8/04/7a8542bed4b16a65c2714bf76cf5a0b026157da7f75e87cc88774aa10b14/pluggy-0.13.1.tar.gz|\n|charset-normalizer|2.0.12|MIT License (MIT)|https://files.pythonhosted.org/packages/56/31/7bcaf657fafb3c6db8c787a865434290b726653c912085fbd371e9b92e1c/charset-normalizer-2.0.12.tar.gz|\n|pypisd|0.1.0|Not found|"Can not find download link for pypisd, version 0.1.0"|\n|more-itertools|8.12.0|MIT License (MIT)|https://files.pythonhosted.org/packages/dc/b5/c216ffeace7b89b7387fe08e1b39a07c6da38ea82c60e2e630dd5883813b/more-itertools-8.12.0.tar.gz|\n|pip|22.0.4|MIT License (MIT)|https://files.pythonhosted.org/packages/33/c9/e2164122d365d8f823213a53970fa3005eb16218edcfc56ca24cb6deba2b/pip-22.0.4.tar.gz|\n|py|1.11.0|MIT License (MIT license)|https://files.pythonhosted.org/packages/98/ff/fec109ceb715d2a6b4c4a85a61af3b40c723a961e8828319fbcb15b868dc/py-1.11.0.tar.gz|\n|pyparsing|3.0.7|MIT License (MIT License)|https://files.pythonhosted.org/packages/d6/60/9bed18f43275b34198eb9720d4c1238c68b3755620d20df0afd89424d32b/pyparsing-3.0.7.tar.gz|\n|soupsieve|2.3.1|MIT License (MIT License)|https://files.pythonhosted.org/packages/e1/25/a3005eedafb34e1258458e8a4b94900a60a41a2b4e459e0e19631648a2a0/soupsieve-2.3.1.tar.gz|\n|pytest|5.4.3|MIT License (MIT license)|https://files.pythonhosted.org/packages/8f/c4/e4a645f8a3d6c6993cb3934ee593e705947dfafad4ca5148b9a0fde7359c/pytest-5.4.3.tar.gz|\n|wcwidth|0.2.5|MIT License (MIT)|https://files.pythonhosted.org/packages/89/38/459b727c381504f361832b9e5ace19966de1a235d73cdbdea91c771a1155/wcwidth-0.2.5.tar.gz|\n|wheel|0.37.1|MIT License (MIT)|https://files.pythonhosted.org/packages/c0/6c/9f840c2e55b67b90745af06a540964b73589256cb10cc10057c87ac78fc2/wheel-0.37.1.tar.gz|\n|requests|2.27.1|Apache Software License (Apache 2.0)|https://files.pythonhosted.org/packages/60/f3/26ff3767f099b73e0efa138a9998da67890793bfa475d8278f84a30fec77/requests-2.27.1.tar.gz|\n|urllib3|1.26.9|MIT License (MIT)|https://files.pythonhosted.org/packages/1b/a5/4eab74853625505725cefdf168f48661b2cd04e7843ab836f3f63abf81da/urllib3-1.26.9.tar.gz|\n|setuptools|61.0.0|MIT License|https://files.pythonhosted.org/packages/cf/68/bc4babfa1f0853d9164ed8f9fc97e3cc8293fa6e77277fb1a72b4de75ba5/setuptools-61.0.0.tar.gz|\n',
    'author': 'Fernando',
    'author_email': 'fegoa89@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fegoa89/pypisd',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
