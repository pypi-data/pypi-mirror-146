# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['seqdat']

package_data = \
{'': ['*']}

install_requires = \
['click-rich-help>=0.3.0',
 'click>=8.0.3,<9.0.0',
 'rich>=10.12.0',
 'tomlkit>=0.10.1']

entry_points = \
{'console_scripts': ['seqdat = seqdat.cli:main']}

setup_kwargs = {
    'name': 'seqdat',
    'version': '22.1.2',
    'description': 'sequencing data manager',
    'long_description': '# SEQDAT\n\n**Seq**uencing **Dat**a Manager\n\n## Usage\n\nSee [docs](docs/usage.md) for more info. Also view available commands with `--help`.\n\n```bash\nseqdat --help\n```\n\n## Development\n\nTo make changes to seqdat generate a new conda enviroment and install dependencies with poetry.\n\n```bash\ngit clone git@github.com:daylinmorgan/seqdat.git\ncd seqdat\nmamba create -p ./env python poetry\nmamba activate ./env\npoetry install\n```\n\n`Black`, `isort` and `flake8` are applied via `pre-commit`, additionally type checking should be enforced with `mypy seqdat`.\n\nWith `just` you can run `just lint`.\n\nAfter making a patch or preparing new minor release use `bumpver` to update version and generate the `git` tag and commit.\n\n## Standalone Binary\n\nUsing `pyoxidizer` and the included config file you can easily generate a standalone binary to handle python and associated dependencies.\n\nRun the below command to generate the binary:\n```bash\npyoxidizer build --release\n```\n\nThis will fetch the necessary `rust`/`python` components necessary to compile everything.\n\nThen you can find your final binary in `./build/x86_64-unknown-linux-gnu/release/install/seqdat/`.\n\n*Note*: If you have `just` and `pyoxidizer` installed you can run `just build install` to build the binary and copy it to `~/bin`.\n',
    'author': 'Daylin Morgan',
    'author_email': 'daylinmorgan@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/daylinmorgan/seqdat',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
