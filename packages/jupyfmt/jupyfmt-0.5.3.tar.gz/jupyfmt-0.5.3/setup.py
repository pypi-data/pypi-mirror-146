# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jupyfmt']

package_data = \
{'': ['*']}

install_requires = \
['black>=21.4,<23.0', 'click>=7.1.2,<9.0.0', 'nbformat>=5.1.2,<6.0.0']

entry_points = \
{'console_scripts': ['jupyfmt = jupyfmt:main']}

setup_kwargs = {
    'name': 'jupyfmt',
    'version': '0.5.3',
    'description': 'Format code in Jupyter notebooks',
    'long_description': "# jupyfmt\n\n[![PyPI](https://img.shields.io/pypi/v/jupyfmt.svg?style=flat)](https://pypi.python.org/pypi/jupyfmt)\n[![Tests](https://github.com/kpj/jupyfmt/workflows/Tests/badge.svg)](https://github.com/kpj/jupyfmt/actions)\n\nThe uncompromising Jupyter notebook formatter.\n\n`jupyfmt` allows you to format notebooks in-place from the commandline as well as assert properly formatted Jupyter notebook cells in your CI.\nInspired by [snakefmt](https://github.com/snakemake/snakefmt/). Uses [black](https://github.com/psf/black/) under the hood.\n\n\n## Installation\n\nInstall the latest release from PyPI:\n\n```python\n$ pip install jupyfmt\n```\n\n\n## Usage\n\n`jupyfmt` can be used to format notebooks in-place or report diffs and summary statistics.\n\nOverview of commandline parameters:\n```\n$ jupyfmt --help\nUsage: jupyfmt [OPTIONS] [PATH_LIST]...\n\n  The uncompromising Jupyter notebook formatter.\n\n  PATH_LIST specifies notebooks and directories to search for notebooks in. By\n  default, all notebooks will be formatted in-place. Use `--check`, `--diff`\n  (or `--compact-diff`) to print summary reports instead.\n\nOptions:\n  -l, --line-length INT           How many characters per line to allow.\n  -S, --skip-string-normalization\n                                  Don't normalize string quotes or prefixes.\n  --check                         Don't write files back, just return status\n                                  and print summary.\n  -d, --diff                      Don't write files back, just output a diff\n                                  for each file to stdout.\n  --compact-diff                  Same as --diff but only show lines that\n                                  would change plus a few lines of context.\n  --assert-consistent-execution   Assert that all cells have been executed in\n                                  correct order.\n  --exclude PATTERN               Regular expression to match paths which\n                                  should be exluded when searching\n                                  directories.  [default: (/.git/|/.ipynb_chec\n                                  kpoints/|/build/|/dist/)]\n  --accepted-languages PATTERN    Only format Jupyter notebooks in these\n                                  languages.  [default: python]\n  --version                       Show the version and exit.\n  --help                          Show this message and exit.\n```\n\nReport formatting suggestions for a given notebook (this is particularly useful for CI workflows):\n```bash\n$ jupyfmt --check --compact-diff Notebook.ipynb\n--- Notebook.ipynb - Cell 1 (original)\n+++ Notebook.ipynb - Cell 1 (formatted)\n@@ -1,2 +1,2 @@\n-def foo (*args):\n+def foo(*args):\n     return sum(args)\n\n--- Notebook.ipynb - Cell 2 (original)\n+++ Notebook.ipynb - Cell 2 (formatted)\n@@ -1 +1 @@\n-foo(1, 2,3)\n+foo(1, 2, 3)\n\n2 cell(s) would be changed 😬\n1 cell(s) would be left unchanged 🎉\n\n1 file(s) would be changed 😬\n```\n\n## Mega-Linter Integration\n\n`jupyfmt` can be run as part of [Mega-Linter](https://github.com/nvuillam/mega-linter) by adding the following to `.mega-linter.yml`:\n\n```yaml\nPLUGINS:\n  - https://raw.githubusercontent.com/kpj/jupyfmt/master/mega-linter-plugin-jupyfmt/jupyfmt.megalinter-descriptor.yml\n\nENABLE_LINTERS:\n  - JUPYTER_JUPYFMT\n```\n",
    'author': 'kpj',
    'author_email': 'kim.philipp.jablonski@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kpj/jupyfmt',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.0,<4.0.0',
}


setup(**setup_kwargs)
