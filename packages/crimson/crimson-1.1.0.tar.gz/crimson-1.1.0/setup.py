# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['crimson']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.2,<6.0', 'click>=8.0,<9.0', 'single-source>=0.2.0,<0.3.0']

entry_points = \
{'console_scripts': ['crimson = crimson.cli:main']}

setup_kwargs = {
    'name': 'crimson',
    'version': '1.1.0',
    'description': 'Bioinformatics tool outputs converter to JSON or YAML',
    'long_description': '# `crimson`\n\n[![pypi](https://img.shields.io/pypi/v/crimson)](https://pypi.org/project/crimson)\n[![sourcehut](https://builds.sr.ht/~bow/crimson.svg)](https://builds.sr.ht/~bow/crimson?)\n\n\n``crimson`` converts non-standard bioinformatics tool outputs to JSON or YAML.\n\nCurrently it can convert outputs of the following tools:\n\n  * [FastQC](http://www.bioinformatics.babraham.ac.uk/projects/fastqc/>) (``fastqc``)\n  * [FusionCatcher](https://github.com/ndaniel/fusioncatcher) (``fusioncatcher``)\n  * [samtools](http://www.htslib.org/doc/samtools.html) flagstat (``flagstat``)\n  * [Picard](https://broadinstitute.github.io/picard/) metrics tools (``picard``)\n  * [STAR](https://github.com/alexdobin/STAR) log file (``star``)\n  * [STAR-Fusion](https://github.com/STAR-Fusion/STAR-Fusion) hits table (``star-fusion``)\n  * [Variant Effect Predictor](http://www.ensembl.org/info/docs/tools/vep/index.html)\n    plain text output (``vep``)\n\nThe conversion can be done using the command line interface or by calling the\ntool-specificparser functions in your Python script.\n\n\n## Installation\n\n``crimson`` is available on the [Python Package Index](https://pypi.org/project/crimson/)\nand you can install it via ``pip``:\n\n```shell\n$ pip install crimson\n```\n\nIt is also available on\n[BioConda](https://bioconda.github.io/recipes/crimson/README.html), both through the\n`conda` package manager or as a\n[Docker container](https://quay.io/repository/biocontainers/crimson?tab=tags).\n\n\n## Usage\n\n### As a command line tool\n\nThe general command is `crimson {program_name}` and by default the output is written to\n`stdout`. For example, to use the `picard` parser, you would execute:\n\n```shell\n$ crimson picard /path/to/a/picard.metrics\n```\n\nYou can also specify a file name directly to write to a file. The following command will\nwrite the output to a file named ``converted.json``:\n\n```shell\n$ crimson picard /path/to/a/picard.metrics converted.json\n```\n\nSome parsers may also accept additional input format. The FastQC parser, for example, also\nworks if you specify a path to a FastQC output directory:\n\n\n```shell\n$ crimson fastqc /path/to/a/fastqc/dir\n```\n\nor path to a zipped result:\n\n```shell\n$ crimson fastqc /path/to/a/fastqc_result.zip\n```\n\nWhen in doubt, use the ``--help`` flag:\n\n```shell\n$ crimson --help            # for the general help\n$ crimson fastqc --help     # for parser-specific (FastQC) help\n```\n\n### As a Python library function\n\nGenerally, the function to import is located at `crimson.{program_name}.parser`. For\nexample, to use the `picard` parser in your script, you can do:\n\n```python\nfrom crimson import picard\n\n# You can specify the input file name as a string ...\nparsed = picard.parse("/path/to/a/picard.metrics")\n\n# ... or a file handle\nwith open("/path/to/a/picard.metrics") as src:\n    parsed = picard.parse(src)\n```\n\n## Why?\n\n  * Not enough tools use standard output formats.\n  * Writing and re-writing the same parsers across different scripts is not a productive\n    way to spend the day.\n\n\n## Local Development\n\nSetting up a local development requires that you set up all of the supported Python\nversions. We recommend using [pyenv](https://github.com/pyenv/pyenv) for this.\n\nThe following steps can be your guide for your local development setup:\n\n```shell\n# Clone the repository and cd into it.\n$ git clone https://git.sr.ht/~bow/crimson\n$ cd crimson\n\n# Create your virtualenv.\n# If you already have pyenv installed, you may use the Makefile rule below.\n$ make dev-pyenv\n\n# Install the package along with its development dependencies.\n$ make dev\n\n# Run the test and linter suite to verify the setup.\n$ make lint test\n```\n\n\n## Contributing\n\nIf you are interested, `crimson` accepts the following types contribution:\n\n  * Documentation additions (if anything seems unclear, feel free to open an issue)\n  * Bug reports\n  * Support for tools\' outputs which can be converted to JSON or YAML.\n\nFor any of these, feel free to open an issue in the [issue\ntracker](https://github.com/bow/crimson/issues>) or submit a pull request.\n\n\n## License\n\n``crimson`` is BSD-licensed. Refer to the ``LICENSE`` file for the full license.\n',
    'author': 'Wibowo Arindrarto',
    'author_email': 'contact@arindrarto.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://git.sr.ht/~bow/crimson',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
