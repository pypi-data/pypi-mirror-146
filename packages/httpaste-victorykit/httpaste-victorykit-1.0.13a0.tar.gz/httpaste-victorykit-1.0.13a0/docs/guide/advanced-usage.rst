Advanced Usage
==============

Binary Data
-----------

httpaste supports encoding. Encode your data as Base64, Base85, Base32, or 
Base16 and provide an encoding specifier.

.. code-block:: shell

    $ cat my.pdf | base64 | curl "http://localhost:8080/paste/public?encoding=base64"
    http://localhost:8080/paste/public/5Rt3E3n6

When getting pastes, you may provide a MIME type, if a client deduces the encoding by looking at the HTTP 'Content-Type' header.

.. code-block:: shell

     $ curl "https://p.victoryk.it/paste/public/5Rt3E3n6?mime=application/pdf"

Custom Expiration
-----------------

Set a paste's lifetime to make it expire after a specified amount of time. The 
lifetime must be provided in minutes and cannot be less than 1. A lifetime of
0 will evaluate to a lifetime 1.

.. code-block:: shell

    $ echo "My paste expires after reading" | curl "http://localhost:8080/paste/public?lifetime=360" -F "data=<-"
    http://localhost:8080/paste/public/5Rt3E3n6

Burn-After-Read Expiration
--------------------------

Set a paste's lifetime to <0 to make it expire right after reading

.. code-block:: shell

    $ echo "My paste expires after reading" | curl "http://localhost:8080/paste/public?lifetime=-1" -F "data=<-"
    http://localhost:8080/paste/public/5Rt3E3n6

.. code-block:: shell

    $ curl http://localhost:8080/paste/public/5Rt3E3n6
    My paste expires after reading
    $ curl http://localhost:8080/paste/public/5Rt3E3n6
    {"detail":"Paste expired","status":410,"title":"Gone"}

Syntax Higlighting
------------------

You can apply syntax highlighting to a multitude of formats. Consult the pygments documentation for valid specifiers.

.. code-block:: shell

    $ curl "http://localhost:8080/paste/public/5Rt3E3n6?syntax=terraform"

Highlighting, by default, will be formatted for 256 color terminals. You can also change the formatting.

.. code-block:: shell

    $ curl "http://localhost:8080/paste/public/5Rt3E3n6?syntax=terraform&format=html"

You can also add line numbers to the output.

.. code-block:: shell

    $ curl "http://localhost:8080/paste/public/5Rt3E3n6?syntax=terraform&format=html&linenos=true"