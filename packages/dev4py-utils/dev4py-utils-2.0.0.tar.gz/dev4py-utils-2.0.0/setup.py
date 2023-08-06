# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src/test/python'}

packages = \
['python', 'python.dev4py.utils', 'python.dev4py.utils_test']

package_data = \
{'': ['*']}

modules = \
['project']
setup_kwargs = {
    'name': 'dev4py-utils',
    'version': '2.0.0',
    'description': 'A set of Python regularly used classes/functions',
    'long_description': '# Dev4py-utils\n\nA set of Python regularly used classes/functions\n\n[![ci](https://github.com/dev4py/dev4py-utils/actions/workflows/ci.yml/badge.svg?event=push&branch=main)](https://github.com/dev4py/dev4py-utils/actions/workflows/ci.yml) <br/>\n[![Last release](https://github.com/dev4py/dev4py-utils/actions/workflows/on_release.yml/badge.svg)](https://github.com/dev4py/dev4py-utils/actions/workflows/on_release.yml) <br/>\n[![Weekly checks](https://github.com/dev4py/dev4py-utils/actions/workflows/weekly_checks.yml/badge.svg?branch=main)](https://github.com/dev4py/dev4py-utils/actions/workflows/weekly_checks.yml) <br/>\n[![Python >= 3.10.1](https://img.shields.io/badge/Python->=3.10.1-informational.svg?style=plastic&logo=python&logoColor=yellow)](https://www.python.org/) <br/>\n[![Maintainer](https://img.shields.io/badge/maintainer-St4rG00se-informational?style=plastic&logo=superuser)](https://github.com/St4rG00se) <br/>\n[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg?style=plastic&logo=github)](https://GitHub.com/Naereen/StrapDown.js/graphs/commit-activity) <br/>\n[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=plastic&logo=github)](https://opensource.org/licenses/MIT)\n\n## Table of contents\n\n- [Project template](#project-template)\n- [Project links](#project-links)\n- [Dev4py-utils modules](#dev4py-utils-modules)\n    * [dev4py.utils.JOptional](#dev4pyutilsjoptional)\n    * [dev4py.utils.objects](#dev4pyutilsobjects)\n    * [dev4py.utils.types](#dev4pyutilstypes)\n\n## Project template\n\nThis project is based on [pymsdl_template](https://github.com/dev4py/pymsdl_template)\n\n## Project links\n\n* [Documentation](https://htmlpreview.github.io/?https://github.com/dev4py/dev4py-utils/blob/main/docs/dev4py/utils.html)\n* [PyPi project](https://pypi.org/project/dev4py-utils/)\n\n## Dev4py-utils modules\n\n### dev4py.utils.JOptional\n\n[JOptional documentation](https://htmlpreview.github.io/?https://github.com/dev4py/dev4py-utils/blob/main/docs/dev4py/utils/JOptional.html)\n\n> ***Note:** [JOptional](src/main/python/dev4py/utils/JOptional.py) class is inspired from\n> [java.util.Optional](https://docs.oracle.com/en/java/javase/17/docs/api//java.base/java/util/Optional.html)\n> class with some adds (like `peek` method).*\n\nExamples:\n\n```python\nfrom dev4py.utils import JOptional\n\nvalue = 1\n\nJOptional.of_noneable(value).map(lambda v: f"The value is {v}").if_present(print)\n```\n\n### dev4py.utils.objects\n\n[Objects documentation](https://htmlpreview.github.io/?https://github.com/dev4py/dev4py-utils/blob/main/docs/dev4py/utils/objects.html)\n\n> ***Note:** The [objects](src/main/python/dev4py/utils/objects.py) module is inspired from\n> [java.util.Objects](https://docs.oracle.com/en/java/javase/17/docs/api//java.base/java/util/Objects.html)\n> class.*\n\nExamples:\n\n```python\nfrom dev4py.utils import objects\n\n# non_none sample\nvalue = None\nobjects.non_none(value)\n\n# require_non_none sample\nvalue = "A value"\nobjects.require_non_none(value)\n\n# to_string sample\nvalue = None\ndefault_value: str = "A default value"\nobjects.to_string(value, default_value)\n```\n\n### dev4py.utils.types\n\n[Types documentation](https://htmlpreview.github.io/?https://github.com/dev4py/dev4py-utils/blob/main/docs/dev4py/utils/types.html)\n\n> ***Note:** The [types](src/main/python/dev4py/utils/types.py) module is inspired from\n> [java.util.function](https://docs.oracle.com/en/java/javase/17/docs/api//java.base/java/util/function/package-summary.html)\n> package*\n\nExamples:\n\n```python\nfrom dev4py.utils.types import Function, Predicate, Consumer\n\n# Function sample\nint_to_str: Function[int, str] = lambda i: str(i)\nstr_result: str = int_to_str(1)\n\n# Predicate sample\nstr_predicate: Predicate[str] = lambda s: s == "A value"\npred_result = str_predicate("Value to test")\n\n\n# Consumer sample\ndef sample(consumer: Consumer[str], value: str) -> None:\n    consumer(value)\n\n\ndef my_consumer(arg: str) -> None:\n    print(arg)\n\n\nsample(my_consumer, "My value")\n```\n',
    'author': 'St4rG00se',
    'author_email': 'st4rg00se@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dev4py/dev4py-utils',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
