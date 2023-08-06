# pymlutil
Python Machine Learning utilities:

## functions

## imutial

## jsonutil

## metrics

## s3

## torch_util

## version

## workflow


[Packaging Python Projects](https://www.freecodecamp.org/news/build-your-first-python-package/)
[How to Publish an Open-Source Python Package to PyPI](https://realpython.com/pypi-publish-python-package/)

- Install twine:
    ```cmd
    pip3 install twine
    ```

- Build whl:
    ```cmd
    py setup.py sdist bdist_wheel
    ```

- Upload package to pipy
    ```cmd
    twine upload dist/*
    ```

[pymlutil](https://pypi.org/project/pymlutil)

- Load package into project
    ```cmd
    pip3 install --upgrade pymlutil
    ```

- Include pymlutil into project
```cmd
from pymlutil import *
```

## Notes
