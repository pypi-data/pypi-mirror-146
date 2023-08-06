# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['actfw_core',
 'actfw_core._private.agent_app_protocol',
 'actfw_core._private.compat',
 'actfw_core._private.schema',
 'actfw_core._private.util',
 'actfw_core.schema',
 'actfw_core.task',
 'actfw_core.util',
 'actfw_core.v4l2']

package_data = \
{'': ['*']}

extras_require = \
{':python_version < "3.7"': ['dataclasses>=0.8,<0.9'],
 ':python_version < "3.8"': ['Pillow>=5,<6'],
 ':python_version >= "3.8"': ['Pillow>=8,<9']}

setup_kwargs = {
    'name': 'actfw-core',
    'version': '2.2.0a1',
    'description': 'Core components of actfw, independent of specific devices',
    'long_description': "# actfw-core\n\nCore components of actfw, a framework for Actcast Application written in Python.\nactfw-core is intended to be independent of any specific device.\n\n## Installation\n\n```console\nsudo apt-get update\nsudo apt-get install -y python3-pip python3-pil \nsudo apt-get install -y libv4l-0 libv4lconvert0  # if using `V4LCameraCapture`\npip3 install actfw-core\n```\n\n## Document\n\n* [API References](https://idein.github.io/actfw-core/latest/)\n\n## Usage\n\nConstruct your application with a task parallel model\n\n* Application\n  * `actfw_core.Application` : Main application\n* Workers\n  * `actfw_core.task.Producer` : Task generator\n    * `actfw_core.capture.V4LCameraCapture` : Generate UVC camera capture image\n  * `actfw_core.task.Pipe` : Task to Task converter\n  * `actfw_core.task.Consumer` : Task terminator\n\nEach worker is executed in parallel.\n\nUser should\n\n* Define subclass of `Producer/Pipe/Consumer`\n\n```python\nclass MyPipe(actfw_core.task.Pipe):\n    def proc(self, i):\n        ...\n```\n\n* Connect defined worker objects\n\n```python\np  = MyProducer()\nf1 = MyPipe()\nf2 = MyPipe()\nc  = MyConsumer()\np.connect(f1)\nf1.connect(f2)\nf2.connect(c)\n```\n\n* Register to `Application`\n\n```python\napp = actfw_core.Application()\napp.register_task(p)\napp.register_task(f1)\napp.register_task(f2)\napp.register_task(c)\n```\n\n* Execute application\n\n```python\napp.run()\n```\n\n## Development Guide\n\n### Installation of dev requirements\n\n```console\npip3 install poetry\npoetry install\n```\n\n### Running tests\n\n```console\npoetry run nose2 -v\n```\n\n### Releasing package & API doc\n\nCI will automatically do.\nFollow the following branch/tag rules.\n\n1. Make changes for next version in `master` branch (via pull-requests).\n2. Make a PR that updates version in `pyproject.toml` and merge it to `master` branch.\n3. Create Git tag from `master` branch's HEAD named `release-<New version>`. E.g. `release-1.4.0`.\n4. Then CI will build/upload package to PyPI & API doc to GitHub Pages.\n",
    'author': 'Idein Inc.',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Idein/actfw-core',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
