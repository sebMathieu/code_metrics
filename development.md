#Developement

For a manual installation, requirements can be installed with ::

    pip install -r requirements.txt

Documentation can be generated with ::

    cd doc; make html; cd ..

The html doc is in ``doc/_build/html``

A code coverage report can be obtained::

    coverage run --source metrics -m tests
    coverage html

You are warmly encouraged to run the metrics package on itself, of course !

