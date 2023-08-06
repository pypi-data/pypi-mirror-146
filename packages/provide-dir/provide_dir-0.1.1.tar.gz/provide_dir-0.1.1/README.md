# provide_directory

Function to create the given path, including potential parent directories. Writes to the provided sink (e.g. `print`) whether the directory was created or whether it already existed.

## Dependencies

None

## Usage

```python
from pathlib import Path
from provide_dir import provide_dir

needed_path = Path("/path/to/directory/with/subdirectories")
provide_dir(needed_path, print)
```

## Installation

### Pip

```
pip install provide_dir
```

### Developer's Installation

You can clone the repository and install it with `pip install -e /path/to/local/repository`.

## Test dependencies

To run the tests you will need

* [pytest][pytest]
* [remove_directory][remove_directory]
* [re_patterns][re_patterns]

[pytest]: https://pypi.org/project/pytest/
[remove_directory]: https://pypi.org/project/remove-directory/
[re_patterns]: https://pypi.org/project/re-patterns/
