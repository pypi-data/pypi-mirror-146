Getting Started
===============

Install
"""""""

.. code-block:: shell

    $ python3 -m pip install httpaste-victorykit
    $ httpaste --help

.. note::
    httpaste is publicly available at `https://httpaste.it`_, and can be accessed
    over the TOR network via `https://pastefao6mwyafs3cznoe2u2a6iizw5laulrznla3dytcnvaizte73yd.onion`_ aswell. Both are hosted on different servers of different service providers.

Create Configuration
""""""""""""""""""""

.. code-block:: shell

    $ httpaste default-config --dump myconfig.ini

.. note::
    The default configuration creates an in-memory SQLite backend, which is not 
    suitable for WWW deployments. Visit `backend`, for more 
    information on configuring the backend.


Run a Local Evaluation Server
"""""""""""""""""""""""""""""

.. code-block:: shell

    $ httpaste standalone --config myconfig.ini --port 8080


Publish a Private Paste
"""""""""""""""""""""""

.. code-block:: shell

    $ echo 'My first private paste' | curl -F 'data=<-' -u myusername:mypassword http://localhost:8080/paste/private
    http://localhost:8080/paste/private/UALUA9

.. note::
    If the user does not exist, they will be created upon authentication.


Retrieve a Private Paste
""""""""""""""""""""""""

.. code-block:: shell

    $ curl -u myusername:mypassword http://localhost:8080/paste/private/UALUA9
    My first private paste


Publish a Public Paste
""""""""""""""""""""""

.. code-block:: shell

    $ echo 'My first public paste' | curl -F 'data=<-' http://localhost:8080/paste/public
    http://localhost:8080/paste/public/X4L39J


Retrieve a Public Paste
""""""""""""""""""""""""

.. code-block:: shell

    $ curl http://localhost:8080/paste/public/X4L39J
    My first public paste