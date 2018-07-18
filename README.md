# Code metrics

## Quickstart

To use the code metrics as a package use the setup script with

    python setup.py install

A basic example can be ran with

    python -m metrics <path_to_your_code>


Developement
=============

For a manual installation, requirements can be installed with ::

    pip install -r requirements.txt

Documentation can be generated with ::

    cd doc; make html; cd ..

The html doc is in ``doc/_build/html``

A code coverage report can be obtained::

    coverage run --source metrics -m tests
    coverage html

You are warmly encouraged to run the metrics package on itself, of course !

