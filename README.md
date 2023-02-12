# anymail-history - Email History (database storage) for [Django Anymail](https://anymail.dev/)

[![CI tests](https://github.com/pfouque/django-anymail-history/actions/workflows/test.yml/badge.svg)](https://github.com/pfouque/django-anymail-history/actions/workflows/test.yml)
[![codecov](https://codecov.io/github/pfouque/django-anymail-history/branch/master/graph/badge.svg?token=GWGDR6AR6D)](https://codecov.io/github/pfouque/django-anymail-history)
[![Documentation](https://img.shields.io/static/v1?label=Docs&message=READ&color=informational&style=plastic)](https://github.com/pfouque/django-anymail-history#settings)
[![MIT License](https://img.shields.io/static/v1?label=License&message=MIT&color=informational&style=plastic)](https://github.com/pfouque/anymail-history/LICENSE)

Keep history of all emails sent by [Django Anymail](https://anymail.dev/)

## Introduction

anymail-history implements database storage for Django Anymail.

## Resources

-   Package on PyPI: [https://pypi.org/project/anymail-history/](https://pypi.org/project/anymail-history/)
-   Project on Github: [https://github.com/pfouque/django-anymail-history](https://github.com/pfouque/django-anymail-history)

## Features

-   Store sent emails
-   Store tracking events
-   Display Admin
-   html templating ?


## Requirements

-   Django >=3.2
-   Python >=3.8

## How to

1. [Install Anymail](https://anymail.dev/en/stable/quickstart/)

2. Install
    ```
    $ pip install "django-anymail-history"
    ```

3. Register anymail_history in your list of Django applications:
    ```
    INSTALLED_APPS = [
        # ...
        "anymail",
        "anymail_history",
        # ...
    ]
    ```
4. Then migrate the app to create the database table
    ```manage.py migrate```

5. 🎉 Voila!

## Settings

You can add settings to your project’s settings.py either as a single `ANYMAIL` dict, or by breaking out individual settings prefixed with ANYMAIL_. So this settings dict:

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

## Contribute

### Principles

-   Simple for developers to get up-and-running
-   Consistent style (`black`, `ruff`)
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
-   `Ruff`, `black` and `pyupgrade` linting
-   `mypy` for type checking
-   `Github Actions` for builds and CI

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

#### CI

- `.github/workflows/lint.yml`: defines and ensure coding rules on Github.

- `.github/workflows/test.yml`: Runs tests on all compatible combinations of Django (3.2+) & Anymail(8.4+), Python (3.8+)in a Github matrix.

- `.github/workflows/coverage.yml`: Calculates the coverage on an up to date version.
