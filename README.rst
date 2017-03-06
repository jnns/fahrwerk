=======================================
Online ordering form for city logistics
=======================================

A web app that provides a clean and intuitive online form for ordering a bike
messenger delivery. See it in action at Fahrwerk_, Berlin's only bike courier
collective.

This app has *white-labeling* capabilites. If you want to use this for your
business you can either host this yourself or `get in touch with us`_ and
we'll figure something out.

.. _Fahrwerk: http://bestellen.fahrwerk-berlin.de
.. _get in touch with us: mailto:info@fahrwerk-berlin.de


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

Collect all static files to the folder defined by ``STATIC_ROOT``. Serving
them is taken care of by WhiteNoise as well.

.. code-block:: sh

  $ ./manage.py collectstatic

Have a look at ``config/settings/production.py`` for environment variables
that need to be set in order to run the app. Your virtualenv's
``postactivate`` hook file is a good place to put them, for example.



Development
===========

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

Localization
------------

If you want to localize this app or if strings have changed, the translation
files need to be updated::

$ cd fwk/
$ ../manage.py makemessages --all
$ ../manage.py makemessages -d djangojs --ignore node_modules --extension js,jsx

Now open up PoEdit or another program to translate the generated files.
Afterwards compile them to ``*.mo`` files via::

$ ./manage.py compilemessages

Deployment
==========

If you're not deploying this app as an ordering form for Fahrwerk, you'll need
to overwrite a few settings here and there:

- add a settings file like ``config.settings.fahrwerk`` and overwrite all
  necessary directives
- adjust all settings under ``admin/constance/config/`` to your liking. Most
  importantly:

  - ``FWK_ORGANIZATION_NAME``
  - ``FWK_INFO_MAIL``
  - ``FWK_CONTRACT_URL``
  - ``FWK_PHONE_NO``

  Don't be confused by the ``FWK_`` prefix, it's a remainder from the pre-
  white-labeling days and will be gone soon.

- overwrite ``templates/_meta.html`` with the appropriate ``META``-tags for
  your organization
- additionally, you can overwrite the template directory in the settings file
  to include your own custom templates.


Issues
======

This is a list of features that I want to implement in the near future:

- implement quickstart with opencage.org geocoding
- check user submitted address for validity on form validation
- PayPal as a payment method
- automatically insert orders into eCourier (either via API or direct SQL).
- logging all admin and form actions using the Python logging framework.
- LDAP-authentication using `django-auth-ldap` for the admin backend.


License
=======

This project is licensed under the GNU General Public License v3.0. For more
information see ``LICENSE``. You're free to use and modify this code as long
as you provide the source code for your changes in return. However, please get
in touch with us if you use this for your business. We'd like to get to know
you :-)