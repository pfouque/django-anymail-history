# anymail-history - Email History for Django Anymail

[![CI tests](https://github.com/pfouque/django-anymail-history/actions/workflows/tox.yml/badge.svg)](https://github.com/pfouque/django-anymail-history/actions/workflows/tox.yml)
[![Documentation](https://img.shields.io/static/v1?label=Docs&message=READ&color=informational&style=plastic)](https://anymail-history.github.io/anymail-history/)
[![MIT License](https://img.shields.io/static/v1?label=License&message=MIT&color=informational&style=plastic)](https://github.com/pfouque/anymail-history/)

Keep history of all emails sent by Django Anymail

## Introduction

anymail-history implements models and signals for Django Anymail.

## Resources

-   Full documentation: SOON
-   Package on PyPI: SOON
-   Project on Github: [https://github.com/pfouque/django-anymail-history](https://github.com/pfouque/django-anymail-history)

## Features

-   Store sent emails
-   Store tracking events
-   Display Admin
-   html templating


## Requirements

-   Django >=3.2
-   Python >=3.7

## How to

1. Install
    ```
    $ pip install "django-anymail[mailgun]" "django-anymail-history"
    ```
2. [Configure Anymail](https://github.com/anymail/django-anymail/#anymail-1-2-3)
    ```
    INSTALLED_APPS = [
        # ...
        "anymail",
        "anymail_history",
        # ...
    ]
    ```
3. Enjoy!

## settings

You can add settings to your project’s settings.py either as a single ANYMAIL dict, or by breaking out individual settings prefixed with ANYMAIL_. So this settings dict:

```
ANYMAIL = {
    "STORE_HTML": True,
}
```
…is equivalent to these individual settings:

```
ANYMAIL_STORE_HTML = True
```

### Available settings

-   `ANYMAIL_STORE_FAILED_SEND`: (default: False) Store message even if esp didn't returned a message-id.
-   `ANYMAIL_STORE_HTML`: (default: False) Store html alternatives.
-   `ANYMAIL_RENDER_HTML`: (default: True) Generate html alternatives.

## Contribute

### Principles

-   Simple for developers to get up-and-running
-   Consistent style (`black`, `isort`, `flake8`)
-   Future-proof (`pyupgrade`)
-   Full type hinting (`mypy`)

### Coding style

We use [pre-commit](https://pre-commit.com/) to run code quality tools.
[Install pre-commit](https://pre-commit.com/#install) however you like (e.g.
`pip install pre-commit` with your system python) then set up pre-commit to run every time you
commit with:

```bash
> pre-commit install
```

You can then run all tools:

```bash
> pre-commit run --all-files
```

It includes the following:

-   `poetry` for dependency management
-   `isort`, `black`, `pyupgrade` and `flake8` linting
-   `mypy` for type checking
-   `tox` and Github Actions for builds and CI

There are default config files for the linting and mypy.

### Tests

#### Tests package

The package tests themselves are _outside_ of the main library code, in a package that is itself a
Django app (it contains `models`, `settings`, and any other artifacts required to run the tests
(e.g. `urls`).) Where appropriate, this test app may be runnable as a Django project - so that
developers can spin up the test app and see what admin screens look like, test migrations, etc.

#### Running tests

The tests themselves use `pytest` as the test runner. If you have installed the `poetry` evironment,
you can run them thus:

```
$ poetry run pytest
```

or

```
$ poetry shell
(anymail-history-py3.10) $ pytest
```

The full suite is controlled by `tox`, which contains a set of environments that will format, lint,
and test against all support Python + Django version combinations.

```
$ tox
...
______________________ summary __________________________
  fmt: commands succeeded
  lint: commands succeeded
  mypy: commands succeeded
  py37-django32: commands succeeded
  py37-django40: commands succeeded
  py37-djangomain: commands succeeded
  py38-django32: commands succeeded
  py38-django40: commands succeeded
  py38-djangomain: commands succeeded
  py39-django32: commands succeeded
  py39-django40: commands succeeded
  py39-djangomain: commands succeeded
```

#### CI

There is a `.github/workflows/tox.yml` file that can be used as a baseline to run all of the tests
on Github. This file runs the oldest LTS (3.2), newest (4.1), and head of the main Django branch.
