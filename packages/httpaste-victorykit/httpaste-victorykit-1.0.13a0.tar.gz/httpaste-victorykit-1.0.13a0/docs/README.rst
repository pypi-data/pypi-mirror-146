httpaste - versatile HTTP pastebin
==================================

.. only:: readme

    ![](docs/_assets/images/favpng_parrot-royalty-free-cartoon.png)

.. only:: not readme

    .. image:: _assets/images/favpng_parrot-royalty-free-cartoon.png

.. note::
    httpaste is publicly hosted at `httpaste.it`_ and as a hidden Tor service (`<https://paste77ubkwxy4fqezffsmthxdh3xerwi72tlsw2mch7ecjhw2xn7iyd.onion>`_). 
    Both services are to be considered evaluatory, as long as the source code 
    is in pre-release. Regarding voidance of pre-release status, see `Open Issues`_, for more information.

This program offers an HTTP interface for storing public and private data
(a.k.a. pastes), commonly referred to as a pastebin application. It is inspired by `sprunge.us`_ and `ix.io`_. It can be hosted through WSGI, CGI, Fast 
CGI, or as a standalone evaluation server. It offers multiple storage backends, 
such as a filesystem backend, SQLite backend, or MySQL backend.

Public data can be accessed through an URL, where as private pastes 
additionally require HTTP basic authentication. Creation of authentication 
credentials happens on the fly, there is no sign-up process. Public pastes can 
only be accessed by knowing their paste ids, they are not listed on any index, 
since it isn't technically possible (by design).

All pastes are symetrically encrypted server-side with an HMAC derived key and 
SHA-256 hashing, a server-side salt and a randomly generated password. Public 
paste's passwords are derived from their ids. Private paste's passwords are 
randomly generated and stored inside a symetrically encrypted personal 
database, with the encryption key also being derived through the same HMAC 
mechanism, where the HTTP basic authentication credentials act as the master 
password.

Paste ids, usernames, and any other identifiable attributes are only stored
inside storage backends as keyed and salted BLAKE2 hashes.

The program supports output formatting for syntax highlighting (powered by 
`pygments`_), as well as MIME type output manipulation, and input encoding. 
The program can therefore serve as a minimalist, anonymous object storage for
small data.

Minute-based and 'burn-after-read' paste expiration are also supported.

.. include:: guide/getting-started.rst

Documentation
-------------

The documentation can be found under `<https://victorykit.bitbucket.io/httpaste/>`_.


Licensing
---------

Copyright (C) 2021  Tiara Rodney (victoryk.it)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.

This program uses licensed third-party software.


.. toctree::
    :maxdepth: 1
    :caption: More Information

    ARCHITECTURE
    CONTRIBUTING

.. _ix.io: http://ix.io/
.. _sprunge.us: http://sprunge.us
.. _pygments: https://pygments.org/
.. _icon: https://favpng.com/png_view/parrot-parrot-royalty-free-cartoon-png/gps7HM42

.. _Open Issues: https://victorykit.atlassian.net/issues/?jql=project%20%3D%20HTTPASTE%20AND%20fixVersion%20in%20(1.1.0-beta%2C%201.2.0-beta%2C%201.3.0)

.. _httpaste.it: http://httpaste.it