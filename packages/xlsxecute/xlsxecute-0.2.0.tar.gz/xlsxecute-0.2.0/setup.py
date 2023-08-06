# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xlsxecute']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.4,<9.0.0', 'formulas>=1.2.2,<2.0.0', 'openpyxl>=3.0.9,<4.0.0']

entry_points = \
{'console_scripts': ['xlsxecute = xlsxecute.command:main']}

setup_kwargs = {
    'name': 'xlsxecute',
    'version': '0.2.0',
    'description': 'Runs an Excel model (.xlsx) with parameters',
    'long_description': '# xlsxecute\n\nThis tool will take an Excel model (.xlsx), update any parameters as defined via command line arguments or in the parameters file and calculate all cells, resulting in an Excel spreadsheet resembling the original, but with all formula cells replaced by the calculated values.\n\nParameters that define how to update cells in your spreadsheet can be provided in three ways: \nJSON file, CSV file, or command line arguments\n\nIf both a config file and command line arguments are provided, the command line arguments \n\n\n### Config file formatting\n\nOnly one config file can be provided at a time. The config file can either be \n\n#### Command line arguments:\n\nCommand line arguments take the form of:\n```bash\n-f "Sheet name.Cell1=Replacement value string" -f "Sheet name.Cell2=Replacement_value_float"\n```\nNote: Quotation marks are not required if there no space in the parameter string.\n\nExample:\n```\nxlsxecute -f "Variables.C2=red" -f Variables.C3=0.8 sample.xlsx\n```\n\n#### JSON:\n```json\n{\n   "Sheet name.Cell1": "Replacement value string",\n   "Sheet name.Cell2": Replacement_value_float\n}\n```\n\nExample: params.json\n```json\n{\n    "Variables.C2": "red",\n    "Variables.C3": 0.8\n}\n```\n\n\n#### CSV:\n```csv\nSheet name.Cell1,Replacement value string\nSheet name.Cell2,Replacement value float\n```\n\nExample: params.csv\n```csv\nVariables.C2,red\nVariables.C3,0.8\n```\n\nNOTE: Do NOT include a header row in the CSV\n\n<br/>\n<br/>\n\n\n#### Executable usage:\n\n```\nusage: xlsxecute [-h] [--output_dir OUTPUT_DIR] [--run_dir RUN_DIR] [--param {sheet}.{cell}={new_value}] source_file [parameter_file]\n\npositional arguments:\n  source_file           Excel (xlsx) file that contains the model\n  parameter_file        Path to json or csv parameter file\n\noptional arguments:\n  -h, --help            show this help message and exit\n  --output_dir OUTPUT_DIR\n                        Optional output location. (Default: output)\n  --run_dir RUN_DIR     Optional directory to store intermediate files. (Default: runs)\n  --param {sheet}.{cell}={new_value}, -p {sheet}.{cell}={new_value}\n```\n',
    'author': 'Matthew Printz',
    'author_email': 'matt@jataware.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dojo-modeling/xlsxecute',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
