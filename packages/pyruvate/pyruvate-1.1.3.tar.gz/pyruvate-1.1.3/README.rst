Pyruvate WSGI server
====================

.. image:: https://gitlab.com/tschorr/pyruvate/badges/master/pipeline.svg
   :target: https://gitlab.com/tschorr/pyruvate

.. image:: https://codecov.io/gl/tschorr/pyruvate/branch/master/graph/badge.svg
   :target: https://codecov.io/gl/tschorr/pyruvate

.. image:: http://img.shields.io/pypi/v/pyruvate.svg
   :target: https://pypi.org/project/pyruvate

Pyruvate is a reasonably fast, multithreaded, non-blocking `WSGI <https://www.python.org/dev/peps/pep-3333>`_ server implemented in `Rust <https://www.rust-lang.org/>`_.

Features
--------

* Non-blocking read/write using `mio <https://github.com/tokio-rs/mio>`_
* Request parsing using `httparse <https://github.com/seanmonstar/httparse>`_
* `rust-cpython <https://github.com/dgrunwald/rust-cpython>`_ based Python interface
* Worker pool based on `threadpool <https://github.com/rust-threadpool/rust-threadpool>`_
* `PasteDeploy <https://pastedeploy.readthedocs.io/en/latest/>`_ entry point

Installation
------------

If you are on Linux and use a recent Python version,

.. code-block::

    $ pip install pyruvate

is probably all you need to do.

Manylinux2010 binary wheels
+++++++++++++++++++++++++++

Manylinux2010 wheels are available for active Python 3 versions (currently 3.6-3.10).
Pip supports manylinux2010 wheels since version `19.0 <https://pip.pypa.io/en/stable/news/#id443>`_.
Setuptools (used by e.g. `zc.buildout <https://pypi.org/project/zc.buildout/>`_) supports manylinux2010 wheels since version `42.0.0 <https://setuptools.readthedocs.io/en/latest/history.html#id216>`_.
So if you are on Linux and the Pyruvate source distribution is preferred over the binary package try upgrading pip and/or setuptools first.

Source installation
+++++++++++++++++++

On macOS or if for any other reason you want to install the source tarball (e.g. using `pip install --no-binary`) you will need to `install Rust <https://doc.rust-lang.org/book/ch01-01-installation.html>`_ first.

Development Installation
++++++++++++++++++++++++

* Install `Rust <https://doc.rust-lang.org/book/ch01-01-installation.html>`__
* Install and activate a Python 3 (>= 3.6) `virtualenv <https://docs.python.org/3/tutorial/venv.html>`_
* Install `setuptools_rust <https://github.com/PyO3/setuptools-rust>`_ using pip::

    $ pip install setuptools_rust

* Install Pyruvate, e.g. using pip::

    $ pip install -e git+https://gitlab.com/tschorr/pyruvate.git#egg=pyruvate[test]

Using Pyruvate in your WSGI application
---------------------------------------

From Python
+++++++++++

A hello world WSGI application using Pyruvate listening on 127.0.0.1:7878 and using 2 worker threads looks like this:

.. code-block:: python

    import pyruvate

    def application(environ, start_response):
        """Simplest possible application object"""
        status = '200 OK'
        response_headers = [('Content-type', 'text/plain')]
        start_response(status, response_headers, None)
        return [b"Hello world!\n"]

    pyruvate.serve(application, "127.0.0.1:7878", 2)

Using PasteDeploy
+++++++++++++++++

Again listening on 127.0.0.1:7878 and using 2 worker threads::

    [server:main]
    use = egg:pyruvate#main
    socket = 127.0.0.1:7878
    workers = 2

Configuration Options
+++++++++++++++++++++

socket
    Required: The TCP socket Pyruvate should bind to.
    `Pyruvate` also supports `systemd socket activation <https://www.freedesktop.org/software/systemd/man/systemd.socket.html>`_
    If you specify `None` as the socket value, `Pyruvate` will try to acquire a socket bound by `systemd`.

workers
    Required: Number of worker threads to use.

write_blocking
    Optional: Use a blocking connection for writing.
    Pyruvate currently supports two types of workers:
    The default worker will write in a non-blocking manner, registering WSGI responses for later processing if the socket isn't available for writing immediately.
    By setting this option to `True` you can enable a worker that will instead set the connection into blocking mode for writing.
    Defaults to `False`.

max_number_headers
    Optional: Maximum number of request headers that will be parsed.
    If a request contains more headers than configured, request processing will stop with an error indicating an incomplete request.
    The default is 32 headers

async_logging
    Optional: Log asynchronously using a dedicated thread.
    Defaults to `True`.

max_reuse_count
    Optional: Specify how often to reuse an existing connection.
    Setting this parameter to 0 will effectively disable keep-alive connections.
    This is the default.

keepalive_timeout
    Optional: Specify a timeout in integer seconds for keepalive connection.
    The persistent connection will be closed after the timeout expires.
    Defaults to 60 seconds.

chunked_transfer
    Optional: Whether to use chunked transfer encoding if no Content-Length header is present.
    Defaults to `False`.

Logging
+++++++

Pyruvate uses the standard `Python logging facility <https://docs.python.org/3/library/logging.html>`_.
The logger name is `pyruvate`.
See the Python documentation (`logging <https://docs.python.org/3/library/logging.html>`_, `logging.config <https://docs.python.org/3/library/logging.config.html>`_) for configuration options.

Example Configurations
----------------------

Django
++++++

After installing Pyruvate in your Django virtualenv, create or modify your `wsgi.py` file (one worker listening on 127.0.0.1:8000):

.. code-block:: python

    import os
    import pyruvate

    from django.core.wsgi import get_wsgi_application

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "your_django_application.settings")

    application = get_wsgi_application()

    pyruvate.serve(application, "127.0.0.1:8000", 1)

You can now start Django + Pyruvate with::

    $ python wsgi.py

Override settings by using the `DJANGO_SETTINGS_MODULE` environment variable when appropriate.
Tested with `Django 3.2.x, 2.2.x <https://www.djangoproject.com/>`_.

MapProxy
++++++++

First create a basic WSGI configuration following the `MapProxy deployment documentation <https://mapproxy.org/docs/latest/deployment.html#server-script>`_.
Then modify `config.py` so it is using Pyruvate (2 workers listening on 127.0.0.1:8005):

.. code-block:: python

    import os.path
    import pyruvate

    from mapproxy.wsgiapp import make_wsgi_app
    application = make_wsgi_app(r'/path/to/mapproxy/mapproxy.yaml')

    pyruvate.serve(application, "127.0.0.1:8005", 2)

Start from your virtualenv::

    $ python config.py

Tested with `Mapproxy 1.13.x, 1.12.x <https://mapproxy.org/>`_.

Plone
+++++

Using `zc.buildout <https://pypi.org/project/zc.buildout/>`_ and `plone.recipe.zope2instance <https://pypi.org/project/plone.recipe.zope2instance>`_ you can define an instance part using Pyruvate's `PasteDeploy <https://pastedeploy.readthedocs.io/en/latest/>` _entry point::

    [instance]
    recipe = plone.recipe.zope2instance
    http-address = 127.0.0.1:8080
    eggs =
        Plone
        pyruvate
    wsgi-ini-template = ${buildout:directory}/templates/pyruvate.ini.in

The `server` section of the template provided with the `wsgi-ini-template <https://pypi.org/project/plone.recipe.zope2instance/#advanced-options>`_ option should look like this (3 workers listening on `http-address` as specified in the buildout `[instance]` part)::

    [server:main]
    use = egg:pyruvate#main
    socket = %(http_address)s
    workers = 3

There is a minimal buildout example configuration for Plone 5.2 in the `examples directory <https://gitlab.com/tschorr/pyruvate/-/tree/master/examples/plone52>`_ of the package.

Tested with `Plone 5.2.x <https://plone.org/>`_.

Pyramid
+++++++

Install Pyruvate in your Pyramid virtualenv using pip::

    $ pip install pyruvate

Modify the server section in your `.ini` file to use Pyruvate's `PasteDeploy <https://pastedeploy.readthedocs.io/en/latest/>` _entry point (listening on 127.0.0.1:7878 and using 5 workers)::

    [server:main]
    use = egg:pyruvate#main
    socket = 127.0.0.1:7878
    workers = 5

Start your application as usual using `pserve`::

    $ pserve path/to/your/configfile.ini

Tested with `Pyramid 2.0, 1.10.x <https://trypyramid.com/>`_.

Radicale
++++++++

You can find an example configuration for `Radicale <https://radicale.org>`_ in the `examples directory <https://gitlab.com/tschorr/pyruvate/-/tree/master/examples/plone52>`_ of the package.
Tested with `Radicale 3.0 <https://radicale.org>`_.

Nginx settings
++++++++++++++

Like other WSGI servers Pyruvate should be used behind a reverse proxy, e.g. Nginx::

    ....
    location / {
        proxy_pass http://localhost:7878;
        ...
    }
    ...

Nginx doesn't use keepalive connections by default so you will need to `modify your configuration <https://nginx.org/en/docs/http/ngx_http_upstream_module.html#keepalive>`_ if you want persistent connections.
