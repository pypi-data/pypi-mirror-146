httpaste - versatile HTTP pastebin
==================================

.. only:: readme

    ![](docs/_assets/images/favpng_parrot-royalty-free-cartoon.png)

.. only:: not readme

    .. image:: _assets/images/favpng_parrot-royalty-free-cartoon.png

httpaste is a pastebin application for easily pasting and retrieving data over 
HTTP from shell environments and web browsers. It is inspired by `sprunge.us`_ 
and `ix.io`_, but focuses on extendability, advanced security, with little to 
no trade-off to simplicity. It can be hosted through WSGI, CGI, Fast CGI, or 
as a standalone evaluation server. It offers multiple storage backends, such as 
a filesystem backend, SQLite backend, MySQL backend, or MongoDB backend.

All pastes are being encrypted on the fly and can only be retrieved by an 
authorized user, either through knowing the paste id of a public paste, or 
having authentication credentials, as well as the paste id of a private paste. 
This makes httpaste ideal as a pastebin for sensitive environments such as the 
Tor network. Authentication credentials are created on-the-fly and don't  require a sign-up process.

httpaste supports output formatting for syntax highlighting (powered by 
`pygments`_), as well as MIME type output manipulation, and input encoding. 
Therefore httpaste can server as an anonymous object storage for small data.

Minute-based and 'burn-after-read' paste expiration are supported.

httpaste focuses on security through cryptography, making it a computationally intensive application.

.. include:: guide/get-started.rst

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