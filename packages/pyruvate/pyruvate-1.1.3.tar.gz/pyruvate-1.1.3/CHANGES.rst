Changelog
=========

1.1.3 (2022-04-11)
------------------

* Simplify response writing and improve performance (`#12 <https://gitlab.com/tschorr/pyruvate/-/issues/12>`_)
* Improve signal handling (`#13 <https://gitlab.com/tschorr/pyruvate/-/issues/13>`_)

1.1.2 (2022-01-10)
------------------

* Migrate to Rust 2021
* Use codecov binary uploader
* Add CONTRIBUTING.rst
* Fixed: The wrk benchmarking tool could make pyruvate hang when there is no Content-Length header (`#11 <https://gitlab.com/tschorr/pyruvate/-/issues/11>`_)

1.1.1 (2021-10-12)
------------------

* Support Python 3.10

1.1.0 (2021-09-14)
------------------

* Refactor FileWrapper and improve its performance
* Increase the default maximum number of headers
* Add `Radicale <https://radicale.org>`_ example configuration
* Update development status 

1.0.3 (2021-06-05)
------------------

* HEAD request: Do not complain about content length mismatch (`#4 <https://gitlab.com/tschorr/pyruvate/-/issues/4>`_) 
* More appropriate log level for client side connection termination (`#5 <https://gitlab.com/tschorr/pyruvate/-/issues/5>`_)
* Simplify request parsing

1.0.2 (2021-05-02)
------------------

* Close connection and log an error in the case where the actual content length is
  less than the Content-Length header provided by the application
* Fix readme

1.0.1 (2021-04-28)
------------------

* Fix decoding of URLs that contain non-ascii characters
* Raise Python exception when response contains objects other than bytestrings
  instead of simply logging the error.

1.0.0 (2021-03-24)
------------------

* Improve query string handling

0.9.2 (2021-01-30)
------------------

* Better support for HTTP 1.1 Expect/Continue
* Improve documentation

0.9.1 (2021-01-13)
------------------

* Improve GIL handling
* Propagate worker thread name to Python logging
* Do not report broken pipe as error
* PasteDeploy entry point: fix option handling

0.9.0 (2021-01-06)
------------------

* Reusable connections
* Chunked transfer-encoding
* Support macOS

0.8.4 (2020-12-12)
------------------

* Lower CPU usage

0.8.3 (2020-11-26)
------------------

* Clean wheel build directories
* Fix some test isolation problems
* Remove a println

0.8.2 (2020-11-17)
------------------

* Fix blocksize handling for sendfile case
* Format unix stream peer address
* Use latest mio

0.8.1 (2020-11-10)
------------------

* Receiver in non-blocking worker must not block when channel is empty

0.8.0 (2020-11-07)
------------------

* Logging overhaul
* New async_logging option
* Some performance improvements
* Support Python 3.9
* Switch to manylinux2010 platform tag

0.7.1 (2020-09-16)
------------------

* Raise Python exception when socket is unavailable
* Add Pyramid configuration example in readme

0.7.0 (2020-08-30)
------------------

* Use Python logging
* Display server info on startup
* Fix socket activation for unix domain sockets

0.6.2 (2020-08-12)
------------------

* Improved logging
* PasteDeploy entry point now also uses at most 24 headers by default

0.6.1 (2020-08-10)
------------------

* Improve request parsing
* Increase default maximum number of headers to 24

0.6.0 (2020-07-29)
------------------

* Support unix domain sockets
* Improve sendfile usage

0.5.3 (2020-07-15)
------------------

* Fix testing for completed sendfile call in case of EAGAIN

0.5.2 (2020-07-15)
------------------

* Fix testing for completed response in case of EAGAIN
* Cargo update

0.5.1 (2020-07-07)
------------------

* Fix handling of read events
* Fix changelog
* Cargo update
* 'Interrupted' error is not a todo
* Remove unused code

0.5.0 (2020-06-07)
------------------

* Add support for systemd socket activation

0.4.0 (2020-06-29)
------------------

* Add a new worker that does nonblocking write
* Add default arguments
* Add option to configure maximum number of request headers
* Add Via header

0.3.0 (2020-06-16)
------------------

* Switch to rust-cpython
* Fix passing of tcp connections to worker threads

0.2.0 (2020-03-10)
------------------

* Added some Python tests (using py.test and tox)
* Improve handling of HTTP headers
* Respect content length header when using sendfile

0.1.0 (2020-02-10)
------------------

* Initial release
