# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

modules = \
['vai_jobspec_tools']
setup_kwargs = {
    'name': 'vai-jobspec-tools',
    'version': '1.0.0',
    'description': 'Utilities for VoxelAI jobspec containers',
    'long_description': '# vai-jobspec-tools\n\nUtilities for VoxelAI jobspec containers\n\n[![PyPI Version](https://img.shields.io/pypi/v/vai-jobspec-tools.svg)](https://pypi.org/project/vai-jobspec-tools/)\n[![codecov](https://codecov.io/gh/voxelai/vai-jobspec-tools/branch/main/graph/badge.svg?token=ZX37CSBE50)](https://codecov.io/gh/voxelai/vai-jobspec-tools)\n[![Tests](https://github.com/voxelai/vai-jobspec-tools/workflows/Tests/badge.svg)](https://github.com/voxelai/vai-jobspec-tools/actions/workflows/test.yaml)\n[![Code Style](https://github.com/voxelai/vai-jobspec-tools/workflows/Code%20Style/badge.svg)](https://github.com/voxelai/vai-jobspec-tools/actions/workflows/lint.yaml)\n[![Type Check](https://github.com/voxelai/vai-jobspec-tools/workflows/Type%20Check/badge.svg)](https://github.com/voxelai/vai-jobspec-tools/actions/workflows/type-check.yaml)\n\n## Installation\n\n```bash\npip install vai-jobspec-tools\n```\n\n## API\n\n```python\nfrom __future__ import annotations\n\nimport contextlib\nimport logging\nfrom pathlib import Path\nfrom typing import Iterator\n\n\ndef configure_logger(\n    logger: logging.Logger,\n    *,\n    verbosity: int = 0,\n    level: int | None = None,\n):\n    """Configure a logger with a level and custom stream handler."""\n    ...\n\n\n@contextlib.contextmanager\ndef optional_temporary_directory(workdir: str | Path | None = None) -> Iterator[Path]:\n    """Create a temporary directory if one is not provided."""\n    ...\n\n\ndef prepare_dst_uri(\n    uri: str,\n    subject_id: str,\n    session_id: str,\n    pipeline_name: str,\n    pipeline_version: str,\n    *,\n    create: bool = True,\n) -> str:\n    """Generate a URI scoped to a particular subject, session, pipeline, and version."""\n    ...\n\n\ndef lowercase_alnum(s: str) -> str:\n    """Transform a string so that it contains only lowercase alphanumeric characters."""\n    ...\n\n```\n',
    'author': 'Andrew Ross',
    'author_email': 'andrew.ross.mail@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/voxelai/vai-jobspec-tools',
    'package_dir': package_dir,
    'py_modules': modules,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
