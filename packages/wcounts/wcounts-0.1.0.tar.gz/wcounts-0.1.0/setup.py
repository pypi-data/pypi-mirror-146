# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['wcounts']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.5.1']

setup_kwargs = {
    'name': 'wcounts',
    'version': '0.1.0',
    'description': 'Calculate word counts in a text file!',
    'long_description': '# wcounts\n\nCalculate word counts in a text file!\n\n## Installation\n\n```bash\n$ pip install wcounts\n```\n\n## Usage\n\n`wcounts` can be used to count words in a text file and plot results\nas follows:\n\n```python\nfrom wcounts.wcounts import count_words\nfrom wcounts.plotting import plot_words\nimport matplotlib.pyplot as plt\n\nfile_path = "test.txt"  # path to your file\ncounts = count_words(file_path)\nfig = plot_words(counts, n=10)\nplt.show()\n```\n\n## Contributing\n\nInterested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.\n\n## License\n\n`wcounts` was created by nazbn. It is licensed under the terms of the MIT license.\n\n## Credits\n\n`wcounts` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n',
    'author': 'nazbn',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9',
}


setup(**setup_kwargs)
