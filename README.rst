=====================
fwk - online ordering
=====================

This web app makes it possible to order deliveries online via a neat and
simple form.

See it in action at Fahrwerk_, Berlin's only bike courier collective.

.. _Fahrwerk: http://fahrwerk-berlin.de


Installation
============

Run the following commands to create a virtualenv for this project and pull in
all required packages that this project depends on.

.. code-block:: sh

  $ mkvirtualenv fwk
  $ pip install -r requirements.pip

WhiteNoise can make use of the brotli compression mechanism. Installing with
``pip`` will fail unless the following libraries are available.

.. code-block:: sh

  $ apt install build-essential python-dev libffi-dev

Install the required node.js packages (defined in ``package.json``):

.. code-block:: sh

  $ npm install

Collect all static files to the folder defined by ``STATIC_ROOT``. Serving is
taken care of by WhiteNoise as well.

.. code-block:: sh

  $ ./manage.py collectstatic

Have a look at ``config/settings/production.py`` for environment variables
that need to be set in order to run the app. Your virtualenv's
``postactivate`` hook file is a good place to put them, for example.



Development
-----------

Install ``npm`` via the nodesource.com repositories and run ``npm install`` in
the project directory. All needed modules are pulled in automatically to
``./node_modules`` because they're defined in ``package.json``.

`django-pipeline` bundles all necessary files together from the app
directories and ``./node_modules``.

Depending on how this project develops I might dive into `webpack` and
integrate that into the stack.


Testing
-------

The tests can be run via::

  $ ./manage.py test fwk


Issues
======

This is a list of features that I want to implement in the near future:

- send confirmation e-mail to customers upon successful order
- implement quickstart with opencage.org geocoding
- check user submitted address for validity on form validation
- PayPal as a payment method
- automatically insert orders into eCourier (either via API or direct SQL).
- logging all admin and form actions using the Python logging framework.
- LDAP-authentication using `django-auth-ldap`.
- ReactJS or Angular.JS frontend.


License
=======

This project is licensed under the GNU General Public License v3.0. For more
information see ``LICENSE``. You're free to use and modify this code as long as
you provide the source code for your changes in return.