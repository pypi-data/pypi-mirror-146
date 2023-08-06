# DependencyConfusion

## Description

This package implements a test for Dependency Confusion using pip.

1. The version `0.0.2` is available on *test.pypi.org*.
2. The version `0.0.2` and `666` are available on *pypi.org*.
3. In the scenario you want to install version `0.0.2` available on *test.pypi.org* and you use the **pip** `--extra-index-url` option to install it.
4. During installation, a window will open to tell you which version is being installed... theoretically version `666` available on *pypi.org* will be installed if your pip version is vulnerable to dependency confusion.

## Requirements

This package require:

 - python3
 - python3 Standard Library

## Installation

```bash
pip install --extra-index-url https://test.pypi.org/simple/ DependencyConfusion
```

## Links

 - [Github Page](https://github.com/mauricelambert/DependencyConfusion/)
 - [Pypi package](https://pypi.org/project/DependencyConfusion/)
 - [Test pypi package](https://test.pypi.org/project/DependencyConfusion/)

## Licence

Licensed under the [GPL, version 3](https://www.gnu.org/licenses/).
