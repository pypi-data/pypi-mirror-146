# Handyman

Common utility framework for ML Services

## Install

1. To install the handyman library, please use the following command in case of [_pip_](https://pip.pypa.io/en/stable/):

```
    pip install handyman
```

* Or add handyman as a poetry dependency.

```
    handyman = 0.1.3
```

## Usage

The handyman library currently consists of the following packages:

* `exceptions`
* `google_sheets`
* `io`
* `json_utils`
* `log`
* `prometheus`
* `sentry`


To use any of the packages stated above, please use:

    from handyman import <package name>

## Publish

Create a distribution package:

    python setup.py sdist

Publish to PyPi:


    pip install twine

    twine upload dist/*

You will be prompted to enter username and password, if you don't have credentials contact `@devops`.