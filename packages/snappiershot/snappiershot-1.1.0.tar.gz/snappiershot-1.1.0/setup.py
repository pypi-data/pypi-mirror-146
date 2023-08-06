# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['snappiershot',
 'snappiershot.plugins',
 'snappiershot.serializers',
 'snappiershot.snapshot']

package_data = \
{'': ['*']}

install_requires = \
['pint>=0.14,<0.15',
 'pprint_ordered_sets>=1.0.0,<2.0.0',
 'tomlkit>=0.7.0,<0.8.0']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>1.5.1'],
 'pandas': ['pandas>=0.20.0']}

entry_points = \
{'pytest11': ['snappiershot = snappiershot.plugins.pytest']}

setup_kwargs = {
    'name': 'snappiershot',
    'version': '1.1.0',
    'description': 'Snapshot testing library.',
    'long_description': '# SnappierShot\nAdd snapshot testing to your testing toolkit.\n\n## Installation\n```bash\n$ pip install snappiershot\n```\n\n## Configuration\nSnappierShot is following the [trend of packages](https://github.com/carlosperate/awesome-pyproject/)\nin performing project-wide configuration through the `pyproject.toml` file established by\n[PEP 518](https://www.python.org/dev/peps/pep-0518/).\n\nWithin the `pyproject.toml` file, all SnappierShot configuration can be found under the\n`[tool.snappiershot]` heading. While the `[tool.snappiershot]` heading is optional, the\n`[tool.poetry.plugins.pytest11]` heading must also be included.\n\n### Example (with default values):\n```toml\n[tool.poetry.plugins.pytest11]\nsnappiershot = "snappiershot.plugins.pytest"\n\n[tool.snappiershot]\nfile_format = "json"\nfloat_absolute_tolerance = 1e-6\nfloat_relative_tolerance = 0.001\nfull_diff = false\njson_indentation = 4\n```\n\nCurrently, the only allowed file format is JSON.\n\n## Usage\n\nSnappierShot allows you to take a "snapshot" of data the first time that a test\n  is run, and stores it nearby in a `.snapshots` directory as a JSON. Then, for all\n  subsequent times that test is run, the data is asserted to "match" the original\n  data.\n\nSnappierShot uses metadata to find tests stored in each snapshot file. Metadata is\n  defined as the inputs to a test method.\n* If the metadata is not found, a new file is Written.\n* If the metadata is found, the contents of the snapshot are checked and can either Pass or Fail.\n* If a snapshot file is found but the test isn\'t run, then the test is marked as Unchecked\n\n### Best Practices\n* Do not run `assert_match` within a loop\n* Do not try to snapshot uninstantiated classes/objects or use them as inputs to a test method\n* If an unsupported object type cannot be recorded, see [CONTRIBUTING.md](CONTRIBUTING.md) for instructions on how\n  to contribute to the project\n  * `__snapshot__` is a workaround described below\n\n\n### Pytest Examples\n```python\nfrom snappiershot import Snapshot\n\ndef test_basic(snapshot: Snapshot):\n    """ Will do a basic snapshotting of one value with no metadata """\n    # Arrange\n    x = 1\n    y = 2\n\n    # Act\n    result = x + y\n\n    # Assert\n    snapshot.assert_match(result)\n\ndef test_ignore_metadata(snapshot: Snapshot, input_to_ignore: str = "ignore me"):\n    """ Test that metadata gets ignored """\n    # Arrange\n    x = 1\n    y = 2\n    ignored_input = ["input_to_ignore"]\n\n    # Act\n    result = x + y\n\n    # Assert\n    snapshot.assert_match(result, ignore=ignored_input)\n```\n\n### No Test Runner Example\n```python\nfrom snappiershot import Snapshot\n\ndef test_no_pytest_runner():\n    """ Run test without pytest runner """\n    # Arrange\n    x = 1\n    y = 2\n\n    # Act\n    result = x + y\n\n    # Assert\n    with Snapshot() as snapshot:\n        snapshot.assert_match(result)\n```\n\n### Custom Encoding and Override Examples\n`__snapshot__` overrides serializing behavior for class objects being recorded. Some of its potential use cases:\n  * Partially recording class objects with many unnecessary properties\n  * Skipping over encoding an object by returning a string\n\n```python\nfrom snappiershot import Snapshot\nfrom pytest import fixture\n\nclass TestClass1:\n  def __init__(self):\n    self.a = 1\n    self.b = 2\n\n  def __snapshot__(self) -> dict:\n    encoding = {\n      "a": self.a,\n      "b": self.b,\n    }\n    return encoding\n\nclass TestClass2:\n  def __init__(self):\n    self.a = 1\n    self.b = 2\n\n  def __snapshot__(self) -> str:\n    encoding = "ENCODING SKIPPED"\n    return encoding\n\n@fixture\ndef class_input1() -> TestClass1:\n  class_input1 = TestClass1()\n  return class_input1\n\n@fixture\ndef class_input2() -> TestClass2:\n  class_input2 = TestClass2()\n  return class_input2\n\ndef test_class1(class_input1: TestClass1, snapshot: Snapshot):\n    """ Test encoding snapshot and metadata for a custom class with a dictionary override"""\n\n    # Act\n    result = class_input1\n\n    # Assert\n    snapshot.assert_match(result)\n\ndef test_class2(class_input2: TestClass2, snapshot: Snapshot):\n    """ Test encoding snapshot and metadata for a custom class with a string override """\n\n    # Act\n    result = class_input2\n\n    # Assert\n    snapshot.assert_match(result)\n```\n\n\n### Raises\nSnappiershot also allows you to record errors that are raised during\n  the execution of a code block. This allows you to track how and when errors\n  are reported more easily.\n\n```python\ndef fallible_function():\n    """ A function with an error state. """\n    raise RuntimeError("An error occurred!")\n\n\ndef test_fallible_function(snapshot):\n    """ Test that errors are being reported as expected"""\n    # Arrange\n\n    # Act & Assert\n    with snapshot.raises(RuntimeError):\n        fallible_function()\n```\n\n### Support Types:\n  * Primitives (`bool`, `int`, `float`, `None`, `str`)\n  * Numerics (`complex`)\n  * Collections (`lists`, `tuples`, `sets`)\n  * Dictionaries\n  * Classes (with an underlying `__dict__`, `__slots__`, or `to_dict`)\n  * Unit types from the `pint` package\n  * Classes with custom encoding (by defining a `__snapshot__` method)\n\n## Contributing\nSee [CONTRIBUTING.md](CONTRIBUTING.md)\n',
    'author': 'Ben Bonenfant',
    'author_email': 'bonenfan5ben@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/MORSECorp/snappiershot',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
