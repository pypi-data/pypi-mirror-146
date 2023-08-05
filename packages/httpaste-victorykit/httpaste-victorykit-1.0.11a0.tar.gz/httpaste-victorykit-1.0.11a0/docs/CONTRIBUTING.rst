Contribution Guidelines
=======================

TODO

Prerequisites
-------------

You need the following tools to be installed:

* Python (> ver. 3.7)
* Python *pip* module

.. code-block:: shell

    $ git clone git@bitbucket.org:victorykit/httpaste.git
    $ cd httpaste
    $ python3 -m pipenv install -d
    $ python3 -m pipenv run tox -e test
    $ python3 -m pipenv run tox -e build
    $ python3 -m pipenv run tox -e docs
    $ python3 -m pipenv run tox -e lint
    $ python3 -m pipenv run tox -e format
