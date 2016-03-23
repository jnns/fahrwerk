======================================================
Online ordering system for Fahrwerk courier collective
======================================================

This is a web app which makes it possible to order deliveries with Berlin's
only bike courier collective, Fahrwerk_, via the internet.
No need to call – but we're happy if you do!

.. _Fahrwerk: http://fahrwerk-berlin.de


Installation
============

Run the following commands to create a virtualenv for this project and pull in
all required packages that this project depends on.

.. code-block:: sh

  $ mkvirtualenv fahrwerk
  $ pip install -r requirements.pip

WhiteNoise can make use of the brotli compression mechanism. Installing with
``pip`` will fail unless the following libraries are available.

.. code-block:: sh

  $ apt install build-essential python-dev libffi-dev


Issues
======

This is a list of features that I want to implement in the near future:

- automatically insert orders into eCourier (either via API or direct SQL).
- logging all admin and form actions using the Python logging framework.
- LDAP-authentication using `django-auth-ldap`.
- ReactJS or Angular.JS frontend.


License
=======

This project is licensed under the GNU General Public License v3.0. For more
information see ``LICENSE``. You're free to use and modify this code as long as
you provide the source code for your changes in return.