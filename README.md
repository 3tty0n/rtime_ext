# RPython Time (`rlib/rtime`) Extension

This library aims to extend `rtime.py` in RPython's `rlib` library.

## Prerequisite

- PyPy source code

## Usage

Append `pypy` to `PYTHONPATH`.

```sh
export PYTHONPATH=/path/to/pypy
```

Import `rtime_ext` and use it.

```py
from rtime_ext import clock_monotonic

print clock_monotonic()
```
