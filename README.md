# Simple todo command-line application

The application is written in Python and requires Python 3.6 or higher to run.
It has no dependencies outside the standard library.

The application can be run with `python todo_app.py`.

## Running the tests

Tests can be run using [pytest](https://pytest.org/) or simply running `python todo_app_test.py` and `python task_test.py`.

If you use [pipenv](https://pipenv.readthedocs.io/en/latest/) for handling virtual environments you can install pytest inside the virtual environment using `pipenv install --dev`. Pytest can then be run inside a virtualenv-shell using `pipenv shell` and then `pytest --spec` (`--spec` option for nicer output), or directly using `pipenv run pytest --spec`.

### Miscellaneous

The commands are case-insensitive so `Do 1` is equivalent to `do 1`.
