# log-indented

[![Python application](https://github.com/markmark206/log-indented/actions/workflows/python-test.yml/badge.svg)](https://github.com/markmark206/log-indented/actions/workflows/python-test.yml)

This is a package for producing indented, easy to understand logs.

Example:

Executing compute_the_answer()

```python
from log_indented import logged, log_info

@logged
def compute_the_answer() -> int:
    for i in range(10):
        time.sleep(0.2)
        log_info(f"{i}, computing the answer")
    return 42
```

will produce output similar to this:

```
    + compute_the_answer: enter
      compute_the_answer: 0, computing the answer
      compute_the_answer: 1, computing the answer
      ...
      compute_the_answer: 9, computing the answer
    - compute_the_answer: exit. took 2,558.9 ms.
```
