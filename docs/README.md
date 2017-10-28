# Titan Rover 2018 Docs

[![Docs](https://media.readthedocs.org/static/projects/badges/passing.svg)](https://titanrover2018.readthedocs.io/en/latest/)

Online readthedocs: https://titanrover2018.readthedocs.io/en/latest/

This year's documentation will be generated using [Sphinx](http://www.sphinx-doc.org/en/stable/). 
Sphinx uses [reStructuredText](http://www.sphinx-doc.org/en/stable/rest.html) as its markup language, and many of its strengths come from the power and straightforwardness of reStructuredText and its parsing and translating suite, the Docutils. Sphinx supports parsing python files and auto generating documents based of docstrings. 

## sphinx-autobuild

[sphinx-autobuild](https://pypi.python.org/pypi/sphinx-autobuild) is an addon tool that watches a Sphinx directory and rebuilds the documentation when a change is detected. It also includes a livereload enabled web server.

### Start sphinx-autobuild

Assuming you are in the `docs/` folder...

- Start command: `sphinx-autobuild -b html ./source ./build`

This starts sphinx-autobuild to watch the `source` folder and rebuild any changes into the `build` folder.

- sphinx-autobuild will serve a live version of the docs at: `localhost:8000` (default port)

## Manually build the docs

If you need to build the docs directly you can use the make file provided in the folder directory.

On Linux: `make html`

On Windows: `.\make.bat html`

## readthedocs

We are using [readthedocs](https://readthedocs.org/) to automatically build and host our docs whenever someone pushes to our GitHub repo.
This ensures our docs are always up to date. 