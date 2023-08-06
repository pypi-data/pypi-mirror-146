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
