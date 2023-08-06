# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['table2sql', 'table2sql.converters']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1,<9.0.0', 'openpyxl>=3.0.7,<4.0.0']

entry_points = \
{'console_scripts': ['table2sql = table2sql.cli:table2sql']}

setup_kwargs = {
    'name': 'table2sql',
    'version': '1.0.1',
    'description': '',
    'long_description': "# table2sql\n\n[![CI](https://github.com/piotrgredowski/table2sql/actions/workflows/ci.yml/badge.svg)](https://github.com/piotrgredowski/table2sql/actions/workflows/ci.yml)\n[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=piotrgredowski_table2sql&metric=alert_status)](https://sonarcloud.io/dashboard?id=piotrgredowski_table2sql)\n[![codecov](https://codecov.io/gh/piotrgredowski/table2sql/branch/main/graph/badge.svg?token=fNkIDyWLq7)](https://codecov.io/gh/piotrgredowski/table2sql)\n[![CodeQL](https://github.com/piotrgredowski/table2sql/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/piotrgredowski/table2sql/actions/workflows/codeql-analysis.yml)\n\nPython CLI tool which allows you to convert file with table (CSV and Excel) to SQL insert statements.\n\n[Docs](https://gredowski.com/table2sql/)\n\n## Basic usage\n\n`some.csv`\n\n```csv\na,b,c,d\nint,str,float,sql\n1,2,3,(SELECT id FROM another.table WHERE name = 'Paul')\n5,6,7,(SELECT id FROM another.table WHERE name = 'Paul')\n```\n\nCommand:\n\n```bash\ntable2sql some.csv --output-table some.table --has-types-row\n```\n\nResult:\n\n```sql\nINSERT INTO some.table (a, b, c, d)\nVALUES (1, '2', 3.0, (SELECT id FROM another.table WHERE name = 'Paul')), (5, '6', 7.0, (SELECT id FROM another.table WHERE name = 'Paul'));\n```\n\n## Install\n\n```bash\npip install table2sql\n```\n",
    'author': 'Piotr Gredowski',
    'author_email': 'piotrgredowski@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/piotrgredowski/table2sql',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0',
}


setup(**setup_kwargs)
